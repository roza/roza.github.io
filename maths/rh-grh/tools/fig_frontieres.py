#!/usr/bin/env python3
"""Figure : fermeture encore accessible sous des frontières de lecture emboîtées (SVG, bibliothèque standard).

Usage : python3 -I fig_frontieres.py analysis/frontieres_resultats.txt analysis/fig
Lit les lignes « k. configuration |B| d% l% n% suppr% dom% … » produites par frontiere.py et écrit
frontieres.svg (français) et frontieres_en.svg (anglais). Pour chaque frontière : trois barres (déclarations,
lignes de l'export, nœuds) et un trait noir à 100 % − (union des poids dominés), ce que laisserait la
somme des sous-arbres dominés : l'écart entre ce trait et la barre « déclarations » est l'effet collectif.
"""
import sys, os, re

LAB = {
    "fr": {"title": "Part de la fermeture encore accessible quand on admet des théorèmes (%)",
           "series": ["déclarations", "lignes de l'export", "nœuds"],
           "mark": "100 − ∪ poids dominés (décl.)",
           "conf": ["aucune frontière", "cœur automorphe admis", "sept grandes théories",
                    "+ quatre liens", "idem, CM.DegSt ouvert"]},
    "en": {"title": "Share of the closure still accessible when theorems are admitted (%)",
           "series": ["declarations", "export lines", "nodes"],
           "mark": "100 − ∪ dominated weights (decl.)",
           "conf": ["no frontier", "automorphic core admitted", "seven large theories",
                    "+ four links", "same, CM.DegSt opened"]},
}
COL = ["#3a6ea5", "#a97a39", "#16866d"]

def parse(src):
    rows = []
    for l in open(src, encoding="utf-8"):
        if not re.match(r"\d\.", l): continue
        p = [float(x) for x in re.findall(r"([\d.]+)%", l)]
        rows.append((p[0], p[1], p[2], 100.0 - p[4]))
    return rows

def main(src, outdir):
    rows = parse(src)
    for lang, L in LAB.items():
        W, left, top, bh, gap = 760, 200, 46, 11, 14
        H = top + len(rows) * (3 * bh + gap) + 90
        sx = (W - left - 50) / 100.0
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, sans-serif" font-size="12">',
             f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
             f'<text x="{left}" y="20" font-size="13" fill="#222">{L["title"]}</text>']
        for k in range(0, 101, 10):
            x = left + k * sx
            o.append(f'<line x1="{x:.1f}" y1="{top-6}" x2="{x:.1f}" y2="{H-84}" stroke="#e3e3e3"/>')
            o.append(f'<text x="{x:.1f}" y="{H-70}" text-anchor="middle" fill="#666" font-size="11">{k}</text>')
        y = top
        for lab, (d, li, n, dom) in zip(L["conf"], rows):
            o.append(f'<text x="{left-8}" y="{y + 1.5*bh + 4:.1f}" text-anchor="end" fill="#222">{lab}</text>')
            for j, v in enumerate((d, li, n)):
                o.append(f'<rect x="{left}" y="{y + j*bh:.1f}" width="{v*sx:.1f}" height="{bh-1}" fill="{COL[j]}"/>')
                vs = f"{v:.1f}".replace(".", ",") if lang == "fr" else f"{v:.1f}"
                o.append(f'<text x="{left + v*sx + 4:.1f}" y="{y + j*bh + bh - 2:.1f}" font-size="10" fill="#333">{vs}</text>')
            xm = left + dom * sx
            o.append(f'<line x1="{xm:.1f}" y1="{y-2:.1f}" x2="{xm:.1f}" y2="{y + 3*bh + 1:.1f}" stroke="#111" stroke-width="2"/>')
            y += 3 * bh + gap
        ly = H - 50
        for j, s in enumerate(L["series"]):
            o.append(f'<rect x="{left + j*150}" y="{ly}" width="12" height="12" fill="{COL[j]}"/>')
            o.append(f'<text x="{left + j*150 + 18}" y="{ly+10}" fill="#222" font-size="11">{s}</text>')
        o.append(f'<line x1="{left + 5}" y1="{ly+21}" x2="{left + 5}" y2="{ly+35}" stroke="#111" stroke-width="2"/>')
        o.append(f'<text x="{left + 18}" y="{ly+32}" fill="#222" font-size="11">{L["mark"]}</text>')
        o.append("</svg>")
        fn = "frontieres.svg" if lang == "fr" else "frontieres_en.svg"
        open(os.path.join(outdir, fn), "w", encoding="utf-8").write("\n".join(o) + "\n")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
