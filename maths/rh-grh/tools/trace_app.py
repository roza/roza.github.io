#!/usr/bin/env python3
"""Graphe des applications instanciées : qui est appliqué à quoi, dans le terme de preuve d'une déclaration.

Usage :
  python3 -I trace_app.py OUT DECL [--callee REGEX] [--types] [--implicit] [--all] [--in-types]
                          [--outline] [--reading] [--slice CALLEE_REGEX:PARAM [--depth N]]
                          [--max-occ N] [--budget N] [--json FICHIER] [--dot FICHIER] [--width N]
Par défaut : applications de théorèmes et de constructeurs (.mk, .intro) du projet (decl2mod.tsv à côté de OUT ;
--lib garde Lean et Mathlib), hors transports, en dehors des types
des lieurs ; --all garde toutes les applications (formations de types, instances), --in-types parcourt aussi
les types des lieurs.

Pour la valeur (terme de preuve ou corps) de DECL, on parcourt le DAG d'expressions et l'on relève chaque
application maximale dont la tête est une constante (une « occurrence »), avec :
  - son contexte : la pile des lieurs (λ, ∀, let, have) traversés pour l'atteindre ;
  - ses arguments, rendus dans ce contexte, alignés sur le télescope du théorème appelé ;
  - la provenance de chaque argument : variable locale (et le lieur qui l'introduit, avec l'occurrence qui la
    définit s'il s'agit d'un let ou d'un have), projection, résultat d'une autre occurrence, constante, fonction ;
  - avec --types, le type attendu de chaque paramètre, instancié par les arguments précédents (substitution
    à l'affichage seulement : aucune vérification de typage ni de convertibilité n'est faite).
Les `have` (letFun v (fun h => b)) et les β-redex ((fun h => b) v) sont traités comme des définitions locales.
Les transports (Eq.mpr, cast, Eq.ndrec…) restent visibles et sont signalés.
Un sous-terme clos partagé n'est parcouru qu'une fois ; ses réapparitions renvoient à la première occurrence.
Limites : niveaux d'univers absents ; identité = même nœud du DAG (le partage de l'export identifie les termes
clos syntaxiquement égaux) ; pas de conversion définitionnelle. Bibliothèque standard seule.
"""
import sys, os, json, re, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lexpr

TRANSPORT = {"Eq.mpr", "Eq.mp", "cast", "Eq.ndrec", "Eq.rec", "Eq.subst", "Eq.symm", "Eq.trans", "congrArg",
             "congrFun", "congr", "HEq.rec", "Eq.recOn", "Eq.casesOn", "id", "of_eq_true", "eq_self", "propext"}
STRUCTURAL = {"letFun"}


class Binder:
    __slots__ = ("name", "kind", "type", "value", "occ")
    def __init__(self, name, kind, type_, value=None, occ=None):
        self.name, self.kind, self.type, self.value, self.occ = name, kind, type_, value, occ


class Tracer:
    def __init__(self, E, budget=2_000_000, width=160, in_types=False):
        self.E, self.budget, self.width, self.in_types = E, budget, width, in_types
        self.occs, self.seen, self.visits, self.truncated = [], {}, 0, False
        self.outline = []   # (profondeur, genre, nom, type, ctx, valeur)

    def names(self, ctx):
        return [b.name for b in ctx]

    def push(self, ctx, nm, kind, ty, value=None, occ=None):
        n = lexpr.fresh(lexpr.clean(nm), self.names(ctx))
        return ctx + [Binder(n, kind, ty, value, occ)]

    def r(self, e, ctx, maxc=None):
        return self.E.render(e, self.names(ctx), maxc or self.width)

    def strip(self, e):
        while self.E.KIND(e) == 8:
            e = self.E.C1[e]
        return e

    # --- parcours
    def walk(self, e, ctx, parent=None, pos=None):
        """Parcourt e ; renvoie l'id d'occurrence si e est une application maximale à tête constante."""
        E = self.E
        self.visits += 1
        if self.visits > self.budget:
            self.truncated = True; return None
        e = self.strip(e)
        k = E.KIND(e)
        if k == 3:
            h, args = E.spine(e)
            h = self.strip(h); hk = E.KIND(h)
            if hk == 2:
                hn = E.cname(h)
                if hn == "letFun" and len(args) >= 4 and E.KIND(self.strip(args[3])) == 4:
                    lam = self.strip(args[3])
                    v = self.walk(args[2], ctx, parent, "have")
                    self.outline.append((len(ctx), "have", E.name(E.PAY(lam)), E.C1[lam], ctx, args[2]))
                    ctx2 = self.push(ctx, E.name(E.PAY(lam)), "have", E.C1[lam], args[2], v)
                    out = self.walk(E.C2[lam], ctx2, parent, pos)
                    for a in args[4:]:
                        self.walk(a, ctx)
                    return out
                key = (e, len(ctx)) if E.lbr(e) > 0 else e
                if key in self.seen:
                    return self.seen[key]
                oid = len(self.occs)
                occ = {"id": oid, "callee": hn, "depth": len(ctx), "parent": parent, "pos": pos,
                       "binders": [b.name for b in ctx[-6:]], "args": [], "transport": hn in TRANSPORT,
                       "expr": e, "_ctx": ctx}
                self.occs.append(occ); self.seen[key] = oid
                for i, a in enumerate(args):
                    sub = self.walk(a, ctx, oid, i)
                    occ["args"].append((a, sub))
                return oid
            if hk == 4 and args:  # β-redex : (fun x => b) v …
                v = self.walk(args[0], ctx, parent, "β")
                self.outline.append((len(ctx), "have", E.name(E.PAY(h)), E.C1[h], ctx, args[0]))
                ctx2 = self.push(ctx, E.name(E.PAY(h)), "have", E.C1[h], args[0], v)
                out = self.walk(E.C2[h], ctx2, parent, pos)
                for a in args[1:]:
                    self.walk(a, ctx)
                return out
            if hk in (0, 7):  # tête locale (variable liée ou projection) : occurrence « locale »
                key = (e, len(ctx))
                if key in self.seen:
                    return self.seen[key]
                oid = len(self.occs)
                occ = {"id": oid, "callee": "⟨" + self.r(h, ctx, 60) + "⟩", "local_head": True, "depth": len(ctx),
                       "parent": parent, "pos": pos, "binders": [b.name for b in ctx[-6:]], "args": [],
                       "transport": False, "expr": e, "_ctx": ctx, "_params": self.local_params(h, ctx)}
                self.occs.append(occ); self.seen[key] = oid
                for i, a in enumerate(args):
                    occ["args"].append((a, self.walk(a, ctx, oid, i)))
                return oid
            self.walk(h, ctx)
            for a in args:
                self.walk(a, ctx)
            return None
        if k in (4, 5):
            if self.in_types:
                self.walk(E.C1[e], ctx)
            return self.walk(E.C2[e], self.push(ctx, E.name(E.PAY(e)), "λ" if k == 4 else "∀", E.C1[e]), parent, pos)
        if k == 6:
            v = self.walk(E.C1[e], ctx, parent, "let")
            self.outline.append((len(ctx), "let", E.name(E.PAY(e)), E.lets.get(e), ctx, E.C1[e]))
            return self.walk(E.C2[e], self.push(ctx, E.name(E.PAY(e)), "let", E.lets.get(e), E.C1[e], v), parent, pos)
        if k == 7:
            self.walk(E.C1[e], ctx)
        return None

    def local_params(self, h, ctx):
        """Noms des paramètres d'une tête locale, lus sur le type de la variable (déplié une fois si c'est
        une définition appliquée). Indicatif : aucune substitution n'est faite."""
        E = self.E; h = self.strip(h)
        if E.KIND(h) != 0 or E.PAY(h) >= len(ctx):
            return []
        t = ctx[-1 - E.PAY(h)].type
        if t is None:
            return []
        t = self.strip(t)
        if E.KIND(t) == 3:
            hd, ar = E.spine(t); hd = self.strip(hd)
            if E.KIND(hd) == 2:
                v = E.vroot.get(E.byname.get(E.cname(hd)), -1)
                if v >= 0:
                    t = v
                    for _ in ar:
                        if E.KIND(t) == 4: t = E.C2[t]
        out = []
        while E.KIND(t) == 5:
            out.append((lexpr.clean(E.name(E.PAY(t))), E.BI(t), None)); t = E.C2[t]
        return out

    def justification(self, v, ctx):
        """Lemme principal qui justifie une valeur : tête de l'application (en traversant transports et id)."""
        E = self.E
        for _ in range(8):
            v = self.strip(v); k = E.KIND(v)
            if k == 4:
                v = E.C2[v]; continue
            if k == 3:
                h, args = E.spine(v); h = self.strip(h)
                if E.KIND(h) == 2:
                    hn = E.cname(h)
                    if hn in TRANSPORT and args:
                        v = args[-1]; continue
                    return hn
                if E.KIND(h) == 0:
                    return "locale " + self.r(h, ctx, 40)
                return "?"
            if k == 0:
                return "locale " + self.r(v, ctx, 40)
            if k == 2:
                return E.cname(v)
            return "?"
        return "?"

    # --- tranchage arrière
    def slice(self, e, ctx, depth, maxdepth, seen, out, indent=1):
        """Provenance récursive d'une expression : variables -> lieur (et valeur si let/have),
        applications -> tête et arguments explicites, projections -> structure. Lecture seule."""
        E = self.E; pad = "  " * indent
        e = self.strip(e); k = E.KIND(e)
        if depth > maxdepth:
            out.append(pad + "… (profondeur maximale)"); return
        if k == 0:
            i = E.PAY(e)
            if i >= len(ctx):
                out.append(pad + f"#{i} (hors contexte)"); return
            b = ctx[-1 - i]; bctx = ctx[:len(ctx) - 1 - i]
            ty = self.r(b.type, bctx) if b.type is not None else "?"
            if b.value is not None and b.kind in ("let", "have"):
                key = ("b", len(bctx), b.name)
                if key in seen:
                    out.append(pad + f"{b.name} ({b.kind}, déjà tranché)"); return
                seen.add(key)
                out.append(pad + f"{b.name} : {ty}   [{b.kind}] ⟸ {self.justification(b.value, bctx)}")
                self.slice(b.value, bctx, depth + 1, maxdepth, seen, out, indent + 1)
            else:
                out.append(pad + f"{b.name} : {ty}   [frontière : lieur {b.kind} de la déclaration]")
            return
        if k == 7:
            out.append(pad + f"projection {E.name(E.C2[e] & ~lexpr.CB)}.{E.PAY(e) + 1} de :")
            self.slice(E.C1[e], ctx, depth + 1, maxdepth, seen, out, indent + 1); return
        if k == 3:
            h, args = E.spine(e); h = self.strip(h)
            if E.KIND(h) == 2:
                cn = E.C1[h] & ~lexpr.CB; hn = E.cname(h)
                tel, _ = E.telescope_full(cn)
                out.append(pad + f"application de {hn}")
                for i, a in enumerate(args):
                    nm, bi, _ = tel[i] if i < len(tel) else (f"x{i}", 0, None)
                    if bi != 0: continue
                    if E.lbr(a) == 0 and E.KIND(self.strip(a)) == 2:
                        out.append(pad + f"  ({nm}) := constante {E.cname(self.strip(a))}"); continue
                    out.append(pad + f"  ({nm}) := {self.r(a, ctx, 120)}")
                    if E.lbr(a) > 0:
                        self.slice(a, ctx, depth + 1, maxdepth, seen, out, indent + 2)
                return
            out.append(pad + f"application de tête locale {self.r(h, ctx, 60)}")
            self.slice(h, ctx, depth + 1, maxdepth, seen, out, indent + 1)
            for a in args:
                if E.lbr(a) > 0: self.slice(a, ctx, depth + 1, maxdepth, seen, out, indent + 1)
            return
        if k == 4:
            out.append(pad + "fonction (λ) : corps")
            self.slice(E.C2[e], self.push(ctx, E.name(E.PAY(e)), "λ", E.C1[e]), depth + 1, maxdepth, seen, out, indent + 1); return
        out.append(pad + self.r(e, ctx, 120))

    # --- provenance
    def prov(self, a, sub, ctx):
        E = self.E; a = self.strip(a); k = E.KIND(a)
        if sub is not None:
            return {"kind": "occurrence", "occ": sub, "callee": self.occs[sub]["callee"]}
        if k == 0:
            i = E.PAY(a)
            if i < len(ctx):
                b = ctx[-1 - i]
                d = {"kind": "locale", "binder": b.name, "binder_kind": b.kind}
                if b.occ is not None:
                    d["defined_by"] = b.occ
                return d
            return {"kind": "locale", "binder": f"#{i}"}
        if k == 2:
            return {"kind": "constante", "name": E.cname(a)}
        if k == 7:
            s = self.strip(E.C1[a])
            return {"kind": "projection", "struct": E.name(E.C2[a] & ~lexpr.CB), "idx": E.PAY(a) + 1,
                    "of": self.prov(s, None, ctx)}
        if k == 3:
            h, args = E.spine(a); h = self.strip(h)
            if E.KIND(h) == 0:
                return {"kind": "application d'une locale", "head": self.prov(h, None, ctx)}
            return {"kind": "application", "head_kind": E.KIND(h)}
        if k == 4:
            return {"kind": "fonction (λ)"}
        if k in (9, 10, 1):
            return {"kind": "valeur"}
        return {"kind": f"genre {k}"}

    def prov_str(self, p):
        k = p["kind"]
        if k == "occurrence": return f"← #{p['occ']} {p['callee']}"
        if k == "locale":
            s = f"locale {p['binder']} ({p.get('binder_kind', '?')})"
            return s + (f", définie par #{p['defined_by']}" if "defined_by" in p else "")
        if k == "constante": return f"constante {p['name']}"
        if k == "projection": return f"projection {p['struct']}.{p['idx']} de [{self.prov_str(p['of'])}]"
        if k == "application d'une locale": return f"application de [{self.prov_str(p['head'])}]"
        return k

    # --- types instanciés (substitution à l'affichage)
    def formal(self, occ, implicit):
        E = self.E
        cn = E.C1[occ["expr"] if E.KIND(occ["expr"]) != 3 else E.spine(occ["expr"])[0]] & ~lexpr.CB
        tel, body = E.telescope_full(cn)
        return tel, body

    def report(self, occ, show_types, implicit):
        E = self.E; ctx = occ["_ctx"]
        if occ.get("local_head"):
            tel, body = occ["_params"], None
        else:
            h, _ = E.spine(occ["expr"]); cn = E.C1[self.strip(h)] & ~lexpr.CB
            tel, body = E.telescope_full(cn)
        rendered = [self.r(a, ctx) for a, _ in occ["args"]]
        lines = []
        hdr = f"#{occ['id']}  {occ['callee']}"
        if occ["transport"]: hdr += "   [transport]"
        if occ["parent"] is not None: hdr += f"   (argument {occ['pos']} de #{occ['parent']})"
        elif occ["pos"] in ("have", "let", "β"): hdr += f"   (valeur d'un {occ['pos']})"
        lines.append(hdr)
        if occ["binders"]:
            lines.append(f"    contexte : … {', '.join(occ['binders'])}  (profondeur {occ['depth']})")
        rec_args = []
        for i, (a, sub) in enumerate(occ["args"]):
            nm, bi, ty = tel[i] if i < len(tel) else (f"x{i}", 0, None)
            p = self.prov(a, sub, ctx)
            rec_args.append({"i": i, "param": nm, "binder_info": bi, "arg": rendered[i], "prov": p,
                             "expr_id": int(self.strip(a)), "closed": E.lbr(a) == 0})
            if bi != 0 and not implicit:
                continue
            br = {0: "()", 1: "{}", 2: "⦃⦄", 3: "[]"}[bi]
            line = f"    {br[0]}{nm}{br[1]} := {rendered[i]}"
            lines.append(line + "   ⟵ " + self.prov_str(p))
            if show_types and ty is not None:
                sub_ctx = [("(" + x + ")" if " " in x else x) for x in rendered[:i]]
                lines.append(f"        : {E.render(ty, sub_ctx, self.width)}")
        if show_types and body is not None:
            n = len(occ["args"])
            if n >= len(tel):
                sub_ctx = [("(" + x + ")" if " " in x else x) for x in rendered[:len(tel)]]
                lines.append(f"    ⊢ {E.render(body, sub_ctx, self.width)}")
        rec = {k: v for k, v in occ.items() if not k.startswith("_") and k not in ("expr", "args")}
        rec["args"] = rec_args; rec["expr_id"] = int(occ["expr"])
        return "\n".join(lines), rec


def dot_graph(tr, sel, recs, path):
    """Graphe biparti : occurrences (boîtes) et objets locaux (ellipses)."""
    esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
    o = ['digraph G {', ' graph [rankdir=LR, fontname="DejaVu Sans", nodesep=0.2, ranksep=0.4];',
         ' node [fontname="DejaVu Sans", fontsize=9];', ' edge [fontname="DejaVu Sans", fontsize=8, color="#555555"];']
    locs = set()
    for r in recs:
        o.append(f' o{r["id"]} [shape=box, style="rounded,filled", fillcolor="#fde8d0", label="#{r["id"]} {esc(r["callee"])}"];')
    ids = {r["id"] for r in recs}
    for r in recs:
        for a in r["args"]:
            if a["binder_info"] != 0:
                continue
            p = a["prov"]
            if p["kind"] == "occurrence" and p["occ"] in ids:
                o.append(f' o{p["occ"]} -> o{r["id"]} [label="{esc(a["param"])}"];')
            elif p["kind"] == "locale":
                key = "L_" + re.sub(r"\W", "_", p["binder"])
                if key not in locs:
                    locs.add(key)
                    o.append(f' {key} [shape=ellipse, style=filled, fillcolor="#e8eefa", label="{esc(p["binder"])}"];')
                o.append(f' {key} -> o{r["id"]} [label="{esc(a["param"])}"];')
            elif p["kind"] == "projection":
                key = "P_%d" % a["expr_id"]
                if key not in locs:
                    locs.add(key)
                    o.append(f' {key} [shape=ellipse, style=filled, fillcolor="#e5f4ee", label="{esc(a["arg"][:60])}"];')
                o.append(f' {key} -> o{r["id"]} [label="{esc(a["param"])}"];')
    o.append("}")
    open(path, "w", encoding="utf-8").write("\n".join(o) + "\n")


def main():
    args = sys.argv[1:]
    def opt(k, d=None, typ=str):
        if k in args:
            i = args.index(k); v = typ(args[i + 1]); del args[i:i + 2]; return v
        return d
    callee = opt("--callee"); maxocc = opt("--max-occ", 200, int); budget = opt("--budget", 2_000_000, int)
    jpath = opt("--json"); dpath = opt("--dot"); width = opt("--width", 160, int)
    show_types = "--types" in args; implicit = "--implicit" in args
    keep_all = "--all" in args; in_types = "--in-types" in args; with_lib = "--lib" in args
    outline = "--outline" in args; reading = "--reading" in args
    slice_spec = opt("--slice"); slice_depth = opt("--depth", 6, int)
    args = [a for a in args if not a.startswith("--")]
    OUT, decl = args[0], args[1]
    E = lexpr.load(OUT)
    d2m = os.path.join(os.path.dirname(os.path.abspath(OUT)), "decl2mod.tsv")
    origin, projns, libns = {}, set(), set()
    if not with_lib and os.path.exists(d2m):
        for l in open(d2m, encoding="utf-8", errors="replace"):
            p = l.split("\t")
            if len(p) > 1:
                origin[p[0]] = p[1]
                (projns if p[1] == "projet" else libns).add(p[0].split(".", 1)[0])
        projns -= {"Mathlib", "KStar", "_private"}

    def is_lib(n):
        """Origine d'une constante : decl2mod.tsv si elle y figure ; sinon, par son espace de noms de tête."""
        if with_lib or not origin:
            return False
        o = origin.get(n)
        if o is not None:
            return o != "projet"
        if n.startswith("_private."):
            return not any(f".{x}." in n for x in projns)
        if "." not in n:
            return True
        c = n.split(".", 1)[0]
        return c not in projns and (c in libns or c in ("Mathlib", "Lean", "Std", "Batteries", "Init"))
    n = E.byname.get(decl)
    if n is None:
        sys.exit(f"{decl} : inconnu dans l'export")
    v = E.vroot.get(n, -1)
    if v < 0:
        sys.exit(f"{decl} : pas de valeur (membre d'inductif ou axiome)")
    for _ in range(8):   # une valeur qui n'est qu'une constante : on suit l'alias
        vv = v
        while E.KIND(vv) == 8:
            vv = E.C1[vv]
        if E.KIND(vv) != 2:
            break
        alias = E.cname(vv)
        print(f"(la valeur de {decl} est la constante {alias} : on suit l'alias)")
        decl = alias; n = E.byname.get(alias); v = E.vroot.get(n, -1)
        if v < 0:
            sys.exit(f"{alias} : pas de valeur")
    tr = Tracer(E, budget, width, in_types)
    print(f"### {decl}  [{E.kindof.get(n)}]")
    print("type :", E.render(E.troot[n], [], 800))
    tr.walk(v, [])
    if outline:
        print("Squelette : étapes intermédiaires (have/let), avec leur énoncé et le lemme qui les justifie.\n")
        for d, kind, nm, ty, ctx, val in tr.outline:
            if lexpr.clean(nm).startswith(("inst", "this_inst")):
                continue
            tys = E.render(ty, tr.names(ctx), width) if ty is not None else "?"
            if tys.startswith(("Decidable", "Fintype", "DecidableEq", "Nonempty", "Inhabited")):
                continue
            print(f"{'  ' * min(d // 4, 10)}{kind} {lexpr.clean(nm)} : {tys}")
            print(f"{'  ' * min(d // 4, 10)}    ⟸ {tr.justification(val, ctx)}")
        print()
    if reading:
        import gzip
        dom = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis", "decl_domtree.tsv.gz")
        idom, own, bynm = {}, {}, {}
        for l in gzip.open(dom, "rt", encoding="utf-8"):
            q = l.rstrip("\n").split("\t")
            if q[0] == "d": continue
            idom[q[0]] = q[1]; own[q[0]] = int(q[6]); bynm[q[3]] = q[0]
        me = bynm.get(decl)
        def under(d):
            for _ in range(400):
                if d == me: return True
                d = idom.get(d)
                if d is None or d == "ROOT": return False
            return False
        callees = sorted({o["callee"] for o in tr.occs if not o.get("local_head")})
        inner, outer = [], []
        for c in callees:
            d = bynm.get(c)
            if d is None or is_lib(c): continue
            (inner if under(d) else outer).append((own.get(d, 0), c))
        print(f"Liste de lecture pour {decl} (poids dominé propre : {own.get(me, 0)} lignes)")
        print(f"  à lire en preuve ({len(inner)} lemmes dominés par la cible) :")
        for w, c in sorted(inner, reverse=True)[:40]: print(f"    {w:>9}  {c}")
        print(f"  à lire en énoncé ({len(outer)} lemmes extérieurs) :")
        for w, c in sorted(outer, reverse=True)[:40]: print(f"    {w:>9}  {c}")
        print()
    if slice_spec:
        crx, pname = slice_spec.rsplit(":", 1)
        cre = re.compile(crx); done = 0
        for o in tr.occs:
            if o.get("local_head") or not cre.search(o["callee"]):
                continue
            h, _ = E.spine(o["expr"]); cn = E.C1[tr.strip(h)] & ~lexpr.CB
            tel, _ = E.telescope_full(cn)
            idx = [i for i, (nm, _, _) in enumerate(tel) if nm == pname]
            if not idx or idx[0] >= len(o["args"]):
                continue
            a = o["args"][idx[0]][0]
            print(f"Tranchage de #{o['id']} {o['callee']}, paramètre ({pname}) := {tr.r(a, o['_ctx'], 200)}")
            out = []; tr.slice(a, o["_ctx"], 0, slice_depth, set(), out)
            print("\n".join(out)); print()
            done += 1
            if done >= 3: break
        if not done:
            print(f"aucune occurrence de {crx} avec un paramètre {pname}")
        return
    if outline or reading:
        if not callee:
            return
    rx = re.compile(callee) if callee else None
    def is_proof_step(o):
        if o.get("local_head"):
            return True
        cn = E.byname.get(o["callee"])
        k = E.kindof.get(cn)
        if is_lib(o["callee"]):
            return False
        if o.get("local_head"):
            return True
        return k == "thm" or (k is None and o["callee"].rsplit(".", 1)[-1] in ("mk", "intro"))
    if rx:
        sel = [o for o in tr.occs if rx.search(o["callee"])]
    elif keep_all:
        sel = list(tr.occs)
    else:
        sel = [o for o in tr.occs if is_proof_step(o) and o["callee"] not in TRANSPORT]
    print(f"{len(tr.occs)} occurrences relevées ({tr.visits} nœuds visités{', TRONQUÉ' if tr.truncated else ''}) ; "
          f"{len(sel)} retenues{' pour ' + callee if callee else (' (toutes)' if keep_all else ' (théorèmes et constructeurs, hors transports)')}.\n")
    from collections import Counter
    cnt = Counter(o["callee"] for o in sel)
    if len(cnt) > 1:
        print("têtes les plus appliquées : " + " ; ".join(f"{c}×{k}" for k, c in cnt.most_common(8)) + "\n")
    recs = []
    for o in sel[:maxocc]:
        txt, rec = tr.report(o, show_types, implicit)
        print(txt); print(); recs.append(rec)
    if len(sel) > maxocc:
        print(f"… {len(sel) - maxocc} occurrences non affichées (--max-occ).")
    if jpath:
        with open(jpath, "w", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps({"decl": decl, **r}, ensure_ascii=False) + "\n")
    if dpath:
        dot_graph(tr, sel, recs, dpath)


if __name__ == "__main__":
    sys.setrecursionlimit(2_000_000)
    threading.stack_size(1024 * 1024 * 1024)
    t = threading.Thread(target=main); t.start(); t.join()
