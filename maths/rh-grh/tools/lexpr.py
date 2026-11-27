#!/usr/bin/env python3
"""Bibliothèque : lecture du DAG d'expressions produit par deps.c, et impression lisible.

Même format et même imprimeur que show.py (dont le code est repris ici sous forme importable) :
c1.u32, c2.u32, aux.u32 (genre | binderInfo<<4 | charge<<6), lets.bin, levels.tsv, lits.tsv,
names*.{u32,u64,bin}, names.tsv, decls.tsv, members.tsv. Genres : 0 bvar, 1 sort, 2 const, 3 app,
4 lam, 5 forallE, 6 letE, 7 proj, 8 mdata, 9 lit nat, 10 lit str. Bibliothèque standard seule.

Usage :  import lexpr; E = lexpr.load(OUT); E.render(expr, ctx=[...])
"""
import os, mmap

NONE, CB = 0xFFFFFFFF, 0x80000000
INFIX = {"HAdd.hAdd": "+", "HSub.hSub": "-", "HMul.hMul": "*", "HDiv.hDiv": "/", "HPow.hPow": "^", "HSMul.hSMul": "•",
         "Eq": "=", "Ne": "≠", "LE.le": "≤", "LT.lt": "<", "GE.ge": "≥", "GT.gt": ">", "And": "∧", "Or": "∨",
         "Iff": "↔", "HasSubset.Subset": "⊆", "HAppend.hAppend": "++", "Dvd.dvd": "∣", "HMod.hMod": "%",
         "Function.comp": "∘", "Prod": "×", "HasEquiv.Equiv": "≈", "Inter.inter": "∩", "Union.union": "∪"}
BINDERS = {"Exists": "∃", "Set.iUnion": "⋃", "iSup": "⨆", "iInf": "⨅", "Finset.sum": "∑", "Finset.prod": "∏", "tsum": "∑'"}


class TooLong(Exception):
    pass


class Env:
    def __init__(self, OUT, explicit=False):
        def mm(fn):
            f = open(os.path.join(OUT, fn), "rb")
            return mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        self.C1 = memoryview(mm("c1.u32")).cast("I")
        self.C2 = memoryview(mm("c2.u32")).cast("I")
        self.AUX = memoryview(mm("aux.u32")).cast("I")
        self.NPRE = memoryview(mm("names_pre.u32")).cast("I")
        self.NOFF = memoryview(mm("names_off.u64")).cast("Q")
        self.POOL = mm("names_pool.bin")
        self.explicit = explicit
        self._nc, self._lbr, self._hb, self._tele = {}, {}, {}, {}
        self.lets = {}
        mv = memoryview(open(os.path.join(OUT, "lets.bin"), "rb").read()).cast("I")
        for i in range(0, len(mv), 2):
            self.lets[mv[i]] = mv[i + 1]
        self.levels = {}
        for l in open(os.path.join(OUT, "levels.tsv")):
            a = l.rstrip("\n").split("\t"); self.levels[int(a[0])] = (a[1], int(a[2]), int(a[3]))
        self.lits = {}
        for l in open(os.path.join(OUT, "lits.tsv"), encoding="utf-8", errors="replace"):
            a = l.rstrip("\n").split("\t", 2); self.lits[int(a[0])] = (a[1], a[2])
        self.troot, self.vroot, self.kindof, self.names_tsv = {}, {}, {}, {}
        for l in open(os.path.join(OUT, "names.tsv"), encoding="utf-8", errors="replace"):
            i, s = l.rstrip("\n").split("\t", 1); self.names_tsv[int(i)] = s
        for l in open(os.path.join(OUT, "decls.tsv")):
            p = l.split("\t")
            nmid = int(p[2]); self.vroot[nmid] = int(p[7]); self.kindof[nmid] = p[1]
        for l in open(os.path.join(OUT, "members.tsv")):
            d, n, t = l.split("\t"); self.troot[int(n)] = int(t)
        self.byname = {s: i for i, s in self.names_tsv.items()}

    # --- accès de base
    def KIND(self, e): return self.AUX[e] & 15
    def BI(self, e): return (self.AUX[e] >> 4) & 3
    def PAY(self, e): return self.AUX[e] >> 6
    def cname(self, e): return self.name(self.C1[e] & ~CB)

    def name(self, n):
        if n == 0:
            return ""
        r = self._nc.get(n)
        if r is not None:
            return r
        o = self.NOFF[n]; e = self.POOL.find(b"\0", o)
        comp = self.POOL[o:e].decode("utf-8", "replace")
        p = self.NPRE[n]
        r = (self.name(p) + "." + comp) if p else comp
        if len(self._nc) < 2_000_000:
            self._nc[n] = r
        return r

    def level(self, l):
        k = self.levels.get(l)
        if l == 0 or k is None:
            return 0, "0"
        t, a, b = k
        if t == "p":
            return None, self.name(a)
        if t == "s":
            n, s = self.level(a)
            return (n + 1, str(n + 1)) if n is not None else (None, s + "+1")
        return None, f"{'max' if t == 'm' else 'imax'} {self.level(a)[1]} {self.level(b)[1]}"

    def sort_str(self, l):
        n, s = self.level(l)
        if n == 0: return "Prop"
        if n == 1: return "Type"
        if n is not None: return f"Type {n-1}"
        return f"Sort ({s})"

    def lbr(self, e):
        r = self._lbr.get(e)
        if r is not None:
            return r
        k = self.KIND(e); C1, C2 = self.C1, self.C2
        if k == 0: r = self.PAY(e) + 1
        elif k in (1, 2, 9, 10): r = 0
        elif k == 3: r = max(self.lbr(C1[e]), self.lbr(C2[e]))
        elif k in (4, 5): r = max(self.lbr(C1[e]), self.lbr(C2[e]) - 1)
        elif k == 6: r = max(self.lbr(self.lets[e]), self.lbr(C1[e]), self.lbr(C2[e]) - 1)
        elif k in (7, 8): r = self.lbr(C1[e])
        else: r = 0
        self._lbr[e] = r
        return r

    def has_bvar(self, e, i):
        if self.lbr(e) <= i:
            return False
        key = (e, i); r = self._hb.get(key)
        if r is not None:
            return r
        k = self.KIND(e); C1, C2 = self.C1, self.C2
        if k == 0: r = self.PAY(e) == i
        elif k == 3: r = self.has_bvar(C1[e], i) or self.has_bvar(C2[e], i)
        elif k in (4, 5): r = self.has_bvar(C1[e], i) or self.has_bvar(C2[e], i + 1)
        elif k == 6: r = self.has_bvar(self.lets[e], i) or self.has_bvar(C1[e], i) or self.has_bvar(C2[e], i + 1)
        elif k in (7, 8): r = self.has_bvar(C1[e], i)
        else: r = False
        self._hb[key] = r
        return r

    def telescope_full(self, cn):
        """[(nom, binderInfo, type_expr)] du type de la constante cn, et le corps restant."""
        t = self.troot.get(cn); r = []
        while t is not None and t >= 0 and self.KIND(t) == 5:
            r.append((clean(self.name(self.PAY(t))), self.BI(t), self.C1[t])); t = self.C2[t]
        return r, t

    def telescope(self, cn):
        r = self._tele.get(cn)
        if r is None:
            r = [bi for _, bi, _ in self.telescope_full(cn)[0]]; self._tele[cn] = r
        return r

    def spine(self, e):
        a = []
        while self.KIND(e) == 3:
            a.append(self.C2[e]); e = self.C1[e]
        a.reverse()
        return e, a

    # --- impression (reprise de show.py)
    def render(self, e, ctx=(), maxc=6000):
        out = []; budget = [maxc]
        try:
            self.pp(e, list(ctx), out, budget)
        except TooLong:
            out.append(" …[tronqué]")
        return "".join(out)

    def pp(self, e, ctx, out, budget):
        if budget[0] <= 0:
            raise TooLong
        budget[0] -= 1
        k = self.KIND(e); C1, C2 = self.C1, self.C2
        if k == 0:
            i = self.PAY(e); out.append(ctx[-1 - i] if i < len(ctx) else f"#{i}")
        elif k == 1: out.append(self.sort_str(self.PAY(e)))
        elif k == 2: out.append(self.cname(e))
        elif k == 9: out.append(self.lits.get(e, ("n", "?"))[1])
        elif k == 10: out.append('"' + self.lits.get(e, ("s", "?"))[1] + '"')
        elif k == 7:
            self.atom(C1[e], ctx, out, budget); out.append(f".{self.PAY(e)+1}")
        elif k == 8: self.pp(C1[e], ctx, out, budget)
        elif k in (4, 5): self.pp_binder(e, ctx, out, budget)
        elif k == 6:
            n = fresh(clean(self.name(self.PAY(e))), ctx)
            out.append(f"let {n} : "); self.pp(self.lets[e], ctx, out, budget); out.append(" := ")
            self.pp(C1[e], ctx, out, budget); out.append("; "); self.pp(C2[e], ctx + [n], out, budget)
        elif k == 3: self.pp_app(e, ctx, out, budget)
        else: out.append("?")

    def pp_binder(self, e, ctx, out, budget):
        k = self.KIND(e); C1, C2 = self.C1, self.C2
        if k == 5 and not self.has_bvar(C2[e], 0):
            self.atom_arrow(C1[e], ctx, out, budget); out.append(" → "); self.pp(C2[e], ctx + ["_"], out, budget); return
        groups = []; cur = list(ctx)
        while self.KIND(e) == k and not (k == 5 and not self.has_bvar(C2[e], 0)):
            n = fresh(clean(self.name(self.PAY(e))), cur)
            groups.append((n, self.BI(e), C1[e], list(cur))); cur.append(n); e = C2[e]
        out.append("∀ " if k == 5 else "fun ")
        br = {0: "()", 1: "{}", 2: "⦃⦄", 3: "[]"}
        for n, bi, ty, c in groups:
            o, cl = br[bi]; out.append(o)
            if not (bi == 3 and n.startswith("inst")):
                out.append(n + " : ")
            self.pp(ty, c, out, budget); out.append(cl + " ")
        out.append(", " if k == 5 else "=> ")
        self.pp(e, cur, out, budget)

    def is_atomic(self, e):
        k = self.KIND(e)
        if k in (0, 1, 2, 9, 10, 7): return True
        if k == 8: return self.is_atomic(self.C1[e])
        if k == 3:
            h, a = self.spine(e)
            if self.KIND(h) == 2 and self.cname(h) == "OfNat.ofNat" and len(a) == 3: return True
        return False

    def operand(self, e, ctx, out, budget):
        k = self.KIND(e); loose = k in (4, 5, 6)
        if k == 3:
            h, a = self.spine(e)
            hn = self.cname(h) if self.KIND(h) == 2 else None
            loose = hn in INFIX or hn in BINDERS or hn == "Not"
        if loose:
            out.append("("); self.pp(e, ctx, out, budget); out.append(")")
        else:
            self.pp(e, ctx, out, budget)

    def atom(self, e, ctx, out, budget):
        if self.is_atomic(e): self.pp(e, ctx, out, budget)
        else:
            out.append("("); self.pp(e, ctx, out, budget); out.append(")")

    def atom_arrow(self, e, ctx, out, budget):
        k = self.KIND(e); loose = k in (4, 5, 6)
        if k == 3:
            h, a = self.spine(e)
            loose = self.KIND(h) == 2 and self.cname(h) in BINDERS
        if loose:
            out.append("("); self.pp(e, ctx, out, budget); out.append(")")
        else:
            self.pp(e, ctx, out, budget)

    def pp_app(self, e, ctx, out, budget):
        h, args_ = self.spine(e)
        hn = self.cname(h) if self.KIND(h) == 2 else None
        if hn and not self.explicit:
            tel = self.telescope(self.C1[h] & ~CB)
            vis = [a for i, a in enumerate(args_) if i >= len(tel) or tel[i] == 0]
            if hn == "OfNat.ofNat" and len(args_) == 3:
                self.pp(args_[1], ctx, out, budget); return
            if hn in INFIX and len(vis) == 2:
                self.operand(vis[0], ctx, out, budget); out.append(f" {INFIX[hn]} "); self.operand(vis[1], ctx, out, budget); return
            if hn == "Not" and len(vis) == 1:
                out.append("¬"); self.atom(vis[0], ctx, out, budget); return
            if hn == "Neg.neg" and len(vis) == 1:
                out.append("-"); self.atom(vis[0], ctx, out, budget); return
            if hn in BINDERS and vis and self.KIND(vis[-1]) == 4:
                lam = vis[-1]; n = fresh(clean(self.name(self.PAY(lam))), ctx)
                out.append(BINDERS[hn] + " " + n)
                for x in vis[:-1]:
                    out.append(" ∈ "); self.atom(x, ctx, out, budget)
                out.append(", "); self.pp(self.C2[lam], ctx + [n], out, budget); return
            args_ = vis
            if not args_:
                out.append(hn); return
        elif hn:
            out.append("@")
        self.atom(h, ctx, out, budget)
        for a in args_:
            out.append(" "); self.atom(a, ctx, out, budget)


def clean(s):
    i = s.find("._@")
    if i >= 0:
        s = s[:i]
    return s or "x"


def fresh(n, ctx):
    if n not in ctx:
        return n
    i = 1
    while f"{n}{i}" in ctx:
        i += 1
    return f"{n}{i}"


def load(OUT, explicit=False):
    return Env(OUT, explicit)
