# Cameron et al., 2021 — A Non-Hallucinogenic Psychedelic Analog with Therapeutic Potential

**Citation:** Cameron LP, Tombari RJ, Lu J, et al. *Nature.* 2021 January; 589(7842): 474–479. doi:10.1038/s41586-020-3008-z.

---

## One-Sentence Takeaway

By systematically stripping ibogaine down to its essential structural features and redesigning the molecule, researchers created tabernanthalog (TBG) — a water-soluble, non-hallucinogenic, non-toxic ibogaine analog that promotes neural plasticity and reduces addiction-related behaviors in rodents after a single dose.

---

## Background & Motivation

Ibogaine is a psychedelic alkaloid extracted from the West African plant *Tabernanthe iboga*, and it has attracted intense interest because anecdotal reports and small open-label studies suggest it can dramatically reduce cravings and prevent relapse across multiple substances — opiates, alcohol, and psychostimulants — in ways that most current addiction medications cannot. This broad-spectrum anti-addictive potential is remarkable because most approved substance use disorder (SUD) treatments are drug-specific (e.g., methadone only works for opioids).

The leading hypothesis for why ibogaine works so durably — often after just a single administration — is that it does not simply block the target drug's receptor. Instead, it is thought to rewire the neural circuits underlying addiction by promoting what researchers call **structural and functional neural plasticity**: physical growth of neurons in regions of the brain involved in motivation and reward, particularly the prefrontal cortex (PFC). This same mechanism has been proposed for other psychoplastogens — a class of compounds that promote neuronal growth — including psilocybin, LSD, and ketamine.

The problem is that ibogaine is genuinely dangerous as a medicine. It is highly non-polar (fat-soluble), meaning it accumulates in fatty tissue and is hard to dose precisely. It causes potentially fatal cardiac arrhythmias by blocking a critical potassium channel in the heart called **hERG** (human ether-à-go-go-related gene). Several deaths have been directly linked to ibogaine treatment. It also causes hallucinations lasting more than 24 hours, which creates serious practical and regulatory barriers to clinical use. The synthesis of ibogaine from scratch is complex (9–16 steps, yields of 0.1–4.8%), and the plant source is becoming over-exploited. These combined problems — toxicity, hallucinations, poor formulation properties, and difficult synthesis — have blocked ibogaine from being developed as a legitimate medicine despite its compelling anti-addictive potential.

The researchers asked a fundamental question: which parts of ibogaine's complex molecular structure are actually responsible for its therapeutic effects, and which parts are responsible for its toxicity and hallucinations? If those features could be separated, a safer drug could be engineered.

---

## Approach & Methods

### Function-Oriented Synthesis (FOS): The Core Strategy

The team used a strategy called **function-oriented synthesis (FOS)**, which means working backward from a biological function to identify the minimum molecular structure needed to produce that function. Rather than trying to make ibogaine safer by tweaking it at the margins, they systematically dismantled its structure and tested each stripped-down version to find the essential pharmacophore — the part of the molecule responsible for its desired biological activity (neuroplasticity promotion).

Ibogaine's architecture has three main features: an **indole ring** (an aromatic nitrogen-containing ring found in many neurotransmitters including serotonin), a **7-membered tetrahydroazepine ring**, and a **bicyclic isoquinuclidine scaffold**. By synthesizing a library of analogs called "ibogalogs" that systematically lack one or more of these features, they could test which structural elements are required for psychoplastogenic activity.

This approach mirrored seminal FOS work done on bryostatin 1, a structurally complex marine natural product, by Wender and colleagues — a precedent that showed you can often dramatically simplify a natural product while retaining its key biological activity.

### Assays Used

The researchers ran a comprehensive battery of tests at each stage:

**For psychoplastogenic activity (the desired therapeutic mechanism):**
- **Dendritogenesis assay:** Rat embryonic cortical neurons were treated with compounds and dendritic arbor complexity was measured using Sholl analysis (counting how many times the dendrites cross concentric circles drawn around the neuron's center). More crossings = more complex, branched dendrites.
- **Spinogenesis assay:** Mature cortical neurons (DIV20) were assessed for dendritic spine density — the small protrusions on dendrites where most excitatory synapses form.
- **In vivo spine dynamics:** Transcranial two-photon microscopy in live mice allowed direct imaging of the same dendritic spines before and 24 hours after drug administration.

**For safety:**
- **Head-twitch response (HTR) in mice:** The gold-standard rodent proxy for hallucinogenic potential. 5-HT2A agonists like 5-MeO-DMT produce a rapid, involuntary head-twitch that correlates with hallucinogenic potency in humans.
- **hERG channel inhibition:** Patch-clamp electrophysiology in HEK293 cells stably expressing the hERG channel, directly measuring IC50 values.
- **Larval zebrafish cardiac assay:** Zebrafish express Zerg (the hERG ortholog), and hERG inhibitors cause bradycardia (slowed heart rate) and arrhythmia in larvae. Heart rate and the ratio of atrial to ventricular beats were measured.
- **Larval zebrafish behavioral profiling:** A high-throughput behavioral assay that classifies drug effects in zebrafish using machine learning. Compounds that produce behavioral profiles resembling a lethal control (eugenol) are flagged as dangerous; compounds resembling vehicle control are considered safer.
- **Zebrafish developmental toxicity:** Larval zebrafish were exposed from 6 hours post-fertilization (hpf) through 5 days post-fertilization (dpf) and assessed for malformations and mortality.
- **Safety pharmacology panel:** TBG was screened against 81 potential molecular targets by Eurofins Discovery.

**For receptor pharmacology:**
- A comprehensive panel of serotonin (5-HT) and opioid receptor functional assays measuring canonical GPCR signaling (Gq-mediated calcium flux for 5-HT2 receptors, Gi/Go-mediated cAMP inhibition, beta-arrestin recruitment, etc.).

**For behavioral/therapeutic effects in rodents:**
- Conditioned place preference (CPP) for abuse liability
- Forced swim test (FST) after unpredictable mild stress (UMS) for antidepressant effects
- Intermittent access two-bottle choice for alcohol intake (binge drinking model)
- Heroin self-administration (SA), extinction, and cued reinstatement in rats
- Sucrose preference and self-administration as anhedonia/non-specific controls

---

## Key Findings

### 1. The Tetrahydroazepine Ring is the Critical Structural Element

The systematic ibogalog testing revealed a clear pattern: analogs that retained the **indole-fused tetrahydroazepine** were consistently good psychoplastogens, while analogs that retained the isoquinuclidine but lacked the tetrahydroazepine were weak or inactive. This was the key structural discovery that guided the rest of the work. It told the researchers that ibogaine's complex isoquinuclidine cage — which contributes heavily to its synthesis difficulty, lipophilicity, and toxicity — is not what's doing the therapeutic work.

The "winning" simplified analog was **IBG (ibogainalog, compound 13)**, which retained psychoplastogenic activity comparable to ibogaine despite having a simpler structure. Crucially, it had a much lower cLogP (2.61) compared to ibogaine (4.27), meaning it is more water-soluble — already a major practical and safety improvement.

### 2. TBG is Non-Hallucinogenic

Noticing that IBG resembled the potent 5-HT2A agonist 5-MeO-DMT, and knowing from prior structure-activity relationship (SAR) work that adding a 6-methoxy substituent (yielding 6-MeO-DMT) abolishes the hallucinogenic drug-discrimination response in rodents without eliminating 5-HT2A activity, the team synthesized **TBG (tabernanthalog, compound 18)** — the 6-methoxyindole-fused tetrahydroazepine. This is structurally analogous to the iboga alkaloid tabernanthine.

The head-twitch response results were clear: 5-MeO-DMT (positive control) produced a robust HTR; IBG produced a significantly reduced but non-zero HTR; TBG produced no detectable HTR at any tested dose (up to 50 mg/kg). TBG is non-hallucinogenic by this measure.

### 3. TBG has a Dramatically Improved Cardiac Safety Profile

Ibogaine inhibits hERG channels with an IC50 of 1.09 μM — a potency that explains its documented cardiotoxicity in humans. IBG is approximately 10-fold less potent (IC50 = 19.3 μM) and TBG is approximately 100-fold less potent (IC50 = 148 μM) than ibogaine at hERG. In the zebrafish cardiac assay, ibogaine and noribogaine caused bradycardia and increased arrhythmia scores; IBG and TBG did not. In the larval zebrafish developmental toxicity assay, ibogaine (100 μM) caused significant malformations and mortality at 2 and 5 dpf. TBG at 100 μM also caused some toxicity, but reducing the dose to 66 μM made TBG statistically indistinguishable from vehicle control in terms of viability at 5 dpf.

In addition, TBG is an antagonist at 5-HT2B receptors (rather than an agonist like 5-MeO-DMT), which is important because 5-HT2B agonism has been linked to cardiac valvulopathy. TBG therefore avoids two distinct cardiac liability mechanisms simultaneously.

### 4. TBG is a Selective, Potent 5-HT2A Agonist

The receptor panel revealed that IBG and TBG are potent agonists at human 5-HT2A receptors (EC50 values in the nanomolar range) and are actually more selective for 5-HT2A compared to the conformationally unrestricted 5-MeO-DMT, which hits many serotonin receptor subtypes. The safety screen across 81 targets confirmed that TBG's primary binding activity is at 5-HT2 receptors (5-HT1B, 5-HT2A, 5-HT2B, and 5-HT2C had ≥50% inhibition; SERT also showed 88% inhibition at 10 μM, though the functional consequence of this warrants further study). TBG showed no meaningful opioid receptor agonist activity, distinguishing it from noribogaine.

The authors note that TBG's 5-HT2B antagonism (versus agonism for most classic psychedelics) is a unique and favorable feature. The dendritogenesis effect of TBG was blocked by pretreatment with the 5-HT2A antagonist ketanserin, confirming that the plasticity-promoting effects are 5-HT2A-dependent.

### 5. TBG Promotes Structural Neural Plasticity In Vitro and In Vivo

TBG significantly increased dendritic arbor complexity in rat embryonic cortical neurons (DIV6), comparable to ibogaine and ketamine (positive controls). It also increased dendritic spine density in mature cortical neurons (DIV20) to an extent comparable to ibogaine. In the transcranial two-photon imaging experiment in live mice, TBG increased spine formation in the primary sensory cortex 24 hours after administration, without affecting spine elimination. This matches the pattern seen with the hallucinogenic 5-HT2A agonist DOI (2,5-dimethoxy-4-iodoamphetamine), suggesting the plasticity-promoting effect is a general property of 5-HT2A agonism rather than a feature unique to hallucinogens.

### 6. TBG has Antidepressant-Like Effects in the FST

After a 7-day unpredictable mild stress (UMS) protocol, mice showed increased immobility in the forced swim test — a proxy for depressive-like behavior. TBG at 50 mg/kg (but not 10 mg/kg) rescued this effect when tested 24 hours after administration, comparable to ketamine. The effect was blocked by ketanserin (the 5-HT2A antagonist), confirming the mechanism. Pharmacokinetic data showed that the 50 mg/kg dose achieves substantially higher brain concentrations (~280 nmol/g brain at 15 minutes) than the 10 mg/kg dose, rapidly clearing to near-zero at 3 hours — consistent with the requirement for a brain-penetrant, transiently present compound that triggers lasting circuit-level changes rather than acting as a continuous occupant of 5-HT2A receptors.

In a head-to-head comparison with ketamine in unstressed mice, both TBG and ketamine reduced FST immobility at 24 hours post-administration. Ketamine's effects appeared more durable at 7 days, though TBG had no effect on locomotion (ruling out a confounding stimulant effect).

### 7. TBG Reduces Alcohol and Heroin-Seeking in Rodents

In the binge-drinking model (7 weeks of intermittent access to 20% ethanol), TBG administered 3 hours before a drinking session significantly reduced binge alcohol consumption during the first 4 hours and for at least 2 days following administration — without affecting water intake or (in a separate experiment) sucrose preference. This selectivity for alcohol over sucrose is important because it suggests TBG is not causing a generalized reduction in reward motivation or making animals feel sick.

In the heroin self-administration model, acute TBG treatment reduced active lever pressing and heroin intake when administered during self-administration (SA) and before extinction (EXT), as well as acutely during cued reinstatement (CUE). However, there is a critical nuance: TBG also acutely reduced sucrose self-administration at all three time points, suggesting its immediate effects on operant responding may not be drug-selective — it appears to generally disrupt goal-directed behavior in the short term.

The most compelling finding in the heroin model is the long-lasting, selective protection against relapse. When TBG had been administered during the SA or EXT phases (12–14 days before the cued reinstatement test), it significantly reduced cue-induced heroin-seeking. In contrast, TBG administered during the same time windows had no long-lasting effect on sucrose-seeking. This dissociation — lasting anti-heroin-seeking but not lasting anti-sucrose-seeking — suggests TBG exerts a long-lasting, addiction-specific effect that cannot be attributed to simple motor suppression or a general blunting of reward.

### 8. TBG has Low Abuse Potential

In the conditioned place preference (CPP) assay, a low dose of TBG (1 mg/kg) produced no place preference or aversion. Higher doses (10 and 50 mg/kg) produced a modest conditioned place aversion (CPA) rather than preference — the opposite of what addictive drugs do — suggesting TBG has a low abuse liability.

---

## Significance & Implications

This paper is a proof-of-concept that function-oriented synthesis can be used to rationally redesign a complex, toxic psychedelic natural product into a simpler, safer molecule that retains (and even improves) its key therapeutic properties. The significance operates on several levels.

**For drug development**, TBG demonstrates that it is possible to separate hallucinogenesis from neuroplasticity promotion in a 5-HT2A agonist. The 5-HT2A receptor is increasingly understood as a master regulator of neuroplasticity in the prefrontal cortex, and many in the field have assumed that psychedelic-induced neuroplasticity and hallucinogenesis are inextricably linked — because both seem to require 5-HT2A activation. TBG challenges that assumption by showing that the conformational restriction imposed by the tetrahydroazepine ring specifically eliminates hallucinogenesis while preserving plasticity promotion and 5-HT2A agonism.

**For the BioChemCore context**, this paper is directly relevant to your work on the 5-HT2A receptor. The 5-HT2A serotonin receptor is a prototypical post-synaptic CNS membrane protein and a class A GPCR. The paper's entire pharmacological rationale depends on understanding 5-HT2A's signaling (Gq-mediated calcium flux, which initiates downstream signaling cascades including PKC and MAPK pathways that regulate cytoskeletal dynamics — the molecular mechanism underlying dendritic growth and spine formation). When you simulate the 5-HT2A receptor in the BioChemCore program, you are working on precisely the molecular target that TBG acts through to produce all the behavioral effects described here. The receptor's transmembrane helices, orthosteric binding pocket, and the conformational changes it undergoes upon agonist binding are what distinguish TBG's "biased" agonism (promoting plasticity) from 5-MeO-DMT's agonism (producing hallucinations). The structural and conformational differences between ligands at the 5-HT2A binding site are what MD simulations can help illuminate at atomistic resolution.

**For the broader field of psychedelic medicine**, TBG represents a new molecular template. Ketamine is the only currently approved rapid-acting neuroplasticity-promoting antidepressant, and it has significant limitations (abuse potential, dissociation). TBG offers a potential path toward neuroplasticity-based treatments that lack these drawbacks.

**One important institutional note**: the lead author (DEO, David E. Olson) disclosed that he is president and chief scientific officer of Delix Therapeutics, which has licensed TBG-related technology from UC Davis. This commercial relationship is worth keeping in mind when evaluating enthusiasm in the paper's framing.

---

## Limitations & Open Questions

**The acute sucrose-seeking suppression is a real confound.** When TBG is given acutely, it suppresses sucrose self-administration just as much as heroin self-administration. This means the immediate "anti-addiction" effect seen right after dosing is almost certainly a non-selective disruption of motivated operant behavior — not a selective anti-addictive effect. The paper is honest about this but it complicates the interpretation of the acute results. The long-lasting heroin-specific protection is more convincing, but the mechanism for why TBG's lasting effects are selective for heroin-seeking but not sucrose-seeking is not established.

**The FST is a limited model of depression.** Forced swim immobility is a widely used proxy for antidepressant effects but is increasingly criticized as insufficient on its own. The paper acknowledges that future studies should evaluate TBG's effects on other depression-relevant behaviors, particularly anhedonia (loss of pleasure) — which sucrose preference would partly address, but the current data were collected in non-stressed mice, limiting the translation.

**The mechanism connecting neural plasticity to behavioral outcomes is unproven.** The paper assumes that TBG's ability to promote dendritic growth and spinogenesis is causally responsible for its antidepressant-like and anti-addictive behavioral effects, following the hypothesis established for ketamine and other psychoplastogens. However, the causal link between structural plasticity in the PFC and long-lasting behavioral change has not been established in rodents or humans for any psychedelic compound. The paper itself acknowledges in the Discussion that "a causal link between psychedelic-induced neuronal growth and behavior has yet to be established in either humans or rodents."

**All data are from rodents.** Human translation is unknown. Ibogaine's cardiac toxicity was not predicted from rodent studies, so the improved zebrafish and hERG data are reassuring but not definitive. The lack of lethal cardiac events at therapeutic doses in humans will require clinical trials to establish.

**SERT inhibition at high concentrations.** The safety screen showed 88% inhibition of SERT (the serotonin transporter — the target of SSRIs) at 10 μM TBG. This off-target activity has not been mechanistically characterized and could be relevant to both therapeutic effects and potential for serotonin syndrome at high doses.

**The 5-HT2A antagonist (ketanserin) blocks TBG's dendritic effects, but the downstream intracellular signaling hasn't been fully characterized.** It would be valuable to know whether TBG's plasticity effects involve canonical Gq signaling, beta-arrestin recruitment, or a biased agonism profile that differs from classical hallucinogens — this is where MD simulations of 5-HT2A with TBG bound versus other ligands could eventually make a contribution.

---

## Key Terms & Concepts

**Psychoplastogen:** A compound that promotes structural and functional neural plasticity — meaning it causes neurons to grow new dendrites and dendritic spines. The hypothesis is that this physical rewiring of brain circuits is what gives psychedelics and ketamine their long-lasting therapeutic effects.

**5-HT2A receptor:** A G protein-coupled receptor (GPCR) for serotonin expressed primarily on pyramidal neurons in the cortex. When activated, it couples to Gq protein, triggering phospholipase C and ultimately increasing intracellular calcium, which activates kinase cascades that regulate cytoskeletal growth. It is the primary molecular target through which classical psychedelics like LSD, psilocin, and DMT produce both their hallucinogenic and plasticity-promoting effects.

**hERG (human ether-à-go-go-related gene):** A potassium channel critical for repolarizing the cardiac action potential. Drugs that block hERG can cause the QT interval on an ECG to lengthen, which predisposes to a dangerous arrhythmia called torsades de pointes. hERG inhibition is one of the most common reasons drug candidates fail in development, and ibogaine's hERG inhibition (IC50 ~1 μM) is considered a primary cause of its cardiotoxicity.

**Function-oriented synthesis (FOS):** A drug design strategy that works backward from a biological function — identifying the minimum pharmacophore responsible for that function in a complex natural product, then synthesizing simplified analogs that retain function while eliminating structural complexity (and often toxicity).

**Head-twitch response (HTR):** A rapid, involuntary, rhythmic rotation of the head observed in rodents treated with serotonergic hallucinogens. It is caused by 5-HT2A receptor activation and serves as the standard preclinical proxy for hallucinogenic potential. The number of head twitches correlates with hallucinogenic potency across compounds in humans.

**Sholl analysis:** A method for quantifying neuronal branching complexity. Concentric circles of increasing radius are drawn around a neuron's soma, and the number of dendrite crossings at each radius is counted. A compound that increases branching produces higher crossing numbers (higher N_max), indicating more complex dendritic arbors.

**Dendritic spines:** Small, mushroom-shaped protrusions on dendrites that are the primary sites of excitatory synaptic input. Spine density correlates with the strength and number of synaptic connections a neuron makes. Loss of spines is a hallmark of depression and chronic stress; increasing spine density is thought to be a key mechanism of rapid antidepressants like ketamine.

---

*Summary saved to `/Users/zakiralibhai/Documents/papers/summaries/Cameron_2021_summary.md`*
