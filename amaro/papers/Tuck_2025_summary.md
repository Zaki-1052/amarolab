# Summary: Tuck et al. (2025) — Molecular Design of a Therapeutic LSD Analogue with Reduced Hallucinogenic Potential

**Citation:** Tuck JR, Dunlap LE, Khatib Y, et al. "Molecular design of a therapeutic LSD analogue with reduced hallucinogenic potential." *PNAS* 122(16): e2416106122. Published April 14, 2025.

---

## 1. One-Sentence Takeaway

By transposing just two atoms in the LSD scaffold to eliminate a single hydrogen bond interaction at the 5-HT2A receptor, the researchers created JRT — a potent, non-hallucinogenic psychoplastogen that promotes cortical neuron growth and produces robust antidepressant, anti-anhedonic, and pro-cognitive effects relevant to schizophrenia treatment.

---

## 2. Background & Motivation

### The problem: schizophrenia has a structural deficit that current drugs ignore

Schizophrenia (SCZ) affects roughly 0.5% of the global population and is characterized by three categories of symptoms: positive symptoms (hallucinations and delusions), negative symptoms (anhedonia and avolition — a loss of pleasure and motivation), and cognitive symptoms (impaired attention and working memory). Current antipsychotic drugs work primarily by blocking dopamine D2 receptors, which addresses positive symptoms reasonably well. But they largely fail at the negative and cognitive symptoms — and these are the ones most correlated with poor quality of life and treatment outcomes.

There's a structural reason why. The prefrontal cortex (PFC) in SCZ patients shows decreased dendritic spine density, reduced dendritic arborization, and lower levels of synaptic proteins. These are the physical substrates of cognition. Dendritic spines are the tiny protrusions on neurons where synapses form; when they atrophy, the circuits that support working memory and executive function degrade. No approved antipsychotic addresses this structural atrophy.

### Psychedelics can regrow neurons — but they cause hallucinations

Psychedelics like LSD are among the most potent known psychoplastogens — a term for small molecules that rapidly and persistently promote structural plasticity in cortical neurons, increasing dendritic spine density and arborization. LSD is an exceptionally potent agonist at the 5-HT2A serotonin receptor (5-HT2AR), and this receptor activation drives both the neuroplastic effects and the hallucinogenic effects. Because hallucinations are a positive symptom of SCZ, giving a hallucinogen to a patient with schizophrenia or a family history of psychosis is contraindicated — it can precipitate or worsen psychosis. Clinical trials for depression have already excluded roughly 95% of volunteers due to this concern.

This creates the central tension the paper addresses: psychedelics have exactly the neuroplasticity-promoting properties needed to treat the structural deficits in SCZ, but their hallucinogenic properties make them unusable in that population. The goal is to separate these two effects.

### Why LSD is the right scaffold to modify

LSD belongs to the ergoline chemical family — a rigid tetracyclic ring structure. The authors had previously shown that moving the dimethylaminoethyl group from carbon C3 to nitrogen N1 in tryptamine-class psychedelics reduced hallucinogenic potential while maintaining neuroplasticity (a compound called isoDMT). They reasoned that an analogous modification to LSD might also reduce hallucinogenicity. Crucially, LSD already has a known, detailed binding pose within the 5-HT2AR crystal structure, so they could design rationally at the atomic level.

---

## 3. Approach & Methods

### Rational structural design guided by receptor binding

The researchers started with a specific structural hypothesis. LSD makes a hydrogen bond between the indole N–H group and two serines in the 5-HT2AR binding pocket: S242 (position 5.46) and G238 (position 5.42). Their prior work had shown that nonhallucinogenic ligands of the 5-HT2AR induce distinct receptor conformational states compared to hallucinogens. The conformational state of the receptor — the precise shape it adopts when a ligand binds — determines whether it triggers hallucinogenic signaling. If they could disrupt this hydrogen bond, they hypothesized the receptor would adopt a non-hallucinogenic conformation.

The solution was elegant: convert LSD's indole core (which has an N–H that can donate a hydrogen bond) to an indolonaphthyridine core (which repositions the nitrogen so no N–H bond is present in the relevant orientation). This is a constitutional isomer of LSD — it has the same molecular formula and the same overall ergoline framework, but two atoms are repositioned. They named this compound JRT.

Molecular docking studies confirmed that JRT should adopt a binding pose nearly identical to LSD within the 5-HT2AR crystal structures (RMSD = 1.239 for one structure, 0.930 for another), except that the indole nitrogen is shifted approximately 1 Å away from the key serines — just far enough to eliminate the hydrogen bond.

### De novo total synthesis

Because JRT cannot be made from lysergic acid (the natural precursor to LSD), the team developed a complete 12-step de novo total synthesis with 11% overall yield. Starting from commercially available 5-bromonicotinic acid, the synthesis involved Suzuki coupling reactions, N-alkylation, selective decarboxylation events, mCPBA oxidation, a Boekelheide rearrangement, and a tosylation-driven ring closure that simultaneously formed the tetracyclic core. Chiral HPLC then separated the (±)-JRT racemate into the pure (+) and (−) enantiomers. X-ray crystallography of a methylated derivative confirmed the absolute stereochemistry.

### Receptor pharmacology panel

The researchers tested both (+)-JRT and (−)-JRT against 55 CNS targets using competitive radioligand binding, then characterized receptor function using:
- **BRET-based Gq activation assays** to measure classical GPCR signaling downstream of 5-HT2A activation
- **psychLight**, an engineered biosensor that couples ligand-induced receptor conformational changes to a fluorescence readout — it reports the conformational state of the receptor more directly than functional assays, and it comes in a wild-type (WT) version and a mutant version (S242A) that lacks the key hydrogen-bonding serine
- **Association/dissociation binding kinetics** to measure how fast each ligand binds and unbinds the receptor

### Neuroplasticity assays

Dendritic growth was measured in cultured embryonic rat cortical neurons (DIV6 and DIV18/19) using Sholl analysis, which quantifies the complexity of dendritic branching by counting how many times dendrites cross concentric circles drawn around the cell body. In vivo, they used scanning electron microscopy of serial sections (S3EM) to directly visualize and quantify dendritic spines and synapses in the medial prefrontal cortex (mPFC) of mice 24 hours after drug administration. They also used a chronic corticosterone (CORT) stress model to induce structural atrophy matching SCZ pathology, and Thy1-EGFP transgenic mice (which have fluorescently labeled neurons in specific cortical layers) to visualize spine rescue.

### Behavioral testing battery

The behavioral work was extensive and targeted three categories:
- **Hallucinogenic potential:** head-twitch response (HTR) assay in mice, a well-validated measure where serotonergic psychedelics induce rapid side-to-side head rotations; prepulse inhibition (PPI) deficits
- **Antidepressant-like effects:** forced swim test (FST), sucrose preference test (SPT) for anhedonia, probabilistic reward task (PRT) for cognitive measure of reward responsiveness
- **Antipsychotic-like effects:** amphetamine- and phencyclidine-induced hyperlocomotion, MK-801-induced PPI deficits
- **Cognitive flexibility:** unpredictable mild stress (UMS) reversal learning task

### Gene expression analysis

Using a transcriptome-wide association study (TWAS) reference set of the top 250 loci most enriched in SCZ versus control postmortem human brain tissue, they performed permutation tests to determine whether differentially expressed genes (DEGs) in mouse PFC following LSD or (+)-JRT administration were disproportionately enriched among SCZ-associated genes.

---

## 4. Key Findings

### JRT is selective for serotonin receptors — not dopamine, histamine, or adrenergic

Competitive binding across 55 CNS targets revealed that both (+)-JRT and (−)-JRT are highly selective for a subset of serotonin receptors. Neither compound showed measurable affinity for dopamine, histamine, or adrenergic receptors. This is pharmacologically important: LSD promiscuously hits many receptor types, which contributes to side effects. (+)-JRT demonstrated high affinity for all 5-HT2 family receptors (Ki range 2–184 nM) and acted as a potent partial agonist at 5-HT2A (Emax = 81%) and 5-HT2B (Emax = 48%), and a near full agonist at 5-HT2C (Emax = 89%). It also showed agonist/partial agonist activity at 5-HT1A and 5-HT7 receptors.

### (+)-JRT induces a non-hallucinogenic receptor conformation

This is the molecular core of the paper. In the psychLight assay using the wild-type human 5-HT2AR, (+)-JRT was two orders of magnitude less potent than LSD (EC50 = 90 nM vs. 0.5 nM) and had markedly lower efficacy (Emax = 33% vs. 44%). More tellingly, when the S242A mutant version of psychLight was used — the version lacking the serine that LSD hydrogen-bonds to — the potency difference between LSD and (+)-JRT largely disappeared. LSD is much more dependent on S242 for its receptor activation signal than (+)-JRT is. This confirms the structural hypothesis: LSD's signaling at the WT receptor is biased through the hydrogen bond with S242, and eliminating that bond in JRT shifts the receptor to a different conformational state.

Kinetic binding studies reinforced this: the dissociation rate (koff) of (+)-JRT from the 5-HT2AR is approximately 10-fold faster than LSD. LSD is known for extremely slow receptor unbinding ("stuck" binding), and this slow dissociation is linked to its hallucinogenic bias in signaling. JRT's faster off-rate means it spends less time locked into the hallucinogenic conformation.

### (+)-JRT has dramatically reduced hallucinogenic potential in vivo

In the mouse head-twitch response (HTR) assay, (+)-JRT did not induce any robust HTR at any dose tested (0.05–1.5 mg/kg), whereas LSD produced clear, dose-dependent HTR at 0.2 mg/kg. Pretreatment with (+)-JRT at 1 mg/kg completely blocked LSD-induced HTR, demonstrating that (+)-JRT actively occupies the 5-HT2AR and competes with LSD rather than simply failing to engage the receptor. (+)-JRT also did not produce PPI deficits — another behavioral hallmark of hallucinogens.

### (+)-JRT is a potent psychoplastogen

In cultured rat cortical neurons:
- (+)-JRT increased maximum dendritic crossings (Nmax in Sholl analysis) to a comparable or greater degree than LSD and the atypical antipsychotic clozapine
- (+)-JRT increased the number of primary dendrites (P < 0.0005 vs. vehicle)
- (+)-JRT promoted dendritic branching; CLZ did not
- (+)-JRT was the only compound statistically significant under the Sholl curve compared to vehicle (P < 0.05)

In vivo (mouse mPFC, 24 h post-administration):
- A single dose of (+)-JRT (1 mg/kg) produced a **46% increase in dendritic spine density** by S3EM
- Synapse density increased by 18% in layer 1 of mPFC
- Synapse size was unchanged, suggesting new spine formation rather than enlargement of existing synapses

In the cortical atrophy rescue model:
- Chronic CORT administration dramatically depleted dendritic spines in layer 2/3 of the mPFC of Thy1-EGFP mice
- A single dose of (+)-JRT completely rescued this structural deficit — it restored dendritic spine density to baseline levels
- Notably, (+)-JRT did not grow spines beyond baseline in non-stressed animals in this layer, suggesting it specifically repairs damaged circuits rather than simply inflating all plasticity

### (+)-JRT produces antidepressant-like effects

In the FST, (+)-JRT reduced immobility and increased swimming behavior at all doses tested 24 hours after administration. It appeared at least 100-fold more potent than ketamine in this assay based on dose comparison. The effect persisted — animals remained in an antidepressant-like state for at least 3 days after a single injection, even while continuing to receive daily cold-water stress. Brain concentrations at the highest dose tested were approximately 20-fold higher than the Ki at 5-HT2AR, consistent with target engagement.

In the sucrose preference test following chronic CORT (a model of anhedonia), (+)-JRT rescued preference for sucrose in CORT-sensitive animals (those who lost preference during stress), with effects observed up to 9 days after the last dose. In the probabilistic reward task (PRT) — a translationally validated measure of anhedonia used in humans, rodents, and nonhuman primates — (+)-JRT rescued chronic stress-induced response bias deficits that also responded to ketamine.

### (+)-JRT does not exacerbate positive symptoms of SCZ

This is critical for the target population. (+)-JRT pretreatment did not exacerbate phencyclidine-induced hyperlocomotion or MK-801-induced PPI deficits. It did attenuate amphetamine-induced hyperlocomotion in female mice — consistent with its 5-HT2C agonism reducing dopamine efflux in the nucleus accumbens, an antipsychotic-like mechanism.

### (+)-JRT does not produce SCZ-associated gene expression signatures

LSD administration induced a set of differentially expressed genes in the mouse PFC that were significantly enriched among SCZ TWAS candidate genes (P = 0.018). In other words, LSD's gene expression signature overlaps with the molecular fingerprint of SCZ. (+)-JRT did not show this enrichment (P = 0.557). This is strong evidence that despite activating the same receptor as LSD, the distinct conformational state induced by (+)-JRT at 5-HT2AR translates all the way to different downstream transcriptional consequences.

### (+)-JRT promotes cognitive flexibility

In the UMS reversal learning task, (+)-JRT did not impair initial stimulus discrimination but significantly rescued the reversal learning deficit caused by unpredictable mild stress. Reversal learning — the ability to update behavior when the rules change — is impaired in SCZ and bipolar disorder. This pro-cognitive effect is distinct from what selective 5-HT2C receptor agonists produce in the same assay, suggesting the unique 5-HT2AR partial agonism of (+)-JRT contributes something that 5-HT2C engagement alone cannot.

---

## 5. Significance & Implications

### This is a proof-of-concept that receptor conformation can be rationally engineered

The paper's deepest contribution is demonstrating that an extraordinarily subtle chemical change — repositioning two atoms, shifting the hydrogen-bond donor by 1 Angstrom — is sufficient to fundamentally reprogram the pharmacology of a receptor ligand. The receptor "cares" not just about whether a molecule binds, but about the precise 3D geometry of that binding. Hallucinogenic and non-hallucinogenic effects are not separate chemical properties requiring different scaffolds; they are emergent consequences of which receptor microstate a ligand stabilizes.

This has major implications for drug design across GPCRs and directly connects to the BioChemCore context: MD simulations of the 5-HT2AR would reveal exactly how LSD vs. JRT affect the receptor's conformational dynamics over time. The distinct koff values (JRT dissociates 10x faster), the different signaling biases (Gq vs. beta-arrestin coupling), and the S242 hydrogen bond are all features that would be visible in an MD trajectory. Studying how the receptor protein fluctuates differently around LSD vs. JRT — through RMSD, RMSF, and contact analysis — is the kind of analysis you'd do in BioChemCore Day 7.

### JRT's polypharmacology may be an asset, not a liability

Most drugs are designed to be maximally selective. JRT's activity across 5-HT2A, 5-HT2B, 5-HT2C, 5-HT1A, and 5-HT7 is not accidental noise — each receptor contributes something: 5-HT2A partial agonism drives neuroplasticity and cognitive effects; 5-HT2C agonism reduces dopamine hyperactivity (addressing positive-symptom-adjacent dopamine dysregulation); 5-HT1A agonism contributes to antidepressant effects; 5-HT7 may modulate circadian and cognitive function. This polypharmacology may explain why JRT outperforms LSD in some neuroplasticity measures despite being a partial agonist.

### The schizophrenia treatment gap may now have a new approach

Negative and cognitive symptoms of SCZ represent an enormous unmet need. Current antipsychotics essentially ignore the dendritic atrophy that underlies these symptoms. If JRT's ability to rescue stress-induced cortical atrophy in a single dose translates to humans, it would represent a mechanistically novel treatment strategy — not symptom management but structural repair of the circuits themselves.

### For your BioChemCore project on the 5-HT2A receptor

This paper gives you rich biological context for why the 5-HT2AR is one of the most pharmacologically important post-synaptic CNS membrane proteins. In your MD simulation, you would be working with the same binding pocket residues this paper focuses on: L229 (EL2), Y370 (7.43), D155 (3.32), S242 (5.46), G238 (5.42), W336 (6.48), and F340 (6.52). Understanding which residues form key contacts with ligands and how mutations at S242 attenuate ligand discrimination maps directly onto RMSF analysis (which residues fluctuate most) and contact frequency analysis (which residues maintain hydrogen bonds across the trajectory).

---

## 6. Limitations & Open Questions

**5-HT2B cardiac risk:** (+)-JRT is a potent partial agonist at 5-HT2B receptors. Chronic stimulation of 5-HT2B has been associated with cardiac valvulopathy (heart valve damage) — this is the mechanism by which the diet drug fenfluramine caused cardiac toxicity. The authors acknowledge this liability explicitly. Whether the dosing regimen envisioned (single or infrequent dosing, as with psychedelics) would cause clinically meaningful 5-HT2B stimulation remains to be determined. This is a genuine safety concern that will need to be addressed in IND-enabling studies.

**All preclinical so far:** Every in vivo result is in mice and rats. The human 5-HT2AR has some notable differences from rodent receptors — for example, the paper specifically notes that LSD hydrogen bonds to S242 in the human receptor but that the mutant S242A assay in psychLight attenuates (but does not eliminate) potency differences. Whether the hallucinogenicity reduction is as complete in humans is unknown.

**Cognitive rescue was modest and context-dependent:** In the reversal learning assay, (+)-JRT rescued stress-induced deficits but did not produce significant effects in non-stressed animals. The number of trials completed only trended toward significance. This suggests the procognitive effects may be restorative rather than enhancing — meaningful for patient populations but limiting the signal in healthy animal models.

**The neuroplasticity mechanism is not fully resolved:** Whether the structural plasticity effects of (+)-JRT require Gq signaling, beta-arrestin signaling, or some intracellular pathway downstream of receptor activation remains unclear. The authors propose that partial Gq agonism is sufficient for neuroplasticity while full activation is required for hallucinations, but this threshold model is not yet directly demonstrated.

**5-HT2AR knockout validation is needed:** The authors block spinogenesis with a 5-HT2AR antagonist (ketanserin) to confirm on-target action, but 5-HT2AR knockout experiments — the gold standard for confirming receptor necessity — are noted as future work.

---

## 7. Key Terms & Concepts

**Psychoplastogen:** A small molecule that rapidly and persistently promotes structural plasticity in cortical neurons — specifically increasing dendritic spine density and arborization — after a single administration. The term distinguishes these compounds from classical antidepressants that require weeks of dosing.

**Dendritic spine:** A small, actin-rich protrusion on a dendrite where most excitatory synapses form; their density is a measurable index of synaptic connectivity and is reduced in schizophrenia, depression, and chronic stress.

**5-HT2A receptor (5-HT2AR):** A G protein-coupled receptor (GPCR) for serotonin, expressed densely in pyramidal neurons of the prefrontal cortex; it is the primary molecular target responsible for both the hallucinogenic effects and the neuroplasticity-promoting effects of classical psychedelics.

**Biased agonism / receptor conformational bias:** The phenomenon in which different ligands binding the same receptor stabilize different active conformations, leading to activation of different downstream signaling pathways. (+)-JRT is "biased" toward a conformation that doesn't efficiently recruit beta-arrestin 2 or trigger hallucinogenic signaling, even though it still activates Gq.

**Ergoline scaffold:** The rigid tetracyclic ring system shared by LSD and JRT, consisting of a tryptamine-like indole embedded in a larger fused ring framework; this scaffold provides highly constrained binding geometry within the 5-HT2AR pocket.

**Sholl analysis:** A neuroanatomy method for quantifying dendritic complexity by counting how many times dendrites cross concentric circles (shells) centered on the cell body; generates a plot from which total dendritic length, branching, and reach can be extracted.

**psychLight:** An engineered BRET-based biosensor developed by the Olson lab that reports the conformational state of the 5-HT2AR in response to ligand binding, providing a more direct readout of receptor activation state than classical downstream signaling assays.

---

*Summary prepared for BioChemCore context. The 5-HT2A receptor binding pocket residues described in this paper (S242, G238, D155, W336, F340, L229, Y370) are directly relevant to structural analysis and MD simulation of this receptor system.*
