"""frontiere_donnees.py OUT FICHIER_DE_NOMS : Remonte depuis les objets signalés par les seuls référents « données » (def, instance, inductive, opaque…),
et liste les théorèmes atteints (la frontière) avec la tête de leur énoncé. Lit l'index inverse de revindex."""
import sys, os
from array import array
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1]; seeds = [l.strip() for l in open(sys.argv[2]) if l.strip()]
P = lambda f: os.path.join(OUT, f)
names = {}
for l in open(P("names.tsv"), encoding="utf-8", errors="replace"):
    i, s = l.rstrip("\n").split("\t", 1); names[int(i)] = s
byname = {s: i for i, s in names.items()}
dname, dkind = {}, {}
for l in open(P("decls.tsv")):
    p = l.split("\t"); d = int(p[0]); dname[d] = names[int(p[2])]; dkind[d] = p[1]
owner = {}
for l in open(P("members.tsv")):
    d, n, _ = l.split("\t"); owner[int(n)] = int(d)
off = array("Q"); off.frombytes(open(P("rev_off.u64"), "rb").read())
rev = array("I"); rev.frombytes(open(P("rev.u32"), "rb").read())
start = [owner[byname[s]] for s in seeds]
seen = set(start); todo = list(start); front = {}
data_via = {}
while todo:
    d = todo.pop()
    for r in rev[off[d]:off[d + 1]]:
        k = dkind[r]; n = dname[r]
        if k == 'thm':
            # les _proof_ auxiliaires d'une définition font partie de la définition
            front.setdefault(r, set()).add(dname[d])
        elif r not in seen:
            seen.add(r); todo.append(r); data_via[r] = dname[d]
import lexpr
E = lexpr.load(OUT)
print(f"# définitions atteintes : {len(seen)} ; théorèmes frontière : {len(front)}")
for d in sorted(seen - set(start), key=lambda x: dname[x]):
    print("DEF", dkind[d], dname[d], "<-", data_via[d], sep="\t")
for r in sorted(front, key=lambda x: dname[x]):
    cn = byname[dname[r]]
    _, body = E.telescope_full(cn)
    s = E.render(body, ctx=[n for n, _, _ in E.telescope_full(cn)[0]], maxc=160) if body is not None and body >= 0 else "?"
    print("THM", dname[r], "<-", ",".join(sorted(front[r]))[:120], s.replace("\n", " ")[:160], sep="\t")
