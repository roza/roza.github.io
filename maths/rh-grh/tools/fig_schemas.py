#!/usr/bin/env python3
"""Quatre schémas réels de la preuve, en Graphviz (FR et EN). Bibliothèque standard + `dot`.

Usage : python3 -I fig_schemas.py analysis/fig
Les noms et chiffres sont ceux lus sur l'export (25/11/2026) :
  - sommet      : everyCharacter_of_row, référents directs (analysis/points_entree.txt) ;
  - dominateurs : analysis/decl_spine.txt (épine dorsale et frères, poids en lignes de l'export) ;
  - dependances : query.py deps / cl Deduction.ch_balance, revindex.py up Deduction.ch_balance ;
  - interfaces  : analysis/interfaces.tsv (voisinage de Lnk.linkCore, poids dominés en lignes).
Écrit schema_sommet, schema_dominateurs, schema_dependances, schema_interfaces (.dot, .svg, et _en).
"""
import os, sys, subprocess

HEAD = ('digraph G {\n  graph [rankdir=%s, fontname="DejaVu Sans", nodesep=0.25, ranksep=0.32, bgcolor="white"];\n'
        '  node [fontname="DejaVu Sans", fontsize=10, shape=box, style="rounded,filled", fillcolor="#f7f7f7", color="#888888"];\n'
        '  edge [fontname="DejaVu Sans", fontsize=9, color="#555555", arrowsize=0.6];\n')
SPINE = 'fillcolor="#fff6dd", color="#c9a24a"'
THEO = 'fillcolor="#e5f4ee", color="#16866d"'
DEAD = 'style="rounded,dashed", fillcolor="#ffffff", color="#b55555", fontcolor="#b55555"'
LIB = 'fillcolor="#eaf1fa", color="#5089cc"'
IFACE = 'shape=ellipse, style=filled, fillcolor="#e8eefa", color="#5089cc"'

def T(fr, en): return {"fr": fr, "en": en}

def sommet(l):
    t = lambda fr, en: T(fr, en)[l]
    return HEAD % "TB" + f'''
  M [label="{t('Main : 5 énoncés', 'Main: 5 statements')}\\n(riemannHypothesis, …)", {SPINE}];
  A [label="allChi : EveryCharacter", {SPINE}];
  E [label="everyCharacter", {SPINE}];
  R [label="everyCharacter_of_row", {SPINE}];
  L [label="every_character_of_literature_of_vWin", {SPINE}];
  C [label="{t('cœur automorphe', 'automorphic core')}\\nevery_character_of_theta_integrals_local_matching", {SPINE}];
  F [label="{t('fabrication', 'construction')}\\nnonempty_hyps_definite_side_of_closed_bound", {SPINE}];
  G [label="{t('représentations galoisiennes', 'Galois representations')}\\ngaloisLocalGlobalStrong_recParameter", {THEO}];
  V [label="{t('Tate–Shafarevich', 'Tate–Shafarevich')}\\nvwin_of_row", {THEO}];
  Q [label="{t('Langlands local partiel', 'partial local Langlands')}\\nrecTExists", {THEO}];
  K [label="{t('covolume', 'covolume')}\\ntopCovolSlim2_use_alt_alt", {THEO}];
  S [label="{t('théorème S, masses de Siegel', 'Theorem S, Siegel masses')}\\n({t('un référent chacun, sous la fabrication', 'one referent each, under the construction')})", {THEO}];
  D [label="{t('échafaudage « littérature »', '“literature” scaffolding')}\\nLitN, published_inputs_combined,\\nPublished.LocalLanglandsGL\\n({t('hors fermeture', 'outside the closure')})", {DEAD}];
  M -> A -> E;
  E -> R; E -> G [label=" {t('injecté', 'plugged in')}"];
  R -> L [label=" ⟨h, recTExists, h⟩\\n {t('(constructeur anonyme)', '(anonymous constructor)')}"];
  R -> V; R -> Q;
  L -> C; L -> K;
  C -> F; F -> S [style=dashed];
  G -> Q [style=dotted, label=" {t('et 24 autres référents,', 'and 24 other referents,')}\\n {t('sous Galois et Ш', 'under Galois and Ш')}"]; V -> Q [style=dotted];
  {{rank=same; G; R}}
}}
'''

def dominateurs(l):
    t = lambda fr, en: T(fr, en)[l]
    pc = (lambda x: x.replace(".", ",")) if l == "fr" else (lambda x: x)
    nodes = [("R0", t("racine virtuelle\\n(5 énoncés de Main)", "virtual root\\n(5 statements of Main)"), "100", SPINE),
             ("A", "allChi", "99.3", SPINE), ("E", "everyCharacter", "99.3", SPINE),
             ("R", "everyCharacter_of_row", "76.6", SPINE), ("L", "every_character_of_literature_of_vWin", "66.3", SPINE),
             ("C", t("cœur automorphe", "automorphic core"), "41.5", SPINE),
             ("F", t("fabrication", "construction"), "35.8", SPINE),
             ("G", "galoisLocalGlobalStrong_recParameter", "6.3", THEO), ("V", "vwin_of_row", "8.2", THEO),
             ("K", "topCovolSlim2_use_alt_alt", "7.1", THEO), ("T", "toroidalForFanKS", "1.2", 'fillcolor="#f7f7f7"'),
             ("W", "theta_integrals_agree_…", "1.1", 'fillcolor="#f7f7f7"'),
             ("H", "hypotheses_nonempty_of_unramified_exponents_alt", "15.0", 'fillcolor="#f7f7f7"'),
             ("Ma", t("masses de Siegel", "Siegel masses") + "\\nlarge_unramified_exponent_bundles_exist_alt", "6.8", THEO),
             ("Gr", "every_character_of_green_v_win", "1.6", 'fillcolor="#f7f7f7"')]
    s = HEAD % "TB"
    for k, lab, p, st in nodes:
        s += f'  {k} [label="{lab}\\n{pc(p)} %", {st}];\n'
    for a, b in [("R0", "A"), ("A", "E"), ("E", "R"), ("E", "G"), ("R", "L"), ("R", "V"), ("L", "C"), ("L", "K"),
                 ("C", "F"), ("L", "T"), ("L", "W"), ("F", "H"), ("C", "Gr"), ("H", "Ma")]:
        s += f"  {a} -> {b};\n"
    s += "}\n"
    return s

def dependances(l):
    t = lambda fr, en: T(fr, en)[l]
    return HEAD % "TB" + f'''
  subgraph cluster_up {{ label="{t('ses utilisateurs : 13 liens, chacun à référent unique', 'its users: 13 links, each with a single referent')}"; fontname="DejaVu Sans"; fontsize=10; color="#cccccc"; style=rounded;
    U4 [label="allChi", {SPINE}];
    U3 [label="level_gm_le_on_family_scales", {SPINE}];
    U2 [label="core_gm", {SPINE}];
    U1 [label="ch_core", {SPINE}];
    U4 -> U3 [style=dashed, label=" {t('8 liens', '8 links')}"]; U3 -> U2 [style=dashed, label=" {t('2 liens', '2 links')}"]; U2 -> U1;
  }}
  X [label="Deduction.ch_balance\\nASK − MAIN = De\\n({t('fermeture : 34 253 décl. ; propre : 66', 'closure: 34,253 decl.; own: 66')})", fillcolor="#fde8d0", color="#c47a2c"];
  U1 -> X [style=dashed, label=" {t('2 liens, via CharacterBalanceMoves.core', '2 links, via CharacterBalanceMoves.core')}"];
  subgraph cluster_proj {{ label="{t('24 dépendances directes du projet', '24 direct dependencies in the project')}"; fontname="DejaVu Sans"; fontsize=10; color="#16866d"; style=rounded;
    P1 [label="askExp\\n({t('orthogonalité', 'orthogonality')})", {THEO}];
    P2 [label="HostFactsS\\n({t('ramification de l’hôte', 'ramification of the host')})", {THEO}];
    P3 [label="ASK, MAIN, De, GPsi", {THEO}];
    P4 [label="E0, InPhi, PhiSet, partner, …", {THEO}];
  }}
  subgraph cluster_lib {{ label="{t('314 dépendances directes de Lean et Mathlib', '314 direct dependencies in Lean and Mathlib')}"; fontname="DejaVu Sans"; fontsize=10; color="#5089cc"; style=rounded;
    B1 [label="ArithmeticFunction.vonMangoldt", {LIB}];
    B2 [label="AddChar, ZMod, Finset.sum", {LIB}];
    B3 [label="{t('instances algébriques', 'algebraic instances')}\\n(AddCommGroup, GroupWithZero, …)", {LIB}];
    B4 [label="Complex, Real", {LIB}];
  }}
  X -> P1; X -> P2; X -> P3; X -> P4; X -> B1; X -> B2; X -> B3; X -> B4;
}}
'''

def interfaces(l):
    t = lambda fr, en: T(fr, en)[l]
    I = lambda k, lab: f'  {k} [label="{lab}", {IFACE}];\n'
    th = lambda k, lab, w: f'  {k} [label="{lab}\\n{w}", fillcolor="#ffffff", color="#888888", fontsize=9];\n'
    s = HEAD % "TB"
    for k, lab in [("iLinkG", "LinkG"), ("iLinkS", "LinkS"), ("iLinkDIV", "LinkDIV"), ("iLinkIRR", "LinkIRR"), ("iLinkMu", "LinkMu"),
                   ("iLoss", "LossesSmallShares"), ("iLossFS", "LossFS"), ("iPlaces", "PlacesF"), ("iSlopesNF", "SlopesNF"),
                   ("iFrameReal", "FrameRealF"), ("iFrameF", "FrameF"), ("iLatF", "LatF"), ("iCountF", "CountF"),
                   ("iSlopesMF", "SlopesMF"), ("iWinF", "WinF"), ("iCharF", "CharF"), ("iChain", "ChainTied")]:
        s += I(k, lab)
    s += f'  core [label="linkCore\\n({t("14 entrées", "14 inputs")})", shape=box, style="filled", fillcolor="#fde8d0", color="#c47a2c", fontsize=11];\n'
    for k, lab, w in [("tG", "linkG_fam_noKer", "1,3 M" if l == "fr" else "1.3 M"), ("tS", "theoremS_link_of_evaluation", "47 k"),
                      ("tMu", "linkMu_of_linkDIV", "0,9 k" if l == "fr" else "0.9 k"), ("tLoss", "losses_of_small_share_weight", "392 k"),
                      ("tLossF", "lossF_of_7", "1,8 k" if l == "fr" else "1.8 k"), ("tPl", "placesF_min'", "196 k"), ("tSN", "slopesNF_of", "33 k"),
                      ("tFR", "frameRealF_of''", "83 k"), ("tFF", "frameF_of", "231 k"), ("tLat", "latF", "3,6 k" if l == "fr" else "3.6 k"),
                      ("tC", "countF_of", "17 k"), ("tSM", "slopesMF_of_count", "36 k"), ("tW", "size_windows_of_thick_set", "22 k"),
                      ("tCh", "charF", "20")]:
        s += th(k, lab, w)
    for a, b in [("tG", "iLinkG"), ("tS", "iLinkS"), ("iLinkDIV", "tMu"), ("tMu", "iLinkMu"),
                 ("iLinkG", "tLoss"), ("tLoss", "iLoss"), ("iLoss", "tLossF"), ("tLossF", "iLossFS"),
                 ("iLinkG", "tPl"), ("iLinkMu", "tPl"), ("tPl", "iPlaces"), ("iPlaces", "tSN"), ("tSN", "iSlopesNF"),
                 ("iLinkS", "tFR"), ("iLinkDIV", "tFR"), ("iLinkIRR", "tFR"), ("tFR", "iFrameReal"),
                 ("iFrameReal", "tFF"), ("iLatF", "tFF"), ("tFF", "iFrameF"), ("iLinkDIV", "tLat"), ("tLat", "iLatF"),
                 ("tC", "iCountF"), ("iCountF", "tSM"), ("tSM", "iSlopesMF"), ("tW", "iWinF"), ("tCh", "iCharF"),
                 ("iLossFS", "core"), ("iSlopesNF", "core"), ("iFrameF", "core"), ("iLatF", "core"), ("iCountF", "core"),
                 ("iSlopesMF", "core"), ("iWinF", "core"), ("iCharF", "core"), ("iLinkDIV", "core"), ("iLinkIRR", "core"),
                 ("core", "iChain")]:
        s += f"  {a} -> {b};\n"
    s += "}\n"
    return s

def raccord(l):
    t = lambda fr, en: T(fr, en)[l]
    return HEAD % "TB" + f'''
  F [label="frame_at_of\\n({t('la donnée réelle D entre ici', 'the actual datum D enters here')})", {SPINE}];
  J [label="joint_a_ramified_holds", {SPINE}];
  TF [label="TheoremF\\n({t('énoncé général, ∀ B', 'general statement, ∀ B')})", {SPINE}];
  BK [label="DivData.Bk (D7.div D)\\n({t('un seul champ : Bk u : V(Nu u) → V(RR)^∨', 'a single field: Bk u : V(Nu u) → V(RR)^∨')})", fillcolor="#fde8d0", color="#c47a2c"];
  P1 [label="{t('intégralité', 'integrality')}\\nmap (B i) (N i) ≤ cc", {IFACE}];
  P2 [label="{t('hauteur', 'height')}\\nhtMap (B i) ≤ h i", {IFACE}];
  P3 [label="{t('rang', 'rank')}\\nBall i = Y′⁻¹ · toMatrix (B i) · Y i", {IFACE}];
  F -> J [label=" B := Bk"]; J -> TF [style=dashed, label=" {t('4 liens', '4 links')}"];
  BK -> P1; BK -> P2; BK -> P3;
  P1 -> TF; P2 -> TF; P3 -> TF;
  {{rank=same; P1; P2; P3}}
}}
'''

def main(out):
    for name, f in [("schema_sommet", sommet), ("schema_dominateurs", dominateurs),
                    ("schema_dependances", dependances), ("schema_interfaces", interfaces),
                    ("schema_raccord", raccord)]:
        for l in ("fr", "en"):
            base = os.path.join(out, name + ("" if l == "fr" else "_en"))
            open(base + ".dot", "w", encoding="utf-8").write(f(l))
            subprocess.run(["dot", "-Tsvg", base + ".dot", "-o", base + ".svg"], check=True)
            print(base + ".svg")

if __name__ == "__main__":
    main(sys.argv[1])
