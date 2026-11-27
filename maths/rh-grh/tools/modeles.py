"""Calculs des modèles réduits de synthese.md (bibliothèque standard seule)."""
import math, sys, os

def primes(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b"\0\0"
    for i in range(2, int(n**.5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n + 1) if s[i]]

def vp_fact(n, p):
    v, q = 0, p
    while q <= n: v += n // q; q *= p
    return v

def tcheb(ns):
    P = primes(2 * max(ns))
    print("n | theta(2n)-theta(n) | log C(2n,n) | n log 4 | sum_{p<=2n} v_p log p")
    for n in ns:
        th = sum(math.log(p) for p in P if n < p <= 2 * n)
        lc = math.lgamma(2*n+1) - 2*math.lgamma(n+1)
        tot = sum((vp_fact(2*n, p) - 2*vp_fact(n, p)) * math.log(p) for p in P)
        print(f"{n} | {th:.1f} | {lc:.1f} | {n*math.log(4):.1f} | {tot:.1f}")

def detail(n):
    P = primes(2 * n)
    print(f"C({2*n},{n}) = {math.comb(2*n,n)}")
    print(" ".join(f"{p}^{vp_fact(2*n,p)-2*vp_fact(n,p)}" for p in P if vp_fact(2*n,p)-2*vp_fact(n,p)))

def theta_vs(ns):
    P = primes(max(ns))
    for x in ns:
        th = sum(math.log(p) for p in P if p <= x)
        print(f"x={x}: theta={th:.1f}  x log4={x*math.log(4):.1f}  x={x}")

if __name__ == "__main__":
    tcheb([10, 100, 1000, 10**4, 10**5, 10**6]); detail(10); theta_vs([100, 1000, 10**4, 10**5, 10**6])

def riesz(ys):
    """S(y)=sum Lambda(n)(y/n-1) contre log floor(y)! (Legendre) et y log y-(1+gamma)y."""
    g = 0.5772156649015329
    for y in ys:
        P = primes(y); S = 0.0
        for p in P:
            q = p
            while q <= y: S += math.log(p) * (y / q - 1); q *= p
        print(f"y={y}: S={S:.1f}  log y!={math.lgamma(y+1):.1f}  ylogy-(1+g)y={y*math.log(y)-(1+g)*y:.1f}  diff={math.lgamma(y+1)-S:.1f}  gamma*y={g*y:.1f}")

def svg_profil(n, path):
    """Profil p -> v_p(C(2n,n)) (barres) contre la cible 1_{n<p<=2n}."""
    P = primes(2 * n); W, H, L, B = 640, 260, 46, 40
    sx = (W - L - 20) / (2 * n); vm = max(vp_fact(2*n,p)-2*vp_fact(n,p) for p in P); sy = (H - B - 40) / vm
    X = lambda t: L + t * sx; Y = lambda v: H - B - v * sy
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif" font-size="12">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<rect x="{X(n):.1f}" y="{Y(1):.1f}" width="{n*sx:.1f}" height="{sy:.1f}" fill="#f4d9b0"/>']
    for v in range(1, vm + 1):
        o.append(f'<line x1="{L}" x2="{W-20}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#ddd"/>')
        o.append(f'<text x="{L-8}" y="{Y(v)+4:.1f}" text-anchor="end">{v}</text>')
    for p in P:
        v = vp_fact(2*n, p) - 2*vp_fact(n, p)
        if v:
            col = "#2b5c8a" if p > n else "#b0413e"
            o.append(f'<rect x="{X(p)-2:.1f}" y="{Y(v):.1f}" width="4" height="{v*sy:.1f}" fill="{col}"/>')
        else:
            o.append(f'<circle cx="{X(p):.1f}" cy="{Y(0):.1f}" r="2" fill="#999"/>')
    o.append(f'<line x1="{L}" x2="{W-20}" y1="{Y(0)}" y2="{Y(0)}" stroke="black"/>')
    for t in (0, n//2, n, 3*n//2, 2*n):
        o.append(f'<text x="{X(t):.1f}" y="{H-B+16}" text-anchor="middle">{t}</text>')
    o.append(f'<text x="{(L+W-20)/2}" y="{H-6}" text-anchor="middle">p (premier)</text>')
    o.append(f'<text x="14" y="{H/2}" transform="rotate(-90 14 {H/2})" text-anchor="middle">v_p(C({2*n},{n}))</text>')
    o.append(f'<text x="{X(1.5*n):.1f}" y="{Y(1)-8:.1f}" text-anchor="middle" fill="#8a5a1a">cible : indicatrice de ]n, 2n]</text>')
    o.append(f'<text x="{L+60}" y="18" fill="#b0413e">rouge : premiers « parasites » (p ≤ n)</text>')
    o.append(f'<text x="{L+330}" y="18" fill="#2b5c8a">bleu : premiers visés</text>')
    o.append('</svg>')
    open(path, "w").write("\n".join(o))

# ---------- Question 2 : multiplication complexe et divisibilité ----------
from fractions import Fraction

def count_points(p):
    """#E(F_p) pour y^2 = x^3 - x (affine + point à l'infini)."""
    sq = [0] * p
    for y in range(p): sq[y*y % p] += 1
    return 1 + sum(sq[(x*x*x - x) % p] for x in range(p))

def hasse(p):
    """Invariant de Hasse : coefficient de x^(p-1) dans (x^3-x)^((p-1)/2) mod p."""
    m = (p - 1) // 2
    # (x^3 - x)^m = x^m (x^2-1)^m ; coefficient de x^(p-1) <=> x^(p-1-m) dans (x^2-1)^m
    k = p - 1 - m
    if k % 2: return 0
    j = k // 2
    return (math.comb(m, j) * (-1) ** (m - j)) % p

def a_n(N):
    """Coefficients a_n de L(E,s), E : y^2 = x^3 - x (conducteur 32)."""
    P = primes(N); ap = {p: (p + 1 - count_points(p)) if p != 2 else 0 for p in P}
    a = [0] * (N + 1); a[1] = 1
    for n in range(2, N + 1):
        m, p = n, None
        for q in P:
            if m % q == 0: p = q; break
        k, r = 0, n
        while r % p == 0: r //= p; k += 1
        # a_{p^k}
        if p == 2: apk = 0
        else:
            u, v = 1, ap[p]
            for _ in range(k - 1): u, v = v, ap[p] * v - p * u
            apk = v
        a[n] = apk * a[r]
    return a

def vp(x, p):
    if x == 0: return math.inf
    x = Fraction(x); v = 0; n, d = x.numerator, x.denominator
    while n % p == 0: n //= p; v += 1
    while d % p == 0: d //= p; v -= 1
    return v

def mul(A, B, N):
    C = [Fraction(0)] * (N + 1)
    for i, x in enumerate(A):
        if x:
            for j in range(0, N + 1 - i):
                if B[j]: C[i + j] += x * B[j]
    return C

def reverse(L, N):
    """Série réciproque E de L (L = X + ...), à l'ordre N : L(E(T)) = T."""
    E = [Fraction(0)] * (N + 1); E[1] = Fraction(1)
    for n in range(2, N + 1):
        # coefficient n de L(E) avec E tronqué ; on corrige E[n]
        S = [Fraction(0)] * (N + 1); Pw = E[:]
        tot = Fraction(0)
        for k in range(1, n + 1):
            if k > 1: Pw = mul(Pw, E, n)
            if L[k]: tot += L[k] * Pw[n]
        E[n] -= tot
    return E

def derivees(L, p, N):
    """v_p(D^a exp_F(0)) = v_p(a! * coeff_a(exp_F)), pour a <= N."""
    E = reverse(L, N)
    return [(a, vp(math.factorial(a) * E[a], p)) for a in range(1, N + 1) if E[a]]

def log_courbe(N):
    a = a_n(N); return [Fraction(0)] + [Fraction(a[n], n) for n in range(1, N + 1)]

def log_honda(p, N, h):
    L = [Fraction(0)] * (N + 1); e = 0
    while p ** (h * e) <= N: L[p ** (h * e)] = Fraction(1, p ** e); e += 1
    return L

def svg_retenu(N, path, inertes=(3, 7, 11), decomposes=(5, 13)):
    """Part de Legendre conservée : v_p(D^a exp_E(0)) / v_p(a!) en fonction de a."""
    E = reverse(log_courbe(N), N)
    W, H, L, B, R = 640, 300, 50, 44, 150
    X = lambda a: L + a * (W - L - R) / N; Y = lambda r: H - B - r * (H - B - 20) / 1.25
    col = {3: "#2b5c8a", 7: "#4f8fc0", 11: "#8bb8dd", 5: "#b0413e", 13: "#e08a7e"}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif" font-size="12">',
         f'<rect width="{W}" height="{H}" fill="white"/>']
    o.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(0)+3}" y2="{Y(0)+3}" stroke="black"/>')
    for r in (0, .25, .5, .75, 1, 1.25):
        o.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(r):.1f}" y2="{Y(r):.1f}" stroke="#ddd"/>')
        o.append(f'<text x="{L-8}" y="{Y(r)+4:.1f}" text-anchor="end">{r:g}</text>')
    ly = 30
    for p in tuple(inertes) + tuple(decomposes):
        pts = []
        for a in range(1, N + 1):
            if E[a] and vp_fact(a, p) >= 2:
                pts.append((a, vp(math.factorial(a) * E[a], p) / vp_fact(a, p)))
        o.append('<polyline fill="none" stroke="%s" stroke-width="%s" points="%s"/>' % (col[p], 1.5 if p in inertes else 4, " ".join(f"{X(a):.1f},{Y(r):.1f}" for a, r in pts)))
        if p in inertes:
            o.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(p/(p+1)):.1f}" y2="{Y(p/(p+1)):.1f}" stroke="{col[p]}" stroke-dasharray="4 3"/>')
        lab = f"p = {p} ({'inerte' if p in inertes else 'décomposé'})"
        o.append(f'<rect x="{W-R+12}" y="{ly-9}" width="12" height="3" fill="{col[p]}"/><text x="{W-R+30}" y="{ly-4}">{lab}</text>'); ly += 20
    o.append(f'<text x="{W-R+12}" y="{ly+6}" fill="#555">tirets : p/(p+1)</text>')
    for a in range(0, N + 1, 40):
        o.append(f'<text x="{X(a):.1f}" y="{H-B+16}" text-anchor="middle">{a}</text>')
    o.append(f'<text x="{(L+W-R)/2}" y="{H-8}" text-anchor="middle">ordre de dérivation a</text>')
    o.append(f'<text x="14" y="{(H-B)/2+10}" transform="rotate(-90 14 {(H-B)/2+10})" text-anchor="middle">v_p(D^a) / v_p(a!)</text>')
    o.append('</svg>'); open(path, "w").write("\n".join(o))

# ---------- Question 3 : Stepanov ----------
def stepanov_S(p, g=lambda x: x**3 - x):
    """|S| = #{x in F_p : g(x) carré non nul}."""
    sq = set((y * y) % p for y in range(1, p))
    return sum(1 for x in range(p) if g(x) % p in sq)

def stepanov_borne(p, m, a):
    """Borne schématique |S| <= p/2 + (m+1)/2 (p/a + a)."""
    return p / 2 + (m + 1) / 2 * (p / a + a)

def svg_equilibre(path, P, cf, cm, xlab, titre_f, titre_m, amin=1, amax=None, ylab="excès sur le terme principal"):
    """Courbes cf*P/a, cm*a et leur somme, abscisse logarithmique sur [amin, amax]."""
    amax = amax or 10 * P; W, H, L, B, R, T = 640, 300, 64, 44, 20, 24
    lx0, lx1 = math.log10(amin), math.log10(amax)
    tot = lambda a: cf * P / a + cm * a
    ymax = max(tot(amin), tot(amax)) * 1.05
    X = lambda a: L + (math.log10(a) - lx0) / (lx1 - lx0) * (W - L - R)
    Y = lambda v: H - B - v / ymax * (H - B - T)
    pts = [10 ** (lx0 + i * (lx1 - lx0) / 300) for i in range(301)]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif" font-size="12">', f'<rect width="{W}" height="{H}" fill="white"/>']
    step = 10 ** math.floor(math.log10(ymax / 4)); k = step
    while k < ymax:
        o.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(k):.1f}" y2="{Y(k):.1f}" stroke="#eee"/><text x="{L-6}" y="{Y(k)+4:.1f}" text-anchor="end">{k:g}</text>')
        k += step * (2 if ymax / step > 8 else 1)
    for f, c, w in ((lambda a: cf * P / a, "#2b5c8a", 1.5), (lambda a: cm * a, "#b0413e", 1.5), (tot, "black", 2.5)):
        o.append('<polyline fill="none" stroke="%s" stroke-width="%s" points="%s"/>' % (c, w, " ".join(f"{X(a):.1f},{Y(f(a)):.1f}" for a in pts)))
    a0 = math.sqrt(cf * P / cm)
    o.append(f'<line x1="{X(a0):.1f}" x2="{X(a0):.1f}" y1="{Y(0)}" y2="{Y(tot(a0)):.1f}" stroke="#888" stroke-dasharray="4 3"/>')
    o.append(f'<text x="{X(a0):.1f}" y="{Y(tot(a0))-10:.1f}" text-anchor="middle">optimum {xlab} ≈ {a0:.0f}, somme ≈ {tot(a0):.0f}</text>')
    o.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(0)}" y2="{Y(0)}" stroke="black"/>')
    t = 10 ** math.ceil(lx0)
    while t <= amax:
        o.append(f'<text x="{X(t):.1f}" y="{H-B+16}" text-anchor="middle">{t:g}</text>'); t *= 10
    o.append(f'<text x="{(L+W-R)/2}" y="{H-8}" text-anchor="middle">{xlab} (échelle logarithmique)</text>')
    o.append(f'<text x="14" y="{(H-B)/2+10}" transform="rotate(-90 14 {(H-B)/2+10})" text-anchor="middle">{ylab}</text>')
    ly = T + 4; lx = (L + W - R) / 2 - 90
    for c, lab in (("#2b5c8a", titre_f), ("#b0413e", titre_m), ("black", "somme")):
        o.append(f'<rect x="{lx}" y="{ly-8}" width="14" height="3" fill="{c}"/><text x="{lx+20}" y="{ly-3}">{lab}</text>'); ly += 18
    o.append('</svg>'); open(path, "w").write("\n".join(o))

# ---------- Question 4 : le côté archimédien ----------
def q4_stirling(ns):
    """log C(2n,n) (exact) contre Stirling et contre la prédiction n log 4."""
    for n in ns:
        lc = math.lgamma(2*n+1) - 2*math.lgamma(n+1)
        st = n*math.log(4) - 0.5*math.log(math.pi*n)
        print(f"n={n}: logC={lc:.4f}  Stirling={st:.4f}  nlog4={n*math.log(4):.4f}  ecart={lc-n*math.log(4):.4f}")

def bernoulli(N):
    B = [Fraction(0)] * (N + 1); B[0] = Fraction(1)
    for m in range(1, N + 1):
        B[m] = -sum(math.comb(m + 1, k) * B[k] for k in range(m)) / (m + 1)
    return B

def masse_unimodulaire(n):
    """Masse des réseaux unimodulaires pairs de rang n (n ≡ 0 mod 8), formule de Siegel."""
    B = bernoulli(n)
    m = abs(B[n // 2]) / n
    for j in range(1, n // 2):
        m *= abs(B[2 * j]) / (4 * j)
    return m

def periode_cm(K=200000):
    """∫_1^∞ dx/√(x³−x) = ∫_0^∞ 2 du/√((1+u²)(2+u²)) (x = 1+u²), puis u = tan t."""
    s, h = 0.0, (math.pi / 2) / K
    for i in range(K):
        t = (i + 0.5) * h; u = math.tan(t)
        s += 2 / math.sqrt((1 + u*u) * (2 + u*u)) / math.cos(t) ** 2 * h
    return s

# ---------- Question 5 : l'équilibre et la taille réelle des fluctuations ----------
ZEROS = [14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
         37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478]

def G_values(Y, npts=1500):
    """G(y) = S(y) − y log y + (1+γ)y aux entiers y, échantillonnés logarithmiquement."""
    g = 0.5772156649015329
    lam = [0.0] * (Y + 1)
    for p in primes(Y):
        q, lp = p, math.log(p)
        while q <= Y: lam[q] = lp; q *= p
    ys = sorted(set(int(round(10 ** (1 + i * (math.log10(Y) - 1) / npts))) for i in range(npts + 1)))
    out, A, psi, k = [], 0.0, 0.0, 0
    for y in range(1, Y + 1):
        A += lam[y] / y; psi += lam[y]
        if k < len(ys) and y == ys[k]:
            out.append((y, y * A - psi - y * math.log(y) + (1 + g) * y)); k += 1
    return out

def zeros_pred(y, nz=10):
    s = 0
    for t in ZEROS[:nz]:
        rho = complex(.5, t)
        s += -2 * (y ** rho / (rho * (rho - 1))).real
    return s

def svg_fluct(path, data):
    W, H, L, B, R, T = 640, 280, 60, 44, 20, 20
    lx0, lx1 = math.log10(data[0][0]), math.log10(data[-1][0])
    c0 = math.log(2 * math.pi)
    vals = [(v - c0) / math.sqrt(y) for y, v in data]
    pred = [zeros_pred(y) / math.sqrt(y) for y, _ in data]
    ym = 0.05
    X = lambda y: L + (math.log10(y) - lx0) / (lx1 - lx0) * (W - L - R)
    Y = lambda v: T + (ym - max(-ym, min(ym, v))) / (2 * ym) * (H - B - T)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif" font-size="12">', f'<rect width="{W}" height="{H}" fill="white"/>']
    for v in (-0.04, -0.02, 0, 0.02, 0.04):
        o.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{"#999" if v == 0 else "#eee"}"/><text x="{L-6}" y="{Y(v)+4:.1f}" text-anchor="end">{v:g}</text>')
    o.append('<polyline fill="none" stroke="#b0413e" stroke-width="1.2" stroke-dasharray="4 2" points="%s"/>' % " ".join(f"{X(y):.1f},{Y(v):.1f}" for (y, _), v in zip(data, pred)))
    o.append('<polyline fill="none" stroke="#2b5c8a" stroke-width="1.4" points="%s"/>' % " ".join(f"{X(y):.1f},{Y(v):.1f}" for (y, _), v in zip(data, vals)))
    k = math.ceil(lx0)
    while 10 ** k <= data[-1][0]:
        o.append(f'<text x="{X(10**k):.1f}" y="{H-B+16}" text-anchor="middle">10{str(k).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))}</text>'); k += 1
    o.append(f'<text x="{(L+W-R)/2}" y="{H-8}" text-anchor="middle">y (échelle logarithmique)</text>')
    o.append(f'<text x="14" y="{(H-B)/2+10}" transform="rotate(-90 14 {(H-B)/2+10})" text-anchor="middle">(G(y) − log 2π) / √y</text>')
    o.append(f'<rect x="{W-R-250}" y="{T+4}" width="14" height="3" fill="#2b5c8a"/><text x="{W-R-230}" y="{T+9}">calculé sur les premiers</text>')
    o.append(f'<rect x="{W-R-250}" y="{T+22}" width="14" height="3" fill="#b0413e"/><text x="{W-R-230}" y="{T+27}">prédit par les 10 premiers zéros</text>')
    o.append('</svg>'); open(path, "w").write("\n".join(o))

# ---------- Figures de la version 3 (portées en bibliothèque standard) ----------
BLUE, TEAL, AMBER, GRAY = "#245b8a", "#008477", "#b56b21", "#5b6670"

class Panel:
    """Repère cartésien dans un SVG : data -> pixels."""
    def __init__(self, x0, y0, w, h, xr, yr, equal=False):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        (a, b), (c, d) = xr, yr
        if equal:
            s = min(w / (b - a), h / (d - c)); cx, cy = (a + b) / 2, (c + d) / 2
            a, b = cx - w / s / 2, cx + w / s / 2; c, d = cy - h / s / 2, cy + h / s / 2
        self.xr, self.yr = (a, b), (c, d); self.o = []
    def X(self, x): a, b = self.xr; return self.x0 + (x - a) / (b - a) * self.w
    def Y(self, y): c, d = self.yr; return self.y0 + self.h - (y - c) / (d - c) * self.h
    def line(self, pts, col, w=1.5, dash=None, fill=None, op=1):
        p = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in pts)
        tag = "polygon" if fill else "polyline"
        self.o.append(f'<{tag} points="{p}" fill="{fill or "none"}" fill-opacity="{op}" stroke="{col if not fill else "none"}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
    def dot(self, x, y, col, r=3):
        self.o.append(f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r}" fill="{col}"/>')
    def rect(self, x, y, w, h, col, op=1):
        self.o.append(f'<rect x="{self.X(x):.1f}" y="{self.Y(y+h):.1f}" width="{self.X(x+w)-self.X(x):.1f}" height="{self.Y(y)-self.Y(y+h):.1f}" fill="{col}" fill-opacity="{op}"/>')
    def axes(self, xt, yt, xl="", yl="", title="", grid=True, fmt=lambda v: f"{v:g}"):
        o = []; a, b = self.xr; c, d = self.yr
        for t in yt:
            if grid: o.append(f'<line x1="{self.x0}" x2="{self.x0+self.w}" y1="{self.Y(t):.1f}" y2="{self.Y(t):.1f}" stroke="#eee"/>')
            o.append(f'<text x="{self.x0-6}" y="{self.Y(t)+4:.1f}" text-anchor="end">{fmt(t)}</text>')
        for t in xt:
            o.append(f'<text x="{self.X(t):.1f}" y="{self.y0+self.h+16}" text-anchor="middle">{fmt(t)}</text>')
        o.append(f'<line x1="{self.x0}" x2="{self.x0+self.w}" y1="{self.y0+self.h}" y2="{self.y0+self.h}" stroke="#8795a0"/>')
        o.append(f'<line x1="{self.x0}" x2="{self.x0}" y1="{self.y0}" y2="{self.y0+self.h}" stroke="#8795a0"/>')
        if xl: o.append(f'<text x="{self.x0+self.w/2:.1f}" y="{self.y0+self.h+34}" text-anchor="middle">{xl}</text>')
        if yl: o.append(f'<text x="{self.x0-40}" y="{self.y0+self.h/2:.1f}" transform="rotate(-90 {self.x0-40} {self.y0+self.h/2:.1f})" text-anchor="middle">{yl}</text>')
        if title: o.append(f'<text x="{self.x0+self.w/2:.1f}" y="{self.y0-8}" text-anchor="middle" font-size="13">{title}</text>')
        self.o = o + self.o

def svg_write(path, W, H, panels, extra=()):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="#283748">',
         f'<rect width="{W}" height="{H}" fill="white"/>']
    for p in panels: o += p.o
    o += list(extra); o.append("</svg>"); open(path, "w").write("\n".join(o))

def legend(x, y, items):
    o = []
    for i, (col, lab, kind) in enumerate(items):
        yy = y + 18 * i
        o.append(f'<rect x="{x}" y="{yy-6}" width="16" height="{4 if kind=="l" else 10}" fill="{col}" fill-opacity="{0.35 if kind=="a" else 1}"/>')
        o.append(f'<text x="{x+22}" y="{yy+3}">{lab}</text>')
    return o

T3 = {
 "fr": dict(fact="Factorielle : ⌊x/n⌋", riesz="Riesz : (x/n − 1)₊", gap="Écart de profil", nx="rapport n/x", wpp="poids par puissance de premier",
            real="La courbe sur ℝ", f7="Sur 𝔽₇ : 7 points affines", raw="Gain brut a/pᵉ", cut="Après troncature (b = 3)", odd="Couches impaires retenues",
            pw="puissance du premier 3", gain="gain (unités de valuation)", tl="Les 8 points de ℤ² de norme 5", l1="L = ℤ² : covolume 1", l2="L′ : covolume 1/6",
            z=["1 paire de zéros", "3 paires de zéros", "10 paires de zéros"], spec="somme spectrale / √y"),
 "en": dict(fact="Factorial: ⌊x/n⌋", riesz="Riesz: (x/n − 1)₊", gap="Profile gap", nx="ratio n/x", wpp="weight per prime power",
            real="The curve over ℝ", f7="Over 𝔽₇: 7 affine points", raw="Raw gain a/pᵉ", cut="After truncation (b = 3)", odd="Odd layers kept",
            pw="power of the prime 3", gain="gain (valuation units)", tl="The 8 points of ℤ² of norm 5", l1="L = ℤ²: covolume 1", l2="L′: covolume 1/6",
            z=["1 pair of zeros", "3 pairs of zeros", "10 pairs of zeros"], spec="spectral sum / √y"),
}

def figures_v3(outdir, lang="fr"):
    t = T3[lang]; suf = "" if lang == "fr" else "_en"; P = lambda n: os.path.join(outdir, n + suf + ".svg")
    import os as _os
    # 1. profil_riesz
    p = Panel(70, 20, 600, 220, (0.125, 1.13), (0, 8.3))
    ts = [0.125 + i * (1.13 - 0.125) / 3000 for i in range(3001)]
    fl = [(u, math.floor(1 / u)) for u in ts]; rz = [(u, max(1 / u - 1, 0)) for u in ts]
    p.line(rz + fl[::-1], None, fill=AMBER, op=0.22)
    step = []
    for u, v in fl:
        if step and step[-1][1] != v: step.append((u, step[-1][1]))
        step.append((u, v))
    p.line(step, BLUE, 1.6); p.line(rz, TEAL, 2.4)
    p.axes([0.2, 0.4, 0.6, 0.8, 1.0], [0, 2, 4, 6, 8], t["nx"], t["wpp"])
    svg_write(P("profil_riesz"), 700, 290, [p], legend(470, 34, [(BLUE, t["fact"], "l"), (TEAL, t["riesz"], "l"), (AMBER, t["gap"], "a")]))
    # 2. courbe_deux_lectures
    a = Panel(60, 30, 300, 220, (-1.6, 2.6), (-2.9, 2.9), equal=True)
    for lo, hi in ((-1, 0), (1, 2.1)):
        xs = [lo + i * (hi - lo) / 400 for i in range(401)]
        up = [(x, math.sqrt(max(0, x ** 3 - x))) for x in xs]
        dn = [(x, -y) for x, y in up]
        a.line(up + dn[::-1] if lo < 0 else dn[::-1] + up, BLUE, 1.8)
    a.line([(a.xr[0], 0), (a.xr[1], 0)], GRAY, 0.5); a.line([(0, a.yr[0]), (0, a.yr[1])], GRAY, 0.5)
    a.axes([-1, 0, 1, 2], [-2, -1, 0, 1, 2], "x", "y", t["real"], grid=False)
    b = Panel(440, 30, 220, 220, (-0.5, 6.5), (-0.5, 6.5))
    for x in range(7):
        for y in range(7):
            if (y * y - x ** 3 + x) % 7 == 0: b.dot(x, y, TEAL, 6)
    b.axes(range(7), range(7), "x mod 7", "y mod 7", t["f7"])
    svg_write(P("courbe_deux_lectures"), 700, 300, [a, b])
    # 3. poids_3
    p = Panel(70, 20, 600, 200, (-0.6, 4.6), (0, 90))
    for k, e in enumerate(range(1, 6)):
        raw = 243 / 3 ** e; cut = max(raw - 3, 0); odd = cut * (e % 2)
        for dx, v, col in ((-0.26, raw, BLUE), (0, cut, "#a5b9cc"), (0.26, odd, TEAL)):
            if v > 0: p.rect(k + dx - 0.12, 0, 0.24, v, col)
    p.axes([], [0, 20, 40, 60, 80], t["pw"], t["gain"])
    ex = [f'<text x="{p.X(k):.1f}" y="{p.y0+p.h+16}" text-anchor="middle">3^{e} = {3**e}</text>' for k, e in enumerate(range(1, 6))]
    svg_write(P("poids_3"), 700, 270, [p], ex + legend(470, 34, [(BLUE, t["raw"], "b"), ("#a5b9cc", t["cut"], "b"), (TEAL, t["odd"], "b")]))
    # 4. theta_reseau
    p = Panel(60, 30, 300, 300, (-3.5, 3.5), (-3.5, 3.5), equal=True)
    r5 = math.sqrt(5); p.line([(r5 * math.cos(2 * math.pi * i / 200), r5 * math.sin(2 * math.pi * i / 200)) for i in range(201)], BLUE, 1.5, "5 4")
    for x in range(-3, 4):
        for y in range(-3, 4):
            p.dot(x, y, TEAL if x * x + y * y == 5 else "#b8c0c6", 6 if x * x + y * y == 5 else 3)
    p.axes(range(-3, 4), range(-3, 4), "a", "b", t["tl"], grid=False)
    svg_write(P("theta_reseau"), 420, 380, [p])
    # 5. division_reseau
    pans = []
    for x0, dx, dy, ttl, col in ((60, 1, 1, t["l1"], BLUE), (420, 1 / 3, 1 / 2, t["l2"], TEAL)):
        q = Panel(x0, 30, 240, 240, (-1.6, 1.6), (-1.6, 1.6))
        q.rect(0, 0, dx, dy, col, 0.2)
        for i in range(-6, 7):
            for j in range(-6, 7):
                if abs(i * dx) <= 1.55 and abs(j * dy) <= 1.55: q.dot(i * dx, j * dy, col, 3 if dx < 1 else 5)
        q.axes([-1, 0, 1], [-1, 0, 1], "", "", ttl); pans.append(q)
    svg_write(P("division_reseau"), 720, 310, pans)
    # 6. ondes_zeros
    p = Panel(80, 40, 600, 200, (3, 5), (-0.022, 0.022))
    xs = [3 + 2 * i / 2500 for i in range(2501)]
    for nz, col, w in ((1, GRAY, 1.0), (3, AMBER, 1.4), (10, BLUE, 2.0)):
        p.line([(u, sum(2 * math.cos(g * u * math.log(10)) / (g * g + 0.25) for g in ZEROS[:nz])) for u in xs], col, w)
    p.axes([3, 3.5, 4, 4.5, 5], [-0.02, -0.01, 0, 0.01, 0.02], "log₁₀ y", t["spec"])
    svg_write(P("ondes_zeros"), 720, 300, [p], legend(150, 16, [(GRAY, t["z"][0], "l")]) + legend(330, 16, [(AMBER, t["z"][1], "l")]) + legend(510, 16, [(BLUE, t["z"][2], "l")]))
