#!/usr/bin/env python3
"""Tests de non-régression des outils, sans l'export (bibliothèque standard seule).

Usage : python3 -I tools/tests.py [--rapide]
  1. frontiere.py --test : le losange (G_B garde D, la suppression le perd) ;
  2. lemniscate.py : A_1, A_5, A_9 et le taux v_3(A_161)/161 ;
  3. modeles.py : Legendre, #E(F_p) pour y²=x³-x, table v_3(D^a exp_E(0)) de l'article (§ 6.2),
     masses de Siegel (E_8, rang 16), constante de la lemniscate ;
  4. poids.py sur analysis/decl_domtree.tsv.gz : les pourcentages publiés
     (analysis/poids_composantes.txt) sont retrouvés (sauté avec --rapide ou sans l'arbre) ;
  5. analysis/checksums.sha256 : les fichiers présents ont l'empreinte enregistrée ;
  6. trace_app.py sur everyCharacter_of_row, si l'extraction export/out_sol est présente.
Code de sortie 0 si tout passe.
"""
import sys, os, subprocess, hashlib, math, re
from fractions import Fraction

T = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(T, "..", "analysis")
sys.path.insert(0, T)
ok = True

def check(nom, cond, detail=""):
    global ok
    print(("OK    " if cond else "ÉCHEC ") + nom + (f" ({detail})" if detail else ""))
    ok &= bool(cond)

def run(*a, timeout=3600):
    return subprocess.run([sys.executable, "-I", *a], capture_output=True, text=True, timeout=timeout)

# 1. frontières : le losange
r = run(os.path.join(T, "frontiere.py"), "--test")
check("frontiere.py --test (losange)", r.returncode == 0 and "OK" in r.stdout, r.stdout.strip() or r.stderr[-200:])

# 2. lemniscate
import lemniscate as L
Al = L.lemniscate(161)
check("lemniscate : A_1, A_5, A_9", [Al[1], Al[5], Al[9]] == [1, -12, 3024])
check("lemniscate : A_n = 0 hors n ≡ 1 (mod 4)", all(Al[n] == 0 for n in range(162) if n % 4 != 1))
r3 = L.val(abs(Al[161]), 3) / 161
check("lemniscate : v_3(A_161)/161 ≈ 0,373", abs(r3 - 0.373) < 5e-4, f"{r3:.4f}")
check("lemniscate : v_5(A_161) = 0", L.val(abs(Al[161]), 5) == 0)
check("lemniscate : A_41 a le facteur premier 47272527433 ≡ 1 (mod 4)", abs(Al[41]) % 47272527433 == 0 and 47272527433 % 4 == 1
      and all(47272527433 % q for q in range(2, 217425)))
wl = math.gamma(0.25) ** 2 / (2 * math.sqrt(2 * math.pi))
dc = math.exp(math.log(abs(Al[161])) - math.lgamma(162) - 162 * math.log(math.sqrt(2) / wl))
check("lemniscate : |A_161| = 4·161!·(√2/ϖ)^162 (Darboux)", abs(dc - 4) < 1e-6, f"{dc:.7f}")

# 3. modèles réduits
import modeles as M
check("Legendre : v_2(100!) = 97, v_3 = 48, v_5 = 24", (M.vp_fact(100, 2), M.vp_fact(100, 3), M.vp_fact(100, 5)) == (97, 48, 24))
check("#E(F_p) = p+1 pour p ≡ 3 (mod 4)", all(M.count_points(p) == p + 1 for p in M.primes(200) if p % 4 == 3))
check("#E(F_7) = 8", M.count_points(7) == 8)
dv = dict(M.derivees(M.log_courbe(161), 3, 161))
attendu = {9: 3, 25: 9, 49: 18, 81: 30, 121: 45, 161: 61}
check("table § 6.2 : v_3(D^a exp_E(0))", all(dv.get(a) == v for a, v in attendu.items()),
      " ".join(f"{a}:{dv.get(a)}" for a in attendu))
check("masse E_8 = 1/696729600", M.masse_unimodulaire(8) == Fraction(1, 696729600))
m16 = Fraction(1, 970864271032320000) + Fraction(1, 685597979049984000)
check("masse rang 16 = 691/277667181515243520000", M.masse_unimodulaire(16) == m16 == Fraction(691, 277667181515243520000))
w = math.gamma(0.25) ** 2 / (2 * math.sqrt(2 * math.pi))
check("∫_1^∞ dx/√(x³−x) = ϖ", abs(M.periode_cm(20000) - w) < 1e-6, f"{w:.6f}")

# 4. poids dominés publiés
dom = os.path.join(A, "decl_domtree.tsv.gz")
if "--rapide" in sys.argv or not os.path.exists(dom):
    print("SAUTÉ poids.py (arbre des dominateurs absent ou --rapide)")
else:
    r = run(os.path.join(T, "poids.py"), dom, "--set", os.path.join(A, "composantes.txt"))
    pub = open(os.path.join(A, "poids_composantes.txt"), encoding="utf-8").read()
    lignes = lambda s: [re.findall(r"[\d.]+%", l) for l in s.splitlines() if l.count("%") == 3]
    check("poids.py : pourcentages publiés retrouvés", r.returncode == 0 and lignes(r.stdout) == lignes(pub),
          f"{len(lignes(pub))} lignes")

# 6. trace_app.py (seulement si l'extraction de l'export est présente)
OUTX = os.path.join(T, "..", "export", "out_sol")
if "--rapide" in sys.argv or not os.path.exists(os.path.join(OUTX, "c1.u32")):
    print("SAUTÉ trace_app.py (extraction absente ou --rapide)")
else:
    r = run(os.path.join(T, "trace_app.py"), OUTX, "UpperTheory.FinalTheorems.everyCharacter_of_row", timeout=1800)
    o = r.stdout
    check("trace_app : 3 occurrences dans everyCharacter_of_row", "3 occurrences relevées" in o and "3 retenues" in o)
    check("trace_app : champs du constructeur anonyme", all(k in o for k in
          ("(caraianiLocalGlobalDual) := h", "(localLanglandsExists) := UpperTheory.Zero.LLC.recTExists", "(galoisRepOfPolarizedPairLit) := h")))
    r = run(os.path.join(T, "fiche.py"), OUTX, "Formalism.BasicNotions.DivData", timeout=1800)
    check("fiche : DivData a un seul champ d'applications Bk (champ 3)", "champ  3 (Bk)" in r.stdout and "champ 10 (delP_le_one)" in r.stdout)
    r = run(os.path.join(T, "trace_app.py"), OUTX, "GlobalTheory.T.recursive_page_lattice_bound", "--outline", "--width", "200", timeout=1800)
    check("trace_app --outline : alias suivi et étape clé QAt", "qAt_run" in r.stdout and "quotientBound_of_kill_detect_constantRoom" in r.stdout)
    r = run(os.path.join(T, "trace_app.py"), OUTX, "UpperTheory.FinalTheorems.everyCharacter_of_row", "--slice", "every_character_of_literature_of_vWin:hV", timeout=1800)
    check("trace_app --slice : hV ⟸ vwin_of_row h, frontière h", "application de UpperTheory.One.vwin_of_row" in r.stdout and "[frontière : lieur λ de la déclaration]" in r.stdout)

# 5. empreintes
n = bad = 0
for l in open(os.path.join(A, "checksums.sha256"), encoding="utf-8"):
    h, f = l.split(maxsplit=1); f = f.strip()
    for base in (A, os.path.join(A, "..", "export")):
        p = os.path.join(base, f)
        if os.path.exists(p):
            n += 1
            d = hashlib.sha256()
            with open(p, "rb") as fh:
                for b in iter(lambda: fh.read(1 << 24), b""): d.update(b)
            if d.hexdigest() != h: bad += 1; print("   empreinte différente :", f)
            break
check("checksums.sha256", bad == 0, f"{n} fichiers présents vérifiés")

print("\nTOUT PASSE" if ok else "\nDES TESTS ÉCHOUENT")
sys.exit(0 if ok else 1)
