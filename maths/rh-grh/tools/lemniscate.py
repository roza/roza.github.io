#!/usr/bin/env python3
"""Le modèle de la lemniscate : divisibilité et taille des dérivées du sinus lemniscatique.

Usage : python3 -I lemniscate.py [N]
s(z) est défini par s(0)=0, s'(0)=1, s'^2 = 1 - s^4, d'où s'' = -2 s^3. Si s(z) = Σ A_n z^n / n!,
  A_{n+2} = -2 Σ_{i+j+k=n} n!/(i! j! k!) A_i A_j A_k,
et les A_n sont des entiers, nuls sauf pour n ≡ 1 (mod 4). Le script affiche, pour quelques n :
la taille log|A_n|, la divisibilité totale Σ_p v_p(A_n) log p, la part des premiers p ≡ 3 (mod 4)
(inertes dans Q(i)) et le rapport de cette part à la taille ; puis la factorisation de A_41 (un premier
47 272 527 433 ≡ 1 mod 4 y figure), la constante de Darboux |A_n|/(n! (√2/ϖ)^(n+1)) = 4 le long de
n ≡ 1 (mod 4), et le profil théorique I(n) des couches impaires. Bibliothèque standard seule.
"""
import sys
from math import comb, log, lgamma, gamma, sqrt, pi, exp

def lemniscate(N):
    A = [0] * (N + 1)
    if N >= 1: A[1] = 1
    for n in range(N - 1):
        if (n + 2) % 4 != 1: continue
        A[n + 2] = -2 * sum(comb(n, i) * comb(n - i, j) * A[i] * A[j] * A[n - i - j]
                            for i in range(1, n + 1, 4) for j in range(1, n - i + 1, 4)
                            if (n - i - j) % 4 == 1)
    return A

def val(a, p):
    k = 0
    while a % p == 0: a //= p; k += 1
    return k

def primes(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** .5) + 1))]

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 401
    A = lemniscate(N)
    assert [A[1], A[5], A[9]] == [1, -12, 3024]
    print("n\tlog|A_n|\tlog n!\tdiv. totale\tdiv. inertes\tinertes/taille")
    for n in range(81, N + 1, 80):
        a = abs(A[n]); P = primes(n)
        tot = sum(val(a, p) * log(p) for p in P)
        ine = sum(val(a, p) * log(p) for p in P if p % 4 == 3)
        print(f"{n}\t{log(a):.1f}\t{lgamma(n + 1):.1f}\t{tot:.1f}\t{ine:.1f}\t{ine / log(a):.3f}")
    for p in (3, 7, 5, 13):
        print(f"p={p} : v_p(A_n)/n pour n=161 : {val(abs(A[161]), p) / 161:.3f} ; taux p/(p²-1) = {p / (p * p - 1):.3f}")
    # Un premier décomposé dans A_41 : 47 272 527 433 ≡ 1 (mod 4).
    a = abs(A[41]); f = {}
    for p in primes(200):
        while a % p == 0: a //= p; f[p] = f.get(p, 0) + 1
    print("A_41 =", " · ".join(f"{p}^{e}" for p, e in f.items()), "·", a, f"(cofacteur ≡ {a % 4} mod 4)")
    # Darboux : quatre pôles simples ±(1±i)ϖ/2, résidus de module 1, en phase pour n ≡ 1 (mod 4).
    w = gamma(0.25) ** 2 / (2 * sqrt(2 * pi)); c = sqrt(2) / w
    for n in range(101, N + 1, 100):
        print(f"n={n} : |A_n| / (n! (√2/ϖ)^(n+1)) = {exp(log(abs(A[n])) - lgamma(n + 1) - (n + 1) * log(c)):.7f}")
    # Profil théorique des couches impaires : I(n) = ½ n log n + O(n).
    P = primes(N)
    I = sum(log(p) * sum(N // p ** e for e in range(1, 64, 2)) for p in P if p % 4 == 3)
    print(f"I({N})/log|A_{N}| = {I / log(abs(A[N])):.4f} ; (I - ½ N log N)/N = {(I - N * log(N) / 2) / N:.3f}")
