#!/usr/bin/env python3
"""Passe 2 : graphe des déclarations (sorties de deps.c) -> fermeture, dominateurs, poids.

Usage : python3 -I analyse_export.py OUTDIR [racine ...]
Par défaut, racines = les 5 théorèmes de Main. Écrit OUTDIR/report_decl.md, closure_*.txt, domtree.tsv.
"""
import sys, os, collections
from array import array

OUT = sys.argv[1]
MAIN = ["riemannHypothesis", "riemannZeta_eq_zero_re", "LFunction_ne_zero_of_half_lt_re",
        "LFunction_eq_zero_re", "LFunction_eq_zero_re_of_isPrimitive"]
ROOTS = sys.argv[2:] or MAIN


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# ---------- chargement ----------
names = {}
with open(os.path.join(OUT, "names.tsv"), encoding="utf-8", errors="replace") as f:
    for l in f:
        i, s = l.rstrip("\n").split("\t", 1)
        names[int(i)] = s
log("names", len(names))

kind, dname, own, tdag, vdag = [], array("I"), array("Q"), array("Q"), array("Q")
with open(os.path.join(OUT, "decls.tsv")) as f:
    for l in f:
        p = l.split("\t")
        kind.append(p[1]); dname.append(int(p[2])); own.append(int(p[3]))
        tdag.append(int(p[4])); vdag.append(int(p[5]))
N = len(kind)
log("decls", N)

owner = {}  # name_id -> d
with open(os.path.join(OUT, "members.tsv")) as f:
    for l in f:
        d, n = l.split("\t")[:2]
        owner[int(n)] = int(d)

# arêtes : CSR d -> d'
off = array("Q", [0]) ; succ = array("I")
raw = array("I")
with open(os.path.join(OUT, "edges.bin"), "rb") as f:
    raw.frombytes(f.read())
missing = 0
i = 0; L = len(raw); d_expect = 0
while i < L:
    d, n = raw[i], raw[i + 1]
    assert d == d_expect; d_expect += 1
    seen = set()
    for c in raw[i + 2:i + 2 + n]:
        t = owner.get(c)
        if t is None:
            missing += 1; continue
        if t != d and t not in seen:
            seen.add(t); succ.append(t)
    off.append(len(succ))
    i += 2 + n
del raw
E = len(succ)
log("edges", E, "missing", missing)

byname = {s: owner[i] for i, s in names.items() if i in owner}


def nm(d):
    return names.get(dname[d], "?")


roots = []
for r in ROOTS:
    if r not in byname:
        sys.exit("racine inconnue : " + r)
    roots.append(byname[r])


# ---------- fermeture ----------
def closure(rs):
    seen = bytearray(N); st = list(rs)
    for r in rs: seen[r] = 1
    while st:
        d = st.pop()
        for k in range(off[d], off[d + 1]):
            t = succ[k]
            if not seen[t]:
                seen[t] = 1; st.append(t)
    return seen


cl_rh = closure([byname["riemannHypothesis"]])
cl_all = closure(roots)
n_rh, n_all = sum(cl_rh), sum(cl_all)
log("closure RH", n_rh, "closure all", n_all)

# ---------- dominateurs (Cooper-Harvey-Kennedy) sur la fermeture de toutes les racines ----------
VR = N  # racine virtuelle
po_num = array("i", [-1]) * (N + 1)
order = array("I")  # postordre
stack = [(VR, 0)]
po_num[VR] = -2
visited = bytearray(N + 1); visited[VR] = 1


def children(v):
    if v == VR:
        return roots
    return succ[off[v]:off[v + 1]]


# DFS itératif
it_stack = [(VR, iter(children(VR)))]
while it_stack:
    v, it = it_stack[-1]
    adv = False
    for t in it:
        if not visited[t]:
            visited[t] = 1
            it_stack.append((t, iter(children(t))))
            adv = True
            break
    if not adv:
        it_stack.pop()
        po_num[v] = len(order); order.append(v)
log("dfs done", len(order))

# prédécesseurs (restreints aux nœuds atteints)
pc = array("I", [0]) * (N + 2)
for v in order:
    for t in children(v):
        pc[t] += 1
poff = array("Q", [0]) * (N + 2)
s = 0
for v in range(N + 1):
    poff[v] = s; s += pc[v]
poff[N + 1] = s
pred = array("I", [0]) * s
fill = array("Q", poff)
for v in order:
    for t in children(v):
        pred[fill[t]] = v; fill[t] += 1
del fill, pc
log("preds", s)

UNDEF = -1
idom = array("i", [UNDEF]) * (N + 1)
idom[VR] = VR
rpo = list(reversed(order))
changed = True; rounds = 0
while changed:
    changed = False; rounds += 1
    for v in rpo:
        if v == VR:
            continue
        new = UNDEF
        for k in range(poff[v], poff[v + 1]):
            p = pred[k]
            if idom[p] == UNDEF:
                continue
            if new == UNDEF:
                new = p; continue
            a, b = p, new
            while a != b:
                while po_num[a] < po_num[b]:
                    a = idom[a]
                while po_num[b] < po_num[a]:
                    b = idom[b]
            new = a
        if idom[v] != new:
            idom[v] = new; changed = True
    log("dom round", rounds)

# poids des sous-arbres (en postordre, les enfants avant le parent dans l'arbre des dominateurs ? non :
# on accumule dans l'ordre postfixe inverse de la profondeur -> utiliser l'ordre postfixe du DFS :
# idom[v] précède v dans tout chemin, donc po_num[idom[v]] > po_num[v]).
sub_n = array("Q", [0]) * (N + 1)
sub_w = array("Q", [0]) * (N + 1)
for v in order:  # postordre croissant : v avant idom[v]
    if v != VR:
        sub_n[v] += 1; sub_w[v] += own[v]
        sub_n[idom[v]] += sub_n[v]; sub_w[idom[v]] += sub_w[v]
kids = collections.defaultdict(list)
for v in order:
    if v != VR:
        kids[idom[v]].append(v)
for k in kids:
    kids[k].sort(key=lambda x: -sub_w[x])

# ---------- sorties ----------
with open(os.path.join(OUT, "domtree.tsv"), "w") as f:
    f.write("d\tidom\tkind\tname\town\tsub_n\tsub_w\ttype_dag\tvalue_dag\n")
    for v in order:
        if v != VR:
            f.write(f"{v}\t{idom[v] if idom[v] != VR else 'ROOT'}\t{kind[v]}\t{nm(v)}\t{own[v]}\t{sub_n[v]}\t{sub_w[v]}\t{tdag[v]}\t{vdag[v]}\n")

with open(os.path.join(OUT, "closure_all.txt"), "w") as f:
    for d in range(N):
        if cl_all[d]:
            f.write(nm(d) + "\n")
with open(os.path.join(OUT, "not_in_closure.txt"), "w") as f:
    for d in range(N):
        if not cl_all[d]:
            f.write(f"{kind[d]}\t{nm(d)}\t{own[d]}\n")

# ---------- attribution aux paquets ----------
d2m = {}
p_d2m = os.path.join(os.path.dirname(os.path.abspath(OUT)), "decl2mod.tsv")
if os.path.exists(p_d2m):
    with open(p_d2m, encoding="utf-8") as f:
        for l in f:
            a = l.rstrip("\n").split("\t")
            d2m[a[0]] = (a[1], a[2])


p_ch = os.path.join(os.path.dirname(os.path.abspath(OUT)), "out_ch", "names.tsv")
ch_names = set()
if os.path.exists(p_ch) and os.path.abspath(OUT) != os.path.dirname(p_ch):
    with open(p_ch, encoding="utf-8", errors="replace") as f:
        ch_names = set(l.rstrip("\n").split("\t", 1)[1] for l in f)


def pkg_of(s):
    if s in ch_names:
        r = d2m.get(s)
        return r[0] if r and r[0] != "projet" else "lean/mathlib (via challenge)"
    if s.startswith("_private."):
        root = s[9:].split(".", 1)[0]  # _private.<Module>.0.nom
        return {"Mathlib": "mathlib", "Init": "core", "Lean": "core", "Std": "core", "Batteries": "batteries",
                "Aesop": "aesop", "Qq": "Qq", "Lake": "core"}.get(root, "projet")
    t = s
    while True:
        r = d2m.get(t)
        if r:
            return r[0]
        i = t.rfind(".")
        if i < 0:
            return "projet"
        t = t[:i]


pkg = [pkg_of(nm(d)) for d in range(N)]

tot_w = sum(own); w_all = sum(own[d] for d in range(N) if cl_all[d]); w_rh = sum(own[d] for d in range(N) if cl_rh[d])
R = []
R.append("# Analyse de l'export (niveau déclarations)\n")
R.append(f"- déclarations exportées (nœuds ; un bloc inductif = 1 nœud) : **{N}**")
R.append(f"- arêtes distinctes (décl → décl) : {E} ; références non résolues : {missing}")
R.append(f"- fermeture de `riemannHypothesis` : **{n_rh}** ({100*n_rh/N:.2f} %) ; poids {w_rh} lignes d'expr. ({100*w_rh/tot_w:.2f} %)")
R.append(f"- fermeture des 5 théorèmes de Main : **{n_all}** ({100*n_all/N:.2f} %) ; poids {w_all} ({100*w_all/tot_w:.2f} %)")
R.append(f"- itérations dominateurs : {rounds}\n")
R.append("## Composition par paquet\n")
R.append("| paquet | décl. exportées | dans fermeture Main | dans fermeture RH | poids (lignes expr.) fermeture Main |")
R.append("|---|---:|---:|---:|---:|")
agg = collections.defaultdict(lambda: [0, 0, 0, 0])
for d in range(N):
    a = agg[pkg[d]]; a[0] += 1
    if cl_all[d]:
        a[1] += 1; a[3] += own[d]
    if cl_rh[d]:
        a[2] += 1
for k, a in sorted(agg.items(), key=lambda x: -x[1][3]):
    R.append(f"| {k} | {a[0]} | {a[1]} | {a[2]} | {a[3]} ({100*a[3]/max(w_all,1):.1f} %) |")
R.append("")
PATS = ["LitN", "LitLoc", "LitAut", "Hypotheses₂", "published_inputs_combined", "Published.LocalLanglandsGL",
        "LocalRepresentationTheoryHypothesesAlt", "GlobalAutomorphicGaloisHypotheses'", "OpenLiteratureStatements",
        "recTExists", "cuspEx", "galoisLocalGlobalStrong_recParameter", "vwin_of_row", "PropsB", "Row0b",
        "every_character_of_theta_integrals_local_matching", "everyCharacter_of_row"]
R.append("## Présence des noms de l'échafaudage (suffixe exact du nom complet)\n")
R.append("| motif | décl. exportées dont le nom finit par le motif | dont dans fermeture Main | exemples |")
R.append("|---|---:|---:|---|")
for pat in PATS:
    hits = [d for d in range(N) if nm(d) == pat or nm(d).endswith("." + pat)]
    inn = [d for d in hits if cl_all[d]]
    R.append(f"| `{pat}` | {len(hits)} | {len(inn)} | {', '.join('`'+nm(d)+'`' for d in hits[:3])} |")
R.append("")
R.append("## Nœuds structurants du projet (dominateurs du projet les plus lourds, hors chaînes triviales)\n")
proj_dom = [v for v in order if v != VR and pkg[v] == "projet" and sub_n[v] > 1]
proj_dom.sort(key=lambda v: -sub_w[v])
for v in proj_dom[:150]:
    p = idom[v]
    R.append(f"- `{nm(v)}` [{kind[v]}] — {sub_n[v]} décl., {100*sub_w[v]/w_all:.2f} % ; idom = `{nm(p) if p != VR else 'ROOT'}`")
R.append("")
R.append("## Enfants directs de la racine virtuelle et premiers niveaux (poids = lignes d'expressions dominées)\n")


def dump(v, depth, maxdepth, minfrac, lines):
    for c in kids.get(v, []):
        if sub_w[c] < minfrac * w_all:
            break
        lines.append(f"{'  '*depth}- `{nm(c)}` [{kind[c]}] — {sub_n[c]} décl., {100*sub_w[c]/w_all:.2f} %")
        if depth + 1 < maxdepth:
            dump(c, depth + 1, maxdepth, minfrac, lines)


lines = []
dump(VR, 0, 12, 0.005, lines)
R += lines
R.append("\n## Épine dorsale (enfant le plus lourd, récursivement)\n")
v = byname["riemannHypothesis"]; depth = 0
while True:
    R.append(f"{depth:3d}. `{nm(v)}` [{kind[v]}] — sous-arbre {sub_n[v]} décl., {100*sub_w[v]/w_all:.2f} % ; propre {own[v]}")
    if not kids.get(v):
        break
    v = kids[v][0]; depth += 1
    if depth > 400:
        break
with open(os.path.join(OUT, "report_decl.md"), "w") as f:
    f.write("\n".join(R) + "\n")
print("\n".join(R[:8]))
