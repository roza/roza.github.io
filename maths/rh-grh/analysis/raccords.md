# Lectures et contrôles sur l'export (expériences E1–E22, 25–27/11/2026)

Outil : `tools/trace_app.py` (graphe des applications instanciées), sur la base `export/out_sol` extraite de l'export du 21/11/2026. Chaque résultat se reproduit par la commande indiquée. Niveaux de raccord : 1 localisation, 2 instanciation, 3 typage (identité syntaxique ou égalité explicite), 4 reconstruction écrite, 5 explication. Aucune conversion définitionnelle n'est vérifiée par l'outil ; les identités annoncées sont des identités de nœuds ou de champs.

Les expériences E15 à E18 sont des **contrôles** plus que des raccords. Elles utilisent aussi `inertes.py` (clauses inertes), `occ.py` et `frontiere_donnees.py` (frontière en données), et `modmap_src.py` (fichiers source d'un export). E18 porte sur un autre export, celui de la preuve courte.

**Sommaire.**

| | Objet | Résultat en une ligne |
|---|---|---|
| Contrôle | `everyCharacter_of_row` | la même preuve remplit deux champs « littérature » |
| E1 | `key_identity5` | conversion par dépliage : les trois compensations |
| E2 | `goal_of_shape_of_hyps` | `HypsAlt` branche 40 certificats et 6 données |
| E3 | trois cartes | identité par construction (un seul champ `Bk`) |
| E4 | `gapA` → $G_\psi$ | identité `gmA_eq` et bornes individuelles |
| E5, bis, ter | gains `LinkG` | admissibilité (Théorème A) et rang $p$-adique `LPprime` |
| E6, bis | pages | étape « tuer, détecter » reconstruite |
| E7, bis | Ш → `LinkN` | le défaut local est un module de congruences |
| E8 | programme de flot | couches impaires |
| E9 | fonctionnelles CM | droite cible lue par tranchage arrière |
| E10, E11 | `LPprime` | assemblage reconstruit ; modules de Weyl et bases de poids |
| E12, E13 | `NoRel` | le paquet de Behrend est inerte ; l'hôte porte la propriété |
| E14 | Théorème B des arcs | coût quadratique des suites de lettres épaisses |
| E15 | clauses inertes | 5 729 théorèmes livrent une conclusion jamais lue |
| E16 | objections de Nielsen | géométrie vide, isolée derrière des propositions |
| E17 | record de comptabilité | les onze hypothèses = (A1)–(A7), (H) de Nelson ; (A4), (A5), (H) sortent de `LinkDIV` |
| E18 | preuve courte de Sernau | même architecture, noms nouveaux ; carte et poids par dossier |
| E19 | bilan original exact | la pente cible se compense ; `ErrX5at` est la somme des erreurs des entrées |
| E20 | bilan court exact | `star_inequality` est le modèle à trois réels de l'Atelier 6, nom pour nom |
| E21 | divergence | même rôle (covolume cible), deux producteurs : Arakelov contre déterminant de chaîne et Selmer |
| E22 | transformation recertifiée | `Data.enough_forms` allégé de deux clauses inertes, recompilé ; défaut de `inertes.py` corrigé |

Le tableau « Synthèse », en fin de document, donne le niveau atteint pour chaque raccord.

## Cas de contrôle : `everyCharacter_of_row`

`python3 -I tools/trace_app.py export/out_sol UpperTheory.FinalTheorems.everyCharacter_of_row --types`

Trois occurrences. Le constructeur anonyme de `OpenLiteratureStatements` reçoit `caraianiLocalGlobalDual := h`, `localLanglandsExists := recTExists`, `galoisRepOfPolarizedPairLit := h` : **la même preuve `h` (la ligne galoisienne) remplit deux champs « littérature »**, et `vwin_of_row h` en tire la borne de Ш. Niveau 3.

## E1. `key_identity5` (témoin)

`python3 -I tools/trace_app.py export/out_sol Formalism.LFunctionChainParameters.WeightedSlopeBounds.key_identity5 --types`

Le terme pose `h := Data.key_identity D C hv hf u0 hw`, puis conclut par `linear_combination h`. La conclusion de `key_identity` contient `abelian₂` et `L`, et un terme `2·logGam/(f·k)` ; celle de `key_identity5` contient `Lam5` et `La`. Après dépliage de `Lam5` et `abelian₂` (définitions lues par `show.py --value`), le terme `cCount·(La + m²La/k)` figure des deux côtés de `key_identity5` et s'annule : l'identité vaut pour toute valeur du champ `La` (champ 8 de `Data`, distinct de `L`, champ 7). La compensation effective est dans `key_identity` ; le passage est une **conversion par dépliage**, sans lemme d'identification nommé (cas 1 de suggestions7bis). Niveau 4.

## E2. `goal_of_shape_of_hyps` : comment `HypsAlt` instancie le mécanisme

`python3 -I tools/trace_app.py export/out_sol GlobalTheory.Fc.goal_of_shape_of_hyps --all --json …` puis `UpperTheory.Top.shape_closed_link_n_of_green`.

`goal_of_shape_of_hyps : TopShapeAlt V NR N G → V → NR → HypsAlt N … → G` est un **branchement pur** : l'hypothèse `t : TopShapeAlt …` se déplie en une fonction à 53 paramètres, appliquée aux champs de `HypsAlt`. 42 champs passent tels quels, sous leur nom ; `hDivG` et `hServ` passent par `Iff.mp`, `rRows` par `Closed.imp` ; 8 paramètres (`sel`, `selS`, `selP`, `selDH`, `selC`, `selB`, `hVC`, `nR`) sont construits à partir des deux champs de données `σ` et `𝒜` (sélections de familles). Le témoin de `TopShapeAlt` est fourni par `UpperTheory.Top.shape_closed_link_n_of_green : Green → TopShapeAlt True True (Closed LinkN) TopG`, qui distribue les paramètres aux théorèmes de liaison :

| Théorème de liaison | Conclusion (`Closed …`) | Champs de `HypsAlt` consommés |
|---|---|---|
| `link_alt_alt_bis` | `LinkS` | `sTy`, `sNG`, `sM`, `sLp`, `sO`, `h30`, `c30`, `hc30`, `hWu`, `hRF`, `hTF`, `hInstR` (théorème S) |
| `link_gl` | `LinkGLOBAL` | `hU`, `hG` (masses), `tie`, `hduty` |
| `closed_family_admissible_twist_link_alt` | `adm2` (parties quadratiques locales admissibles) | `aPt0`, `aPtTw`, `aPer0`, `aPerTw`, `aP10`, `aAtG`, `hServ` (lignes servies du Théorème A) |
| `closed_linkIRR_of_join_count` | `LinkIRR` | `cIc`, `hcI`, `irrC` |
| `closed_linkEta_of_duty` | `LinkEta` | `hduty` |
| `link_alt_alt_alt` | `SmallLevelRankEq` | `hLamP`, `hDivG`, `zL`, sélections |
| `link_brest_alt` | `RemainingDivisionBounds` | `rRows`, `tie`, `hRB`, `hDivG`, `hDcPtG`, sélections |
| `selection_closed_of_wu_decay_alt` | `ComplementCountFamily` | `hWu`, `hRF`, `jOn`, `selJ`, `rRows` |
| `wire_sel_alt` | `SingleMapCondition` | `hTw`, `hPA`, `hDivG`, `hDcPtG`, `selB` |
| `designExists_of_tuSize_aux4n_litThin` | `DesignExists` | `cT`, `hEx`, `hLit`, `hduty` |
| `Pk.Closed.sub`, `topDesWin` | — | `hTu`, `hn4` ; `nRest` |

Les champs se répartissent, d'après la sorte de leur type (`Prop` ou `Type`, lue sur le télescope de `HypsAlt.mk`), en **6 données** (`𝒜`, la classe de familles ; `σ`, la sélection ; `cT : ℝ → ℝ → ℝ` ; `c30 : List ℝ → CountingConstants` ; `selJ`, une sélection dépendante ; `cIc : ℝ`) et **40 certificats** (39 propositions, plus `nRest : N(…)` avec `N` à valeurs dans `Prop`). Correction (suggestions8, § 5) : une version antérieure annonçait 2 données et 44 certificats. Niveau 2 (instanciation complète) ; le sens de chaque lien reste à lire.

## E3. Le raccord des trois cartes (intégralité, hauteur, rang)

`show.py Formalism.HN.TheoremF` ; `revindex.py up Formalism.LFunctionChainParameters.MatrixLatticeEstimates.flat_lattice_theorem_holds` ; `trace_app.py … Formalism.MainNotions.Lnk.frame_at_of --callee joint_a_ramified_holds --implicit`.

Dans l'énoncé de `TheoremF`, **la même famille `B i : V i →ₗ W`** porte les trois propriétés : intégralité (`Submodule.map (B i) (N i) ≤ cc`), hauteur (`htMap (b i) (X i) b' X' (B i) ≤ h i`) et rang (la matrice `Ball i` est définie comme `Y'⁻¹ · toMatrix(B i) · Y i` en la place v, et entre dans la condition de corang `frK`/`frQ`). Le chemin d'usage est `TheoremF` ← `theoremF` ← `flat_lattice_theorem_holds` ← `ramification_condition_holds` ← `joint_a_ramified_holds` ← `frame_at_of` ← `frameF_of` ← … ← `link_gl`. Là où la donnée réelle entre (`frame_at_of`), `B` est instancié par **`DivData.Bk (D7.div D)`**, les réseaux sources par `HLat.L (DivData.Nu …)`, le réseau cible par `HLat.dualL (DivData.RR …)`, les hauteurs par `DivData.h`. `DivData.mk` a un seul champ d'applications : `Bk u : V(Nu u) →ₗ Dual(V RR)`, l'accouplement des périodes. Le raccord des trois cartes de [R2] est donc, dans Lean, **une identité par construction**, garantie par le typage (cas 1). La question mathématique restante n'est pas de raccorder trois cartes, mais de montrer que le `Bk` fabriqué satisfait les trois propriétés (`FrameReal_at`, `Lat_at`, `NuFull`). Par ailleurs, la fabrication impose explicitement une condition de carte unique sur les réalisations (`SingleMapCondition`, `IndefiniteRealisationBoundedRows.oneMap`, E2). Niveau 3.

## E4. De `gapA` à la majoration de $G_\psi$

`show.py UpperTheory.Comparison₂.core_gm Formalism.HC.EAtH.mk UpperTheory.Comparison₂.gmA_eq UpperTheory.Comparison₂.sigA_le UpperTheory.Comparison₂.charsA` ; `trace_app.py … core_gm`.

`core_gm` déduit `Level.Gm Λ x ≤ x^{1/2+(eD+eL+7)ε}` de `CoreAtH` (la borne de chaîne) et de `EAtH`, dont le constructeur exige : `o_eq` ; `KeptInXp`, `ExceptionalCharacterKept` (les caractères gardés du niveau sont dans le groupe de caractères de l'hôte) ; `Shares φ TT (x^{-1+ε})` (échantillonnage des classes par les colonnes selon `Frame.lam`, profil 4 : 3) ; `BoundedCharsPointwise` (bornes ponctuelles des caractères non gardés) ; `bdL` ($|L'/L(1,\chi)|\le C\log x$). La déduction tient en trois lemmes : `gmA_eq` établit que la combinaison produite par la somme sur les colonnes, pondérée par $1/(3o+1)$ sur les caractères gardés, est **identiquement** `Level.Gm Λ y` ; `sigA_le` borne les caractères parasites **un par un** par `EAtH.bdG` puis somme ($\le 4o\,x^{1/2+\varepsilon}$) ; `charsA` contrôle les caractères gardés. Il n'y a pas d'erreur de moyenne : la cible est la combinaison positive elle-même, sur laquelle Landau opère, et les parasites sont bornés individuellement. Niveau 3, avec une reconstruction écrite possible.

## E5. La fabrication des gains (`LinkG`)

`show.py Formalism.L2.G.linkG_fam_noKer Formalism.MainNotions.G.gam Formalism.MainNotions.G.cap Formalism.MainNotions.G.FirstTheoremAtFamily Formalism.MainNotions.G.SecondTheoremAtFamily --value` ; `trace_app.py … Formalism.L2.G.link_of_local_closed --callee …`.

`gam p = p/(p²−1)` ; `cap` est un seuil défini par blocs de segments, `A0 + Σ_{i<l}(coarseA − oEff)`. `linkG_fam_noKer` conclut `LinkG` de dix hypothèses : `SecondTheoremAtFamily` (une borne de valuation le long des orbites, `OrbitValuationBound`), `FirstTheoremAtFamily` (`Conclusion2Family`), `La > 0`, `Ce ≥ 1`, `CbLarge`, `TrivialStabiliserFiniteClasses`, `StdSubAt`, `Adm2F` (alimenté par les lignes servies du Théorème A, E2), `NPDescF`, `FamilyWindowLogBound`. Son unique consommateur, `link_of_local_closed`, les tire toutes d'**un seul paquet local `h`** par projections `And.left`/`And.right` ; les deux théorèmes viennent de `second_theorem_absolute_constant (extremal_projector_tools_of_loc h) (local_model_results h)` et de `first_theorem_threshold_functions (…, loc8All_of (…, local_model_results h, local_flatness_results h))`. Provenance établie (niveau 2) ; la réalisation mathématique des profils tronqués reste à lire dans ces trois familles de résultats locaux.

## E6. Les « pages »

`show.py GlobalTheory.T.recursive_page_lattice_bound GlobalTheory.RunJoin.PageOK Formalism.L2.Pj.recPJ --value`.

Une page est un **étage $j<m$** de la chaîne (`InR D j`, avec $j<$ `Ranks.m (D7.R D)`). `recPJ h j` construit la donnée d'étage (`PJ`) à partir d'un système `Pj.Top` : familles de poids `Wt D j`, points `PtA T j` au-dessus des places d'un corps de coefficients, images `imgV`, valuations `vAtV`. `recursive_page_lattice_bound` transforme, étage par étage, une condition de réseau `LatAt` en une borne de quotient `QAt` (constantes 7 et 4), sous `PageOK` ; la construction est récursive (`recB`). Niveau 2.

## E5 bis. La chaîne des gains, lue jusqu'au bout (niveau 2–3)

Outils : `show.py --value` (`OrbitValuationBound`, `aux₃`, `Conclusion2Family`, `Conclusion2`, `LPprime`, `LPprimeAt`, `OrbitHyp`, `IsGoodOrbit`, `UnramifiedQuadraticSetting`, `OrbitLatticeBounds`, `LatticeSandwich`, `LPBaseChange`, `SplitConstantsUniformBound`) ; `trace_app.py --reading` (`linkG_fam_noKer`) ; `revindex.py up` et `path` (`thmAGauss`).

**Les deux théorèmes de famille ont la même conclusion, `LPprime`.** Le second (`OrbitValuationBound`, via `aux₃`) et le premier (`Conclusion2Family`, via `Conclusion2`) concluent `LPprime p n' ι σ w r lam0 t D κ cStar`, dans un cadre `UnramifiedQuadraticSetting` (extension non ramifiée de $\mathbb Q_p$ de Frobenius σ, anneau $O$ d'uniformisante $w$ avec $|O/w|=p^{2n'}$). `LPprime` dit : pour tout réseau $L$ de $\mathbb Q_q^{m+1}$, il existe des **arêtes** $e_i$ aboutissant à $L$ (`IsEdge p n' r` : voisins de Hecke en $p$) et des fonctionnelles $F_i$ attachées à leurs sources, telles que (séparation) pour toute autre arête $e'$ de même source, `Re(e')` multipliée par $w^{c^*}$ tombe dans $F_i$, et (rang) l'accouplement entre les $F_i$ et l'espace cible est de rang $\ge(1-\kappa)\dim$ à la précision $p^D$ (`GoodRankK`). Les paramètres : troncature $t$, précision $D$, proportion κ, poids `lam0` sur $m+1$ étages, positions `TT`. Les hypothèses d'orbite (`OrbitHyp`, `IsGoodOrbit`) sont une condition de **pavage d'intervalles** le long de l'orbite de Frobenius (`GoodOrbitIntervalTileCondition`, `orbitWindowCount`), là où interviennent les ensembles sans relation courte.

**L'assemblage.** `OrbitLatticeBounds` affirme `LPprime` pour chaque mot $u$, chaque place $w$ de caractéristique $p$ et chaque position retenue $t_0$, avec $t=\lceil t_v\rceil$, $D=D_p$, $\kappa=\kappa_v$ ; il est produit par une **entrée de programmation linéaire** (`linear_programming_input_of_hypotheses`, à partir des deux théorèmes, `HypIAt`, `HypIIAt`) ; `LatticeSandwich` encadre le réseau, $\ell^{e_p}M_{\rm na}\subset M\subset M_{\rm na}$ ; `LPBaseChange` rend `LPprime` stable par extension finie des coefficients.

**Où entre le Théorème A.** `revindex.py path` : ni `local_model_results`, ni les deux théorèmes de famille n'utilisent `thmAGauss`. Son unique référent, `thmA_of`, sert `split_bound_eleven_one : SplitConstantsUniformBound 11 1` (pour toute donnée locale admissible, la conclusion du Théorème A avec une perte uniforme de constante 1, et un corollaire de constante 11). Cette borne est consommée par `sum_over_primes_service` → `closed_servF_of_servT_of_dGamSize` → `closed_family_admissible_twist_link_alt` (l'admissibilité `adm2` des lignes servies, qui alimente l'hypothèse `Adm2F` de `linkG_fam_noKer`), et par `rowTwU` → … → `hServ_of_linkR` (le champ `hServ` de `HypsAlt`). **Le Théorème A atteint donc `LinkG` par l'admissibilité, non par les théorèmes de rang.**

**Ce qui reste.** Les preuves de `LPprime` (premier et second théorèmes de famille, `local_model_results`, 1,26 M lignes en propre) et de l'entrée de programmation linéaire. Leur reconstruction demande la théorie des réseaux dans l'immeuble et des correspondances de Hecke en $p$.

## E5 ter. Le sens exact de `LPprime` (suggestions8, § 2)

`show.py --value --explicit` sur `GoodRankK`, `IsEdge`, `be`, `Re`, `Nsrc`, `Ntgt`, `Vsp`.

**Les arêtes.** `IsEdge p n' r e` : `src ⊂ tgt` sont deux réseaux, $p\cdot\mathrm{tgt}\subset\mathrm{src}$ et $[\mathrm{tgt}:\mathrm{src}]=p^{n'r}$. Ce sont des voisins de Hecke en $p$ (si le corps résiduel de $W$ a $p^{n'}$ éléments, ce que suggère le cadre sans que cela ait été vérifié, ce sont les sous-réseaux de codimension $r$ de $\mathrm{tgt}/p\,\mathrm{tgt}$ : les arêtes de type $r$ de l'immeuble de $\mathrm{GL}_{m+1}$).

**Les fonctionnelles.** Les $F_i$ vivent dans `Nsrc` (un réseau de polynômes en coordonnées de Weyl graduées, `Vsp`, dilaté par $w^{-t}$ et intersecté avec les `Re` des arêtes) ; la séparation demande $F_i\in w^{c^*}\mathrm{Re}(e')$ pour toute autre arête $e'$ de même source. L'accouplement est $\varphi_i(G)=G(p^{A_r}F_i)$ (`be`), pour $G$ dans le réseau dual cible `Ntgt(L)`.

**Le rang à précision.** `GoodRankK π A φ n D` : il existe $u:O^n\to A$ $O$-linéaire et $M$ à coefficients dans $O$ avec $M\,\Phi(u(x))=\pi^Dx$ pour tout $x$ ($\pi=p$ ici). **Lemme (démontré, niveau 4).** Pour $B=\Phi\circ u$ à coefficients entiers, la condition équivaut à : $B$ injective et ses $n$ facteurs invariants $s_i\le D$. Preuve par la forme de Smith (synthèse, § 3.5). Corollaire : $\operatorname{len}(\operatorname{im}B\bmod p^{D'})=\sum_i(D'-s_i)_+\ge n(D'-D)$ pour $D'\ge D$. `LPprime` demande $n\ge(1-\kappa)\dim$. **Non vérifié :** l'intégralité de l'accouplement réel ; sans elle, le lemme s'applique après mise à l'échelle.

**Ce qui reste.** La preuve de `LPprime` (rôle de `NoRel` et du pavage des orbites dans la séparation), et le programme linéaire d'`OrbitLatticeBounds` (variables, contraintes, certificat).

## E6 bis. Reconstruction de l'étape des pages (niveau 4, sur le corps commun ; voir la réserve et sa résolution)

Outils : `trace_app.py --outline --reading` (squelette et liste de lecture), `fiche.py`, `show.py --value`.

**Chaîne lue.** `recursive_page_lattice_bound := RunJoin.qAt_run` (alias). **Réserve (26/11).** La reconstruction suppose les fonctionnelles à valeurs dans des droites sur le corps de coefficients $K$. Si elles sont à valeurs dans des droites sur des extensions $K_{1,k}/K$, le noyau d'une fonctionnelle peut être de codimension $>1$ et l'argument du déterminant ne s'applique plus tel quel (contre-exemple : $x+\sqrt2\,y$ sur $\mathbb Q^2$). Il faut alors un corps commun avec détection après extension des scalaires, ou une famille stable par Galois. Voir la synthèse, § 5.5.

**Résolution (26/11).** `show.py --value` : `ArcCM.NumGood`, `DetectQ`, `KillQ`, `qbridge_of_numGood`, `Pj.QAt.QBridgeAt`, `FreeQuotientRank.KerCoreStatement`, `GaloisDescentStatement` ; `query.py deps` ; parcours de la valeur de `qbridge_of_numGood`. L'export fait la seconde réparation. `NumGood K₁ φ` porte sur `φ : V →ₗ[K] K₁`, $K_1$ quelconque, avec longueurs aux places $w$ de $K_1$ (indice de ramification) et normalisation par $[K_1:\mathbb Q]$. L'hypothèse de `qbridge_of_numGood` est : pour tout $F\notin W$, il existe $K_1$ et φ avec $W\le\ker\varphi$, $\varphi(F)\ne0$ et `NumGood`. Sa conclusion `QBridgeAt` fournit un $K_1$ **commun** et $\rho$ formes $K_1$-linéaires sur $K_1\otimes V$, de noyau commun exactement `baseSpan K₁ W`, avec les bornes locales et archimédiennes. Le passage se fait par `kerCore_holds : KerCoreStatement` (19 621 lignes propres). Pour une famille `Fam` de formes $V\to K_1$ qui s'annulent sur $W$, détectent sur $K$ et sont stables par plongement $e:K'\to K_1$, il existe $K_1$, $\rho$ et des $g_i\in$ `Fam` dont les extensions ont pour noyau commun $K_1\otimes W$, avec $\dim W+\rho=\dim V$. Ses dépendances : `IntermediateField.normalClosure`, `IsGalois.normalClosure`, `finiteDimensional_iSup_of_finite`, séparabilité, et `galoisDescent_holds : GaloisDescentStatement` (un sous-espace de $K_2\otimes V$ stable par Galois est `baseSpan` de ses $K$-points). La stabilité par plongement est démontrée dans `qbridge_of_numGood` (témoin `LinearMap.comp (AlgHom.toLinearMap e) f`). La reconstruction vaut donc sur le corps commun ; niveau 4 rétabli, sous cette forme. Non lus ligne à ligne : les preuves de `kerCore_holds`, `galoisDescent_holds` et `qat_of_bridge'`.

Le squelette de `qAt_run` montre que l'étape clé `key : QAt …` est justifiée par `quotientBound_of_kill_detect_constantRoom := ArcCM.qat_of_kill_detect` (alias), avec en entrée `ArcCM.Known` (le théorème CM, `arithmeticCMKnownTheorems_proof`). La liste de lecture de `qat_of_kill_detect` donne en propre `cmArcDatumFamily_functional_bounded_linear_on_cuspForms` (1,65 M lignes), `qbridge_of_numGood`, `qat_of_bridge'`, `room_of_bounds`, `log₂`, `NumGood`.

**Les objets, lus sur les définitions.** Un corps de nombres $K$ (`KO`) de degré $\delta$ ; l'espace $V$ des formes paraboliques de l'étage $j$ (`Cusp B j ka`) ; un réseau $M\subset V$ (`Mlat`, `LatAt` = `Submodule.IsLattice`) ; des tailles $S_\sigma(F)$ (`supN`) aux plongements $\sigma$, et $\mathrm{meanLogSup}(F)=\frac1\delta\sum_\sigma\log S_\sigma(F)$ ; un sous-espace $W$ (`MggK`) ; le quotient $Q$ (`Qm`), de rang $\rho$ (`rhoP`). `KillQ` et `DetectQ` disent ensemble que $W$ est **exactement** le noyau commun des fonctionnelles « coefficient du jet en un point CM » (`cfOf` d'une donnée d'arc). `NumGood(M,S,\mathfrak b,C_{\rm arch},B_{\rm deg},K_1,\varphi)` dit qu'il existe une droite hermitienne $N$ sur $K_1\supset K$, de degré normalisé $\le B_{\rm deg}$, telle que $\varphi(M)\subset\mathfrak b^{-1}I_N$ (en chaque place finie, avec l'indice de ramification) et $\|\varphi(F)\|_{N,\sigma}\le e^{C_{\rm arch}}S_\sigma(F)$.

**Proposition.** Supposons : (i) pour tout $F\in V\setminus W$, il existe $\varphi$ nulle sur $W$, avec $\varphi(F)\ne0$, satisfaisant `NumGood` pour les mêmes $\mathfrak b=\prod\lambda^{b(\lambda)}$, $C_{\rm arch}$, $B_{\rm deg}$ ; (ii) $\frac1\delta\sum_\lambda b(\lambda)\log N\lambda$ est borné. Alors, pour toute famille $t_1,\dots,t_\rho\in M$ dont les images engendrent $V/W$, le quotient $Q/\langle t_i\rangle$ a des longueurs locales $\ell_\lambda\le n(\lambda)+\rho\,b(\lambda)$, avec
$$\frac1\delta\sum_\lambda n(\lambda)\log N\lambda\;\le\;\sum_{i=1}^\rho\Big(\mathrm{meanLogSup}(t_i)+C_{\rm arch}+B_{\rm deg}+\tfrac12\log\rho\Big).$$

*Démonstration.* Choisissons, par (i) et par récurrence, $\varphi_1,\dots,\varphi_\rho$ nulles sur $W$ et linéairement indépendantes sur $V/W$ (si $\rho=0$ il n'y a rien à démontrer ; sinon, prendre $F_k\in\big(\bigcap_{l<k}\ker\varphi_l\big)\setminus W$, non vide par le théorème du rang, et la fonctionnelle que (i) lui associe ; correction suggestions8, § 4.3). L'application $\Phi=(\varphi_k)$ est injective sur $V/W$, donc sur $Q$, et la matrice $A=(\varphi_k(t_i))$ est inversible. Soit $\Delta=\det A$, section non nulle de la droite $\bigotimes_kN_k$ (sur un corps $K'$ contenant les $K_{1,k}$), de degré normalisé $\le\rho B_{\rm deg}$. Aux places finies, $\Phi(Q)\subset\bigoplus_k\mathfrak b^{-1}I_{N_k}$, donc la longueur de $Q/\langle t\rangle$ en $\lambda$ est au plus celle de $\bigoplus_k\mathfrak b^{-1}I_{N_k}/\Phi\langle t\rangle$, c'est-à-dire $\mathrm{ord}_\lambda(\Delta)-\mathrm{ord}_\lambda(\bigotimes I_{N_k})+\rho\,b(\lambda)$ ; on pose $n(\lambda)$ égal aux deux premiers termes. La formule du produit pour la section $\Delta$ donne $\frac1\delta\sum_\lambda n(\lambda)\log N\lambda=\widehat{\deg}_n(\textstyle\bigotimes N_k)+\frac1\delta\sum_\sigma\log\|\Delta\|_\sigma$. Le premier terme est $\le\rho B_{\rm deg}$. Pour le second, l'inégalité de Hadamard majore $|\det A|_\sigma$ par le produit des normes euclidiennes des colonnes, chacune au plus $\sqrt\rho\max_k\|\varphi_k(t_i)\|_\sigma\le\sqrt\rho\,e^{C_{\rm arch}}S_\sigma(t_i)$ ; en moyennant sur $\sigma$, $\frac1\delta\sum_\sigma\log\|\Delta\|_\sigma\le\sum_i(\mathrm{meanLogSup}(t_i)+C_{\rm arch})+\frac\rho2\log\rho$. $\square$

**Correspondance avec Lean.** L'hypothèse de `qbridge_of_numGood` est exactement $\mathrm{PPv}(C_h)\,\mathrm{size}+C_{\rm arch}+B_{\rm deg}+\frac12\log\rho\le\mathrm{PPv}(C_c)\,\mathrm{size}$ (borne par vecteur de la proposition), avec la borne des dénominateurs $\frac1\delta\sum b\log N\lambda\le\mathrm{PPv}(C_c)\,\mathrm{size}$ ; la conclusion de `QAt` est la forme intégrée, $\frac1\delta\sum n\log N\lambda\le\rho\,\mathrm{PPv}(C_c)\,\mathrm{size}$. Dans `qat_of_kill_detect`, $C_c=C_h+3C_0+C_d$ : $C_h$ pour les hauteurs des $t_i$, $3C_0$ pour les trois bornes de `RoomAt` ($C_{\rm arch}$, $B_{\rm deg}$, et discriminant plus $\log n$), $C_d$ pour $\log\dim$ (la perte de Hadamard). **La preuve Lean de l'étape déterminant (`qat_of_bridge'`, 186 k lignes) n'a pas été lue** : la proposition démontre la même conclusion à partir des mêmes hypothèses, ce qui suffit pour un niveau 4, sans affirmer que Lean suit ce chemin.

**Ce qui reste.** L'existence de fonctionnelles CM numériquement bonnes, avec $B_{\rm deg}$ relié à $\tfrac12\log\Omega$ par le théorème CM : c'est `cmArcDatumFamily_functional_bounded_linear_on_cuspForms` (1,65 M lignes) et `numGood_of_famQ`. La troisième articulation se réduit donc à cette existence.

## E7. Comment Ш entre dans `LinkN`

`show.py UpperTheory.GalC.linkN_of_twGood_galoisPreconditions GlobalTheory.NLink.ExtraAlt Formalism.MainNotions.PairedCharacterCondition.PairedCharacterConditionAlt Formalism.MainNotions.TwistedPlaces.vvTerm Formalism.MainNotions.TwistedPlaces.etaSum_le`.

μ_w est le champ 15 de `Rows.Data` (`muAt`, un uplet par place). `linkN_of_twGood_galoisPreconditions` prend le paquet `NLink.Hypotheses₂` et construit, pour chaque donnée coupée par un caractère (`cut D c`), une borne `ExtraAlt` = `CommutingEndomorphismCondition` ∧ `PairedCharacterConditionAlt`. Cette dernière porte sur les places locales dont la caractéristique ℓ est l'un des deux premiers de l'hôte $g(k)$, avec des représentations à valeurs dans GL, une décomposition semi-simple, des conditions de taille et la **finitude de `shaLen`** pour toutes les torsions $e<t$. `vvTerm(D, ℓ) = Σ_{e=1}^{t−1} shaLen(ℓ, e)·log ℓ` est indexé par **le premier ℓ**. La conclusion de `etaSum_le` majore la masse des places tordues de l'étage $j$ par des termes de taille, une somme sur l'**image** des places tordues par la caractéristique résiduelle (chaque ℓ compté une fois, avec `log ℓ · lamG(ℓ)`), et **`dZ0(j) · Σ_ℓ vvTerm(D, ℓ)`**. Ш entre donc une fois par premier, avec un **facteur de multiplicité explicite** `dZ0(j)` : ce n'est pas une injection conjointe des défauts locaux, mais un regroupement par caractéristique résiduelle avec multiplicité payée (deuxième scénario de suggestions7, § 4.1). Niveau 2 ; le lien entre un défaut local et les longueurs de Ш reste dans la preuve de `PairedCharacterConditionAlt`.

## E7 bis. Le défaut local est un module de congruences

Outils : `fiche.py Formalism.BasicNotions.NData`, `show.py --value` (`NData.etaLoc`, `MtUp`, `MtLow`, `mult`, `PairedCharacterConditionAlt`, `rhs`, `SizeData₂.dZ0`, `TwistedPlaces.etaSum`), `trace_app.py --reading` (`exists_const_tieChi_bound_of_facts`, alias `ExtraFromFacts.main_alt_alt` ; `exists_bound_tieChi_of_prints`, alias `NormFromFacts.main_alt_alt`).

**La donnée locale (`NData`, 81 champs).** Chaque indice local `i` est une place tordue $w(i)$ d'un étage $j(i)$, de caractéristique $\ell(i)$ (`w_l`, `mu_w`, `w_tw`). Il porte un anneau de valuation discrète complet $O$ fini sur $\mathbb Z_\ell$ ; une algèbre de Hecke locale $T\subset O^X$ ($X$ fini : les systèmes propres), engendrée par des opérateurs aux places décomposées hors de $S\cup Q$ et de ℓ ; un $O$-module libre $M_t$ sur lequel $T$ agit fidèlement, avec un réseau $L$ (`MtIn`) comparé à celui de la ligne tordue (`prMt`) ; des caractères galoisiens $\chi_c=\chi_1\cdot\mathrm{cyc}^{-(c-1)}$, $1\le c\le t$ (torsions de Tate) ; des ensembles $Z\supset Z_{\rm good}\subset X$ et des multiplicités de Hecke `mult`.

**Le défaut (niveau 4).** `etaLoc(i)` est la longueur de `MtUp/MtLow`, avec `MtLow` $=L\cap E_{\rm good}$ et `MtUp` $=E_{\rm good}\cap(L+E_{\rm bad})$, où $E_{\rm good}$ et $E_{\rm bad}$ sont les sommes d'espaces propres des systèmes de $Z_{\rm good}$ et de son complémentaire. `MtUp` est l'image de $L$ par le projecteur sur $E_{\rm good}$ parallèlement à $E_{\rm bad}$ : `etaLoc` est le **module de congruences** de Ribet et Wiles, qui mesure les dénominateurs de ce projecteur. Modèle : pour $T=\begin{pmatrix}0&1\\0&\ell\end{pmatrix}$ sur $L=\mathbb Z^2$, $E_{\rm good}=\mathbb Q(1,\ell)$, $E_{\rm bad}=\mathbb Q(1,0)$, la projection de $L$ est $\mathbb Z(1/\ell,1)$, $L\cap E_{\rm good}=\mathbb Z(1,\ell)$, et le quotient est $\mathbb Z/\ell$ : $\eta=1=v_\ell(\ell-0)$.

**La borne locale (niveau 3).** `PairedCharacterConditionAlt` conclut $\mathrm{etaLoc}(i)\le\sum_{\pi\in Z_{\rm good}}\mathrm{mult}(\pi)\cdot\mathrm{rhs}(\pi)$, où `rhs` contient $\sum_{0<e<t}\operatorname{len}\text{Ш}(\ell,e)$ et des termes locaux (`sPi`, $v_\ell(h_E)$, `vdel`, une somme sur $Q(i)$, des termes en $f$, $n_V$, $r$). Les hypothèses : ℓ est l'un des deux premiers de l'hôte, représentations galoisiennes $\rho$ attachées aux systèmes propres, décomposition semi-simple, conditions de taille, finitude des longueurs de Ш. **Comptabilité** : `etaSum(j)` $=\sum_{w\ \text{tordue}}\mathrm{lwP}(w)\,e_w\,\mathrm{etaJ}(j,w)$, et `dZ0(j)` est la dimension de l'espace de formes de l'étage $j$, qui majore la multiplicité totale : d'où le facteur $d_{Z_0}(j)$ devant $\sum_\ell\mathrm{vvTerm}(\ell)$ dans `etaSum_le`. Les normalisations des poids `lwP` n'ont pas toutes été vérifiées.

**Le mécanisme (niveau 1–2).** La preuve de la borne passe par `conclusion41_of_pAdicHodge_alt` (4,7 M lignes : comparaison de Wach et Bhatt–Scholze, Fontaine, « congruences de type premier ») et `no_cut_passes_of_artin_reciprocity` (1,2 M). C'est le schéma de la méthode de Ribet ⟦I⟧ : des congruences entre systèmes propres produisent des classes de cohomologie galoisienne dans des torsions de Tate, dont la théorie de Hodge p-adique contrôle les conditions locales en ℓ ; la borne de Ш (`VWin`) majore alors le module de congruences. Non reconstruit.

## E8. Le programme de flot des couches impaires (niveau 4)

`show.py --value` : `Formalism.BasicNotions.lpFeasible`, `lpF`, `FactLpF`, `Formalism.IncomingBounds.{IsFlow, maxFlow, flowVal, Fnum, gam, rho, oddLevels}`, `Formalism.L2.FormalSeriesBounds.LemmaFe` ; `revindex.py refs lpF`.

**Le programme.** Sur une orbite de Frobenius de longueur $d$ (positions $s\in\mathbb Z/d$), avec des capacités $D_s\ge0$ et un premier $l$, un flot est une famille $x_{s,i}\ge0$ indexée par la position et une **couche impaire** $i<d$, telle qu'en chaque position $\sum_i l^ix_{s,i}+\sum_ix_{s-i,i}\le D_s$ : une couche $i$ lancée en $s$ pèse $l^i$ en $s$ et $1$ en $s+i$. `maxFlow` est le supremum de $\sum x$ ; `lpF` $=\gamma(l)\sum_sD_s-\text{maxFlow}$, avec $\gamma(l)=l/(l^2-1)$, le taux du Théorème A.

**Son rôle.** Dans le corollaire du Théorème A (`Loc.Cor2`, consommé par `corollary_split_eleven_one`), la conclusion `KvalGe` minore une valuation par $\sum\mathrm{baseTerm}+\mathrm{lpF}(l,d,s\mapsto(k-1)w_s)-\text{pertes}$ : `lpF` est un **gain**, le gain brut diminué d'un coût de troncature qui est **exactement l'optimum d'un programme de flot** sur l'orbite. `lpF` sert aussi de « contenu inerte » (`InertContent.orbit`, `FInert_le`). Le théorème nommé `linear_programming_input_of_hypotheses` est, lui, un simple empaquetage des deux théorèmes de famille ; il n'utilise pas `lpFeasible`.

**Lemme (`LemmaFe`, reconstruit).** Si $l\ge2$, $d\ge2$ pair et $D_{a'}\le l\,D_a$ pour tous $a,a'$, alors $\text{maxFlow}=\frac{\sum_sD_s}{l+1}$, donc `Fnum` $=$ `lpF` $=\frac{\sum_sD_s}{l^2-1}$. *Démonstration.* Majoration : en sommant les contraintes, $\sum_{s,i}(l^i+1)x_{s,i}\le\sum D$, et $l^i+1\ge l+1$. Égalité : on n'utilise que la couche 1 et l'on sature, $l\,x_s+x_{s-1}=D_s$ sur le cycle ; pour $d$ pair, $x_s=(1-l^{-d})^{-1}\sum_{k<d}(-1)^kD_{s-k}l^{-(k+1)}$, somme alternée de termes décroissants exactement sous la condition d'équilibre, donc $\ge0$ en groupant par paires. Vérifié en fractions exactes sur 400 cas aléatoires ; sans équilibre ($D=(10,1,10,1)$, $l=2$), la construction donne des $x_s<0$.

## E9. La droite cible des fonctionnelles CM (niveau 3)

`trace_app.py --reading` et `--slice` sur `GlobalTheory.ArcCM.numGood_of_famQ` ; `show.py --value` : `CMIn.valLine`, `valLine_ndeg_le`, `Formalism.L2.LamCM.pDeg`, `GlobalTheory.LamF.LamDegSt`.

**Les obligations de `NumGood`** (liste de lecture de `numGood_of_famQ`) : la droite cible (`CMIn.valLine`, `valLine_ndeg_le`, `lamDegSt_logOm₂`, `cmValueLine_length_conj_eq`) ; l'intégralité aux places finies (`cmArcDatum_functional_finite_integrality_bound`, 1,14 M lignes) ; la norme archimédienne (`RunNum.arch_all`, 318 k).

**La fonctionnelle** (tranchage du témoin) : $\varphi=\psi\circ\iota$, où $\psi$ est définie sur un espace de **sections** (`sec`) et $\iota$ l'inclusion des formes paraboliques (`cutR ≤ cusp ≤ sec`) ; les sections sont celles d'un fibré en droites sur une variété abélienne polarisée (`Semi.LB.Sec (PolAV.L …)`), évaluées en jet le long d'un « arc » en un point CM (`ArcIn`).

**La droite cible.** $\mathrm{valLine}(s,\mathrm{mo},n)=(T_l^\vee)^{\otimes n}\otimes\big(\bigotimes_v\mathrm{line}(s,v)^{\otimes\mathrm{mo}(v)}\big)^\vee$, où `mo` est le multi-indice du jet sur les directions $v$ et `line(s, v)` les droites propres. **Borne** (`valLine_ndeg_le`, sous `LamDegSt` et $La\ge1$) : $\mathrm{ndeg}\le\big(\mathrm{pDeg}(\log\Omega)+\tfrac12\log La\big)\big(\sum_v\mathrm{mo}(v)+\tfrac{[E:\mathbb Q]}2(p+q)\,n\big)$, avec $\mathrm{pDeg}(\log\Omega)=\frac{1+|\log\Omega|}2$ ; `LamDegSt` donne à chaque droite élémentaire le degré normalisé exact $\log\Omega/2$. La structure de la borne suit des identités de tensorisation (additivité) et de dualité (signe) ; la borne n'utilise que la **taille** $|\log\Omega|$, la compensation exacte du terme principal étant faite ailleurs (`MAIN`). Non lu : `ndeg_line_option_le`, l'intégralité et la norme.

## E10. La preuve de `LPprime` (assemblage : niveau 4 ; rang par arête : niveau 2)

`revindex.py refs LPprime LPprimeAt RhoL RhoLowerBoundLargeConductor RestEdgeCount` ; `show.py --value` : `RestEdgeCount`, `RhoLowerBoundLargeConductor`, `RhoL`, `dL`, `gaussianNumber`, `RhoGE`, `JSmith`, `isUnit_det_of_one_add`, `goodRank_core`, `CloudLowerBoundWeyl`, `CloudWeightLowerBound`, `ResidueClassCount`, `WeylV`, `IsBaseWeight`, `flatW`, `kappaOneExponent` ; `trace_app.py --reading rho_lower_bound_of_edge_count`.

**Trivialités.** `lpprime_of_one_le` : si $\kappa\ge1$, `LPprime` vaut ; `LPprime_mono_kappa` : monotonie en κ. `jSmith` : `LPprime` entraîne `JSmith` — pour tout réseau $L_v$, une base $b$ du réseau dual cible et un ensemble « mauvais » d'au plus $\kappa\dim V$ indices tels que $p^Db_a$ soit dans le span des fonctionnelles pour tout $a$ hors de cet ensemble.

**Assemblage (`rho_lower_bound_of_edge_count : RestEdgeCount → RhoLowerBoundLargeConductor`, reconstruit).** (1) `RestEdgeCount` : tout réseau $L$ de rang $k$ reçoit au moins $\frac{q^k-1}{q-1}$ arêtes de type 1 (`gaussianNumber`), $q=p^{n'}$ — le nombre d'hyperplans de $\mathbb F_q^k$, classique. (2) `RhoL` demande, **pour chaque arête**, un accouplement de rang $\ge X=(1-\kappa)\,d_L$ à la précision $D$, avec $d_L=\dim V/\frac{q^{m+1}-1}{q-1}$ (`dL`) ; `RhoGE` : il existe $n\ge X$ facteurs invariants $\le D$ (`FactorsLE`). (3) Les rangs s'additionnent : si les blocs diagonaux s'écrivent $P_e\,\mathrm{diag}(z)$ avec $P_e$ inversible et $v(z)\le D$, et si la séparation rend les blocs croisés divisibles par $w^{c^*}$ avec $c^*>8D$, la matrice globale est $P\,\mathrm{diag}(z)$ avec $P$ congrue modulo l'idéal maximal à une matrice diagonale par blocs inversible, donc $\det P$ inversible (`isUnit_det_of_one_add`) ; `goodRank_core` donne alors `GoodRankK` avec $M=\mathrm{diag}(z')P^{-1}$, $z'z=p^D$. Le rang total est $\ge\frac{q^{m+1}-1}{q-1}\cdot(1-\kappa)d_L=(1-\kappa)\dim V$.

**Rang par arête (niveau 2).** Il est obtenu par une **récurrence sur le plus haut poids** λ (`CloudWeightLowerBound`, `CloudLowerBoundWeyl`, `ResidueClassCount`, à partir de `cloud_prop_of_maps_retraction_basis` et de `tensor_bound_of_order_bound`) : on passe de poids « plats » $\lambda_s=(A_s,0,\dots,0,-B_s)$ (`flatW`) et de leurs translatés par $2c$ aux poids de base (`IsBaseWeight` : en $s\in TT$, $\lambda_s=(a_s,\text{coefficients}\le c,-b_s)$ ; hors de $TT$, coefficients $\le c$), au prix d'une précision $D\mapsto2D+|TT|\lceil r^2\,\mathrm{lgA}(p,a,r)\rceil$ (`kappaOneExponent`) et d'une séparation $c\mapsto c-2|TT|c_{\rm cl}$. Les dimensions sont comparées par la **formule de dimension de Weyl** pour $\mathrm{GL}_{m+1}$ (`WeylV` : $\dim V(\lambda)=\prod_s\prod_{i<j}\frac{\lambda_{s,i}-\lambda_{s,j}+j-i}{j-i}$). Les grands coefficients $a_s$, $-b_s$ du plus haut poids, aux positions retenues, rappellent la paire $(a,b)$ de la troncature de Riesz ⟦I⟧ (non suivi jusqu'aux paramètres d'échelle). Le rôle de `NoRel` n'apparaît pas sur ce chemin ; `TT` y est le support du poids.

**Ce qui reste.** Les lemmes du « nuage » (`cloud_prop_of_maps_retraction_basis`, 98 k lignes ; `tensor_bound_of_order_bound`, 46 k) : la divisibilité des accouplements sur les modules de Weyl entiers.

## E11. Le rang par arête : modules de Weyl et bases de poids (niveau 3)

`show.py` : `cloud_prop_of_maps_retraction_basis`, `tensor_bound_of_order_bound`, `BePerfect`, `DualHeightBasis`, `DualHeightInclusion`, `LatRetract`, `RestOrdBound`, `elementary_divisor_basis`, `HL`, `dualWeyl`, `edgeLat`, `order` ; `revindex.py refs DualHeightBasis BePerfect` ; listes de lecture.

**Les deux lemmes du « nuage » sont conditionnels** : ils réduisent le rang par arête à des hypothèses nommées (`RestCloudMaps`, `LatRetract`, `BePerfect`, `DualHeightBasis`, `RestTensor`, `RestOrdBound`, `DualHeightInclusion`), et ne possèdent en propre qu'un comptage (`cloud_count`) et des changements d'échelle (`nu_scale`, `mu_scale`, `dual_bases`). Ces hypothèses sont fournies par le **modèle local** (`Formalism.L2.G.Model.dualHeightBasis`, `Model.bePerfect`, regroupés dans `Loc6`, `Loc8All` : les `local_model_results` de E5).

**Les objets.** `dualWeyl R r n ν` est le sous-module des polynômes en les coefficients d'une matrice, homogènes de poids ν, **invariants par les opérations d'addition de colonnes** (`colAddGen`) : la réalisation classique du module de Weyl dual $H^0(\nu)$ par invariants unipotents, valable sur tout anneau. `HL(L)` est le produit tensoriel, sur les positions $s$ de l'orbite de Frobenius, de ces modules tordus par $\sigma^s$ (`extO … s`) : $V(\lambda)=\bigotimes_sH^0(\lambda_s)^{\sigma^s}$, réalisé sur le réseau $L$.

**La base commune d'une arête** (`DualHeightBasis`, prouvé par `elementary_divisor_basis` à partir d'une base adaptée à l'arête, `edgeLat`, et d'une base de produit tensoriel, `ten_basis`) : il existe une base $(x_i)$ de `HL(src)` et des exposants $\pi_i$ tels que $(p^{\pi_i}x_i)$ soit une base de `HL(tgt)`, $(w^{\pi_i}x_i)$ une base de `HLe(e)`, et $(w^{\pi_i-A_r}x_i)$ une base de `Re(e)` (`order` $=A_r-\pi$). Lecture ⟦I⟧ : dans une base de tgt adaptée, src $=\mathrm{diag}(p^{\varepsilon_j})\cdot$tgt, la dilatation agit diagonalement sur des vecteurs de poids, d'exposant l'accouplement du poids avec $\varepsilon$.

**Le rang par arête** revient alors à compter les vecteurs de cette base dont l'exposant tient dans la précision (`cloud_count`), et à comparer ce nombre à la dimension par la formule de Weyl ; l'accouplement entre réseaux duaux est parfait (`BePerfect`). Non lus : `cloud_count` et `ten_basis`.

## E12. Le rôle de `NoRel` : pas trois places épaisses consécutives (niveau 4 pour l'énoncé)

`revindex.py refs NoRel`, `up dropping_proposition_holds` ; `show.py` : `Host.second_set_no_relation`, `UnusedSlot33.no_three`, `Conclusion5`.

**Où.** `NoRel` sert à la construction de l'hôte (`hostOfFieldOf`, `hostThickExists`, champ `Host.second_set_no_relation : NoRel T2 Lw`), aux orbites épaisses du repère, et à `dropping_proposition_holds`, dont la chaîne d'usage est `field_lemmas_except_seven` → `linkG_fam_noKer`. *Corrigé en E13 : cette dernière chaîne est formelle, la clause n'y est jamais projetée.*

**Quoi.** `Conclusion5` fournit, pour tout $L_w\ge2$, un ensemble $T_2$ de positions : (i) majorées par $n_0/(4L_w)$ ; (ii) de **densité de Behrend**, $|T_2|\ge n_0\exp(-C\sqrt{\log n_0\log L_w})/L_w$ ; (iii) sans relation à trois termes ; (iv) pour tout translaté de $T_2$ et toute orbite $t+i\,h$ : si l'ordre de $h$ dépasse $4L_w$, **toute fenêtre de $L_w$ pas consécutifs contient au plus deux points** ; sinon, l'orbite entière en contient au plus un. `no_three` le dit négativement : trois puissances consécutives $\varphi^i\tau$, $\varphi^{i+1}\tau$, $\varphi^{i+2}\tau$ ne tombent pas toutes sur des places épaisses. La clause (iv) est exactement le lemme d'orbite de la synthèse (§ 3.5), dont la démonstration est celle que la synthèse donne.

**Ce qui reste.** Voir E13.

## E13. Où sert vraiment `NoRel` : le paquet de Behrend est inerte, l'hôte porte la propriété (niveau 3)

`trace_app.py --all --json linkG_fam_noKer`, `stabF`, `stabiliser_family_of_column_lemma` ; `show.py --value stabiliser_family_of_definite` ; `revindex.py refs Conclusion5 Host.second_set_no_relation`, `up LongWindow.main long_clusters inert_nothree_nonthick NLinkClose.main_alt_alt` ; `fiche.py WordsB`.

**Le paquet `field_lemmas_except_seven` est déstructuré mais presque pas lu.** Ses deux consommateurs sont `linkG_fam_noKer` et `stabF` (aucun autre consommateur de `Conclusion5`, établi par `revindex`). Dans `linkG_fam_noKer`, la locale `h59` qui le porte n'a **qu'une** occurrence : `And.left (And.right³ (h59 D sc))`, soit `Conclusion4 D 100`, qui devient `hO : FamilyGlobalOrderEstimate Fm 100` (ordres 2-adiques des `hOf l`, sommes $\sum\log l/l^2$). Dans `stabF`, le paquet est reconditionné en `Conclusion₂` (avec `division_rows_rational_lattice`) et transmis, par `stabiliser_family_of_column_lemma`, à `stabiliser_family_of_definite`, qui n'en extrait **que** `division_rows_rational_lattice` (`And.left (And.right⁷ (h x hx1 i))`). **`Conclusion5` (Behrend, `NoRel`, fenêtres) et `TorusPairsWithVariant` sont démontrés, dans la fermeture, mais jamais projetés** : leur contenu ne sert pas. Ceci corrige E12, qui plaçait `dropping_proposition_holds` sur le chemin des gains.

**Le canal effectif est le champ de l'hôte.** `Host.second_set_no_relation : NoRel T2 Lw` est consommé par `LongWindow.main` : sur toute orbite $\tau\varphi^i$ d'ordre $>4L_w$, le prédicat « place épaisse » vérifie `WindowTwo` (pas trois points dans une fenêtre de $L_w$). De là, deux lemmes :

- `long_clusters` (orbite longue) : pour $1\le j$, $2j+2\le L_w$, les lettres épaisses se groupent en **grappes** (`Clusters`) : chaque lettre épaisse appartient à une unique paire $\{x,\,x+\mathrm{sp}(x)\}$ (ou singleton), avec $\mathrm{sp}(x)\le j$, aucune lettre épaisse strictement entre, et **aucune dans les $j$ lettres qui précèdent** $x$ ;
- `inert_nothree_nonthick` (premier inerte, signe $-1$) : `NoThree` et au moins une lettre non épaisse.

Ces propriétés deviennent les hypothèses des **mots de page** (`pageWord` : sur l'orbite, une lettre par place avec un marquage et une taille `szT`) et des **mots récursifs** (`recWord`, `WordsB` : grappes de profondeur $j_A$, marge $C(j_A+1)(w+S+\eta+1)\le b$) ; la profondeur vaut $\mathrm{depth}(l)=\min\{j : l_A\le(l-1)^j\}$, et `HypA` exige $40(j+1)(G+1)\le b$ dès qu'une lettre est épaisse. La chaîne d'usage remonte par les jonctions B, C, D (`RecS.fam_jointBCD_closed_alt`) à **`NLinkClose.main_alt_alt`** (conclusion `ConclF`), puis à `GalC.linkN_of_twGood_galoisPreconditions` et à `nonempty_hyps_definite_side_of_closed_bound` → cœur. **La propriété de fenêtre sert donc la branche `LinkN` (côté Galois), non `LinkG`.**

**Ce qui reste.** La correspondance entre le marquage des lettres du mot (`pos ε`) et les places épaisses de l'hôte, et le lemme combinatoire sur les mots qui convertit grappes et marge en borne (consommateur de `WordsB`).

## E14. Le lemme sur les mots : le Théorème B (niveau 3)

`revindex.py refs WordsB Clusters HidaSetting`, `up thmB_at` ; `show.py` : `jointB_of_large`, `JointB`, `WordBase` (`fiche.py`), `wordConditions_common_natural_representation`, `cyclicWordMarkedClusters_letterwise`, `thmB_at`, `ThmB`, `arcOf`, `Thick`, `Alt`, `Sg`, `arc_proposition_alternative`.

**Conditionnement.** `jointB_of_large` produit `JointB` : pour toute place inerte $l\ge11$ de l'hôte et toute place $w\mid l$, $K_w$ est non ramifié, et il existe un mot `Wd` sur l'orbite du Frobenius (`recWord`) avec sa base (`WordBase` : non-ramification, degré, scindage, réseaux $T_1$ ⊂ sommes de duaux tordus, $T_2$ dual tordu de la représentation galoisienne), la marge $C_2(j_A+1)(w+S+\eta+1)\le b$, et les grappes de profondeur $j_A$. Le mot est produit par `wordConditions_common_natural_representation` ; les grappes viennent de `long_clusters` (E13) par `cyclicWordMarkedClusters_letterwise` (une lettre marquée est isolée sur $j$ pas, ou bien a une seule voisine marquée à distance $d\le j$, isolée sur $d+j$ pas).

**Le Théorème B** (`N.Ln17.thmB_at`, 2,7 M lignes ; énoncé `ThmB`). Une lettre est *épaisse* si sa taille tombe dans la bande $[b,\,b+\eta]$ (`Thick`). Pour un morphisme $F:T_1\to T_2$ de réseaux cristallins dans le cadre de Hida (modules de Wach), $l\ge11$, $20w,20\eta,20S\le b$ et au moins une lettre non épaisse, avec $h=h_B$, $r=\operatorname{rg}T_2$, $\mathrm{lg}=\log_l(2h)$ :

- si les orientations alternent (`up`) et qu'il n'y a jamais **trois lettres épaisses consécutives** (`Alt`), l'exposant de $F$ (`ColLeR`) est au plus $C(n+1)\,r\,\big(h/l^2+(w+\eta)/l+S+1+\mathrm{lg}+\eta\cdot\mathrm{band}\big)+C\,n\,m\,e'$ ;
- si l'orientation est constante et qu'il n'y a jamais **$R$ lettres épaisses consécutives**, même borne avec $R^2(S+1+\mathrm{lg})$ à la place de $S+1+\mathrm{lg}$.

**Mécanisme.** L'orbite est découpée en **arcs** (`arcOf`) : un arc se termine à une lettre $c$ suivie d'une lettre non épaisse et remonte jusqu'à la lettre non épaisse précédente ; sa longueur est donc 1 + le nombre de lettres épaisses consécutives. La proposition des arcs (`arc_proposition_alternative`, avec les cas de longueur 1–2, 3 et 4 : `arc_length_*`) relève $F$ le long d'un arc avec une perte $e_1\le40\,\mathrm{Sg}+\eta\cdot\mathrm{bandI}$, si l'arc a longueur $\le2$ ou si la marge $40\,\mathrm{Sg}\le b/4$ est disponible. **Le coût d'un passage épais croît comme le carré de sa longueur** ; la propriété de fenêtre de `NoRel` (au plus deux places épaisses par fenêtre, E13) borne cette longueur, donc rend le coût par lettre uniforme et la borne linéaire en $n$.

**Chaîne.** `thmB_at` → `frobenius_statement_of_inputs` → `theoremB_of_admitted_inputs` → `theoremB_closing` → `localLiftingTheoremB_of_blochKato_tateDuality_eulerChar` → `NLink.InertStep.main_alt_alt` → `adm_at_inert_of_range` : le Théorème B est l'étape « premiers inertes » du lien `LinkN`.

**Ce qui reste.** La preuve des relèvements d'arcs (théorie des modules de Wach, 2,7 M lignes) ; la provenance exacte de la bande $[b,b+\eta]$ à partir des places épaisses de l'hôte.

## E15. Les clauses inertes sur tout l'export (contrôle, niveau 3)

`python3 -I tools/inertes.py export/out_sol > analysis/inertes.tsv` (22 h 17 sur un Mac M1 de 16 Go ; journal : `# fin : {'résolu': 89047, 'non résolu': 9, 'inerte': 5747}`).

**La question.** E13 a montré, à la main, qu'un paquet de conclusions peut être démontré, être dans la fermeture, et n'être lu qu'en partie : `field_lemmas_except_seven` contient la densité de Behrend, que ses deux consommateurs ne projettent jamais. `inertes.py` systématise ce contrôle. Pour chaque théorème de la fermeture dont la conclusion est une conjonction (après les `∀` et les `∃`), il suit dans tous ses référents les projections effectivement appliquées. Il traite les projections `And.left`/`And.right`/`proj`, les éliminateurs (`And.casesOn`, `And.rec`, `Exists.casesOn`…), les β-rédex et `letFun`, et la transmission interprocédurale aux paramètres des théorèmes appelés, sur au plus 8 niveaux. Une composante est **inerte** si aucun référent ne la lit.

**Fiabilité.** L'outil est conservateur : tout usage qu'il ne sait pas suivre (passage à une fonction non analysée, budget épuisé) compte comme une lecture. Une composante déclarée inerte n'est donc lue nulle part. La réciproque ne vaut pas : il existe des clauses inutiles qu'il ne détecte pas. Le résultat manuel de E13 est retrouvé. **Correctif du 27/11 (E22).** Deux défauts faisaient perdre la trace d'un théorème passé comme argument fonctionnel à un éliminateur, ou dont l'éliminateur était appliqué à plus d'arguments ; l'outil n'était donc pas conservateur dans ces cas. Les chiffres ci-dessous sont ceux de l'outil corrigé, relancé sur les 5 747 théorèmes d'abord marqués (`--from`) : 18 en sortent (−0,3 %). Les 9 cas non résolus de la première passe n'ont pas été relancés.

**Résultats.**

- 89 056 théorèmes candidats, ceux du projet dont la conclusion a au moins deux composantes. 89 047 sont résolus et 9 ne le sont pas (budget épuisé). Les 9 non résolus sont `evLaws_genFr_atlas`, `liftIdentifications_of_liftsComparison`, `rowIdentifications_realRowSide_of_chainComparison`, `pol_pull_of_relAmple_local`, `exists_prime_residueField_eq_zero`, `exists_levi_mul_unip`, `LocalDualityAll.exists_prime_mem`, `Rw.Hd.stdPsi` et `exists_identification_typeRepresentatives_classes`.
- **5 729 théorèmes (6,43 %) ont au moins une composante inerte.** Ils totalisent 19 107 composantes, dont **8 525 inertes** (44,6 % : proportion conditionnelle, propre à ces seuls théorèmes, non un taux global). 2 675 de ces théorèmes ont deux composantes, 1 264 en ont trois.
- **707 théorèmes sont entièrement inertes** : ils sont référencés, mais aucune de leurs composantes n'est lue. Exemples : `exists_twistRings_characters_classGroups`, `series_representation_weight_lower_bound`, `PositivityTheory.Xgp.W.core`.
- **Têtes des composantes inertes.** Ce sont surtout des énoncés auxiliaires : `Eq` (2 702), `LE.le` (743), `Membership.mem` (710), `Exists` (532), `Ne` (288), `LT.lt` (221), `Iff` (205), `Continuous` (172). Ce sont des égalités de normalisation, des bornes et des appartenances livrées en même temps que la conclusion utile, puis jamais relues.
- **Répartition.** Le phénomène est concentré dans les grands théorèmes de raccord de `GlobalTheory.T` (1 694 cas), puis dans `UpperTheory.V` (314), `PositivityTheory` (229), `GlobalTheory.CompanionTheory` (225), `ReciprocityTheory` (194) et `GroundTheory` (192). 770 cas sont des auxiliaires (`_proof_`, `_private`).

**Les cas les plus lourds** (poids dominé du théorème, en lignes) :

| Théorème | Poids | Composantes | Inertes |
|---|---:|:-:|---|
| `GlobalTheory.T.member_exists_baseLattice_alt` | 48,8 M | 2 | `Fc.ExBL` |
| `T.all_stages_at_member_of_specializations_alt` | 4,2 M | 10 | 4 : `First/Second/ThirdIntermediateLevelExists`, `FinitenessStatement` |
| `T.twistedPlace_selmerLengthBound_of_localDuality` | 2,6 M | 3 | `EmbeddingTypeJumps.Conclusion0/1` |
| `T.theoremE_corollaryA_closing_all_data` | 2,3 M | 2 | `WachCoordinates.Conclusion1` |
| `T.slope_bound_of_line_large_degree` | 2,1 M | 2 | `Ar.Prov.LemmaS` |
| `UpperTheory.Et.purAll` | 1,6 M | 3 | `CohomologicalPurity.LeafTube`, `Goal` |

Deux recoupements. `member_exists_baseLattice_alt` passe par `exists_baseLattice_of_prime_alt`, qui instancie `anyGeometry` (E16), et sa clause `ExBL` n'est pas lue. Dans `theoremE_corollaryA_closing_all_data`, une des deux conclusions de coordonnées de Wach est inerte (comparer E14).

**Le poids mort mesurable.** On compte les théorèmes qui ne servent qu'à démontrer une composante inerte, c'est-à-dire dont l'unique référent est le théorème lui-même. Ils pèsent **1,45 M lignes** (250 cas), soit 0,14 % des lignes de l'export (un volume attribué, non un gain recertifié). Les plus lourds se trouvent dans `satAgree` (141 k, `inert_satake_parameters_agree_under_dictionary`), `unfoldings_of_chain` (133 k), `EndPullNu.main` (89 k) et `frame_of_cut` (81 k). **C'est une borne inférieure** : les preuves des composantes inertes passent le plus souvent par des sous-paquets partagés, que ce critère ne compte pas. Les dégager exigerait de propager l'inertie à travers les valeurs de retour.

**Lecture.** « Dans la fermeture » ne veut pas dire « utilisé ». Environ un théorème de raccord sur quinze livre des conclusions que personne ne lit. C'est la signature d'un développement par accumulation : on démontre un paquet large, puis le consommateur n'en prend que ce dont il a besoin. Le paquet de Behrend (E13) et le champ Γ (E16) en sont deux cas lus en détail. En volume, ce qui est mesurable reste faible (0,14 %). La conséquence porte sur la lecture : une recherche de dépendances surestime ce qui sert, et toute affirmation du type « la preuve utilise X » doit être établie en suivant les projections.

**Comparaison avec la preuve courte.** Sur l'édition lisible de la réécriture de Sernau (`export_short/out_read`, avec `decl2mod` construit par la règle « projet = `New.` ou `_private` contenant `.New.` »), la même analyse prend 769 s (outil corrigé). Elle trouve 2 354 candidats, dont 1 non résolu, et 106 théorèmes inertes (4,5 %). Ils totalisent 165 composantes inertes sur 277, dont 39 entièrement inertes, et le poids mort mesurable est de 1,3 k lignes. Les inertes y sont surtout des `Eq` (69) ; le cas le plus lourd est `New.Selmer.exists_operator_ellVal_le_liftValuationBound` (3,6 M lignes, clause `PreservesHeckeEigenspaces`). La compression a presque éliminé les clauses inertes : 49 fois moins en absolu.

**Ce qui reste.** Propager l'inertie à travers les valeurs de retour, pour obtenir le poids mort complet ; vider les mémos par lots dans `inertes.py`, ajouter des points de reprise et un journal à intervalles fixes ; trancher les 9 cas non résolus avec un budget plus grand.

## E16. Les objections de Nielsen : une géométrie vide, isolée derrière des propositions (contrôle, niveau 3)

Sources : la critique de Nielsen, et la contre-expertise de Z. Zeng, *The Invalidity of "The Invalidity of Alpöge's Proof of the Riemann Hypothesis"* (23–24/11/2026, dépôt `ArtificialZeng/Riemann-hypothesis-Auditing`), dont nous reprenons les noms des objets signalés (`analysis/nielsen_objets.txt`) ; tout est revérifié sur l'export. `show.py --value` : `anyGeometry`, `GeoP`, `geoCl`, `GeoCl`, `Parameters`, `Parameters.s`, `OX`, `OAt`, `geoDegenerate`, `algDegenerate`, `padDegenerate`, `mdlJunk`, `cxJunk`, `divXFl`, `exists_divT`, `geoOver_stages`, `x0`, `hExpl6`, `hExpl6_lower`, `setDiv` ; `revindex.py refs` et `path` ; `tools/occ.py` (pour une preuve, les applications qui englobent les constantes cherchées, sur le DAG complet) ; `tools/frontiere_donnees.py OUT analysis/nielsen_objets.txt` (remontée par les seules définitions) ; `poids.py --set`.

**Les constats de Nielsen sont exacts.** Les treize objets signalés sont tous dans la fermeture de `riemannHypothesis` (`decl_domtree`) :

- (1) `GlobalTheory.Mem.Top.Bl.anyGeometry := fun _ _ _ => True`, un prédicat `GeoP` sur les triplets $(D,J,X)$ ;
- (2) le modèle dégénéré `Formalism.L2.Geo.geoDegenerate` : un `DV.Geo` dont les prédicats valent `True`, les sections `PUnit`, une application `fun _ => 0` ; ses compagnons `algDegenerate` (identité, rang 0), `padDegenerate` et `mdlJunk` (`… => 0`), `cxJunk` (`Bot.bot`, $e^1$, 0) ; `divXFl` en fait une donnée de diviseur `DivX` ;
- (3) les identifications par `rfl` : la graine `DivRec.x0` pose `MjH := mjH Z`, `logLam := logLamOf Z`, `kapR := fun _ => kapSharp D` ;
- (4) la « hauteur » : `setDiv` la remplace par `hExpl6`.

**(1) Γ est un champ porté, jamais lu.** Le cœur `nonempty_hyps_definite_side_of_closed_bound` fixe les paramètres par `parametersOfDependence hL c = parametersOfExtension (extensionWithList hL c) SExt.none (geoCl anyGeometry)`. Γ descend par `Parameters.Γ` → `Parameters.s` → `Slots.mk … (OX Γ)` jusqu'à la structure `OAt Γ t X`, qui a deux champs : `geo : Γ(D,J,X)` et `lam : LamAre … X`. Dans tout l'export, `OAt.geo` n'a que deux référents, et `occ.py` montre ce qu'ils en font :

- `divEx_geoCl` : `OAt.geo` → `geoCl_of` → `OAt.mk` (relèvement de Γ en `GeoCl Γ`) ;
- `oAt_setDiv` : `OAt.geo` → `GeoCl.step` → `OAt.mk` (transport le long de `setDiv`).

Le champ est rempli par `trivial` (`divEx_prov`), relevé, recopié, **jamais consommé**. Les quatre autres référents du groupe `OAt` (`movable_prmR_nel_alt`, `slot_mv_extension_with_list_geo_cl`, `divisionGeometryScalars_transfer_setDivision`, `divEx_prov`) ne le projettent pas. Le seul lecteur de contenu, `parameter_of_discrete_series_ray_alt`, ne projette que `OAt.lam` (vers `logLam_twArgs_pz`). C'est le phénomène de E13 : une hypothèse transportée, jamais lue.

**(2)–(3) Le modèle dégénéré et les `rfl` : un témoin existentiel.** Les objets dégénérés convergent vers `DivRec.exists_divT` : il existe $Y$ tel que `DivT … Y`, `MjAre Z Y`, $\kappa_R(Y)=\kappa^\sharp(D)$ et `LamAre Z Y`. Ces conditions demandent que $Y$ **recopie** les données de lignes $Z$. La graine $Y$ est donc un conteneur de $Z$, d'où les `rfl` (`exists_mjHTie … rfl HEq.rfl`, `lamAre_of_eq … rfl`). Le contenu est dans $Z$ (réseaux `mjLat`, lemmes `mjH_good`, `jM_lat`, `jM_metric`). `geoOver_stages` énonce même `GeoOver (fun _ => True) X₀`.

**La dégénérescence ne fuit pas.** `frontiere_donnees.py` remonte depuis les treize objets en ne traversant que des définitions (des données). On atteint 21 définitions et 52 théorèmes :

- **Définitions atteintes :**
  - `famFlJ`, `formsFl`, `shimUFl`, `shimXFl`, internes à `Formalism.L2.Geo`. Les théorèmes qui les lisent (`isoInv_famFlJ`, `levInTie_famFlJ`, `md_heq`, `shimXFl_congr`, `toShimX_fl`, `tiedX_fl`) n'ont qu'un débouché, `geoOver_stages`, qui alimente `exists_divT`, puis `divEx_prov` ;
  - `GeoOver`, `Keeps`, `NLink.Final.mainTheorem`, à valeurs dans `Prop` ;
  - `parametersOfDependence`, qui porte Γ, champ mort.
- **Toutes les autres sorties sont des propositions :**
  - `exists_divT` (`∃ Y, …`) et `DivEx` ;
  - `exists_geo` ($\exists\,G\,Y,\ H^0(G,Y,0)\neq\bot$) ;
  - `nonempty_divX` (`Nonempty (DivX D)`) ;
  - `exists_divisor_eigenvalueIndex_labeling_alt` (`∃ Xd E, …`) ;
  - `idx_zero_off_twisted(_anyEta)` (des égalités).

Un consommateur n'accède au témoin d'un `∃` ou d'un `Nonempty` que par élimination vers `Prop` ou par `Classical.choose`, qui est opaque : il ne voit pas la définition du témoin et ne dispose que des propriétés énoncées, qui sont vraies du témoin dégénéré. Cette frontière en données est un résultat syntaxique, non un théorème de non-interférence. La dégénérescence ne sert qu'à l'intérieur des preuves de ces propositions.

**(4) La hauteur : un nom pour une expression explicite.** On a

$$\texttt{hExpl6}(D,L,X,C,u)=\mathrm{SZbP}+\sum_j\mathrm{kernelPlaceMeanBound}_j-\sum_j\mathrm{L6lo}_j-\operatorname{moy}_e\log\kappa_R(X)(e).$$

Le lemme utile, `hExpl6_lower`, borne $-\big(\texttt{hExpl6}+\operatorname{moy}_e\log\kappa_R(X)(e)\big)$ par $(500+2|C_{Tu}|+30|C_{sz}|)\,\mathrm{szPol}^9\,b$. **Le seul terme qui dépend de $X$ s'y simplifie**, et la borne porte sur les termes de taille. Ce n'est ni une branche morte ni une branche vide : on ignore l'habillage « hauteur géométrique » et on garde la borne. `hExpl6` a 32 référents (`linkDIVt_of_rowsF`, `hhRest_of_parts`, `hExpl6_lower(_pow,_at)`, `pkg_of_rowsK_alt`…).

**Indépendance des inégalités centrales.** `Formalism.L2.DIV.divClausesR_of`, qui démontre les deux inégalités de `WordFacts` (un seul référent : `linkDIV_L2R_face`), n'utilise ni `anyGeometry`, ni `GeoP`, ni `geoDegenerate`, ni `x0`, ni `exists_mjHTie`, ni `hExpl6`, ni `hExpl6_lower` (`revindex.py path` : NON pour chacun). Cela confirme Zeng.

**Poids.** `poids.py --set` sur les sous-arbres de `exists_divT`, `geoOver_stages`, `x0`, `provisionalDivX`, `pointGeo`, `graft`, `anyGeometry`, `padDegenerate`, `geoDegenerate` donne une union de 5 sous-arbres maximaux. Ils pèsent **0,051 %** des déclarations, **0,019 %** des lignes et **0,021 %** des nœuds. La plomberie de Γ (`OAt`, `GeoCl`, `oAt_setDiv`) est partagée avec le champ utile `lam` et n'est pas comptée.

**Bilan.**

| Objet | Statut | Pour la lecture |
|---|---|---|
| Γ = `anyGeometry` | branche portée (champ jamais lu) | retirable en principe, après recertification |
| modèle dégénéré, `rfl` | branche vide : témoin d'un `∃` dont les conditions recopient $Z$ | se résume à « on emballe $Z$ » |
| hauteur `hExpl6` | nom d'une expression explicite | garder `hExpl6_lower`, ignorer l'habillage |

Les objections portent sur l'interprétation, non sur la validité. La couche nommée « géométrie » est une coquille, et le contenu passe par les données de lignes et les bornes de taille. Le critère de la **frontière en données** (un objet qui ne sort que derrière des propositions ne peut influencer le reste que par ce qu'elles énoncent) complète le suivi des projections de E13.

**Ce qui reste.** Le dénombrement de Zeng (30 dépendants de `anyGeometry`, 124 des objets signalés) n'est pas refait ; nous comptons 14 référents directs de `anyGeometry` et 168 de `GeoP`. Le contenu de `DivT` n'est pas lu.

## E17. Le record de comptabilité : les entrées (A1)–(A7) de Nelson, nom par nom (niveau 3)

Source : l'instantané `original-route` du classeur de Nelson [Ne0], ch. 58 (« Assembly at one scale ») et 59 (« The accounting in the Lean formalization »), téléchargés et lus en entier. Sur l'export : `show.py --value` sur `each_unit_bound_statement`, `PointwiseBoundVariant`, les champs de `RankGapBounds.WeightedMeanData.Data` et les prédicats ci-dessous ; `revindex.py refs` ; parcours de la valeur de `linkCore` avec `lexpr` (arguments des fabricants `Lnk.Mod.data_*`).

**Le théorème de comptabilité.** `Formalism.LFunctionChainParameters.WeightedSlopeBounds.each_unit_bound_statement` démontre `PointwiseBoundVariant D C X''`. Ce prédicat a onze hypothèses, les « onze inégalités du record » dont parle Nelson, et conclut, pour chaque translaté $u_0$ :
$$\texttt{ASK}(u_0)\;\le\;\texttt{Main}(u_0)+\texttt{ErrX5at}(u_0),$$
où `ASK` $=S=\sum_{t,j}P_{t,w_j}(a_t)$ est un champ du record, et $\texttt{Main}=\sum_j\sum_ta_t\big(\log a_t-1-\gamma+\texttt{LpL}-\tfrac1f\sum_\rho\log w_j(\rho)\big)=\sum_{t,j}M_{w_j}(a_t)$. C'est le Théorème 58.1.1 de Nelson, $\sum_{t,j}(P-M)\le e$. Son seul référent est `Deduction.ch_top`, le théorème qui produit le crochet d'erreur (article, § 5.4).

**L'appariement.** Les notations du record sont `muCC` $=\mu(R^\vee)$, `h` $=h_u$, `Fo` $=\mathcal L$, `T` $=T_u$, `Ga` $=\Gamma$, `Ee` $=E_u$, `muN`/`muMaxN` $=\mu(N_u)$/$\mu_{\max}(N_u)$, `muM`/`muMaxM` $=\mu(M_u)$/$\mu_{\max}(M_u)$, `IO` $=I$, `HH` $=Z$, `del`, `η`, `e` $=\delta_F,\eta_F,e_F$.

| Entrée (Nelson, ch. 58) | Hypothèse de `PointwiseBoundVariant` | Énoncé lu sur l'export | Fabricant dans `linkCore` | Interface (§ 5.4 de l'article) |
|---|---|---|---|---|
| (A1) $S\le\Gamma+e_1$ ; et $I\le e_1$ | `LossBounds` | `ASK − Ga ≤ LoP` et `IO ≤ LoP` | — (lemme local `L8`, à partir de `hloss`, `hask`, `hio`) | `LossFS` (par `hLo`) |
| (A2), (A2⁺) | `QuotientSlopeBoundsWith` | $\mu(M)+\Gamma+\mathcal L-E-\mathrm{Lo5}\le\mu(N)$ ; $\mu_{\max}(N)\le\mu_{\max}(M)+\Gamma+\mathcal L-E+c\,mB_0$ | `model_slopes_five` | `SlopesNF` (par `SlopesN_at`, établi) |
| (A3), forme du théorème des cadres | `SlopeIneq`, `HHBound`, `FParams` | $s-\log\lvert\mathcal W\rvert-(1-\delta_F)^{-1}\big(4u_F\log(1+Z/u_F)+(\eta_F+4\sqrt{e_F})Z\big)\le\mu(R^\vee)$ si $s-\mu_{\min}\le Z$ ; $0<Z\le x^{c}b$ ; bornes sur $\delta_F,\eta_F,e_F$ | `data_SlopeIneq`, `data_HHBound` | `FrameF` (`Frame_at`, par le type) ; `LatF` pour `HHBound` (par `Lat_at`, établi) |
| (A4) | `DIV` | $\mu(R^\vee)+h_u-\mathcal L\le\sum_t\big(m\varphi(a_t)-ma_t\log\Omega-a_t\log T_u\big)+c\,n_TaL_a+c\,m(B_0+N_c)x^{e_D\varepsilon}$ | `data_DIV` | `LinkDIV` (par `LinkDIV_at`, établi) |
| (A5), (A5⁻) | `EComp5` | $\lvert E_u-mAg\rvert\le c\,mB_0$ | `data_EComp5` | `LinkDIV` (par `LinkDIV_at`, établi) |
| (A6), (A6′) | `Count5` | $\log T_u\ge\sum_j\frac1f\sum_\rho\log\frac{w_j(\rho)v}\pi+mg-c(L_a+m^2L_a/k)$ ; $\log T_u\le c\,mL$ ; $\lvert\log T_u-\log T_{u'}\rvert\le c\log k$ | `data_Count5` | `CountF` (par `Count_at`, établi) |
| (A7), (A7⁺) | `Slopes` | $-c\,n_TaL_a(1+m/k)\le\mu(M_u)$ ; $\mu_{\max}(M_u)\le c\,n_TaL_a$ | `data_Slopes` | `SlopesMF` (par `SlopesM_at`, établi) |
| (H) | `HComp` | $\lvert(h_u+A\log T_u)-(h_{u'}+A\log T_{u'})\rvert\le c(n_TaL_a+mB_0)$ | `data_HComp` | `LinkDIV` (par `LinkDIV_at`, établi) |
| conditions de signe | `HidaSetting` | positivité de $x,b,a,b',k,v,f,a_t,w,d_u,T_u$ ; $\mu\le\mu_{\max}$ ; $\bar\delta_F<1$, $\bar e_F\le\frac14$ | — | — |

Les erreurs lues sur l'export ont exactement la forme que donne le ch. 59 de Nelson, par exemple $e_4=c\,n_TaL_a+c\,m(B_0+N_c)x^{e_D\varepsilon}$ et $e_6=c(L_a+m^2L_a/k)$. Deux remarques.

- **Un nom trompeur.** Le `HidaSetting` de ce record ne contient que des conditions de signe. Il n'a rien de commun avec le cadre de Hida du Théorème B des arcs (E14).
- **Les fabricants.** `Lnk.Mod.mk` ne contient que des données : un point de base `i0`, des tailles `av`, `bv`, et un choix de point `pt` par translaté, avec deux égalités de compatibilité. Il ne porte aucune interface. Celles-ci entrent par les preuves passées aux fabricants. Dans la valeur de `linkCore`, la dernière preuve passée à chaque fabricant ne cite qu'une locale. `data_DIV`, `data_EComp5` et `data_HComp` citent `hDu := fun u0 => hD x hxD (pt u0)`, où `hD` provient de la déstructuration de `lD : LinkDIV` (`LinkDIV_at`). `data_Count5` cite `hC`, issu de `hCount : CountF` (`Count_at`). `data_Slopes` cite `hS`, issu de `hSM : SlopesMF` (`SlopesM_at`). `data_HHBound` cite `hL`, issu de `hLat : LatF` (`Lat_at`). `data_SlopeIneq` cite une locale dont le type est l'inégalité du théorème des cadres, avec $\eta_F,e_F$ bornés par `etaB`, `eB`, c'est-à-dire le contenu de `Frame_at` (`hFr : FrameF`) ; sa provenance exacte passe par un choix et n'a pas été suivie. `QuotientSlopeBoundsWith` vient de `model_slopes_five`, qui prend `SlopesN_at` (`SlopesNF`). `LossBounds` vient d'un lemme local qui utilise `hloss`, `hask` (lecture des sommes de caractères) et `hio`, issus de `hLo`, la déstructuration de `LossFS`.
- **Lecture.** Trois entrées, (A4) la borne de division, (A5) les termes locaux et (H) l'écart des hauteurs, sortent toutes du **même lien**, `LinkDIV`. La branche de division porte donc à la fois la hauteur des applications de périodes et la comptabilité des places de niveau et tordues. `CharF` n'alimente directement aucune de ces onze hypothèses.

**D'où vient le contenu des entrées** (Nelson [Ne0], ch. 47, 51, 52, 57, lus dans l'instantané ; chaque chapitre donne un « statut » dans la formalisation). On rapproche ces indications des provenances établies ci-dessus.

- **(A4), la borne de division.** Elle vient du Théorème 47.2.2, une estimation de covolume pour les réseaux de formes $M_j$ des $m$ relèvements : $\mathrm{lcv}(M_j)/D\le\sum_\rho(p_j-q_j)w_{j\rho}\log\Omega+CB_0\log\log x$. Elle s'obtient par géométrie d'Arakelov sur les variétés de Shimura (ch. 51). On passe à un revêtement, on change le poids, on applique une inégalité de Hilbert–Samuel arithmétique effective sur chaque composante, puis on redescend. Les outils sont Kawamata–Viehweg et Nadel, la compactification toroïdale, le théorème de Moriwaki, un lemme de Siegel absolu, Hodge–Tate et l'astuce de Zarhin. Selon Nelson, certains énoncés y sont admis comme théorèmes publiés. À cela s'ajoutent la période CM $\log\Omega=\gamma+\log(\pi/v)-c_{\chi_d}$ (Théorème 47.1.1, Chowla–Selberg ; synthèse, § 5.5) et le terme $m\,N_c$, coût des défauts de congruence aux places tordues (Théorème 52.4.5). Ce terme est borné grâce à la **borne de Selmer sur les fenêtres d'échelles**, $V(E,t)\le\sqrt b$ pour $t=\lfloor x^{401}\rfloor$ (Théorèmes 52.4.1 et 57.1.1), qui est un théorème dans la formalisation : c'est notre `VAt`, la borne de Ш de E7. Que (A4) sorte de `LinkDIV` concorde avec l'arête `LinkN` → `DIVinN` de l'article (§ 5.4) : la borne sur les places tordues conditionne la division.
- **(A5), les termes locaux.** Théorème 52.1.1 : $\lvert E_{u,j}-Ag\rvert\le CB_0$, à partir de formules explicites pour les exposants locaux (ch. 53). Il est prouvé dans la formalisation pour la famille qu'elle construit.
- **(A6), le budget de dimension et le premier auxiliaire $T_u$.** Théorème 47.3.1 : les rangs sont donnés exactement par la formule de masse et les degrés formels de Harish-Chandra, et la minoration de $T_u$ vient des lemmes sur les niveaux critiques.
- **(A7), la pente du réseau de base.** Théorème 47.4.1 : $\mu(M_u)=-\frac{\log T_u}k\sum_\rho\lvert\lambda_\rho\rvert+\sum_\rho\mu_{\rm std}(\nu_\rho)\ge-e_7$.

Pour chaque entrée, Nelson signale l'écart avec l'exposition d'Adriazola [Ad], qui suppose comme hypothèses (Hyp. 15.16, 17.11, 18.10…) ce que la formalisation démontre. C'est le sens de « The formalization proves the final theorem; the corresponding step in [Adr] is this hypothesis ».

**Les trois compensations** du ch. 58 sont celles de E1 (`key_identity5`) : les hauteurs entre (A3) et (A4), les termes de niveau entre (A5) et (A6), et les termes linéaires. `u_function_le_mean` majore l'étalement des $u_F$, et la condition (H) y est nécessaire : sans elle, l'étalement n'est pas borné (Nelson, exercice 59.1.6).

**Ce qui reste.** Suivre la provenance exacte de la locale du théorème des cadres et de `hLo` ; situer `CharF`, `NodesF`, `WinF` et les choix (`ChosenTT`, `ChosenQD`, `ChosenThin`, `LinkIRR`), qui servent ailleurs dans `linkCore`, par exemple aux contraintes de fenêtre et au crochet d'erreur.

## E18. La preuve courte de Sernau : une carte de lecture (contrôle, niveau 2–3)

Données : `export_short/readable-solution.ndjson.zst` (édition lisible de `lsernau/grh-lean`, commit `72fead1`), empreinte conforme à [Su2] ; `tools/deps` puis `analyse_export.py export_short/out_read` ; `query.py cl`, `show.py`, `inertes.py`. Guide : `grh/GUIDE.md` du dépôt, lu en entier.

**Taille.** La fermeture de `riemannHypothesis` compte 216 559 déclarations et 80,7 M lignes d'expressions, contre 1 468 390 et 1 065 M (celle des cinq énoncés : 216 567 contre 1 468 414). Le projet vit sous `New.` (48 922 déclarations avec les auxiliaires `_private`). Hors de `New.`, il n'ajoute que quelques dizaines d'auxiliaires `_private.Lib.*` ; les autres noms nouveaux viennent de la version plus récente de Mathlib. **Aucune déclaration du projet d'origine n'y survit sous son nom**, hors des énoncés.

**L'épine dorsale** suit exactement le plan du guide :

`New.grh` (91,6 % des déclarations) → `eventually_primeRemainder_le_rpow` → `Data.primeRemainder_le` (72 %) → `star_inequality` (72 %) → `Data.integral_forms_long` (45 %) → `exists_hasSmallRatios_heightLe_liftDeterminant_div` (39 %) → `exists_isRegularFamily` (35 %) → `Selmer.exists_mFoldTwist_hasDenominatorsLe` (32 %) → `GaloisRep.exists_rep_of_cuspidal_type` (19 %) → `Variety.Model.exists_galois_rep` (9 %).

Les trois théorèmes et l'inégalité principale sont ceux du classeur de Nelson [Ne], nom pour nom (voir aussi la synthèse, Atelier 6) :

| Rôle (Nelson, ch. 35) | Déclaration | Énoncé | Fermeture | Dominé |
|---|---|---|---:|---:|
| inégalité principale (Th. 35.2.1) | `New.star_inequality` | $m\cdot\mathrm{rem}\le f\,a\,(\log b)^5$ | 80,2 M l. | 58,1 M (72 %) |
| Théorème C (54.2.1) | `New.Data.integral_forms_long` | $(1-4/b^2)d_T\le n$, indice $\le\delta$, covolume $\le c$ ⇒ $d_T(h_{\rm main}-3fa\log^4b)\le c+2\delta$ | 75,3 M | 36,3 M (45 %) |
| (B) | `New.Data.enough_forms` | $d_T>0$ ; ∃ $t$, $\#t\cdot\dim S_{\rm ram}\le5d_T\log(1+2b^2)$ et $\dim\bigvee_s\mathrm{im}\ge(1-4/b^2)d_T$ | 43,3 M | 0,9 M |
| (A1) | `New.Data.span_short_integralRamified_eq_top` | les formes entières courtes ($\|\Theta_1A_s\varphi\|^2_\sigma\le e^{h_{\rm main}-m\,\mathrm{rem}+F}$) engendrent | 39,6 M | 0,1 M |
| (A2) | `New.Data.indexLe_normalizedPoincare` | indice $\le\#t\cdot\dim S_{\rm ram}\cdot U$ | 39,3 M | 0,02 M |

Le Théorème C porte l'essentiel, par la chaîne Selmer → `GaloisRep`. A et B partagent un socle d'environ 39 M lignes, qui ne leur est donc pas attribué.

**Reproduire.** Les empreintes sont celles de `exports.sha256` de [Su2], vérifiées sur le flux décompressé (`zstd -dc … | shasum -a 256`).
```
zstd -dc --long=30 export_short/readable-solution.ndjson.zst | tools/deps export_short/out_read   # 17 s
python3 -I tools/analyse_export.py export_short/out_read                                          # 54 s
python3 -I tools/revindex.py export_short/out_read build
python3 -I tools/inertes.py export_short/out_read > export_short/inertes_read.tsv                 # 769 s (outil corrigé)
python3 -I tools/modmap_src.py export_short/src_sernau/<dépôt>/grh export_short/out_read/domtree.tsv export_short/modmap_read.tsv
```
Pour `inertes.py`, `export_short/decl2mod.tsv` classe comme « projet » les noms `New.*` et les `_private` qui contiennent `.New.`. L'édition compacte se traite de même dans `export_short/out_comp`.

**Le plan du guide**, dossier par dossier, dans l'ordre de l'argument, avec l'élément de notre lecture de l'original qui lui correspond. Cette correspondance est une lecture ⟦I⟧ : les noms ont tous changé.

| Dossier (`New/…`) | Contenu selon le guide | Dans la preuve d'origine |
|---|---|---|
| `Reduction` | borne unilatérale → zéros ; données ; réseaux, indice, covolume, hauteurs (`HeightLe`, `TwistedLattice`) ; Théorèmes A, B, C ; `MainInequality` ; `OneSidedBound` | Landau en fenêtres, `gapA`, crochet d'erreur (§§ 1, 6 de la synthèse) |
| `Derivatives` | dérivées de fonctions thêta qui comptent les premiers ; corps et caractères ; groupe formel et facteur exponentiel ; vide entier ; optimalité | Théorème A (`DworkPowerSeriesWeights`, § 3) |
| `UpperBound` | noyaux thêta entre espaces définis ; formes source et cible, chaînes de relèvements ; identité de bascule (*seesaw*) ; divisibilité et taille du relèvement composé ; diviseurs élémentaires d'un opérateur de Hecke | la chaîne de relèvements, les gains `LinkG`, `LPprime` (E5, E10–E11) |
| `Spanning` | second moment et théorème d'engendrement ; multiplicités ; Bessel ; dépliage ; terme principal ; deux cadres en une place | la quasi-orthogonalité (`LinkS`, `FrameF`) |
| `Determinant` | une torsion par premier ; normes de relèvements thêta ; identité d'échange ; norme d'une chaîne ; formes auxiliaires | les covolumes, la borne inférieure de pente |
| `OneLift` | un relèvement et les valeurs de Hecke ; opérateur de comparaison ; périodes des faux relèvements ; valeurs L de Hecke comme normes | Rallis, les périodes |
| `Congruences` | choix des torsions ; représentations galoisiennes ; Selmer anticyclotomique ; perte locale ; relèvement de classes d'extension cristallines en grand poids | Ш → `LinkN`, Théorème B des arcs (E7, E14) |

Les places b éparses sont construites d'après Behrend (`Parameters.IsSparse`), avec la construction de Mathlib (`Behrend.map`) que l'original utilisait aussi.

**Ce que `Lib` reconstruit, en version affaiblie.** Le guide le dit explicitement : `Lib` démontre des morceaux de théories classiques, « souvent sous une forme plus faible qui suffit ici ». En voici des exemples :

- des représentations galoisiennes compatibles aux polynômes de Hecke pour la plupart des Frobenius seulement (`GaloisRep.Attached`), sans représentation de Weil–Deligne ;
- la théorie du corps de classes et la dualité ;
- la cohomologie ℓ-adique et de Hodge ;
- la théorie de Hodge $p$-adique, les modules de Kisin (`frame_theorem`) et les variétés de Shimura (`Variety.Model.exists_galois_rep`) ;
- Siegel–Weil et Rallis, une formule des traces simple, Chowla–Selberg ;
- les premiers en progression, et un comptage de densité de zéros par Pólya–Vinogradov pour le choix de $d$.

C'est le même trait que dans l'original : une correspondance de Langlands locale partielle (`recTExists`), vraie là où elle sert.

**Clauses inertes.** `inertes.py` en trouve 165 (106 théorèmes sur 2 354), contre 8 525 dans l'original (E15).

**Lecture.** La preuve courte n'est pas une simple élagage de l'original. Ses noms sont nouveaux, et plusieurs ingrédients y sont remplacés : les modules de Kisin au lieu des modules de Wach, un second moment pour l'engendrement, des Théorèmes A, B, C au lieu de sept inégalités de pentes. Elle garde pourtant l'architecture : divisibilité par les dérivées thêta aux premiers inertes, chaîne de relèvements, borne de taille, borne inférieure arithmétique par Selmer et représentations galoisiennes, et équilibre en $\sqrt x$. Comme carte de lecture, elle a sur l'original trois avantages : une épine dorsale franche, un guide qui suit l'ordre de l'argument, et un glossaire qui relie chaque nom Lean à son équivalent standard.

**L'édition compacte** (environ 76 000 lignes de source, quatre fois moins que l'édition lisible) a été passée dans les mêmes outils. Son empreinte `ab7b4223…` est conforme. Elle compte 204 570 déclarations dans la fermeture, mais **93,3 M lignes d'expressions, plus que l'édition lisible (80,7 M)**. Compresser le source ne compresse pas les termes de preuve : une preuve plus courte à écrire peut être plus longue à vérifier. Les noms y sont pour la plupart hors de `New.` (16 seulement en `New.`, dont 7 communs). L'épine dorsale est la même : `New.grh` (91,6 %) → `eventually_primeError_le_rpow` → `star_inequality` (74 %) → `sphericalCompat_of_odd/split` → `exists_rep_of_cuspidal_type` (20 %). Une différence : `Data.integral_forms_long` n'y domine plus que 14 %, car la branche galoisienne y est rattachée directement à l'inégalité principale.

**Le poids par dossier.** L'export ne dit pas de quel fichier vient chaque déclaration. `tools/modmap_src.py` reconstruit cette correspondance à partir du source publié (commit `72fead1`, téléchargé dans `export_short/src_sernau`). Il lit le texte des 805 fichiers `.lean` (espaces de noms, déclarations, noms privés), sans rien compiler ni exécuter, et rattache les auxiliaires à leur déclaration parente. 46 040 déclarations, soit 58,4 % du poids, sont rattachées à un fichier du projet. Mathlib et le noyau pèsent environ 31 M lignes (38 %). 3 116 auxiliaires du projet, surtout des instances anonymes, restent non rattachés (2,4 M lignes, 3 %). En lignes d'expressions et en part de la fermeture :

| Dossier | Décl. | Poids | Part |
|---|---:|---:|---:|
| `New/Congruences` (choix des torsions, Selmer, représentations galoisiennes, relèvement cristallin) | 3 116 | 5,53 M | 6,9 % |
| `New/Spanning` (second moment, Bessel, dépliage) | 5 341 | 4,81 M | 6,0 % |
| `New/UpperBound` (noyaux thêta, bascule, relèvement composé) | 4 073 | 4,24 M | 5,3 % |
| `New/Determinant` (torsions, normes, échange, chaîne) | 1 961 | 2,63 M | 3,3 % |
| `New/OneLift` (valeurs de Hecke, faux relèvements) | 1 697 | 2,17 M | 2,7 % |
| `New/Derivatives` (dérivées thêta, groupe formel : le Théorème A de l'original) | 1 140 | 0,75 M | 0,9 % |
| `New/Reduction` (données, réseaux, Théorèmes A/B/C, inégalité principale) | 1 015 | 0,39 M | 0,5 % |
| `New/Appendix` | 441 | 0,33 M | 0,4 % |
| **`New`, total** | 18 790 | 20,9 M | 25,9 % |
| `Lib/Weil`, `Shimura`, `DiscreteSeries`, `Cohomology`, `ClassField`, `General`, `Adelic`, `GaloisRep`, `SiegelWeil`, `PadicHodge`, `PadicComparison`, `LocalGL`, `GLn`, `CM`, `Cyclotomic`, `Analytic` | 27 250 | 26,2 M | 32,5 % |

L'argument propre (`New`) pèse donc environ un quart de la fermeture, et les théories d'arrière-plan reconstruites (`Lib`) un tiers. Les plus lourdes sont la représentation de Weil (4,4 %), les variétés de Shimura (3,7 %), les séries discrètes (3,4 %), la cohomologie (2,7 %) et le corps de classes (2,6 %). Comme dans l'original, la réduction et l'inégalité principale ne coûtent presque rien (0,5 %). La divisibilité par les dérivées thêta, cœur conceptuel du Théorème A, pèse moins de 1 %. Le gros du coût est dans les congruences, l'engendrement et la borne supérieure.

**Ce qui reste.** Apparier précisément ses Théorèmes A, B, C aux interfaces de `linkCore` (E17) ; lire le Théorème C, qui porte 45 % du poids.

## E19. Le bilan original exact : la pente cible se compense (niveau 3–4)

`trace_app.py --outline` sur `each_unit_bound_statement` et `Ga_bound5` ; `show.py --value` : `s_lower5`, `u_function_le_mean`, `K5v5`, `K0v5`, `Data.K3`, `Lo5`, `Data.s`, `uF`, `ErrX5at`, `Data.LoP`.

**Structure.** `each_unit_bound_statement` ne fait que deux pas. Il prend (A1), `ASK − Ga ≤ LoP` (projection de `LossBounds`), et une borne sur le gain total, `Ga_bound5`, qui porte tout le bilan (55 k lignes dominées) :
$$\Gamma\;\le\;\mathrm{Main}+\log\lvert\mathcal W\rvert+K_0+\langle\mathrm{Lo5}\rangle+(1-\bar\delta)^{-1}\Big(4\log(1+x^{c_{HH}})\big(K_3+\langle\mathrm{Lo5}\rangle+b\big)+(\bar\eta+4\sqrt{\bar e})\,x^{c_{HH}}b\Big),$$
où $\langle\cdot\rangle$ est la moyenne sur les mots pondérée par les rangs $d_u$ (`wmean`).

**Le squelette de `Ga_bound5`.** Il n'y a pas d'inégalité « R3 » séparée : Lean fait **se compenser la pente cible $\mu_R$** entre deux bornes sur le seuil $s=\langle\mu(N)-h\rangle$ (`Data.s`).

1. `s_lower5`, à partir de `DIV`, `EComp5`, `Count5`, `Slopes`, `QuotientSlopeBoundsWith` et `HidaSetting` (A2, A4, A5, A6, A7) : $\Gamma+\mu_R-K_5-\langle\mathrm{Lo5}\rangle\le s$. Ici $\mathrm{Lo5}_u=c_{Sl1}I+c_{Sl1}n_Tm(a/k+b')\log T_u+c_{Sl1}X''+1$ est la perte de (A2) mot par mot, et $K_5$ regroupe les erreurs de (A7), (A5) et (A4) avec le terme $S_{\rm Div}-A\,\Lambda_5$.
2. `SlopeIneq` appliqué avec $Z=$ `HH`, donc sous `HHBound` (A3) : $s-\log\lvert\mathcal W\rvert-(1-\delta)^{-1}\big(4u_F\log(1+Z/u_F)+(\eta+4\sqrt e)Z\big)\le\mu_R$.
3. `u_function_le_mean`, à partir de (A2⁺), (A5), `HComp` (H), (A6), (A7) : l'étalement $u_F=\max_u(\mu_{\max}(N_u)-h_u)-s$ vérifie $u_F\le K_3+\langle\mathrm{Lo5}\rangle$, avec $K_3=c_{\rm Sl}n_TaL_a(2+m/k)+V_{\rm var}+c_{Sl1}mB_0$.
4. `phi_bound` : la monotonie de $v\mapsto v\log(1+Z/v)$ et $Z\le x^{c_{HH}}b$ remplacent $u_F$ et $Z$ par leurs majorants (Nelson, exercice 59.1.4) ; $\delta\le\bar\delta$, $\eta\le\bar\eta$, $e\le\bar e$ par `FParams`.
5. `key_identity5` (E1) : $S_{\rm Div}-A\Lambda_5+mA\lg=\mathrm{Main}+A\,c_{\rm Count}(L_a+m^2L_a/k)$, d'où $K_5=\mathrm{Main}+K_0$ : **le terme principal apparaît**.

En combinant 1 et 2, $\mu_R$ disparaît, et 3 à 5 donnent la borne.

**Les coefficients exacts.** La conclusion de `each_unit_bound_statement` est $\mathrm{ASK}\le\mathrm{Main}+\mathrm{ErrX5at}$, et `ErrX5at` est la somme, terme à terme, des erreurs de chaque entrée :

| Terme de `ErrX5at` | Entrée | Multiplicateur |
|---|---|---|
| $A\,c_{\rm Count}(L_a+m^2L_a/k)$ | (A6) | $A$ |
| $c_{\rm Div}n_TaL_a+c_{\rm Div}m(B_0+N_c)x^{e_D\varepsilon}$ | (A4) | 1 |
| $m\,c_EB_0$ | (A5) | 1 |
| $c_{\rm Sl}n_TaL_a(1+m/k)$ | (A7) | 1 |
| $\log\lvert\mathcal W\rvert+(1-\bar\delta)^{-1}\big(4\log(1+x^{c_{HH}})(\bar U+b)+(\bar\eta+4\sqrt{\bar e})x^{c_{HH}}b\big)$ | (A3), avec $\bar U$ (`UBar5`) majorant de l'étalement | 1 |
| `LoP` $=c_{\rm Loss}n_Tmb\,x^{e_L\varepsilon}$ | (A1) | 1 |
| `MLo5` (majorant de $\langle\mathrm{Lo5}\rangle$) | (A2) | 1 |

C'est le certificat $(1,1,1,1,1,A,1)$ du modèle relaxé, avec la forme moyennée de (A3) de Nelson : sous $\bar\delta\le\frac12$ et $(\bar\eta+4\sqrt{\bar e})x^{c_{HH}}\le6$, le terme de (A3) est au plus $\log\lvert\mathcal W\rvert+8\log(1+x^{c_{HH}})(\bar U+b)+12b$, son $e_3$ (exercice 59.1.5).

**Statut.** La dérivation est lue au niveau des énoncés intermédiaires (squelette `--outline`, chaque étape avec son énoncé et le lemme qui la justifie), et elle concorde avec la reconstruction de la synthèse (§ 6.2). Les preuves de `s_lower5` et de `u_function_le_mean` (8,7 k lignes) ne sont pas lues ligne à ligne ; ce sont des combinaisons de moyennes pondérées des entrées.

## E20. Le bilan court exact : trois réels, nom pour nom (niveau 4)

Export lisible de Sernau (`export_short/out_read`). `trace_app.py --outline New.star_inequality` ; valeurs des `let` lues avec `lexpr`.

**Les quantités.** La preuve de `New.star_inequality` pose
$$F=\texttt{loss}=f\,a\,(\log b)^4,\qquad \texttt{logNormSq}=\texttt{mainAmount}-m\cdot\mathrm{rem}+F,\qquad I=\texttt{indexPerDim}=10\log(1+2b^2)\cdot U,$$
avec $U=$ `errorUnit` $=f\,a\,(\log b)^3$, et `err` $=4F+2I$.

**Le squelette.**

1. `span_short_integralRamified_eq_top` (A1) : les formes entières courtes engendrent. Leurs images par les translatés normalisés de l'application de Poincaré engendrent la même chose que les images de toutes les formes (`span_eq`). On en extrait une base $y_1,\dots,y_n$, avec $n\le d_T$.
2. `covolumeLe_of_normSqAt_le` (Hadamard) : covolume logarithmique $c\le n\cdot$`logNormSq`.
3. `indexLe_normalizedPoincare` (A2), avec le $J$ de `enough_forms` (B) : indice logarithmique $\delta\le d_T\cdot I$.
4. `integral_forms_long` (Théorème C) : $d_T(\texttt{mainAmount}-3F)\le c+2\delta$.
5. `h_main` : $n(\texttt{mainAmount}+F)\le d_T(\texttt{mainAmount}+F)$, puisque $n\le d_T$ et $\texttt{mainAmount}+F\ge0$ (`mainAmount_nonneg`). C'est le pas « $H+F\ge0$ » de l'Atelier 6, sans lequel la conclusion tombe.
6. `h_both` : $n\,m\,\mathrm{rem}\le d_T\cdot$`err`.
7. `h_half` : $d_T\le2n$, de $(1-4/b^2)d_T\le n$ (B) et $4/b^2\le\frac12$.
8. `h_err` : $\lvert2\,\mathrm{err}\rvert\le f\,a\,(\log b)^5$, d'où $m\cdot\mathrm{rem}\le fa(\log b)^5$.

**Lecture.** C'est exactement le modèle à trois réels de l'Atelier 6 de la synthèse, avec $H=$ `mainAmount`, $\rho=m\cdot\mathrm{rem}$, $F$ et $I$ ci-dessus, et les exercices 35.2.1 à 35.2.4 de Nelson. Les quantités $c$ et $\delta$ sont bien logarithmiques : `CovolumeLe` borne le logarithme du déterminant de Gram, et `IndexLe` une somme $\sum\delta_\ell\log\ell$ (guide de Sernau, glossaire). L'indice est pris dans le réseau cible des formes tordues, `targetLattice`. Lu au niveau des énoncés intermédiaires ; les quatre théorèmes appelés sont ceux du tableau A, B, C de E18.

## E21. Une divergence entre les deux routes : la minoration du covolume cible (niveau 2–3)

Les deux exports. `show.py` sur `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt` (original) et `New.Data.integral_forms_long` (route courte) ; `revindex.py refs` ; comptage des noms par motif dans les deux fermetures (`decl_domtree.tsv.gz`, `export_short/out_read/domtree.tsv`).

**Le rôle commun.** Dans les deux bilans, le terme principal entre par une inégalité **arithmétique du côté de la cible**, qui minore son covolume ou, de façon équivalente, majore sa pente, puisque $\mu=-\log\mathrm{covol}/\mathrm{rang}$. Dans l'original, c'est (A4), $\mu_R+h_u-\mathcal L\le P-A\log T_u+e_4$, où $P=m\sum_t\varphi(a_t)-mA\log\Omega$ porte le terme principal (E17, E19). Dans la route courte, c'est le Théorème C, $d_T(\texttt{mainAmount}-3F)\le c+2\delta$ (E20). Même rôle au sens N1–N2 de *Démêler la preuve* (§ 10.2) : une borne du volume cible par le terme principal. Les objets diffèrent toutefois : la pente d'un réseau de formes dans un cas, le covolume et l'indice d'une famille de formes tordues dans l'autre.

**Deux producteurs.**

- *Original : géométrie d'Arakelov sur les variétés de Shimura.* Le producteur est `topCovolSlim2_use_alt_alt`, qui domine 80 720 déclarations et 75,1 M lignes (7,1 % de la fermeture) ; son unique référent est `every_character_of_literature_of_vWin`. Il prend en hypothèse quinze énoncés « publiés » : `ResolutionCharZero`, `PrincipalisationCharZero`, `PoincareLelongInv`, `HSUse` (Hilbert–Samuel), `MoriwakiBigStatement`, `FarguesExact`, `ZarhinStatement`, `NefRR`, `SiegelToroidalIntegral`, `ToroidalForFanKS`, `SemiAbelianLieSeminegative`, `PointSeparationPair`, `ArDegree`, `PublishedHodgeBundleTheorems`, `GrothendieckDeformation`. Il conclut `CovolumeBoundOfX`. C'est l'estimation de covolume du Théorème 47.2.2 de Nelson et du ch. 51 (revêtement, changement de poids, Hilbert–Samuel arithmétique effectif, descente).
- *Route courte : déterminant d'une chaîne de relèvements.* Le producteur est `integral_forms_long`, qui domine 54 563 déclarations et 36,3 M lignes (45 % de la fermeture). Selon son guide, il passe par une torsion par premier, les normes des relèvements thêta, l'identité d'échange, la norme d'une chaîne, les valeurs de Hecke comme normes, les congruences et les bornes de Selmer anticyclotomiques (dossiers `Determinant`, `OneLift`, `Congruences`).

**Les théories mobilisées**, par le nombre de déclarations de chaque fermeture dont le nom contient le motif :

| Motif | Original | Route courte |
|---|---:|---:|
| Hilbert–Samuel | 5 962 | 0 |
| Arakelov, degré arithmétique | 1 105 | 0 |
| compactification toroïdale | 190 | 0 |
| Moriwaki | 14 | 0 |
| résolution (Hironaka…) | 10 918 | 149 |
| Rallis | 302 | 47 |
| Chowla–Selberg | 3 | 13 |
| Selmer | 1 101 | 1 969 |

**Lecture.** C'est une première divergence mathématique caractérisée : même rôle, deux producteurs, deux familles de théories. La route courte se passe entièrement de la géométrie d'Arakelov sur les modèles entiers de variétés de Shimura, qui était dans l'original l'un des deux plus gros organes archimédiens (synthèse, § 5.6). Elle la remplace par une borne inférieure obtenue par des normes de relèvements thêta et le contrôle de leurs dénominateurs, où Selmer, déjà présent dans l'original pour les places tordues, prend la place centrale. En coût absolu, le producteur court est environ deux fois plus léger, mais il porte une part bien plus grande de sa preuve.

**Limites.** Le comptage par motif de nom est indicatif (statut N0 pour les noms, N1 pour les rôles) : un concept peut être présent sous un autre nom. Les deux énoncés ne portent pas sur les mêmes objets, et nous n'avons pas démontré d'implication entre eux (N3). Le lien exact entre la pente de (A4) et le couple covolume–indice du Théorème C reste à écrire.

## E22. Une transformation recertifiée : deux clauses inertes retirées du Théorème B court (niveau 4)

Édition compacte de `lsernau/grh-lean` (commit `72fead1`), compilée localement : la contrainte « ne rien exécuter qui vienne de l'archive » a été levée par l'auteur pour ce seul projet, dans `export_short/build_sernau/`. Lean v4.35.0, Mathlib `56a00585` (cache officiel). Patch : `analysis/patches/patch_enough_forms.py`, diff dans `analysis/patches/enough_forms.diff`.

**Le choix de la clause.** `inertes.py`, corrigé (voir ci-dessous), trouve 35 théorèmes concernés dans l'édition compacte. Les candidats `_proof_*` sont engendrés par le compilateur et absents du source. Parmi les déclarations nommées :

- `map_restrict_haar_eq` : sa clause inerte, une égalité de mesures, sert à démontrer l'autre (`E ▸ inferInstance`). La retirer de l'énoncé ne retirerait aucune preuve : **une clause inerte n'est pas une preuve morte**.
- `Data.enough_forms`, le Théorème B court : l'énoncé est $0<\dim(\text{colonnes})\wedge0<\dim(\text{lignes})\wedge\exists t,\dots$, et l'unique consommateur, `exists_family_covolumeSq_le`, déstructure en `-, -, t, ht, big` en ignorant les deux premières clauses. Leurs preuves (`finrank_pos`, `D.finrank_rows_ne_zero.pos`) sont indépendantes de la troisième.

**Le patch.** L'énoncé de `Data.enough_forms` devient la seule clause $\exists t,\dots$ ; sa preuve perd les deux preuves de positivité ; le motif du consommateur devient `t, ht, big`. Deux fichiers, sept lignes changées.

**La recertification.**

- Référence non modifiée : `lake build` réussit (9 843 tâches, 2 h 15, pic de 6,6 Go sur un Mac M1 de 16 Go), et `#print axioms` donne `propext`, `Classical.choice`, `Quot.sound` pour les cinq théorèmes. Le résultat de Sutherland et de Rubinstein est reproduit en local.
- Projet patché : recompilation incrémentale réussie en 5 min 23 s (quatre modules refaits : `New.Endgame.ShortAndEnough`, `New.Endgame.LongForms`, `New.Main`, `Main`), mêmes axiomes.
- `Statements.lean` et `Main.lean` sont identiques à l'original, octet pour octet : les cinq énoncés n'ont pas changé. Le comparateur officiel (`comparator.json`), qui demande Linux et environ 64 Go, n'a pas été lancé.

**Le gain net.** Il est à peu près nul, et c'est attendu. `finrank_rows_ne_zero` reste utilisé par `star_inequality` et `exists_comparison_forms`, et le caractère non trivial des colonnes par d'autres preuves : aucune déclaration ne sort de la fermeture. Le gain se limite au terme de preuve de `Data.enough_forms` et à son énoncé, plus simple. La leçon : une clause inerte ne raccourcit la preuve que si sa démonstration n'est pas partagée. C'est la distinction de *Démêler la preuve* (§ 11) entre clause inerte, preuve morte et gain de fermeture.

**Un défaut corrigé dans `inertes.py`.** En cherchant ce candidat, nous avons trouvé un faux positif : `exists_lie_exponential` était déclaré entièrement inerte, alors que son consommateur utilise ses six composantes. Le théorème y est passé **comme argument fonctionnel** à `And.elim`, dont le résultat, une fonction, est ensuite appliqué à d'autres arguments. L'outil jetait le résultat dans ces deux situations : la conclusion d'une fonction non λ appliquée par un éliminateur (`lams`), et le résultat d'un éliminateur appliqué à plus d'arguments que prévu (sept branches). Il n'était donc **pas conservateur**. Corrigé le 27/11 : les analyses de E15 et E18 ont été refaites, voir E15.

## Synthèse

| Raccord | Cas (suggestions7bis) | Niveau |
|---|---|:-:|
| trois cartes (E3) | identité par construction (un seul champ `Bk`) | 3 |
| `gapA` → $G_\psi$ (E4) | identité `gmA_eq` + bornes individuelles | 3 |
| `key_identity5` (E1) | conversion par dépliage | 4 |
| `HypsAlt` → liens (E2) | branchement par application, 40 certificats + 6 données | 2 |
| gains `LinkG` (E5, E10) | `LPprime` : assemblage des arêtes reconstruit (4) ; rang par arête par récurrence sur le plus haut poids, formule de Weyl (2) ; admissibilité (Théorème A) | 2–4 |
| clauses inertes (E13, E15) | 5 729 théorèmes (6,43 %) livrent au moins une composante jamais lue ; 8 525 composantes inertes sur 19 107 ; poids mort mesurable ≥ 1,45 M lignes | 3 |
| comptabilité (E17) | onze hypothèses de `PointwiseBoundVariant` ↔ (A1)–(A7), (H) de Nelson ; conclusion = Théorème 58.1.1 ; chaque hypothèse rattachée à son interface de `linkCore` ; (A4), (A5), (H) sortent toutes de `LinkDIV` | 3 |
| preuve courte de Sernau (E18) | même architecture, noms tous nouveaux ; épine dorsale `grh` → `star_inequality` → Théorème C → Selmer → `GaloisRep` ; 165 composantes inertes | 2–3 |
| bilan original exact (E19) | `Ga_bound5` : $\mu_R$ se compense entre `s_lower5` et `SlopeIneq` ; `ErrX5at` = somme des erreurs, certificat $(1,1,1,1,1,A,1)$ | 3–4 |
| bilan court exact (E20) | `star_inequality` = modèle à trois réels : $H$ = `mainAmount`, $F=fa\log^4b$, $\rho=m\,\mathrm{rem}$, $I=10\log(1+2b^2)\,fa\log^3b$ | 4 |
| divergence (E21) | minoration du covolume cible : Arakelov sur Shimura (original, 75 M lignes) contre déterminant de chaîne et Selmer (court, 36 M) | 2–3 |
| transformation recertifiée (E22) | deux clauses inertes du Théorème B court retirées ; recompilation et axiomes contrôlés ; gain net nul (preuves partagées) | 4 |
| objections de Nielsen (E16) | Γ = champ porté, jamais lu ; modèle dégénéré = témoin d'un `∃` recopiant $Z$ ; hauteur = expression explicite ; aucune dépendance de `divClausesR_of` | 3 |
| pages (E6) | étages de la chaîne ; étape « tuer, détecter » reconstruite (proposition) | 4 |
| Ш → `LinkN` (E7) | défaut = module de congruences (4) ; borne locale et multiplicité `dZ0(j)` = dimension (3) ; mécanisme par Hodge p-adique (1–2) | 3 |
