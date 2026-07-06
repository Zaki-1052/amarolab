# Xu et al. 2026 — Psychedelics elicit their effects by 5-HT2A receptor-mediated Gi signalling

**Citation:** Xu Z. et al. *Nature* 651, 829–837 (19 March 2026). https://doi.org/10.1038/s41586-025-10061-7

---

## One-Sentence Takeaway

Classic psychedelics produce their hallucinogenic and therapeutic effects primarily through non-canonical Gi protein signalling downstream of the 5-HT2A receptor — not through the traditionally assumed Gq pathway — and this mechanistic insight enabled the rational design of a new non-hallucinogenic 5-HT2A agonist (DOI-NBOMe) with antidepressant and anxiolytic activity.

---

## Background & Motivation

Psychedelics — drugs like LSD, psilocybin, and DMT — are experiencing a genuine clinical renaissance. More than 200 trials are currently investigating them for major depressive disorder, treatment-resistant depression, anxiety, PTSD, and addiction. Yet despite this surge in therapeutic interest, the precise molecular mechanisms by which they work remain poorly understood. That knowledge gap matters enormously: without understanding the mechanism, it is very hard to separate the therapeutic benefits from the hallucinogenic side effects that create safety concerns and restrict clinical use.

The serotonin 2A receptor (5-HT2AR) has long been recognized as the primary molecular target of psychedelics. Textbooks and earlier research had framed 5-HT2AR as a "Gq-coupled receptor," meaning the dominant signalling pathway activated when a ligand binds is through the Gq family of G proteins. Gq activation triggers phospholipase C, which releases calcium and activates protein kinase C — a well-studied cascade. The prevailing assumption was therefore that Gq signalling drives the effects of psychedelics.

However, a puzzle existed. Non-hallucinogenic analogues (nHAs) — compounds structurally similar to psychedelics but lacking hallucinogenic activity — also bind 5-HT2AR with high affinity. Compounds like ariadne, isoDMT, and 2-Br-LSD sit alongside their hallucinogenic counterparts, binding to the same receptor. If Gq signalling were the entire story, there would be no clean pharmacological distinction between psychedelics and nHAs. This suggested that something more nuanced was happening — specifically, that differential engagement of non-canonical G protein pathways might be the key.

This paper set out to test whether Gi signalling, the "non-canonical" pathway for 5-HT2AR, is what distinguishes psychedelics from nHAs and drives hallucinogenic effects.

---

## Approach & Methods

The research combined pharmacological profiling, in vivo behavioural experiments, cryo-electron microscopy (cryo-EM) structural biology, alanine-scanning mutagenesis, molecular dynamics simulations, and structure-based drug design into one integrated study. This is a substantial methodological toolkit, and each component answered a distinct question.

**Pharmacological profiling.** The team systematically measured how well psychedelics and nHAs activate three downstream effectors of 5-HT2AR: Gq, Gi, and beta-arrestin 2 (βarr2). They used BRET (bioluminescence resonance energy transfer)-based assays in HEK293 cells, specifically GloSensor assays for Gi (measuring cAMP suppression) and TRUPATH assays to determine which of seven Gβγ subtypes are involved. This gave them a full signalling "fingerprint" for each compound. They then quantified signalling bias using the delta-log(RA) metric, which measures relative activity normalized to the endogenous ligand serotonin (5-HT), allowing direct comparison between pathways and compounds.

**In vivo behavioural experiments.** To establish whether Gi signalling matters in a living animal, they used the head-twitch response (HTR) assay, a well-validated proxy for hallucinogenic activity in rodents (the rapid side-to-side head shaking is a 5-HT2AR-mediated behaviour that correlates with human psychedelic experiences). They selectively blocked Gi signalling in vivo by injecting pertussis toxin (PTX) intracerebroventricularly (directly into brain ventricles), which inactivates Gi/o proteins. They also used Gq inhibitor YM25 and the CUMS (chronic unpredictable mild stress) mouse model of depression to test therapeutic effects.

**Cryo-EM structural biology.** The team resolved five cryo-EM structures of 5-HT2AR in complex with either Gi or Gq heterotrimers and bound to different ligands: DOI-bound 5-HT2AR–Gi (2.84 Å), psilocin-bound 5-HT2AR–Gi (2.62 Å), DOI-bound 5-HT2AR–Gq (2.76 Å), ariadne-bound 5-HT2AR–Gq (3.27 Å), and DOI-NBOMe–5-HT2AR–Gq (2.98 Å). The high resolution of these structures enabled detailed analysis of receptor-ligand and receptor-G protein interfaces. Focused local refinement was performed to improve density at the receptor, and all resolutions were validated with the gold-standard Fourier shell correlation (FSC) at the 0.143 criterion.

**Alanine mutagenesis and functional assays.** The team systematically mutated 60 residues throughout the receptor and measured the effect on Gq versus Gi signalling. This produced a pharmacological map of which parts of the receptor control which pathway.

**Molecular dynamics (MD) simulations.** They performed MD simulations of DOI-, psilocin-, and ariadne-bound receptor conformations, specifically measuring the distance between each ligand and the phenyl ring of residue F3396.51 (using the Ballesteros-Weinstein numbering convention for GPCRs). This provided mechanistic insight into how different ligands position differently within the binding pocket at an atomic level.

**Structure-based drug design.** Using the structural insights, they rationally designed DOI-NBOMe, a DOI derivative with an added methoxy-benzyl (NBOMe) group, and synthesized a series of analogues (compounds 7 and 7a–7d) to optimize Gq-biased, non-hallucinogenic activity. They validated DOI-NBOMe in multiple behavioural assays including HTR, forced swim test (FST), sucrose preference test (SPT), open field test (OFT), and marble-burying test (MBT).

---

## Key Findings

### 1. Psychedelics activate Gi signalling at 5-HT2AR far more potently than nHAs

When the team measured Gi, Gq, and βarr2 activation across a panel of classic psychedelics (DOI, LSD, psilocin, DMT, 5-MeO-DMT, 25I-NBOMe) and nHAs (ariadne, isoDMT, 2-Br-LSD, lisuride), the most striking pharmacological distinction was in Gi signalling. Psychedelics showed much stronger Gi coupling — characterized by both higher potency and higher efficacy — compared to nHAs, which clustered at pEC50 < 6.5 with efficacy below 50% of the 5-HT response. This Gi distinction was far more pronounced than differences in Gq or βarr2 signalling. TRUPATH assays confirmed that psychedelics activate the non-canonical Gαi subtype specifically, through pathways not engaged by nHAs.

### 2. Gi signalling is necessary for the hallucinogenic behavioural effect in vivo

When PTX was injected intracerebroventricularly to block Gi/o proteins, the head-twitch responses induced by DOI, psilocybin, and LSD were significantly attenuated. This is a strong in vivo demonstration that Gi signalling downstream of 5-HT2AR is functionally required for the hallucinogenic-like behavioural signature. PTX did not fully abolish HTR (which the authors attribute to dose-dependent incomplete blockade), but the partial blockade was still statistically significant and mechanistically informative. Notably, YM25 (the Gq inhibitor) did not block the HTR — underscoring that Gq is not the hallucinogenic pathway.

### 3. Gi signalling also mediates the therapeutic antidepressant and anxiolytic effects

Using the CUMS model, the team found that DOI and LSD reduced immobility in the forced swim test and increased sucrose preference — classic antidepressant-like effects. These therapeutic effects were blocked by YM25 (Gq inhibitor) but were unaffected by PTX (Gi blocker). This means the therapeutic effects depend on Gq, not Gi. The distinction is critical: hallucinogenic effects require Gi, but the therapeutic effects require Gq. This biased pharmacology is the key to developing non-hallucinogenic therapeutic agents.

### 4. Five cryo-EM structures reveal how receptor conformation differs between Gi and Gq complexes

The structural data showed that 5-HT2AR adopts a generally similar overall conformation whether coupling to Gq or Gi — the canonical orthosteric binding pocket accommodates psychedelics and nHAs similarly. However, the G protein coupling interface at the intracellular side differs critically. The αN helix of Gαi is positioned approximately 9 Å closer to intracellular loop 2 (ICL2) compared to Gαq, and this proximity involves a key salt bridge between Glu (in Gαi, at the position corresponding to G.HN.52) and Arg189 in the receptor's ICL2 (R1894.39). This interaction exists in DOI–5-HT2AR–Gi but not DOI–5-HT2AR–Gq complexes. The R189A mutation in 5-HT2AR significantly attenuated Gi signalling while mildly enhancing Gq — a beautiful example of a single residue controlling G protein selectivity.

### 5. Alanine scanning identifies three regions that specifically govern Gi activation

Systematic mutagenesis of 60 residues identified three distinct regions governing Gi versus Gq pathway selectivity. Region 1, around the orthosteric binding pocket (OBP), includes residues T1603.37, F2345.38, V2355.39, and L2294.52 — these undergo conformational changes when the ligand engages differently. Region 2 comprises residues on the intracellular face of TM1-3 and Helix 8 (including L1132.43, F1122.42, I1693.46, Y3876.50). Region 3, near TM5-6, includes Y2545.58, L3256.37, and K3206.32. The residue L2294.52 at ECL2 emerged as particularly important for DOI-mediated Gi signalling: its alanine substitution abolished Gi coupling while leaving Gq relatively intact for both DOI and psilocin, meaning it participates in drug-specific signalling bias rather than being a global Gi/Gq switch.

### 6. Molecular dynamics confirms ligand depth in the pocket predicts Gi coupling

MD simulations showed that DOI and psilocin maintained an average distance of approximately 5 Å from residue F3396.51 throughout their trajectories. Ariadne, the nHA, consistently remained closer at around 4 Å. The extra methoxy moiety of ariadne generates steric hindrance with W3366.48 and F3396.51, causing a rotation of the alkyl chain and a deeper binding pocket penetration. This structural distinction correlates with ariadne's failure to engage Gi. Importantly, substitution of F3396.51 with tryptophan (F339W) — adding steric bulk to mimic what ariadne encounters — abolished psychedelic-induced Gi signalling while preserving Gq, validating the MD prediction experimentally.

### 7. Rational design of DOI-NBOMe: a potent, selective Gq-biased agonist without hallucinogenic activity

Using the DOI-NBOMe–5-HT2AR–Gq cryo-EM structure, the team designed a DOI derivative that preferentially drives Gq over Gi. DOI-NBOMe has an NBOMe (2,3-dimethoxybenzyl) group on the amine of DOI. In the structure, the methyl group on the DOI alkyl chain of DOI-NBOMe faces toward F3396.51 in TM6-7, mimicking ariadne's binding mode. DOI-NBOMe showed no Gi activation (confirmed by TRUPATH and GloSensor assays), acted as a Gq-biased agonist in primary neurons, and was selective for 5-HT2AR over 5-HT1A, 5-HT2B, and 5-HT2C receptors. In behavioural tests, DOI-NBOMe did not induce head-twitch responses (confirming no hallucinogenic activity). It also attenuated the HTR induced by classical psychedelics including DOI and LSD. In the CUMS model, DOI-NBOMe improved sucrose preference and reduced FST immobility comparably to fluoxetine. These antidepressant-like and anxiolytic-like effects were abolished by MDL (a 5-HT2AR antagonist), confirming on-target activity. Marble-burying tests at 30 minutes and 24 hours after administration showed sustained anxiolytic effects, unlike DOI which showed only short-term effects consistent with its hallucinogenic mechanism.

---

## Significance & Implications

This paper resolves a long-standing mechanistic puzzle in psychedelic pharmacology. The field had assumed, based on the textbook classification of 5-HT2AR as a Gq-coupled receptor, that Gq signalling was the primary driver of psychedelic effects. This paper shows that is incorrect — or at minimum, incomplete. The hallucinogenic effects require Gi, and the therapeutic effects require Gq. The two pathways are dissociable, which means it is pharmacologically possible to design compounds that produce the therapeutic benefit without the hallucinogenic risk.

This is directly relevant to the clinical problem: the FDA and many clinicians are cautious about broad psychedelic use because of the hallucinogenic risks, particularly in patients with pre-existing psychotic disorders. If therapeutic effects can be achieved through a non-hallucinogenic, Gq-selective agonist like DOI-NBOMe, this opens a genuinely new class of antidepressant.

For the BioChemCore program specifically, this paper is an excellent case study in why molecular dynamics simulations and cryo-EM structures of GPCRs matter at a biological level. The MD simulations in this paper were not just confirmatory — they generated a specific, testable mechanistic hypothesis (that ligand depth in the OBP relative to F3396.51 gates Gi coupling), which was then directly validated by mutagenesis. This is exactly the kind of structure-function bridge that a 5-HT2AR MD simulation can contribute: identifying which receptor conformations correspond to which G protein partners.

The five cryo-EM structures deposited (PDB: 9LL7, 9LL8, 9LL9, 9LLA, 9LLB) provide high-quality starting templates for anyone simulating 5-HT2AR in different signalling states. They are especially valuable because they capture the receptor in both Gi-coupled and Gq-coupled states — meaning the conformational differences at the intracellular coupling interface are directly visible and measurable, not inferred.

The study also illustrates biased agonism as a general drug design strategy for GPCRs. Rather than needing to find a completely new target, one can tune the same receptor's signalling output by modifying ligand structure in ways that shift the receptor conformation toward one G protein coupling state versus another. This is an increasingly important concept in modern drug discovery for GPCRs broadly.

---

## Limitations & Open Questions

The paper is strong overall, but several limitations deserve note.

**The PTX blockade of HTR was incomplete.** The authors acknowledge this and attribute it to dose-dependent partial Gi/o inhibition. However, it leaves open the question of whether Gi is strictly necessary for the hallucinogenic effect or whether partial Gi activity alongside Gq contributes in a more complex, additive or synergistic manner. A complete dose-response characterization of PTX's effect on HTR would have been clarifying.

**Therapeutic vs. hallucinogenic signals appear to involve different pathways — but both require 5-HT2AR.** The conclusion that Gq drives therapeutic effects comes from the YM25 blockade of antidepressant-like behaviours. However, YM25 (pimavanserin) is an inverse agonist at 5-HT2AR with complex pharmacology. The interpretation assumes YM25 acts purely through Gq blockade, which may be an oversimplification.

**DOI-NBOMe has not been tested in humans.** All therapeutic claims are based on mouse models (CUMS, FST, SPT, MBT), which have limited translational reliability for complex psychiatric outcomes. The pharmacokinetics in mice (brain concentrations peak rapidly and clear within 8 hours) may not extrapolate directly to humans.

**The mechanism of G protein selectivity at the coupling interface warrants further investigation.** The R1894.39 - Glu salt bridge that favours Gi coupling is identified, but the full allosteric pathway by which ligand binding in the OBP selectively propagates to that intracellular surface is not completely resolved. The three intracellular regions identified by mutagenesis lack a complete mechanistic narrative connecting them.

**MD simulation details.** The molecular dynamics simulations described are relatively short comparisons of ligand-pocket distances; longer simulations tracking the full conformational transition between Gi- and Gq-coupled receptor states would provide richer mechanistic detail.

---

## Key Terms & Concepts

**5-HT2AR (serotonin 2A receptor):** A G protein-coupled receptor (GPCR) expressed in cortical neurons, the primary target of classic psychedelics. Traditionally classified as Gq-coupled, but this paper establishes it also couples functionally to Gi.

**Biased agonism (signalling bias):** When two ligands bind the same receptor but differentially activate downstream pathways. In this context, psychedelics are "Gi-biased" relative to nHAs at 5-HT2AR — they preferentially engage Gi over Gq compared to the endogenous ligand serotonin.

**Gi protein signalling (non-canonical for 5-HT2AR):** Gi/o proteins classically inhibit adenylyl cyclase, reducing cAMP. When activated by 5-HT2AR, Gi signalling also activates MAPK pathways and modulates transcription factors like Egr2. This paper establishes it as essential for hallucinogenic effects.

**Gq protein signalling (canonical for 5-HT2AR):** Gq activates phospholipase C, releases calcium, activates PKC, and drives gene expression of Fos. This paper shows that Gq-mediated signalling underlies the therapeutic antidepressant and anxiolytic effects of psychedelics.

**Non-hallucinogenic analogues (nHAs):** Compounds structurally similar to classic psychedelics that bind 5-HT2AR with high affinity but fail to induce hallucinogenic effects in behavioural assays. Examples include ariadne, isoDMT, and 2-Br-LSD. They are Gi-deficient at 5-HT2AR.

**BRET (bioluminescence resonance energy transfer):** A technique to measure protein-protein interactions (here, receptor-G protein coupling) in living cells. When two proteins bearing energy donor and acceptor tags are in close proximity (within ~10 nm), energy transfers and generates a measurable signal ratio. Used here to measure Gq dissociation and βarr2 recruitment.

**Cryo-EM (cryo-electron microscopy):** A structural biology technique that flash-freezes purified protein complexes in vitreous ice and uses electron beams to reconstruct 3D atomic-resolution structures. The five structures in this paper ranged from 2.62 to 3.27 Å resolution, sufficient to model individual side chains and atomic contacts.

**Orthosteric binding pocket (OBP):** The primary ligand-binding site in a GPCR, located within the transmembrane helix bundle. For 5-HT2AR, this is where all psychedelics and nHAs bind. Residues lining the OBP include W3366.48, F3396.51, S1593.36, and Y3707.43.

---

*Summary prepared for BioChemCore program context — 5-HT2AR is directly relevant as a post-synaptic CNS membrane protein target for MD simulation.*
