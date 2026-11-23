# Analyse de l'export (niveau déclarations)

- déclarations exportées (nœuds ; un bloc inductif = 1 nœud) : **1468418**
- arêtes distinctes (décl → décl) : 114115002 ; références non résolues : 0
- fermeture de `riemannHypothesis` : **1468390** (100.00 %) ; poids 1065212063 lignes d'expr. (100.00 %)
- fermeture des 5 théorèmes de Main : **1468414** (100.00 %) ; poids 1065214329 (100.00 %)
- itérations dominateurs : 2

## Composition par paquet

| paquet | décl. exportées | dans fermeture Main | dans fermeture RH | poids (lignes expr.) fermeture Main |
|---|---:|---:|---:|---:|
| projet | 1261660 | 1261660 | 1261646 | 1023784408 (96.1 %) |
| mathlib | 176085 | 176085 | 176084 | 38914360 (3.7 %) |
| lean/mathlib (via challenge) | 23766 | 23765 | 23756 | 1897421 (0.2 %) |
| core | 6745 | 6742 | 6742 | 603389 (0.1 %) |
| batteries | 159 | 159 | 159 | 14741 (0.0 %) |
| aesop | 3 | 3 | 3 | 10 (0.0 %) |

## Présence des noms de l'échafaudage (suffixe exact du nom complet)

| motif | décl. exportées dont le nom finit par le motif | dont dans fermeture Main | exemples |
|---|---:|---:|---|
| `LitN` | 0 | 0 |  |
| `LitLoc` | 0 | 0 |  |
| `LitAut` | 0 | 0 |  |
| `Hypotheses₂` | 2 | 2 | `GlobalTheory.NLink.Hypotheses₂`, `UpperTheory.V.GC.Hypotheses₂` |
| `published_inputs_combined` | 0 | 0 |  |
| `Published.LocalLanglandsGL` | 0 | 0 |  |
| `LocalRepresentationTheoryHypothesesAlt` | 1 | 1 | `GlobalTheory.Mem.LiteralAutomorphy.LocalRepresentationTheoryHypothesesAlt` |
| `GlobalAutomorphicGaloisHypotheses'` | 1 | 1 | `GlobalTheory.Mem.LiteralAutomorphy.GlobalAutomorphicGaloisHypotheses'` |
| `OpenLiteratureStatements` | 1 | 1 | `UpperTheory.LiteratureTheorems.OpenLiteratureStatements` |
| `recTExists` | 1 | 1 | `UpperTheory.Zero.LLC.recTExists` |
| `cuspEx` | 1 | 1 | `UpperTheory.Zero.LLC.cuspEx` |
| `galoisLocalGlobalStrong_recParameter` | 1 | 1 | `UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter` |
| `vwin_of_row` | 1 | 1 | `UpperTheory.One.vwin_of_row` |
| `PropsB` | 1 | 1 | `UpperTheory.GalStar.PropsB` |
| `Row0b` | 1 | 1 | `UpperTheory.GalStar.Row0b` |
| `every_character_of_theta_integrals_local_matching` | 1 | 1 | `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` |
| `everyCharacter_of_row` | 1 | 1 | `UpperTheory.FinalTheorems.everyCharacter_of_row` |

## Nœuds structurants du projet (dominateurs du projet les plus lourds, hors chaînes triviales)

- `allChi` [thm] — 1409557 décl., 99.31 % ; idom = `ROOT`
- `UpperTheory.FinalTheorems.everyCharacter` [thm] — 1409556 décl., 99.31 % ; idom = `allChi`
- `UpperTheory.FinalTheorems.everyCharacter_of_row` [thm] — 982855 décl., 76.62 % ; idom = `UpperTheory.FinalTheorems.everyCharacter`
- `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin` [thm] — 849323 décl., 66.26 % ; idom = `UpperTheory.FinalTheorems.everyCharacter_of_row`
- `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` [thm] — 543325 décl., 41.45 % ; idom = `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin`
- `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound` [thm] — 451610 décl., 35.78 % ; idom = `UpperTheory.Lit.every_character_of_theta_integrals_local_matching`
- `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt` [thm] — 153377 décl., 15.04 % ; idom = `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound`
- `UpperTheory.One.vwin_of_row` [thm] — 92705 décl., 8.21 % ; idom = `UpperTheory.FinalTheorems.everyCharacter_of_row`
- `UpperTheory.One.Join.automorphic_window_of_inputs` [thm] — 92702 décl., 8.21 % ; idom = `UpperTheory.One.vwin_of_row`
- `UpperTheory.One.Join.v_window_of_depth_zero_residual_bc_cm` [thm] — 91716 décl., 8.13 % ; idom = `UpperTheory.One.Join.automorphic_window_of_inputs`
- `UpperTheory.V.v_window_of_literal_automorphy_n` [thm] — 91656 décl., 8.13 % ; idom = `UpperTheory.One.Join.v_window_of_depth_zero_residual_bc_cm`
- `UpperTheory.V.HV.DescentVanishingReductions.v_window_of_automorphy_csd_ss_mono_odd` [thm] — 91655 décl., 8.13 % ; idom = `UpperTheory.V.v_window_of_literal_automorphy_n`
- `UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt` [thm] — 80724 décl., 7.38 % ; idom = `UpperTheory.V.HV.DescentVanishingReductions.v_window_of_automorphy_csd_ss_mono_odd`
- `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt` [thm] — 80720 décl., 7.05 % ; idom = `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin`
- `GlobalTheory.T.large_unramified_exponent_bundles_exist_alt` [thm] — 37318 décl., 6.84 % ; idom = `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt`
- `GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt` [thm] — 37317 décl., 6.84 % ; idom = `GlobalTheory.T.large_unramified_exponent_bundles_exist_alt`
- `UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter` [thm] — 95102 décl., 6.31 % ; idom = `UpperTheory.FinalTheorems.everyCharacter`
- `UpperTheory.Gal.Int.galoisRepresentations_of_thetaLift` [thm] — 90962 décl., 6.07 % ; idom = `UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter`
- `UpperTheory.Gal.Int.Geo.geoOne_holds` [thm] — 82643 décl., 5.50 % ; idom = `UpperTheory.Gal.Int.galoisRepresentations_of_thetaLift`
- `UpperTheory.Gal.Int.Geo.geometric_realization_of_weight_one` [thm] — 79447 décl., 5.23 % ; idom = `UpperTheory.Gal.Int.Geo.geoOne_holds`
- `GlobalTheory.T.member_exists_baseLattice_alt` [thm] — 26263 décl., 4.58 % ; idom = `GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt`
- `GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt` [thm] — 26262 décl., 4.58 % ; idom = `GlobalTheory.T.member_exists_baseLattice_alt`
- `PositivityTheory.HtPt.Ah.deep_slim_use` [thm] — 46110 décl., 3.88 % ; idom = `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt`
- `GlobalTheory.CompanionTheory.Ar.Plug.deepStR_of_use` [thm] — 45411 décl., 3.84 % ; idom = `PositivityTheory.HtPt.Ah.deep_slim_use`
- `GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt` [thm] — 54172 décl., 3.52 % ; idom = `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt`
- `UpperTheory.Gal.Int.Geo.steps_holds` [thm] — 54486 décl., 3.24 % ; idom = `UpperTheory.Gal.Int.Geo.geometric_realization_of_weight_one`
- `GlobalTheory.Fc.S0.ontoX_and_lamLow_of_unitaryGroupHypotheses'` [thm] — 34969 décl., 2.90 % ; idom = `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound`
- `GlobalTheory.BigOn.ontoX_of_hypotheses_alt_alt` [thm] — 34362 décl., 2.85 % ; idom = `GlobalTheory.Fc.S0.ontoX_and_lamLow_of_unitaryGroupHypotheses'`
- `GlobalTheory.CompanionTheory.Ar.Link.good_tower_volume_theorem_bis` [thm] — 31846 décl., 2.83 % ; idom = `GlobalTheory.CompanionTheory.Ar.Plug.deepStR_of_use`
- `GlobalTheory.T.final_theorem_of_inputs_right` [thm] — 31842 décl., 2.83 % ; idom = `GlobalTheory.CompanionTheory.Ar.Link.good_tower_volume_theorem_bis`
- `GlobalTheory.CompanionTheory.Ar.Top.goodTower_volume_of_reduced` [thm] — 31841 décl., 2.83 % ; idom = `GlobalTheory.T.final_theorem_of_inputs_right`
- `GlobalTheory.T.sFino_and_secondNo_of_sFinl'` [thm] — 1736 décl., 2.69 % ; idom = `GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt`
- `GlobalTheory.HeightCounting.Up.sFino_and_secondNo_of_rat_cusp_finl` [thm] — 1735 décl., 2.69 % ; idom = `GlobalTheory.T.sFino_and_secondNo_of_sFinl'`
- `GlobalTheory.HeightCounting.Up.secondNo_of_sMt_sRat_sCusp_sFinl` [thm] — 1733 décl., 2.69 % ; idom = `GlobalTheory.HeightCounting.Up.sFino_and_secondNo_of_rat_cusp_finl`
- `UpperTheory.GalC.final_alt_alt` [thm] — 28195 décl., 2.48 % ; idom = `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt`
- `UpperTheory.GalC.final_of_alt` [thm] — 26622 décl., 2.40 % ; idom = `UpperTheory.GalC.final_alt_alt`
- `UpperTheory.GalC.linkedAt_linkN_of_boundAtTwoThree` [thm] — 25757 décl., 2.32 % ; idom = `UpperTheory.GalC.final_of_alt`
- `UpperTheory.GalC.linkN_of_boundAtTwoThree_slot` [thm] — 25756 décl., 2.32 % ; idom = `UpperTheory.GalC.linkedAt_linkN_of_boundAtTwoThree`
- `UpperTheory.GalC.linkN_of_twGood_galoisPreconditions` [thm] — 25755 décl., 2.32 % ; idom = `UpperTheory.GalC.linkN_of_boundAtTwoThree_slot`
- `GlobalTheory.T.good_tower_volume_theorem` [thm] — 27142 décl., 2.30 % ; idom = `GlobalTheory.CompanionTheory.Ar.Top.goodTower_volume_of_reduced`
- `GlobalTheory.CompanionTheory.Ar.Top.goodTower_and_volume` [thm] — 27141 décl., 2.30 % ; idom = `GlobalTheory.T.good_tower_volume_theorem`
- `GlobalTheory.T.open0_of_unitary_group_hypotheses` [thm] — 22768 décl., 2.29 % ; idom = `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound`
- `GlobalTheory.Fc.S0.Open0ProofU.open_orbit_of_unramified_exponents_alt` [thm] — 22767 décl., 2.29 % ; idom = `GlobalTheory.T.open0_of_unitary_group_hypotheses`
- `SelfIntersectionVolumeEstimates.topCovolG_alt_alt` [thm] — 20154 décl., 2.03 % ; idom = `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt`
- `GlobalTheory.T.moveToBase_of_inputs_serN` [thm] — 1362 décl., 1.83 % ; idom = `GlobalTheory.HeightCounting.Up.secondNo_of_sMt_sRat_sCusp_sFinl`
- `GlobalTheory.HeightCounting.Up.multiplicity_bound_of_local_components_alt` [thm] — 1360 décl., 1.83 % ; idom = `GlobalTheory.T.moveToBase_of_inputs_serN`
- `GlobalTheory.T.levelI_same_gal_transfer_to_levelB1_list` [thm] — 1356 décl., 1.83 % ; idom = `GlobalTheory.HeightCounting.Up.multiplicity_bound_of_local_components_alt`
- `GlobalTheory.HeightCounting.Up.exists_levelB1_carried_of_levelI_same_gal` [thm] — 1355 décl., 1.83 % ; idom = `GlobalTheory.T.levelI_same_gal_transfer_to_levelB1_list`
- `GlobalTheory.T.main_theorem_published_inputs_third_alt_alt` [thm] — 20146 décl., 1.81 % ; idom = `GlobalTheory.Fc.S0.Open0ProofU.open_orbit_of_unramified_exponents_alt`
- `GlobalTheory.miStarRow_alt_alt` [thm] — 20145 décl., 1.81 % ; idom = `GlobalTheory.T.main_theorem_published_inputs_third_alt_alt`
- `GlobalTheory.T.main_theorem_published_inputs_variant_alt_alt` [thm] — 19762 décl., 1.78 % ; idom = `GlobalTheory.miStarRow_alt_alt`
- `GlobalTheory.miStarRowClosing_alt_alt` [thm] — 19761 décl., 1.78 % ; idom = `GlobalTheory.T.main_theorem_published_inputs_variant_alt_alt`
- `GlobalTheory.T.main_theorem_published_results_final_alt_alt` [thm] — 19265 décl., 1.71 % ; idom = `GlobalTheory.miStarRowClosing_alt_alt`
- `GlobalTheory.Fam.miStar_row_alt_alt` [thm] — 19264 décl., 1.71 % ; idom = `GlobalTheory.T.main_theorem_published_results_final_alt_alt`
- `GlobalTheory.T.multiplicity_pos_of_restricted_eigenform_copy_alt` [thm] — 1220 décl., 1.69 % ; idom = `GlobalTheory.HeightCounting.Up.exists_levelB1_carried_of_levelI_same_gal`
- `GlobalTheory.HeightCounting.Up.multiplicity_lower_bound_of_restricted_copy_alt` [thm] — 1219 décl., 1.69 % ; idom = `GlobalTheory.T.multiplicity_pos_of_restricted_eigenform_copy_alt`
- `UpperTheory.Gal.Int.Geo.kodaira_spencer_of_weight_one` [thm] — 18918 décl., 1.69 % ; idom = `UpperTheory.Gal.Int.Geo.geometric_realization_of_weight_one`
- `GlobalTheory.T.conclF_of_family_facts_and_bound_at_two_three` [thm] — 18289 décl., 1.68 % ; idom = `UpperTheory.GalC.linkN_of_twGood_galoisPreconditions`
- `GlobalTheory.NLinkClose.main_alt_alt` [thm] — 18288 décl., 1.68 % ; idom = `GlobalTheory.T.conclF_of_family_facts_and_bound_at_two_three`
- `UpperTheory.Top.every_character_of_green_v_win` [thm] — 23523 décl., 1.56 % ; idom = `UpperTheory.Lit.every_character_of_theta_integrals_local_matching`
- `UpperTheory.Top.zero_free_all_of_green_v_win` [thm] — 23514 décl., 1.56 % ; idom = `UpperTheory.Top.every_character_of_green_v_win`
- `GlobalTheory.T.main_theorem_from_published_results_alt_alt_alt_alt_alt` [thm] — 18804 décl., 1.50 % ; idom = `GlobalTheory.Fam.miStar_row_alt_alt`
- `GlobalTheory.Fam.miAt_of_truePack_alt_alt` [thm] — 18802 décl., 1.50 % ; idom = `GlobalTheory.T.main_theorem_from_published_results_alt_alt_alt_alt_alt`
- `GlobalTheory.T.main_theorem_from_published_results_alt_alt_alt_alt` [thm] — 18801 décl., 1.50 % ; idom = `GlobalTheory.Fam.miAt_of_truePack_alt_alt`
- `GlobalTheory.Fam.miStar2_of_allTrue_alt_alt` [thm] — 18800 décl., 1.50 % ; idom = `GlobalTheory.T.main_theorem_from_published_results_alt_alt_alt_alt`
- `GlobalTheory.LocalRows.lg1_sLp_sO_hTF` [thm] — 23153 décl., 1.49 % ; idom = `GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt`
- `GlobalTheory.LocalRows.sLp_sO_hTF_of_siegelWeil` [thm] — 23152 décl., 1.49 % ; idom = `GlobalTheory.LocalRows.lg1_sLp_sO_hTF`
- `GlobalTheory.LocalRows.at_choice_alt` [thm] — 23151 décl., 1.49 % ; idom = `GlobalTheory.LocalRows.sLp_sO_hTF_of_siegelWeil`
- `GlobalTheory.CarrierGap.offDiag` [thm] — 22167 décl., 1.42 % ; idom = `GlobalTheory.LocalRows.at_choice_alt`
- `GlobalTheory.T.true_geometry_family_row_data_alt` [thm] — 17877 décl., 1.41 % ; idom = `GlobalTheory.Fam.miStar2_of_allTrue_alt_alt`
- `GlobalTheory.MiTop.famAllQ_of_allTrue_alt` [thm] — 17876 décl., 1.41 % ; idom = `GlobalTheory.T.true_geometry_family_row_data_alt`
- `GlobalTheory.T.mem_of_series_carry_alt` [thm] — 763 décl., 1.20 % ; idom = `GlobalTheory.HeightCounting.Up.multiplicity_lower_bound_of_restricted_copy_alt`
- `GlobalTheory.HeightCounting.SerCarry.series_restage_of_carry_alt` [thm] — 762 décl., 1.20 % ; idom = `GlobalTheory.T.mem_of_series_carry_alt`
- `UpperTheory.Top.shape_closed_link_n_of_green` [thm] — 19248 décl., 1.20 % ; idom = `UpperTheory.Top.zero_free_all_of_green_v_win`
- `GlobalTheory.TorKSField.toroidalForFanKS` [thm] — 7185 décl., 1.15 % ; idom = `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin`
- `UpperTheory.V.HV.DescentVanishingReductions.sp4In0_alt` [thm] — 11275 décl., 1.15 % ; idom = `UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt`
- `GlobalTheory.HeightCounting.SerCarry.series_move` [thm] — 526 décl., 1.13 % ; idom = `GlobalTheory.HeightCounting.SerCarry.series_restage_of_carry_alt`
- `GlobalTheory.FinalJoin.runHolds_of_parOK` [thm] — 10151 décl., 1.12 % ; idom = `GlobalTheory.BigOn.ontoX_of_hypotheses_alt_alt`
- `GlobalTheory.T.volume_theorem_of_inputs` [thm] — 13623 décl., 1.11 % ; idom = `GlobalTheory.CompanionTheory.Ar.Top.goodTower_and_volume`
- `GlobalTheory.CompanionTheory.Ar.Cusp.volumeTheoremX_of_inputs` [thm] — 13622 décl., 1.11 % ; idom = `GlobalTheory.T.volume_theorem_of_inputs`
- `UpperTheory.V.Z.Kato.WeilSphericalRecords.katoTwoW_of_printsH` [thm] — 15273 décl., 1.11 % ; idom = `UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt`
- `UpperTheory.V.Z.Kato.WeilSphericalRecords.katoTwoW_of_printsH_of_rT_of_quadBC2` [thm] — 15272 décl., 1.11 % ; idom = `UpperTheory.V.Z.Kato.WeilSphericalRecords.katoTwoW_of_printsH`
- `UpperTheory.V.Z.Kato.WeilSphericalRecords.twoS` [thm] — 14545 décl., 1.06 % ; idom = `UpperTheory.V.Z.Kato.WeilSphericalRecords.katoTwoW_of_printsH_of_rT_of_quadBC2`
- `UpperTheory.LiteratureTheorems.theta_integrals_agree_and_local_matching_of_literature` [thm] — 14173 décl., 1.05 % ; idom = `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin`
- `GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_pair_alt` [thm] — 13951 décl., 1.04 % ; idom = `GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt`
- `GlobalTheory.T.adelicData_extend_largerFields_of_hypotheses` [thm] — 866 décl., 1.03 % ; idom = `GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt`
- `GlobalTheory.Mem.R3.Rw.datExt0_of_hypotheses` [thm] — 865 décl., 1.03 % ; idom = `GlobalTheory.T.adelicData_extend_largerFields_of_hypotheses`
- `GlobalTheory.T.hServ_of_linkR` [thm] — 16285 décl., 1.03 % ; idom = `GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt`
- `GlobalTheory.row_hServ_of_link_alt` [thm] — 16284 décl., 1.03 % ; idom = `GlobalTheory.T.hServ_of_linkR`
- `GlobalTheory.T.reciprocity_kernel_of_artin` [thm] — 16273 décl., 1.03 % ; idom = `GlobalTheory.row_hServ_of_link_alt`
- `GlobalTheory.Svd.servH_row_linkR_alt` [thm] — 16272 décl., 1.03 % ; idom = `GlobalTheory.T.reciprocity_kernel_of_artin`
- `GlobalTheory.T.bundle_bothParts_of_standardKernel_of_globalArtinReciprocity` [thm] — 16264 décl., 1.03 % ; idom = `GlobalTheory.Svd.servH_row_linkR_alt`
- `GlobalTheory.Svd.servH_row_of_artin` [thm] — 16263 décl., 1.03 % ; idom = `GlobalTheory.T.bundle_bothParts_of_standardKernel_of_globalArtinReciprocity`
- `GlobalTheory.HeightCounting.SerCarry.serAt_move` [thm] — 305 décl., 1.02 % ; idom = `GlobalTheory.HeightCounting.SerCarry.series_move`
- `GlobalTheory.T.exists_indexBoundHypothesesWithNet_allValuedPoints` [thm] — 8558 décl., 1.02 % ; idom = `GlobalTheory.FinalJoin.runHolds_of_parOK`
- `GlobalTheory.InputsAtRecord.inputsNet_recPlus` [thm] — 8557 décl., 1.02 % ; idom = `GlobalTheory.T.exists_indexBoundHypothesesWithNet_allValuedPoints`
- `UpperTheory.V.Z.Kato.Final.zetaUr` [thm] — 12986 décl., 0.95 % ; idom = `UpperTheory.V.Z.Kato.WeilSphericalRecords.twoS`
- `GlobalTheory.T.exists_extendedColumnData_all_clauses_but_places` [thm] — 601 décl., 0.93 % ; idom = `GlobalTheory.Mem.R3.Rw.datExt0_of_hypotheses`
- `GlobalTheory.Mem.R3.Rw.ExtBuild.exists_ext_build` [thm] — 600 décl., 0.93 % ; idom = `GlobalTheory.T.exists_extendedColumnData_all_clauses_but_places`
- `GlobalTheory.T.exists_extendedAdelicData_with_intertwiners_over_enlargedCore` [thm] — 580 décl., 0.93 % ; idom = `GlobalTheory.Mem.R3.Rw.ExtBuild.exists_ext_build`
- `GlobalTheory.Mem.R3.Rw.datExt_rest` [thm] — 579 décl., 0.93 % ; idom = `GlobalTheory.T.exists_extendedAdelicData_with_intertwiners_over_enlargedCore`
- `UpperTheory.LiteratureTheorems.siegel_toroidal_integral_of_literature` [thm] — 5446 décl., 0.91 % ; idom = `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin`
- `GlobalTheory.siegelToroidalIntegral_holds` [thm] — 5445 décl., 0.91 % ; idom = `UpperTheory.LiteratureTheorems.siegel_toroidal_integral_of_literature`
- `GlobalTheory.T.siegelToroidalCompactification_polarisedCharts` [thm] — 5262 décl., 0.89 % ; idom = `GlobalTheory.siegelToroidalIntegral_holds`
- `GlobalTheory.SiegJoin.siegelToroidalPolCharts` [thm] — 5261 décl., 0.89 % ; idom = `GlobalTheory.T.siegelToroidalCompactification_polarisedCharts`
- `PositivityTheory.ThKR.theoremK_head2` [thm] — 11543 décl., 0.87 % ; idom = `UpperTheory.LiteratureTheorems.theta_integrals_agree_and_local_matching_of_literature`
- `PositivityTheory.ThKR.theoremK_head2_of_mod` [thm] — 11280 décl., 0.86 % ; idom = `PositivityTheory.ThKR.theoremK_head2`
- `GlobalTheory.T.rigidBoundaryChartsForFan_unitaryDatum` [thm] — 4240 décl., 0.80 % ; idom = `GlobalTheory.TorKSField.toroidalForFanKS`
- `GlobalTheory.RigChart.rigidForFan_holds` [thm] — 4239 décl., 0.80 % ; idom = `GlobalTheory.T.rigidBoundaryChartsForFan_unitaryDatum`
- `PositivityTheory.Sph.Tr.closeSph` [thm] — 8196 décl., 0.69 % ; idom = `PositivityTheory.ThKR.theoremK_head2_of_mod`
- `GlobalTheory.T.star_ad_and_bb_le_of_joint_cond` [thm] — 6332 décl., 0.68 % ; idom = `GlobalTheory.NLinkClose.main_alt_alt`
- `GlobalTheory.NLink.rowsAD_in_setting_alt` [thm] — 6331 décl., 0.68 % ; idom = `GlobalTheory.T.star_ad_and_bb_le_of_joint_cond`
- `GlobalTheory.T.adm_at_inert_of_range` [thm] — 6281 décl., 0.67 % ; idom = `GlobalTheory.NLink.rowsAD_in_setting_alt`
- `GlobalTheory.NLink.InertStep.main_alt_alt` [thm] — 6280 décl., 0.67 % ; idom = `GlobalTheory.T.adm_at_inert_of_range`
- `GlobalTheory.T.hasSemiAbelianUniformisation_complete_normal_base` [thm] — 4965 décl., 0.66 % ; idom = `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin`
- `GlobalTheory.Mum.has_of_base` [thm] — 4964 décl., 0.66 % ; idom = `GlobalTheory.T.hasSemiAbelianUniformisation_complete_normal_base`
- `GlobalTheory.T.bundle_bothParts_of_standardKernel_and_six_hypotheses` [thm] — 8803 décl., 0.65 % ; idom = `GlobalTheory.Svd.servH_row_of_artin`
- `GlobalTheory.Svd.servH_row` [thm] — 8802 décl., 0.65 % ; idom = `GlobalTheory.T.bundle_bothParts_of_standardKernel_and_six_hypotheses`
- `UpperTheory.V.Z.Sym.W.unitary_three_automorphy_dense_of_prints` [thm] — 6622 décl., 0.64 % ; idom = `UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt`
- `UpperTheory.V.Z.Sym.W.unitary_three_automorphy_dense_of_prints_and_row` [thm] — 6621 décl., 0.64 % ; idom = `UpperTheory.V.Z.Sym.W.unitary_three_automorphy_dense_of_prints`
- `Formalism.L2.G.linkG_concrete5` [thm] — 10772 décl., 0.64 % ; idom = `UpperTheory.Top.shape_closed_link_n_of_green`
- `GlobalTheory.RowClaim.Join.thetaLift_row_properties_conj` [thm] — 9399 décl., 0.63 % ; idom = `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound`
- `GlobalTheory.Mem.Top.Closing.memberE_closing_alt_alt` [thm] — 10148 décl., 0.58 % ; idom = `GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_pair_alt`
- `UpperTheory.Gal.Int.galoisLocalGlobalStrong_of_geometry_lift` [thm] — 8091 décl., 0.56 % ; idom = `UpperTheory.Gal.Int.galoisRepresentations_of_thetaLift`
- `UpperTheory.Gal.Int.galoisLocalGlobal_of_geometry_lift` [thm] — 8068 décl., 0.56 % ; idom = `UpperTheory.Gal.Int.galoisLocalGlobalStrong_of_geometry_lift`
- `GlobalTheory.T.geometricHalf_to_analyticData_enlargedBase` [thm] — 278 décl., 0.56 % ; idom = `GlobalTheory.Mem.R3.Rw.datExt_rest`
- `GlobalTheory.T.exists_const_tieChi_bound_of_facts` [thm] — 6332 décl., 0.56 % ; idom = `UpperTheory.GalC.linkN_of_twGood_galoisPreconditions`
- `GlobalTheory.ExtraFromFacts.main_alt_alt` [thm] — 6331 décl., 0.56 % ; idom = `GlobalTheory.T.exists_const_tieChi_bound_of_facts`
- `UpperTheory.Lit.functionalsSeparate_of_howeUnram_of_siegelWeil` [thm] — 7161 décl., 0.56 % ; idom = `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound`
- `GlobalTheory.CarrierGap.theoremS_leaves_of_carrierG` [thm] — 8961 décl., 0.56 % ; idom = `GlobalTheory.CarrierGap.offDiag`
- `UpperTheory.V.Z.Sym.W.adjoint_automorphy_w_of_printed_hida_window` [thm] — 5307 décl., 0.55 % ; idom = `UpperTheory.V.Z.Sym.W.unitary_three_automorphy_dense_of_prints_and_row`
- `GlobalTheory.T.minimalBlowup_smooth_with_semiAbelianCharts` [thm] — 3384 décl., 0.53 % ; idom = `GlobalTheory.SiegJoin.siegelToroidalPolCharts`
- `GlobalTheory.SiegJoin.chartSt5_holds` [thm] — 3383 décl., 0.53 % ; idom = `GlobalTheory.T.minimalBlowup_smooth_with_semiAbelianCharts`
- `GlobalTheory.T.true_geometry_family_invariance_alt` [thm] — 6300 décl., 0.52 % ; idom = `GlobalTheory.MiTop.famAllQ_of_allTrue_alt`
- `GlobalTheory.Fam.colSide_alt` [thm] — 6299 décl., 0.52 % ; idom = `GlobalTheory.T.true_geometry_family_invariance_alt`
- `UpperTheory.Gal.Int.Geo.jumpStep_holds` [thm] — 6094 décl., 0.52 % ; idom = `UpperTheory.Gal.Int.Geo.steps_holds`
- `GlobalTheory.HeightCounting.SerCarry.exportTie_move` [thm] — 289 décl., 0.52 % ; idom = `GlobalTheory.HeightCounting.SerCarry.serAt_move`
- `GlobalTheory.T.unitaryToroidalSeparation_of_base` [thm] — 2154 décl., 0.50 % ; idom = `GlobalTheory.RigChart.rigidForFan_holds`
- `GlobalTheory.UPoincTop.uStB` [thm] — 2153 décl., 0.50 % ; idom = `GlobalTheory.T.unitaryToroidalSeparation_of_base`
- `GlobalTheory.UPoincTop.uPoinStX_sep` [thm] — 2152 décl., 0.50 % ; idom = `GlobalTheory.UPoincTop.uStB`
- `GlobalTheory.HeightCounting.SideCopy.LamCopy.lam_copy` [thm] — 4 décl., 0.50 % ; idom = `GlobalTheory.HeightCounting.SerCarry.serAt_move`
- `GlobalTheory.T.globalLatticeIndexTheorem_of_lengthBoundAtPlaces` [thm] — 4685 décl., 0.49 % ; idom = `UpperTheory.Lit.every_character_of_theta_integrals_local_matching`
- `GlobalTheory.SelmerBoundAtPoint.main` [thm] — 4684 décl., 0.49 % ; idom = `GlobalTheory.T.globalLatticeIndexTheorem_of_lengthBoundAtPlaces`
- `GlobalTheory.BigTop.Fun.Close.fourier_coefficient_fit_of_join_alt` [thm] — 6720 décl., 0.49 % ; idom = `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound`
- `GlobalTheory.BigTop.Fun.Close.fittedFunction_at_zero_close_alt` [thm] — 6719 décl., 0.49 % ; idom = `GlobalTheory.BigTop.Fun.Close.fourier_coefficient_fit_of_join_alt`
- `GlobalTheory.CarrierGap.carrierP` [thm] — 8009 décl., 0.48 % ; idom = `GlobalTheory.CarrierGap.offDiag`
- `UpperTheory.V.Pa.pFromAut` [thm] — 4108 décl., 0.48 % ; idom = `UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt`
- `UpperTheory.Gal.Seam.HT.htSpecGood` [thm] — 5562 décl., 0.48 % ; idom = `UpperTheory.Gal.Int.Geo.jumpStep_holds`
- `UpperTheory.V.Z.Sym.W.specOutS` [thm] — 4551 décl., 0.47 % ; idom = `UpperTheory.V.Z.Sym.W.adjoint_automorphy_w_of_printed_hida_window`
- `GlobalTheory.BigOn.geoSt_of_pageSt_alt` [thm] — 7949 décl., 0.46 % ; idom = `GlobalTheory.BigOn.ontoX_of_hypotheses_alt_alt`

## Enfants directs de la racine virtuelle et premiers niveaux (poids = lignes d'expressions dominées)

- `allChi` [thm] — 1409557 décl., 99.31 %
  - `UpperTheory.FinalTheorems.everyCharacter` [thm] — 1409556 décl., 99.31 %
    - `UpperTheory.FinalTheorems.everyCharacter_of_row` [thm] — 982855 décl., 76.62 %
      - `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin` [thm] — 849323 décl., 66.26 %
        - `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` [thm] — 543325 décl., 41.45 %
          - `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound` [thm] — 451610 décl., 35.78 %
            - `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt` [thm] — 153377 décl., 15.04 %
              - `GlobalTheory.T.large_unramified_exponent_bundles_exist_alt` [thm] — 37318 décl., 6.84 %
                - `GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt` [thm] — 37317 décl., 6.84 %
                  - `GlobalTheory.T.member_exists_baseLattice_alt` [thm] — 26263 décl., 4.58 %
                    - `GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt` [thm] — 26262 décl., 4.58 %
                      - `GlobalTheory.T.sFino_and_secondNo_of_sFinl'` [thm] — 1736 décl., 2.69 %
                      - `GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_pair_alt` [thm] — 13951 décl., 1.04 %
                  - `GlobalTheory.T.adelicData_extend_largerFields_of_hypotheses` [thm] — 866 décl., 1.03 %
                    - `GlobalTheory.Mem.R3.Rw.datExt0_of_hypotheses` [thm] — 865 décl., 1.03 %
                      - `GlobalTheory.T.exists_extendedColumnData_all_clauses_but_places` [thm] — 601 décl., 0.93 %
              - `GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt` [thm] — 54172 décl., 3.52 %
                - `GlobalTheory.LocalRows.lg1_sLp_sO_hTF` [thm] — 23153 décl., 1.49 %
                  - `GlobalTheory.LocalRows.sLp_sO_hTF_of_siegelWeil` [thm] — 23152 décl., 1.49 %
                    - `GlobalTheory.LocalRows.at_choice_alt` [thm] — 23151 décl., 1.49 %
                      - `GlobalTheory.CarrierGap.offDiag` [thm] — 22167 décl., 1.42 %
                - `GlobalTheory.T.hServ_of_linkR` [thm] — 16285 décl., 1.03 %
                  - `GlobalTheory.row_hServ_of_link_alt` [thm] — 16284 décl., 1.03 %
                    - `GlobalTheory.T.reciprocity_kernel_of_artin` [thm] — 16273 décl., 1.03 %
                      - `GlobalTheory.Svd.servH_row_linkR_alt` [thm] — 16272 décl., 1.03 %
              - `UpperTheory.GalC.final_alt_alt` [thm] — 28195 décl., 2.48 %
                - `UpperTheory.GalC.final_of_alt` [thm] — 26622 décl., 2.40 %
                  - `UpperTheory.GalC.linkedAt_linkN_of_boundAtTwoThree` [thm] — 25757 décl., 2.32 %
                    - `UpperTheory.GalC.linkN_of_boundAtTwoThree_slot` [thm] — 25756 décl., 2.32 %
                      - `UpperTheory.GalC.linkN_of_twGood_galoisPreconditions` [thm] — 25755 décl., 2.32 %
            - `GlobalTheory.Fc.S0.ontoX_and_lamLow_of_unitaryGroupHypotheses'` [thm] — 34969 décl., 2.90 %
              - `GlobalTheory.BigOn.ontoX_of_hypotheses_alt_alt` [thm] — 34362 décl., 2.85 %
                - `GlobalTheory.FinalJoin.runHolds_of_parOK` [thm] — 10151 décl., 1.12 %
                  - `GlobalTheory.T.exists_indexBoundHypothesesWithNet_allValuedPoints` [thm] — 8558 décl., 1.02 %
                    - `GlobalTheory.InputsAtRecord.inputsNet_recPlus` [thm] — 8557 décl., 1.02 %
            - `GlobalTheory.T.open0_of_unitary_group_hypotheses` [thm] — 22768 décl., 2.29 %
              - `GlobalTheory.Fc.S0.Open0ProofU.open_orbit_of_unramified_exponents_alt` [thm] — 22767 décl., 2.29 %
                - `GlobalTheory.T.main_theorem_published_inputs_third_alt_alt` [thm] — 20146 décl., 1.81 %
                  - `GlobalTheory.miStarRow_alt_alt` [thm] — 20145 décl., 1.81 %
                    - `GlobalTheory.T.main_theorem_published_inputs_variant_alt_alt` [thm] — 19762 décl., 1.78 %
                      - `GlobalTheory.miStarRowClosing_alt_alt` [thm] — 19761 décl., 1.78 %
            - `GlobalTheory.RowClaim.Join.thetaLift_row_properties_conj` [thm] — 9399 décl., 0.63 %
            - `UpperTheory.Lit.functionalsSeparate_of_howeUnram_of_siegelWeil` [thm] — 7161 décl., 0.56 %
          - `UpperTheory.Top.every_character_of_green_v_win` [thm] — 23523 décl., 1.56 %
            - `UpperTheory.Top.zero_free_all_of_green_v_win` [thm] — 23514 décl., 1.56 %
              - `UpperTheory.Top.shape_closed_link_n_of_green` [thm] — 19248 décl., 1.20 %
                - `Formalism.L2.G.linkG_concrete5` [thm] — 10772 décl., 0.64 %
        - `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt` [thm] — 80720 décl., 7.05 %
          - `PositivityTheory.HtPt.Ah.deep_slim_use` [thm] — 46110 décl., 3.88 %
            - `GlobalTheory.CompanionTheory.Ar.Plug.deepStR_of_use` [thm] — 45411 décl., 3.84 %
              - `GlobalTheory.CompanionTheory.Ar.Link.good_tower_volume_theorem_bis` [thm] — 31846 décl., 2.83 %
                - `GlobalTheory.T.final_theorem_of_inputs_right` [thm] — 31842 décl., 2.83 %
                  - `GlobalTheory.CompanionTheory.Ar.Top.goodTower_volume_of_reduced` [thm] — 31841 décl., 2.83 %
                    - `GlobalTheory.T.good_tower_volume_theorem` [thm] — 27142 décl., 2.30 %
                      - `GlobalTheory.CompanionTheory.Ar.Top.goodTower_and_volume` [thm] — 27141 décl., 2.30 %
          - `SelfIntersectionVolumeEstimates.topCovolG_alt_alt` [thm] — 20154 décl., 2.03 %
        - `GlobalTheory.TorKSField.toroidalForFanKS` [thm] — 7185 décl., 1.15 %
          - `GlobalTheory.T.rigidBoundaryChartsForFan_unitaryDatum` [thm] — 4240 décl., 0.80 %
            - `GlobalTheory.RigChart.rigidForFan_holds` [thm] — 4239 décl., 0.80 %
              - `GlobalTheory.T.unitaryToroidalSeparation_of_base` [thm] — 2154 décl., 0.50 %
                - `GlobalTheory.UPoincTop.uStB` [thm] — 2153 décl., 0.50 %
                  - `GlobalTheory.UPoincTop.uPoinStX_sep` [thm] — 2152 décl., 0.50 %
        - `UpperTheory.LiteratureTheorems.theta_integrals_agree_and_local_matching_of_literature` [thm] — 14173 décl., 1.05 %
          - `PositivityTheory.ThKR.theoremK_head2` [thm] — 11543 décl., 0.87 %
            - `PositivityTheory.ThKR.theoremK_head2_of_mod` [thm] — 11280 décl., 0.86 %
              - `PositivityTheory.Sph.Tr.closeSph` [thm] — 8196 décl., 0.69 %
        - `UpperTheory.LiteratureTheorems.siegel_toroidal_integral_of_literature` [thm] — 5446 décl., 0.91 %
          - `GlobalTheory.siegelToroidalIntegral_holds` [thm] — 5445 décl., 0.91 %
            - `GlobalTheory.T.siegelToroidalCompactification_polarisedCharts` [thm] — 5262 décl., 0.89 %
              - `GlobalTheory.SiegJoin.siegelToroidalPolCharts` [thm] — 5261 décl., 0.89 %
                - `GlobalTheory.T.minimalBlowup_smooth_with_semiAbelianCharts` [thm] — 3384 décl., 0.53 %
                  - `GlobalTheory.SiegJoin.chartSt5_holds` [thm] — 3383 décl., 0.53 %
        - `GlobalTheory.T.hasSemiAbelianUniformisation_complete_normal_base` [thm] — 4965 décl., 0.66 %
          - `GlobalTheory.Mum.has_of_base` [thm] — 4964 décl., 0.66 %
      - `UpperTheory.One.vwin_of_row` [thm] — 92705 décl., 8.21 %
        - `UpperTheory.One.Join.automorphic_window_of_inputs` [thm] — 92702 décl., 8.21 %
          - `UpperTheory.One.Join.v_window_of_depth_zero_residual_bc_cm` [thm] — 91716 décl., 8.13 %
            - `UpperTheory.V.v_window_of_literal_automorphy_n` [thm] — 91656 décl., 8.13 %
              - `UpperTheory.V.HV.DescentVanishingReductions.v_window_of_automorphy_csd_ss_mono_odd` [thm] — 91655 décl., 8.13 %
                - `UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt` [thm] — 80724 décl., 7.38 %
                  - `UpperTheory.V.HV.DescentVanishingReductions.sp4In0_alt` [thm] — 11275 décl., 1.15 %
                  - `UpperTheory.V.Z.Kato.WeilSphericalRecords.katoTwoW_of_printsH` [thm] — 15273 décl., 1.11 %
                    - `UpperTheory.V.Z.Kato.WeilSphericalRecords.katoTwoW_of_printsH_of_rT_of_quadBC2` [thm] — 15272 décl., 1.11 %
                      - `UpperTheory.V.Z.Kato.WeilSphericalRecords.twoS` [thm] — 14545 décl., 1.06 %
                  - `UpperTheory.V.Z.Sym.W.unitary_three_automorphy_dense_of_prints` [thm] — 6622 décl., 0.64 %
                    - `UpperTheory.V.Z.Sym.W.unitary_three_automorphy_dense_of_prints_and_row` [thm] — 6621 décl., 0.64 %
                      - `UpperTheory.V.Z.Sym.W.adjoint_automorphy_w_of_printed_hida_window` [thm] — 5307 décl., 0.55 %
    - `UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter` [thm] — 95102 décl., 6.31 %
      - `UpperTheory.Gal.Int.galoisRepresentations_of_thetaLift` [thm] — 90962 décl., 6.07 %
        - `UpperTheory.Gal.Int.Geo.geoOne_holds` [thm] — 82643 décl., 5.50 %
          - `UpperTheory.Gal.Int.Geo.geometric_realization_of_weight_one` [thm] — 79447 décl., 5.23 %
            - `UpperTheory.Gal.Int.Geo.steps_holds` [thm] — 54486 décl., 3.24 %
              - `UpperTheory.Gal.Int.Geo.jumpStep_holds` [thm] — 6094 décl., 0.52 %
            - `UpperTheory.Gal.Int.Geo.kodaira_spencer_of_weight_one` [thm] — 18918 décl., 1.69 %
        - `UpperTheory.Gal.Int.galoisLocalGlobalStrong_of_geometry_lift` [thm] — 8091 décl., 0.56 %
          - `UpperTheory.Gal.Int.galoisLocalGlobal_of_geometry_lift` [thm] — 8068 décl., 0.56 %

## Épine dorsale (enfant le plus lourd, récursivement)

  0. `riemannHypothesis` [thm] — sous-arbre 1 décl., 0.00 % ; propre 1
