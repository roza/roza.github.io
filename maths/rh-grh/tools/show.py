#!/usr/bin/env python3
"""Imprime le type (et éventuellement la valeur) de déclarations, depuis les sorties de deps.c.

Usage :
  python3 -I show.py OUTDIR NOM [NOM ...] [--value] [--max 6000] [--explicit]
  python3 -I show.py OUTDIR --grep REGEX        (liste les noms de déclarations correspondants)
Lecture par mmap : c1.u32, c2.u32, aux.u32 (genre | binderInfo<<4 | charge<<6).
"""
import sys, os, mmap, re, threading

args = sys.argv[1:]
OUT = args.pop(0)
SHOW_VAL = "--value" in args
EXPLICIT = "--explicit" in args
MAXC = 6000
if "--max" in args:
    i = args.index("--max"); MAXC = int(args[i + 1]); del args[i:i + 2]
args = [a for a in args if not a.startswith("--") or a == "--grep"]


def mm(fn):
    f = open(os.path.join(OUT, fn), "rb")
    return mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)


C1 = memoryview(mm("c1.u32")).cast("I")
C2 = memoryview(mm("c2.u32")).cast("I")
AUX = memoryview(mm("aux.u32")).cast("I")
NPRE = memoryview(mm("names_pre.u32")).cast("I")
NOFF = memoryview(mm("names_off.u64")).cast("Q")
POOL = mm("names_pool.bin")
NONE, CB = 0xFFFFFFFF, 0x80000000

_nc = {}


def name(n):
    if n == 0:
        return ""
    r = _nc.get(n)
    if r is not None:
        return r
    o = NOFF[n]
    e = POOL.find(b"\0", o)
    comp = POOL[o:e].decode("utf-8", "replace")
    p = NPRE[n]
    r = (name(p) + "." + comp) if p else comp
    if len(_nc) < 2_000_000:
        _nc[n] = r
    return r


lets = {}
raw = open(os.path.join(OUT, "lets.bin"), "rb").read()
mv = memoryview(raw).cast("I")
for i in range(0, len(mv), 2):
    lets[mv[i]] = mv[i + 1]
levels = {}
for l in open(os.path.join(OUT, "levels.tsv")):
    a = l.rstrip("\n").split("\t"); levels[int(a[0])] = (a[1], int(a[2]), int(a[3]))
lits = {}
for l in open(os.path.join(OUT, "lits.tsv"), encoding="utf-8", errors="replace"):
    a = l.rstrip("\n").split("\t", 2); lits[int(a[0])] = (a[1], a[2])

# nom -> (type_root, value_root) ; pour les membres d'inductifs, value_root = -1
troot, vroot, kindof = {}, {}, {}
names_tsv = {}
for l in open(os.path.join(OUT, "names.tsv"), encoding="utf-8", errors="replace"):
    i, s = l.rstrip("\n").split("\t", 1); names_tsv[int(i)] = s
for l in open(os.path.join(OUT, "decls.tsv")):
    p = l.split("\t")
    nmid = int(p[2]); vroot[nmid] = int(p[7]); kindof[nmid] = p[1]
for l in open(os.path.join(OUT, "members.tsv")):
    d, n, t = l.split("\t"); troot[int(n)] = int(t)
byname = {s: i for i, s in names_tsv.items()}


def level(l):
    k = levels.get(l)
    if l == 0 or k is None:
        return 0, "0"
    t, a, b = k
    if t == "p":
        return None, name(a)
    if t == "s":
        n, s = level(a)
        return (n + 1, str(n + 1)) if n is not None else (None, s + "+1")
    return None, f"{'max' if t == 'm' else 'imax'} {level(a)[1]} {level(b)[1]}"


def sort_str(l):
    n, s = level(l)
    if n == 0:
        return "Prop"
    if n == 1:
        return "Type"
    if n is not None:
        return f"Type {n-1}"
    return f"Sort ({s})"


KIND = lambda e: AUX[e] & 15
BI = lambda e: (AUX[e] >> 4) & 3
PAY = lambda e: AUX[e] >> 6

_lbr = {}


def lbr(e):
    """loose bvar range"""
    r = _lbr.get(e)
    if r is not None:
        return r
    k = KIND(e)
    if k == 0:
        r = PAY(e) + 1
    elif k in (1, 2, 9, 10):
        r = 0
    elif k == 3:
        r = max(lbr(C1[e]), lbr(C2[e]))
    elif k in (4, 5):
        r = max(lbr(C1[e]), lbr(C2[e]) - 1)
    elif k == 6:
        r = max(lbr(lets[e]), lbr(C1[e]), lbr(C2[e]) - 1)
    elif k in (7, 8):
        r = lbr(C1[e])
    else:
        r = 0
    _lbr[e] = r
    return r


_hb = {}


def has_bvar(e, i):
    """e contient-il la variable liée libre d'indice i ?"""
    if lbr(e) <= i:
        return False
    key = (e, i)
    r = _hb.get(key)
    if r is not None:
        return r
    k = KIND(e)
    if k == 0:
        r = PAY(e) == i
    elif k == 3:
        r = has_bvar(C1[e], i) or has_bvar(C2[e], i)
    elif k in (4, 5):
        r = has_bvar(C1[e], i) or has_bvar(C2[e], i + 1)
    elif k == 6:
        r = has_bvar(lets[e], i) or has_bvar(C1[e], i) or has_bvar(C2[e], i + 1)
    elif k in (7, 8):
        r = has_bvar(C1[e], i)
    else:
        r = False
    _hb[key] = r
    return r


_tele = {}


def telescope(cn):
    """binderInfos du type de la constante cn"""
    r = _tele.get(cn)
    if r is not None:
        return r
    t = troot.get(cn)
    r = []
    while t is not None and t >= 0 and KIND(t) == 5:
        r.append(BI(t)); t = C2[t]
    _tele[cn] = r
    return r


def clean(s):
    i = s.find("._@")
    if i >= 0:
        s = s[:i]
    return s or "x"


INFIX = {"HAdd.hAdd": "+", "HSub.hSub": "-", "HMul.hMul": "*", "HDiv.hDiv": "/", "HPow.hPow": "^", "HSMul.hSMul": "•",
         "Eq": "=", "Ne": "≠", "LE.le": "≤", "LT.lt": "<", "GE.ge": "≥", "GT.gt": ">", "And": "∧", "Or": "∨",
         "Iff": "↔", "HasSubset.Subset": "⊆", "HAppend.hAppend": "++", "Dvd.dvd": "∣", "HMod.hMod": "%",
         "Function.comp": "∘", "Prod": "×", "HasEquiv.Equiv": "≈", "Inter.inter": "∩", "Union.union": "∪"}
BINDERS = {"Exists": "∃", "Set.iUnion": "⋃", "iSup": "⨆", "iInf": "⨅", "Finset.sum": "∑", "Finset.prod": "∏", "tsum": "∑'"}


class TooLong(Exception):
    pass


def pp(e, ctx, out, budget):
    """ctx : liste des noms de lieurs (le plus interne en dernier)."""
    if budget[0] <= 0:
        raise TooLong
    budget[0] -= 1
    k = KIND(e)
    if k == 0:
        i = PAY(e); out.append(ctx[-1 - i] if i < len(ctx) else f"#{i}")
    elif k == 1:
        out.append(sort_str(PAY(e)))
    elif k == 2:
        out.append(name(C1[e] & ~CB))
    elif k == 9:
        out.append(lits.get(e, ("n", "?"))[1])
    elif k == 10:
        out.append('"' + lits.get(e, ("s", "?"))[1] + '"')
    elif k == 7:
        atom(C1[e], ctx, out, budget); out.append(f".{PAY(e)+1}")
    elif k == 8:
        pp(C1[e], ctx, out, budget)
    elif k in (4, 5):
        pp_binder(e, ctx, out, budget)
    elif k == 6:
        n = fresh(clean(name(PAY(e))), ctx)
        out.append(f"let {n} : "); pp(lets[e], ctx, out, budget); out.append(" := ")
        pp(C1[e], ctx, out, budget); out.append("; "); pp(C2[e], ctx + [n], out, budget)
    elif k == 3:
        pp_app(e, ctx, out, budget)
    else:
        out.append("?")


def fresh(n, ctx):
    if n not in ctx:
        return n
    i = 1
    while f"{n}{i}" in ctx:
        i += 1
    return f"{n}{i}"


def pp_binder(e, ctx, out, budget):
    k = KIND(e)
    if k == 5 and not has_bvar(C2[e], 0):  # flèche non dépendante
        atom_arrow(C1[e], ctx, out, budget); out.append(" → "); pp(C2[e], ctx + ["_"], out, budget); return
    groups = []; cur_ctx = list(ctx)
    while KIND(e) == k and not (k == 5 and not has_bvar(C2[e], 0)):
        n = fresh(clean(name(PAY(e))), cur_ctx)
        groups.append((n, BI(e), C1[e], list(cur_ctx))); cur_ctx.append(n); e = C2[e]
    out.append("∀ " if k == 5 else "fun ")
    br = {0: "()", 1: "{}", 2: "⦃⦄", 3: "[]"}
    for i, (n, bi, ty, c) in enumerate(groups):
        o, cl = br[bi]
        out.append(o)
        if bi == 3 and n.startswith("inst"):
            pass
        else:
            out.append(n + " : ")
        pp(ty, c, out, budget); out.append(cl + " ")
    out.append(", " if k == 5 else "=> ")
    pp(e, cur_ctx, out, budget)


def is_atomic(e):
    k = KIND(e)
    if k in (0, 1, 2, 9, 10, 7):
        return True
    if k == 8:
        return is_atomic(C1[e])
    if k == 3:
        h, a = spine(e)
        if KIND(h) == 2 and name(C1[h] & ~CB) == "OfNat.ofNat" and len(a) == 3:
            return True
    return False


def operand(e, ctx, out, budget):
    k = KIND(e)
    loose = k in (4, 5, 6)
    if k == 3:
        h, a = spine(e)
        hn = name(C1[h] & ~CB) if KIND(h) == 2 else None
        loose = hn in INFIX or hn in BINDERS or hn == "Not"
    if loose:
        out.append("("); pp(e, ctx, out, budget); out.append(")")
    else:
        pp(e, ctx, out, budget)


def atom(e, ctx, out, budget):
    if is_atomic(e):
        pp(e, ctx, out, budget)
    else:
        out.append("("); pp(e, ctx, out, budget); out.append(")")


def atom_arrow(e, ctx, out, budget):
    k = KIND(e); loose = k in (4, 5, 6)
    if k == 3:
        h, a = spine(e)
        loose = KIND(h) == 2 and name(C1[h] & ~CB) in BINDERS
    if loose:
        out.append("("); pp(e, ctx, out, budget); out.append(")")
    else:
        pp(e, ctx, out, budget)


def spine(e):
    a = []
    while KIND(e) == 3:
        a.append(C2[e]); e = C1[e]
    a.reverse()
    return e, a


def pp_app(e, ctx, out, budget):
    h, args_ = spine(e)
    hn = name(C1[h] & ~CB) if KIND(h) == 2 else None
    if hn and not EXPLICIT:
        tel = telescope(C1[h] & ~CB)
        vis = [a for i, a in enumerate(args_) if i >= len(tel) or tel[i] == 0]
        if hn == "OfNat.ofNat" and len(args_) == 3:
            pp(args_[1], ctx, out, budget); return
        if hn in INFIX and len(vis) == 2:
            operand(vis[0], ctx, out, budget); out.append(f" {INFIX[hn]} "); operand(vis[1], ctx, out, budget); return
        if hn == "Not" and len(vis) == 1:
            out.append("¬"); atom(vis[0], ctx, out, budget); return
        if hn in ("Neg.neg",) and len(vis) == 1:
            out.append("-"); atom(vis[0], ctx, out, budget); return
        if hn in BINDERS and vis and KIND(vis[-1]) == 4:
            lam = vis[-1]; n = fresh(clean(name(PAY(lam))), ctx)
            out.append(BINDERS[hn] + " " + n)
            for x in vis[:-1]:
                out.append(" ∈ "); atom(x, ctx, out, budget)
            out.append(", "); pp(C2[lam], ctx + [n], out, budget); return
        args_ = vis
        if not args_:
            out.append(hn); return
    else:
        if hn:
            out.append("@")
    atom(h, ctx, out, budget)
    for a in args_:
        out.append(" "); atom(a, ctx, out, budget)


def render(e, maxc):
    out = []; budget = [maxc]
    try:
        pp(e, [], out, budget)
    except TooLong:
        out.append(" …[tronqué]")
    return "".join(out)


def main():
    if args and args[0] == "--grep":
        rx = re.compile(args[1])
        for s in sorted(byname):
            if rx.search(s):
                print(s)
        return
    for nm in args:
        n = byname.get(nm)
        if n is None:
            print(f"### {nm} : INCONNU dans l'export\n"); continue
        print(f"### {nm}  [{kindof.get(n, 'membre d’inductif')}]")
        print(render(troot[n], MAXC))
        if SHOW_VAL and vroot.get(n, -1) >= 0:
            print("  :=")
            print(render(vroot[n], MAXC))
        print()


sys.setrecursionlimit(1_000_000)
threading.stack_size(512 * 1024 * 1024)
t = threading.Thread(target=main); t.start(); t.join()
