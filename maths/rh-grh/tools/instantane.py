#!/usr/bin/env python3
"""Instantané figé et reproductible des outils et des données dérivées.

Usage : python3 -I tools/instantane.py ÉTIQUETTE   (ex. : v0.8-2026-11-25)
Produit analysis/instantanes/rh-check-outils-ÉTIQUETTE.tar.gz et son MANIFEST.sha256.
L'archive est déterministe : fichiers triés, dates fixées à l'époque SOURCE_DATE (le jour de
l'étiquette), propriétaire 0, droits normalisés, gzip sans nom ni date. Deux exécutions sur les
mêmes fichiers donnent la même empreinte. Bibliothèque standard seule.
Contenu : tools/ (sources, sans binaire ni cache), les listes de nœuds, résultats, extraits et
empreintes de analysis/. L'arbre des dominateurs (decl_domtree.tsv.gz, 27 Mo) n'est pas inclus :
son empreinte figure dans le manifeste, et il est publié à part.
"""
import sys, os, io, tarfile, gzip, hashlib, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
tag = sys.argv[1]
date = datetime.date.fromisoformat(tag[-10:])   # l'étiquette se termine par AAAA-MM-JJ
MTIME = int(datetime.datetime(date.year, date.month, date.day, tzinfo=datetime.timezone.utc).timestamp())

def files():
    out = []
    for f in sorted(os.listdir(os.path.join(ROOT, "tools"))):
        if f.endswith((".py", ".c", ".md")): out.append("tools/" + f)
    A = os.path.join(ROOT, "analysis")
    for f in sorted(os.listdir(A)):
        if (f.endswith((".txt", ".csv", ".tsv", ".sha256")) and not f.startswith(("suggestions", "rubinstein"))) \
                or f == "raccords.md":
            out.append("analysis/" + f)
    for f in sorted(os.listdir(os.path.join(A, "extraits"))):
        out.append("analysis/extraits/" + f)
    return out

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 24), b""): h.update(b)
    return h.hexdigest()

L = files()
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w", format=tarfile.USTAR_FORMAT) as tar:
    for rel in L:
        data = open(os.path.join(ROOT, rel), "rb").read()
        ti = tarfile.TarInfo("rh-check-outils-" + tag + "/" + rel)
        ti.size = len(data); ti.mtime = MTIME; ti.uid = ti.gid = 0; ti.uname = ti.gname = ""
        ti.mode = 0o644
        tar.addfile(ti, io.BytesIO(data))
D = os.path.join(ROOT, "analysis", "instantanes"); os.makedirs(D, exist_ok=True)
tgz = os.path.join(D, f"rh-check-outils-{tag}.tar.gz")
with open(tgz, "wb") as fh:
    with gzip.GzipFile(filename="", mode="wb", fileobj=fh, mtime=0, compresslevel=9) as gz:
        gz.write(buf.getvalue())
man = os.path.join(D, f"rh-check-outils-{tag}.MANIFEST.sha256")
with open(man, "w", encoding="utf-8") as m:
    m.write(f"# Instantané {tag} : {len(L)} fichiers. Vérification : shasum -a 256 -c (depuis la racine du projet)\n")
    for rel in L: m.write(f"{sha(os.path.join(ROOT, rel))}  {rel}\n")
    dom = os.path.join(ROOT, "analysis", "decl_domtree.tsv.gz")
    if os.path.exists(dom): m.write(f"{sha(dom)}  analysis/decl_domtree.tsv.gz\n")
    m.write(f"# archive\n# {sha(tgz)}  analysis/instantanes/{os.path.basename(tgz)}\n")
print(tgz, sha(tgz), f"{len(L)} fichiers", sep="\n")
