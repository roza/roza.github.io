# Outils d'analyse de l'export de la preuve

Écrits avec l'assistance de Claude (Anthropic). Ils lisent l'export NDJSON de la preuve (format lean4export) publié par A. Sutherland (<https://math.mit.edu/~drew/grh/>), **en flux**, sans le décompresser sur le disque. Python ≥ 3.8 (bibliothèque standard) et un compilateur C.

| Outil | Rôle |
|---|---|
| `deps.c` | Passe 1, en C : `zstd -dc --long=30 solution.ndjson.zst \| ./deps OUT`. Dépendances de chaque déclaration (types **et** valeurs), DAG persisté en `mmap` (`c1/c2/aux.u32`, environ 13 Go). Compilation : `cc -O2 -o deps deps.c`. |
| `analyse_export.py OUT` | Fermeture de `riemannHypothesis` et des autres énoncés, dominateurs (Cooper–Harvey–Kennedy), poids dominés, composition, échafaudage. |
| `show.py OUT NOM… [--value]` | Réimprime l'énoncé (et la preuve) d'une déclaration ; `--grep REGEX` pour chercher un nom. |
| `query.py OUT spine \| deps NOM… \| refs NOM… \| cl NOM…` | Épine dorsale, dépendances directes, référents, taille de la fermeture. |
| `revindex.py OUT build \| up NOM \| refs NOM… \| path SOURCE CIBLE…` | Index inverse ; `path` dit si SOURCE utilise transitivement CIBLE et donne la chaîne. |

Sans refaire la passe 1, `query.py OUT spine` et `query.py OUT cl NOM` fonctionnent avec le seul arbre des dominateurs. Télécharge-le depuis la [release GitHub](https://github.com/roza/roza.github.io/releases/tag/rh-grh-data-v1.0) et place-le dans `analysis/decl_domtree.tsv.gz`, à côté de `tools/`.

Toute conclusion négative (« X n'est pas utilisé ») doit être établie avec ces outils sur l'export, et non par recherche textuelle dans le source : celle-ci rate les constructions anonymes.
