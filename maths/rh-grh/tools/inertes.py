#!/usr/bin/env python3
"""Clauses inertes : composantes de conjonctions démontrées mais jamais extraites.

Pour chaque théorème T du projet, dans la fermeture de RH, dont l'énoncé (après ∀ et ∃) est une
conjonction A₀ ∧ (A₁ ∧ … ∧ Aₙ₋₁), on suit la preuve de T dans la valeur de chacun de ses référents
de la fermeture, et l'on note les chemins (suites L/R de projections) effectivement consommés.

Flot suivi : And.left/right, projections .1/.2, And.casesOn/rec/elim, Exists.casesOn/rec/elim,
Exists.choose_spec, Exists.intro, And.intro (reconditionnement), let, have (letFun), β-redex,
λ et application à des arguments (transparents). Un passage en argument d'une constante du projet
est analysé dans la valeur de cette constante (paramètre correspondant, récursivement) ; tout
autre usage compte comme consommation entière (conservatif). Au-delà du budget : « non résolu ».

Une composante est INERTE si aucun chemin consommé ne la touche, dans aucun référent, et si tous
les référents sont résolus. Conclusion négative, donc établie seulement dans ce cas.

Usage : inertes.py OUT [--min-n 2] [--budget 3000000] [--only NOM] [--from INERTES.tsv] > analysis/inertes.tsv
(--from : ne réexamine que les théorèmes marqués « inerte » dans un résultat antérieur.)
"""
import sys, os, gzip, time
from array import array
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lexpr

sys.setrecursionlimit(1_000_000)


class Unresolved(Exception):
    pass


class H:  # poignée : sous-formule au chemin p de la racine suivie
    __slots__ = ("p",)
    def __init__(self, p): self.p = p


class C:  # conjonction reconstruite (And.intro)
    __slots__ = ("a", "b")
    def __init__(self, a, b): self.a, self.b = a, b


def proj(av, d):
    if av is None: return None
    if isinstance(av, H): return H(av.p + (d,))
    return av.a if d == "L" else av.b


def main():
    args = sys.argv[1:]
    def opt(k, dflt, f=str):
        if k in args:
            i = args.index(k); v = f(args[i + 1]); del args[i:i + 2]; return v
        return dflt
    min_n = opt("--min-n", 2, int); BUDGET = opt("--budget", 3_000_000, int); only = opt("--only", None); fromf = opt("--from", None)
    only_set = {l.split("\t")[2] for l in open(fromf) if l.startswith("inerte")} if fromf else None
    OUT = args[0]; P = lambda f: os.path.join(OUT, f)
    E = lexpr.load(OUT)
    t0 = time.time()

    # fermeture et poids
    dom = {}
    # domtree.tsv de OUT s'il existe (autre export), sinon la copie compressée de l'original
    _dt = os.path.join(OUT, "domtree.tsv")
    with (open(_dt, encoding="utf-8") if os.path.exists(_dt) else
          gzip.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis", "decl_domtree.tsv.gz"), "rt", encoding="utf-8")) as f:
        f.readline()
        for l in f:
            p = l.rstrip("\n").split("\t"); dom[p[3]] = (int(p[0]), p[2], int(p[6]))
    # décl <-> noms ; index inverse
    owner, dname = {}, {}
    for l in open(P("members.tsv")):
        d, n, _ = l.split("\t"); owner[int(n)] = int(d)
    for l in open(P("decls.tsv")):
        p = l.split("\t", 3); dname[int(p[0])] = int(p[2])
    off = array("Q"); off.frombytes(open(P("rev_off.u64"), "rb").read())
    rev = array("I"); rev.frombytes(open(P("rev.u32"), "rb").read())
    # origine projet / bibliothèque (même règle que trace_app.py)
    origin, projns, libns = {}, set(), set()
    d2m = os.path.join(os.path.dirname(os.path.abspath(OUT)), "decl2mod.tsv")
    for l in open(d2m, encoding="utf-8", errors="replace"):
        p = l.split("\t")
        if len(p) > 1:
            origin[p[0]] = p[1]; (projns if p[1] == "projet" else libns).add(p[0].split(".", 1)[0])
    projns -= {"Mathlib", "KStar", "_private"}
    def is_lib(n):
        o = origin.get(n)
        if o is not None: return o != "projet"
        if n.startswith("_private."): return not any(f".{x}." in n for x in projns)
        if "." not in n: return True
        c = n.split(".", 1)[0]
        return c not in projns and (c in libns or c in ("Mathlib", "Lean", "Std", "Batteries", "Init"))

    KIND, C1, C2, PAY, spine = E.KIND, E.C1, E.C2, E.PAY, E.spine
    CB = lexpr.CB
    def cid(e): return C1[e] & ~CB

    def strip(t):
        """Retire ∀ et ∃ ; renvoie la liste des composantes de la chaîne de ∧."""
        while True:
            k = KIND(t)
            if k == 5: t = C2[t]; continue
            if k == 8: t = C1[t]; continue
            if k == 3:
                h, a = spine(t)
                if KIND(h) == 2:
                    n = E.cname(h)
                    if n == "Exists" and len(a) == 2 and KIND(a[1]) == 4: t = C2[a[1]]; continue
                    if n == "And" and len(a) == 2:
                        comps = [a[0]]; t = a[1]
                        while True:
                            while KIND(t) == 8: t = C1[t]
                            if KIND(t) == 3:
                                h2, a2 = spine(t)
                                if KIND(h2) == 2 and E.cname(h2) == "And" and len(a2) == 2:
                                    comps.append(a2[0]); t = a2[1]; continue
                            comps.append(t); return comps
            return []

    def head_name(e):
        while KIND(e) in (5, 8, 4):
            e = C2[e] if KIND(e) in (4, 5) else C1[e]
        h, _ = spine(e) if KIND(e) == 3 else (e, [])
        return E.cname(h) if KIND(h) == 2 else E.render(e, maxc=60)

    # ---------- analyse de flot
    param_memo, in_prog = {}, set()

    class Ctx:
        def __init__(self, target):
            self.target = target; self.used = set(); self.steps = 0; self.tmemo = {}

        def hasT(self, e):
            if self.target is None: return False
            r = self.tmemo.get(e)
            if r is not None: return r
            k = KIND(e)
            if k == 2: r = cid(e) == self.target
            elif k == 3 or k in (4, 5): r = self.hasT(C1[e]) or self.hasT(C2[e])
            elif k == 6: r = self.hasT(C1[e]) or self.hasT(C2[e])
            elif k in (7, 8): r = self.hasT(C1[e])
            else: r = False
            self.tmemo[e] = r; return r

        def relevant(self, e, env):
            if self.hasT(e): return True
            lb = E.lbr(e)
            if lb == 0: return False
            n = len(env)
            for i in range(min(lb, n)):
                if env[n - 1 - i] is not None and E.has_bvar(e, i): return True
            return False

        def use(self, av, p=()):
            if av is None: return
            if isinstance(av, H): self.used.add(av.p + p); return
            if not p: self.use(av.a); self.use(av.b); return
            self.use(av.a if p[0] == "L" else av.b, p[1:])

        def escape(self, fn, i, av, depth):
            if fn is None or is_lib(E.name(fn)) or E.vroot.get(fn, -1) < 0 or depth > 8:
                self.use(av); return
            for p in param_used(fn, i, depth + 1): self.use(av, p)

        def lams(self, f, env, avs, depth):
            """Applique f (λ attendue) aux valeurs abstraites avs."""
            env = list(env); k = 0
            while k < len(avs) and KIND(f) == 4:
                env.append(avs[k]); f = C2[f]; k += 1
            if k < len(avs):   # forme η-réduite : f appliquée aux restants
                h, a = spine(f) if KIND(f) == 3 else (f, [])
                if KIND(h) == 2:
                    for j, av in enumerate(avs[k:]):
                        if av is not None: self.escape(cid(h), len(a) + j, av, depth)
                else:
                    for av in avs[k:]: self.use(av)
                # le résultat de f appliquée aux restants est celui de la visite de f (correctif du 26/11 :
                # il était jeté, ce qui perdait la conclusion d'un théorème passé à And.elim, Exists.elim…)
                return self.visit(f, env, depth)
            return self.visit(f, env, depth)

        def visit(self, e, env, depth):
            self.steps += 1
            if self.steps > BUDGET: raise Unresolved
            if not self.relevant(e, env): return None
            k = KIND(e)
            if k == 0: return env[len(env) - 1 - PAY(e)]
            if k == 2: return H(()) if cid(e) == self.target else None
            if k == 8: return self.visit(C1[e], env, depth)
            if k == 7:
                av = self.visit(C1[e], env, depth)
                if av is None: return None
                if PAY(e) in (0, 1): return proj(av, "L" if PAY(e) == 0 else "R")
                self.use(av); return None
            if k == 4: return self.visit(C2[e], env + [None], depth)
            if k == 5: return None
            if k == 6:
                av = self.visit(C1[e], env, depth)
                return self.visit(C2[e], env + [av], depth)
            if k != 3: return None
            h, a = spine(e); hk = KIND(h)
            if hk == 2:
                n = E.cname(h); L = len(a)
                def rest(i0):
                    for x in a[i0:]: self.use(self.visit(x, env, depth))
                if n in ("And.left", "And.right") and L >= 3:
                    av = proj(self.visit(a[2], env, depth), "L" if n == "And.left" else "R"); rest(3)
                    return av if L == 3 else (self.use(av) or None)
                if n == "And.intro" and L == 4:
                    x, y = self.visit(a[2], env, depth), self.visit(a[3], env, depth)
                    return C(x, y) if (x is not None or y is not None) else None
                if n == "And.casesOn" and L >= 5:
                    t = self.visit(a[3], env, depth); r = self.lams(a[4], env, [proj(t, "L"), proj(t, "R")], depth); rest(5); return r   # arguments en plus : la preuve d'un énoncé universel, appliquée, garde ses composantes
                if n == "And.rec" and L >= 5:
                    t = self.visit(a[4], env, depth); r = self.lams(a[3], env, [proj(t, "L"), proj(t, "R")], depth); rest(5); return r   # arguments en plus : la preuve d'un énoncé universel, appliquée, garde ses composantes
                if n == "And.elim" and L >= 5:
                    t = self.visit(a[4], env, depth); r = self.lams(a[3], env, [proj(t, "L"), proj(t, "R")], depth); rest(5); return r   # arguments en plus : la preuve d'un énoncé universel, appliquée, garde ses composantes
                if n == "Exists.casesOn" and L >= 5:
                    t = self.visit(a[3], env, depth); r = self.lams(a[4], env, [None, t], depth); rest(5); return r   # arguments en plus : la preuve d'un énoncé universel, appliquée, garde ses composantes
                if n == "Exists.rec" and L >= 5:
                    t = self.visit(a[4], env, depth); r = self.lams(a[3], env, [None, t], depth); rest(5); return r   # arguments en plus : la preuve d'un énoncé universel, appliquée, garde ses composantes
                if n == "Exists.elim" and L >= 5:
                    t = self.visit(a[3], env, depth); r = self.lams(a[4], env, [None, t], depth); rest(5); return r   # arguments en plus : la preuve d'un énoncé universel, appliquée, garde ses composantes
                if n == "Exists.choose_spec" and L >= 3:
                    t = self.visit(a[2], env, depth); rest(3); return t if L == 3 else (self.use(t) or None)
                if n == "Exists.choose" and L >= 3:
                    self.visit(a[2], env, depth); rest(3); return None
                if n == "Exists.intro" and L == 4:
                    self.visit(a[2], env, depth); return self.visit(a[3], env, depth)
                if n == "letFun" and L >= 4:
                    av = self.visit(a[2], env, depth); r = self.lams(a[3], env, [av], depth); rest(4); return r
                fn = cid(h)
                if fn == self.target:   # T appliquée à ses arguments
                    for x in a: self.use(self.visit(x, env, depth))
                    return H(())
                for i, x in enumerate(a):
                    av = self.visit(x, env, depth)
                    if av is not None: self.escape(fn, i, av, depth)
                return None
            if hk == 4:   # β-redex
                return self.lams(h, env, [self.visit(x, env, depth) for x in a], depth)
            hv = self.visit(h, env, depth)
            for x in a: self.use(self.visit(x, env, depth))
            return hv

    def param_used(fn, i, depth):
        key = (fn, i)
        r = param_memo.get(key)
        if r is not None: return r
        if key in in_prog: return {()}
        in_prog.add(key)
        v = E.vroot.get(fn, -1); env = []; k = 0
        while k <= i and v >= 0 and KIND(v) == 4:
            env.append(H(()) if k == i else None); v = C2[v]; k += 1
        if k <= i:
            r = {()}
        else:
            cx = Ctx(None)
            try:
                cx.use(cx.visit(v, env, depth))
                r = cx.used
            except (Unresolved, RecursionError):
                r = {()}
        in_prog.discard(key); param_memo[key] = r
        return r

    def touches(paths, tgt):
        return any(p[:len(tgt)] == tgt or tgt[:len(p)] == p for p in paths)

    def comp_proofs(T, n):
        """Preuves des composantes dans la valeur de T (si la valeur est un ⟨…⟩ lisible)."""
        v = E.vroot.get(T, -1); out = [None] * n
        def go(e, k):
            while True:
                kk = KIND(e)
                if kk == 4: e = C2[e]; continue
                if kk == 8: e = C1[e]; continue
                if kk == 6: e = C2[e]; continue
                if kk != 3: break
                h, a = spine(e)
                if KIND(h) != 2: break
                nm = E.cname(h)
                if nm == "Exists.intro" and len(a) == 4: e = a[3]; continue
                if nm == "letFun" and len(a) == 4: e = a[3]; continue
                if nm == "And.intro" and len(a) == 4 and k < n - 1:
                    out[k] = a[2]; e = a[3]; k += 1; continue
                break
            if k == n - 1: out[k] = e
        if v >= 0: go(v, 0)
        return out

    def consts_in(e, acc, seen):
        if e in seen or len(seen) > 20000: return
        seen.add(e); k = KIND(e)
        if k == 2: acc.add(cid(e))
        elif k in (3, 4, 5, 6): consts_in(C1[e], acc, seen); consts_in(C2[e], acc, seen)
        elif k in (7, 8): consts_in(C1[e], acc, seen)

    # ---------- candidats
    cands = []
    for name, (d, kind, w) in dom.items():
        if kind != "thm" or is_lib(name) or (only and name != only) or (only_set is not None and name not in only_set): continue
        nid = E.byname.get(name)
        if nid is None: continue
        comps = strip(E.troot.get(nid, -1)) if E.troot.get(nid, -1) >= 0 else []
        if len(comps) >= min_n: cands.append((w, name, nid, comps))
    cands.sort(reverse=True)
    print(f"# candidats : {len(cands)}  ({time.time()-t0:.0f} s)", file=sys.stderr)

    print("statut\tpoids\tthéorème\tn\tréférents\tinertes\tcomposantes inertes (tête)\tpoids mort\tpreuves mortes")
    stats = {"résolu": 0, "non résolu": 0, "inerte": 0, "sans référent": 0}
    for idx, (w, name, T, comps) in enumerate(cands):
        n = len(comps)
        d = owner.get(T)
        refs = [r for r in rev[off[d]:off[d + 1]] if E.names_tsv.get(dname[r]) in dom] if d is not None else []
        if not refs:
            stats["sans référent"] += 1; continue
        cx = Ctx(T); status = "résolu"
        try:
            for r in refs:
                rn = dname[r]; v = E.vroot.get(rn, -1)
                if v < 0: cx.used.add(()); continue
                cx.steps = 0
                cx.use(cx.visit(v, [], 0))
        except (Unresolved, RecursionError):
            status = "non résolu"
        if len(E._hb) > 20_000_000: E._hb.clear()
        stats[status] += 1
        if status != "résolu":
            print(f"{status}\t{w}\t{name}\t{n}\t{len(refs)}\t\t\t\t"); continue
        tg = [("R",) * k + ("L",) if k < n - 1 else ("R",) * (n - 1) for k in range(n)]
        inert = [k for k in range(n) if not touches(cx.used, tg[k])]
        if not inert: continue
        stats["inerte"] += 1
        heads = "; ".join(f"{k}:{head_name(comps[k])}" for k in inert)
        # poids mort : constantes de la preuve des composantes inertes dont T est le seul référent
        pr = comp_proofs(T, n); dead, dw = [], 0
        for k in inert:
            if pr[k] is None: continue
            acc = set(); consts_in(pr[k], acc, set())
            for c in acc:
                cn = E.name(c)
                if cn not in dom or c == T or is_lib(cn): continue
                dc = owner.get(c)
                rs = {dname[x] for x in rev[off[dc]:off[dc + 1]] if E.names_tsv.get(dname[x]) in dom} if dc is not None else set()
                if rs == {T} and dom[cn][1] == "thm":
                    dead.append(cn); dw += dom[cn][2]
        print(f"inerte\t{w}\t{name}\t{n}\t{len(refs)}\t{len(inert)}\t{heads}\t{dw}\t{', '.join(dead[:6])}", flush=True)
        if idx % 200 == 0:
            print(f"# {idx}/{len(cands)} {stats} ({time.time()-t0:.0f} s)", file=sys.stderr, flush=True)
    print(f"# fin : {stats} ({time.time()-t0:.0f} s)", file=sys.stderr)


if __name__ == "__main__":
    import threading
    threading.stack_size(1 << 29)
    t = threading.Thread(target=main); t.start(); t.join()
