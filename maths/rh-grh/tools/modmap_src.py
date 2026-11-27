#!/usr/bin/env python3
"""modmap_src.py SRC_ROOT DOMTREE SORTIE.tsv : rattache les déclarations d'un export à leurs fichiers source,
sans compiler ni exécuter le projet (lecture du texte des .lean).

Lecture : `namespace`/`section`/`end`, et les déclarations (`theorem`, `lemma`, `def`, `abbrev`, `instance`,
`structure`, `class`, `inductive`, `opaque`) avec leurs modificateurs. Un nom `private` devient
`_private.<Module>.0.<nom>`. Les déclarations auxiliaires de l'export (`._proof_1`, `.match_1`, champs, `.mk`,
`.rec`…) sont rattachées en retirant des composants à droite jusqu'à un nom connu. Bibliothèque standard seule.
Sortie : nom, module (ou `?`), poids propre (colonne own de DOMTREE). Résumé par dossier sur stderr."""
import os, re, sys, collections

SRC, DOM, OUTF = sys.argv[1:4]
KW = r"(?:theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque|irreducible_def)"
DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)*((?:(?:private|protected|noncomputable|partial|unsafe|nonrec|scoped)\s+)*)"
                  + KW + r"\s+([^\s:({\[⦃]+)")
NS = re.compile(r"^\s*namespace\s+(\S+)")
SEC = re.compile(r"^\s*(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")
END = re.compile(r"^\s*end(?:\s+(\S+))?\s*$")

where = {}
for dp, _, fs in os.walk(SRC):
    for f in fs:
        if not f.endswith(".lean"): continue
        p = os.path.join(dp, f)
        mod = os.path.relpath(p, SRC)[:-5].replace(os.sep, ".")
        stack = []          # éléments : ('ns', [composants]) ou ('sec', nom)
        incomment = False
        for line in open(p, encoding="utf-8", errors="replace"):
            if "/-" in line and "-/" not in line: incomment = True
            if incomment:
                if "-/" in line: incomment = False
                continue
            m = NS.match(line)
            if m: stack.append(("ns", m.group(1).split("."))); continue
            m = SEC.match(line)
            if m: stack.append(("sec", m.group(1))); continue
            m = END.match(line)
            if m and stack:
                stack.pop(); continue
            m = DECL.match(line)
            if not m: continue
            mods, name = m.group(1), m.group(2)
            if name.startswith("_root_."): full = name[len("_root_."):]
            else:
                ns = [c for kind, v in stack if kind == "ns" for c in v]
                full = ".".join(ns + [name])
            if "private" in mods: full = f"_private.{mod}.0.{full}"
            where.setdefault(full, mod)

own, names = {}, []
with open(DOM, encoding="utf-8") as fh:
    fh.readline()
    for l in fh:
        p = l.rstrip("\n").split("\t"); own[p[3]] = int(p[4]); names.append(p[3])

def find(n):
    if n in where: return where[n]
    m = re.match(r"_private\.(.+?)\.0\.(.+)$", n)          # privé : le module est dans le nom
    if m: return m.group(1) if os.path.exists(os.path.join(SRC, m.group(1).replace(".", os.sep) + ".lean")) else None
    parts = n.split(".")
    for k in range(len(parts) - 1, 0, -1):
        c = ".".join(parts[:k])
        if c in where: return where[c]
    return None

agg = collections.Counter(); cnt = collections.Counter(); tot = 0; found = 0
with open(OUTF, "w", encoding="utf-8") as out:
    for n in names:
        mod = find(n); w = own[n]; tot += w
        out.write(f"{n}\t{mod or '?'}\t{w}\n")
        if mod:
            found += 1
            parts = mod.split(".")
            key = ".".join(parts[:3]) if parts[0] == "src" else ".".join(parts[:2])
            agg[key] += w; cnt[key] += 1
print(f"# déclarations : {len(names)} ; rattachées à un fichier du projet : {found} ; "
      f"poids rattaché : {sum(agg.values())} / {tot} lignes ({100*sum(agg.values())/tot:.1f} %)", file=sys.stderr)
for k, w in agg.most_common():
    print(f"{k}\t{cnt[k]}\t{w}\t{100*w/tot:.2f} %", file=sys.stderr)
