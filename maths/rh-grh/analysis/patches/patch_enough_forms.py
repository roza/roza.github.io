"""Retire les deux clauses inertes de Data.enough_forms (édition compacte de grh-lean, 72fead1)
et adapte son unique consommateur. Usage : python3 -I patch_enough_forms.py RACINE_DU_PROJET"""
import sys, os
R = sys.argv[1]
def sub(rel, old, new):
    p = os.path.join(R, rel); s = open(p).read()
    assert s.count(old) == 1, (rel, s.count(old), old[:60])
    open(p, 'w').write(s.replace(old, new)); print(rel, 'ok')
sub('src/New/Endgame/ShortAndEnough.lean',
"""/-- Enough forms: columns and rows are non-zero, and for some set t ⊂ 𝖦 with #t·dim(columns) ≤
5D log(1 + b²), D = dim(rows), the images of the maps `Data.projectedPoincare` s, s ∈ t, span
dimension at least (1 − 4/b²)D. -/
lemma Data.enough_forms : 0 < finrank ℂ D.Column ∧ 0 < D.rowDim ∧
  ∃ t, #t * finrank ℂ D.Column ≤ 5 * D.rowDim * log (1 + D.b ^ 2) ∧ (1 - 4 / D.b ^ 2) * D.rowDim ≤
  finrank ℂ ↥(⨆ s ∈ t, (D.projectedPoincare s).range) := have := D.columnCoords.nontrivial
  ⟨finrank_pos, D.finrank_rows_ne_zero.pos, (exists_few_translates (W :=
    D.rows) (HasLogBound.pos D) (D.ramifiedColumns_fill_rows _)).imp fun _ ↦ .imp (by simp)
    (·.trans (mod_cast finrank_mono (iSup₂_mono fun _ _ _ ⟨φ, e⟩ ↦ ⟨⟨_, φ, rfl⟩, e⟩)))⟩""",
"""/-- Enough forms: for some set t ⊂ 𝖦 with #t·dim(columns) ≤ 5D log(1 + b²), D = dim(rows), the
images of the maps `Data.projectedPoincare` s, s ∈ t, span dimension at least (1 − 4/b²)D.
(Patched 2026-11-27: the two positivity clauses, never read by the only consumer, are removed.) -/
lemma Data.enough_forms :
  ∃ t, #t * finrank ℂ D.Column ≤ 5 * D.rowDim * log (1 + D.b ^ 2) ∧ (1 - 4 / D.b ^ 2) * D.rowDim ≤
  finrank ℂ ↥(⨆ s ∈ t, (D.projectedPoincare s).range) := have := D.columnCoords.nontrivial
  (exists_few_translates (W :=
    D.rows) (HasLogBound.pos D) (D.ramifiedColumns_fill_rows _)).imp fun _ ↦ .imp (by simp)
    (·.trans (mod_cast finrank_mono (iSup₂_mono fun _ _ _ ⟨φ, e⟩ ↦ ⟨⟨_, φ, rfl⟩, e⟩)))""")
sub('src/New/Endgame/LongForms.lean',
"  obtain ⟨⟨q, q0, B, hB, ⟨S, hS, sp, size⟩, index⟩, -, -, t, ht, big⟩ :=",
"  obtain ⟨⟨q, q0, B, hB, ⟨S, hS, sp, size⟩, index⟩, t, ht, big⟩ :=")
