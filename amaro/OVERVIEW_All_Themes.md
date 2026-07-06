# BioChemCore Reading List — Master Overview

**33 papers across 4 themes | Prepared for BioChemCore, June 2026**

---

## One-Sentence Takeaway

The 5-HT2A serotonin receptor is a molecular switch that can be tuned — by different drugs, different conformations, and different membrane environments — to produce outcomes ranging from hallucinations to lasting antidepressant neuroplasticity, and your MD simulation is the tool that can reveal how that tuning works at the atomic level.

---

## The Story in Five Minutes

Imagine a single protein, seven helices threaded through a neuron's membrane in the prefrontal cortex. Serotonin arrives. The protein shifts shape. Depending on exactly *how* it shifts — which helix moves, which loop closes, which intracellular pocket opens — completely different things happen inside the cell. One conformation triggers a signaling cascade that rebuilds withered dendritic spines. Another triggers hallucinations. A third does both. A fourth does neither.

That protein is the **5-HT2A serotonin receptor**, and these 33 papers collectively tell you everything the field currently knows about how it works, why it matters, and how to simulate it.

Here is the arc:

**Act 1 — The clinical surprise.** Psilocybin, given once or twice under therapeutic supervision, produces antidepressant effects that last months — in patients who had failed every other treatment (Griffiths 2016, Carhart-Harris 2018). The effect sizes are 3-4x larger than conventional antidepressants. Something fundamentally different is happening at the molecular level.

**Act 2 — The mechanism.** That "something different" is neuroplasticity. Psychedelics physically rebuild atrophied neurons in the prefrontal cortex — growing new dendritic spines and forming new synapses within 24 hours of a single dose (Ly 2018). The entire effect requires the 5-HT2A receptor. Block it, and nothing happens. Knock it out genetically, and nothing happens. The receptor is the gatekeeper.

**Act 3 — The conformation problem.** But here's the catch: the same receptor that drives therapeutic neuroplasticity also drives hallucinations. Both require 5-HT2A activation. So how do you get one without the other? The answer is **biased agonism** — different drugs stabilize different receptor conformations, and different conformations preferentially activate different downstream signaling pathways (Urban 2007). A drug that nudges the receptor into *just the right* shape can promote spine growth without triggering the perceptual storm.

**Act 4 — The structural revolution.** Cryo-EM structures now show, at atomic resolution, what those different shapes look like (Cao 2022, Gumpper 2025, Xu 2026). The toggle switch residue W336 in TM6 flips between rotameric states. The NPxxY motif in TM7 shifts. ECL2 closes like a lid over LSD. A non-canonical intermediate state — partially active, compatible with beta-arrestin but not full Gq coupling — has been captured for the first time. MD simulations reveal the dynamics between these states that no single frozen structure can show (Viohl 2025, Peeters 2025).

**Act 5 — The design payoff.** Armed with structural knowledge, chemists have now engineered compounds that separate hallucination from therapy. Tabernanthalog (TBG) promotes plasticity without hallucinations, without glutamate bursts, without immediate early gene activation (Cameron 2021, Aarrestad 2025). JRT, an LSD analogue differing by just two atoms, eliminates hallucinogenicity while retaining full neuroplastic potency — by breaking a single hydrogen bond to S242 in the binding pocket (Tuck 2025). Two atoms. One angstrom. Completely different clinical profile.

**Your role:** You are simulating the protein at the center of this entire story. Your MD trajectory captures the conformational dynamics that determine whether a drug heals or hallucinates. The membrane you build in CHARMM-GUI, the residues you monitor in MDAnalysis, the helix movements you track — all of it connects directly to the biology and pharmacology described across these 33 papers.

---

## How the Four Themes Connect

The themes are not four independent topics. They are four layers of the same system, from broadest context to atomic detail.

### Layer 1: Serotonin Biology & MD Tools (5 papers)

**What it covers:** The widest lens. What serotonin actually does across the body (it's 95% in the gut, not the brain). What the 5-HT2A receptor does when drugs bind it (functional selectivity — the same drug can be an agonist in one cell and an antagonist in another). How serotonin fluctuates at the receptor in real time (millisecond bursts during fear, sleep, social interaction). And on the computational side: how to run OpenMM simulations efficiently (MPS for GPU throughput) and how to compute drug binding kinetics that are beyond the reach of standard MD (SEEKR2 milestoning).

**Why it matters for BioChemCore:** This is your "before you start" context. You need to know what serotonin biology looks like before you can interpret what your simulation shows. You need to know the tools before you can use them. The key practical takeaway is that 5-HT2A couples to Gq (not Gs or Gi canonically), so if you include a G protein in your simulation, Gq is the correct partner. And MPS can double your throughput on equilibration runs with two shell commands.

### Layer 2: Neuroplasticity & Membrane Lipids (6 papers)

**What it covers:** Two questions that seem unrelated but converge at the simulation. First: *why* does the 5-HT2A receptor matter therapeutically? Because it's the gatekeeper for a signaling cascade (5-HT2A → TrkB → mTOR → spine growth) that physically rebuilds atrophied cortical neurons. Psychedelics exploit this cascade. So do non-hallucinogenic psychoplastogens like TBG. Second: *where* does the receptor sit? Not in a generic lipid bilayer, but in a specific, compositionally tuned neuronal membrane — rich in cholesterol (~22% of dry weight in neurites), sphingomyelin, phosphatidylserine on the inner leaflet, and complex gangliosides. This membrane is not a passive container; it actively shapes receptor behavior through hydrophobic mismatch, lateral pressure, and lipid raft formation.

**Why it matters for BioChemCore:** The neuroplasticity papers tell you what your simulation is *for* — understanding the receptor dynamics that determine whether a drug promotes spine growth. The lipid papers tell you how to build a biologically defensible membrane in CHARMM-GUI on Day 4. A POPC-only bilayer will work as a first pass, but a membrane with cholesterol, PE, PS (inner leaflet), and sphingomyelin (outer leaflet) will produce dynamics that more closely reflect what happens in a real cortical dendrite.

### Layer 3: Psychedelic Pharmacology & Therapeutics (10 papers)

**What it covers:** The clinical and pharmacological landscape surrounding your receptor. The clinical trials proving psilocybin works for depression and cancer-related distress. The polypharmacology maps showing psychedelics hit dozens of receptors simultaneously. The head-to-head comparison showing mescaline, LSD, and psilocybin produce identical subjective experiences at equivalent doses — because 5-HT2A agonism dominates everything else. The drug design papers showing you can engineer out hallucinations while keeping neuroplasticity. And a universal safety concern: every classical psychedelic activates 5-HT2B, which causes cardiac valve damage with chronic use.

**Why it matters for BioChemCore:** This theme gives you the "so what" for your simulation. When you see TM6 move outward in your trajectory, that corresponds to Gq coupling, which drives the IP3/DAG/PKC cascade, which ultimately drives dendritic spine growth. When you track the hydrogen bond between a ligand and S242, you're watching the exact molecular interaction that distinguishes hallucinogenic LSD from non-hallucinogenic JRT. The simulation is not abstract — it maps onto clinical effects in real patients.

### Layer 4: 5-HT2A Structure & Signaling (12 papers)

**What it covers:** The molecular core. Atomic-resolution structures of the receptor in every signaling state — Gq-coupled, Gi-coupled, beta-arrestin-coupled, transducer-free, non-canonical intermediate. The toggle switch (W336), the ionic lock (R173–E318), the NPxxY motif, the PIF motif, the ECL2 lid — every molecular switch that determines what the receptor does. MD simulations showing the receptor collapses back toward the inactive state without a bound G protein. PCA-based conformational landscapes separating psychedelic from non-psychedelic receptor states. And the field's biggest active debate: does Gq or Gi signaling cause hallucinations?

**Why it matters for BioChemCore:** This is the direct instruction manual for your simulation. Which PDB to start from. Which residues to monitor. What conformational metrics to compute. What your results mean biologically. Every paper in this theme either validates your simulation approach or provides specific analysis techniques to apply on Day 7.

---

## The Three Things You Need to Know Before Diving In

### 1. Biased Agonism Is the Central Concept

If you internalize one idea from all 33 papers, make it this: **different drugs at the same receptor produce different outcomes because they stabilize different receptor conformations, which preferentially couple to different downstream signaling pathways.**

This is called biased agonism (or functional selectivity). It was first articulated as a concept in 2007 (Urban, Raote). It was structurally confirmed in 2022-2025 (Cao, Gumpper). It is the mechanistic basis for designing drugs that separate hallucination from therapy (Tuck 2025, Cameron 2021, Aarrestad 2025). And it is exactly what your MD simulation is designed to probe: different ligand-bound conformational states of the same receptor.

At 5-HT2A, the key biases are:
- **Gq-biased** → linked to calcium signaling, PKC activation, and (per Wallach 2023) hallucinogenicity above a ~70% efficacy threshold
- **Gi-biased** → linked to hallucinogenic effects per Xu 2026's more recent work, with Gq driving therapeutic effects instead
- **Beta-arrestin-biased** → linked to receptor internalization and desensitization; correlated with non-hallucinogenic antidepressant effects per Jastrzebski 2025
- **Balanced** → serotonin itself, which activates everything proportionally and is somehow not psychedelic (probably because it can't cross the cell membrane to reach intracellular receptor pools)

The Gq vs. Gi debate (Wallach 2023 vs. Xu 2026) is the single most active scientific controversy in this field. Both papers are strong. Neither has been definitively resolved. Your reading list captures this debate in real time.

### 2. The Receptor's Shape Is the Message

Five structural motifs appear across nearly every paper in the collection. These are the molecular switches you'll track in your simulation:

**W6.48 (W336) — the toggle switch.** A tryptophan in TM6 whose side-chain rotamer state distinguishes inactive (~120° chi2), active (~50°), and non-canonical biased (~-15°) receptor conformations. It is the single most informative residue to monitor. Gumpper 2025, Wallach 2023, Peeters 2025, and Cummins 2025 all converge on this.

**NPxxY motif (TM7) — the activation stamp.** When this motif locks into its active conformation, the receptor is fully committed to signaling. Psychedelic agonists stabilize it more completely than non-psychedelic partial agonists (Peeters 2025, Gumpper 2025). Its tyrosine (Y380) position distinguishes the non-canonical state from the fully active state.

**DRY / ionic lock (R173–E318) — the activation gate.** A salt bridge between TM3 and TM6 that must break for the receptor to open its intracellular cavity to G proteins. The R173–E318 distance is one of the most mechanistically interpretable metrics you can compute from a trajectory (Viohl 2025).

**ECL2 (extracellular loop 2) — the lid and the bias switch.** L229 on ECL2 closes over LSD's binding pocket, trapping it inside and explaining LSD's hours-long duration. More broadly, ECL2 contact frequency predicts whether a ligand will preferentially couple to Gi or Gq (Kossatz 2024). More ECL2 contact → more Gi → more hallucinogenic.

**S242 (5.46) on TM5 — the human-specific residue.** This serine forms a hydrogen bond with LSD that contributes to G protein bias (Peeters 2025, Tuck 2025). Rodents have an alanine here instead, creating a systematic cross-species pharmacological discrepancy. This single residue is why human and mouse 5-HT2A can behave differently with the same drug.

### 3. The Membrane Is Not Decoration

The lipid bilayer you build in CHARMM-GUI is not just a solvent for the protein. It is a functional component of the system. Three papers establish this:

- **Calderon 1995** measured the actual lipid composition of neuronal neurites (the compartment closest to the post-synaptic membrane you're modeling): high cholesterol (C/PL ratio ~0.74), elevated sphingomyelin, PS on the inner leaflet, complex gangliosides only.
- **Harayama 2018** explains why this matters biophysically: hydrophobic mismatch between your bilayer thickness and the receptor's TM domain length will distort helix geometry. Wrong membrane = wrong dynamics.
- **Lim 2009** gives quantitative composition data: PC ~29%, PE ~27%, cholesterol ~21%, PS ~10%, ceramide ~6%, SM ~4%.

A realistic membrane for your simulation would include cholesterol at 20-30 mol%, PE and PS on the inner leaflet, SM on the outer leaflet, and mixed PC species with at least one unsaturated chain. CHARMM-GUI supports asymmetric bilayer construction — use it.

---

## The Active Debates Worth Tracking

These are the questions that the papers genuinely disagree on. As you read, pay attention to which papers support which positions.

### Does Gq or Gi cause hallucinations?

**Wallach 2023 says Gq.** Gq efficacy above ~70% is required for hallucinations. Beta-arrestin shows zero correlation. Gq/PLC pharmacological blockade abolishes the head-twitch response.

**Xu 2026 says Gi.** Psychedelics activate Gi far more than non-hallucinogenic analogues. Pertussis toxin (Gi blocker) attenuates HTR. Gq blockade does *not* prevent HTR but *does* prevent therapeutic effects.

**Kossatz 2024 adds nuance.** Gi drives psychosis-related behavior; Gq drives memory deficits. Different symptoms, different pathways, same receptor.

The likely resolution is that both Gq and Gi contribute, with their relative importance depending on brain region, dose, drug, and which behavioral endpoint you measure. This is genuinely unresolved.

### Is the hallucinogenic experience required for therapy?

**Clinical data says it correlates.** Griffiths 2016 and Carhart-Harris 2018 both found that the intensity of the mystical/psychedelic experience predicts therapeutic outcome.

**Preclinical data says no.** TBG (Cameron 2021, Aarrestad 2025) and JRT (Tuck 2025) both produce antidepressant effects and neuroplasticity in rodents without any hallucinogenic signature.

**Honest answer as of 2026:** In rodents, the trip is not required. In humans, no one has tested a non-hallucinogenic psychoplastogen in a clinical trial yet. The question remains open.

### Is the glutamate burst required for neuroplasticity?

**The classical model says yes.** 5-HT2A activation → glutamate release → AMPA activation → BDNF/TrkB → mTOR → spine growth.

**Aarrestad 2025 says no.** TBG grows spines without any detectable glutamate burst and without IEG activation. Either basal glutamatergic tone is sufficient, or there's a glutamate-independent route from 5-HT2A to TrkB.

---

## Your BioChemCore Pipeline, Mapped to the Literature

| BioChemCore Day | What You Do | Papers That Inform It |
|---|---|---|
| **Days 1-2** (Protein Selection) | Choose 5-HT2A; read background | Berger 2009, Raote 2007, Kwan 2022 |
| **Day 3** (Maestro Prep) | Clean structure, fix loops, protonation | Cummins 2025 (binding pocket geometry), Gumpper 2025 (PDB codes) |
| **Day 4** (CHARMM-GUI) | Build membrane, embed protein | Calderon 1995, Harayama 2018, Lim 2009, Peeters 2025 (membrane recipe) |
| **Day 5** (Min & Equil) | Energy minimization, NVT/NPT | NVIDIA 2025 (MPS for throughput), Viohl 2025 (expect TM6 collapse without G protein) |
| **Day 6** (Production) | Launch production MD | Peeters 2025 (methodological template), Wallach 2023 (analysis metrics) |
| **Day 7** (Analysis) | RMSD, RMSF, contacts, lipid order | All structure papers; Viohl 2025 (ionic lock distance), Peeters 2025 (PCA of DOFs), Kossatz 2024 (ECL2 contacts) |
| **Day 8** (MegaMembrane) | Assemble multi-protein membrane | Harayama 2018 (lipid heterogeneity), Calderon 1995 (raft composition) |

### PDB Structure Selection

| If you want... | Use PDB | From |
|---|---|---|
| Active state with serotonin | 9ARX | Gumpper 2025 |
| Active state with psilocin | 9AS7 | Gumpper 2025 |
| Active state with LSD (Gq) | 9AS3 | Gumpper 2025 |
| Gi-coupled with psilocin | 9LL8 | Xu 2026 |
| Gi-coupled with DOI | 9LL7 | Xu 2026 |
| Non-canonical (biased) state | 9AS9 | Gumpper 2025 |
| Beta-arrestin-coupled (5-HT2B) | 7SRS | Cao 2022 |

### Membrane Composition Reference

**Biologically realistic (Peeters 2025 recipe):** 57 POPC, 52 POPE, 18 POPS, 8 PSM, 12 CER160, 4 POPI, 42 cholesterol (75x75 Å box)

**Simpler first-pass:** Pure POPC or POPC + 30% cholesterol (used by Kossatz 2024, Viohl 2025)

**Ideal (combining lipid papers):** Asymmetric bilayer — outer leaflet enriched in PC + SM; inner leaflet enriched in PE + PS. Cholesterol in both leaflets at ~25-30 mol%.

---

## Recommended Theme Reading Order

Read the themes in this order. Each one builds the context for the next.

**1. MD Tools & Serotonin Biology** — Start here. It's the shortest (5 papers) and gives you the broadest context: what serotonin is, what 5-HT2A does pharmacologically, and what computational tools you'll use. You'll understand the system before you understand the details.

**2. Neuroplasticity & Membrane Lipids** — Read second. Now that you know the receptor and the tools, learn why the receptor matters (it's the gatekeeper for cortical neuroplasticity) and where it lives (a compositionally specific neuronal membrane). This builds the biological motivation for everything that follows.

**3. Psychedelic Pharmacology & Therapeutics** — Read third. With the biology in place, absorb the clinical and pharmacological evidence. The trials, the polypharmacology, the drug design. This is where the "so what" becomes concrete: real patients, real outcomes, real drug candidates.

**4. 5-HT2A Structure & Signaling** — Read last. This is the largest theme (12 papers) and the most technically dense. But by now you have all the context to appreciate it: you know the biology, the therapeutics, the membrane, and the tools. The structural papers become a practical guide for your own simulation rather than abstract crystallography.

Within each theme, the individual summaries include their own recommended reading order.

---

## Key Terms — The Absolute Essentials

These 10 terms appear across all four themes. If you know these cold, you can navigate any paper in the collection.

**5-HT2A receptor** — Seven-transmembrane GPCR on cortical pyramidal neurons. Primary target of psychedelics. Couples to Gq (canonical), Gi, and beta-arrestin. The protein you are simulating.

**Biased agonism** — Different drugs at the same receptor activate different downstream pathways by stabilizing different conformations. The central organizing concept of the entire reading list.

**Psychoplastogen** — A compound that promotes rapid, lasting structural neuroplasticity (spine growth, dendritic arborization) after a single dose. Includes both hallucinogenic psychedelics and non-hallucinogenic analogues like TBG and JRT.

**Toggle switch (W6.48/W336)** — The tryptophan in TM6 whose rotamer state is the single best indicator of receptor activation state. Monitor its chi2 dihedral angle in your trajectory.

**ECL2 (extracellular loop 2)** — The flexible loop above the binding pocket. Forms a lid over LSD. Contact frequency with ligands predicts Gi vs. Gq coupling bias.

**Gq signaling** — The canonical 5-HT2A pathway: PLC → IP3 + DAG → calcium release + PKC. Drives downstream mTOR/TrkB → neuroplasticity.

**Head-twitch response (HTR)** — Rodent behavioral proxy for hallucinogenic potential. Requires 5-HT2A. The endpoint used by Wallach, Kossatz, and Xu to study which signaling pathway causes psychedelic effects.

**NPxxY motif** — Conserved TM7 sequence whose conformation distinguishes full activation from partial/biased states. Psychedelic agonists lock it in the active position.

**Hydrophobic mismatch** — The energetic penalty when your bilayer thickness doesn't match the receptor's TM domain length. Wrong membrane = wrong receptor dynamics in your simulation.

**Residence time (tau)** — How long a drug stays bound (1/k_off). LSD's long residence time is caused by ECL2 lid formation. Clinically relevant because it determines how long the receptor stays activated after a single dose.

---

*This overview synthesizes 4 thematic master summaries covering 33 papers spanning 2004-2026. All papers are individually summarized in the md/ directory. Written for BioChemCore, UCSD Bioinformatics, June 2026.*
