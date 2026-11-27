#!/usr/bin/env python3
"""Quels organes alimentent quelles interfaces ?

Pour chaque organe (une déclaration), on calcule par l'index inverse l'ensemble des déclarations
qui l'utilisent transitivement. Pour chaque théorème producteur d'interface (interfaces.tsv),
on note les organes qu'il utilise.

Usage : python3 -I organes.py OUT interfaces.tsv ORGANE=nom.complet ... > organes.tsv
"""
import sys, os, collections
from array import array

OUT, ITSV = sys.argv[1], sys.argv[2]
organs = [a.split("=", 1) for a in sys.argv[3:]]
P = lambda f: os.path.join(OUT, f)
names = {}
for l in open(P("names.tsv"), encoding="utf-8", errors="replace"):
    i, s = l.rstrip("\n").split("\t", 1); names[int(i)] = s
byname = {s: i for i, s in names.items()}
owner, dname = {}, {}
for l in open(P("members.tsv")):
    d, n, _ = l.split("\t"); owner[int(n)] = int(d)
for l in open(P("decls.tsv")):
    p = l.split("\t", 3); dname[int(p[0])] = int(p[2])
off = array("Q"); off.frombytes(open(P("rev_off.u64"), "rb").read())
rev = array("I"); rev.frombytes(open(P("rev.u32"), "rb").read())

prods = []
for l in open(ITSV):
    if l.startswith("theoreme"):
        continue
    t, w, h, c = l.rstrip("\n").split("\t")
    prods.append((t, int(w), c))

up = {}
for lab, nm in organs:
    d0 = owner[byname[nm]]; seen = bytearray(len(off)); seen[d0] = 1; q = collections.deque([d0]); k = 1
    while q:
        d = q.popleft()
        for r in rev[off[d]:off[d + 1]]:
            if not seen[r]:
                seen[r] = 1; q.append(r); k += 1
    up[lab] = seen
    print(f"# {lab} = {nm} : utilisé (transitivement) par {k} déclarations", file=sys.stderr)

print("producteur\tpoids\tconclusions\t" + "\t".join(l for l, _ in organs))
for t, w, c in prods:
    d = owner.get(byname.get(t, -1))
    if d is None:
        continue
    print(f"{t}\t{w}\t{c}\t" + "\t".join("X" if up[l][d] else "" for l, _ in organs))
