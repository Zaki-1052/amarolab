# Gumpper et al. (2025) — The Structural Diversity of Psychedelic Drug Actions Revealed

**Citation:** Gumpper RH, Jain MK, Kim K, Sun R, Sun N, Xu Z, DiBerto JF, Krumm BE, Kapolka NJ, Kaniskan HU, Nichols DE, Jin J, Fay JF, Roth BL. *Nature Communications* 16:2734 (2025). https://doi.org/10.1038/s41467-025-57956-7

---

## One-Sentence Takeaway

Seven cryo-EM structures of the 5-HT2A serotonin receptor bound to every major class of psychedelic and non-psychedelic ligand reveal chemotype-specific binding motifs and conformational states that explain how different drugs produce distinct signaling biases — including hallucinogenic versus non-hallucinogenic effects.

---

## Background & Motivation

The 5-HT2A receptor (5-HT2AR) is a G protein-coupled receptor (GPCR) that sits in the postsynaptic membrane of cortical pyramidal neurons. It is the primary molecular target responsible for the psychedelic effects of compounds like psilocybin (the active ingredient in "magic mushrooms"), LSD, DMT, and mescaline. Over the past decade, these classical psychedelics have attracted enormous clinical interest as treatments for depression, anxiety, addiction, cluster headaches, and PTSD — and several are now in Phase II clinical trials.

Despite this excitement, a fundamental problem persisted: almost nobody understood at the atomic level *why* different psychedelics feel so different, or why some structurally related compounds are non-hallucinogenic while others produce vivid hallucinations. For example, 2-bromo-LSD (BOL) is an analog of LSD that is structurally very similar but completely non-hallucinogenic, yet it was recently found to effectively prevent cluster headaches. How can such similar molecules behave so differently?

The key to answering this lies in *biased signaling*. When the 5-HT2AR is activated, it can signal through at least two major pathways: the Gq protein pathway (which triggers intracellular calcium release and is associated with hallucination-related neural changes) and the beta-arrestin-2 (barr2) pathway (which triggers receptor internalization and different downstream effects). There are two competing hypotheses about which of these pathways produces hallucinations: one says barr2-biased signaling causes hallucinations; the other says a threshold level of G-protein activation is required, and partial agonism below that threshold produces therapeutic effects without hallucinations. A clear mechanistic picture required seeing how each drug class physically interacts with the receptor — which exact atoms touch which residues, and what conformational changes those contacts trigger.

Before this paper, crystal structures of the 5-HT2AR existed but were limited or contradictory. The authors had previously published two structures with selected phenethylamine agonists. What was missing was a comprehensive, internally consistent set of structures spanning every chemotype — tryptamines, ergolines, and phenethylamines — including both hallucinogenic and non-hallucinogenic representatives, and a biased agonist.

---

## Approach & Methods

### Structure Determination

The authors determined **seven active-state cryo-EM structures** of the 5-HT2AR in complex with the heterotrimeric Gq protein, covering:

- **Tryptamines:** serotonin (5-HT, the endogenous ligand), psilocin (the active form of psilocybin), and DMT
- **Ergolines:** LSD (hallucinogenic) and BOL (2-bromo-LSD, non-hallucinogenic)
- **Phenethylamines:** mescaline and RS130-180 (a novel beta-arrestin-biased compound)

They used a previously validated construct: the 5-HT2AR complexed with mini-GaqiN-Gb1-Gy2 (a mini-Gaq heterotrimer) stabilized by a single-chain antibody fragment (scFv16). This complex was co-expressed and purified from insect cells (Spodoptera frugiperda). The cryo-EM data were collected on a Talos Arctica electron microscope with a Gatan K3 detector, processed in cryoSPARC, and refined in Phenix using ChimeraX for model building. Resolutions ranged from approximately 3.1 to 3.5 Angstroms globally, with local refinement around the receptor itself reaching 2.5 to 3.5 Angstroms — good enough to place individual ligands confidently. Ligand placements were additionally validated using the GemSpot docking pipeline, which uses cryo-EM maps as docking restraints.

For **structural flexibility analysis**, the team used cryoSPARC's 3DFlex pipeline to generate conformational landscape models from each particle dataset, followed by UMAP dimensionality reduction. This captures the continuous distribution of receptor conformations rather than just a single averaged structure.

### Functional Validation

Structural findings were validated with two complementary approaches:

- **TRUPATH assays (BRET2):** A bioluminescence resonance energy transfer platform measuring Gaq activation in living cells in real time. This allows quantification of functional selectivity (bias) between Gq and barr2 pathways.
- **Beta-arrestin recruitment assays (BRET1):** Measured arrestin recruitment separately.
- **NB6 dissociation assay:** A conformational sensor using a 5-HT2A-kOR chimeric receptor with a nanobody (Nb6) that binds only the inactive state. When an agonist drives the receptor active, Nb6 dissociates, providing a readout of the active-to-inactive-state transition kinetics. This allowed time-dependent bias measurements for all ligands.
- **Site-directed mutagenesis:** Key residues identified in the structures were mutated (e.g., L229A, F234A, N343A, V235M/M218V for receptor subtype selectivity), and the functional consequences were measured to validate structural predictions.

---

## Key Findings

### 1. All ligands converge on the same orthosteric pocket with the same canonical pose

Despite spanning three chemically distinct classes, all seven ligands bind at the same orthosteric site on the 5-HT2AR — the cavity defined by transmembrane helices TM3, TM5, TM6, and TM7. Every ligand makes contact with D3.32 (Asp at Ballesteros-Weinstein position 3.32), which is the conserved "ionic lock" residue that forms a salt bridge with the protonated amine of all aminergic ligands. This validates decades of biochemical data confirming D3.32 as the primary anchor point.

The paper also confirms that the tryptamines (5-HT, psilocin, DMT) occupy the classic orthosteric site — not an alternative "extended binding pocket" that a prior structural report had proposed. When the authors compared their structures to those published by another group, the tryptamine core consistently sits in the validated orthosteric position, matching both the biochemistry and their new mutagenesis data.

### 2. Tryptamines share common contacts but show subtle, functionally important differences

The three tryptamines — 5-HT, psilocin, and DMT — all make ionic contact with D3.32 and hydrophobic contact with F3.39 and F6.52. However, subtle differences in how they position the indole ring have measurable functional consequences.

The most notable difference is in the 4'-OH position of psilocin versus the 5'-OH of 5-HT. The hydroxyl on 5-HT sits within hydrogen-bonding range of N6.55, while the psilocin hydroxyl points toward the amino tail of the molecule rather than N6.55. This is consistent with mutagenesis data showing that the N343A (N6.55) mutation influences 5-HT potency but not psilocin potency — suggesting water-mediated or electrostatic interactions differ between the two. DMT shows a slight shift in indole ring position compared to 5-HT because it lacks any accessory hydroxyl group to anchor it, explaining its different potency profile.

### 3. The ECL2 lid explains why ergolines bind so differently from tryptamines

LSD and BOL (the ergolines) are rigidified tetracyclic compounds derived from ergot alkaloids. Their bulky ring systems cannot fit into the orthosteric pocket the same way tryptamines do. Both ergolines contact D3.32 and F6.52, but LSD additionally forms a tight hydrophobic interaction with **L229 on extracellular loop 2 (ECL2)**. This ECL2 contact closes a "lid" over the orthosteric pocket, trapping LSD inside. Mutagenesis confirmed this: the L229A mutation converts mescaline from an agonist to an inverse agonist and dramatically alters LSD's behavior, whereas it doesn't affect 5-HT as strongly. This ECL2 interaction is the proposed mechanism for LSD's extraordinarily long receptor residence time (hours, not minutes), which may contribute to its prolonged duration of action.

BOL is distinguished from LSD by a single bromine atom at the 2-position. This bromine makes van der Waals contact deep within the orthosteric pocket with **I163** (I3.40 in BW numbering). Importantly, I163 sits in the **PIF motif** — a conserved structural element involving Pro-Ile-Phe residues in TM3 that undergoes a significant conformational change during receptor activation. The bromine-I163 interaction may interfere with full engagement of this PIF motif conformational switch, which the authors propose explains BOL's non-hallucinogenic partial agonist pharmacology.

### 4. Mescaline uses the ECL2 lid as a mechanism for 5-HT2A over 5-HT2B selectivity

Mescaline is a phenethylamine with relatively low potency at 5-HT2AR and even lower potency at the related 5-HT2BR. Unlike the ergolines, mescaline uses its 3'-methoxy group to form a hydrophobic interaction with L229 on ECL2 (the same residue critical for LSD). Structural overlay shows mescaline nestled between the ECL2 lid (L229) and TM5 (F234). Mutagenesis of F234A abolished mescaline's ability to activate the receptor.

The discovery that L229 is involved in mescaline's activation led the team to identify it as a potential selectivity determinant between 5-HT2A and 5-HT2B. At the 5.39 position, 5-HT2AR has a valine, while 5-HT2BR has a methionine. When they swapped these residues (V235M in 5-HT2AR and M218V in 5-HT2BR), BOL's behavior was dramatically altered — switching BOL into a partial agonist at 5-HT2AR and greatly attenuating its potency. This provides a molecular mechanism for how ergoline-based drugs could be redesigned for 5-HT2A selectivity.

### 5. The beta-arrestin-biased compound RS130-180 stabilizes a non-canonical receptor conformation

RS130-180 is an N-benzylated phenethylamine (related to the 25CN-NBOH compound) that functions as a beta-arrestin-biased agonist — meaning it preferentially recruits beta-arrestin-2 rather than coupling Gq. The cryo-EM structure reveals the molecular basis for this bias.

RS130-180 directly interacts with **W6.48** — the "toggle switch" tryptophan that is a universal activation switch for class A GPCRs. All other psychedelics in this study push on W6.48 indirectly or not at all, but RS130-180 physically contacts it due to its bulkier N-benzyl group. However, due to its steric bulk, RS130-180 forces W6.48 into an entirely downward-facing position not seen in any other 5-HT2AR structure.

This downward displacement of W6.48 causes an inward rotation of F332 (in the PIF motif), which in turn pushes Y380 (in the NPxxY motif) outward toward the receptor core. The NPxxY motif is critical for full G-protein coupling. The outward shift of Y380 at the bottom of TM7 is reminiscent of the inactive state crystal structure — meaning RS130-180 creates a conformation that is suboptimal for Gq activation but compatible with arrestin recruitment. The authors call this a **non-canonical (NC) state**, previously predicted from MD simulations but never before observed experimentally stabilized by an arrestin-biased ligand. Importantly, this is the first direct structural evidence of how biased agonism arises from a conformational intermediate rather than purely from kinetic differences in ligand dissociation.

### 6. Conformational diversity analysis (UMAP) shows each ligand stabilizes a unique receptor ensemble

Using 3DFlex and UMAP dimensionality reduction on the cryo-EM particle ensembles, the authors showed that despite all structures appearing globally similar in their average maps, each ligand stabilizes a **distinct conformational space** within the receptor. When all structures are aligned and then dimensionality-reduced, the particle clouds from each ligand separate into distinct clusters in UMAP space. This means the receptor does not adopt a single "active state" — each drug stabilizes a subtly different ensemble of conformations, which can differentially engage downstream transducers. This result directly supports the idea that biased signaling arises from ligand-specific conformational selection rather than a binary active/inactive switch.

### 7. Time-dependent bias measurements reveal a kinetic component for some ligands

Using TRUPATH time-course experiments, the authors measured Gq vs. barr2 activation as a function of time for all ligands. They found that 5-HT and mescaline show Gq-biased signaling, while RS130-180 and 25CN-NBOH show barr2 bias. For most ligands, the ratio of Gq to barr2 signaling shifts over time, suggesting a kinetic component to bias. However, RS130-180 and 25CN-NBOH dissociate rapidly from the receptor after the addition of the antagonist risperidone, whereas ergolines (LSD, BOL) do not — indicating that for N-benzylated phenethylamines, the observed signaling bias is not due to prolonged receptor residence time but rather to stabilization of the NC conformational state.

---

## Significance & Implications

This paper is a landmark in GPCR structural pharmacology for several reasons.

**For the psychedelics field specifically:** it provides the first comprehensive structural atlas of how every major psychedelic chemotype interacts with the 5-HT2AR at atomic resolution. The finding that all active compounds bind the same orthosteric site in the same canonical pose, yet produce different functional outcomes by subtly repositioning critical activation switches (PIF motif, toggle switch, NPxxY motif), explains decades of structure-activity relationship data and resolves contradictions between biochemical and structural models.

**For GPCR biology generally:** the NC state stabilized by RS130-180 is a rare direct structural observation of a conformational intermediate that explains biased agonism mechanistically. Most previous explanations of biased agonism relied on kinetic models or indirect evidence. The 3DFlex/UMAP analysis showing ligand-specific conformational ensembles also advances the view that GPCRs are not toggle switches but dynamic conformational selectors.

**For drug design:** the paper identifies specific residues and structural features that can be targeted to separate therapeutic signaling from hallucinogenic signaling, including the ECL2 lid (L229, F234) for isoform selectivity, the I163/PIF motif for BOL-like partial agonism, and the W6.48 toggle switch for arrestin bias. If hallucinations arise from full Gq activation rather than arrestin recruitment, then RS130-180-like compounds that stabilize the NC state could produce antidepressant or anti-addictive effects without psychedelic experiences. This would make them far more practical as daily-use psychiatric medications.

**For your BioChemCore program:** This paper is directly relevant because you are setting up an MD simulation of the 5-HT2AR (or could be). The cryo-EM structures deposited here (PDB accession codes 9ARX, 9ARY, 9AS0, 9AS2, 9AS3, 9AS4, 9AS5, 9AS7, 9AS9, 9ASA) provide excellent starting structures for MD work. The conformational flexibility analysis with 3DFlex and UMAP is essentially asking the same question that your RMSD/RMSF analysis will ask — how does the receptor move over time, and are certain regions more mobile than others? The distinction between the "global" (receptor-heterotrimer complex) and "local" (receptor alone) cryo-EM maps mirrors the kind of per-domain analysis you'll do in MDAnalysis. The ECL2 dynamics, the TM helix movements, and the conformational transitions of the NPxxY and PIF motifs are exactly the features you would want to track in a production trajectory.

---

## Limitations & Open Questions

**Limitations the authors acknowledge or that are worth noting:**

- **Mini-Gaq is not native Gaq.** The authors use a truncated, stabilized mini-Gaq heterotrimer to facilitate cryo-EM. While they note that mini-Gaq does not change the efficacy or potency of 5-HT2AR signaling, it does bias the receptor toward the Gq-coupled conformation. Structures with native Gq or with arrestin-2 directly bound would provide a more complete picture.
- **Cryo-EM structures are ensemble averages.** Each "structure" is actually an average over millions of particles. The 3DFlex analysis partially addresses this by recovering continuous conformational distributions, but the dynamic interconversion between states on physiological timescales — the thing MD simulations actually capture — is not directly observable by cryo-EM.
- **RS130-180 has suboptimal in vivo pharmacokinetics.** The authors acknowledge this directly: RS130-180 was optimized for in vitro potency and has poor metabolic stability for in vivo use. The structural mechanism it reveals is valuable, but the compound itself is not a clinical candidate.
- **The NC state was captured in one structure.** While the authors interpret the RS130-180 structure as stabilizing a non-canonical intermediate state, this is a single snapshot. MD simulations or additional biophysical measurements would be needed to confirm this state is thermodynamically stable and not a crystallographic or sample-preparation artifact.
- **The biological basis of hallucinations remains unresolved at the circuit level.** The paper contributes greatly to the molecular picture, but whether it is Gq signaling or arrestin signaling (or something else) that produces the psychedelic experience in humans is still not settled. The structural data provides mechanistic hypotheses, not direct causal proof.

**Open questions for future work:**
- What do these structures look like with native arrestin-2 rather than Gq as the transducer?
- Can MD simulations starting from the NC state (RS130-180 structure) capture the transition back to the fully active state?
- Are the ECL2 dynamics captured in the 3DFlex analysis relevant to ligand on-rate and selectivity in a lipid bilayer environment?

---

## Key Terms & Concepts

**5-HT2A receptor (5-HT2AR):** A G protein-coupled receptor (GPCR) in the serotonin receptor family, expressed on cortical pyramidal neurons, that binds serotonin (5-HT) as its native ligand and is the primary molecular target mediating the psychedelic effects of psilocybin, LSD, DMT, and mescaline.

**Biased agonism (functional selectivity):** The property of a ligand that preferentially activates one downstream signaling pathway over another at the same receptor — for example, driving beta-arrestin recruitment more than G protein activation, or vice versa. Different biases may produce different therapeutic and side-effect profiles.

**Orthosteric site:** The primary, evolutionarily conserved ligand-binding pocket of a receptor, where the endogenous ligand (here, serotonin) binds. Contrasted with allosteric sites, which are elsewhere on the protein and modulate activity indirectly.

**Ballesteros-Weinstein (BW) numbering:** A universal residue numbering system for GPCRs that assigns each residue a number based on its transmembrane helix (first digit) and its position relative to the most conserved residue in that helix (second number). For example, D3.32 means the aspartate on TM3, 32 positions from the most conserved residue. This allows direct comparison of equivalent residues across all GPCRs regardless of sequence differences.

**PIF motif:** A conserved triad of Pro-Ile-Phe residues in TM3 (specifically P5.50, I3.40, F6.44 in BW notation) that undergoes a characteristic conformational rearrangement during GPCR activation. Movement of this "microsensor" is coupled to outward movement of TM6 and transducer coupling.

**NPxxY motif:** A conserved sequence in TM7 (Asn-Pro-x-x-Tyr) whose tyrosine (Y7.53) changes position during activation and is involved in coupling TM7 movement to G protein or arrestin engagement at the intracellular face.

**Toggle switch (W6.48):** The conserved tryptophan residue at position 6.48 on TM6, whose rotameric state acts as an on/off switch for class A GPCR activation. Inward rotation of W6.48 is associated with receptor activation and outward movement of TM6, enabling transducer binding at the intracellular face.

**Non-canonical (NC) state:** A receptor conformation intermediate between the inactive and fully active G protein-coupled states, in which the intracellular surface is partially reorganized in a manner that impairs Gq coupling but permits arrestin recruitment. This state had been predicted by MD simulations and was directly observed here in the RS130-180 structure.

**cryo-EM (cryo-electron microscopy):** A structural biology technique that fires an electron beam through a thin film of rapidly frozen protein complex, producing thousands of 2D projection images that are computationally reconstructed into a 3D density map at near-atomic resolution. Unlike X-ray crystallography, it does not require crystals and works well for large membrane protein complexes.

---

*Summary prepared for BioChemCore — MD simulations of post-synaptic membrane proteins (5-HT2AR focus). PDB accession codes for structures in this paper: 9ARX (5-HT), 9ARY (BOL global), 9AS0 (BOL local), 9AS2 (DMT global), 9AS3 (LSD local), 9AS4 (mescaline global), 9AS5 (mescaline local), 9AS7 (psilocin local), 9AS9 (RS130-180 local), 9ASA (RS130-180 global).*
