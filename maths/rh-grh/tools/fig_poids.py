#!/usr/bin/env python3
"""Figure : poids dominés des grandes composantes selon trois pondérations (SVG, bibliothèque standard).

Usage : python3 -I fig_poids.py analysis/poids_composantes.csv analysis/fig
Écrit poids_trois_mesures.svg (français) et poids_trois_mesures_en.svg (anglais).
"""
import sys, os, csv

LAB = {
    "fr": {"title": "Poids dominé (%) selon trois mesures — composantes emboîtées, non additives",
           "series": ["déclarations", "lignes de l'export", "nœuds par déclaration"],
           "names": {"every_character_of_theta_integrals_local_matching": "cœur automorphe",
                     "nonempty_hyps_definite_side_of_closed_bound": "fabrication",
                     "vwin_of_row": "Tate–Shafarevich",
                     "topCovolSlim2_use_alt_alt": "covolume",
                     "galoisLocalGlobalStrong_recParameter": "représentations galoisiennes",
                     "offDiag": "théorème S"}},
    "en": {"title": "Dominated weight (%) under three measures — nested components, not additive",
           "series": ["declarations", "export lines", "nodes per declaration"],
           "names": {"every_character_of_theta_integrals_local_matching": "automorphic core",
                     "nonempty_hyps_definite_side_of_closed_bound": "manufacture",
                     "vwin_of_row": "Tate–Shafarevich",
                     "topCovolSlim2_use_alt_alt": "covolume",
                     "galoisLocalGlobalStrong_recParameter": "Galois representations",
                     "offDiag": "theorem S"}},
}
COL = ["#3a6ea5", "#a97a39", "#16866d"]

def main(src, outdir):
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    for lang, L in LAB.items():
        data = []
        for key, lab in L["names"].items():
            r = next(r for r in rows if r["nom"].endswith(key))
            data.append((lab, [float(r["pct_decl"]), float(r["pct_lignes"]), float(r["pct_noeuds"])]))
        W, left, top, bh, gap = 760, 210, 46, 11, 14
        H = top + len(data) * (3 * bh + gap) + 40
        sx = (W - left - 60) / 45.0
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, sans-serif" font-size="12">',
             f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
             f'<text x="{left}" y="20" font-size="13" fill="#222">{L["title"]}</text>']
        for k in range(0, 46, 5):
            x = left + k * sx
            o.append(f'<line x1="{x:.1f}" y1="{top-6}" x2="{x:.1f}" y2="{H-34}" stroke="#e3e3e3"/>')
            o.append(f'<text x="{x:.1f}" y="{H-20}" text-anchor="middle" fill="#666" font-size="11">{k}</text>')
        y = top
        for lab, vals in data:
            o.append(f'<text x="{left-8}" y="{y + 1.5*bh + 4:.1f}" text-anchor="end" fill="#222">{lab}</text>')
            for j, v in enumerate(vals):
                o.append(f'<rect x="{left}" y="{y + j*bh:.1f}" width="{v*sx:.1f}" height="{bh-1}" fill="{COL[j]}"/>')
                vs = f"{v:.1f}".replace(".", ",") if lang == "fr" else f"{v:.1f}"
                o.append(f'<text x="{left + v*sx + 4:.1f}" y="{y + j*bh + bh - 2:.1f}" font-size="10" fill="#333">{vs}</text>')
            y += 3 * bh + gap
        lx = W - 230
        for j, s in enumerate(L["series"]):
            o.append(f'<rect x="{lx}" y="{top + 120 + j*18}" width="12" height="12" fill="{COL[j]}"/>')
            o.append(f'<text x="{lx+18}" y="{top + 130 + j*18}" fill="#222" font-size="11">{s}</text>')
        o.append("</svg>")
        fn = "poids_trois_mesures.svg" if lang == "fr" else "poids_trois_mesures_en.svg"
        open(os.path.join(outdir, fn), "w", encoding="utf-8").write("\n".join(o) + "\n")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
