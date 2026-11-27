#!/usr/bin/env python3
"""Poids dominés selon trois pondérations, et union reproductible d'un ensemble de nœuds.

Usage : python3 -I poids.py [DOMTREE] [--set FICHIER] [--csv SORTIE.csv] [--max SORTIE.txt]
  DOMTREE : domtree.tsv ou analysis/decl_domtree.tsv.gz (par défaut).
  FICHIER : un nom par ligne, « # » pour les commentaires ; un nom sans point est cherché
            comme suffixe « .NOM » et doit être unique.

Pondérations, pour chaque déclaration d de la fermeture :
  décl.   : 1 ;
  lignes  : lignes de l'export introduites avec d (colonne own) ;
  nœuds   : nœuds d'expression distincts du type et de la valeur de d (type_dag + value_dag),
            le partage étant compté à l'intérieur d'une déclaration, pas entre déclarations.
Le poids dominé d'un nœud est la somme sur son sous-arbre de l'arbre des dominateurs.
Deux sous-arbres sont emboîtés ou disjoints : l'union d'un ensemble se calcule en ne gardant
que ses éléments maximaux. Bibliothèque standard seule.
"""
import sys, os, gzip, collections

args = sys.argv[1:]
setfile = None; csvfile = None; maxfile = None
if "--csv" in args:
    k = args.index("--csv"); csvfile = args[k + 1]; del args[k:k + 2]
if "--max" in args:
    k = args.index("--max"); maxfile = args[k + 1]; del args[k:k + 2]
if "--set" in args:
    k = args.index("--set"); setfile = args[k + 1]; del args[k:k + 2]
path = args[0] if args else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis", "decl_domtree.tsv.gz")
f = gzip.open(path, "rt", encoding="utf-8") if path.endswith(".gz") else open(path, encoding="utf-8")
f.readline()
idom, name, w = {}, {}, {}
for l in f:
    p = l.rstrip("\n").split("\t")
    d = p[0]; idom[d] = p[1]; name[d] = p[3]
    w[d] = (1, int(p[4]), int(p[7]) + int(p[8]))
kids = collections.defaultdict(list)
for d, p in idom.items(): kids[p].append(d)
# sommes de sous-arbres, ordre postfixe itératif
sub = {}
st = [("ROOT", 0)]
while st:
    v, i = st.pop()
    ch = kids.get(v, [])
    if i < len(ch):
        st.append((v, i + 1)); st.append((ch[i], 0))
    else:
        a = list(w.get(v, (0, 0, 0)))
        for c in ch:
            s = sub[c]; a[0] += s[0]; a[1] += s[1]; a[2] += s[2]
        sub[v] = tuple(a)
TOT = sub["ROOT"]
byname = {}
for d, n in name.items(): byname.setdefault(n, d)
suffix = collections.defaultdict(list)
for n, d in byname.items():
    suffix[n.rsplit(".", 1)[-1]].append(n)

def resolve(n):
    if n in byname: return n
    c = [x for x in suffix.get(n, []) if not x.startswith("_private")]
    return c[0] if len(c) == 1 else None

def pct(s): return " ".join(f"{100*s[i]/TOT[i]:7.3f}%" for i in range(3))
print(f"total : {TOT[0]} décl., {TOT[1]} lignes, {TOT[2]} nœuds")
print(f"{'':52s} {'décl.':>8s} {'lignes':>8s} {'nœuds':>8s}")
if setfile:
    names = [l.split("#")[0].strip() for l in open(setfile, encoding="utf-8")]
    names = [n for n in names if n]
else:
    names = [name[c] for c in sorted(kids["ROOT"], key=lambda c: -sub[c][1])[:15]]
sel = []; rows = []
for n in names:
    r = resolve(n)
    if r is None:
        print(f"{n:52s} introuvable ou ambigu : {suffix.get(n, [])[:4]}"); continue
    d = byname[r]; sel.append(d)
    print(f"{r[:52]:52s} {pct(sub[d])}")
    rows.append((r, sub[d]))
if setfile:
    S = set(sel); mx = []
    for d in sel:
        v = idom[d]; inside = False
        while v != "ROOT":
            if v in S: inside = True; break
            v = idom[v]
        if not inside: mx.append(d)
    u = [sum(sub[d][i] for d in mx) for i in range(3)]
    if maxfile:
        with open(maxfile, "w", encoding="utf-8") as g:
            g.write("# Sous-arbres maximaux : nœuds de la liste qu'aucun autre nœud de la liste ne domine\n")
            for d in mx: g.write(name[d] + "\n")
    print(f"{'UNION (' + str(len(mx)) + ' sous-arbres maximaux)':52s} {pct(u)}")
if csvfile:
    with open(csvfile, "w", encoding="utf-8") as g:
        g.write("nom,decl,lignes,noeuds,pct_decl,pct_lignes,pct_noeuds\n")
        for r, v in rows + ([("UNION", u)] if setfile else []):
            g.write(f"{r},{v[0]},{v[1]},{v[2]}," + ",".join(f"{100*v[i]/TOT[i]:.4f}" for i in range(3)) + "\n")
