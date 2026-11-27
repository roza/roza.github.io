#!/usr/bin/env python3
"""Graphe des interfaces : quels théorèmes de l'export transforment quels prédicats en quels autres.

Une « interface » est une définition à valeur dans Prop dont le nom correspond à REGEX
(par défaut : les prédicats de Formalism.MainNotions, dont Lnk.*_at, Link*, ChainTied…).
Pour chaque théorème qui mentionne une interface dans son type, on lit :
  - les hypothèses : types des lieurs ∀ / → dont la tête est une interface ;
  - les conclusions : têtes des conjoints de la conclusion finale (après les ∀ et les ∃).
Sortie TSV : théorème, poids dominé, hypothèses (séparées par ,), conclusions.

Usage : python3 -I interfaces.py OUT [REGEX] > interfaces.tsv
"""
import sys, os, mmap, re, gzip
from array import array

OUT = sys.argv[1]
RX = re.compile(sys.argv[2] if len(sys.argv) > 2 else
                r"^Formalism\.MainNotions\.(Lnk\.|StandardLattice\.)?[A-Z][A-Za-z0-9_]*$")
P = lambda f: os.path.join(OUT, f)


def mm(fn):
    f = open(P(fn), "rb")
    return memoryview(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)).cast("I")


C1, C2, AUX = mm("c1.u32"), mm("c2.u32"), mm("aux.u32")
CB = 0x80000000
KIND = lambda e: AUX[e] & 15
PAY = lambda e: AUX[e] >> 6
levels = {}
for l in open(P("levels.tsv")):
    a = l.rstrip("\n").split("\t"); levels[int(a[0])] = a[1]

names = {}
for l in open(P("names.tsv"), encoding="utf-8", errors="replace"):
    i, s = l.rstrip("\n").split("\t", 1); names[int(i)] = s
troot, owner, kind, dname = {}, {}, {}, {}
for l in open(P("members.tsv")):
    d, n, t = l.split("\t"); troot[int(n)] = int(t); owner[int(n)] = int(d)
for l in open(P("decls.tsv")):
    p = l.split("\t"); kind[int(p[2])] = p[1]; dname[int(p[0])] = int(p[2])
off = array("Q"); off.frombytes(open(P("rev_off.u64"), "rb").read())
rev = array("I"); rev.frombytes(open(P("rev.u32"), "rb").read())

weight = {}
gz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis", "decl_domtree.tsv.gz")
with gzip.open(gz, "rt", encoding="utf-8") as f:
    f.readline()
    for l in f:
        p = l.rstrip("\n").split("\t"); weight[p[3]] = int(p[6])


def head(e):
    while KIND(e) == 3:
        e = C1[e]
    while KIND(e) == 8:  # mdata
        e = C1[e]
    return (C1[e] & ~CB) if KIND(e) == 2 else None


def is_prop_valued(n):
    t = troot.get(n)
    while t is not None and KIND(t) == 5:
        t = C2[t]
    return t is not None and KIND(t) == 1 and PAY(t) == 0


iface = {n for n, s in names.items() if RX.match(s) and kind.get(n) == "def" and is_prop_valued(n)}
iname = lambda n: names[n].replace("Formalism.MainNotions.", "")


def conjuncts(e, acc):
    """têtes d'interfaces dans un conjoint (∧, ∃, ∀ imbriqués)."""
    while KIND(e) == 5:
        e = C2[e]
    h = head(e)
    if h is None:
        return
    hn = names.get(h, "")
    if h in iface:
        acc.add(h); return
    if hn in ("And", "Iff"):
        a = []
        x = e
        while KIND(x) == 3:
            a.append(C2[x]); x = C1[x]
        for y in a[:2]:
            conjuncts(y, acc)
    elif hn == "Exists":
        lam = C2[e]
        if KIND(lam) == 4:
            conjuncts(C2[lam], acc)
    elif hn == "Nonempty":
        conjuncts(C2[e], acc)


cands = set()
for n in iface:
    d = owner.get(n)
    if d is None:
        continue
    for r in rev[off[d]:off[d + 1]]:
        cands.add(dname[r])
print("theoreme\tpoids\thypotheses\tconclusions")
for n in sorted(cands, key=lambda n: names[n]):
    if kind.get(n) != "thm":
        continue
    t = troot[n]; hyps = set()
    while KIND(t) == 5:
        conjuncts(C1[t], hyps); t = C2[t]
    concl = set(); conjuncts(t, concl)
    hyps -= concl
    if concl and (hyps or True):
        print(f"{names[n]}\t{weight.get(names[n], 0)}\t{','.join(sorted(map(iname, hyps)))}\t{','.join(sorted(map(iname, concl)))}")
print(f"# interfaces : {len(iface)}", file=sys.stderr)
