# Personnal Web site


Jekyll So-simple 
The following is a list of targets:

```shell
.
├── _config.yml
├── _plugins
├── _tabs
└── index.html

```

 Structure des fichiers à connaître

  ┌─────────────────┬───────────────────────────────────────────────┐
  │ Fichier/Dossier │                     Rôle                      │
  ├─────────────────┼───────────────────────────────────────────────┤
  │ _config.yml     │ Titre, description, navigation, plugins       │
  ├─────────────────┼───────────────────────────────────────────────┤
  │ index.html      │ Page d'accueil (cards de cours, bannière)     │
  ├─────────────────┼───────────────────────────────────────────────┤
  │ _posts/         │ Articles du blog (format YYYY-MM-DD-titre.md) │
  ├─────────────────┼───────────────────────────────────────────────┤
  │ _data/books.yml │ Données des livres (page Publications)        │
  ├─────────────────┼───────────────────────────────────────────────┤
  │ assets/images/  │ Images, icônes, SVGs                          │
  └─────────────────┴───────────────────────────────────────────────┘

## Modifier du contenu

- Texte d'une card de cours → index.html
- Bannière → assets/images/banner.svg (texte SVG direct)
- Titre/description du site → _config.yml
- Un article → le fichier .md correspondant dans _posts/
- Un livre → _data/books.yml

## Ajouter un article

### Créer un fichier dans _posts/ nommé YYYY-MM-DD-mon-titre.md avec ce header :

```yaml
  ---
  title: "Mon titre"
  date: 2026-03-30 10:00:00 +0100
  categories: [Cours]
  tags: [php, git]
  ---
```

  Contenu en Markdown...

  Publier les modifications
```sh
  git add nom-du-fichier-modifié
  git commit -m "description du changement"
  git push
```


Le site se rebuilt automatiquement sur GitHub Pages.

## Tester en local :

```sh
  bundle exec jekyll serve
```

→ Accessible sur http://localhost:4000