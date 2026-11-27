#!/usr/bin/env python3
"""Frontières de lecture : ce qui reste à lire quand on admet provisoirement des théorèmes.

Usage : python3 -I frontiere.py OUT RACINE[,RACINE…] CONFIG.txt [--test]
  plusieurs racines : racine virtuelle reliée à chacune (comme pour l'arbre des dominateurs)
  OUT     : répertoire de la passe 1 (decls.tsv, members.tsv, edges.bin, c1/c2/aux.u32, lets.bin)
  RACINE  : nom de la déclaration cible (par ex. riemannHypothesis)
  CONFIG  : fichier « nom_de_config : nom1 nom2 … » (une configuration par ligne, # pour commenter)

Pour une frontière B (des théorèmes admis), on construit
    G_B = (V, E_type ∪ { (u,v) ∈ E : u ∉ B })
c'est-à-dire qu'on garde l'énoncé de chaque théorème de B, et les constantes dont il dépend,
mais pas sa preuve. Les arêtes de type d'un théorème de B sont recalculées en parcourant son
type dans le DAG des expressions (c1/c2/aux.u32), comme show.py. Les définitions ne sont jamais
rendues opaques : seule une déclaration de genre « thm » peut être dans B.

Pour comparaison, on donne aussi
  - la zone atteinte quand on SUPPRIME les sommets de B (C_B, au sens de la proposition de l'article) ;
  - l'union des poids dominés des éléments de B (arbre des dominateurs).
Trois pondérations : déclarations, lignes de l'export, nœuds d'expression par déclaration.
La composition (bibliothèques Lean/Mathlib… contre projet) utilise OUT/../decl2mod.tsv si présent :
une déclaration qui n'y figure pas comme bibliothèque est comptée dans le projet.
Bibliothèque standard seule.
"""
import sys, os, mmap
from array import array

NONE, CB = 0xFFFFFFFF, 0x80000000

def bfs(root, succ):
    seen = {root}; st = [root]
    while st:
        d = st.pop()
        for c in succ(d):
            if c not in seen: seen.add(c); st.append(c)
    return seen

def test():
    # losange T→A, T→B, A→D, B→D ; A et B sont des théorèmes dont la valeur utilise D, le type rien
    full = {"T": ["A", "B"], "A": ["D"], "B": ["D"], "D": []}
    typ = {"A": [], "B": []}
    B = {"A", "B"}
    gb = bfs("T", lambda d: typ[d] if d in B else full[d])
    rm = bfs("T", lambda d: [c for c in full[d] if c not in B])
    assert gb == {"T", "A", "B"}, gb      # A, B restent lisibles (énoncés) ; D devient invisible
    assert rm == {"T"}, rm
    print("test losange : G_B =", sorted(gb), "; suppression =", sorted(rm), "OK")

def main():
    if "--test" in sys.argv: test(); return
    OUT, root_name, cfg = sys.argv[1], sys.argv[2], sys.argv[3]
    names = {}
    for l in open(os.path.join(OUT, "names.tsv"), encoding="utf-8", errors="replace"):
        i, s = l.rstrip("\n").split("\t", 1); names[int(i)] = s
    byname = {s: i for i, s in names.items()}
    owner = {}
    for l in open(os.path.join(OUT, "members.tsv")):
        d, n, _ = l.split("\t"); owner[int(n)] = int(d)
    kind, own, nodes, troot, dname = {}, {}, {}, {}, {}
    for l in open(os.path.join(OUT, "decls.tsv")):
        p = l.rstrip("\n").split("\t"); d = int(p[0])
        kind[d] = p[1]; dname[d] = int(p[2]); own[d] = int(p[3]); nodes[d] = int(p[4]) + int(p[5]); troot[d] = int(p[6])
        owner.setdefault(int(p[2]), d)
    N = len(kind)
    raw = array("I"); raw.frombytes(open(os.path.join(OUT, "edges.bin"), "rb").read())
    off = array("Q", [0]) * (N + 1); has = bytearray(N); i = 0; L = len(raw)
    while i < L:
        off[raw[i]] = i; has[raw[i]] = 1; i += 2 + raw[i + 1]
    def full(d):
        if not has[d]: return ()
        o = off[d]; n = raw[o + 1]
        return {owner[c] for c in raw[o + 2:o + 2 + n] if c in owner and owner[c] != d}
    # DAG des expressions, pour les types
    def mm(fn):
        f = open(os.path.join(OUT, fn), "rb"); return memoryview(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)).cast("I")
    C1, C2, AUX = mm("c1.u32"), mm("c2.u32"), mm("aux.u32")
    lets = {}
    lb = array("I"); lb.frombytes(open(os.path.join(OUT, "lets.bin"), "rb").read())
    for k in range(0, len(lb), 2): lets[lb[k]] = lb[k + 1]
    def type_consts(d):
        seen = set(); out = set(); st = [troot[d]]
        while st:
            v = st.pop()
            if v == NONE or v in seen: continue
            if v & CB: out.add(v & ~CB); continue
            seen.add(v); k = AUX[v] & 15
            if k == 2: out.add(C1[v] & ~CB); continue          # constante
            for c in (C1[v], C2[v]):
                if c != NONE: st.append(c)
            if k == 6 and v in lets: st.append(lets[v])         # type d'un let
        return {owner[c] for c in out if c in owner and owner[c] != d}
    def resolve(n):
        if n in byname: return owner[byname[n]]
        c = [s for s in byname if s.endswith("." + n) and not s.startswith("_private")]
        if len(c) == 1: return owner[byname[c[0]]]
        sys.exit(f"nom introuvable ou ambigu : {n} {c[:4]}")
    lib = set()
    modf = os.path.join(OUT, "..", "decl2mod.tsv")
    if os.path.exists(modf):
        for l in open(modf, encoding="utf-8", errors="replace"):
            q = l.rstrip("\n").split("\t")
            if len(q) >= 2 and q[1] != "projet" and q[0] in byname and byname[q[0]] in owner:
                lib.add(owner[byname[q[0]]])
    roots = [resolve(r) for r in root_name.split(",")]
    VR = -1   # racine virtuelle reliée aux racines données
    def succ_full(d): return roots if d == VR else full(d)
    root = VR
    total = bfs(root, succ_full); total.discard(VR)
    W = lambda S: (len(S), sum(own[d] for d in S), sum(nodes[d] for d in S))
    T = W(total)
    pct = lambda w: " ".join(f"{100*w[i]/T[i]:6.2f}%" for i in range(3))
    # arbre des dominateurs (pour l'union des poids dominés)
    import gzip, collections
    dt = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis", "decl_domtree.tsv.gz")
    idom = {}; f = gzip.open(dt, "rt", encoding="utf-8"); f.readline()
    for l in f:
        p = l.split("\t"); idom[int(p[0])] = (p[1], int(p[5]), int(p[6]), int(p[7]) + int(p[8]))
    print(f"racine {root_name} : {T[0]} décl., {T[1]} lignes, {T[2]} nœuds")
    print(f"{'configuration':34s} {'|B|':>4s}   {'G_B : reste à lire (décl. lignes nœuds)':>40s}   {'suppression':>22s}   {'∪ dominés':>8s}")
    for line in open(cfg, encoding="utf-8"):
        line = line.split("#")[0].strip()
        if not line: continue
        lab, rest = line.split(":", 1)
        B = {resolve(n) for n in rest.split()}
        bad = [names[dname[b]] for b in B if kind[b] != "thm"]
        if bad: sys.exit(f"{lab}: pas des théorèmes : {bad}")
        tc = {b: type_consts(b) for b in B}
        gb = bfs(root, lambda d: roots if d == VR else (tc[d] if d in B else full(d))); gb.discard(VR)
        rm = bfs(root, lambda d: [c for c in (roots if d == VR else full(d)) if c not in B]); rm.discard(VR)
        # union des dominés : éléments maximaux de B
        mx = []
        for b in B:
            v = idom[b][0]; inside = False
            while v != "ROOT":
                if int(v) in B: inside = True; break
                v = idom[int(v)][0]
            if not inside: mx.append(b)
        dom = sum(idom[b][1] for b in mx)
        nl = sum(1 for d in gb if d in lib)
        print(f"{lab.strip():34s} {len(B):4d}   {pct(W(gb)):>40s}   {100*len(rm)/T[0]:20.2f}%   {100*dom/T[0]:7.2f}%   biblio {nl} / projet {len(gb)-nl}")
        print(f"    exact : |R_cut| = {len(gb)}, |R_cut ∩ B| = {len(gb & B)}, |(R_cut \\ B) \\ R_del| = {len((gb - B) - rm)}, "
              f"|R \\ R_cut| = {len(total - gb)}, |R_del| = {len(rm)}, |∪ dominés| = {dom}")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
