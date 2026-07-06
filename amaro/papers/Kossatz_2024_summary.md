# Kossatz et al. (2024) — G protein-specific mechanisms in the serotonin 5-HT2A receptor regulate psychosis-related effects and memory deficits

**Citation:** Kossatz E, Diez-Alarcia R, Gaitonde SA, et al. *Nature Communications* 15:4307 (2024). https://doi.org/10.1038/s41467-024-48196-2

---

## 1. One-Sentence Takeaway

By using structurally related chemical probes derived from serotonin and combining live-cell assays, human postmortem brain tissue, mouse behavioral experiments, and molecular dynamics simulations, this study demonstrates that the 5-HT2A receptor's Gαi protein pathway drives psychosis-related behavior while its Gαq pathway drives memory deficits — showing that these two schizophrenia-relevant symptoms are controlled by mechanistically separable intracellular signaling routes.

---

## 2. Background & Motivation

### The problem with blunt-instrument antipsychotics

Schizophrenia is a severe psychiatric disorder with three symptom clusters: positive symptoms (hallucinations, paranoid ideation), negative symptoms (amotivation, anhedonia, social withdrawal), and cognitive deficits (impaired working memory, long-term memory). Current antipsychotic medications — both classical and atypical — primarily address positive symptoms, but they largely fail to improve cognitive or negative symptoms. This is clinically serious because it is precisely the cognitive and negative symptoms that most undermine a patient's ability to function in daily life. On top of that, up to 30% of patients are treatment-resistant, and adverse side effects are pervasive.

The underlying pharmacology problem is that most antipsychotics work by broadly inhibiting receptors like the serotonin 5-HT2A receptor (5-HT2AR) without regard to which specific downstream signaling pathway is being blocked. This matters because GPCRs — the superfamily of receptors to which 5-HT2AR belongs — do not send a single signal when activated. They are more like switchboards: a single activated receptor can simultaneously recruit multiple G protein subtypes (each triggering its own intracellular cascade) as well as β-arrestin proteins (which regulate receptor trafficking and initiate their own signaling). Indiscriminately blocking all of these pathways at once can produce beneficial effects through one route while simultaneously causing harm or losing efficacy through another.

### Why the 5-HT2A receptor specifically

The 5-HT2AR is one of the most important targets in psychiatric pharmacology. It is expressed at high levels in the prefrontal cortex — a region central to cognition, executive function, and the filtering of sensory information. It is the principal target of classical psychedelic drugs (LSD, psilocybin) and is implicated in the mechanism of action of many atypical antipsychotics. Critically, a prior study found that fully silencing 5-HT2AR-mediated signaling via antipsychotics reduces expression of the metabotropic glutamate receptor 2 (mGlu2R), which is itself therapeutically relevant — suggesting that non-selective inhibition of the receptor is counterproductive.

### The concept of biased signaling (pathway bias)

When a receptor agonist preferentially activates one downstream pathway over others relative to the endogenous ligand, this is called **biased agonism** or **functional selectivity**. The discovery that small molecules can be designed to be biased toward specific signaling pathways opened a conceptual door: rather than blocking or activating a receptor wholesale, one might be able to selectively engage only the pathways that produce the desired therapeutic effect, while avoiding the pathways responsible for side effects or cognitive impairment.

The gap this paper addresses is that, despite the clinical importance of the 5-HT2AR, the contribution of specific signaling pathways to the distinct symptom clusters of schizophrenia — psychosis, cognition, and affect — was largely unknown. Which G protein subtype controls which behavioral outcome? This was the core unanswered question.

---

## 3. Approach & Methods

The authors used a four-pronged strategy that is genuinely sophisticated in its design: they worked simultaneously at the molecular, cellular, tissue, and whole-animal levels, and used computational modeling to tie structural observations to functional outcomes.

### The signaling probes

Rather than using random drug candidates, the team built their study around four small molecules that are all structural derivatives of the endogenous agonist serotonin (5-HT). This was a smart choice because it allows direct attribution of signaling differences to specific structural features of the molecule, rather than having differences in binding affinity or pharmacokinetic properties confound the comparison.

- **Nitro-I:** 3-(2-aminoethyl)-1-methyl-1H-indol-5-ol hydrochloride — a close analog with a nitro group
- **Met-I:** 3-(2-aminoethyl)-1-methyl-1H-indol-5-ol hydrochloride — a methyl-substituted analog
- **OTV1:** 2-[5-(2,3-dihydro-1,4-benzodioxin-6-yl)-1H-indol-3-yl]ethan-1-amine — has a bulky 1,4-benzodioxin (5-benzodioxan) substituent at position 5 of the indole scaffold
- **OTV2:** 2-(5-phenoxy-1H-indol-3-yl)ethan-1-amine — has a phenoxy substituent at position 5

OTV1 and OTV2 were retrieved through a virtual screen of the ZINC database (~100,000 lead-like compounds), docked to the 5-HT2AR orthosteric binding site using four conformational ensembles in Glide (Schrödinger). The key distinction among the probes is what substituent they carry at position 5 of the indole ring, which turns out to directly affect how much the molecule contacts extracellular loop 2 (ECL2) of the receptor.

### Live-cell BRET assays

To map which G proteins each compound activates in living cells, the researchers used **enhanced bystander BRET (ebBRET)** biosensors in HEK-293 cells. BRET (Bioluminescence Resonance Energy Transfer) works by engineering a bioluminescent donor (RlucII) and a fluorescent acceptor (rGFP) such that energy transfer only occurs when the two are in close proximity — meaning when the G protein or β-arrestin is actively recruited to an effector or membrane location upon receptor activation. This gave the team real-time readout of receptor coupling to Gαq, Gαi1, Gαi2, Gαi3, β-arrestin 1, and β-arrestin 2 — six distinct downstream transducers — for each of the four compounds and for 5-HT itself as a reference.

Bias factors (using the operational model, which corrects for differences in intrinsic receptor activity and system-level amplification) were then computed for each compound against each pathway, with 5-HT as the reference agonist.

### Human postmortem brain tissue — [35S]GTPγS binding with antibody capture (SPA)

To move from cell lines to biologically relevant tissue, the team used **[35S]GTPγS binding scintillation proximity assay (SPA)** on postmortem human prefrontal cortex (PFC) membrane homogenates. GTPγS is a non-hydrolyzable analog of GTP — when a G protein is activated by a receptor, it normally exchanges GDP for GTP; here, the radioactive GTPγS gets incorporated and stays there, allowing quantification of activation. By adding subtype-specific antibodies to immunoprecipitate individual Gα proteins onto scintillation beads, the team could measure activation of Gαi1, Gαi2, Gαi3, and Gαq/11 separately for each compound in actual human brain tissue.

Crucially, to confirm that the effects were 5-HT2AR-mediated (and not through other receptors in the tissue), all assays were repeated in the presence of MDL-11,939, a selective 5-HT2AR neutral antagonist. The same approach was used in mouse brain tissue comparing wild-type (WT) and 5-HT2AR knockout (KO) mice.

### In vivo behavioral testing in mice

Two behavioral paradigms were selected as translational models of schizophrenia symptoms:

- **Head twitch response (HTR):** A rapid, side-to-side rotational head movement in rodents that serves as a behavioral proxy for hallucinogenic/psychosis-related effects at the 5-HT2AR. Classic psychedelics like DOI and LSD robustly induce HTR. This was used to interrogate the psychosis-related arm.

- **Novel object recognition (NOR):** A test of long-term memory in which a mouse is exposed to two objects, then 24 hours later presented with one familiar object and one novel object. Mice with intact memory spend more time with the novel object (higher discrimination index). This was used as a proxy for the cognitive deficit arm.

To disambiguate which specific G protein subtype mediated each behavioral effect, the researchers used two complementary reduction strategies:
1. Pharmacological inhibition via ICV (intracerebroventricular) administration of **YM-254890**, a selective Gαq/11 inhibitor
2. Genetic knockdown via ICV antisense **oligodeoxynucleotides (ODNs)** targeting Gαi1 or Gαi3 mRNA — confirmed by Western blot

All experiments were run in both WT and 5-HT2AR KO mice to confirm receptor-dependence.

### Molecular dynamics simulations

The team built 3D structural models of each ligand-5-HT2AR complex based on the active-state crystal structure (PDB 6WHA, an agonist-bound, miniGαq-coupled structure). Missing loops and side chains were modeled using MODELLER and Homolwat. Protonation states were assigned by ProteinPrepare (HTMD). Each ligand was docked with the MOE Molecular Operating Environment tool, and the top-ranked poses were subjected to energy minimization (MMFF94x force field). Then each complex was embedded in a POPC lipid bilayer with TIP3 water and run under NVT conditions for 3 × 500 ns (1.5 µs total per ligand) using ACEMD3 with the CHARMM force field. Trajectories were clustered by ligand RMSD, and contact frequencies for each residue — including orthosteric binding site residues and ECL2 residues — were computed from the most populated cluster.

---

## 4. Key Findings

### Finding 1: The four probes have dramatically different G protein coupling profiles

In live HEK-293 cells, all four compounds are full agonists at the canonical Gαq pathway (the one typically associated with 5-HT2AR activation), but they are only partial agonists at Gαi family members and β-arrestins compared to 5-HT.

The key divergence happens among the compounds themselves:

- **Nitro-I and Met-I** both show a strong **Gαq physiology-bias** relative to the Gαi family and β-arrestins (>50-fold Gαq bias over β-arrestin 2 for both). In plain terms: they preferentially activate Gαq.

- **OTV2** shows the opposite — a **Gαi family physiology-bias** over Gαq (particularly toward Gαi1, Gαi2, Gαi3). It also has a substantially reduced ability to recruit β-arrestin 1 (17-fold Gαq bias over β-arrestin 1, compared to the Gαq-biased compounds). OTV2 has the highest binding affinity among the probes (pKi = 7.24 ± 0.08), linked to its phenoxy substituent.

- **OTV1** (the benzodioxin analog) loses most of its ability to stimulate Gαi2/Gαi3 and β-arrestin recruitment compared to 5-HT, while maintaining a strong Gαq activation preference over Gαi proteins. Its ECL2 interactions differ from OTV2.

### Finding 2: These coupling differences are preserved in human postmortem brain tissue

The same compounds were tested in human PFC tissue using SPA. The results broadly confirmed the cell-based data:

- Nitro-I activated Gαi1, Gαi3, and Gαq/11
- Met-I showed inverse agonism at Gαi1 (reducing basal Gαi1 activity below baseline) while acting as an agonist at Gαi3
- OTV1 showed inverse Gαi1 agonism and agonism at Gαi3 and Gαq/11
- OTV2 showed agonism across Gαi1, Gαi2, Gαi3, and Gαq/11

Notably, Met-I and OTV1 behaved as inverse agonists at Gαi1 in human brain tissue — a finding not fully reflected in the cell-based assays — likely because expression levels of G protein subtypes differ between cell lines and brain tissue, and because the presence of receptor heteromers in tissue can alter coupling profiles.

All effects were confirmed as 5-HT2AR-mediated by their partial or full reversal with MDL-11,939, and by their absence or alteration in 5-HT2AR KO mice.

### Finding 3: Gαi activation drives psychosis-related behavior (HTR)

When tested in vivo for head twitch response:

- **Nitro-I** (Gαq-biased) and **OTV2** (Gαi-biased) both **significantly increased HTR** in WT mice but not in 5-HT2AR KO mice — confirming 5-HT2AR-dependence
- **Met-I** and **OTV1** (which show inverse Gαi1 agonism in brain tissue) **did not increase HTR**
- Pharmacological inhibition of Gαq/11 (YM-254890 ICV) did NOT block OTV2-induced HTR
- Genetic knockdown of Gαi1 AND Gαi3 together via antisense ODNs **did block** OTV2-induced HTR

This pattern of results — only Gαi knockdown abrogates HTR, not Gαq inhibition — provides strong evidence that **Gαi/o family signaling is the mechanistic driver of psychosis-related (hallucinogenic) behavior via the 5-HT2AR**. The authors note this is consistent with earlier findings showing that hallucinogenic LSD stimulates Gαi/o coupling while the non-hallucinogenic analog lisuride does not.

### Finding 4: Gαq activation drives long-term memory deficits

In the novel object recognition test:

- **Met-I, OTV1, and OTV2** all induced significant **long-term memory deficits** in WT mice (lower discrimination index) in a 5-HT2AR-dependent manner (absent in KO mice)
- **Nitro-I did not impair memory** at any dose tested — despite being a Gαq agonist, it lacks significant ECL2 contacts and does not couple strongly to Gαi3 in brain tissue
- Pharmacological inhibition of Gαq/11 (YM-254890 ICV) **abrogated OTV2-induced memory deficits**
- Genetic knockdown of Gαi1/Gαi3 did **not** rescue the memory deficits

This clearly separates the memory phenotype from the psychosis phenotype at the mechanistic level: **Gαq pathway activation via 5-HT2AR is the driver of long-term memory impairment**. The data also suggest co-factors may be required beyond Gαq activation alone, since Nitro-I activates Gαq but does not impair memory — suggesting the pattern of G protein activation matters.

### Finding 5: ECL2 contacts in MD simulations predict in vivo behavioral divergence

The molecular dynamics simulations reveal a structural explanation for why these compounds have different coupling profiles. All four compounds share the same core tryptamine scaffold and occupy the orthosteric binding site with virtually identical contacts at key residues (D3.32, V3.33, S3.36, S5.46, F6.51, F6.52, N6.55 — the canonical aminergic receptor binding pocket). The critical difference is in their contacts with **extracellular loop 2 (ECL2)**, particularly residues L228, L229, and A230.

- **Nitro-I:** minimal ECL2 contacts; primarily orthosteric pocket
- **Met-I, OTV1, OTV2:** progressively more ECL2 contacts, especially with L228/L229/A230
- **OTV2** (phenoxy at position 5): highest ECL2 contact frequency, driven by hydrophobic interactions with L228 and L229 plus additional hydrogen bonds at the ECL2 backbone
- **OTV1** (benzodioxan at position 5): contacts ECL2 via polar interactions involving L229

The authors propose that increased ECL2 interaction drives the shift toward Gαi family coupling and away from Gαq. This is mechanistically consistent with a prior study by Wacker et al. showing that mutational modifications in ECL2 of 5-HT2BR alter ligand binding kinetics and receptor response. It is also consistent with structural data on LSD (which strongly contacts ECL2 via its diethylamine group and shows Gαi/o coupling) vs. lisuride (minimal ECL2 contact, no Gαi/o coupling).

---

## 5. Significance & Implications

### Rewriting the pharmacology of 5-HT2AR

This paper is genuinely novel in two ways. First, it provides direct experimental evidence — in living cells, human brain tissue, and mouse behavior — that individual G protein subtypes downstream of the same receptor control distinct behavioral outputs. This had been hypothesized based on indirect evidence, but Kossatz et al. provide the most complete mechanistic case to date. Second, by connecting ECL2 structural contacts to G protein coupling bias to in vivo behavioral outcomes, the paper creates a drug design roadmap.

### Implications for schizophrenia drug development

The implications are clinically significant. Current atypical antipsychotics (like clozapine and risperidone) inhibit the 5-HT2AR non-selectively. If psychosis is driven by Gαi and memory deficits are driven by Gαq, then:

- A **Gαi-biased inverse agonist or antagonist** at 5-HT2AR could selectively reduce psychosis-related symptoms without disrupting Gαq-mediated processes
- A **Gαq-selective partial agonist** or Gαq inhibitor might be explored to address cognitive symptoms without triggering hallucinations
- Current antipsychotics that indiscriminately suppress all 5-HT2AR signaling are potentially suppressing the Gαq pathway that regulates memory, which could explain why cognitive symptoms remain untreated

The finding that fully blocking Gαq/11 is linked to impaired mGlu2R regulation further underscores why indiscriminate inactivation is problematic.

### Connection to your BioChemCore work

This paper is directly relevant to your project. The 5-HT2AR is a canonical post-synaptic CNS membrane protein — exactly the type of system BioChemCore is designed to model. The paper's MD simulation methodology closely mirrors what you are learning: starting from a PDB structure of an active-state receptor (PDB 6WHA for the Gαq-coupled form), building the lipid bilayer system (POPC), running multi-replica NVT simulations, and then performing contact frequency analysis on trajectory clusters. The CHARMM force field they use is the same family (CHARMM36m) as in your BioChemCore pipeline.

The ECL2 finding is especially relevant for structural interpretation in MD contexts. When you analyze your own 5-HT2AR simulation, ECL2 dynamics and its contacts with bound ligands or the lipid headgroups will be an informative target. ECL2 acts as a "gating" element that modulates ligand kinetics and G protein coupling — understanding its flexibility in your trajectory (RMSF analysis) would directly connect to this paper's conclusions.

The paper also demonstrates how MD snapshots can be used to build mechanistic hypotheses that are then tested experimentally — a workflow that exemplifies the "biology-first" principle of BioChemCore.

---

## 6. Limitations & Open Questions

**Methodological limitations the authors acknowledge:**

- The GTPγS SPA assay uses a single submaximal concentration (10 µM) for brain tissue experiments, which is technically informative but means formal bias factors cannot be calculated across different subunits (because each antibody immunoprecipitation detects a different Gα with different sensitivity/stoichiometry). Only within-subunit comparisons are valid.

- Cross-reactivity of the antisense ODNs used to knock down Gαi1 and Gαi3 was observed — the Gαi1 ODN also partially reduced Gαi3 levels, and vice versa. This means the study cannot cleanly discriminate Gαi1-mediated from Gαi3-mediated effects with the current tools; they discuss both together as Gαi/o.

- The OTV2 HTR result could in principle involve mechanisms beyond Gαi1/3 — other coupling partners including Gαs proteins, Gβγ subunits, and β-arrestins have been reported to contribute to HTR in other studies. The paper makes a strong case for Gαi involvement but cannot exclude all contributions.

- The MD simulations use a POPC lipid bilayer, which is a simplified membrane composition. Real neuronal membranes contain cholesterol, sphingolipids, PIP2, and other lipids that influence GPCR conformation and G protein coupling. This simplification is practically necessary but limits the direct translatability of structural insights to native membrane behavior.

- Only male mice were tested in behavioral experiments. Sex differences in 5-HT2AR signaling are well-documented and not addressed here.

**Open questions:**

- What is the precise mechanism by which ECL2 contacts shift G protein preference? The paper provides correlative evidence, but direct mutagenesis of ECL2 residues (L228, L229, A230) to abolish OTV2 contacts would be the decisive experiment.

- Do the same pathway-behavior relationships hold in female animals, in aged animals, or in genetic mouse models of schizophrenia?

- Can a truly Gαi-selective inverse agonist at 5-HT2AR improve positive symptoms in preclinical models without causing cognitive side effects? This is the immediate therapeutic follow-up question the paper opens.

- The paper focuses on dorsolateral PFC. Different brain regions express different ratios of G protein subtypes, and the same 5-HT2AR agonist might couple differently in hippocampus vs. cortex. Region-specific coupling profiles remain to be mapped.

---

## 7. Key Terms & Concepts

**G protein-coupled receptor (GPCR):** A large superfamily of seven-transmembrane-helix cell surface receptors that, upon ligand binding, activate heterotrimeric G proteins (composed of Gα, Gβ, Gγ subunits) and β-arrestins to initiate intracellular signaling cascades; GPCRs are the target of ~30-40% of marketed drugs.

**Biased agonism (functional selectivity / pathway bias):** The property of a ligand that allows it to preferentially activate one downstream signaling pathway over another at the same receptor, relative to the endogenous agonist — enabling selective engagement of therapeutically beneficial pathways while avoiding harmful ones.

**Gαq vs. Gαi:** Two major families of Gα subunit. Gαq activates phospholipase C, leading to IP3/DAG production and calcium release. Gαi inhibits adenylyl cyclase, reducing cAMP levels. These two families often produce opposing or distinct downstream effects. In this paper, Gαq activation drives memory deficits while Gαi activation drives psychosis-related behavior, both via 5-HT2AR.

**Extracellular loop 2 (ECL2):** A flexible loop on the extracellular face of GPCRs that sits above the orthosteric binding pocket. ECL2 is a key modulator of ligand entry/exit kinetics and, as this paper demonstrates, of G protein coupling selectivity — more ECL2 contact correlates with Gαi family preference.

**Head twitch response (HTR):** A stereotyped rapid head rotation in rodents induced by serotonergic hallucinogens acting at 5-HT2AR; used as a translational proxy for the hallucinogenic/pro-psychotic potential of 5-HT2AR agonists.

**BRET (Bioluminescence Resonance Energy Transfer):** A proximity-based biosensor technique in which a bioluminescent donor enzyme (RlucII) transfers energy to a fluorescent acceptor (rGFP) only when they are brought within ~10 nm of each other — used here in the enhanced bystander format (ebBRET) to detect G protein activation and β-arrestin recruitment at the plasma membrane in living cells.

**[35S]GTPγS binding assay:** A radioligand binding technique that measures G protein activation in membrane homogenates; GTPγS is a non-hydrolyzable GTP analog that becomes permanently incorporated into activated Gα subunits, providing a stable, quantifiable readout of receptor-mediated G protein activation in native tissue.

---

*Summary prepared for BioChemCore context — 5-HT2AR molecular dynamics project, UCSD Bioinformatics Year 2.*
