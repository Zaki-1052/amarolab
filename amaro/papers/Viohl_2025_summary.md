# Viohl et al. (2025) — Molecular insights into the modulation of the 5HT2A receptor by serotonin, psilocin, and the G protein subunit Gqα

**Citation:** Viohl, N., Hakami Zanjani, A. A., & Khandelia, H. (2025). Molecular insights into the modulation of the 5HT2A receptor by serotonin, psilocin, and the G protein subunit Gqα. *FEBS Letters, 599*(6), 876–891. https://doi.org/10.1002/1873-3468.15099

---

## One-Sentence Takeaway

Using all-atom molecular dynamics simulations and free-energy calculations, this paper shows that serotonin and psilocin both preferentially bind the deeper orthosteric pocket of 5-HT2A receptor, that the receptor's active "open" conformation collapses without a bound G protein, and that an intermediate "partially-open" state exists along the activation pathway.

---

## Background & Motivation

The 5-HT2A receptor (5HT2AR) is a G protein-coupled receptor (GPCR) — the largest family of cell-surface drug targets in humans. It sits in the postsynaptic membrane of neurons and is the primary molecular target for psychedelic drugs like psilocybin (the prodrug form of psilocin), LSD, and mescaline. When activated, it couples to the heterotrimeric Gq protein, initiating downstream signaling cascades that alter gene expression and synaptic plasticity. A second pathway involves β-arrestin recruitment, leading to distinct functional outcomes. Both pathways are thought to contribute to the antidepressant and hallucinogenic effects of psychedelics, though the relative contributions are still debated.

Understanding exactly *how* ligands like serotonin and psilocin bind to and activate this receptor is critical for designing better psychiatric drugs — ones that might retain therapeutic benefit while minimizing side effects like hallucinations. The problem is that most structural studies capture the receptor frozen in single snapshots (either inactive "closed" or fully active "open" states), while the receptor's *dynamics* — how it moves between those states and what drives those transitions — remain poorly understood. Computational MD simulations are ideally suited to fill this gap because they can capture atomic-level motions occurring on timescales of nanoseconds to microseconds that are invisible to crystallography or cryo-EM.

The binding pocket of 5HT2AR has two adjacent subpockets: the **orthosteric binding pocket (OBP)**, which is the deeper, more evolutionarily conserved site, and the **extended binding pocket (EBP)**, which sits slightly above it toward the extracellular side. Crystal structures of the receptor in complex with serotonin and psilocin suggested that both ligands' indole ring cores occupy the EBP, while other computational studies placed the indole cores in the OBP. This discrepancy needed resolving. Additionally, there is a less-explored **side-extended pocket (SEP)** specific to the 5-HT2 receptor subfamily. The authors set out to clarify: (1) which pocket is the preferred binding site, (2) how does the receptor's conformational state depend on Gq protein presence, and (3) what intermediate states exist along the activation pathway?

---

## Approach & Methods

The team used **all-atom molecular dynamics (MD) simulations** with the CHARMM36m force field, run in GROMACS 2023.3. This force field is specifically optimized for membrane proteins and intrinsically disordered regions, making it well-suited for a flexible receptor in a lipid bilayer. Their simulation systems consisted of 5HT2AR embedded in a heterogeneous lipid bilayer membrane designed to approximate a real postsynaptic neural membrane — containing POPC, PSPC, PAPC, SDPC, SSM, cholesterol, and POPS in realistic proportions derived from neuronal lipid composition data.

**System construction** used CHARMM-GUI Membrane Builder and PyMOL (Schrödinger). The protein models came from the Protein Data Bank: the active state structure (PDB: 7RAN/6WHA), the inactive state (PDB: 6A93), and the Gqα subunit (AlphaFold, PDB: 7W40). Missing intracellular and extracellular loops were modeled as disordered loops using MODELLER. Both protonation states of the key anchor residue D155^3.32 and both ligands (serotonin and psilocin) were considered, and previous simulations established that protonated ligands paired with deprotonated D155^3.32 is the most stable configuration — so all simulations used this pairing.

The team ran two categories of MD:

- **Conventional MD simulations:** Systems without Gqα were run for 2 μs total (three replicas with different initial velocity distributions), while systems with Gqα ran for 1 μs. These explored how the receptor naturally samples its conformational landscape.

- **Potential of Mean Force (PMF) / umbrella sampling simulations:** These are enhanced sampling techniques used to calculate binding free energies. To simulate ligand binding, the researchers used steered molecular dynamics (SMD) to pull ligands from their binding sites out through the extracellular vestibule and into bulk water, creating a series of ~40 "windows" spaced ~0.1 nm apart along the unbinding pathway. Each window was independently equilibrated and sampled to build up a free energy profile. The same approach was used to calculate Gqα binding affinity by pulling the C-terminal α5-helix of Gqα away from the intracellular binding cavity. Free energy profiles were extracted using the Weighted Histogram Analysis Method (WHAM) with Bayesian bootstrap error estimation.

**Analysis tools** included RMSD, RMSF, intramolecular distance tracking (particularly between Cα atoms of R173^3.50/E318^6.30 and Q262^5.66/E318^6.30 — two pairs that mark opening of the intracellular G-protein binding cavity), the **A100 activation index** (a multi-distance metric for class A GPCRs that combines distances across six structural motifs), and **Principal Component Analysis (PCA)** of backbone Cα atoms in the transmembrane (TM) core to identify dominant conformational states. k-means clustering was used on the PCA projections to identify representative receptor conformations, which were then compared to experimental reference structures.

---

## Key Findings

### Finding 1: The "Open" Active State Collapses Without Gqα

When the team started simulations from the experimentally determined active "open" state (outward-tilted TM5 and TM6, open intracellular G-protein cavity) but without any Gqα present, the receptor rapidly collapsed toward the inactive "closed" configuration. This happened in two of three simulation replicas within just 250 ns of production run. Only a single replica maintained the "open" conformation for the full 1 μs. When Gqα was present in the intracellular cavity, however, the open TM5/TM6 geometry was preserved in all replicas in good agreement with experimental references.

This is a conceptually important finding: it means the active conformation of 5HT2AR is not a stable free-energy minimum on its own — it requires a transducer (the G protein) to be thermodynamically stable. Ligand binding alone (serotonin or psilocin) does not prevent this collapse. The receptor is intrinsically unstable in the fully active conformation without its downstream coupling partner.

The A100 activation index analysis adds nuance here: while the intramolecular distances (TM5/TM6 tilts) show the receptor collapsing to "closed," the A100 score for the "open" simulations shows the receptor remaining in an intermediate state rather than fully reverting to inactive. This discrepancy across analysis methods underscores the importance of using multiple metrics when describing GPCR activation — a single measurement doesn't capture the full conformational picture.

### Finding 2: A "Partially-Open" Intermediate State Exists

PCA of the TM1-7/H8 backbone revealed that in approximately 55% of simulation ensembles, the receptor adopts a **"partially-open"** conformation with a less extensive outward tilt of TM6 — approximately 4 Å instead of the ~8 Å seen in fully G protein-bound experimental structures. This intermediate appears in both ligand-bound and ligand-free systems in the absence of Gqα.

Key molecular signatures of the partially-open state:
- The toggle switch residue W336^6.48 rotates, indicating early-stage activation
- Rearrangements in F332^6.44 in the PIF motif (a conserved activation microswitch) occur
- The ionic lock between R173^3.50 and E318^6.30 is loosened but not fully broken
- The NPXXY motif inward shift (another activation hallmark) is not observed

The partially-open state corresponds well to the known intermediate **R'' state** in the multi-step GPCR activation model: after agonist binding relaxes the low-affinity ground state (R → R'), the receptor partially exposes the intracellular binding cavity (R'' state), before Gqα binding completes the opening (R* and R*G states). The authors suggest the partially-open state is a pre-coupling intermediate that allows initial low-affinity alignment of Gqα before the high-affinity, fully-open engagement occurs.

### Finding 3: The Active State Has ~3x Higher Gqα Affinity Than the Closed State

PMF calculations comparing Gqα C-terminal α5-helix binding to the open versus closed intracellular cavities revealed a striking difference:
- Active "open" state: binding free energy ≈ **−16.51 ± 0.52 kcal/mol**
- Inactive "closed" state: binding free energy ≈ **−5.69 ± 0.5 kcal/mol**

This ~11 kcal/mol difference represents a roughly 3-order-of-magnitude difference in binding affinity at physiological temperature. Notably, even the closed state retains a meaningful Gqα affinity (~−10.8 kcal/mol estimated for initial low-affinity contact), which the authors propose serves an alignment/priming function — the initial Gqα contact stabilizes the receptor and facilitates the subsequent conformational opening that creates the high-affinity fully-open state.

### Finding 4: Serotonin and Psilocin Prefer the Orthosteric Binding Pocket (OBP) Over the EBP

PMF calculations for ligand binding to both the OBP and EBP produced the following binding free energies (Table 1):

| System             | ΔG_OBP (kcal/mol) | ΔG_EBP (kcal/mol) | ΔΔG_EBP-OBP |
| ------------------ | ----------------- | ----------------- | ----------- |
| Serotonin / open   | −12.19 ± 0.74     | −7.05 ± 0.64      | +5.14       |
| Serotonin / closed | −12.21 ± 0.74     | −5.58 ± 0.35      | +6.63       |
| Psilocin / open    | −11.91 ± 0.64     | −7.82 ± 0.67      | +4.09       |
| Psilocin / closed  | −13.12 ± 0.95     | −6.46 ± 0.38      | +6.66       |

Both ligands bind the OBP ~4-6 kcal/mol more favorably than the EBP, regardless of whether the receptor is in the active or inactive conformation. This OBP preference was also supported by conventional MD: ligands in the OBP remained stably bound throughout all simulations, while EBP-placed ligands escaped in 5 of 12 simulations.

A critical detail: the probability of OBP occupancy over EBP occupancy (calculated using a Boltzmann factor from the free energy difference) is **3 orders of magnitude higher** in the open state and **4 orders of magnitude higher** in the closed state. This strongly resolves the earlier debate: the OBP, not the EBP, is the primary binding location for both serotonin and psilocin.

The authors also note that in crystal structures of 5HT2AR, the EBP and SEP are occupied by a small monoolein lipid. This suggests that lipids like monoolein, oleamide, or 2-oleoyl glycerol are not merely passive membrane components — they may actively modulate 5HT2AR activity by competing with ligands at the EBP, and overcoming this competition could be necessary for effective EBP-mediated signaling.

---

## Significance & Implications

This paper is directly relevant to BioChemCore because you are running MD simulations of 5HT2AR specifically — this is a paper about exactly the methodology you are using (CHARMM36m force field, membrane bilayer construction, GROMACS) applied to exactly your protein of interest.

Several findings matter for how you think about your own simulations:

**Conformational instability without Gqα.** If your production simulation starts from the active state PDB structure (7RAN) without a bound Gq protein, you should expect the receptor to drift toward the closed state relatively quickly. This is not a simulation failure — it reflects real physics. The "open" state requires transducer stabilization. If you see RMSD increasing and TM5/TM6 collapsing inward, that is the partially-open or closed state being sampled, which is actually physically meaningful.

**Lipid environment matters.** The lipid composition Viohl et al. used (30% POPC, 12% PSPC, 9% PAPC, 9% SDPC, 10% SSM, 30% cholesterol in the outer leaflet; slightly different proportions in the inner leaflet) approximates real postsynaptic membrane composition, drawing on the same lipid references you will encounter in your BioChemCore reading. The choice of lipid bilayer composition affects protein-lipid contacts, membrane fluidity, and potentially receptor dynamics — it is worth noting how the CHARMM-GUI setup handles this when you construct your own system.

**The PIF motif and ionic lock as conformational sensors.** The authors tracked W336^6.48 rotation and the R173^3.50 / E318^6.30 ionic lock as diagnostic markers of activation state. In your own RMSD/contact analysis, monitoring these distances can give you more interpretable information about activation state than backbone RMSD alone.

More broadly, this work illustrates how computational methods like umbrella sampling and PMF calculations are capable of generating thermodynamic data (binding free energies) that directly complement and extend what structural biology alone can tell us. The ~5 kcal/mol preference for the OBP over the EBP would be essentially impossible to determine from a single crystal structure — it required MD to reveal.

From a drug discovery perspective, the finding that both serotonin and psilocin favor the OBP over the EBP, combined with the knowledge that some lipid molecules occupy the EBP, suggests that EBP-targeting ligands might require overcoming lipid competition — a design challenge for next-generation psychedelic-derived therapeutics.

---

## Limitations & Open Questions

**Only the Gqα C-terminal helix was modeled, not the full Gβγ complex.** The N-terminus of Gqα was omitted because it is highly flexible and protrudes from the binding cavity. This simplification saves computational cost but means Gβγ-mediated allosteric effects on receptor dynamics and ligand affinity are not captured. The paper appropriately flags this as a limitation and calls for future work with complete G-protein models.

**Simulation timescale is still short relative to biological processes.** The longest simulations run for 2 μs total across three replicas. Conformational transitions in GPCRs can take milliseconds or longer in vivo. The collapse of the open state seen here within hundreds of nanoseconds may reflect an artificially fast transition — or it may genuinely reflect sub-microsecond dynamics. The authors are careful not to overclaim here, noting that the true timescale of the open-to-closed collapse in the absence of G-protein is unknown.

**Functional selectivity (biased agonism) is not addressed.** Serotonin and psilocin both activate Gq signaling and β-arrestin recruitment, but with different bias profiles. The paper focuses purely on Gq coupling via the α5-helix, so it does not address how ligand-specific conformational differences in the intracellular cavity might differentially recruit β-arrestin. This is a significant open question for the psychedelic pharmacology field.

**The "partially-open" intermediate is identified but not deeply characterized.** While the authors identify this state and align it with the R'' intermediate in GPCR activation theory, the specific residue-level interactions that stabilize it are not worked out in detail. Future cryo-EM trapping experiments or more extensive enhanced sampling MD could map this state more precisely.

**No explicit testing of hallucinogenic vs. non-hallucinogenic compounds.** The field has a major interest in whether structural analogs of psilocin can be designed that preserve antidepressant efficacy without hallucinogenicity. This paper lays groundwork but does not directly compare psilocin to biased agonists — that comparison appears in related papers in Zara's reading list (e.g., Tuck 2025, Cameron 2021).

---

## Key Terms & Concepts

**Orthosteric Binding Pocket (OBP):** The primary, deeper ligand binding site within 5HT2AR, highly conserved across the 5-HT receptor family. Ligands anchored here interact with the conserved D155^3.32 residue via their basic amine group and coordinate their aromatic core through hydrophobic and hydrogen-bonding interactions. This paper shows it is the thermodynamically preferred binding site for both serotonin and psilocin.

**Extended Binding Pocket (EBP):** A secondary binding subpocket located slightly above (extracellular to) the OBP, accessible from the extracellular vestibule. The EBP is closed by a lid formed by extracellular loop 2 (ECL2). Crystal structures placed psilocin's indole core here, but MD free energy calculations show EBP binding is ~4-6 kcal/mol weaker than OBP binding.

**Potential of Mean Force (PMF) / Umbrella Sampling:** A computational free energy method that calculates the thermodynamic work required to move a molecule along a chosen reaction coordinate (e.g., pulling a ligand out of its binding pocket). It involves running many short simulations at closely spaced points along the pathway and then reconstructing the continuous free energy profile using WHAM. The result is a binding free energy in kcal/mol that can be compared between different conditions or binding sites.

**Toggle Switch (W336^6.48):** A conserved tryptophan residue in TM6 that rotates upon GPCR activation, acting as a molecular gate. Its rotation is one of the earliest indicators of activation-associated conformational change and propagates to rearrangements in the PIF motif.

**Ionic Lock (R173^3.50 – E318^6.30):** A salt bridge between arginine on TM3 and glutamate on TM6 that stabilizes the inactive conformation of class A GPCRs. Breaking this interaction is a hallmark of activation; here it is loosened (but not fully broken) in the partially-open intermediate state.

**PIF Motif:** A conserved hydrophobic cluster (P246^5.50, I163^3.40, F332^6.44) that acts as a transmission switch in class A GPCRs. Rearrangement of F332^6.44 follows the W336^6.48 toggle switch rotation and propagates the activation signal from the ligand-binding pocket toward the intracellular G-protein coupling region.

**A100 Activation Index:** A scalar metric developed to classify class A GPCR conformations from MD trajectories into inactive, intermediate, or active states. It computes a weighted combination of six intramolecular Cα distances that collectively reflect the activation state of conserved structural motifs.

---

## Connection to BioChemCore Curriculum

This paper is an ideal companion piece to your BioChemCore simulations. The methodology here (CHARMM-GUI membrane builder, CHARMM36m force field, GROMACS, VMD visualization) is exactly what you are using. Specific connections:

- **Day 4 (CHARMM-GUI membrane setup):** The lipid bilayer composition used by Viohl et al. is a direct model for building a neurobiologically realistic membrane around 5HT2AR. Note that they used asymmetric leaflet compositions derived from postsynaptic membrane lipidomics data (same references as Calderon 1995 and Lim 2009 in your reading list).
- **Day 5 (Minimization & Equilibration):** Their equilibration protocol (250 ps NVT, 1625 ps NPT with gradually released position restraints) is a standard approach and gives you a concrete reference for what equilibration looks like for this receptor.
- **Day 7 (Analysis):** The RMSD, RMSF, and intramolecular distance analyses they describe are exactly the metrics you will compute. Tracking the R173-E318 and Q262-E318 distances is a more mechanistically meaningful approach than RMSD alone.
- **Biology context:** The paper's introduction and discussion give you the clearest available picture of *why* 5HT2AR activation dynamics matter for psychedelic pharmacology — important for the "biology first" principle of BioChemCore.
