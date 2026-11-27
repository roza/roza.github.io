#!/usr/bin/env python3
"""Figure : concentration du noyau gamma dans une fenêtre d'échelles (Landau en fenêtres).

Usage : python3 -I fig_landau.py DOSSIER   ; écrit landau_fenetres.svg et landau_fenetres_en.svg
Modèle : densité de U/L où U suit la loi gamma q(u) = σ^{k+1} u^k e^{-σu} / k!, avec L = log Y
et k+1 ≈ σ(1+λ)L/2, pour que la moyenne tombe au milieu de la fenêtre [1, λ] (en unités de L).
Illustration du mécanisme de localisation, non preuve du critère. Bibliothèque standard seule.
"""
import sys, os, math

SIGMA, LAM = 2.0, 1.5
LAB = {"fr": ("log Y = {L}", "u / log Y", "fenêtre", "densité normalisée de U / log Y"),
       "en": ("log Y = {L}", "u / log Y", "window", "normalized density of U / log Y")}

def density(t, L):
    k = round(SIGMA * (1 + LAM) * L / 2) - 1
    u = t * L
    lq = (k + 1) * math.log(SIGMA) + k * math.log(u) - SIGMA * u - math.lgamma(k + 1)
    return L * math.exp(lq), k

def panel(x0, L, lab):
    W, H, l, b = 330, 230, 40, 40
    ts = [0.65 + i * (1.2 / 400) for i in range(401)]
    ys = [density(t, L)[0] for t in ts]; k = density(1.0, L)[1]
    ymax = max(ys) * 1.1
    X = lambda t: x0 + l + (t - 0.65) / 1.2 * (W - l - 10)
    Y = lambda y: 20 + (H - b - 20) * (1 - y / ymax)
    o = [f'<rect x="{X(1):.1f}" y="20" width="{X(LAM) - X(1):.1f}" height="{H - b - 20}" fill="#dcece5"/>',
         f'<text x="{(X(1) + X(LAM)) / 2:.1f}" y="34" text-anchor="middle" font-size="10" fill="#16866d">{lab[2]}</text>']
    pts = " ".join(f"{X(t):.1f},{Y(y):.1f}" for t, y in zip(ts, ys))
    o.append(f'<polyline points="{pts}" fill="none" stroke="#3a6ea5" stroke-width="2"/>')
    mean = (k + 1) / (SIGMA * L)
    o.append(f'<line x1="{X(mean):.1f}" y1="20" x2="{X(mean):.1f}" y2="{H - b}" stroke="#a97a39" stroke-dasharray="4 3"/>')
    o.append(f'<line x1="{x0 + l}" y1="{H - b}" x2="{x0 + W - 10}" y2="{H - b}" stroke="#444"/>')
    for t in (0.75, 1.0, 1.25, 1.5, 1.75):
        o.append(f'<text x="{X(t):.1f}" y="{H - b + 14}" text-anchor="middle" font-size="10" fill="#555">{t:g}</text>')
    o.append(f'<text x="{x0 + l + (W - l) / 2:.1f}" y="{H - 8}" text-anchor="middle" font-size="11" fill="#222">{lab[1]}</text>')
    o.append(f'<text x="{x0 + l + (W - l) / 2:.1f}" y="14" text-anchor="middle" font-size="12" fill="#222">{lab[0].format(L=L)}, k = {k}</text>')
    return o

def main(outdir):
    for lang, lab in LAB.items():
        W, H = 700, 250
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, sans-serif">',
             f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
        o += panel(0, 20, lab) + panel(350, 200, lab)
        o.append("</svg>")
        fn = "landau_fenetres.svg" if lang == "fr" else "landau_fenetres_en.svg"
        open(os.path.join(outdir, fn), "w", encoding="utf-8").write("\n".join(o) + "\n")

if __name__ == "__main__":
    main(sys.argv[1])
