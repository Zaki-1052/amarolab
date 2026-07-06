# Aarrestad et al. 2025 — Summary
**Citation:** Aarrestad, I. K., Cameron, L. P., Fenton, E. M., et al. (2025). The psychoplastogen tabernanthalog induces neuroplasticity without proximate immediate early gene activation. *Nature Neuroscience*, 28, 1919–1931. https://doi.org/10.1038/s41593-025-02021-1

---

## One-Sentence Takeaway

Tabernanthalog (TBG), a nonhallucinogenic psychoplastogen, promotes cortical neuroplasticity and sustained antidepressant-like effects through the same 5-HT2A receptor / TrkB / mTOR / AMPA receptor pathway as classic psychedelics, but does so without triggering a glutamate burst or immediate early gene (IEG) activation — demonstrating that those two hallmarks of classic psychedelics are not required for structural plasticity.

---

## Background & Motivation

### The Problem: Cortical Atrophy in Neuropsychiatric Disease

Cortical atrophy — the shrinking and pruning of neurons, especially in the prefrontal cortex (PFC) — is a hallmark of depression, PTSD, and addiction. Neurons lose dendritic spines (the tiny protrusions on dendrites where synapses form), and this structural loss correlates with functional deficits: impaired mood regulation, emotional processing, and cognitive flexibility.

Classic psychedelics like psilocybin (found in magic mushrooms), LSD, and 5-methoxy-N,N-dimethyltryptamine (5-MeO-DMT) can reverse this atrophy rapidly. A single dose promotes the regrowth of dendritic spines in rodent PFC and produces sustained antidepressant-like effects lasting days to weeks — effects that appear to exceed those of ketamine, another rapid-acting antidepressant. Recent clinical trials have confirmed that psilocybin-assisted therapy produces robust, lasting antidepressant effects in humans.

### The Catch: Hallucinogenic Effects Limit Clinical Use

The same receptors that seem to drive neuroplasticity — primarily the 5-HT2A serotonin receptor (5-HT2AR) — also mediate the hallucinogenic effects of psychedelics. Profound perceptual distortions require clinical supervision, exclude patients with psychosis risk, and create scalability barriers. This has motivated the development of **psychoplastogens**: compounds that preserve the neuroplasticity-promoting properties of psychedelics while eliminating or reducing the hallucinogenic effects.

### Enter Tabernanthalog (TBG)

TBG is a synthetic, nonhallucinogenic analog of ibogaine (the psychoactive compound in the iboga plant) developed by the Olson lab at UC Davis. It had previously been shown to promote cortical spine growth and produce antidepressant-like and anti-addictive behavioral effects in rodents after a single dose. However, the *mechanism* of TBG-induced neuroplasticity was unclear. Two specific questions drove this paper:

1. Does TBG require 5-HT2AR activation to promote neuroplasticity? (Contested in the literature — some reports suggested psychoplastogens could work independently of 5-HT2ARs, perhaps through TrkB, the receptor for BDNF.)
2. Do psychedelics promote neuroplasticity *because* they trigger a glutamate burst and IEG expression — and does TBG need to do the same?

These questions matter both for mechanistic understanding and for drug design: if IEG induction is truly necessary for plasticity, then a drug that avoids it cannot be therapeutically effective. This paper argues it is not necessary.

---

## Approach & Methods

The researchers took a multi-layered strategy combining pharmacological manipulation, genetic knockout models, fiber photometry, two-photon calcium imaging, single-nucleus RNA sequencing, and whole-brain immunohistochemistry. This diversity of approaches is a strength of the paper — the core claims are supported by convergent evidence across methods.

### Pharmacological and Genetic Dissection of the 5-HT2AR Requirement

To test whether 5-HT2ARs are required, they used **5-HT2AR knockout (KO) mice** — animals genetically engineered to lack this receptor entirely. They administered TBG (50 mg/kg, intraperitoneal) to both wild-type and KO animals, then measured:
- Dendritic spine density in layer 5 pyramidal neurons of the medial PFC using Golgi-Cox staining (a classical method that silver-stains neurons to reveal their full morphology)
- Spontaneous excitatory postsynaptic currents (sEPSCs) via ex vivo electrophysiology — a measure of functional synaptic activity
- Antidepressant-like behavior using the Tail Suspension Test (TST), where decreased immobility indicates antidepressant effect

They also used **ketanserin**, a pharmacological 5-HT2AR antagonist, to block receptor activation in wild-type animals, and compared TBG to 5-MeO as a positive control classic psychedelic.

### Causal Link Between Spinogenesis and Behavioral Effect

To prove that the spines TBG grows are *causally required* for the antidepressant behavior (not just correlated), they used an elegant optogenetic approach. They injected a viral vector encoding a **photoactivatable Rac1 (AS-PaRac1)** construct targeted to activated synapses into the bilateral PFC. AS-PaRac1, when activated by blue light (465 nm), causes rapid shrinkage and elimination of dendritic spines. By administering TBG on Day 1 and then shining blue light 12 hours later — at the time of new spine peak — they could selectively ablate TBG-induced spines. The TST was then measured 24 hours after TBG. If spines caused the behavior, photoablation should eliminate the antidepressant effect.

### Glutamate Burst Measurement: Fiber Photometry

Classic psychedelics are known to trigger a rapid, large increase in extracellular glutamate in the PFC. To measure glutamate release in real time in freely moving mice, the authors used **fiber photometry** with the genetically encoded glutamate sensor iGluSnFR3 (intensiometric Glutamate-Sensing Fluorescent Reporter 3), expressed via viral injection into the PFC and detected through an implanted fiber-optic probe. This allowed them to directly compare glutamate dynamics following 5-MeO versus TBG.

### Calcium Imaging: Two-Photon and Fiber Photometry

To examine neuronal activation at both the population and single-cell level, they used two calcium biosensors. **CaMKII-GCaMP6f** was used for bulk fiber photometry (measuring the aggregate calcium signal from a population of excitatory neurons), and a GRIN lens was implanted for **two-photon imaging** of individual neurons, enabling longitudinal tracking of the same cells across weeks.

### IEG Quantification: Three Convergent Approaches

To measure IEG (immediate early gene) induction — genes like c-Fos and NPAS4 that are rapidly transcribed when neurons fire intensely — the researchers used:
1. **Confocal immunohistochemistry** for c-Fos protein across the brain
2. **Light-sheet microscopy** combined with a whole-brain atlas, enabling voxel-wise comparisons of c-Fos and NPAS4 across hundreds of brain regions in 3D
3. **Single-nucleus RNA sequencing (snRNA-seq)** on PFC tissue harvested 1 hour after drug administration, using the BICCN cell atlas to identify cell types and the NEUROeSTIMator machine learning tool to score IEG activity at the individual cell level

### Behavioral Comparison with SSRIs and Psychedelics

To position TBG relative to other antidepressants, they used the **SmartCube** system — a high-throughput behavioral phenotyping platform that monitors spontaneous and evoked behaviors and clusters drugs by their signatures — and also conducted microdialysis (measuring extracellular neurotransmitter levels in the PFC of behaving rats) and PET imaging in pigs using the radiotracer [13C]Cimbi-36 to quantify brain 5-HT2AR occupancy.

---

## Key Findings

### 1. TBG Requires 5-HT2AR Activation for All Neuroplastic and Behavioral Effects

In 5-HT2AR KO mice, TBG completely failed to increase spine density in the PFC — the spines simply did not grow. sEPSC frequency and amplitude also showed no increase. And in the TST, TBG had no antidepressant effect in KO animals, while it significantly reduced immobility time in wild-type littermates. The same pattern held with ketanserin pharmacological blockade. This establishes that 5-HT2AR activation is not just correlated with TBG's effects — it is mechanistically necessary.

This is important because some prior literature had suggested psychoplastogens might work through TrkB (the BDNF receptor) independent of 5-HT2ARs. The paper found TBG is neither an agonist of TrkB nor a positive allosteric modulator of TrkB, ruling out that alternative mechanism for this compound. Downstream of 5-HT2AR, both TBG and classic psychedelics required mTOR, TrkB (likely activated downstream of 5-HT2AR via intracellular signaling cascades), and AMPA receptor activation to promote dendritogenesis in culture — the same pathway is used by both hallucinogenic and nonhallucinogenic compounds.

### 2. Cortical Spinogenesis Is Causally Required for TBG's Antidepressant Effect

The AS-PaRac1 photoablation experiment showed that mice given TBG and then had their new spines ablated with blue light did NOT show antidepressant effects in the TST. Mice that received TBG without photoablation showed the expected decrease in immobility. Importantly, ablating a random set of dendritic spines (using a non-synapse-targeted construct) had no effect on behavior, confirming it was specifically the TBG-induced new spines — not generalized spine disruption — that drove the behavior. This mirrors previous causal evidence for ketamine-induced spinogenesis in the FST.

### 3. TBG Does Not Induce a Glutamate Burst

5-MeO produced large, discrete, high-amplitude glutamate transients in the mPFC, visible as sharp spikes in the iGluSnFR3 photometry signal. TBG produced no such transients — glutamate event frequency was actually *decreased* relative to vehicle (consistent with TBG's partial agonism at 5-HT2AR, since full agonism is thought to drive localized epileptiform cortical activity). This was replicated by microdialysis in rats, where systemic TBG did not increase extracellular glutamate levels in the PFC even at doses that produced antidepressant effects. The lack of glutamate burst means TBG also would not be expected to activate AMPA receptors acutely — yet its neuroplasticity is still AMPA-dependent (likely via tonic baseline AMPA signaling rather than acute glutamate flooding).

### 4. TBG Does Not Activate IEGs in the PFC

This is the headline finding the title refers to. IEGs — including c-Fos, NPAS4, Arc, and others — are transcription factors and activity-dependent genes that are robustly expressed within minutes to an hour of strong neuronal activation. They have long been used as markers of neuronal plasticity and are sometimes called "plasticity-related genes." Psychedelics like 5-MeO strongly increased both c-Fos and NPAS4 expression across the cortex, particularly in layers 2/3 and 5 of the mPFC. TBG had no significant effect on c-Fos or NPAS4 at the same FDR threshold (q < 0.05 and q < 0.005 respectively).

The snRNA-seq data confirmed this at cellular resolution. At 1 hour post-administration, 5-MeO significantly upregulated IEG module scores in L4/5 intratelencephalic (IT) glutamatergic neurons — the same excitatory cortical cell populations that express Htr2a (the gene encoding 5-HT2AR). Classical IEGs including Tiparp, Fosb2, Nr4a2, and Arc were strongly induced. TBG produced no IEG induction above vehicle in any cluster. This was consistent across both female and male animals and across biological replicates.

Critically, this also extended to two other nonhallucinogenic psychoplastogens tested: BOL-148 (2-Br-LSD) and AAZ-A-154 — neither increased c-Fos in the PFC. This suggests the absence of IEG induction may be a general feature of nonhallucinogenic psychoplastogens, not specific to TBG.

### 5. TBG Occupies 5-HT2ARs In Vivo and Partially Blocks Psychedelic Effects

PET imaging in pigs confirmed that TBG engages brain 5-HT2ARs in vivo, with dose-dependent receptor occupancy (IC50 of 550 ng/mL plasma concentration; occupancies exceeding 46% at therapeutic-range doses). Behaviorally, TBG pretreatment in mice completely blocked 5-MeO-induced head-twitch responses (a rodent proxy for hallucinogenic activity), consistent with competitive partial agonism at 5-HT2ARs. This is the in vivo confirmation that TBG is acting as a partial agonist — not just in binding assays.

### 6. Calcium Activation Pattern Differs Between TBG and 5-MeO Despite Overlap

Both drugs increased cytosolic calcium in mPFC excitatory neurons. However, 5-MeO increased the prominence (height) of calcium transient peaks, while TBG primarily increased peak width (duration) without the dramatic amplitude spikes. Two-photon imaging showed that 76% of neurons were concordant in their response direction to TBG and 5-MeO (cells activated by one tended to be activated by the other), and the proportions of activated versus inhibited cells were statistically indistinguishable — consistent with both drugs targeting the same cellular population. However, the magnitude of responses differed substantially and stochastically, suggesting the different activity signatures are not due to fundamentally different cell populations being recruited.

### 7. TBG's Behavioral Profile Aligns More with Psychedelics than SSRIs

SmartCube analysis placed TBG's behavioral signature closer to psilocybin and psilocin than to SSRIs. TBG, like ketamine, abolished social interaction deficits in mice exposed to chronic social defeat stress — an effect not seen with the SSRI fluoxetine. TBG also produced antidepressant-like effects in the Forced Swim Test (FST) within 24 hours and lasting at least 7 days in rats. Monoamine oxidase A (MAO-A), NET, and SERT inhibition by TBG was confirmed but at potencies 2-4 orders of magnitude lower than standard inhibitors, so these off-target effects are unlikely to explain its antidepressant effects at the doses used.

---

## Significance & Implications

### Rethinking the Glutamate Burst Hypothesis

A dominant model of how psychedelics work — the "AMPA receptor surge" model — proposes that 5-HT2AR activation triggers a rapid glutamate burst in the PFC, which activates AMPA receptors, which then activates TrkB and mTOR signaling to drive dendritic spine growth. This paper shows TBG can activate the downstream portion of this pathway (TrkB, mTOR, AMPA) and produce the same plastic outcome *without* triggering the glutamate burst. This forces a revision of the model: either the basal level of glutamatergic tone is sufficient to activate AMPA receptors downstream of 5-HT2AR, or there is a 5-HT2AR-to-TrkB/mTOR signal route that does not require acute glutamate elevation.

The authors suggest that full 5-HT2AR agonists (like 5-MeO) drive localized epileptiform cortical activity that releases glutamate in large bursts — and that this may actually be more related to IEG induction and hallucinogenic effects than to plasticity per se. TBG, as a partial agonist, activates 5-HT2AR enough to initiate the plasticity cascade but not enough to drive the excessive glutamate release.

### IEG Induction Is Not Required for Structural Plasticity

This is perhaps the most surprising conceptual contribution. The assumption that "plasticity-related gene expression" (i.e., IEGs) is required for structural plasticity has been widespread. This paper provides direct evidence against it: TBG promotes robust, behaviorally meaningful cortical spine growth without any detectable IEG induction at 1 hour post-dosing. Other nonhallucinogenic psychoplastogens (BOL-148, AAZ-A-154) also fail to induce c-Fos. The authors acknowledge that IEG expression may still be important for other forms of neuroplasticity, but it does not appear to be a required upstream trigger for psychoplastogen-induced spinogenesis.

### Design Principle for Next-Generation Psychoplastogens

This paper suggests a design framework: compounds that are partial agonists at 5-HT2ARs may be the sweet spot — activating the receptor enough to drive the plasticity-promoting intracellular cascade (via Gq, mTOR, TrkB, AMPA) while staying below the threshold needed for the glutamate burst that drives hallucinations and IEG induction. Low or absent proximate IEG response may serve as a biomarker for low hallucinogenic potential. This has direct implications for medicinal chemistry efforts to develop safer psychedelic-adjacent therapeutics.

### Relevance to BioChemCore / 5-HT2AR Simulation Work

This paper is directly relevant to your MD simulation work on the 5-HT2AR. The key pharmacological distinction being made here is between **full agonism** (5-MeO, psilocin — driving maximal receptor activation, glutamate bursts, IEG induction, hallucinogenesis) and **partial agonism** (TBG — submaximal receptor activation, no glutamate burst, preserved plasticity signaling). This distinction is a conformational one at the receptor level: full versus partial agonists stabilize different active-state conformations of GPCRs, which in turn couple differently to downstream G proteins and beta-arrestin pathways. The paper confirms via BRET-based biosensors that TBG is a balanced partial agonist at both Gq and beta-arrestin pathways.

When you simulate 5-HT2AR, the conformational dynamics distinguishing partial from full agonist-bound states are something you could look for in your trajectory analysis. The TM6 outward movement and TM5/TM3 rearrangements associated with full G-protein activation differ from those of partial agonist-bound states. Additionally, the intracellular signaling cascade described here — Gq → IP3 → intracellular Ca2+ → CaMKII → mTOR / TrkB transactivation → AMPA receptor upregulation — maps directly onto the Gq-coupled signaling mode of 5-HT2AR, which is the same coupling your simulation will represent when building the receptor in a realistic membrane environment.

---

## Limitations & Open Questions

**Rodent-only mechanistic data.** The core mechanistic findings (spine growth, KO rescue, glutamate photometry, IEG sequencing) are all in mice or rats. While PET occupancy data in pigs provide some translational bridge, direct evidence that TBG produces the same mechanistic profile in human neurons or human brain is lacking. Human neurons in the PFC have substantially different densities and distributions of 5-HT2ARs than rodent neurons.

**Temporal window for IEG is limited.** The snRNA-seq and immunohistochemistry were performed at 1 hour post-dosing. IEGs peak and decline rapidly — some reach peak expression within 30 minutes and return to baseline by 3-4 hours. The paper's conclusion is that TBG does not induce *proximate* IEG activation (the title explicitly says this). Whether TBG might induce delayed IEG expression at a later timepoint (e.g., 4-6 hours) is not addressed.

**Mechanism of spine stabilization is unexplored.** The paper shows TBG induces new spines and that ablating them eliminates the antidepressant effect. But the molecular mechanism of how the new spines are maintained over days in the absence of an IEG transcriptional program is unclear. IEGs like Arc are thought to be important for synaptic tagging and long-term potentiation consolidation — how does TBG-induced spine growth persist without this?

**Partial agonism as a necessary versus sufficient condition.** The paper shows TBG (a partial agonist) works without IEGs. It does not systematically show that all partial agonists work this way, or that full agonists cannot also be designed to spare IEGs. The design principle implied (partial agonism = no hallucination = no IEG) is a working hypothesis that needs broader structure-activity testing.

**No human data on TBG.** The compound has not been tested in humans yet. Its hallucinogenic potential can only be inferred from rodent and pig data. Clinical translation will require first-in-human studies to confirm absence of subjective psychedelic effects.

---

## Key Terms & Concepts

**Psychoplastogen:** A drug that promotes structural neuroplasticity (especially dendritic spine growth in the PFC) without producing hallucinogenic effects. The goal is to capture the antidepressant and neurotropic benefits of psychedelics in a clinically scalable, safer form.

**5-HT2A Receptor (5-HT2AR):** The serotonin type 2A receptor, a Gq-coupled GPCR expressed on cortical pyramidal neurons. It is the primary molecular target of classic psychedelics and, as this paper shows, is also required for TBG's neuroplastogenic effects. Full agonism drives hallucinations; partial agonism drives plasticity without hallucinogenesis.

**Dendritic Spinogenesis:** The process of growing new dendritic spines — the small protrusions on neuronal dendrites that form the postsynaptic side of excitatory synapses. More spines generally means more synaptic connectivity. Their loss is associated with depression; their regrowth correlates with antidepressant effect.

**Immediate Early Genes (IEGs):** Genes that are rapidly and transiently transcribed in response to strong neuronal activity, without requiring new protein synthesis. Examples include c-Fos, NPAS4, Arc, and Nr4a1. They are used as markers of neuronal activation and have historically been assumed to be required for experience-dependent synaptic plasticity.

**Partial Agonist:** A drug that binds a receptor and activates it, but produces a submaximal response compared to the endogenous ligand or a full agonist, even at saturating concentrations. TBG is a partial agonist at 5-HT2ARs — it activates the receptor enough to trigger downstream plasticity signaling but not enough to drive the full hallucinogenic cascade.

**mTOR (mechanistic Target of Rapamycin):** A serine/threonine kinase that integrates upstream growth signals and promotes protein synthesis and cell growth. Downstream of 5-HT2AR activation, mTOR drives the synthesis of synaptic proteins needed to build and stabilize new dendritic spines. Rapamycin (an mTOR inhibitor) blocks psychoplastogen-induced spine growth.

**TrkB:** The high-affinity receptor for BDNF (Brain-Derived Neurotrophic Factor). Activation of TrkB triggers ERK and PI3K/Akt signaling cascades that support neuronal survival and synapse formation. TrkB is activated downstream of 5-HT2AR in the psychoplastogen plasticity cascade, though TBG itself does not directly bind or allosterically modulate TrkB.
