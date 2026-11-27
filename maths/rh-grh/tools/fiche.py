#!/usr/bin/env python3
"""Fiche d'une structure (ou d'un inductif à un constructeur) : paramètres, champs nommés et leurs types.

Usage : python3 -I fiche.py OUT NOM [--width N] [--ctor NOM_DU_CONSTRUCTEUR]
Le constructeur est NOM.mk par défaut. Ses binders se lisent sur le télescope de son type : les premiers
sont les paramètres de la structure (autant que de binders dans le type de NOM), les suivants sont les
champs, dans l'ordre, avec leur nom et leur type (rendu dans le contexte des binders précédents).
Pour chaque champ, la projection NOM.champ est signalée si elle existe dans l'export. Bibliothèque standard.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lexpr


def main():
    a = sys.argv[1:]
    width = 400
    if "--width" in a:
        i = a.index("--width"); width = int(a[i + 1]); del a[i:i + 2]
    ctor = None
    if "--ctor" in a:
        i = a.index("--ctor"); ctor = a[i + 1]; del a[i:i + 2]
    OUT, S = a[0], a[1]
    E = lexpr.load(OUT)
    ctor = ctor or S + ".mk"
    sid, cid = E.byname.get(S), E.byname.get(ctor)
    if sid is None or cid is None:
        sys.exit(f"{S} ou {ctor} : inconnu dans l'export")
    npar = len(E.telescope_full(sid)[0])
    t = E.troot[cid]; ctx = []; i = 0
    print(f"### {S}   (constructeur {ctor}, {npar} paramètre(s))")
    print("type :", E.render(E.troot[sid], [], width))
    while E.KIND(t) == 5:
        nm = lexpr.fresh(lexpr.clean(E.name(E.PAY(t))), ctx)
        bi = E.BI(t); br = {0: "()", 1: "{}", 2: "⦃⦄", 3: "[]"}[bi]
        ty = E.render(E.C1[t], ctx, width)
        if i < npar:
            print(f"  param  {br[0]}{nm}{br[1]} : {ty}")
        else:
            proj = S + "." + nm
            mark = "" if proj in E.byname else "   (pas de projection nommée)"
            print(f"  champ {i - npar + 1:>2} {br[0]}{nm}{br[1]} : {ty}{mark}")
        ctx.append(nm); t = E.C2[t]; i += 1
    print(f"  ⊢ {E.render(t, ctx, width)}")


if __name__ == "__main__":
    import threading
    sys.setrecursionlimit(1_000_000); threading.stack_size(512 * 1024 * 1024)
    th = threading.Thread(target=main); th.start(); th.join()
