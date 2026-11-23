#!/usr/bin/env python3
"""Construit l'index inverse décl -> décl référentes (CSR) : rev_off.u64, rev.u32 dans OUT.
Puis : revindex.py OUT up NOM [profondeur]  -> remonte les chaînes de référents (BFS, poids dominés)."""
import sys, os
from array import array

def open_domtree(OUT):
    """domtree.tsv dans OUT, sinon la copie compressée analysis/decl_domtree.tsv.gz."""
    import os, gzip
    p = os.path.join(OUT, "domtree.tsv")
    if os.path.exists(p):
        return open(p, encoding="utf-8")
    gz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis", "decl_domtree.tsv.gz")
    return gzip.open(gz, "rt", encoding="utf-8")
OUT, cmd = sys.argv[1], sys.argv[2]
P = lambda f: os.path.join(OUT, f)
if cmd == "build":
    owner = {}; N = 0
    for l in open(P("members.tsv")):
        d, n, _ = l.split("\t"); owner[int(n)] = int(d)
    for l in open(P("decls.tsv")): N += 1
    raw = array("I"); raw.frombytes(open(P("edges.bin"), "rb").read())
    cnt = array("Q", [0]) * (N + 1); i = 0; L = len(raw); pairs_src = array("I"); pairs_dst = array("I")
    while i < L:
        d, n = raw[i], raw[i + 1]; seen = set()
        for c in raw[i + 2:i + 2 + n]:
            t = owner.get(c)
            if t is not None and t != d and t not in seen:
                seen.add(t); cnt[t] += 1; pairs_src.append(t); pairs_dst.append(d)
        i += 2 + n
    off = array("Q", [0]) * (N + 1); s = 0
    for v in range(N): off[v] = s; s += cnt[v]
    off[N] = s; fill = array("Q", off); rev = array("I", [0]) * s
    for k in range(len(pairs_src)):
        t = pairs_src[k]; rev[fill[t]] = pairs_dst[k]; fill[t] += 1
    off.tofile(open(P("rev_off.u64"), "wb")); rev.tofile(open(P("rev.u32"), "wb"))
    print("ok", N, s); sys.exit()
names = {}; dname = {}
for l in open(P("names.tsv"), encoding="utf-8", errors="replace"):
    i, s = l.rstrip("\n").split("\t", 1); names[int(i)] = s
byname = {s: i for i, s in names.items()}
owner = {}
for l in open(P("members.tsv")):
    d, n, _ = l.split("\t"); owner[int(n)] = int(d)
for l in open(P("decls.tsv")):
    p = l.split("\t", 3); dname[int(p[0])] = int(p[2])
off = array("Q"); off.frombytes(open(P("rev_off.u64"), "rb").read())
rev = array("I"); rev.frombytes(open(P("rev.u32"), "rb").read())
nm = lambda d: names.get(dname[d], "?")
if cmd == "up":   # chaîne de référents jusqu'à une décl. ayant > 1 référent ou la racine
    d = owner[byname[sys.argv[3]]]; depth = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    for k in range(depth):
        rs = rev[off[d]:off[d + 1]]
        print(f"{k:2d} {nm(d)}   ({len(rs)} référents)")
        if len(rs) != 1:
            for r in rs[:12]: print("      <-", nm(r))
            break
        d = rs[0]
if cmd == "refs":   # référents directs, triés par poids dominé
    dom = {}
    f = open_domtree(OUT); f.readline()
    for l in f:
        p = l.rstrip("\n").split("\t"); dom[p[3]] = (p[2], int(p[5]), int(p[6]))
    for a in sys.argv[3:]:
        d = owner[byname[a]]; rs = rev[off[d]:off[d + 1]]
        print(f"== {a} ({len(rs)})")
        for r in sorted(rs, key=lambda r: -dom.get(nm(r), ("", 0, 0))[2])[:25]:
            k, n, w = dom.get(nm(r), ("?", 0, 0)); print(f"   {w:>9} {k:<9} {nm(r)}")
if cmd == "path":   # chemin d'usage : SOURCE utilise (transitivement) CIBLE ? BFS remontant depuis CIBLE
    import collections
    src = owner[byname[sys.argv[3]]]; tgts = [owner[byname[a]] for a in sys.argv[4:]]
    for tg in tgts:
        prev = {tg: None}; q = collections.deque([tg]); found = False
        while q:
            d = q.popleft()
            if d == src: found = True; break
            for r in rev[off[d]:off[d + 1]]:
                if r not in prev: prev[r] = d; q.append(r)
        print(f"== {nm(src)}  utilise  {nm(tg)} ? {'OUI' if found else 'NON'}  (remontée : {len(prev)} décl.)")
        if found:
            d = src; chain = []
            while d is not None: chain.append(nm(d)); d = prev[d]
            for c in chain: print("     ", c)
