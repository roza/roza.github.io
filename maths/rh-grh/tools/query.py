#!/usr/bin/env python3
"""Requêtes sur le graphe : épine depuis ROOT, dépendances directes, référents de noms.
Usage : query.py OUT spine | deps NOM... | refs NOM..."""
import sys, os, collections
from array import array

def open_domtree(OUT):
    """domtree.tsv dans OUT, sinon la copie compressée analysis/decl_domtree.tsv.gz."""
    import os, gzip
    p = os.path.join(OUT, "domtree.tsv")
    if os.path.exists(p):
        return open(p, encoding="utf-8")
    gz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis", "decl_domtree.tsv.gz")
    return gzip.open(gz, "rt", encoding="utf-8")
OUT, cmd, args = sys.argv[1], sys.argv[2], sys.argv[3:]
names = {}
for l in open(os.path.join(OUT, "names.tsv"), encoding="utf-8", errors="replace"):
    i, s = l.rstrip("\n").split("\t", 1); names[int(i)] = s
byname = {s: i for i, s in names.items()}
if cmd == "spine":
    rows = {}; kids = collections.defaultdict(list)
    f = open_domtree(OUT); f.readline()
    for l in f:
        p = l.rstrip("\n").split("\t")
        rows[p[0]] = p; kids[p[1]].append(p[0])
    tot = sum(int(rows[c][6]) for c in kids["ROOT"])
    v = "ROOT"; dep = 0
    while kids.get(v):
        ch = sorted(kids[v], key=lambda c: -int(rows[c][6]))
        c = ch[0]; r = rows[c]
        alt = "; ".join(f"{rows[x][3]} {100*int(rows[x][6])/tot:.1f}%" for x in ch[1:4] if int(rows[x][6]) > tot * 0.003)
        print(f"{dep:3d} {100*int(r[6])/tot:6.2f}% {r[5]:>8} {r[3]}" + (f"   || frères: {alt}" if alt else ""))
        v = c; dep += 1
    sys.exit()
if cmd == "cl":
    # taille de la fermeture (décl. + lignes d'expr.) pour chaque nom, et part propre (dominée)
    owner = {}; dname = {}; own = {}
    for l in open(os.path.join(OUT, "members.tsv")):
        d, n, _ = l.split("\t"); owner[int(n)] = int(d)
    for l in open(os.path.join(OUT, "decls.tsv")):
        p = l.split("\t"); dname[int(p[0])] = int(p[2]); own[int(p[0])] = int(p[3])
    N = len(dname)
    raw = array("I"); raw.frombytes(open(os.path.join(OUT, "edges.bin"), "rb").read())
    off = array("Q", [0]) * (N + 1); i = 0; L = len(raw)
    while i < L:
        off[raw[i]] = i; i += 2 + raw[i + 1]
    dom = {}
    f = open_domtree(OUT); f.readline()
    for l in f:
        p = l.rstrip("\n").split("\t"); dom[p[3]] = (int(p[5]), int(p[6]))
    for a in args:
        if a not in byname: print("inconnu", a); continue
        r = owner[byname[a]]; seen = {r}; st = [r]; w = 0
        while st:
            d = st.pop(); w += own[d]; o = off[d]; n = raw[o + 1]
            for c in raw[o + 2:o + 2 + n]:
                t = owner.get(c)
                if t is not None and t not in seen: seen.add(t); st.append(t)
        dn, dw = dom.get(a, (0, 0))
        print(f"{a}\tfermeture {len(seen)} décl. / {w} lignes\tdominé {dn} décl. / {dw} lignes")
    sys.exit()
targets = {byname[a] for a in args if a in byname}
miss = [a for a in args if a not in byname]
if miss: print("inconnus:", miss)
owner = {}; dname = {}
for l in open(os.path.join(OUT, "members.tsv")):
    d, n, _ = l.split("\t"); owner[int(n)] = int(d)
for l in open(os.path.join(OUT, "decls.tsv")):
    p = l.split("\t", 3); dname[int(p[0])] = int(p[2])
raw = array("I"); raw.frombytes(open(os.path.join(OUT, "edges.bin"), "rb").read())
i = 0; L = len(raw)
want = {owner[t] for t in targets} if cmd == "deps" else None
res = collections.defaultdict(list)
while i < L:
    d, n = raw[i], raw[i + 1]; seg = raw[i + 2:i + 2 + n]
    if cmd == "deps" and d in want:
        res[names[dname[d]]] = sorted(names.get(c, "?") for c in seg)
    elif cmd == "refs":
        for c in seg:
            if c in targets and dname[d] != c: res[names[c]].append(names[dname[d]])
    i += 2 + n
for k, v in res.items():
    print(f"== {k} ({len(v)})")
    for x in (v if cmd == "deps" else v[:60]): print("   ", x)
