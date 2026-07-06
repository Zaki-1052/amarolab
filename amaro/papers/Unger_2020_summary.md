# Directed Evolution of a Selective and Sensitive Serotonin Sensor via Machine Learning

**Citation:** Unger et al. (2020). *Cell*, 183(7): 1986–2002.e26. doi:10.1016/j.cell.2020.11.040

---

## One-Sentence Takeaway

Using a three-stage machine-learning-guided directed evolution pipeline, researchers engineered iSeroSnFR — a fluorescent serotonin sensor built from a bacterial binding protein — that can detect millisecond-scale serotonin release in live neurons, brain slices, and freely behaving mice.

---

## Background & Motivation

Serotonin (5-hydroxytryptamine, or 5-HT) is one of the most clinically important neuromodulators in the brain. It shapes mood, cognition, fear, sleep, and social behavior, and its dysregulation underlies depression, anxiety, and many other psychiatric disorders. Nearly every major class of antidepressant — including the widely prescribed selective serotonin reuptake inhibitors (SSRIs) like escitalopram and fluoxetine — works by targeting the serotonin system. And yet, as of 2020, researchers still had no reliable way to directly watch serotonin being released in real time inside a living brain.

The tools that existed before iSeroSnFR were seriously limited. Microdialysis collects fluid from brain tissue but averages signal over many minutes and millimeters — far too coarse to capture the sub-second dynamics of neurotransmitter release. Fast-scan cyclic voltammetry (FSCV) is faster but requires implanted electrodes and can only work in a handful of brain regions where the signal-to-noise is favorable. Neither approach can be targeted to specific cell types or subcellular compartments.

The emerging alternative — genetically encoded fluorescent sensors — seemed promising. These are protein constructs that change their fluorescence brightness when they bind a specific molecule, and they can be introduced into neurons using viral gene delivery. Several sensors had been developed for other neurotransmitters (glutamate, dopamine, acetylcholine, GABA). The problem with serotonin was that no naturally occurring bacterial binding protein, called a periplasmic binding protein (PBP), was known to bind 5-HT with high affinity. PBPs are the preferred scaffold for these sensors because they are soluble, can be targeted anywhere in the cell, don't respond to pharmaceutical drugs, and produce large fluorescence changes when they grab their ligand. Without a serotonin-binding PBP to start from, the researchers had to engineer one from scratch — essentially reprogramming the binding pocket of an acetylcholine-sensing PBP to recognize a structurally very different molecule.

This paper describes exactly how they did that, and how well the resulting sensor works.

---

## Approach & Methods

The core challenge was converting a protein that naturally binds choline and acetylcholine (ACh) into one that binds serotonin — two molecules with very different shapes, charges, and chemical properties. The strategy was a three-step pipeline combining computational protein design, machine learning, and a classic biochemical optimization technique called site-saturated mutagenesis (SSM).

**Starting scaffold.** The team started with an early version of their existing acetylcholine sensor, iAChSnFR0.6. The binding domain came from a PBP called OpuBC, derived from the thermophile bacterium *Thermoanaerobacter sp. X513*. Conveniently, this protein already showed a very weak, detectable response to serotonin (dissociation constant K_d greater than 1 mM), giving the team a foothold to work from.

**Step I: Rosetta computational redesign.** The researchers used the Rosetta protein design software to computationally model the binding pocket. They first generated multiple 3D conformations of serotonin using a cheminformatics tool (Open Eye Omega), docked these into the closed structure of the protein, and then asked Rosetta to predict which amino acid mutations would make the pocket bind serotonin better. From 250,000 computationally ranked variants, they synthesized and tested the top 18. The best of these — called iSeroSnFR0.0 — showed an 87% fluorescence change in response to 10 mM serotonin, with no detectable ACh response. This was an 18-fold improvement in selectivity. Crucially, it was not yet sensitive enough for physiological detection, but it established the binding scaffold.

**Step II: Random Forest (RF) modeling.** With iSeroSnFR0.0 in hand, the team performed site-saturated mutagenesis at the four positions Rosetta had ranked as most important (positions 66, 170, 143, and 188). In SSM, every possible amino acid is substituted at each target position, and the variants are tested. Rather than just picking the best individual mutants, they used a Random Forest model — an ensemble machine learning approach — to analyze the data from ~2,576 screened variants. Random Forest is particularly good at working with small, noisy datasets and at identifying which positions matter most ("feature importance"). The key insight was that the best-performing variants consistently combined mutations at multiple positions. No single mutation dramatically improved things; synergistic combinations were required. The RF model correctly predicted the rank order of position importance (66 > 170 > 143 > 188), validating the approach.

**Step III: Generalized Linear Model (GLM).** Because mutations weren't simply additive — T66Y and H170A each gave ~40% and ~10% improvements alone, but together gave 140% — the team needed a model that could predict non-additive (epistatic) interactions. They applied a Generalized Linear Model, a form of Gaussian regression, to identify which specific amino acid identities at each position contributed synergistically to improved sensor response. GLM generated predictions for small, focused libraries of promising combination mutants, which were synthesized and tested. The best GLM variant, T66Y/F143M/H170A/H188T (named iSeroSnFR0.1), showed a 9-fold increase in fluorescence response and a 2-fold improvement in affinity compared to iSeroSnFR0.0.

This process was repeated for two more rounds, each time at progressively lower serotonin concentrations (500 µM, then 50 µM) to enrich for variants with tighter binding. In total, approximately 16,000 variants were screened across three rounds, interrogating more than 60 positions in the protein. The final sensor, iSeroSnFR (PDB: 6PER), contains 19 mutations relative to the starting scaffold iAChSnFR0.6.

---

## Key Findings

**1. iSeroSnFR is highly selective and sensitive.**

The final sensor has an affinity of 310 ± 30 µM for serotonin in purified protein, improving to ~390 µM in intact cells. Critically, of all the endogenous neurotransmitters, metabolites, and drugs tested, only tryptamine and dopamine produced any detectable response — and even they bound 8- to 16-fold more weakly than serotonin. All common neurotransmitters (ACh, GABA, glutamate, norepinephrine), amino acids, and most clinical drugs produced no response. This pharmacological specificity is essential for any tool intended to measure a single neurotransmitter in the chemically complex brain.

**2. The fluorescence response is large and detectable at physiologically relevant concentrations.**

In purified protein, iSeroSnFR shows up to 800% (ΔF/F₀) maximum fluorescence change. In mammalian HEK293T cells, the signal was even larger — up to 1,700% — likely because the cellular environment stabilizes the sensor's active conformation. Importantly, the sensor reliably detected serotonin concentrations as low as 338 pM on the surface of mammalian cells, which falls within the physiological range of extracellular serotonin in the brain. Signal detection theory analysis (ROC curves and discriminability index d') confirmed near-perfect discrimination between true serotonin responses and buffer noise.

**3. The sensor has millisecond-scale kinetics.**

Using stopped-flow fluorescence experiments (rapidly mixing protein with ligand and measuring the fluorescence change), the researchers found that serotonin binding reaches saturation in 10–40 seconds in purified protein. However, the kinetics showed a more complex, two-component pattern: a very fast initial rise (τ ≈ 0.5–10 ms) followed by a slower rise to saturation (τ ≈ 5–18 s). The researchers interpret this as the sensor existing in two conformational states — an "inactive" form (iSeroSnFR) and a pre-activated "active" form (iSeroSnFR*) — with serotonin binding rapidly to the active form and the slow phase reflecting interconversion between states. Validation using a light-activated caged serotonin molecule confirmed millisecond-resolution detection in live neurons on cell surfaces.

**4. iSeroSnFR detects endogenous serotonin release in brain slices and live mice.**

When delivered via adeno-associated virus (AAV) into mouse brain regions — including the dorsal striatum, medial prefrontal cortex (mPFC), basolateral amygdala (BLA), and orbitofrontal cortex (OFC) — iSeroSnFR reported robust, action-potential-dependent serotonin transients in response to electrical stimulation. These transients were abolished by tetrodotoxin (TTX), confirming they are driven by real neuronal firing. In freely behaving mice, fiber photometry recordings showed that serotonin levels in the mPFC and BLA rose during the cue period of fear conditioning and declined during the footshock, consistent with the known role of serotonin in aversive processing. During social interaction, serotonin increased in OFC, BNST, and BLA, with effects modulated by prior access to voluntary wheel running. Most strikingly, iSeroSnFR tracked serotonin across sleep-wake cycles over many hours, showing highest fluorescence during wakefulness, intermediate during NREM sleep, and lowest during REM sleep — a pattern consistent with the known activity of dorsal raphe serotonergic neurons.

**5. iSeroSnFR enables a pharmacological assay for the human serotonin transporter (hSERT).**

Because iSeroSnFR is soluble and can be expressed inside cells (cytoplasmically), the researchers adapted it for use in the Oscillating Stimulus Transporter Assay (OSTA). By expressing the sensor intracellularly and oscillating extracellular serotonin concentrations, they could measure hSERT-mediated uptake in real time in individual living cells. They confirmed that hSERT requires sodium and chloride for influx, measured sodium's binding affinity (Km ≈ 6.5 mM), and directly quantified the kinetics and dose-dependence of SERT inhibition by cocaine, escitalopram, clomipramine, and vilazodone. They also measured MDMA-driven serotonin efflux, demonstrating a mechanism by which MDMA pushes serotonin out through SERT rather than simply blocking reuptake.

**6. Machine learning consistently outperformed random mutagenesis screening.**

A key methodological validation: in every round of the screening campaign, variants selected from the GLM-focused libraries outperformed variants from the random SSM libraries. The best variant in each round consistently came from the ML-guided library, not the random screen. The average performance of GLM-library variants was statistically significantly higher than SSM variants (p < 0.001). This demonstrates that the ML guidance was genuinely useful — not merely equivalent to screening more random variants.

---

## Significance & Implications

This paper matters on two levels: the sensor itself, and the engineering strategy used to build it.

**iSeroSnFR as a neuroscience tool.** For anyone studying the 5-HT system — including the serotonin 2A receptor (5-HT2A) that sits at the center of your BioChemCore project — iSeroSnFR fills a critical gap. Prior to this work, researchers knew that the 5-HT2A receptor is activated by serotonin, psychedelics, and other ligands, and that different ligands produce different functional outcomes (biased agonism). But they could not measure the actual serotonin concentrations that cells experience in the moment. iSeroSnFR makes it possible to ask: exactly when and how much serotonin arrives at a post-synaptic cell? How does that relate to the downstream signaling measured by other assays? This is directly relevant to understanding how the post-synaptic 5-HT2A receptor integrates fluctuating neurotransmitter input.

The sensor's millisecond temporal resolution is also significant for MD-simulation-adjacent thinking. Molecular dynamics simulations can capture receptor conformational changes over nanosecond-to-microsecond timescales, and NMR or crystallography captures static snapshots. iSeroSnFR bridges those microscopic snapshots to the macroscopic, second-to-minute behavioral timescales of neuroscience — by providing an intermediate, millisecond-resolution readout of the actual chemical signal arriving at receptors.

**The ML-guided engineering pipeline.** The three-step approach — Rosetta for initial reprogramming, Random Forest for identifying important positions, GLM for predicting synergistic combinations — is a generalizable method for engineering binding proteins when no natural scaffold for your target exists. The authors tested the pipeline on firefly luciferase first (as a proof of concept) before applying it to the much harder serotonin problem. The fact that just ~16,000 variants screened across three rounds yielded a >5,000-fold improvement in affinity, complete elimination of ACh binding, and a 3-fold improvement in fluorescence response is remarkable. Purely random mutagenesis of a protein with hundreds of residues would require orders of magnitude more screening to achieve comparable results.

**The SERT pharmacology assay.** The OSTA-iSeroSnFR combination is a direct pharmacological tool relevant to how antidepressants work. The ability to watch SSRIs block SERT transport kinetics in real time, in individual cells, and at clinically relevant nanomolar concentrations, is a genuinely novel capability. It also revealed something unexpected: vilazodone — an antidepressant with reported Ki comparable to clomipramine — caused transport inhibition that did not reverse after 20+ minutes of washout. This irreversibility-like behavior was not anticipated and remains unexplained, illustrating the kind of new observation this assay can generate.

---

## Limitations & Open Questions

**Affinity is weaker than GPCR-based sensors.** The functional affinity of iSeroSnFR in the high-µM range is weaker than the nanomolar affinities of GPCR-based serotonin sensors. The authors acknowledge this, noting that the very large fluorescence response compensates for the weaker affinity by keeping low-concentration events detectable. However, sparse or very brief serotonin release events may still be missed. The authors explicitly call for a future "complementary sensor with higher affinity."

**Unexpected insensitivity to cocaine and citalopram in brain slice.** In the brain slice experiments, bath application of cocaine (10 µM) and citalopram (1 µM) — both SERT blockers that the in vitro assay clearly showed inhibit serotonin reuptake — did not prolong or amplify the electrically evoked serotonin transients detected by iSeroSnFR. The authors offer several possible explanations (fast off-kinetics of iSeroSnFR, diffusion of released 5-HT away from the sensor, artifacts of the slice preparation) but cannot determine which is correct. This is a notable inconsistency between the in vitro pharmacology and the ex vivo brain slice results, and it warrants follow-up.

**Two-component kinetics are not fully explained.** The observation of a fast (0.5–10 ms) and a slow (5–18 s) component in serotonin binding kinetics is intriguing but mechanistically unclear. The authors propose two conformational states but have not directly characterized the structural basis. This matters because the kinetic behavior affects how faithfully the sensor reports dynamic serotonin transients.

**Fiber photometry sacrifices spatial resolution.** For the in vivo experiments, the team used fiber photometry, which measures bulk fluorescence from thousands of cells simultaneously, losing all spatial information. The authors acknowledge that two-photon imaging — which they show works in brain slice — is the path to cell-type-specific and subcellular-resolution imaging. The in vivo fiber photometry data are a proof of concept, not the sensor's full potential.

**No 5-HT2A receptor biology.** This paper engineers and characterizes a sensor for extracellular serotonin detection. It does not address what happens after serotonin binds the 5-HT2A receptor — the conformational changes, G-protein coupling, arrestin recruitment, or downstream signaling cascades that are central to your BioChemCore project. iSeroSnFR is a tool that could be combined with receptor-focused experiments, not a substitute for them.

---

## Key Terms & Concepts

**Periplasmic Binding Protein (PBP):** A class of bacterial proteins that bind small molecules (nutrients, amino acids) by closing around them like a clam shell. They are the structural scaffold for iSeroSnFR — chosen because they are soluble, undergo large conformational changes upon ligand binding (producing big fluorescence signals), don't respond to most mammalian drugs, and can be targeted anywhere in a cell.

**Site-Saturated Mutagenesis (SSM):** A biochemical technique in which every possible amino acid is substituted at a specific position in a protein (or multiple positions simultaneously), and all the resulting variants are screened for a desired property. It exhaustively tests all possibilities at chosen sites but cannot efficiently explore the exponentially large space of multi-site combinations.

**Generalized Linear Model (GLM):** A statistical model that predicts a continuous outcome (here, sensor fluorescence response) from a set of input features (here, amino acid identities at each position). The "linear" part means predictions are additive combinations of feature effects, but the model can also capture interaction terms. In this paper, GLM was critical for identifying which specific amino acid combinations produced synergistic improvements — something SSM alone cannot predict.

**Random Forest (RF):** An ensemble machine learning method that builds many decision trees on random subsets of the data and averages their predictions. Its key advantage here was "feature importance" — it could rank which protein positions most strongly influenced sensor performance, allowing the team to prioritize positions for further mutagenesis rather than randomly sampling.

**iSeroSnFR (intensiometric Serotonin-Sniff-Fluorescent Reporter):** The final genetically encoded fluorescent serotonin sensor produced by this study. It contains 19 mutations relative to the ancestral acetylcholine sensor, has a 5-HT affinity of ~310 µM, and produces up to 800% fluorescence change (and 1,700% in cells), enabling optical detection of serotonin in neurons, brain slices, and freely behaving animals.

**hSERT (human Serotonin Transporter):** The membrane protein that removes serotonin from the synapse by pumping it back into the presynaptic neuron. It is the primary target of SSRI antidepressants. Because iSeroSnFR can be expressed cytoplasmically and is not itself affected by most drugs targeting SERT, it was ideal for building a real-time functional assay of SERT activity.

**Oscillating Stimulus Transporter Assay (OSTA):** An assay design in which the extracellular concentration of a transporter substrate (here, serotonin) is oscillated between high and low values while an intracellular sensor reports how much is being imported. The oscillation separates the transport signal from baseline drift, making measurements more precise. Combined with iSeroSnFR, this enabled real-time, single-cell quantification of SERT function and drug inhibition kinetics.
