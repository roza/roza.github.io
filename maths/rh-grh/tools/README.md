# Outils d'analyse de l'export de la preuve

Écrits avec l'assistance de Claude (Anthropic). Ils lisent l'export NDJSON de la preuve (format lean4export) publié par A. Sutherland (<https://math.mit.edu/~drew/grh/>), **en flux**, sans le décompresser sur le disque. Python ≥ 3.8 (bibliothèque standard) et un compilateur C.

| Outil | Rôle |
|---|---|
| `deps.c` | Passe 1, en C : `zstd -dc --long=30 solution.ndjson.zst \| ./deps OUT`. Dépendances de chaque déclaration (types **et** valeurs), DAG persisté en `mmap` (`c1/c2/aux.u32`, environ 13 Go). Compilation : `cc -O2 -o deps deps.c`. |
| `analyse_export.py OUT` | Fermeture de `riemannHypothesis` et des autres énoncés, dominateurs (Cooper–Harvey–Kennedy), poids dominés, composition, échafaudage. |
| `show.py OUT NOM… [--value]` | Réimprime l'énoncé (et la preuve) d'une déclaration ; `--grep REGEX` pour chercher un nom. |
| `query.py OUT spine \| deps NOM… \| refs NOM… \| cl NOM…` | Épine dorsale, dépendances directes, référents, taille de la fermeture. |
| `interfaces.py OUT [REGEX]` | Graphe des **interfaces** : pour chaque théorème, les prédicats `Prop` (par défaut ceux de `Formalism.MainNotions`) pris en hypothèse et conclus. Sortie TSV (`analysis/interfaces.tsv`). |
| `organes.py OUT interfaces.tsv LAB=nom …` | Pour chaque organe, les producteurs d'interfaces qui l'utilisent transitivement (par l'index inverse). |
| `modeles.py` | Calculs des modèles réduits de la synthèse (Tchebychev, $y^2=x^3-x$, Stepanov, masses, fluctuations de $G$) et figures SVG. Bibliothèque standard seule. |
| `revindex.py OUT build \| up NOM \| refs NOM… \| path SOURCE CIBLE…` | Index inverse ; `path` dit si SOURCE utilise transitivement CIBLE et donne la chaîne. |
| `poids.py [DOMTREE] [--set FICHIER] [--csv SORTIE] [--max SORTIE]` | Poids dominés selon trois pondérations (déclarations, lignes de l'export, nœuds d'expression par déclaration) et union reproductible d'un ensemble de nœuds (éléments maximaux pour la domination). Listes utilisées : `analysis/composantes.txt`, `analysis/mecanisme.txt`. |
| `fig_poids.py CSV DOSSIER` | Figure SVG des poids dominés selon les trois pondérations (FR et EN), à partir de `analysis/poids_composantes.csv`. |
| `frontiere.py OUT RACINE CONFIG [--test]` | Frontières de lecture : ce qui reste à lire quand on admet des théorèmes (on garde leur énoncé, on coupe leur preuve), comparé à la suppression des sommets et à l'union des poids dominés ; trois pondérations, et composition bibliothèques/projet. Configurations : `analysis/frontieres.txt`. |
| `tests.py [--rapide]` | Tests de non-régression sans l'export : losange de `frontiere.py`, lemniscate, modèles réduits (table du § 6.2, masses de Siegel, ϖ), poids publiés retrouvés depuis l'arbre des dominateurs, empreintes de `analysis/checksums.sha256`. |
| `instantane.py ÉTIQUETTE` | Instantané figé et reproductible (archive déterministe et manifeste SHA-256) dans `analysis/instantanes/`. |
| `fig_frontieres.py RÉSULTATS DOSSIER` | Figure SVG des frontières de lecture (FR et EN), à partir de `analysis/frontieres_resultats.txt`. |
| `fig_schemas.py DOSSIER` | Quatre schémas réels en Graphviz (FR et EN) : sommet du graphe de la preuve, haut de l'arbre des dominateurs, dépendances autour de `ch_balance`, voisinage de `linkCore` dans le graphe des interfaces. Noms et chiffres lus sur l'export. |
| `fiche.py OUT STRUCT` | Fiche d'une structure : paramètres, champs nommés et types (télescope du constructeur). |
| `inertes.py OUT [--only NOM] [--budget N]` | Clauses inertes : pour chaque théorème dont la conclusion est une conjonction, suit les projections dans tous ses référents (éliminateurs, β-rédex, transmission interprocédurale sur 8 niveaux) ; analyse conservatrice. Lit `OUT/domtree.tsv` s'il existe, sinon `analysis/decl_domtree.tsv.gz`, et `decl2mod.tsv` à côté de `OUT`. Sortie : `analysis/inertes.tsv` (E15). |
| `occ.py OUT DECL CIBLE…` | Pour une preuve, où apparaissent les constantes cherchées, avec l'application qui les englobe (parcours complet du DAG, sans troncature). |
| `frontiere_donnees.py OUT FICHIER` | Remonte depuis une liste d'objets en ne traversant que des définitions ; liste les définitions atteintes et les théorèmes de frontière avec leur énoncé (E16 : `analysis/nielsen_objets.txt`). |
| `modmap_src.py SRC DOMTREE SORTIE` | Rattache les déclarations d'un export à leurs fichiers source en lisant le texte des `.lean` (espaces de noms, déclarations, noms privés), sans compiler ni exécuter ; poids par dossier sur stderr (E18). |
| `lexpr.py` | Bibliothèque : lecture du DAG d'expressions de `deps.c` et impression lisible (le code de `show.py` sous forme importable). |
| `trace_app.py OUT DECL [--callee RE] [--types] [--implicit] [--all] [--json F] [--dot F]` | **Graphe des applications instanciées** : dans le terme de preuve de DECL, chaque application de théorème ou de constructeur, son contexte de lieurs, ses arguments alignés sur le télescope de l'appelé, la provenance de chaque argument (locale, `have`/`let`, projection, autre occurrence) et, avec `--types`, les types instanciés à l'affichage ; `--outline` donne le squelette de la preuve (suite des `have`/`let` avec leur énoncé et le lemme qui les justifie), `--reading` la liste de lecture (lemmes dominés par la cible, à lire en preuve ; lemmes extérieurs, à lire en énoncé). Les alias (valeur réduite à une constante) sont suivis. `--slice CALLEE:PARAM [--depth N]` fait un **tranchage arrière** (*backward slicing*) : il remonte la provenance d'un seul argument (variables → lieurs, `let`/`have` → valeur, applications → arguments explicites, projections → structure) jusqu'aux lieurs de la déclaration. Pas de vérification de convertibilité. Résultats : `analysis/raccords.md`. |
| `fig_landau.py DOSSIER` | Figure SVG du noyau gamma qui localise Landau dans une fenêtre d'échelles (FR et EN). |

Sans refaire la passe 1, `query.py OUT spine` et `query.py OUT cl NOM` fonctionnent avec le seul arbre des dominateurs. Télécharge-le depuis la [release GitHub](https://github.com/roza/roza.github.io/releases/tag/rh-grh-data-v1.0) et place-le dans `analysis/decl_domtree.tsv.gz`, à côté de `tools/`.

Toute conclusion négative (« X n'est pas utilisé ») doit être établie avec ces outils sur l'export, et non par recherche textuelle dans le source : celle-ci rate les constructions anonymes.


**Instantané figé.** La version citée par l’article 1.3.1 est `analysis/instantanes/rh-check-outils-v1.2-2026-11-27.tar.gz` (les archives `v1.0-2026-11-25` et `v1.1-2026-11-26` ont été régénérées et ne reflètent plus l'état de leur date) ; son manifeste donne l'empreinte de chaque fichier et celle de l'archive. `python3 -I tools/instantane.py v1.2-2026-11-27` la reconstruit à l'identique tant que les fichiers n'ont pas changé.

## Tests, limites et version

**Version.** Les outils cités par l’article 1.3.1 sont ceux de l'instantané `v1.2-2026-11-27` ; son manifeste donne l'empreinte de chaque fichier. `inertes.py` y est dans sa version corrigée du 27/11/2026.

**Tests.** `python3 -I tools/tests.py` vérifie, sans l'export : la frontière sur un exemple (`frontiere.py --test`), les modèles numériques (`lemniscate.py`, `modeles.py`), les poids publiés recalculés à partir de l'arbre des dominateurs (`poids.py`), et les empreintes de `analysis/checksums.sha256`. Si l'extraction de l'export est présente, il rejoue aussi `trace_app.py` sur `everyCharacter_of_row`.

**Limites des analyseurs.**

- *Graphe de dépendances* (`deps.c`, `analyse_export.py`, `revindex.py`) : il sur-approxime l'usage, toute constante citée dans un terme comptant comme une dépendance. Une absence de chemin est un résultat syntaxique sur cet export et ces conventions, non une indépendance sémantique.
- *Graphe des applications* (`trace_app.py`) : il ne vérifie aucune conversion définitionnelle ; une expression ouverte se lit avec son contexte.
- *Clauses inertes* (`inertes.py`) : l'analyse se veut conservatrice (tout usage non suivi compte comme une lecture), mais c'est un objectif de conception, non une garantie démontrée. Deux défauts ont été trouvés et corrigés le 27/11/2026 : un théorème passé comme argument fonctionnel à un éliminateur (`And.elim f h`), ou un éliminateur appliqué à plus d'arguments que prévu, perdait sa trace, d'où des faux positifs (carnet, E22). Cas de non-régression, sur l'édition compacte de la preuve de Sernau : `exists_lie_exponential` n'est pas inerte, `map_restrict_haar_eq` l'est. Ils demandent l'export de Sernau et ne sont pas dans `tests.py`. Une clause inerte n'est pas une preuve morte : sa démonstration peut servir ailleurs, ou à démontrer une autre clause.
- *Frontière en données* (`frontiere_donnees.py`) : résultat syntaxique, non un théorème de non-interférence ; `Classical.choose` donne accès au témoin d'un `∃`, même s'il reste opaque.
- *Rattachement aux fichiers* (`modmap_src.py`) : lecture du texte des `.lean`, sans compilation ; les déclarations auxiliaires anonymes (instances) ne sont pas toutes rattachées.

**Licence.** Les outils de ce répertoire sont sous licence MIT (voir `LICENSE`). Les textes, figures et données du projet sont sous CC BY-NC 4.0.
