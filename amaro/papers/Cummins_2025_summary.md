# Summary: Cummins et al. 2025 — 5-HT2A Receptors: Pharmacology and Functional Selectivity

**Citation:** Cummins BR, Billac GB, Nichols DE, Nichols CD. *Pharmacological Reviews* 77 (2025) 100059.
**DOI:** https://doi.org/10.1016/j.pharmrev.2025.100059

---

## One-Sentence Takeaway

The 5-HT2A serotonin receptor is a structurally complex GPCR whose different ligand classes — psychedelics, antipsychotics, and serotonin itself — each engage distinct amino acid residues in the binding pocket to stabilize different receptor conformations, selectively activating downstream Gq or beta-arrestin signaling pathways with profound implications for drug design.

---

## Background & Motivation

Serotonin (5-hydroxytryptamine, or 5-HT) is a small molecule hormone and neurotransmitter that regulates nearly every biological process — mood, cognition, development, gut function, cardiovascular activity, and nociception. When serotonin signaling goes wrong, the downstream consequences include depression, anxiety, schizophrenia, obsessive compulsive disorder, and cardiovascular disease.

There are seven distinct families of 5-HT receptors (5-HT1 through 5-HT7), encoding 14 receptor subtypes total. Of these, 5-HT2A is the most consequential in the central nervous system. It is the most abundant excitatory serotonin receptor in the brain, with especially high density in layer V of the cortex. It is the primary molecular target of all classical psychedelic drugs — LSD, psilocybin (after conversion to psilocin), DMT, and mescaline — as well as the main target of atypical antipsychotics like clozapine, risperidone, and the Parkinson's drug pimavanserin.

The gap this paper addresses is nuanced but critical: we have long known *that* different ligands bind 5-HT2A, but we have not fully understood *how* they bind differently at the atomic level, and how those structural differences translate into different downstream signals. This concept — that a single receptor can produce different biological outcomes depending on which ligand is bound — is called **functional selectivity** or **biased agonism**. It is the central organizing idea of this review.

The motivation is urgent and practical. Psychedelic-assisted therapy has shown remarkable clinical results for treatment-resistant depression, PTSD, and addiction in recent trials. But psychedelics produce hallucinogenic experiences that complicate their clinical use. If researchers could understand which exact molecular interactions determine hallucinogenesis versus therapeutic benefit — and those may be separable signaling pathways — it would open the door to designing drugs that capture the therapy without the trip.

---

## Approach & Methods

This is a comprehensive review article, not an experimental study. The authors — including David Nichols, the preeminent synthetic chemist in psychedelic pharmacology — synthesize decades of structural, biochemical, and pharmacological evidence to build a detailed mechanistic picture of 5-HT2A receptor function.

Their method is systematic integration of multiple lines of evidence:

- **Structural data** from X-ray crystallography and cryo-electron microscopy (cryo-EM) of the 5-HT2A receptor in complex with different ligands, providing atomic-resolution snapshots of binding poses
- **Mutagenesis studies** that systematically substitute individual amino acids to determine which residues are required for binding, signaling, or both
- **Pharmacological assays** measuring functional outputs — Gq-mediated phosphoinositide (PI) hydrolysis, beta-arrestin recruitment, calcium flux — across different ligands and expression systems
- **Structure-activity relationship (SAR) analysis** comparing how chemical modifications to each ligand class change receptor binding and signaling
- **In vivo behavioral assays**, particularly the head twitch response (HTR) in rodents, used as a proxy for hallucinogenicity
- **Computational approaches** including HOMO energy calculations to compare the electronic properties of phenylalkylamine ligands to serotonin

A key methodological note the authors make: functional selectivity results depend heavily on the experimental system. Results from heterologous cell lines (engineered to express the receptor) can differ from native tissues, because native cells contain the full complement of scaffolding proteins, regulatory mechanisms, and endogenous signaling components. The review is careful to contextualize findings against this caveat throughout.

---

## Key Findings

### 1. The 5-HT2A Receptor Has Two Distinct Binding Pockets

The receptor's binding site contains two overlapping regions with different properties. The **orthosteric binding pocket (OBP)** is a narrow cleft deep within the transmembrane (TM) bundle — bounded by TM3, TM5, TM6, and TM7 — and is the site where the endogenous ligand serotonin binds. The **extended binding pocket (EBP)** is located higher up toward the extracellular side, near TM2, TM3, and TM7. Different ligand classes preferentially occupy these different regions of the overall binding site, and this geometric difference is part of what drives biased signaling.

A universally conserved anchor point in the OBP is **D3.32(155)**, an aspartate residue in TM3. It forms a salt bridge with the positively charged amine nitrogen present in virtually all 5-HT2A agonists. Mutation of this single residue eliminates binding for nearly every agonist tested — it is the essential foundation of ligand recognition.

### 2. Three Chemotypes Bind with Distinct Residue Contacts

The paper organizes 5-HT2A agonists into three structural families — ergolines, tryptamines, and phenylalkylamines — and shows each engages the receptor differently.

**Ergolines** (LSD, lisuride) are rigid, tetracyclic molecules. Their ergoline core sits deep in the OBP, with the diethylamide group of LSD occupying the EBP, making unique contacts with Y7.43(370) in TM7. LSD forms a "lid" with ECL2 (extracellular loop 2), which physically caps the binding pocket and explains LSD's exceptionally slow binding kinetics — the lid must move to let the drug out. Both LSD and lisuride show beta-arrestin bias over Gq, but the degree differs: the interaction of LSD's diethyl group versus lisuride's single ethyl group with Y7.43(370) appears to drive LSD's greater beta-arrestin engagement.

**Tryptamines** (psilocin, DMT, serotonin itself) bind with their indole cores higher in the pocket, near the EBP. Serotonin contacts the OBP primarily, interacting with D3.32(155) and S3.36(159) via hydrogen bonds. Notably, S3.36(159) is a serine unique to 5-HT2A among the 5-HT2 subfamily — the related 5-HT2B and 5-HT2C receptors both have an alanine at this position. This single amino acid difference appears to be a key determinant of subtype selectivity. The tryptamine psilocin lacks the contact with S3.36(159) that serotonin makes, likely contributing to different signaling outcomes.

**Phenylalkylamines** (mescaline, DOI, 25CN-NBOH) are more selective for 5-HT2A over other serotonin receptors than tryptamines are, despite having lower raw affinity than ergolines. Mescaline adopts an unusual out-of-plane orientation when bound, enabling hydrogen bonding with serine residues while maintaining contact with F6.52(340), which is essential for agonist activity. The 2,5-dimethoxy substitution pattern common in potent phenylalkylamine agonists appears to provide electronic properties — specifically HOMO (highest occupied molecular orbital) energy — nearly identical to serotonin's indole ring, suggesting these substitutions electronically mimic serotonin's aromatic system.

### 3. Key Microswitches Govern the Active vs. Inactive State

Receptor activation involves rearrangement of conserved "toggle switch" residues that act like molecular switches between active and inactive conformations. The most important is **W6.48(336)** in the CWxP motif, which undergoes a dramatic ~80-degree rotation and 5 Angstrom displacement upon agonist binding. N-benzyl phenethylamine agonists interact with W6.48(336) in a way that biases signaling toward beta-arrestin recruitment specifically.

Other key motifs include the **PIF motif** (P5.50, I3.40, F6.44 — forming an interface between TM3, TM5, and TM6 near the base of the OBP), the **DRY motif** (D3.49, R3.50, Y3.51 — a conserved salt bridge in the intracellular domain), and the **NPxxY motif** (N7.49 through Y7.53 in TM7). Indications of beta-arrestin-biased conformation include larger perturbations in TM7 and the NPxxY motif, combined with a partially activated PIF motif and intact DRY salt bridge.

The paper also highlights **I3.51(181)** in intracellular loop 2 as critical for Gq coupling — mutation to alanine completely abolishes Gq activation by 25CN-NBOH while increasing beta-arrestin recruitment.

### 4. Canonical Signaling: The Gq-PLC-IP3-Calcium Cascade

The primary downstream pathway from 5-HT2A activation is Gq coupling, which activates **phospholipase C-beta (PLC-beta)**. PLC-beta cleaves PIP2 (phosphatidylinositol 4,5-bisphosphate) in the membrane into two second messengers: **diacylglycerol (DAG)**, which stays in the membrane and activates protein kinase C (PKC), and **IP3** (inositol 1,4,5-triphosphate), which diffuses to the endoplasmic reticulum and opens calcium channels. This IP3-mediated calcium release is the most widely studied output of 5-HT2A activation and the assay used to measure canonical agonism.

Kim et al. (2020) showed using BRET-based G protein dissociation assays that 5-HT2A receptors primarily couple to Gq and G-alpha-11, and to a much lesser degree G-alpha-2. The review notes that the rodent 5-HT2A OBP differs from the human OBP at position 5.46(242) — rodents have an alanine where humans have a serine — and this single difference has order-of-magnitude effects on agonist affinity and potency. This is a critical caveat for interpreting mouse HTR data.

### 5. Noncanonical Signaling: beta-Arrestin and Beyond

Beyond Gq, 5-HT2A receptors signal through beta-arrestin recruitment (mediating receptor desensitization and internalization), phospholipase A2 (PLA2, releasing arachidonic acid), Src kinase, ERK, AKT, and even JAK-STAT and Rho/Arf pathways. The full signaling web is shown in Fig. 9 of the paper.

Beta-arrestin signaling is of special interest because Wallach et al. (2023) reported a series of beta-arrestin-biased 5-HT2A agonists that did NOT produce the head twitch response in mice — suggesting that Gq signaling, not beta-arrestin, is required for at least this proxy of hallucinogenicity. However, the relationship is complicated by Rodriguz et al. (2021), who found that beta-arrestin 2 knockout actually attenuates the HTR to LSD — implying beta-arrestin 2 is needed for LSD's full HTR even though it is not sufficient alone. The paper is admirably honest that this picture is unresolved.

The paper also highlights that ligands can show **selective antagonism** of G protein subtypes. Pimavanserin, altanserin, and volinanserin show differential effects on Galpha-i versus Galpha-q/11 coupling in postmortem human brain, revealing that even "antagonism" at this receptor is more nuanced than a simple on/off switch.

### 6. Implications for Drug Design Are Significant but Not Yet Realized

Antagonists have been clinically useful for decades (antipsychotics), but agonist development is newer and more complex. The authors identify that it may be possible to design ligands targeting specific residues to activate anti-inflammatory pathways without behavioral effects, since Flanagan et al. (2020) showed anti-inflammatory effects of some psychedelics are independent of both Gq and beta-arrestin signaling. For psychiatric disorders where Gq and psychedelic effects may be intertwined, truly separating therapeutic from experiential effects may be harder.

The authors identify that a 70% Emax threshold for Gq activation appears necessary to produce HTRs in rodents, and that Gq inhibitor experiments in cortical neurons confirm Gq is required for psilocin/25CN-NBOH's effect on pyramidal neuron firing. This pharmacological threshold gives a quantitative target for functionally selective drug design.

---

## Significance & Implications

This review is foundational reading for anyone working with the 5-HT2A receptor. Its core contribution is connecting atomic-level structural data to macroscopic pharmacological and behavioral outcomes — a "structure tells us function" framework that is the gold standard for rational drug design.

For the BioChemCore program specifically, this paper is directly relevant to MD simulation work on the 5-HT2A receptor in several ways:

**Conformational states:** The active vs. inactive receptor structures are described in detail, with specific TM helix displacements (TM5 and TM6 moving outward, TM7 shifting slightly inward). These are exactly the structural dynamics that MD simulations would capture. The RMSD and RMSF analyses done in trajectory analysis correspond directly to measuring these conformational changes.

**Key residues to monitor:** D3.32(155), W6.48(336), S5.46(242), S3.36(159), and the motif residues (DRY, NPxxY, PIF) are the structural landmarks to track in any 5-HT2A simulation. Deviations in these regions indicate conformational state transitions.

**Ligand binding pocket geometry:** The description of the OBP vs. EBP and how ECL2 forms a "lid" over the binding site is directly relevant to understanding what conformational changes to expect in an apo (unbound) receptor simulation versus a ligand-bound one.

**Membrane context:** The paper notes that system-dependent effects are major confounders in pharmacology — the lipid environment around the receptor affects signaling. This underscores the importance of using realistic lipid compositions in MD simulations, which connects to the CHARMM-GUI membrane builder setup in BioChemCore.

**Broader implications:** Functionally selective agonism at 5-HT2A is the rationale behind the entire psychedelic therapeutics field's push to develop non-hallucinogenic analogs. Understanding this receptor is not just academic — it underpins clinical development for depression, addiction, OCD, Alzheimer's, and neurodegenerative disease.

---

## Limitations & Open Questions

The paper is a review and is appropriately careful about what is and is not established. Key open questions include:

- **Which signaling pathway mediates therapeutic effects?** This is openly unresolved. The HTR/hallucinogenesis link to Gq is supported, but neither Gq nor beta-arrestin has been definitively shown to underlie clinical antidepressant or anxiolytic effects.
- **Rodent vs. human translatability.** The single amino acid difference at 5.46(242) between mouse (Ala) and human (Ser) 5-HT2A causes order-of-magnitude shifts in agonist pharmacology. This is a substantial limitation of any rodent pharmacology study, including the HTR behavioral data used throughout.
- **The subjective experience problem.** The authors are candid that it is unknown whether the patient's subjective psychedelic experience (the "trip") is necessary for therapeutic benefit. This cannot be resolved in animals.
- **Cell line vs. native tissue discordance.** Heterologous expression systems may not faithfully capture native signaling because endogenous scaffolding proteins, regulators, and lipid environments differ. Many of the cited studies use heterologous systems.
- **The PLA2 pathway data is old and partially retracted.** The paper notes that the original 1975 report of 5-HT stimulating PLA2 was in a subsequently retracted paper — a small but notable flag about the canonical status of this pathway.

---

## Key Terms & Concepts

**Functional selectivity (biased agonism):** The ability of different ligands at the same receptor to preferentially activate different downstream signaling pathways — for example, one ligand biasing toward Gq while another biases toward beta-arrestin.

**Orthosteric binding pocket (OBP):** The deep, conserved region within the transmembrane bundle where the endogenous ligand (serotonin) normally binds, anchored by D3.32(155).

**Extended binding pocket (EBP):** A secondary region above the OBP, near the extracellular face, where bulkier ligand substituents (like LSD's diethylamide) make additional contacts that influence selectivity and kinetics.

**Toggle switch (W6.48):** A tryptophan residue in TM6 that undergoes large-scale rotation and translation upon receptor activation, functioning as a molecular on/off switch. Its position is diagnostic of active vs. inactive vs. beta-arrestin-biased receptor conformations.

**Gq-PLC-IP3-calcium cascade:** The canonical 5-HT2A downstream pathway: Gq protein activates phospholipase C-beta, which cleaves PIP2 into DAG and IP3; IP3 triggers calcium release from the endoplasmic reticulum, activating kinases and downstream gene expression.

**Head twitch response (HTR):** A rapid, stereotyped head movement in rodents induced by 5-HT2A agonists that serves as a behavioral proxy for hallucinogenicity. Currently the best available in vivo readout for comparing agonist bias toward hallucinogenic potential.

**ECL2 (extracellular loop 2):** A flexible loop that forms a "lid" over the ligand binding pocket. For LSD, ECL2 contacts with the diethylamide group are proposed to explain LSD's unusually slow dissociation kinetics (long residence time in the receptor).
