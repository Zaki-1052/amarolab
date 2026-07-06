# Olson 2022 — Biochemical Mechanisms Underlying Psychedelic-Induced Neuroplasticity

**Citation:** Olson, D. E. (2022). Biochemical Mechanisms Underlying Psychedelic-Induced Neuroplasticity. *Biochemistry*, 61(3), 127–136. https://doi.org/10.1021/acs.biochem.1c00812

---

## One-Sentence Takeaway

Psychedelics promote long-lasting structural and functional neuroplasticity in the prefrontal cortex primarily through the 5-HT2A receptor, but the exact downstream signaling cascade linking receptor activation to neuron growth remains unresolved — and answering that question is essential for engineering safer, non-hallucinogenic therapeutics.

---

## Background & Motivation

Depression, PTSD, and addiction share a striking anatomical feature: the neurons of the prefrontal cortex (PFC) — a brain region governing mood, fear regulation, and decision-making — become physically smaller and less connected. This is not a metaphor. Under chronic stress, PFC neurons actually lose dendritic spines (the tiny protrusions that form synaptic connections with neighboring neurons), and their dendritic trees retract. The PFC becomes literally atrophied, and dysfunctional circuits controlling mood and behavior follow. This cortical atrophy is a convergent pathological mechanism underlying several distinct neuropsychiatric conditions, which is why compounds capable of reversing it have such broad therapeutic potential.

What makes psychedelics remarkable is not just that they produce powerful acute subjective effects — it is that their *behavioral* benefits in clinical settings (reduced depression, reduced PTSD symptoms, decreased addiction relapse) appear after only one or a few doses and persist long after the drugs have been cleared from the body. Traditional antidepressants must be taken every day and work, in part, through slow and incomplete compensatory mechanisms. Something else is going on with psychedelics.

One compelling hypothesis, and the focus of this review, is that psychedelics promote **structural and functional neuroplasticity** in the PFC — that is, they physically rebuild the atrophied neurons and restore synaptic connectivity. Olson frames psychedelics as belonging to a broader chemical class he calls **psychoplastogens**: compounds that produce robust, lasting growth in cortical neurons following a single administration. The paper reviews what is currently known about the molecular signaling machinery that gets activated when psychedelics hit the brain, and honestly maps out where the field still has large gaps.

This review is directly relevant to your BioChemCore work because the primary molecular target of serotonergic psychedelics — the 5-HT2A receptor — is the exact post-synaptic CNS membrane protein you are simulating. Understanding its signaling biology gives critical biological meaning to the structural and dynamic features you will observe in MD trajectories.

---

## Approach & Methods

This is a **review paper**, meaning Olson synthesizes and critically evaluates existing experimental literature rather than presenting new primary data. He draws on a combination of his own lab's findings (notably the Ly et al. 2018 *Cell Reports* study and follow-up work) and a wide body of published research from other groups.

The body of evidence he reviews spans multiple experimental systems and scales:

- **In vitro neuronal cultures** — rat embryonic cortical neurons treated with psychedelics and assessed for neurite outgrowth, spinogenesis (spine formation), and synaptogenesis
- **In vivo rodent studies** — mice and rats given single systemic doses, with brain tissue examined weeks later for dendritic spine density and functional synaptic changes
- **Two-photon live imaging** — longitudinal imaging in living mice to track spine formation and elimination in real time
- **Genetic knockouts** — mice lacking the 5-HT2A receptor or specific downstream signaling components, to establish which genes are required for psychedelic effects
- **Pharmacological blockade** — using receptor antagonists and selective inhibitors to dissect which pathways are necessary
- **Transcriptomics, proteomics, and epigenomics** — measuring gene expression, protein phosphorylation, and chromatin remodeling after psychedelic treatment
- **Fluorescent biosensors (psychLight)** — a novel engineered GPCR sensor that fuses a circularly permuted GFP to the third intracellular loop of the 5-HT2A receptor, allowing real-time optical readout of receptor conformation

The review is organized around a central unresolved question: which 5-HT2A receptor signaling cascades are actually responsible for promoting neuronal growth, as opposed to those responsible for the hallucinogenic experience?

---

## Key Findings

### 1. Psychedelics promote robust, long-lasting structural neuroplasticity

The most foundational finding, from Olson's own lab (Ly et al., 2018), is that psychedelic compounds from chemically diverse families — tryptamines (DMT), ergolines (LSD), and phenethylamines (DOI) — all robustly promote neuritogenesis (growth of neuronal processes), spinogenesis (formation of dendritic spines), and synaptogenesis (formation of new synaptic connections) in cultured rat cortical neurons. Serotonin itself cannot do this, and D-amphetamine cannot do this, establishing that the effect is pharmacologically specific to psychedelics rather than a generic stimulatory response.

In vivo, a single dose of DMT increases dendritic spine density in the PFC that persists long after the drug is gone. Psilocybin induces rapid, persistent growth of dendritic spines in the frontal cortex of mice for at least a month after a single dose. These structural changes are accompanied by functional changes: increased amplitude and frequency of spontaneous excitatory postsynaptic currents (sEPSCs), indicating that the new spines are forming active synapses. Psilocybin also increases the density of a presynaptic marker (SV2A), suggesting new synaptic contacts are being built on both sides of the synapse.

### 2. The 5-HT2A receptor is required

All of the psychoplastogenic effects of serotonergic psychedelics are blocked or strongly attenuated by ketanserin (a 5-HT2A/2C antagonist) in vitro, and by genetic knockout of the 5-HT2A receptor in vivo. This establishes 5-HT2A receptor activation as necessary for these effects. Crucially, this is true for both the hallucinogenic head-twitch response (an animal proxy for hallucinations) and for neuroplasticity, which initially suggested the two phenomena might share the same receptor trigger.

However, Olson emphasizes important caveats. Ketanserin incompletely blocks psilocybin's plasticity effects in vivo, likely because ketanserin has poor brain penetration and only occupies ~30% of cortical 5-HT2A receptors at the doses used. The parallel between hallucinogenicity and psychoplastogenicity at the receptor level does not mean the downstream pathways are identical.

### 3. Hallucinogenicity and psychoplastogenicity can be dissociated

This is arguably the most therapeutically important finding reviewed. The compound tabernanthalog (TBG) is a non-hallucinogenic structural analog of ibogaine that does not produce a head-twitch response in rodents (the proxy for hallucination) but still robustly promotes neuroplasticity in vitro and in vivo. A single dose of TBG rescued dendritic spines lost after chronic stress and normalized cortical neuron activity. This demonstrates that the hallucinogenic and plasticity-promoting properties of psychedelics, while both requiring 5-HT2A, diverge at some downstream point in the signaling cascade. Non-hallucinogenic psychoplastogens from multiple chemical scaffolds have now been identified, including analogs from Olson's own structure-activity relationship work on DMT (producing compounds like AAZ).

### 4. The downstream signaling chain involves BDNF, TrkB, AMPA receptors, and mTOR — but is not fully resolved

The prevailing hypothesis for how 5-HT2A activation leads to neuron growth goes like this: psychedelic binding to 5-HT2A triggers a **glutamate burst** in the cortex (excitatory neurotransmitter release from nearby presynaptic terminals). This glutamate activates **AMPA receptors** on the postsynaptic neuron, which stimulates secretion of **BDNF** (brain-derived neurotrophic factor, a protein that promotes neuronal growth). BDNF binds to its receptor **TrkB**, which activates **mTOR** (a master growth-regulating kinase). mTOR increases production of plasticity-related proteins, and also promotes more BDNF release, creating a self-sustaining feedback loop. The result: lasting neuron growth even after the drug is gone.

Supporting this: blocking AMPA receptors, TrkB, or mTOR inhibits psychoplastogenic effects in cultured neurons. BDNF-KO mice lose ketamine's antidepressant effects, and anti-BDNF antibodies block scopolamine's effects. Psychedelics increase BDNF gene expression in the cortex, and this is blocked by 5-HT2A antagonists.

However, Olson is explicit that this pathway has not been rigorously demonstrated for serotonergic psychedelics the way it has for ketamine. The necessity of a large glutamate burst for psychedelic-induced plasticity is questioned by the fact that non-hallucinogenic psychoplastogens (which presumably do not trigger glutamate bursts the same way) produce equivalent plasticity. BDNF necessity has not been directly tested with conditional knockouts for serotonergic psychedelics.

### 5. Canonical Gq/PLC signaling is necessary but not sufficient for psychoplastogenicity

The 5-HT2A receptor canonically couples to the Gq alpha subunit, which activates **phospholipase C (PLC)**, producing **IP3** and raising intracellular calcium. This pathway clearly contributes: blocking PLC abolishes c-Fos expression (an immediate early gene used as a neuroplasticity marker) after psychedelic treatment. Psychedelics also increase expression of BDNF and neuroplasticity-associated immediate early genes (c-Fos, arc, egr-1) through 5-HT2A, requiring CaMKII and MAPK activation downstream.

But Gq/PLC activation alone is not the answer, because many non-hallucinogenic 5-HT2A ligands also activate PLC (e.g., lisuride, 6-F-DET, TBG) but some of these are poor or failed psychoplastogens, and full agonist serotonin activates PLC but cannot promote neuroplasticity. The receptor can also engage Gi, G12/13, phospholipase A2, beta-arrestin, ERK, JAK2, GSK3beta, and others. Cellular context (which scaffolding proteins are present, which heterodimers form) determines which pathways dominate.

### 6. The psychLight biosensor separates receptor conformational states for hallucinogens vs. non-hallucinogens

Olson's lab engineered a fluorescent 5-HT2A receptor biosensor called **psychLight** by inserting a circularly permuted GFP into the third intracellular loop (the loop connecting TM5 and TM6). This is the same region that changes conformation dramatically upon GPCR activation — the G protein-coupling interface. When expressed in HEK293T cells, psychLight fluorescence correlates strongly with the hallucinogenic potency of compounds across a chemically diverse set of ligands. Non-hallucinogenic 5-HT2A agonists like TBG and 6-F-DET act as *inverse agonists* of psychLight (they decrease fluorescence, stabilizing a different receptor conformation) even though they activate PLC. This is powerful evidence for **functional selectivity** (also called biased agonism) at 5-HT2A — different ligands stabilize distinct receptor conformations that preferentially activate different downstream pathways. The current version of psychLight predicts hallucinogenicity but cannot yet predict psychoplastogenicity.

### 7. Species differences in the 5-HT2A receptor are pharmacologically meaningful

Human and rodent 5-HT2A receptors differ at a key position in transmembrane domain V: humans have a serine at residue 242 while rodents have an alanine. This single amino acid difference allows certain ligands to form a hydrogen bond with the human receptor that they cannot form with the rodent receptor, significantly altering binding potency and kinetics. The rat and human receptors also differ in their C-terminal sequences, affecting receptor trafficking, internalization rates, and GRK2/beta-arrestin-2 interactions. This is a direct caution for anyone building MD simulations: results from rodent receptor structures may not fully translate to predictions about human pharmacology.

---

## Significance & Implications

This paper is a foundational orienting document for anyone studying the 5-HT2A receptor in the context of psychiatric drug development. For your BioChemCore project specifically, it provides the biological rationale for why the 5-HT2A receptor is one of the most consequential drug targets in the nervous system right now.

The concept of **functional selectivity (biased agonism)** is the central mechanistic puzzle of the paper and is directly relevant to your simulation goals. Different ligands stabilize different conformational states of the 5-HT2A receptor, and those different conformations activate different intracellular signaling pathways — some leading to hallucinations, some to neuroplasticity, and some to neither. MD simulations are one of the most powerful tools available for understanding *how* different ligands induce different receptor conformations at the atomic level. The paper implicitly motivates exactly the kind of structural dynamics work that BioChemCore is designed to train you in.

The psychLight biosensor finding is particularly exciting from a structural biology lens: inserting a fluorescent sensor into the third intracellular loop (ICL3) and observing that it discriminates hallucinogenic from non-hallucinogenic conformations tells you that ICL3 is a key readout region for biased agonism at this receptor. In your MD simulations, tracking ICL3 dynamics (RMSD, RMSF, distance metrics) could be a meaningful analysis target.

The broader translational picture is that the field is racing to develop non-hallucinogenic psychoplastogens for psychiatric treatment. The dissociation of hallucination from neuroplasticity means it should be possible to design drugs that rebuild broken neural circuits without the perceptual and psychological risks of classical psychedelics. Structure-based drug design, enabled by MD simulations and cryo-EM structures of the receptor in active and inactive states, is identified as the path forward.

---

## Limitations & Open Questions

Olson is commendably honest about the gaps. The paper identifies the following as unresolved:

- **Is a large glutamate burst required?** The evidence is circumstantial, and non-hallucinogenic psychoplastogens challenge the assumption.
- **Is BDNF actually essential for psychedelic-induced plasticity?** Demonstrated for ketamine and scopolamine but not yet tested with BDNF conditional knockouts for serotonergic psychedelics.
- **Which specific 5-HT2A signaling pathway is causally responsible for neuron growth?** None of the candidates (Gq, Gi, G12/13, beta-arrestin, PLA2) has been definitively established.
- **What is the role of beta-arrestin?** Beta-arrestin signaling is important for 5-HT2A ligand-directed effects in vivo, but its role in structural plasticity is entirely unknown.
- **Does cell-type selectivity matter?** 5-HT2A receptors are expressed on many neuron types and non-neuronal cells. Whether psychoplastogenic effects are restricted to specific cell populations is unknown.
- **Do heterodimers change the picture?** The 5-HT2A-mGlu2 heterodimer has received significant attention, but non-hallucinogenic psychoplastogens do not appear to activate this complex, leaving its role in plasticity unclear.
- **Species translation:** Most preclinical data are from rodents, but key residue differences between human and rodent 5-HT2A receptors mean that mechanistic conclusions require validation in human-relevant systems.
- **Epigenomics comparison across drug classes:** A single DOI dose causes sustained epigenomic changes at enhancer regions of neuroplasticity genes in mice. Whether psilocybin and non-hallucinogenic psychoplastogens produce similar or distinct epigenomic profiles has not been directly compared.

One methodological note worth flagging: ketanserin, the primary pharmacological tool used to implicate 5-HT2A receptors in psychedelic effects, has poor brain penetration. Olson acknowledges this directly. Conclusions drawn from in vivo ketanserin blockade studies should be interpreted with appropriate caution.

---

## Key Terms & Concepts

**Psychoplastogen** — A compound that promotes robust, rapid, and lasting structural and functional neuroplasticity in cortical neurons, typically with efficacy after a single dose; broader than "psychedelic" because it includes non-hallucinogenic compounds with the same plasticity-promoting effects.

**Spinogenesis / Dendritogenesis / Synaptogenesis** — The growth of dendritic spines, dendritic branches, and synaptic connections, respectively; together these represent structural neuroplasticity, and their loss underlies cortical atrophy in depression, PTSD, and addiction.

**Functional selectivity (biased agonism)** — The phenomenon where different ligands binding the same receptor stabilize different receptor conformations, leading to preferential activation of different downstream signaling pathways; critical concept explaining why some 5-HT2A agonists hallucinate, others promote plasticity, and others do neither.

**mTOR (mechanistic target of rapamycin)** — A central cellular kinase that acts as a master regulator of protein synthesis and cell growth; activated downstream of TrkB/BDNF signaling, and its activation is required for psychoplastogen-induced neuronal growth.

**BDNF / TrkB** — Brain-derived neurotrophic factor (BDNF) is a secreted protein that promotes neuron growth and survival; TrkB is its receptor tyrosine kinase. BDNF-TrkB signaling is the key link between synaptic activity and long-term structural changes in neurons.

**psychLight** — A genetically encoded fluorescent biosensor constructed by inserting a circularly permuted GFP into the third intracellular loop of the 5-HT2A receptor; its fluorescence signal correlates with hallucinogenic potency and distinguishes receptor conformational states induced by hallucinogenic versus non-hallucinogenic ligands.

**Head-twitch response (HTR)** — A rapid, involuntary head movement in rodents that is a well-validated proxy for the hallucinogenic potential of 5-HT2A receptor agonists in humans; genetically and pharmacologically validated as 5-HT2A-dependent, and used to screen compounds for hallucinogenic liability.

---

*Summary prepared for BioChemCore context: 5-HT2A receptor MD simulation program. Paper filed at `/Users/zakiralibhai/Documents/papers/Olson 2022 - Biochemical Mechanisms Underlying Psychedelic-Induced Neuroplasticity.pdf`*
