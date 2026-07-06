# Peeters et al. 2025 — Molecular Dynamics Study of Differential Effects of Serotonin-2A-Receptor (5-HT2AR) Modulators

**Full citation:** Peeters J, De Bundel D, Vanommeslaeghe K (2025). Molecular dynamics study of differential effects of serotonin-2A-receptor (5-HT2AR) modulators. *PLoS Comput Biol* 21(9): e1013000. https://doi.org/10.1371/journal.pcbi.1013000

---

## 1. One-Sentence Takeaway

By running atomistic molecular dynamics simulations of the 5-HT2A serotonin receptor bound to seven structurally and pharmacologically distinct ligands — with and without an intracellular G protein mimic — this study shows that hallucinogens drive the receptor into an excessively activated conformational state, while sufficiently weak partial agonists produce the milder activation profile associated with antidepressant effects without psychedelic side effects.

---

## 2. Background & Motivation

The serotonin-2A receptor (5-HT2AR) sits at the intersection of two major clinical problems: the treatment of depression and the risk of hallucinations. This receptor belongs to the G protein-coupled receptor (GPCR) superfamily — a massive family of seven-transmembrane-helix proteins that detect extracellular signals and convert them into intracellular responses. The 5-HT2AR is implicated in schizophrenia, bipolar disorder, ADHD, migraine, and depression.

In psychiatry, this receptor has traditionally been *blocked* rather than activated. Atypical antipsychotics like risperidone and zotepine act as antagonists or inverse agonists at 5-HT2AR to treat schizophrenia. Meanwhile, classic antidepressants (SSRIs, SNRIs, MAOIs) work upstream, increasing synaptic serotonin levels rather than directly targeting 5-HT2AR. The problem is that direct 5-HT2AR agonists — drugs that switch the receptor on — are powerful psychedelics: LSD, psilocybin (which converts to psilocin in the brain), and mescaline all work primarily through this receptor.

This creates an intriguing therapeutic puzzle. Clinical studies of psilocybin have shown rapid and long-lasting antidepressant effects that persist even after the drug is cleared, suggesting that directly activating 5-HT2AR has genuine antidepressant potential. But the hallucinations are a serious barrier. Several research groups have recently synthesized partial agonists — compounds that activate the receptor only partially — such as IHCH-7086 and (R)-69, which show antidepressant-like effects in mouse models without triggering hallucinations (measured by the "head-twitch response," a rodent behavioral proxy for psychedelic effects). The molecular mechanism separating antidepressant activation from hallucinogenic activation was not well understood at the atomic level. This paper sets out to map those differences by comparing how different ligands shift the receptor's conformational landscape during MD simulations.

---

## 3. Approach & Methods

### The simulation strategy

The researchers ran 15 atomistic MD simulations using 7 experimentally determined crystal and cryo-EM structures of the 5-HT2AR as starting points. The 7 ligands represent the full spectrum of 5-HT2AR pharmacology:

- **Zotepine** — antagonist (antipsychotic)
- **Risperidone** — inverse agonist (antipsychotic)
- **Lisuride** — G protein-biased partial agonist, non-hallucinogenic
- **(R)-69** — G protein-biased partial agonist, non-hallucinogenic
- **IHCH-7086** — β-arrestin-biased partial agonist, non-hallucinogenic
- **25CN-NBOH** — β-arrestin-biased partial agonist, hallucinogenic
- **LSD** — β-arrestin-biased partial agonist, hallucinogenic

Crucially, each system was simulated in **two conditions**: with and without a small engineered G protein construct ("mini-Gq") inserted at the intracellular face of the receptor. This two-condition design was the key methodological choice. It lets the researchers observe the receptor *deactivating* (when G protein is absent, they can watch the active state collapse) and understand the *role of the G protein* in stabilizing active conformations.

### System preparation

Structures were downloaded from the RCSB PDB and prepared using **CHARMM-GUI**, the same tool you use in BioChemCore. CHARMM-GUI handled missing loop modeling, protonation of ligands with OpenBabel, and construction of the lipid bilayer. The membrane composition was modeled after synaptic vesicle membranes and contained POPC, POPS, PSM, POPE, ceramide, POPI, and cholesterol — a realistic, heterogeneous bilayer rather than a simplified pure-lipid system. Simulations ran in NAMD with the CHARMM36m force field (the same force field used in BioChemCore), with box dimensions of 75 x 75 Å and a water layer of 13.5 Å.

Each simulation ran between ~1 and ~4.8 microseconds. The equilibration protocol followed CHARMM-GUI's standard cascade: 10,000-step energy minimization, then progressive NVT and NPT equilibration runs with gradually weakening harmonic restraints, followed by unrestrained production MD.

### Analysis

The researchers quantified conformational state using "degrees of freedom" (DOFs) — a curated set of structural measurements known to track GPCR activation. These include:

- **Inter-helix distances**: TM6-2 (the canonical activation marker — TM6 moves outward during activation) and TM3-7
- **Microswitch angles**: torsion angles of key side chains like the tryptophan toggle switch (W336 on TM6), the ionic lock (E/DRY motif), and the PIF motif (F332)
- **NPxxY motif RMSD**: how much this conserved activation motif deviates from its inactive vs. active conformation

**Principal component analysis (PCA)** was applied to the time series of all DOFs to reduce the high-dimensional conformational data into two dominant axes of variance (PC1 and PC2), allowing all 15 simulations to be compared visually on a single 2D map.

---

## 4. Key Findings

### The G protein is necessary for full activation

Perhaps the most striking finding is that the receptor cannot achieve its fully active conformation — defined by the large outward swing of transmembrane helix 6 (TM6) — from agonist binding alone. In PCA space, all simulations *without* the G protein construct clustered to the left (inactive side), while all simulations *with* the G protein construct clustered to the right (active side), regardless of which ligand was bound. This directly supports the "conformational selection" model of GPCR activation, in which agonists do not directly *drive* the structural change but instead shift the receptor's energy landscape so that the G-protein-bound active state becomes more thermodynamically accessible. The activating ligand biases the probabilities; the G protein actually stabilizes the new conformation.

The ICL2 (second intracellular loop) remained helical only when the G protein construct was present, and TM6 reverted toward its inactive position within the first few hundred nanoseconds whenever the G protein was absent. This is a mechanistically important observation: the intracellular binding partner (whether the G protein or β-arrestin) is functionally required to lock in the active state.

### Hallucinogens occupy a distinct conformational region

In the G-protein-coupled simulations, the second principal component (PC2) separated the psychedelic ligands (25CN-NBOH and LSD) from the non-psychedelics. The psychedelics populated a region with higher PC2 values, associated with greater stabilization of the active NPxxY motif (Asn-Pro-x-x-Tyr on TM7). Non-psychedelic agonists like IHCH-7086 and (R)-69 landed in intermediate PC2 regions, while the apo receptor (no ligand) and the antagonist zotepine occupied the lowest PC2 values.

The contour plot in Figure 8 — plotting TM6-2 distance versus TM3-7 distance across all simulations — showed that psychedelics bound to the G protein-coupled receptor sampled the most "fully activated" conformational region (largest TM6-2 expansion combined with TM3-7 inward movement). Non-psychedelic partial agonists occupied partially activated states. This quantitatively supports the hypothesis that **hallucinations result from excessive, fully active-state populations of 5-HT2AR**, while **antidepressant effects correlate with modest, partial activation**.

### The NPxxY motif distinguishes psychedelic from non-psychedelic activation

The NPxxY motif (residues Asn-Pro-x-x-Tyr on TM7, a highly conserved structural element in GPCRs) remained in a low-RMSD, active-like conformation throughout the psychedelic simulations (25CN-NBOH, LSD) when the G protein was present. For the non-psychedelic ligand IHCH-7086, the NPxxY motif showed equilibrium between low-RMSD (active) and high-RMSD (inactive) conformations. For (R)-69 and lisuride with the G protein construct, the NPxxY motif gradually transitioned toward its inactive conformation within 200-300 ns, suggesting these G-protein-biased partial agonists cannot hold NPxxY locked in its active state as effectively.

### The tryptophan toggle switch explains hallucinogen specificity

The tryptophan residue W336 (on TM6, Ballesteros-Weinstein notation W6x48) is a critical "toggle switch" conserved across GPCRs. It exists in three rotameric states: "off" (inactive), "on" (active), and an unusual "alternative" conformation. The 25CN-NBOH simulations showed W336 clearly transitioning from the "off" to "on" state (χ2 angle shifting from ~120° to ~50°), driving active NPxxY stabilization through a hydrogen bond between W336 and N376 on TM7. (R)-69, the non-psychedelic G-protein-biased partial agonist, instead pushed W336 into the "alternative" rotamer — a conformation not seen with psychedelics and only observed with G protein-biased compounds. This alternative rotamer may represent a pharmacologically exploitable state for designing new G-protein-biased non-hallucinogenic compounds.

The antagonist zotepine penetrates deeper into the binding pocket and physically *blocks* the tryptophan toggle switch, preventing the conformational rearrangements needed to activate the PIF motif downstream.

### The TM5 bulge separates G protein bias from β-arrestin bias

A second PCA analysis that incorporated ligand-residue distances identified the TM5 bulge (centered on S242, position 5x46) as a key differentiator between G-protein-biased and β-arrestin-biased signaling. G-protein-biased agonists (R)-69, lisuride, and LSD all formed hydrogen bonds with S242 on TM5. This interaction induced an inward movement of I163 (3x40), which repositions the PIF motif phenylalanine F332, subtly modifying the receptor's intracellular surface geometry to favor G protein recruitment. By contrast, the β-arrestin-biased compounds IHCH-7086 and 25CN-NBOH did not form this hydrogen bond with S242, suggesting a mechanistic basis for their β-arrestin signaling preference. IHCH-7086 was in fact intentionally designed to avoid this interaction, consistent with these findings.

### A proposed activation sequence

The 2D density plots of TM6-2 versus TM3-7 distances across all simulations revealed that these two large-scale helix movements do not happen simultaneously — they occur sequentially. TM6 first moves outward (expanding TM6-2 distance), creating space for G protein binding, and only then do TM3 and TM7 move inward (reducing TM3-7 distance) to complete the full activation geometry. This sequential mechanism echoes findings from the β2-adrenergic receptor (Dror et al., 2011) and suggests a conserved stepwise activation pathway across the GPCR family.

---

## 5. Significance & Implications

### For drug design against depression

This paper provides atomic-level evidence for a mechanistic framework to guide the design of non-hallucinogenic 5-HT2AR antidepressants. The key design principle that emerges is: a sufficiently weak partial agonist — one that biases the receptor's conformational ensemble only modestly toward the active state — can generate antidepressant signaling without accumulating enough fully activated receptors to cause hallucinations. The distinction between "quantitative" activation (you bind weakly, so only a small fraction of receptors get activated) and "qualitative" activation (you bind strongly but stabilize a non-ideal partially active conformation) may both be viable routes to the same outcome.

The "alternative" rotamer of W336 observed during (R)-69 simulations is a specific, newly identified structural target. It represents a conformational state that is uniquely sampled by G-protein-biased partial agonists and may be useful for structure-based virtual screening of new drug candidates.

### Connection to BioChemCore

This paper is directly relevant to your MD simulation work. Every tool in the BioChemCore pipeline — CHARMM-GUI for system preparation, the CHARMM36m force field, NAMD-style equilibration protocols, VMD for visualization, and MDAnalysis for trajectory analysis — is used exactly as described in this paper. If you are simulating the 5-HT2AR yourself, the membrane composition they used (57 POPC, 18 POPS, 8 PSM, 12 CER160, 52 POPE, 4 POPI, 42 cholesterol) represents a biologically realistic synaptic vesicle membrane and could serve as a reference for your own CHARMM-GUI Membrane Builder setup.

The PCA approach to analyzing conformational states is directly applicable to your Day 7 analysis phase: rather than looking at RMSD alone, applying PCA to a set of curated DOFs (inter-helix distances, microswitch torsion angles) gives a far richer picture of what conformational states the receptor is sampling. This is essentially a more sophisticated extension of the RMSD and RMSF analysis planned for BioChemCore Day 7.

### Broader GPCR biology

The finding that G protein binding is necessary to *lock in* receptor activation (rather than agonists doing it alone) adds to a growing mechanistic consensus for the GPCR family. This "conformational selection plus induced stabilization" model has previously been observed in the β2-adrenergic receptor and may be a general principle. For a bioinformatics student working on membrane proteins, this is a key conceptual framework: ligand binding is not simply an on/off switch but a probabilistic bias of an ensemble of conformational states.

---

## 6. Limitations & Open Questions

**Timescale limitations.** The simulations are 1–5 microseconds, which is long by MD standards but still far shorter than the millisecond-to-second timescales of GPCR conformational transitions measured experimentally. The authors explicitly note that zotepine's behavior in G-protein-coupled simulations may not reflect its true thermodynamics due to insufficient sampling — the system never transitioned away from the active starting structure. Enhanced sampling methods (metadynamics, replica exchange, milestoning) would be needed to obtain converged free energy profiles.

**G protein construct is a simplification.** The intracellular "G protein construct" retains only the helical domain fragments from the mini-Gq protein that contact the receptor. It captures the stabilizing effect of G protein binding but does not reproduce the full allosteric complexity of the intact heterotrimeric Gq protein, including GDP/GTP exchange dynamics. Similarly, there is no β-arrestin model in the system, so the β-arrestin pathway is inferred indirectly from ligand biasing patterns rather than directly observed.

**Biased signaling ambiguity.** The study acknowledges that distinguishing between "G protein-biased" and "β-arrestin-biased" receptor conformations is difficult in MD because the structural differences between these putative states are small (as supported by Hammond's postulate, which predicts that nearby states on a reaction coordinate have similar structures). The paper is candid that this distinction may not matter much practically — both effects likely occur together in many cases.

**Limited ligand set.** Only seven ligands were studied, and some pharmacologically important compounds (ketanserin, DOI, psilocin itself) were not included. The conclusions about psychedelic vs. non-psychedelic structural signatures are supported within this set but would benefit from validation across a broader chemical series.

**No free energy calculations.** The 2D probability density plots are Boltzmann-inverted to "free energy units" but the authors explicitly state these should not be interpreted as converged free energy profiles. The quantitative barriers between states are not reliably estimated.

---

## 7. Key Terms & Concepts

**Transmembrane helix 6 (TM6) outward movement:** The defining structural event of GPCR activation — TM6 swings outward from the intracellular face of the receptor, opening a cavity that allows the G protein to bind. In 5-HT2AR, this outward movement is the primary readout of activation throughout the paper.

**Ballesteros-Weinstein numbering:** A standardized residue numbering system for GPCRs that assigns each residue a two-part identifier (helix number.relative position), allowing comparison across different GPCRs regardless of sequence alignment. For example, W6x48 means tryptophan on helix 6, position 48 within that helix's conserved numbering. This system is used throughout the paper.

**Microswitch:** A conserved residue or motif in GPCRs whose side-chain conformation changes discretely between active and inactive states, acting as a molecular switch. Key microswitches in 5-HT2AR include the tryptophan toggle switch (W6x48), the ionic lock (E/DRY motif on TM3-TM6), and the NPxxY motif on TM7.

**Biased agonism (functional selectivity):** When a ligand preferentially activates one downstream signaling pathway over another at the same receptor. For 5-HT2AR, G-protein bias means preferential Gq activation (leading to PLC/IP3 signaling), while β-arrestin bias leads to receptor internalization and arrestin-dependent kinase cascades. Different structural contacts — like the TM5 bulge hydrogen bond with S242 — appear to encode this preference.

**NPxxY motif:** A highly conserved amino acid sequence (Asn-Pro-x-x-Tyr) on TM7 that rearranges during GPCR activation. In the active state, the tyrosine residue (Y7x53) shifts inward and participates in a water-mediated hydrogen bonding network with conserved tyrosines on TM5 (the "TyrTyr" interaction). Its RMSD from the inactive structure serves as one of the key metrics in this paper.

**Principal component analysis (PCA) of conformational DOFs:** A dimensionality reduction technique applied here to ~40 structural measurements of the receptor. PCA finds the axes of maximum variance across all simulations, so that the complex multi-dimensional conformational landscape can be visualized on a 2D plot. PC1 here captures the classic active/inactive distinction; PC2 separates psychedelic from non-psychedelic activation patterns.

**Conformational selection vs. induced fit:** Two models for how ligands activate receptors. In induced fit, the ligand *causes* the receptor to change shape. In conformational selection, the receptor already samples many conformations spontaneously, and the ligand just stabilizes one. This paper's results support a conformational selection model for 5-HT2AR: agonist binding biases the ensemble, but the G protein is needed to fully stabilize the active state.

---

*Summary prepared in the context of the BioChemCore program (MD simulations of post-synaptic CNS membrane proteins). Paper accessed June 2026.*
