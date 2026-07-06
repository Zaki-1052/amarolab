<!-- analysis/gq_vs_gi_comparison.md -->

# Psilocin-bound 5-HT2A Receptor: G<sub>q</sub> vs G<sub>i</sub> MD Comparison

> 10 ns all-atom MD, CHARMM36m, Ingolfsson brain-PM membrane (16 species, 585 lipids, 46% cholesterol). Side-by-side analysis across 10 phases.
>
> - **Gq** — PDB 9AS8 · 280,277 atoms · 266 receptor residues
> - **Gi** — PDB 9LL8 · 270,555 atoms · 262 receptor residues

---

## Phase 2 — Backbone RMSD

Both trajectories aligned per-frame to frame 0. The receptor backbone is well-equilibrated in both systems, but the G protein tells a strikingly different story.

| Metric | Gq (9AS8) | Gi (9LL8) | Δ |
|---|---|---|---|
| Receptor RMSD range | 0.00–1.69 Å | 0.00–1.58 Å | −0.11 Å |
| Receptor plateau | ~1.3–1.5 Å by 2 ns | ~0.8–1.1 Å by 1 ns | Gi settles faster |
| G protein RMSD range | 0.00–5.30 Å | 0.00–2.96 Å | −2.34 Å |
| G protein behavior | Never plateaus; step-jump at ~6–7 ns | Rises to ~1.3–1.8 Å, stabilizes | |

> **Key difference:** The mini-Gq heterotrimer drifts nearly twice as far as the Gi (5.30 vs 2.96 Å max RMSD) and never equilibrates within 10 ns. The Gi interface appears substantially more conformationally stable at this timescale.

---

## Phase 3 — Per-residue Flexibility (RMSF)

Cα RMSF after in-memory realignment. The Gi-coupled receptor is slightly more flexible overall (**0.75 Å** mean vs **0.65 Å**), but the pattern is region-specific.

| Region | Gq RMSF (Å) | Gi RMSF (Å) | Δ (Å) |
|---|---|---|---|
| TM1 | 0.56 ± 0.16 | 0.66 ± 0.17 | +0.10 |
| ICL1 | 0.65 ± 0.07 | 0.89 ± 0.13 | +0.24 |
| TM2 | 0.45 ± 0.09 | 0.51 ± 0.14 | +0.06 |
| ECL1 | 0.61 ± 0.12 | 0.90 ± 0.16 | +0.29 |
| TM3 | 0.42 ± 0.10 | 0.51 ± 0.15 | +0.09 |
| ICL2 | 1.24 ± 0.44 | 1.01 ± 0.18 | **−0.23** |
| TM4 | 0.60 ± 0.17 | 0.75 ± 0.35 | +0.15 |
| ECL2 | 0.97 ± 0.57 | 1.01 ± 0.31 | +0.04 |
| TM5 | 0.64 ± 0.23 | 0.56 ± 0.15 | **−0.08** |
| ICL3c | 0.81 ± 0.17 | 1.36 ± 0.76 | **+0.55** |
| TM6 | 0.55 ± 0.09 | 0.63 ± 0.14 | +0.08 |
| ECL3 | 1.15 ± 0.34 | 1.20 ± 0.18 | +0.05 |
| TM7 | 0.50 ± 0.10 | 0.56 ± 0.12 | +0.06 |
| H8 | 0.72 ± 0.18 | 1.12 ± 0.36 | **+0.40** |
| Ct | 1.74 ± 0.46 | 2.39 ± 0.23 | +0.65 |

> **Pattern:** Gi coupling loosens the intracellular face — ICL3c (+0.55 Å), H8 (+0.40 Å), ICL1 (+0.24 Å), and ECL1 (+0.29 Å) are all more flexible under Gi. The one region that stiffens is **ICL2** (−0.23 Å), which in the Gq system is the most flexible intracellular loop. TM5 also stiffens slightly under Gi (−0.08 Å).

---

## Phase 4 — Psilocin Binding Pose

The orthosteric pocket and salt bridge to D155 are essentially identical regardless of G protein coupling.

| Metric | Gq | Gi |
|---|---|---|
| Salt bridge (N1···D155) | 2.86 ± 0.12 Å | 2.87 ± 0.14 Å |
| Salt bridge integrity | 100/100 frames (<3.5 Å) | 100/100 frames (<3.5 Å) |
| Ligand RMSD (heavy atoms) | 0.77 ± 0.20 Å | 0.73 ± 0.18 Å |
| Pocket backbone RMSD | 0.67 ± 0.12 Å | 0.72 ± 0.13 Å |
| Pocket residues (5 Å cutoff) | 25 residues, 100 BB atoms | 22 residues, 88 BB atoms |

> The Gi pocket is **3 residues smaller** — L236, F243, and I344 (lit. numbering) fall outside the 5 Å cutoff. These sit at the pocket periphery (TM5/ECL2 and TM6 interfaces), suggesting a subtle narrowing or reorientation of the pocket mouth in the Gi-coupled state, while the core pharmacophoric contacts are unchanged.

---

## Phase 8 — Psilocin–Receptor Hydrogen Bonds

Custom donor/acceptor detection (CGenFF atom-type workaround). All observed H-bonds are sidechain-mediated in both systems; no backbone involvement.

| H-bond | Gq occ. | Gi occ. | Δ |
|---|---|---|---|
| Amine N1–H17 → D155:OD1 | 98% | 93% | −5% |
| Amine N1–H17 → D155:OD2 | 44% | 61% | +17% |
| Indole N2–H13 → S242:OG | 67% | 54% | −13% |
| Indole N2–H13 → T160:OG1 | 19% | 17% | −2% |
| Hydroxyl O ← N343:ND2–HD21 | 3% | 0% | −3% |
| **H-bonds/frame** | **2.3 ± 0.7** (1–4) | **2.2 ± 0.6** (1–3) | −0.1 |

> The Gq system supports **5 unique H-bond types** vs **4 in Gi**. The hydroxyl–ASN343 interaction (3% occupancy) is exclusive to Gq — psilocin's hydroxyl never donates or accepts in the Gi pocket. The amine group redistributes: the primary D155:OD1 contact weakens (−5%) while the secondary OD2 contact strengthens (+17%), suggesting the protonated amine samples both carboxylate oxygens more evenly under Gi. The indole NH–S242 contact drops 13%.

---

## Phases 9 & 10 — Aromatic Cage Dynamics & Rotamers

Ring reorientation (SVD-derived normal vectors) and χ1/χ2 dihedral analysis for the 6 pocket aromatics + psilocin.

| Residue | Gq total rotation | Gi total rotation | Gq χ1 trans. | Gi χ1 trans. | Rotamer |
|---|---|---|---|---|---|
| W336 (toggle) | 1035° | 879° | 0 | 0 | g− |
| F339 | 1274° | 1300° | 0 | 0 | t |
| F340 | 989° | 1033° | 0 | 0 | g− |
| F234 | 2390° | 2596° | 0 | **4** | t |
| F243 | 1046° | 973° | 0 | 0 | t |
| Y370 | 1129° | 1169° | 0 | 0 | g− |
| Psilocin | 1058° | 965° | — | — | — |
| D155 | — | — | 0 | 0 | t |

> **F234 is the critical differentiator.** Both systems show F234 as a mobility outlier (~2× cumulative rotation of any other ring), but only in the Gi system does it undergo **4 discrete χ1 rotamer transitions** (Gq: zero). Its χ1 std is 32.0° in Gi vs 8.2° in Gq, and χ2 std is 111.3° vs 125.3°. This suggests F234 explores multiple rotameric wells under Gi coupling, while remaining locked in one well (but wobbling freely) under Gq. W336 (the toggle switch) stays locked in the activated g− rotamer in both systems.

---

## Phase 6 — Receptor–Lipid Contact Profile

4.0 Å cutoff contact search across 609 lipid molecules (16 species). The lipid annulus around the receptor reshuffles substantially between coupling states.

| Species | Gq total freq | Gi total freq | Gq per-mol | Gi per-mol |
|---|---|---|---|---|
| CHL1 | 73.3 | 65.7 | 0.26 | 0.24 |
| POPE | 36.0 | 0.1 | 2.40 | 0.00 |
| POPC | 9.0 | 57.2 | 0.19 | 1.19 |
| PAPE | 24.5 | 58.2 | 0.68 | 1.62 |
| DOPC | 26.5 | — | 2.95 | — |
| SDPE | 33.1 | 31.7 | 0.61 | 0.59 |
| SDPS | 11.8 | 22.9 | 0.79 | 1.53 |
| PSM | 24.3 | 2.5 | 0.90 | 0.09 |
| GalCer | 24.2 | 9.2 | 1.01 | 0.38 |
| PAPS | 11.3 | 11.4 | 1.26 | 1.26 |
| SAPI | 14.3 | 9.9 | 1.59 | 1.10 |

> **Dramatic lipid annulus rearrangement.** POPE contacts the Gq receptor heavily (36.0 total, 2.40/mol) but essentially never touches Gi (0.1). Conversely, POPC and PAPE are minor players around Gq but become dominant contacts around Gi (57.2 and 58.2 total, respectively). PSM and GalCer (sphingolipids) strongly favor the Gq annulus. Since both simulations use the same membrane composition, this reshuffling reflects how G protein coupling changes the receptor's TM surface geometry and charge distribution, selectively recruiting different lipid species.

### Cholesterol contacts

| | Gq | Gi |
|---|---|---|
| Persistent CHL1 contacts (≥0.9) | 54 | 44 |
| Residues at freq = 1.00 | 28 | 21 |
| Clusters | TM1, ECL1/TM3, TM4–TM5, TM6–TM7 | Less dense TM4–TM5 cluster |

---

## Cross-phase — CRAC/CARC Cholesterol Recognition Motifs

Sequence-predicted motifs cross-referenced against simulation CHL1 contact frequencies. Same 7 motifs detected in both systems; different ones are functionally active.

| Motif | Type | Region | Gq central Y/F CHL1 | Gi central Y/F CHL1 | Status |
|---|---|---|---|---|---|
| L136–Y137–R140 | CRAC | TM2 | 0.24 | 0.99 | Gi active |
| L136–Y139–R140 | CRAC | ECL1 | 0.00 | 0.89 | Gi active |
| V251–Y254–K259 | CRAC | TM5 | 0.99 | 0.01 | Gq active |
| R173–Y174–V175 | CARC | TM3 | 1.00 | 1.00 | Both active |
| K191–F193–L194 | CARC | TM4 | 0.00 | 1.00 | Gi active |

> The TM3 CARC motif (R173–Y174–V175) is a constitutive cholesterol site in both coupling states. However, **Gq uniquely activates the TM5 CRAC** (V251–Y254, freq 0.99 vs 0.01), while **Gi uniquely activates the TM2/ECL1 CRAC and TM4 CARC**. The coupling state effectively relocates the cholesterol recognition surface — Gq binds cholesterol on TM5 while Gi binds it on TM2/TM4.

---

## Phase 5 — Lipid Acyl-chain Order Parameters

|S<sub>CD</sub>| values are essentially identical between the two systems, confirming that the membrane bulk properties are unperturbed by the choice of G protein.

| Chain | Gq mean |S_CD| | Gi mean |S_CD| |
|---|---|---|
| POPC sn-1 (16:0) | 0.241 | 0.235 |
| POPC sn-2 (18:1) | 0.182 | 0.185 |
| POPE sn-1 (16:0) | 0.254 | 0.247 |
| POPE sn-2 (18:1) | 0.189 | 0.185 |
| SDPE sn-1 (18:0) | 0.224 | 0.224 |
| SDPE sn-2 (DHA 22:6) | 0.056 | 0.055 |

All values within <0.01 of each other. The DHA (22:6) sn-2 chain in SDPE is radically disordered in both (|S_CD| ~0.055), as expected for 6 *cis* double bonds.

---

## Cross-phase — RMSF vs Lipid Contact Correlation

| Correlation | Gq ρ | Gi ρ |
|---|---|---|
| All residues vs total contacts | 0.030 (p=0.63) | 0.003 (p=0.96) |
| Contacting residues only | −0.171 (p=0.018) | −0.253 (p=4×10⁻⁴) |
| RMSF vs CHL1 only | −0.015 (p=0.81) | 0.006 (p=0.93) |

Both systems show no global RMSF–lipid contact relationship, but a significant weak negative correlation among lipid-contacting residues — stronger in Gi (ρ=−0.253 vs −0.171). This suggests the Gi lipid annulus exerts slightly more stabilizing influence on the residues it contacts.

---

## Synthesis: What G protein coupling changes

- **G protein interface stability.** Gi sits far more stably on the receptor (max RMSD 2.96 vs 5.30 Å). The mini-Gq never equilibrates over 10 ns, suggesting either a weaker interface or ongoing conformational search.

- **Intracellular flexibility redistribution.** Gi loosens ICL3c, H8, and ICL1/ECL1 while stiffening ICL2. Gq does the opposite — ICL2 is the most mobile intracellular loop. This mirrors the known structural basis: ICL2 and ICL3 are the primary G protein contact points, and their relative mobility likely reflects differences in how the two Gα subunits engage the receptor intracellular face.

- **Orthosteric pocket is invariant.** The psilocin salt bridge, ligand RMSD, and total H-bonds/frame are indistinguishable. G protein coupling does not propagate structurally to the ligand pose at this timescale.

- **Subtle H-bond redistribution.** The amine–D155 interaction redistributes between the two carboxylate oxygens (OD1 vs OD2), and the indole NH–S242 contact weakens by 13% under Gi. The hydroxyl–N343 contact (3%) exists only in Gq.

- **F234 rotameric switching is Gi-specific.** This pocket aromatic undergoes 4 χ1 transitions only in Gi, despite comparable ring mobility in both. F234 sits adjacent to D155 and could serve as a dynamic relay between the binding pocket and TM5/TM6 region.

- **Lipid annulus reshuffles by coupling state.** PE/sphingolipid-enriched in Gq, PC/PE-plasmalogen-enriched in Gi. The 16-species composition is identical, so this reflects receptor surface changes selectively recruiting different lipid headgroups.

- **Cholesterol recognition sites relocate.** The TM3 CARC is constitutive; Gq adds TM5 CRAC, Gi adds TM2/TM4 CRAC/CARC. The cholesterol binding footprint rotates around the receptor helix bundle.

- **Membrane bulk properties are unchanged.** Lipid order parameters are identical within noise, confirming the differences are local to the receptor–lipid interface.

---

*Both systems: 10 ns production, CHARMM36m, 310.15 K, OpenMM/Metal GPU (Apple M4), 100 frames @ 100 ps. Ingolfsson brain PM membrane: 585 lipids, 16 species, 46% cholesterol. Receptor: psilocin-bound 5-HT2A with ICL3 unresolved. Gq system uses 3-segment receptor (PROA/PROB/PROC, offset +78/+127); Gi uses 2-segment (PROE/PROF, offset +79/+131).*
