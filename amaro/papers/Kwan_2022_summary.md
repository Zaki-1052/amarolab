# Kwan et al. (2022) — The Neural Basis of Psychedelic Action

**Citation:** Kwan AC, Olson DE, Preller KH, Roth BL. *Nature Neuroscience* 25(11): 1407–1419. doi:10.1038/s41593-022-01177-4

---

## 1. One-Sentence Takeaway

Psychedelics produce their profound perceptual and potentially therapeutic effects primarily through agonism at the 5-HT2A serotonin receptor, which triggers downstream molecular signaling, reshapes neuronal firing patterns across multiple brain regions, and reorganizes large-scale functional connectivity networks — but how exactly these molecular events translate into subjective experience and durable therapeutic benefit remains an open question.

---

## 2. Background & Motivation

Psychedelics are a class of molecules capable of profoundly altering perception, cognition, and mood. After flourishing as research tools in the 1950s–1960s, they were largely sidelined by controlled substance legislation in the 1970s. A renewed wave of scientific and clinical interest has emerged in the past decade, driven by Phase II clinical trials showing that one or a few sessions of psilocybin-assisted psychotherapy can produce durable reductions in depression symptoms, anxiety, and substance-use disorders that outlast the acute drug effects by weeks to months.

The core motivation of this review is to synthesize what is known across multiple levels of biology — chemistry, receptor pharmacology, intracellular signaling, single-neuron electrophysiology, and whole-brain neuroimaging — into a coherent picture. The authors want to answer: why do these particular molecules do what they do, and can that knowledge guide better drug design and a mechanistic explanation of the psychedelic state?

This paper is directly relevant to the BioChemCore program because the 5-HT2A receptor — the principal target of psychedelics — is the prototypical post-synaptic CNS membrane protein for this curriculum. Everything in this review, from pharmacophore shape to downstream signaling to receptor localization in apical dendrites, maps onto the molecular and structural biology of the exact protein class being simulated.

---

## 3. Approach & Methods

This is a comprehensive narrative review published in *Nature Neuroscience*, meaning the authors synthesized findings across roughly 157 cited studies rather than conducting new experiments. The review is organized as a bottom-up journey through scales of biology: molecular chemistry first, then receptor pharmacology and signaling, then single-neuron and circuit effects, then whole-brain network changes, and finally theoretical frameworks that try to unify all of these levels into a coherent account of psychedelic action.

The authors specifically chose to focus on basic neurobiology rather than clinical outcomes, and they were careful to distinguish what is supported by rigorous evidence from what remains hypothetical. They draw heavily on animal electrophysiology, structural biology (cryo-EM and X-ray crystallography of 5-HT2A receptor complexes), human neuroimaging (fMRI, PET, EEG, MEG), and genetic/transcriptomic data. The review also incorporates historical experiments from the Aghajanian lab on raphe nucleus electrophysiology that date back to the 1960s, pointing out which classic findings hold up and which have been revised.

---

## 4. Key Findings

### The Pharmacophore: Why These Molecules Work

All classical psychedelics share a conserved chemical scaffold called the primary pharmacophore: an aromatic ring group separated from a basic amine by a two-carbon linker. This geometry is not arbitrary. When the basic nitrogen is protonated at physiological pH, it forms a salt bridge with aspartate residue D155 in the 5-HT2A binding pocket, while the aromatic ring makes hydrophobic contacts elsewhere in the receptor. The two-carbon linker length is optimal — shortening it by one carbon converts the agonist DMT into the antagonist gramine.

Psychedelics fall into two chemical families based on the aromatic ring. Tryptamines (psilocin, DMT, 5-MeO-DMT) carry a C3-substituted indole, and phenethylamines (mescaline, 2C-I, 2C-B) carry a phenyl ring. Ergolines like LSD are a specialized case of tryptamines: they embed the tryptamine pharmacophore within a rigid ring system, and this conformational rigidity reduces the entropic cost of binding, making LSD exceptionally potent.

A critically important practical point is that serotonin itself cannot easily cross the blood-brain barrier because it is highly polar. Psychedelic tryptamines like psilocin and DMT are structurally similar to serotonin but substantially more lipophilic, enabling rapid CNS penetration. The stark difference between orally active psilocin and the peripherally inactive bufotenin — two constitutional isomers that differ only in the position of a single hydroxyl group — illustrates how a small structural change can completely determine whether a compound has any psychedelic effect, despite comparable 5-HT2A affinity in a test tube.

### The 5-HT2A Receptor Is the Critical Target

Multiple converging lines of evidence establish 5-HT2A as the necessary receptor for the hallucinogenic effects of psychedelics:

- In humans, pre-treatment with the 5-HT2 antagonist ketanserin blocks both the subjective effects of psilocybin and LSD in a dose-dependent manner.
- Brain occupancy of 5-HT2A receptors directly predicts the intensity of the psychedelic effect.
- Human hallucinogenic potency and rodent behavioral potency (drug discrimination assays, head-twitch response) both correlate tightly with 5-HT2A binding affinity across dozens of structurally distinct compounds.
- Head-twitch response is abolished in 5-HT2A receptor knockout mice.

However, psychedelics are not selective — they are promiscuous agonists at many biogenic amine receptors. LSD, for example, is a high-affinity agonist at all 14 known human serotonin receptors plus several dopamine and adrenergic receptors. Actions at 5-HT2B receptors deserve special concern: chronic 5-HT2B agonism is well-established to cause potentially life-threatening cardiac valvulopathy, making selectivity away from 5-HT2B a design priority for any future psychedelic-derived therapeutic.

### Downstream Signaling: Multiple Pathways from One Receptor

When a psychedelic binds 5-HT2A, the receptor is a Class A GPCR — a seven-transmembrane helix protein embedded in the post-synaptic membrane — and it activates at least three distinct downstream pathways:

1. **Gq-mediated pathway:** The receptor couples to heterotrimeric Gq proteins, activating phospholipase C-beta (PLC-beta), which cleaves the membrane lipid PIP2 into two second messengers. IP3 triggers calcium release from the ER, and DAG activates protein kinase C (PKC). This is the canonical signaling arm.

2. **Beta-arrestin pathway:** Receptor activation also recruits beta-arrestin, which scaffolds an ERK1/2 MAP kinase signaling cascade that feeds into transcriptional changes. Beta-arrestin signaling is separable from G-protein signaling — a phenomenon called functional selectivity or biased agonism — and is genetically required for some behavioral effects of LSD (beta-arrestin-2 knockout abolishes certain LSD-induced behaviors in mice).

3. **Arachidonic acid release:** 5-HT2A receptors also couple to a Gi-mediated pathway that regulates arachidonic acid release via PLA2, though this pathway is less well characterized.

The key insight here is that different ligands can activate the same receptor but produce different ratios of signaling through these pathways. Engineering molecules that preferentially activate one pathway over another — biased agonism — is a major therapeutic strategy: for example, designing compounds that produce neuroplasticity-relevant signaling without the Gq-mediated cascade thought to underlie hallucinations.

Recent cryo-EM and X-ray crystallographic structures have resolved the 5-HT2A receptor in complex with LSD and other psychedelics, providing atomic-resolution images of the binding pocket and the receptor-G-protein interface. These structures are now being used as the starting point for computational drug design and virtual screening of hundreds of millions of compounds, accelerating the search for novel chemotypes with improved selectivity profiles.

### Neuronal Effects: What Happens at the Cellular Level

At the single-neuron level, psychedelics have different effects depending on the brain region and cell type, reflecting the heterogeneous distribution of 5-HT2A and other serotonin receptor subtypes.

In the **prefrontal cortex**, 5-HT2A receptors are predominantly postsynaptic and are densely concentrated in the apical dendrites of deep-layer pyramidal neurons. This localization predicts that psychedelics should increase dendritic excitability and promote excitatory postsynaptic potentials. In practice, the picture is more complex because cortical microcircuits contain mixed populations of pyramidal neurons and multiple GABAergic interneuron subtypes that express different amounts of 5-HT2A and other serotonin receptors. As a result, different cortical neurons show varied and sometimes opposing responses to systemic psychedelic administration.

In the **visual cortex**, psychedelics reduce stimulus-evoked spiking activity overall. Orientation tuning (the ability of neurons to respond selectively to visual stimuli at particular angles) remains intact, but surround suppression — the mechanism by which a neuron's response to a stimulus is reduced when similar stimuli appear in the surrounding visual field — is impaired. This suggests that psychedelics disrupt the contextual processing of visual information, which may contribute to altered visual perception.

The **dorsal raphe nucleus** shows one of the most striking acute effects: intravenous LSD causes a near-complete cessation of spiking within 1–2 minutes, returning to baseline after 20–30 minutes. This effect is psychedelic-specific (atropine and scopolamine do not replicate it) and arises from local somatodendritic 5-HT1A autoreceptors in the raphe, not 5-HT2A. Interestingly, raphe suppression does not correlate with LSD's behavioral effects in freely moving animals, so its functional significance for the psychedelic experience remains unclear.

### Longer-Term Effects: Structural Plasticity

A single dose of a psychedelic can initiate lasting structural changes in neurons. These include:

- Rapid increases in dendritic spine size and density in the medial frontal cortex, observable within 24 hours of a single psilocybin dose in rodents. Crucially, elevated spine density persists for at least one month.
- Upregulation of immediate early genes (c-fos, arc, egr-2) within 90 minutes, indicating a rapid transcriptional response in the neocortex.
- Increased BDNF (brain-derived neurotrophic factor) expression in some brain regions.
- Prolonged epigenetic and synaptic plasticity alterations, including changes in glutamate receptor expression.

These long-lasting structural changes are the cellular basis of what has been called "psychoplastogenesis" — the idea that psychedelics and related compounds promote neuroplasticity in ways that may underlie their durable therapeutic effects. An important unresolved question is whether 5-HT2A is strictly necessary for this structural remodeling, or whether other receptors or signaling events contribute.

### Network-Level Effects: What fMRI and EEG Show

At the whole-brain level, neuroimaging reveals two consistent findings across multiple psychedelics:

1. **Disruption of association networks:** Psilocybin and LSD acutely reduce activity and internal functional connectivity within the default-mode network (DMN) — a set of brain regions including medial prefrontal cortex, posterior cingulate, and parietal areas that is most active during self-referential thinking and internally focused cognition. At the same time, connectivity between sensory brain regions is paradoxically increased.

2. **Increased thalamo-cortical connectivity:** LSD consistently increases functional connectivity between the thalamus and sensory cortical regions, particularly in the somato-motor network. The thalamus serves as a relay and gating station for sensory information reaching the cortex, so increased thalamo-cortical connectivity may reflect a breakdown of the thalamus's normal filtering function.

These network changes depend on 5-HT2 receptor binding, as pharmacological blockade with ketanserin prevents the LSD-induced connectivity changes.

### Theories of Psychedelic Action

Four major theoretical frameworks attempt to translate the circuit and network findings into an account of how psychedelics alter consciousness:

- **CSTC model (Cortico-Striato-Thalamo-Cortical):** Psychedelics disrupt thalamic gating via 5-HT2A agonism in cortico-striato-thalamic loops, resulting in increased sensory feedforward information reaching cortex. Supported by impaired sensorimotor gating (prepulse inhibition) in humans and increased thalamo-cortical connectivity in neuroimaging.

- **REBUS model (Relaxed Beliefs Under Psychedelics / Anarchic Brain):** Psychedelics increase the influence of bottom-up sensory signals while reducing the strength of top-down prior beliefs — the brain's expectations that normally constrain perception. This would increase neural entropy (unpredictability of brain signals). Supported by DMN disruption and EEG evidence of weakened top-down alpha-band signals. However, this model conflicts with electrophysiology showing mostly reduced stimulus-evoked responses in sensory cortex.

- **Strong Prior (SP) model:** The psychedelic experience arises not from increased sensory input but from reduced sensory signals paired with aberrant over-reliance on top-down prior expectations. Recent evidence from conditioning-induced hallucinations supports the idea that psychedelics heighten dependence on inappropriate learned beliefs.

- **CCC model (Cortico-Claustro-Cortical):** Psychedelics disrupt communication between the prefrontal cortex and the claustrum (a thin subcortical structure with dense 5-HT2A expression), impairing the coordinated response of association networks to changing task demands.

The authors note that CSTC and CCC are implementation-level models (what circuits are altered), while SP and REBUS are computational-level models (what cognitive operations change). These are complementary rather than mutually exclusive, and a complete theory will need to account for both.

---

## 5. Significance & Implications

This review is foundational reading for anyone working with the 5-HT2A receptor, and its relevance to the BioChemCore program is immediate and direct.

**For molecular dynamics simulations of 5-HT2A:** The paper describes the binding pocket geometry in atomic detail — the D155 aspartate salt bridge, hydrophobic contacts, and how the two-carbon pharmacophore linker length determines agonist vs. antagonist activity. When you analyze your MD trajectory, you can look for these specific interactions. The paper also highlights that the binding pocket has a "second binding pocket" that explains the enhanced potency of NBOMe compounds. Crystal structures and cryo-EM structures of the receptor are now available and were used to generate structural figures in this review.

**For understanding why the receptor matters:** The paper explains that 5-HT2A is not just any GPCR. It is densely localized in the postsynaptic apical dendrites of prefrontal pyramidal neurons — the very location that your MD system represents. The receptor's downstream signaling through Gq activates PLC-beta, generating IP3 and DAG, which in turn mobilize calcium and PKC. This is classic GPCR signal transduction, directly relevant to how conformational changes in the receptor (observable in MD) connect to cellular outcomes.

**For the broader field:** This paper represents a synthesis moment in psychedelic neuroscience — a field that had fragmented across chemistry, pharmacology, neuroscience, and psychiatry, and is now being unified. Psychedelics are emerging as clinically meaningful tools. The race to design compounds with therapeutic effects but reduced hallucinogenicity (psychoplastogens like isoDMT, TBG, and AAZ) depends on understanding exactly what structural features of the molecule and receptor drive which signaling pathways. Computational chemistry and MD are central to this effort.

---

## 6. Limitations & Open Questions

**The 5-HT2A vs. 5-HT2C problem.** Most psychedelics also potently activate 5-HT2C receptors, which are highly expressed in the brain and regulate dopaminergic pathways. There is currently no pharmacological tool that can cleanly separate 5-HT2A and 5-HT2C activity, and no truly selective 5-HT2A antagonist exists. This limits the ability to assign specific effects definitively to 5-HT2A.

**5-HT2A and structural plasticity causality is unresolved.** It is debated whether 5-HT2A receptor activation is actually required for psilocybin-induced dendritic spine remodeling. Some studies show ketanserin pretreatment does not block psilocybin-evoked spine growth; others using knockout animals suggest it is essential. The discrepancy may reflect incomplete receptor blockade by ketanserin or developmental effects of constitutive knockouts.

**Cell-type resolution is lacking.** Much classic neurophysiology was done before the current era of cell-type classification. GABAergic interneuron subtypes (parvalbumin, somatostatin, etc.) in the frontal cortex express 5-HT2A at different levels and should respond differently to psychedelics, but the circuit-level consequences are largely unmapped.

**The hallucination-therapy dissociation question is unresolved.** Whether the acute subjective experience is necessary, sufficient, or irrelevant to the therapeutic effects of psychedelics is one of the most important open questions in the field. The authors note this cannot yet be answered from existing clinical data.

**Most mechanistic work is in rodents.** The subjective state that defines a "psychedelic experience" is inherently difficult to model in animals. Behavioral proxies like the head-twitch response and drug discrimination have good predictive validity for potency, but cannot capture the cognitive and emotional dimensions that seem relevant to therapeutic outcomes.

**Network imaging studies lack longitudinal depth.** Long-term changes in functional connectivity after psychedelic administration exist but are understudied. Individual variability is large, baseline 5-HT2A receptor availability predicts the acute experience, and the mechanistic connection between acute network disruption and lasting therapeutic change remains unclear.

---

## 7. Key Terms and Concepts

**Pharmacophore:** The minimal chemical scaffold responsible for a drug's biological activity at a given receptor. For classical psychedelics, this is an aromatic ring separated from a protonatable basic amine by a two-carbon linker. The shape and electronic properties of this scaffold determine 5-HT2A binding.

**Biased agonism (functional selectivity):** The ability of different ligands at the same receptor to preferentially activate one downstream signaling pathway over another. A biased agonist at 5-HT2A might preferentially activate beta-arrestin/ERK signaling (thought to drive plasticity) while minimally activating Gq/PLC (thought to contribute to hallucinations). This is a major principle guiding next-generation psychedelic drug design.

**Gq-PLC-IP3/DAG cascade:** The canonical downstream signaling pathway of 5-HT2A. Gq activates phospholipase C-beta (PLC-beta), which cleaves the membrane phospholipid PIP2 into inositol trisphosphate (IP3) and diacylglycerol (DAG). IP3 opens ER calcium channels; DAG activates protein kinase C (PKC). Both second messengers feed into gene expression changes and altered neuronal excitability.

**Psychoplastogen:** A compound — psychedelic or non-hallucinogenic psychedelic analog — that promotes structural neuroplasticity (dendritic spine growth, increased BDNF, new synapse formation). The idea is that the plasticity-promoting effects, not the perceptual effects, may be what makes psychedelics therapeutically useful.

**Default-mode network (DMN):** A set of brain regions (medial prefrontal cortex, posterior cingulate cortex, angular gyrus) that are co-active at rest and during self-referential thought. Psychedelics acutely disrupt DMN internal connectivity. This disruption has been linked to the dissolution of habitual self-referential thought patterns, which may be relevant to their antidepressant effects.

**Thalamic gating:** The function of the thalamus in filtering and controlling which sensory information reaches the cortex. The CSTC model proposes that psychedelics disrupt this gating via 5-HT2A receptors in the cortico-striato-thalamic loop, leading to sensory "overload" — too much sensory information flowing to association cortex without normal filtering.

**REBUS model:** "Relaxed Beliefs Under Psychedelics and the Anarchic Brain." A theoretical framework proposing that psychedelics reduce the strength of top-down prior beliefs (the brain's predictions about what it will perceive) while increasing the influence of bottom-up sensory signals. The net effect is higher entropy in neural dynamics and a loosening of perceptual constancy — which could manifest as hallucinations and altered sense of self.

---

*Summary prepared for BioChemCore program context: 5-HT2A serotonin receptor molecular dynamics simulations.*
