# Signaling Snapshots of a Serotonin Receptor Activated by the Prototypical Psychedelic LSD

**Citation:** Cao et al. (2022). *Neuron*, 110(19): 3154–3167.e7. doi:10.1016/j.neuron.2022.08.006

---

## One-Sentence Takeaway

By solving three cryo-EM structures of the serotonin receptor HTR2B bound to LSD — in its transducer-free, Gq protein-coupled, and beta-arrestin-1-coupled states — this paper reveals the distinct molecular conformations the receptor adopts as it progresses through its full signaling cycle and explains, at atomic resolution, how LSD triggers two very different downstream pathways.

---

## Background & Motivation

Lysergic acid diethylamide (LSD) is the prototypical psychedelic drug. It was first synthesized in 1938 and is active in humans at doses as low as 25 micrograms — making it one of the most potent psychoactive substances known. Its effects (altered perception, mood, and sensation) can last 12 hours or more. Beyond recreational notoriety, LSD and related psychedelics are attracting serious attention as potential therapeutics for depression, PTSD, and addiction. However, the same receptor activity that produces psychedelic effects also poses medical risks: chronic LSD use, including microdosing, can cause drug-induced valvular heart disease through the serotonin 2B receptor (HTR2B).

LSD achieves all of this primarily by binding to G protein-coupled receptors (GPCRs). GPCRs are the largest family of membrane receptors in the human body, and LSD binds to nearly all 14 known serotonin receptor subtypes. The psychedelic effects are primarily mediated through HTR2A (the 2A subtype), but HTR2B is structurally very similar and much easier to work with experimentally — it expresses more highly, and a previous crystal structure of LSD-bound HTR2B already existed. This makes HTR2B an excellent model system for studying how LSD engages the molecular machinery of signaling.

The critical unanswered question before this paper was: how does LSD — a single molecule sitting in the same binding pocket — selectively engage two fundamentally different downstream signaling pathways at the same receptor? GPCRs signal through two major types of transducers: heterotrimeric G proteins (which produce the primary signaling output) and beta-arrestins (which traditionally desensitize the receptor but also initiate their own signaling cascades). Certain drugs, called biased agonists, preferentially activate one pathway over the other. LSD is known to activate the beta-arrestin pathway particularly strongly at many biogenic amine GPCRs. Understanding this at the structural level requires snapshots of the receptor in all three relevant states: alone (transducer-free), bound to a G protein, and bound to beta-arrestin. Before this paper, no receptor had been captured in all three states with the same ligand using cryo-EM.

---

## Approach & Methods

The core strategy was cryo-EM structure determination of HTR2B in three distinct states, combined with molecular dynamics (MD) simulations and functional assays to validate the structural observations.

**Getting the structures:**

HTR2B is a 54 kDa class A GPCR, but roughly 20 kDa of that is made up of flexible, unstructured loops that are invisible in standard structural methods. The authors used a previously described antibody fragment (Fab P2C2) as a fiducial marker — a rigid, well-characterized object attached to the receptor that gives cryo-EM particle alignment software something consistent to lock onto. This yielded 2.7–2.9 Angstrom resolution maps for the transducer-free and Gq-coupled states.

The beta-arrestin complex was considerably harder to build. The challenge is that GPCR-arrestin complexes are inherently unstable, because arrestin coupling normally requires receptor phosphorylation at specific residues on the receptor's C-terminal tail, and the assembled complex can fall apart during purification. The authors addressed this through extensive engineering:

- They first used BRET (bioluminescence resonance energy transfer) assays to systematically truncate HTR2B's C-terminal tail and identify which residues were essential for beta-arrestin-1 recruitment. They found that residues I453–L464 were critical, and that phosphorylatable serines S455, S456, and S457 within that region are likely the key phosphorylation sites.
- They introduced two point mutations (K247V and E319L) that break an ionic lock stabilizing the inactive receptor conformation, boosting LSD-stimulated beta-arrestin recruitment to levels comparable to the full agonist serotonin.
- They fused a constitutively active beta-arrestin-1 (with the R169E mutation) directly to the receptor C-terminus, bypassed the need for nanodiscs by using beta-arrestin isoform 2 (which lacks a membrane-anchoring C-edge loop), and fused a stabilizing scFv30 nanobody to the arrestin.
- GRK2 was co-expressed to phosphorylate the receptor, and the assembled HTR2B-beta-arrestin-1-scFv30 complex was purified and imaged to 3.3 Angstrom resolution.

All MD simulations used the CHARMM36m force field with AMBER20 as the simulation engine, run across five distinct conditions (transducer-free, Gq-coupled, beta-arrestin-coupled, and the two transducer-removed conditions). Each condition used 12 independent simulations of approximately 2–3 microseconds each, embedded in a POPC lipid bilayer, with system preparation done in Maestro (Schrodinger).

---

## Key Findings

### 1. The transducer-free state is partially active, not fully inactive

Compared to the earlier X-ray crystal structure of LSD-bound HTR2B, the cryo-EM transducer-free structure looks meaningfully different. The intracellular tips of transmembrane helices TM5 and TM6 — the helices that move the most during receptor activation — are not resolved in the cryo-EM map, meaning they are dynamically disordered. This is actually informative: it means LSD alone traps the receptor in a partially active conformation where the intracellular region is too flexible to be pinned down without a transducer. The extracellular ends of several transmembrane helices show 0.9–2.5 Angstrom outward movements compared to the crystal structure, slightly enlarging the ligand binding pocket. The authors argue this transducer-free cryo-EM structure may actually be a better template for computational drug docking than the crystal structure, because it more accurately reflects the receptor in solution.

MD simulations of the transducer-free state directly support this interpretation: the intracellular cavity spontaneously opens and closes on the microsecond timescale, transiently sampling conformations that could accommodate either a G protein or an arrestin. When transducers are computationally removed from the Gq- or arrestin-coupled simulation systems, the receptor relaxes back toward the transducer-free conformation. This captures the concept of conformational selection: LSD-bound HTR2B is not waiting in a single locked state but dynamically sampling a range of conformations, and whichever transducer is present stabilizes the conformation that fits it best.

### 2. Gq coupling follows expected GPCR mechanics with HTR2B-specific nuances

In the HTR2B-Gq complex, the alpha-5 helix of Gq inserts into the cytoplasmic cavity of HTR2B and makes extensive hydrophobic contacts primarily with TM2, TM3, TM5, TM6, TM7, and the second intracellular loop (ICL2). The ICL2 adopts a helical structure and sits in a hydrophobic groove on the Gq alpha-N helix — this binding mode is widely conserved across GPCR-G protein complexes. A key residue, I161 in ICL2, forms extensive hydrophobic interactions with the Gq surface that are essential for coupling; mutations here dramatically reduce coupling efficiency.

The comparison with HTR2A reveals one notable difference: ICL2 of HTR2B has a 2 Angstrom inward displacement compared to HTR2A, which shifts the alpha-N helix of Gq inward upon coupling. However, the alpha-5 helix coupling mode is nearly identical between the two receptors because the relevant residues in the cytoplasmic cavity are highly conserved. This validates the use of HTR2B as a structural model for HTR2A's signaling behavior.

### 3. Beta-arrestin-1 engages HTR2B through a flexible "finger loop" that adapts its conformation

Beta-arrestin-1 couples to HTR2B in a conformation roughly intermediate between those seen in M2R- and NTSR1-arrestin complex structures, tilted approximately 25 degrees less toward the receptor than in NTSR1, and rotated about 50 degrees relative to NTSR1. The engagement occurs at three points: the receptor core (primarily via arrestin's finger loop), ICL2, and the phosphorylated C-terminal tail.

The finger loop is the most important and interesting contact. In the HTR2B complex, the finger loop adopts a helical conformation — one of several conformations observed across different GPCR-arrestin structures — and threads into the cytoplasmic cavity to contact TM2, TM3, TM5, TM6, and TM7. The flexibility of the finger loop across different GPCR-arrestin structures appears to be a general mechanism by which a single arrestin molecule can adapt to the diverse cytoplasmic cavities of the GPCR superfamily. The G protein alpha-5 helix, by contrast, appears more rigid and adopts a similar conformation regardless of which GPCR it couples to.

Mutations in specific finger loop residues (L71, L73, R65) significantly reduce LSD-stimulated beta-arrestin recruitment, confirming these contacts are functionally important, not just structural observations.

### 4. The phosphorylated C-tail uses a distinct phosphorylation barcode compared to other GPCRs

The cryo-EM density of the phosphorylated C-tail of HTR2B was visible in the map and placed in contact with the arrestin R7 residue and the K294 gate loop — two sites known to be critical for arrestin activation. Mass spectrometry confirmed phosphorylation at S455 and S456, with lower probability at S457. Functional alanine mutations of each residue individually reduced beta-arrestin recruitment Emax by 30–50%. Importantly, the C-tail of HTR2B in this complex overlays well with the V2R C-tail (a well-characterized reference) but arrestin R7 has rotated more than 100 degrees to engage phospho-S457, suggesting HTR2B uses a C-tail phosphorylation pattern distinct from V2R.

### 5. Structural differences between transducer-coupled states explain biased signaling

This is the paper's most pharmacologically significant finding. Comparing the Gq- and beta-arrestin-coupled structures reveals that beta-arrestin coupling requires a substantially larger outward displacement of TM5 (1.7 Angstrom extra) and TM6 (2.5 Angstrom extra) beyond what Gq coupling needs. This larger opening is required to accommodate the bulkier helical finger loop of beta-arrestin compared to the thinner alpha-5 helix of Gq. Additionally, TM7 shows a less inward shift in the arrestin-coupled state, and ICL1 moves outward while helix 8 undergoes a downward rotation.

At the level of conserved receptor motifs, both transducer-coupled states share certain activation signatures — the toggle switch W337 downward movement, PIF motif rearrangement, and DRY motif conformational changes — but with distinct nuances. The DRY motif residue R153 adopts an extended conformation in the Gq-coupled state (pointing toward the alpha-5 helix) but bends downward toward the finger loop in the beta-arrestin-coupled state. The polar core residues N376 and S373 rotate toward TM2 and form an electrostatic interaction with D100 specifically in the Gq-coupled state, but remain in an intermediate orientation in the beta-arrestin-coupled state. This D2.50-N7.49 polar interaction appears to be a G protein-specific activation feature.

A single residue, N384 on helix 8, plays opposite roles in the two pathways. It forms a hydrogen bond with Gq alpha-5 helix residue N244, contributing to Gq coupling; when this residue is mutated to alanine, Gq recruitment drops by 40%. In the arrestin complex, N384 rotates 90 degrees to stack on top of V70 in the arrestin finger loop, favoring the hydrophobic interaction needed for arrestin recruitment. Mutating N384A actually increases LSD-stimulated arrestin recruitment by 15%. This single residue thus functions as a molecular switch that differentially contributes to each pathway.

### 6. MD simulations directly capture the transducer-coupling mechanism

The MD simulations provide the mechanistic link between the static snapshots. The transducer-free receptor simulations show the intracellular cavity spontaneously opening to a size consistent with transducer binding. The conformational space sampled by the transducer-free receptor substantially overlaps with the space sampled in both the Gq- and arrestin-coupled simulations. When transducers are removed from the coupled simulations, the receptor converges back toward the transducer-free ensemble. This supports a model where transducers function as allosteric stabilizers, locking down the conformational ensemble that LSD alone cannot fully stabilize.

---

## Significance & Implications

This paper achieves something genuinely novel: the first set of structures capturing the same GPCR with the same ligand in all three key signaling states (unbound, Gq-coupled, beta-arrestin-coupled) determined by cryo-EM rather than crystallography. The cryo-EM transducer-free structure better represents the receptor in its native solution state than prior crystal structures, making it a more useful template for structure-based drug design.

The mechanistic findings have direct implications for the design of biased agonists — drugs that selectively activate either the G protein or the arrestin pathway at a receptor. For the 5-HT2 receptor family, this is clinically significant. There is ongoing interest in developing psychedelic-inspired therapeutics with reduced cardiac risk (the valvular heart disease risk from HTR2B/arrestin signaling), or drugs with specific therapeutic profiles targeting one pathway's downstream effects. Knowing that Gq coupling requires a smaller TM6 outward movement than arrestin coupling suggests, for example, that a partial agonist that cannot fully open TM6 might be selectively Gq-biased.

The finding that the mechanism of functional selectivity differs across GPCR subfamilies (Gi-, Gs-, and Gq-coupled receptors all show distinct intracellular conformational changes when in arrestin-coupled states) is also important. It means that biased agonist design may not be generalizable — lessons learned at one receptor family may not transfer cleanly to another.

For the BioChemCore program context: this paper is highly relevant to understanding why 5-HT2A is the MD simulation target. HTR2B is the structural model for HTR2A, and the three cryo-EM structures reported here are likely the best available structural references for building and analyzing an HTR2A simulation. The PDB codes deposited (7SRS for the beta-arrestin complex, 7SRR for the Gq complex, 7SRQ for the transducer-free state) provide validated starting structures for system preparation in Maestro. The conformational differences identified in the transmembrane helices and intracellular loops are exactly the kinds of structural features to watch for when analyzing RMSD and RMSF from MD trajectories.

---

## Limitations & Open Questions

The engineered nature of the beta-arrestin-1 complex is the primary limitation, and the authors are admirably transparent about it. To achieve a stable complex, they truncated ICL3, fused beta-arrestin-1 directly to the receptor C-terminus, used a constitutively active beta-arrestin mutant (R169E), co-expressed GRK2, and added a stabilizing scFv30 nanobody. Each of these interventions could potentially perturb the exact details of how beta-arrestin engages the native receptor in a cell. The removed intracellular loop regions (which are not involved in arrestin recruitment based on BRET data) might still influence arrestin conformation subtly. The specific phosphorylation pattern enforced by GRK2 co-expression may not reflect the barcode that endogenous kinases produce in neurons.

The paper also does not address the temporal dynamics of signaling — the structures are snapshots, and transitions between them happen on timescales the simulations begin to probe but cannot fully capture. The MD simulations show the transducer-free receptor sampling open conformations but cannot yet simulate the actual assembly of the transducer-receptor complex from scratch.

Finally, while HTR2B is a validated model for HTR2A, direct structural studies of LSD-bound HTR2A in transducer-coupled states (which were done for the Gq state in Kim et al. 2020) would be needed to confirm whether all the detailed interaction differences noted here apply equally to the pharmacologically primary target.

---

## Key Terms & Concepts

**Cryo-EM (cryo-electron microscopy):** A structural biology technique where purified protein complexes are rapidly frozen in a thin layer of vitreous ice and imaged with an electron beam; single-particle analysis of thousands of images generates a 3D density map at near-atomic resolution without requiring crystals.

**Biased agonism (functional selectivity):** When a drug binds a receptor and preferentially activates one downstream signaling pathway over another — for example, preferentially engaging G proteins versus beta-arrestins — rather than activating both equally as an unbiased agonist would.

**Transducer:** Any protein that couples to an activated GPCR to relay its signal; in this paper the two transducers studied are the heterotrimeric G protein (Gq) and beta-arrestin-1.

**PIF motif:** A conserved trio of residues (Pro-Ile-Phe, by their single-letter amino acid codes) in GPCRs whose rearrangement acts as a mechanical relay between the ligand binding pocket and the intracellular surface; its transition to the active conformation is required to open the cytoplasmic cavity for transducer coupling.

**DRY motif:** A conserved Asp-Arg-Tyr sequence at the cytoplasmic base of TM3 in class A GPCRs; the arginine residue's rotamer state is a well-established indicator of receptor activation state and contacts the alpha-5 helix of G proteins upon coupling.

**Phosphorylation barcode:** The specific pattern of phosphorylated residues on the receptor's C-terminal tail and intracellular loops, installed by GPCR kinases (GRKs), that determines which arrestin conformation is recruited and how tightly; different receptors use different barcodes to encode distinct functional outcomes.

**CWxP / NPxxY motifs:** Conserved sequence motifs within the transmembrane bundle of class A GPCRs that undergo characteristic conformational changes during activation; the NPxxY motif near TM7 repositions the tyrosine residue to open the intracellular cavity, and its movement is closely linked to the polar core rearrangements that distinguish G protein from arrestin coupling.
