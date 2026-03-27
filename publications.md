---
layout: page
title: "Publications"
permalink: /publications/
---

<style>
.books-section-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding-bottom: 6px;
  border-bottom: 2px solid currentColor;
  margin-bottom: 16px;
  margin-top: 2rem;
}
.books-section-label--dunod { color: #3b82f6; border-color: #3b82f6; }
.books-section-label--hatier { color: #059669; border-color: #059669; }

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 14px;
  margin-bottom: 2rem;
}

.book-card {
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.book-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.12);
  text-decoration: none;
}

.book-cover {
  width: 100%;
  aspect-ratio: 3/4;
  object-fit: cover;
  display: block;
}

.book-info {
  padding: 8px 10px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.book-title {
  font-size: 12px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.3;
}
.book-authors {
  font-size: 10px;
  color: #6b7280;
  line-height: 1.3;
}
.book-link {
  font-size: 10px;
  margin-top: auto;
  padding-top: 6px;
}
.book-link--dunod { color: #3b82f6; }
.book-link--hatier { color: #059669; }
</style>

<p style="color:#6b7280;font-size:14px;margin-bottom:1.5rem;">Ouvrages co-écrits, disponibles chez Dunod et Hatier.</p>

<div class="books-section-label books-section-label--dunod">Dunod</div>
<div class="books-grid">
  {% for book in site.data.books.dunod %}
  <a href="{{ book.url }}" class="book-card" target="_blank" rel="noopener">
    <img src="{{ book.cover }}" alt="{{ book.title }}" class="book-cover" loading="lazy">
    <div class="book-info">
      <span class="book-title">{{ book.title }}</span>
      <span class="book-authors">{{ book.authors }}</span>
      <span class="book-link book-link--dunod">dunod.com →</span>
    </div>
  </a>
  {% endfor %}
</div>

<div class="books-section-label books-section-label--hatier">Hatier</div>
<div class="books-grid">
  {% for book in site.data.books.hatier %}
  <a href="{{ book.url }}" class="book-card" target="_blank" rel="noopener">
    <img src="{{ book.cover }}" alt="{{ book.title }}" class="book-cover" loading="lazy">
    <div class="book-info">
      <span class="book-title">{{ book.title }}</span>
      <span class="book-authors">{{ book.authors }}</span>
      <span class="book-link book-link--hatier">hatier.fr →</span>
    </div>
  </a>
  {% endfor %}
</div>
