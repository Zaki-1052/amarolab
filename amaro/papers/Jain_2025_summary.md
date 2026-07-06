# Jain et al., 2025 — The Polypharmacology of Psychedelics Reveals Multiple Targets for Potential Therapeutics

**Citation:** Jain MK, Gumpper RH, Slocum ST, et al. *Neuron* 113, 3129–3142. October 1, 2025. https://doi.org/10.1016/j.neuron.2025.06.012

---

## 1. One-Sentence Takeaway

Classical psychedelics like LSD, psilocybin, and mescaline are not single-target drugs — they potently activate dozens of serotonin, dopamine, and adrenergic receptors simultaneously, and their hallucinogenic effects in vivo correlate most strongly with activation of multiple downstream signaling pathways at the 5-HT2A receptor.

---

## 2. Background & Motivation

For decades, neuropharmacologists assumed that psychedelics worked through a single, clean mechanism: activation of the 5-HT2A serotonin receptor (5-HT2AR), a GPCR expressed densely on layer 5 pyramidal neurons in the cortex. This receptor hypothesis explained why blocking 5-HT2AR with antagonists like ketanserin reliably abolishes the hallucinogenic effects of LSD and psilocybin in animals and humans.

But that tidy story had cracks. Other receptors — including 5-HT1A, 5-HT2B, dopamine D2, and TAAR1 — had been proposed as secondary contributors to psychedelic action, and there were inconsistencies in the literature about whether compounds like LSD and psilocybin also activate TrkB (the receptor for brain-derived neurotrophic factor, BDNF). Several groups proposed that TrkB activation, rather than serotonin receptor binding, might underlie the therapeutic antidepressant effects of psychedelics.

This paper's central motivation was to systematically resolve the confusion. The Roth lab, which runs one of the world's largest GPCR pharmacology programs, wanted to do an unbiased, comprehensive map of everything that classical psychedelics actually bind and activate across the entire druggable GPCR landscape. The question was: are psychedelics surprisingly dirty drugs with dozens of targets, or surprisingly clean ones with a few key receptors?

The answer turned out to be the former — and the implications go well beyond basic pharmacology, touching on drug development, safety, and how we think about the mechanism of action of a whole class of psychiatric medicines.

---

## 3. Approach & Methods

The team built a library of 41 classical psychedelics spanning three chemical classes: tryptamines (psilocybin, DMT, 5-MeO-DMT, and analogs), phenethylamines (mescaline, DOI, NBOMe compounds), and lysergamides (LSD, ETH-LAD, AL-LAD, and analogs). These were chosen using a computational technique called the Similarity Ensemble Approach (SEA), which uses pairwise Tanimoto similarity scores between compounds to ensure good chemical diversity coverage of the psychedelic structural space.

The experimental pipeline had three stages:

**Stage 1 — Broad receptor profiling (GPCRome screen).** All 41 compounds were screened against a panel of 318 human GPCRs using the PRESTO-Tango assay, a cell-based reporter system that measures receptor activation by quantifying beta-arrestin recruitment (which acts as a proxy for receptor activation). This gave an initial activity map at a single high dose (10 µM). Hits with >50% inhibition in primary binding were followed up in full radioligand competition binding assays to calculate precise binding affinity values (pKi).

**Stage 2 — Kinase screen for LSD.** Because recent papers had claimed LSD and psilocybin activate TrkB kinase directly, the team screened LSD against 450 human protein kinases using the commercial KINOMEscan platform. They also used live-cell reporter assays to test whether psilocybin or LSD allosterically modulate TrkB-BDNF signaling.

**Stage 3 — Transducer profiling (TRUPATH assay).** For the 5-HT, dopamine, and adrenergic receptor hits, the team used TRUPATH — a BRET2-based biosensor platform where individual G-protein transducers are labeled so you can measure which specific intracellular signaling pathway (Gaq, Gaz, Ga11, b-arrestin 1/2, etc.) gets activated, and by how much, for each drug-receptor combination. This produced a 100-pathway transducer matrix for each compound. The logic here is important: it's not enough to know a drug binds a receptor; you need to know which downstream signals it fires, because different pathways have different physiological consequences.

To connect this pharmacological data back to behavior, the team correlated their transduction coefficient values (a standardized measure of signaling pathway engagement) with published in vivo data — specifically the ED50 for the head-twitch response (HTR) in mice (a validated proxy for psychedelic-like behavior) and the mean recreational dose in humans.

For structural biology, they solved a 2.3 Å cryo-EM structure of LSD bound to the D2 dopamine receptor, then used molecular dynamics (MD) simulations to validate the binding pose of LSD's diethylamide moiety in the orthosteric pocket.

---

## 4. Key Findings

### Psychedelics are broad-spectrum GPCR agonists, not serotonin-selective drugs

The GPCRome heatmap showed that all 41 tested psychedelics activate nearly every member of the 5-HT receptor family, dopamine receptor family, and alpha2-adrenergic receptor family. Lysergamides (like LSD) hit the greatest number of targets (mean: 21.3 targets), followed by tryptamines (mean: 13.8), and then phenethylamines (mean: 12.0). In terms of binding affinity, lysergamides also had higher affinities across the board (mean pKi 6.97) compared to tryptamines (6.5) and phenethylamines (6.3).

A few compounds (25B-NBOMe, psilocin, DOI, and Bromo-DragonFLY) also showed activity at histamine H1, melatonin MT1/MT2, lysophosphatidic acid LPA2, somatostatin SST4, and opioid receptors — extending the polypharmacology even further.

### Psychedelics do not activate TrkB

LSD showed only weak, non-concentration-dependent interactions with a handful of kinases (BTK, DYRK1B, LKB1, PRKCE, RAF1, TGFBR1) with no potent hits at any of the 450 tested kinases, including TrkB. Neither psilocybin nor LSD showed agonist or allosteric modulatory activity at TrkB in live-cell reporter assays. This finding directly contradicts the TrkB hypothesis and is one of the paper's strongest and most pharmacologically consequential results.

### Psychedelics primarily signal through Gaq at the 5-HT2AR

The TRUPATH transducer profiling showed that the vast majority of psychedelics are biased toward the Gaq signaling pathway at the 5-HT2AR, rather than beta-arrestin pathways. Three compounds were notably beta-arrestin-biased: 5-MeO-DALT, 5-MeO-DiPT, and 5-MeO-EiPT. The bias toward Gaq is significant because recent evidence suggests 5-HT2AR Gaq-pathway activation is necessary for psychedelic-like effects in vivo.

### In vivo hallucinogenic effects correlate with 5-HT2AR signaling — specifically multiple pathways

When the researchers correlated their transduction coefficients with the head-twitch response ED50 in mice, they found strong correlations only for pathways within the 5-HT2 receptor family. The 5-HT2AR Gaq pathway showed the highest correlation (r = 0.97, p = 3.2e-7). In the human recreational dose analysis, 5-HT2AR was the only receptor with a strong correlation (>0.8), and specifically the Gaq, Ga11, and Ga15 pathways all showed correlations of r = 0.96.

This is a nuanced finding: it doesn't say only 5-HT2AR matters, but rather that the engagement of multiple transducer pathways at 5-HT2AR best predicts the drug's behavioral potency. Notably, ligand residence time (how long the drug stays bound to the receptor) was shown not to explain psychedelic potency — ruling out a simpler kinetic explanation.

### All tested psychedelics activate 5-HT2BR — a cardiac safety concern

Every compound in the library activated the 5-HT2BR via the Gaq pathway. This is a major finding because 5-HT2BR agonism is mechanistically linked to cardiac valvulopathy (heart valve damage) in humans — the same mechanism responsible for the serious cardiac side effects seen with the weight-loss drug fenfluramine and the anti-migraine drug ergotamine. The fact that all psychedelics in this study hit this target raises important safety questions for chronic or repeated use (such as in microdosing protocols).

### Cryo-EM reveals LSD binding architecture at D2R

The 2.3 Å cryo-EM structure of LSD bound to D2R confirmed LSD sits in the orthosteric binding pocket and adopts a trans conformation of its diethylamide moiety — consistent with what was seen in the 5-HT2AR-LSD crystal structure. Both D2R and 5-HT2AR use conserved H-bonding interactions with D3.32 and S5.46. The key aromatic residue in D2R is F110(3.28), while in 5-HT2AR it is W151(3.28). LSD's higher potency at 5-HT2AR compared to D2R is likely due to the closer positioning of W151 relative to the diethylamide moiety, creating stronger hydrophobic contacts. MD simulations independently validated the trans diethylamide conformation in the D2R binding pocket.

---

## 5. Significance & Implications

### For your BioChemCore project on the 5-HT2AR

This paper is directly relevant to your MD simulation work. It provides detailed pharmacological context for why the 5-HT2AR is such a rich simulation target: the receptor couples to at least three distinct G-protein subtypes (Gaq, Ga11, Ga15) plus beta-arrestin 1 and 2, meaning different conformational states of the receptor have different downstream effects. The transduction coefficient data quantifies how different ligands differentially stabilize different receptor conformations — this is the molecular basis for biased agonism, and it's exactly the kind of question MD simulations can probe by tracking TM helix movements and intracellular loop dynamics.

The cryo-EM/MD comparison in Figure 5 is particularly relevant: the authors used MD to validate LSD's binding pose in D2R, showing that simulation agrees with structural data on the preferred diethylamide conformation. This is a model for how you might analyze ligand dynamics in your own simulation — tracking which conformation a ligand adopts in the orthosteric pocket over time.

### For drug development

The finding that all psychedelics activate 5-HT2BR is a genuine red flag for therapeutic development programs. If you're designing a psychedelic-inspired antidepressant for repeated dosing, you need either a compound that selectively avoids 5-HT2BR or a dosing strategy that minimizes cumulative 5-HT2BR exposure.

The TrkB-negative result is equally important: it shifts the mechanistic explanation for psychedelic antidepressant effects back toward serotonin receptor-mediated plasticity (dendritic spine formation, cortical connectivity changes) rather than direct neurotrophin signaling. Drug programs that were targeting TrkB allosterism as the key antidepressant mechanism need to reconsider.

### The broader polypharmacology picture

This paper establishes definitively that psychedelics are polypharmacological agents. This complicates the narrative that their therapeutic effects are cleanly separable from their subjective effects — if you try to eliminate the hallucinogenic 5-HT2AR Gaq signaling to create a "non-hallucinogenic psychedelic," you might lose therapeutic efficacy too, given the tight correlation found here. The data suggest the two are mechanistically entangled.

---

## 6. Limitations & Open Questions

**The PRESTO-Tango assay has a structural caveat.** The assay engineers a vasopressin V2 receptor tail, a TEV protease cleavage site, and a transcriptional activator onto the C-terminus of each GPCR — a modification that can interfere with some ligands that non-specifically interact with those components. The authors note this explicitly for ETH-LAD and bromocriptine/cabergoline, which showed anomalous interference. This means some hits (and potentially some misses) in the GPCRome screen may be assay artifacts rather than true receptor pharmacology.

**The kinase screen only covered LSD.** The conclusion that psychedelics don't activate TrkB is fully supported for LSD but was extended to psilocin via a live-cell reporter assay. Other psychedelics in the library were not tested in the full kinase screen — a gap left explicitly unaddressed.

**Functional transducer profiling covered only 20 of 318 targets.** The TRUPATH analysis was limited to serotonin, dopamine, and adrenergic receptors, not all 318 GPCRome hits. Compounds with activity at histamine, melatonin, opioid, or LPA2 receptors were not characterized for their transducer coupling profiles at those secondary targets.

**In vivo correlation relies on the head-twitch response.** While the HTR is widely validated as a proxy for hallucinogenic activity in rodents, it is not a perfect model of human psychedelic experience. The correlation analysis, however impressive (r = 0.97), reflects a behavioral readout that may not fully capture the therapeutic or adverse effects relevant to clinical use.

**Cardiac safety is flagged but not fully characterized.** The paper identifies universal 5-HT2BR activation as a concern but does not quantify dose-response relationships for valvulopathy risk or model the cumulative exposure required to produce clinically significant valve changes.

---

## 7. Key Terms & Concepts

**Polypharmacology** — the property of a drug to bind and activate multiple distinct molecular targets simultaneously; this paper demonstrates it is a defining feature of classical psychedelics, not an incidental side effect of their chemistry.

**GPCR (G-protein-coupled receptor)** — the largest family of membrane receptor proteins in humans, spanning hundreds of subtypes; they transduce extracellular signals (hormones, neurotransmitters, drugs) into intracellular responses by activating G-proteins or recruiting beta-arrestins.

**Transduction coefficient (tau/KA)** — a quantitative measure of how efficiently a specific ligand-receptor pair activates a specific downstream signaling pathway; calculated from the maximum response (Emax) and the EC50 in a standardized assay, then normalized to a reference ligand. Higher values mean more signaling through that pathway.

**Biased agonism** — when a ligand preferentially activates one signaling pathway downstream of a receptor over another (e.g., preferring Gaq over beta-arrestin at 5-HT2AR); clinically significant because different pathways produce different physiological outcomes.

**TRUPATH** — a BRET2-based biosensor platform that directly measures which G-protein subtype dissociates from a receptor upon ligand binding, allowing pathway-specific quantification of GPCR signaling without relying on downstream second messenger readouts.

**PRESTO-Tango** — a cell-based reporter assay that measures receptor activation via beta-arrestin recruitment; used here for the initial 318-GPCR screen (GPCRome) of all 41 psychedelic compounds.

**5-HT2BR cardiac valvulopathy** — the well-documented mechanism by which chronic 5-HT2BR agonism causes structural changes in heart valve leaflets, leading to valvular regurgitation; mechanistically established from ergotamine, fenfluramine, and cabergoline case data, and now flagged as a concern for psychedelics.

---

*Summary prepared for BioChemCore context: Zara Alibhai, UCSD Year 2 Bioinformatics. Focused on 5-HT2A serotonin receptor MD simulation project.*
