# The Promises and Perils of Psychedelic Pharmacology for Psychiatry

**Citation:** McClure-Begley, T.D. & Roth, B.L. (2022). *Nature Reviews Drug Discovery*, 21, 463–473. https://doi.org/10.1038/s41573-022-00421-7

---

## One-Sentence Takeaway

The 5-HT2A serotonin receptor is the central molecular target of classical psychedelic drugs, and while structural and clinical evidence supports their therapeutic promise for depression and anxiety, significant pharmacological complexity and methodological challenges must be resolved before psychedelic-inspired medicines can be reliably developed.

---

## Background & Motivation

Psychedelic drugs — psilocybin (the active ingredient in "magic mushrooms"), LSD, and DMT (N,N'-dimethyltryptamine) — are having a scientific renaissance after decades of legal suppression. Their potential to treat depression, anxiety, and other psychiatric conditions is generating enormous clinical and commercial interest: nearly 60 companies had already formed to exploit this space as of 2022.

The historical context matters here. Psychedelics were used in indigenous cultures for millennia and were subjects of active psychiatric research in the 1950s–60s, when they were used as adjuncts to psychotherapy. That research trajectory was interrupted by the 1970 Controlled Substances Act (CSA), which classified most psychedelics as Schedule I substances — defined as having high abuse potential and no accepted therapeutic use. This classification created both practical barriers to research (requiring special DEA licenses, restricting federal funding) and a chilling effect on the field for decades.

The scientific motivation for revisiting these drugs is compelling. Phase II clinical trials have now demonstrated that psilocybin can produce statistically significant reductions in depression and anxiety after just one or two administrations — an effect that can persist for up to six months. This is remarkable compared to conventional antidepressants, which require daily dosing and weeks to show effect. But a critical mechanistic gap remains: despite strong evidence that the 5-HT2A serotonin receptor mediates the behavioral effects of psychedelics, it is not clear which specific aspects of 5-HT2A signaling are responsible for therapeutic benefits, and whether those aspects can be separated from the hallucinogenic effects.

This paper by McClure-Begley and Roth (a DARPA researcher and one of the world's leading GPCR pharmacologists, respectively) is a perspectives piece — a synthesis of the current state of the field, written to orient both scientists and clinicians to what is known, what is contested, and what must be figured out.

---

## Approach & Methods

This is a review and perspectives article, not a primary research paper, so there is no single experimental design. Instead, the authors synthesize findings from multiple bodies of work:

- **Structural biology**: X-ray crystallography and cryogenic electron microscopy (cryo-EM) studies of LSD and 25CN-NBOMe bound to the 5-HT2A receptor, revealing how these drugs physically interact with the receptor at atomic resolution.
- **Receptor pharmacology**: Radioligand binding studies, G protein coupling assays, and arrestin interaction studies that characterize how psychedelics engage downstream signaling.
- **Animal behavioral models**: Head twitch response (HTR) assays and drug substitution paradigms used to predict psychedelic-like activity in rodents.
- **Clinical trial data**: Phase II trials of psilocybin for anxiety and depression in cancer patients, treatment-resistant depression, and a head-to-head comparison with escitalopram (a standard SSRI antidepressant).
- **Computational approaches**: Ultra-large-scale virtual docking of billions of molecules against 5-HT2A receptor structures to guide discovery of new ligands.

The authors are explicit about what the paper will and will not cover: they focus on classical psychedelics (LSD-like drugs) acting via defined receptors, and they deliberately exclude MDMA-related studies, which involve different mechanisms.

---

## Key Findings

### 1. The 5-HT2A receptor is the essential molecular target — but it is not the only one

Virtually all classical psychedelics are agonists at the 5-HT2A serotonin receptor, and this activity is necessary for their psychedelic effects. The evidence is strong:

- Transgenic mice that lack 5-HT2A receptors (knockout mice) do not show psychedelic-like behaviors in response to LSD or psilocybin.
- The 5-HT2A-preferring antagonist ketanserin blocks the behavioral effects of LSD and psilocybin in both mice and humans.
- There is a linear correlation between a drug's binding affinity for cortical 5-HT2A receptors and the dose required to produce discriminative effects in rats.

However, LSD is also an agonist at 12 of the 14 human 5-HT receptor subtypes, and at all five dopamine receptors (D1–D5), and at alpha-adrenergic receptors, and at trace amine receptors (TAAR1). Figure 2 in the paper displays a phylogram of the entire human GPCR superfamily with LSD's high-affinity targets marked — the reach is striking. This "polypharmacology" complicates mechanistic conclusions: you cannot simply assume that any observed effect is 5-HT2A-mediated.

### 2. Structural biology has revealed why LSD acts the way it does

Recent X-ray and cryo-EM structures of the 5-HT2A receptor bound to LSD have answered longstanding questions about LSD's unusually long duration of action and slow receptor dissociation kinetics.

The key structural finding is that LSD's diethylamide moiety interacts with Leu229 in extracellular loop 2 (EL2) of the receptor, forming what the authors call a "lid" over the binding pocket. This lid physically traps LSD inside the receptor, dramatically slowing its dissociation rate (koff = 0.003 min⁻¹ for wild-type vs. 0.014 min⁻¹ when the critical Ser242 residue is mutated). This slow dissociation is the structural explanation for LSD's famously long and intense effects.

A separate but important finding concerns a species difference that has bedeviled researchers: rodents have an alanine at position 242 in the 5-HT2A receptor, whereas humans have a serine (Ser242). This single amino acid difference reduces the potency of many hallucinogens — including tryptamines and ergotamines — at rodent receptors, which means rodent behavioral assays may underestimate the potency of psychedelics in humans. This is a real limitation for translating animal data to clinical predictions.

The structures also showed that 5-HT2A receptors couple selectively to Gq-family G proteins (specifically Gq, G11, and G15), with minimal interaction with other G protein subtypes. This selectivity has implications for which intracellular signaling cascades are activated downstream.

### 3. 5-HT2A receptor signaling drives spinogenesis and synaptic plasticity — a plausible therapeutic mechanism

One of the most exciting recent findings, discussed at length, is that psychedelics promote dendritic spine formation (spinogenesis) in cortical neurons in vitro and in vivo by activating 5-HT2A receptors. Dendritic spines are the small protrusions on neurons where most excitatory synapses form; their density and morphology are strongly linked to learning, memory, and mood regulation. Depression is associated with reduced spine density.

The signaling cascade works as follows: psilocybin is dephosphorylated to psilocin in the body, which then crosses the blood-brain barrier and activates 5-HT2A receptors on Layer V cortical pyramidal neurons (the deep output neurons of the cortex). Receptor activation drives Gq-mediated signaling, triggering phospholipase C activity, which generates IP3 (inositol trisphosphate) and DAG (diacylglycerol). This activates downstream kinases and ion channels. The net result includes enhanced neuronal excitability and, ultimately, structural changes: the growth of new dendritic spines.

Critically, this spinogenesis effect requires not just the 5-HT2A receptor but also its interaction with synaptic scaffolding proteins at post-synaptic densities — specifically PDZ-domain proteins. Mice in which 5-HT2A receptors cannot interact with these scaffolding proteins show attenuated psychedelic-induced effects on pre-pulse inhibition (a measure of sensory gating). This implies that the receptor's location at the synapse, embedded in a specific protein complex, matters — not just receptor activation per se.

This finding directly connects to non-psychedelic antidepressants: conventional antidepressants like SSRIs also induce spine formation, suggesting convergent mechanisms for mood improvement despite completely different pharmacology.

### 4. Phase II clinical trials show promise but have significant limitations

Table 1 summarizes three key trials:

- **Psilocybin vs. niacin for anxiety/depression in cancer patients** (n=29): statistically significant improvements in both anxiety and depression.
- **Low-dose vs. high-dose psilocybin for anxiety/depression in cancer patients** (n=51): significant improvements in both groups.
- **Psilocybin vs. escitalopram for depression** (n=59): significant improvements for both treatments; the secondary analysis appeared to favor psilocybin, but the study was underpowered to detect superiority of either treatment.

These results led to psilocybin receiving FDA Breakthrough Therapy designation for depression and treatment-resistant depression. However, the authors are refreshingly candid about the limitations:

- All trials are small (phase II scale).
- High exclusion rates: up to 96.3% of initially screened individuals were disqualified (due to history of psychosis, schizophrenia, bipolar disorder, active antidepressant use, etc.), meaning trials are studying a highly selected subset of the population that would actually seek treatment.
- Most trials are not placebo-controlled in the conventional sense, because the subjective effects of psilocybin make true blinding nearly impossible.
- The therapeutic effect may require a specific "set and setting" — the psychological context in which the drug is administered — which is difficult to standardize or replicate across clinics.
- Potential drug interactions: antidepressants (particularly SSRIs) may blunt psilocybin's effects, but the mechanism is unknown.

### 5. Off-target risks are real and mechanistically understood

The 5-HT2B receptor — the "off-target" that poses the most serious safety concern — mediates valvular heart disease when chronically activated. LSD and psilocin are both potent 5-HT2B agonists. Drugs that activate 5-HT2B receptors chronically (like the diet drugs fenfluramine/benfluorex, the ergot derivatives ergotamine and methysergide, and MDMA) have been definitively linked to valvular heart disease in humans. This is a legitimate concern if microdosing (chronic low-dose use) becomes widespread.

Additionally, most psychedelics can trigger serotonin syndrome — a potentially fatal constellation of symptoms from excessive serotonin receptor activation — if co-administered with serotonergic antidepressants or anti-migraine drugs.

### 6. Non-psychedelic analogs are a promising but not-yet-proven path

A major open question is whether the subjective psychedelic experience (hallucinations, altered consciousness) is *necessary* for therapeutic benefit, or whether it is merely a side effect of the pharmacology responsible for the actual healing. If the hallucinations can be separated from the antidepressant effect, it would dramatically expand the clinical utility and accessibility of these drugs.

The authors discuss tabernanthalog (TBG), a synthetic compound derived from ibogaine that lacks significant 5-HT2A activity, shows antidepressant and anxiolytic effects in animal models, and does not produce hallucinogen-like behavior (HTR) in mice. However, its actions in vivo were partially blocked by the 5-HT2A antagonist ketanserin — meaning its mechanism remains incompletely understood, possibly involving indirect effects on 5-HT2A signaling rather than direct agonism.

They also discuss a new biosensor called PsychLight, in which a circularly permuted GFP was inserted into the 5-HT2A receptor. This sensor can distinguish psychedelic from non-psychedelic 5-HT2A agonists in vitro, and was used to discover AAZ-134, a tryptamine derivative with antagonist activity at 5-HT2A and antidepressant-like actions in mice. The utility of PsychLight is its potential to screen large compound libraries for biased 5-HT2A engagement.

---

## Significance & Implications

This paper is directly relevant to your BioChemCore project because the 5-HT2A receptor — the protein you are most likely simulating — is the central protagonist of the entire paper.

**For your MD simulation work**, the structural findings here are of immediate practical relevance:

- The X-ray and cryo-EM structures of 5-HT2A bound to LSD (Wacker et al. 2017, Nat. Struct. Mol. Biol.; and the Roth lab's 2020 structure of the full signaling complex) provide the atomic-resolution starting points for simulation. The paper's discussion of Ser242 in the binding pocket, the extracellular loop 2 conformation that creates LSD's "lid," and the selective Gq coupling interface are all structurally characterized features you would see in those PDB structures.

- The signaling cascade described — 5-HT2A → Gq → phospholipase C → IP3 + DAG → PKC → spinogenesis — is a textbook example of GPCR-mediated signal transduction. The TM helix rearrangements that enable G protein coupling, the role of the second and third intracellular loops, and the receptor's interaction with PDZ scaffolding proteins are all dynamics accessible (at least partially) via MD simulation.

- The species difference at position 242 (Ala in rodents, Ser in humans) is a concrete example of how a single amino acid in the binding pocket can alter drug residence time — something directly visible in simulation as altered hydrogen bonding or hydrophobic contacts.

**For the broader field**, this paper argues that the pharmacological complexity of psychedelics — their polypharmacology, the difficulty of separating psychedelic from therapeutic effects, the context-dependence of their actions — means that future drug development will require precision tools. Ultra-large-scale computational docking, structure-guided medicinal chemistry, and biased agonism (designing molecules that preferentially activate some downstream pathways over others) are presented as the path forward.

The paper also makes an important policy and scientific sociology point: the CSA's Schedule I classification of psychedelics for 50+ years genuinely slowed research, and the current resurgence is only possible because the clinical evidence finally became strong enough to overcome the regulatory and reputational barriers.

---

## Limitations & Open Questions

The authors themselves are admirably forthcoming about what is not yet known:

**Mechanistic gaps:**
- It is not known whether the subjective psychedelic experience is necessary for therapeutic benefit. This is arguably the most important open question in the field.
- The precise intracellular signaling pathway responsible for spinogenesis — and whether it is the same pathway responsible for hallucinations — has not been conclusively identified.
- The role of beta-arrestin (a non-G-protein signaling pathway that is also activated by 5-HT2A) versus canonical Gq signaling in therapeutic effects is unresolved.

**Clinical limitations:**
- All existing trials are small (phase II). No phase III trials are yet complete.
- The extreme exclusion criteria mean we have essentially no safety or efficacy data for psilocybin in people with comorbidities — the very population most likely to seek treatment.
- The interaction between psilocybin and antidepressants (which millions of people take daily) is uncharacterized beyond observational reports of attenuation.
- Long-term durability data beyond 6 months is minimal.

**Translational limitations:**
- The Ala/Ser242 species difference means rodent behavioral models may systematically misrepresent human pharmacology for many tryptamine-class compounds.
- The HTR assay has both false positives (non-psychedelic compounds can induce head twitch) and limitations in predicting human psychedelic potency.

**One notable gap the authors understate:** The paper acknowledges but does not deeply explore how the "set and setting" — the psychological environment of the psychedelic experience — contributes to outcomes. Clinical trials require therapeutic support sessions before, during, and after drug administration. It is genuinely unclear how much of the measured benefit is pharmacological versus psychotherapeutic, and this confound is very hard to control for.

---

## Key Terms & Concepts

**5-HT2A receptor** — A G protein-coupled receptor (GPCR) in the serotonin receptor family, expressed primarily on Layer V cortical pyramidal neurons; the principal molecular target through which classical psychedelics produce their behavioral effects.

**Polypharmacology** — The property of a drug that allows it to bind to and activate multiple receptor targets simultaneously; LSD, for example, has high affinity for 12 of 14 serotonin receptors, all 5 dopamine receptors, and several adrenergic receptors, making it extremely difficult to attribute any single effect to any single receptor.

**Biased agonism (functional selectivity)** — The property of some receptor ligands that preferentially activate one downstream signaling pathway over another at the same receptor; at 5-HT2A, a biased agonist might activate Gq without activating beta-arrestin, or vice versa. This concept underpins the hope of separating therapeutic from hallucinogenic effects.

**Spinogenesis** — The formation of new dendritic spines on neurons; psychedelics and (via different mechanisms) conventional antidepressants both promote spinogenesis, suggesting this structural plasticity is part of the therapeutic mechanism for depression.

**Head twitch response (HTR)** — A rapid, repetitive rotational head movement in rodents induced by 5-HT2A receptor activation; it is the primary animal behavioral surrogate for predicting psychedelic-like drug action, though it has both false positives and species-specific limitations.

**PDZ scaffolding proteins / post-synaptic density** — Structural proteins at synapses that organize and anchor receptors, ion channels, and signaling enzymes into functional complexes; 5-HT2A receptors interact with these scaffolds, and this interaction is required for some of the receptor's behavioral effects.

**Schedule I (CSA)** — The most restrictive category under the US Controlled Substances Act, designating substances with high abuse potential and no accepted medical use; most psychedelics fall here, which historically required special DEA licensure for research and prohibited federal funding that "promotes legalization."

---

*Summary prepared for BioChemCore program context. The 5-HT2A receptor's structural features described here — particularly the binding pocket geometry, Ser242, EL2 conformation, and Gq coupling interface — are directly relevant to MD simulation setup and analysis.*
