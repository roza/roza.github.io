---
layout: page
title: "Catégories"
permalink: /categories/
---

<img src="/assets/images/babel.svg" alt="Bibliothèque de Babel" style="width:100%;height:auto;display:block;margin-bottom:2rem;border-radius:6px;">

{% assign categories_list = site.categories | sort %}
{% for category in categories_list %}
  {% assign category_name = category[0] %}
  {% assign category_posts = category[1] %}
  <h2><a href="/categories/{{ category_name | slugify }}/">{{ category_name }}</a>
  <small>({{ category_posts.size }})</small></h2>
{% endfor %}
