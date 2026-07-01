# 5-HT2AR / psilocin / mini-Gq: trajectory analysis summary

10 ns all-atom MD of the psilocin-bound 5-HT2A serotonin receptor with a mini-Gq heterotrimer, embedded in a realistic neuronal membrane (Ingolfsson Brain PM composition, 585 lipids, 46% cholesterol). 280,277 atoms, 100 frames at 100 ps intervals, CHARMM36m force field, 310.15 K, run on Apple M4 via OpenMM with the Metal GPU backend.

The short version: everything worked. The receptor is stable, psilocin never moves, the membrane behaves like a real neuronal bilayer, and cholesterol packs into the expected TM grooves. The G protein is the one component still relaxing at the end of 10 ns. Below is what each analysis found.

---

## The receptor is structurally stable

Receptor backbone RMSD plateaus at 1.3-1.5 Å by about 2 ns and stays flat for the remaining 8. That's low even for a membrane protein. The bilayer is doing its job clamping the TM bundle.

The G protein is a different story. Its RMSD climbs to 5.3 Å with no plateau, including a step around 6-7 ns where it jumps from ~3.5 to ~4.5 Å. The heterotrimer (~10,200 atoms, 3 subunits) hangs below the membrane tethered only at the receptor interface, so it has room to rearrange. The mini-Gaq construct is also chimeric (engineered), which may mean it doesn't have one deep energy minimum. 10 ns wasn't enough time for it to settle. Any G protein observations from this trajectory describe relaxation, not equilibrium.

The simulation box itself was still equilibrating too: XY shrank ~1.5% and Z grew ~3.3% over the 10 ns production. But this didn't contaminate the receptor RMSD. If it had, the receptor curve would drift along with the box. It doesn't.

## Flexibility matches the classic GPCR pattern

RMSF across the 266 receptor residues ranges from 0.33 to 2.71 Å (mean 0.65 Å). The pattern is exactly what you'd expect for a 7-TM receptor: rigid helices constrained by lipid and helix-helix packing, with flexibility peaks at loops and termini.

**Rigid regions.** TM3 is the most rigid helix (mean 0.42 Å), followed by TM2 (0.45 Å). These sit at the innermost core of the bundle, packed against the most neighbors. D77, the psilocin salt bridge anchor (D155 in literature numbering), has RMSF 0.37 Å, putting it among the 15 most rigid residues in the entire receptor.

**Flexible regions.** The ECL2 tip (resids 145-147, up to 2.71 Å) is the most flexible part of the receptor. But three residues downstream at C149 (the disulfide cysteine C227), RMSF drops 5-fold to 0.55 Å. The conserved TM3-ECL2 disulfide is acting as a structural hinge: everything above it flaps, everything at and below it is locked to TM3.

The ICL2 peak at the PROA/PROB segment boundary (resid 109, 2.26 Å) is partially a real flexibility signal and partially inflated by the ACE/CT2 capping at the artificial chain break. TM5's C-terminal end (resids 184-185) frays toward the missing ICL3 gap with similar capping artifacts.

## Psilocin is locked in the binding pocket

The salt bridge between psilocin's protonated nitrogen (N1) and the D77 carboxylate is intact in all 100 frames. Range 2.61-3.23 Å, mean 2.86 Å. It never approaches the 3.5 Å weakened threshold. The carboxylate rotates freely (OD1 and OD2 swap which is closer frame to frame), but the min distance stays flat at ~2.9 Å.

Ligand RMSD (heavy atoms, aligned to the binding pocket backbone) averages 0.77 Å with a max of 1.33 Å. Sub-angstrom. The cryo-EM binding pose is essentially unchanged after 10 ns. Slight variability in the 3-7 ns range comes from the ethylamine tail exploring rotamers while the rigid indole ring stays locked in place.

The binding pocket contains 25 residues from 6 of the 7 TM helices. Six aromatic residues (W336, F339, F340, F234, F243, Y370, all in literature numbering) form a cage around the indole ring through pi-stacking and hydrophobic contacts. Combined with the electrostatic salt bridge, the ligand is overdetermined. Unbinding events for agonists at this affinity require microseconds to milliseconds.

## The membrane is healthy

Order parameter profiles for 3 lipid species (POPC, POPE, SDPE) across 6 acyl chains all show the expected shapes.

Saturated chains (POPC and POPE palmitoyl, SDPE stearoyl) have the classic profile: rise from C2, plateau at C5-C8 (0.30-0.33), smooth decline to terminal CH3. The plateau values are elevated above what you'd see in a pure POPC bilayer (~0.20-0.22) because 46% cholesterol condenses the lipid packing, forcing more ordered (all-trans) chain conformations. This cholesterol condensing effect is one of the defining features of neuronal membranes, and it shows up cleanly.

The POPC oleoyl chain (sn-2) reproduces two known structural signatures: the double bond dip at C9=C10 (drops to 0.06) and the sn-2 C2 anomaly (|S_CD| starts at 0.13 instead of the sn-1's 0.25, because the sn-2 chain bends toward the membrane surface before turning downward).

SDPE's DHA chain (22:6, 6 cis double bonds) is radically different from the saturated chains: mean |S_CD| of just 0.056 with an irregular sawtooth profile. This is the correct behavior for a highly unsaturated chain. The hydrogen-per-carbon pattern [2,2,1,1,2,1,1,2,1,1,2,1,1,2,1,1,2,1,1,2,3] was auto-discovered from the PSF bonding topology, confirming all 6 double bond positions. DHA's disorder is what keeps neuronal membranes fluid despite the high cholesterol content.

Upper and lower leaflets broadly agree, with the lower leaflet ~0.03-0.07 more ordered for POPC sn-1 (reflecting compositional asymmetry and small sample sizes: 30 upper vs 18 lower POPC). lipyphilic cross-validation on POPC confirmed chain ordering is internally consistent (saturated > unsaturated in both methods).

## Cholesterol fills the canonical TM grooves

115 of 266 receptor residues contact cholesterol at least once. 54 are persistent (frequency >= 0.9), and 28 contact cholesterol in every single frame. These map to 4 clusters that correspond to known GPCR cholesterol binding grooves:

1. **TM1 outer face** (lit 79-89): LEU79-80, ILE85-86-89.
2. **ECL1/TM3 junction** (lit 125-147): PHE125, PRO129, VAL130, PRO142, PRO144, LEU147. Proline's rigid ring creates grooves that cholesterol's flat sterol ring fits into.
3. **TM4-TM5 groove** (lit 201-258): the densest cluster. GLY205, ILE206, MET208, PRO209, VAL212, PHE213, LEU215, PHE234, ILE237, PHE240, VAL241, ILE249, ILE252, PHE255, ILE258 are all at 100%.
4. **TM6-TM7 groove** (lit 327-382): ILE327, PHE329-330, VAL334, VAL364, PHE365, ILE368, LEU371, VAL375, LEU378, LEU382, PHE383.

The TM4-TM5 groove is notably aromatic-rich (PHE234, PHE240, PHE255), consistent with CH-pi interactions between cholesterol's methyl groups and phenylalanine rings.

### Per-molecule normalization flips the species ranking

Cholesterol dominates raw contact totals (73.3) because 279 molecules is a lot. But most of those cholesterols are far from the receptor. Per-molecule, DOPC leads at 2.95 contacts per lipid, POPE at 2.40. Their few molecules (9 and 15 respectively) are almost all positioned next to the receptor. SAPI at 1.59 per molecule reflects electrostatic attraction between the anionic inositol headgroup and basic residues (Lys, Arg) on the intracellular face.

Four species essentially never contact the receptor in this trajectory: POPS (0.06/mol), SDPC (0.06), SSM (0.04), POPI (0.02). Placement coincidence, not biology, since lipid exchange takes hundreds of nanoseconds.

### Leaflet asymmetry is maintained

Outer-leaflet species (PSM, GalCer) contact the extracellular half of TM helices. Inner-leaflet species (PAPS, SDPS, SAPI) contact the intracellular half and H8. This confirms the Ingolfsson Brain PM composition we built in CHARMM-GUI produced a physically correct asymmetric bilayer that held through production.

## Cross-phase findings

### Two CRAC/CARC cholesterol recognition motifs are active

Scanning the receptor sequence for CRAC ((L/V)-X1-5-(Y)-X1-5-(K/R)) and CARC ((K/R)-X1-5-(Y/F)-X1-5-(L/V)) motifs, then cross-referencing with the simulation's cholesterol contact data, identifies 7 motifs total. Two are cholesterol-active:

**CRAC on TM5: V251-I-T-Y254-F-L-T-I-K259.** Y254 contacts cholesterol at 0.99, V251 at 0.59. Sits in the TM4-TM5 groove (Cluster 3). The lysine's role in CRAC is to interact with the polar headgroup region at the lipid-water interface, not the sterol ring, which is why K259's lower contact frequency (0.17) doesn't disqualify it.

**CARC on TM3: R173-Y174-V175.** Minimal motif (3 consecutive residues). Y174 contacts cholesterol at 1.00, V175 at 0.71. R173 faces inward toward the helix bundle (CHL1 = 0.00). Near Cluster 2 (ECL1/TM3 junction).

The other 5 motifs are inactive. L136-Y137/Y139-R140 on TM2 faces inward. The two H8 motifs have their L/V anchors contacting cholesterol but the central Y faces the cytoplasm, consistent with H8's parallel orientation along the bilayer surface. Sequence prediction and simulation converge on TM3 and TM5 as CRAC/CARC sites.

### RMSF and lipid contacts are geometrically independent

Spearman correlation between per-residue RMSF and total lipid contact frequency: rho = 0.03, p = 0.63. No relationship.

The scatter plot shows an L-shaped distribution with 3 clusters that map directly to the 7-TM architecture:

- **Bottom-right (TM outward faces):** rigid and lipid-exposed. High contacts, low RMSF.
- **Upper-left (loops):** flexible and solvent-facing. Low contacts, high RMSF.
- **Bottom-left (TM inward faces):** rigid from helix packing, but buried away from lipids. Low contacts, low RMSF.

Rigidity and lipid contact are each determined by geometry (helix secondary structure and outward-facing orientation, respectively), not by each other. Among contacting residues only, there's a weak negative correlation (rho = -0.17, p = 0.018) hinting that more lipid packing means slightly more constraint, consistent with cholesterol's ordering effect on adjacent protein structure. But the signal is too weak to claim confidently from 10 ns.

---

## What 10 ns can and can't tell us

**Can assess from this trajectory:**

- Structural stability of the receptor (yes, it's stable)
- Per-residue flexibility profile (classic GPCR pattern confirmed)
- Ligand retention and salt bridge integrity (100% intact, pose unchanged)
- Bilayer integrity and ordering (healthy by all metrics)
- Which lipids are near the receptor during this trajectory window
- Whether the CHARMM-GUI build produced a correct asymmetric membrane (it did)

**Cannot assess:**

- Rare conformational transitions (TM6 outward swing for activation takes microseconds)
- Lipid exchange kinetics (which lipids bind preferentially requires sampling many on/off events)
- G protein dissociation or conformational dynamics (still relaxing at 10 ns)
- Long-range allostery or correlated motions between distant sites
- Thermodynamic convergence (free energy estimates need much more sampling)

The G protein caveat is worth emphasizing. The receptor RMSD converged; the G protein RMSD did not. Any analysis of the G protein from this trajectory describes its behavior during the first 10 ns of relaxation from the cryo-EM starting pose, not its equilibrium dynamics.

---

## Exported snapshots

Representative frame: frame 62 (6.2 ns), chosen as the frame closest to the mean receptor RMSD (1.328 vs 1.324 Å mean).

| File | Contents | Atoms |
|---|---|---|
| `5ht2ar_membrane_snapshot.pdb` | Receptor + psilocin + 609 lipids | 65,199 |
| `5ht2ar_receptor_snapshot.pdb` | Receptor only (PROA/PROB/PROC) | 4,327 |
| `5ht2ar_receptor_psilocin.pdb` | Receptor + psilocin | 4,359 |

The membrane snapshot is ready for Day 8 MegaMembrane assembly. No water, ions, or G protein included.

---

## Analysis scripts and output files

| Phase | Script | Key outputs |
|---|---|---|
| 1. Visual | (VMD) | `phase1_visual/side_frame0.tga`, `psilocin.tga` |
| 2. RMSD | `phase2_rmsd/` | `rmsd_time_series.png`, `rmsd_data.csv` |
| 3. RMSF | `phase3_rmsf/` | `rmsf_profile.png`, `rmsf_data.csv`, `receptor_rmsf_bfactor.pdb` |
| 4. Psilocin | `phase4_psilocin/` | `binding_pose.png`, `psilocin_data.csv` |
| 5. Order params | `phase5_lipid_order/` | `scd_POPC/POPE/SDPE.png`, `scd_data.csv` |
| 6. Contacts | `phase6_contacts/` | `contacts_by_species.png`, `contact_data.csv`, `cholesterol_contacts.png` |
| 6x. Cross-phase | `p_crossphase.py` | `rmsf_vs_contacts.png` |
| 7. Summary | `phase7_summary/` | this file, 3 snapshot PDBs |

All analysis scripts are in `charmm-gui-8190629385/analysis/`. CSVs contain per-residue data with both current and literature numbering. The B-factor PDB (`receptor_rmsf_bfactor.pdb`) can be loaded in PyMOL and colored with `spectrum b, blue_white_red` to see flexibility painted on the 3D structure.

### Numbering reminder

PROA and PROB residues (current 1-185): add 78 for literature numbering.
PROC residues (current 186-266): add 127 for literature numbering. The extra 49 comes from the skipped ICL3.
