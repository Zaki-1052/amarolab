# Wallach et al. 2023 — Identification of 5-HT2A Receptor Signaling Pathways Associated with Psychedelic Potential

**Citation:** Wallach, J., Cao, A.B., Calkins, M.M., et al. (2023). Identification of 5-HT2A receptor signaling pathways associated with psychedelic potential. *Nature Communications*, 14, 8221. https://doi.org/10.1038/s41467-023-44016-1

---

## One-Sentence Takeaway

5-HT2A receptor Gq-protein signaling — not beta-arrestin2 recruitment — is the critical transducer pathway for psychedelic effects, and a Gq-efficacy threshold of ~70% (relative to serotonin) must be crossed for a drug to produce psychedelic-like behavior in mice.

---

## Background & Motivation

Serotonergic psychedelics — including psilocybin (the active component of magic mushrooms), LSD, DMT, and mescaline — have attracted enormous renewed interest as potential treatments for depression, PTSD, and addiction. However, a fundamental pharmacological question has remained unanswered: which molecular pathway downstream of 5-HT2A receptor activation actually produces the hallucinogenic experience?

The 5-HT2A receptor (5-hydroxytryptamine 2A receptor) is a G protein-coupled receptor (GPCR) — a class of membrane proteins that spans the cell membrane seven times and transduces extracellular chemical signals into intracellular responses. When a psychedelic drug binds to 5-HT2A, the receptor can activate two major downstream pathways. The first is the Gq/11 pathway: the receptor couples to a Gq protein, which activates phospholipase C (PLC), ultimately releasing second messengers like IP3 and DAG and raising intracellular calcium. The second is the beta-arrestin2 pathway: the receptor recruits the scaffolding protein beta-arrestin2, which both desensitizes the receptor and triggers its own set of signaling cascades.

The problem is that essentially all classical psychedelics activate *both* pathways to similar degrees. This "balanced" or "unbiased" pharmacology means you cannot simply compare a psychedelic to a non-psychedelic and conclude which pathway matters — both drugs hit both pathways. Attempts to disentangle this using knockout mice or pharmacological inhibitors have yielded conflicting, inconclusive results.

What was needed was a set of pharmacological tools — molecules engineered to be selective for one pathway over the other — that could be tested systematically. This study set out to build exactly that toolkit and use it to definitively answer which 5-HT2A transducer pathway drives psychedelic effects.

---

## Approach & Methods

The research team used a coordinated strategy combining medicinal chemistry, cell-based signaling assays, computational structural biology, and in vivo behavioral pharmacology.

**Assay platform — BRET:** To measure receptor signaling in living cells, the researchers used bioluminescence resonance energy transfer (BRET). This technique exploits the fact that energy can transfer between a luminescent donor molecule and a fluorescent acceptor molecule only when they are within a few nanometers of each other. By fusing luciferase to the G protein and a fluorescent protein (GFP or Venus) to another G protein subunit, you can read out G protein dissociation in real time as a proxy for receptor activation. A complementary BRET setup measured beta-arrestin2 recruitment directly. These assays have the advantage of measuring signaling at the receptor level, before second-messenger amplification steps confound the readout. All assays were run at physiologically relevant temperature (37°C) with 60-minute incubations to ensure full receptor occupancy.

**Compound library — the 25N series:** Classical psychedelics (psilocin, DMT, LSD, DOI, 25I-NBOMe) were first profiled at 5-HT2A. These all showed broadly similar Gq and beta-arrestin2 activity, confirming the unbiased problem. To create biased tools, the team built upon phenethylamine scaffolds, specifically 2,5-dimethoxyphenethylamine derivatives. They developed a series of N-benzyl substituted analogs (the "25N series") by systematically modifying the N-benzyl ring — varying electrostatic properties using Hammett sigma constants, introducing steric bulk at specific ring positions, and extending to larger aromatic systems like naphthalene and biphenyl. This structure-activity relationship (SAR) campaign systematically walked Gq efficacy down while preserving or enhancing beta-arrestin2 recruitment, ultimately yielding beta-arrestin2-biased agonists (e.g., 25N-NI-Nap, compound 16; 25N-NBPh, compound 17).

**Docking and molecular dynamics (MD) simulations:** To understand the structural basis of biased agonism, the team docked key compounds into the Gq-bound 5-HT2A cryo-EM structure (PDB: 6WHA) using induced fit docking (IFD) in Schrödinger's suite. Critically, they also ran 250 ns molecular dynamics simulations of the balanced agonist 25CN-NBOH and the beta-arrestin-biased agonist 25N-NI-Nap, each embedded in a lipid bilayer of DPPC phospholipids with explicit SPC water, using the GROMACS engine with the GROMOS96 54a7 force field. Twelve independent replicate trajectories were run for statistical robustness. This is directly relevant to the BioChemCore program — it exemplifies precisely the type of membrane protein MD simulation pipeline you are learning (system preparation via Schrödinger Maestro, lipid bilayer embedding, NPT production runs, trajectory analysis).

**In vivo behavioral readout — Head-Twitch Response (HTR):** In mice, psychedelic 5-HT2A agonists produce a characteristic rapid, involuntary side-to-side head movement called the head-twitch response (HTR). This behavior is absent for non-psychedelic 5-HT2A agonists, correlates well with human hallucinogenic potency across drug classes, and is blocked by 5-HT2A antagonists. The HTR was measured using head-mounted magnets and detection coils in C57BL/6J male mice. The team tested 17 compounds from the 25N series plus additional phenethylamine psychedelics, covering a wide range of Gq and beta-arrestin2 efficacies.

**Pathway inhibition:** To further confirm which pathway is required, the authors pharmacologically blocked downstream Gq signaling before administering psychedelics. YM-254890 is a selective inhibitor of Gq/11 that traps the G protein in its GDP-bound (inactive) state. Edelfosine is a phosphatidylinositol-selective PLC inhibitor targeting the Gq-PLC effector step. Both were administered centrally (intracerebroventricularly) or systemically before HTR testing.

---

## Key Findings

### 1. Classical psychedelics are pharmacologically balanced — neither Gq-biased nor beta-arrestin2-biased

When the team ran all classical psychedelics (psilocin, DMT, 5-MeO-DMT, LSD, 2C-I, DOI, 25I-NBOMe) through their BRET platform, every drug showed similar potency and efficacy at activating Gq dissociation and recruiting beta-arrestin2. The time-course profiles closely mirrored those of endogenous serotonin (5-HT). None of the drugs showed strong transducer bias. This is an important baseline finding: the field had been trying to link one pathway to psychedelia, but the drugs themselves don't give a clean answer because they don't separate the two pathways.

### 2. A 5-HT2A-selective biased agonist template was rationally designed

Using N-benzyl phenethylamine SAR, the team discovered that the electronic density at the C5 position of the N-benzyl ring (measured by Hammett sigma constants, a physical organic chemistry metric) strongly correlates with 5-HT2A binding affinity (Pearson R = −0.8887, p < 0.0001). Electron-donating groups at C5 increase potency. Steric bulk at the C2 position reduces 5-HT2B receptor activity (enhancing 5-HT2A selectivity), while steric bulk at C3 selectively reduces Gq Emax without eliminating beta-arrestin2 recruitment. The most selective compound, 25N-NBI (compound 10), showed 23-fold selectivity for 5-HT2A over 5-HT2C and minimal 5-HT2B activity. This systematic structure-function mapping is a textbook example of medicinal chemistry applied to GPCR pharmacology.

### 3. Bulkier N-aryl groups generate beta-arrestin2-biased agonists via a structural mechanism at W336^6.48

Extending the N-benzyl ring to naphthalene (25N-NI-Nap, compound 16) or biphenyl (25N-NBPh, compound 17) dramatically reduced Gq Emax while preserving beta-arrestin2 efficacy — the hallmark of beta-arrestin2-biased agonism. Induced fit docking and MD simulations revealed why: the key toggle switch residue W336^6.48 (in transmembrane helix 6, using the Ballesteros-Weinstein numbering system) occupies distinct rotameric conformations depending on which ligand is bound. For the balanced agonist 25CN-NBOH, W336^6.48 favors a chi2 angle around +66 degrees — the "active" rotamer seen in the cryo-EM active state structure. For 25N-NI-Nap, W336^6.48 is pushed into a chi2 angle around −15 degrees, an intermediate state between fully active and inactive. The larger N-naphthyl ring physically wedges W336^6.48 into this alternative rotamer, disrupting the full Gq activation pathway while preserving enough conformational change for beta-arrestin2 recruitment. TM6, which pivots outward during GPCR activation (the canonical activation movement), showed less outward swing with 25N-NI-Nap than with 25CN-NBOH in the MD simulations. These findings demonstrate that beta-arrestin-biased agonism at 5-HT2A arises from a specific, structurally explainable mechanism — not just a general partial agonist effect.

### 4. Gq-efficacy, not beta-arrestin2 recruitment, predicts psychedelic potential

This is the paper's central finding. Across 14 compounds in the 25N series spanning a wide range of Gq and beta-arrestin2 efficacies, there was a robust and highly significant positive correlation between 5-HT2A Gq-efficacy (Emax as percent of serotonin) and HTR magnitude (Spearman Rs = 0.8242, p = 0.0005). There was essentially no correlation between beta-arrestin2 recruitment Emax and HTR magnitude (Rs = −0.0153, p = 0.9638). Critically, this correlation was nonlinear with a clear inflection point: compounds with Gq Emax below ~70% of 5-HT failed to induce the HTR at all. The balanced agonist 25N-NBOMe (Emax ~100%) produced robust head twitches; the beta-arrestin2-biased compounds 25N-NI-Nap (Emax ~30–40% Gq) and 25N-NBPh (Emax ~60% Gq) produced no head twitches. This threshold relationship was also confirmed in a broader set of 24 phenethylamine psychedelics (Rs = 0.7339, p < 0.0001).

### 5. The Gq-PLC pathway is mechanistically required for the HTR

Blocking Gq signaling pharmacologically — not just genetically — ablated the HTR. Intracerebroventricular YM-254890 (Gq/11 inhibitor) blocked the HTR induced by R-DOI. Systemic edelfosine (PLC inhibitor) blocked the HTR induced by both R-DOI and 25N-NBOMe. These convergent pharmacological results strongly support the conclusion that continuous Gq-PLC signaling is required to produce the HTR — not just for receptor activation, but for the downstream effector cascade.

### 6. Non-psychedelic 5-HT2A agonists (lisuride, 2-Br-LSD, 6-F-DET, 6-MeO-DMT) fail to cross the Gq threshold

A long-standing mystery in the field has been why lisuride (a dopamine/serotonin agonist used clinically for Parkinson's disease and cluster headaches) binds 5-HT2A with high affinity but lacks psychedelic effects in humans. This paper provides a quantitative answer: lisuride has a Gq Emax of only ~48% relative to 5-HT — below the ~70% threshold. The same explanation applies to 2-Br-LSD (Emax ~64%), 6-F-DET, and 6-MeO-DMT (Emax ~57%). In the HTR assay, none of these compounds induced head twitches, while psychedelics LSD, psilocin, 5-MeO-DMT, and DET (all with Emax >70%) robustly did. The correlation coefficient for this extended set (including tryptamines and lysergamides) was R = 0.8948 (p = 0.0027). The Gq-efficacy threshold concept explains, in a principled way, why these structurally diverse compounds are non-psychedelic despite being 5-HT2A agonists.

### 7. Beta-arrestin2-biased agonists block psychedelic effects and induce tachyphylaxis

The beta-arrestin2-biased compounds 25N-NI-Nap and 25N-NBPh not only lack psychedelic potential themselves but also act as functional antagonists at the Gq pathway in vivo. Pretreatment with either compound blocked the HTR induced by the psychedelic DOI. Furthermore, repeated daily administration of 25N-NI-Nap for five days induced tolerance (tachyphylaxis) to a subsequent DOI challenge — similar to the tolerance induced by repeated DOI administration itself. This tolerance is likely mediated by beta-arrestin2-dependent receptor internalization and downregulation: in NanoBiT internalization assays, both 25N-NI-Nap and 25N-NBPh drove robust 5-HT2A receptor internalization from the cell surface, consistent with their strong beta-arrestin2 recruitment. This stands in contrast to the 5-HT2A antagonist/inverse agonist pimavanserin, which did not drive internalization and did not produce tolerance.

---

## Significance & Implications

This paper resolves a long-standing and pharmacologically important debate. The psychedelic field has been moving toward developing "non-hallucinogenic psychedelics" — drugs that might retain the therapeutic benefits (neuroplasticity, antidepressant effects) without the hallucinogenic experience. Two competing hypotheses existed: (1) you need beta-arrestin2 signaling for therapeutics and can eliminate Gq to remove hallucinations, or (2) you need Gq for both effects and must find other ways to reduce hallucinations. This study strongly supports the second interpretation, at least for the head-twitch behavioral phenotype.

The practical implications are significant. If therapeutic neuroplasticity (which has been associated with 5-HT2A Gq signaling and downstream TrkB activation) and hallucinogenic effects both require Gq activation, then non-psychedelic 5-HT2A agonists with therapeutic utility will need to be designed as partial Gq agonists — compounds that activate Gq enough to drive neuroplasticity but not enough to cross the ~70% threshold for hallucinations. 2-Br-LSD is already being explored clinically along these lines.

For the BioChemCore program specifically, this paper is a landmark example of how MD simulations of membrane proteins contribute directly to drug discovery. The W336^6.48 toggle switch story — where 250 ns simulations of the 5-HT2A receptor in a lipid bilayer distinguished active from intermediate receptor conformations — is exactly the type of analysis you will perform. The simulation setup (lipid bilayer, GROMACS, GROMOS force field, Maestro preparation, RMSD/dihedral angle analysis) maps directly onto the BioChemCore pipeline. The insight about TM6 outward pivot as a signature of Gq activation is foundational for analyzing your own simulation trajectories.

---

## Limitations & Open Questions

**Experimental limitations acknowledged by the authors:**

The HTR is a mouse behavioral proxy for human psychedelic experience. While the correlation between HTR potency and human hallucinogenic potency is well-validated, it is not perfect — species differences in 5-HT2A receptor pharmacology exist, and the degree to which the ~70% Gq-efficacy threshold translates to humans is unknown. The authors acknowledge this directly.

The study used recombinant HEK293T cells for signaling assays, which overexpress 5-HT2A and lack the native neuronal signaling environment, trafficking machinery, and receptor reserve effects present in brain tissue. The paper notes that future work in native tissues is needed.

Constitutive knockout approaches were deliberately not used (noting that beta-arrestin2 KO mice may have compensatory adaptations), but this means the paper cannot definitively rule out contributions from beta-arrestin2 in other 5-HT2A-mediated behaviors or in the therapeutic (non-HTR) effects of psychedelics.

**Open questions the paper raises but doesn't close:**

The mechanism linking Gq activation to the subjective psychedelic experience in humans remains unknown. The paper establishes a behavioral correlate but not the neural circuit mechanism. The question of whether partial 5-HT2A Gq agonists can produce antidepressant-like effects in preclinical models without HTR activity (the "therapeutic non-psychedelic" hypothesis) is raised but not tested here. The role of other G protein subtypes — the paper notes that Gi/11 deletion attenuates but doesn't eliminate the HTR, suggesting Gi or other subtypes may contribute — also remains open.

---

## Key Terms & Concepts

**5-HT2A receptor:** A G protein-coupled receptor (GPCR) expressed on cortical neurons that is the primary target of serotonergic psychedelics. It spans the membrane with seven alpha-helical transmembrane domains and couples to intracellular signaling proteins upon ligand binding.

**Gq/11 pathway:** One of the two major 5-HT2A downstream pathways. Gq proteins activate phospholipase C-beta (PLC-beta), which cleaves PIP2 into IP3 and DAG, releasing intracellular calcium and activating protein kinase C. This is the pathway the paper identifies as necessary for psychedelic effects.

**Beta-arrestin2 pathway:** The second major downstream pathway. Beta-arrestin2 is a scaffolding protein recruited to phosphorylated GPCRs. It desensitizes Gq signaling, drives receptor internalization, and activates its own downstream cascades (e.g., MAP kinases). This pathway is sufficient but not necessary for psychedelic behavior by itself.

**Biased agonism (functional selectivity):** A phenomenon where a ligand stabilizes a receptor conformation that preferentially activates one downstream pathway over another. A Gq-biased agonist activates Gq more than beta-arrestin2 (relative to a balanced reference agonist like the endogenous ligand); a beta-arrestin2-biased agonist does the opposite.

**BRET (bioluminescence resonance energy transfer):** A proximity-based assay used to measure protein-protein interactions in living cells. When two proteins fused to compatible donor/acceptor pairs come within ~10 nm, energy transfers and produces a measurable fluorescence signal. Used here to quantify both G protein dissociation and beta-arrestin2 recruitment at 5-HT2A.

**Toggle switch (W336^6.48):** A conserved tryptophan residue in TM6 of many GPCRs (superscript notation uses Ballesteros-Weinstein generic numbering). Its rotameric state (chi2 dihedral angle) is a key determinant of GPCR activation state — the "switch" flips between inactive and active conformations as the receptor activates. Bulky ligands in the orthosteric pocket can lock this residue in intermediate states, creating partial or biased activation.

**Head-twitch response (HTR):** A behavioral bioassay for psychedelic 5-HT2A agonist activity in mice. The involuntary, rapid side-to-side head movement is absent for non-psychedelic 5-HT2A agonists, 5-HT2A antagonists block it, and its potency correlates with human hallucinogenic potency across drug classes. Used here as the primary in vivo readout of psychedelic potential.
