# Master Thematic Summary: MD Simulation Tools & Serotonin Biology Foundations

**Theme Group:** Practical & Biological Foundations for 5-HT2A MD Simulations
**Papers covered:** NVIDIA 2025, Votapka 2022, Berger 2009, Shapiro 2003, Unger 2020
**Prepared for:** BioChemCore — molecular dynamics simulations of the 5-HT2A serotonin receptor

---

## 1. Theme Overview

This group of five papers forms the practical and biological bedrock of your BioChemCore project. Two papers cover the computational infrastructure — how to run simulations efficiently and how to extract kinetic quantities from them. Three papers cover the biology and pharmacology of serotonin — what serotonin does across the body, what the 5-HT2A receptor does when a drug binds to it, and how researchers can actually watch serotonin move in living neurons. Together, these papers answer two questions you need answered before writing a single line of simulation code: "What software toolkit am I working in, and what biology am I trying to model?"

---

## 2. The Narrative Arc

### Part A: Building the Computational Infrastructure

The BioChemCore pipeline runs on OpenMM. That choice is not arbitrary — it reflects a broader shift in the computational biophysics field over the past decade. OpenMM was designed as a Python-native, GPU-accelerated, extensible engine, and both simulation tools in this group are built on top of it.

NVIDIA 2025 addresses a practical problem that anyone running membrane protein simulations will hit: GPU underutilization. Modern GPUs have enormous parallel compute capacity, but a single GPCR simulation (roughly 90,000 atoms — protein plus bilayer plus water plus ions) does not generate enough computational work to keep all that hardware busy. The paper benchmarks NVIDIA's Multi-Process Service (MPS), which allows multiple OpenMM simulations to run truly simultaneously on one GPU, sharing hardware without the overhead of context switching. The core finding is simple and actionable: for systems in the ApoA1 size range (92,000 atoms, which maps well to a membrane-embedded 5-HT2A system), running two to four concurrent simulations on a single GPU meaningfully increases total simulation throughput at no additional hardware cost. The additional tuning via `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE=$(( 200 / NSIMS ))` captures another 10-15% on top of that.

Votapka 2022 addresses a deeper problem: even a perfectly efficient single simulation can only access nanoseconds to microseconds of simulated time, but drug binding and unbinding events happen on millisecond-to-hour timescales. SEEKR2 solves this with milestoning — a strategy that slices the binding/unbinding pathway into short segments, simulates each independently, and mathematically combines the results to reconstruct kinetics that no single trajectory could ever observe. The critical engineering update in SEEKR2 is replacing the old NAMD-based backend with an OpenMM plugin, yielding roughly 20-fold throughput gains. This is not just a computational paper — it establishes that predicting how long a drug stays bound to a receptor (residence time, tau = 1/k_off) is now computationally tractable on single-GPU hardware that academic labs can actually access.

What connects these two papers is their shared platform and their complementary concerns. NVIDIA 2025 optimizes raw simulation throughput; SEEKR2 extends what that throughput can scientifically accomplish. One makes your equilibration and production runs more efficient. The other makes it possible to ask questions about drug binding kinetics that your production MD alone cannot answer.

### Part B: Understanding What You Are Simulating

The three serotonin biology papers do not form a simple chronological progression — they operate at three different levels of resolution and serve three distinct functions.

Berger 2009 is the widest-angle lens. It establishes serotonin as a whole-body signaling system: 15 receptor subtypes, 95% of total serotonin stored in the gut rather than the brain, receptors expressed in every organ from heart to uterus. For anyone approaching the 5-HT2A receptor as "the brain receptor for psychedelics," this paper is the necessary reframe. The 5-HT2A receptor is one member of a large family. It sits on Layer V cortical pyramidal neurons alongside 5-HT1A (which has opposing inhibitory effects), it mediates liver regeneration via platelet-derived signals, and its sister receptor 5-HT2B caused cardiac deaths in patients taking fen-phen because nobody checked what norfenfluramine was doing there. Berger 2009 also introduces serotonylation — the receptor-independent mechanism where serotonin is covalently attached to intracellular GTPases by tissue transglutaminase, constitutively activating G protein pathways without any membrane receptor involved. This is relevant not as a simulation target but as a reminder that the receptor-ligand interaction your MD is capturing is only part of the molecule's biological story.

Shapiro 2003 zooms in from the whole-body to the receptor level. It provides the most comprehensive pre-structural pharmacological characterization of a drug (aripiprazole) acting at multiple serotonin and dopamine receptor subtypes, and in doing so it introduces what became one of the most important concepts in GPCR biology: functional selectivity, also called biased agonism. Aripiprazole was studied because it was a puzzling clinical success — a drug that shouldn't have worked quite the way it did based on the simple D2-blockade model. The paper's most striking finding is that the same drug, at the same receptor subtype (D2L), is a partial agonist in two cell lines and a pure antagonist in three others. The explanation — that receptor conformational outcomes depend on which G proteins and signaling partners are present in a given cellular context — laid the groundwork for the current era of structure-based drug design that your BioChemCore project is connected to. The 5-HT2A receptor data from Shapiro 2003 establishes: (1) 5-HT2A couples to Gq through PI hydrolysis, (2) receptor reserve substantially changes how a drug's efficacy appears, and (3) aripiprazole behaves as a net antagonist at 5-HT2A in most brain regions. This is exactly the kind of pharmacological baseline an MD simulation of the 5-HT2A receptor needs.

Unger 2020 operates at yet another level of resolution — not the receptor's downstream signaling, but the actual serotonin concentration arriving at the receptor in real time. iSeroSnFR is a genetically encoded fluorescent sensor built by reprogramming a bacterial acetylcholine-binding protein to recognize serotonin, using a three-stage ML pipeline (Rosetta computational design, then Random Forest for identifying critical positions, then a Generalized Linear Model for predicting synergistic multi-site combinations). The resulting sensor detects serotonin at millisecond timescales in living neurons, brain slices, and freely behaving mice — tracking serotonin rise and fall across fear conditioning, social interaction, and the full sleep-wake cycle. For BioChemCore, Unger 2020 is the most distant paper from the simulation pipeline itself, but it is conceptually important: it establishes the actual dynamic range and temporal profile of serotonin signals that the 5-HT2A receptor must process. If you are choosing whether to simulate an agonist-bound or apo (unoccupied) receptor structure, knowing that serotonin fluctuates at millisecond timescales between 0 and high-micromolar concentrations in the synaptic cleft is real biological context.

---

## 3. Key Concepts & Converging Evidence

**OpenMM as the central platform.** Both computational papers treat OpenMM as the default engine. NVIDIA 2025 benchmarks it directly; SEEKR2 is built as an OpenMM plugin. This convergence reinforces the BioChemCore syllabus choice to use OpenMM with CHARMM36m.

**Throughput is a bottleneck and is solvable.** Both NVIDIA 2025 and Votapka 2022 independently address the same root problem: running one standard simulation at a time wastes compute capacity. The solutions are complementary and stack: MPS for maximizing GPU utilization across parallel runs, milestoning for accessing timescales beyond what any single run can reach.

**Functional selectivity is real and emerges from receptor conformation.** Shapiro 2003 demonstrates this pharmacologically at the D2L and 5-HT2A receptors. Berger 2009 provides the wider system context (15 receptor subtypes, each capable of context-dependent signaling). These papers establish the phenomenon; more recent papers in your BioChemCore collection (Peeters 2025, Jastrzębski 2025) provide the structural explanation. The conceptual through-line — that receptor conformation determines signaling outcome — is exactly what MD simulations are uniquely positioned to investigate.

**Serotonin biology extends far beyond the synapse.** Both Berger 2009 and Unger 2020 establish this, from different angles. Berger 2009 does it through receptor distribution across organ systems; Unger 2020 does it by showing serotonin rising and falling across sleep-wake cycles in prefrontal cortex, amygdala, and striatum simultaneously. Neither paper contradicts the other — they reinforce that serotonin is a global regulatory molecule, not a point-to-point neurotransmitter.

---

## 4. Active Debates & Unresolved Questions

**Does HMR compromise kinetic accuracy?** Votapka 2022 validates hydrogen mass repartitioning (HMR) for the trypsin-benzamidine and beta-cyclodextrin systems and concludes it does not significantly alter k_on, k_off, or ΔG_bind. However, the authors explicitly flag that this needs broader validation, particularly for systems with slower or more complex conformational dynamics — like membrane-embedded GPCRs undergoing large TM helix rearrangements. This question is directly relevant to your BioChemCore workflow if you use HMR to extend your timestep.

**What is the optimal number of concurrent MPS simulations?** NVIDIA 2025 shows that optimal NSIMS varies by GPU model and system size. There is no universal formula. For a 90,000-atom membrane protein system on a specific GPU, you would need to benchmark empirically. The paper provides the framework but not a plug-and-play answer.

**How does serotonylation interact with receptor-mediated signaling?** Berger 2009 identifies serotonylation (covalent serotonin modification of intracellular GTPases) as a receptor-independent signaling mechanism but acknowledges its physiological importance relative to canonical receptor signaling is unknown. This remains unresolved as of 2026 and does not directly affect MD simulation design, but it is conceptually important when interpreting any experiment that perturbs total cellular serotonin levels.

**Why do SERT blockers not prolong serotonin transients in Unger 2020's brain slice experiments?** The iSeroSnFR sensor clearly shows that cocaine and citalopram block SERT in vitro, but bath application of these drugs in brain slices failed to prolong electrically evoked serotonin signals. The authors propose several explanations (fast off-kinetics of the sensor, diffusion dynamics, slice preparation artifacts) but cannot resolve which is correct. This inconsistency between in vitro pharmacology and ex vivo biology is a genuine unresolved question.

**Is aripiprazole's 5-HT2A activity agonist, partial agonist, or antagonist in vivo?** Shapiro 2003 argues it is effectively an antagonist in most brain regions due to low receptor reserve, but the in vitro data show partial agonism in high-reserve systems. This distinction matters for understanding the drug's clinical mechanism and for interpreting what "antagonism" vs. "partial agonism" means at the structural level — a question MD simulations could in principle address.

---

## 5. Direct BioChemCore Relevance

### Simulation Setup and Efficiency (Days 4-6)

Your membrane protein system will be in the 80,000-150,000 atom range — protein, bilayer, water, and ions. NVIDIA 2025 places this squarely in the "ApoA1-like" regime where MPS provides real throughput gains. Practical recommendations for your workflow:

- Run two to four concurrent equilibration trajectories simultaneously on a single GPU using MPS (`nvidia-cuda-mps-control -d`).
- Set `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE=$(( 200 / NSIMS ))` for each process.
- This is particularly useful on Day 5 (minimization and equilibration) when you may want multiple independent equilibration runs to check convergence.

If you consider using HMR to extend your timestep from 2 fs to 4 fs, Votapka 2022 gives you confidence it does not compromise thermodynamic accuracy and likely does not compromise kinetics — but be aware the validation is on soluble systems, not GPCRs in membranes.

### Kinetic Analysis Beyond Your Trajectories (Post-Day 7)

SEEKR2 is not part of the BioChemCore pipeline for Days 1-8, but it is the natural next step if you want to ask binding kinetics questions about your 5-HT2A receptor. The workflow is direct: SEEKR2 runs through OpenMM with CHARMM force fields, uses the same system preparation you already did, and adds milestoning logic on top. A SEEKR2 calculation for a serotonin-bound vs. ligand-free 5-HT2A system would let you estimate how long serotonin or a psychedelic ligand stays bound — a quantity that Shapiro 2003 argues (via the residence time concept) may be more clinically meaningful than binding affinity alone. The 36% FEP throughput improvement from NVIDIA 2025's MPS is also relevant here: comparative binding free energy calculations are computationally expensive, and MPS makes them more accessible.

### Understanding Your Receptor's Biology (Days 1-2)

For protein selection and literature background (Days 1-2), Berger 2009 gives you the whole-body context for the 5-HT receptor family. The key facts directly relevant to setting up your simulation:

- The 5-HT2A receptor is expressed on Layer V cortical pyramidal neurons, where it co-localizes with 5-HT1A (opposing effects). This neuronal post-synaptic membrane is your target biological environment.
- The lipid composition of neuronal membranes — rich in cholesterol, sphingomyelin, and specific polyunsaturated phospholipids — differs from the generic 1-palmitoyl-2-oleoyl-phosphatidylcholine (POPC) bilayers used in many benchmark simulations. Berger 2009 argues this matters pharmacologically, because the membrane microenvironment shapes receptor behavior.
- The 5-HT2A receptor signals through Gq (confirmed by PI hydrolysis assays in Shapiro 2003), not Gs or Gi. This means you are modeling a Gq-coupled receptor, and if you include a G protein or Gq peptide in your simulation, Gq is the correct partner.

Shapiro 2003 gives you the pharmacological baseline for the receptor itself:

- 5-HT2A affinity for aripiprazole: Ki = 8.7 nM (ketanserin displacement assay)
- Functional output: PI hydrolysis (Gq/phospholipase C pathway)
- Receptor reserve: low in most brain regions, meaning partial agonists are effectively antagonists in vivo
- Relevant residues for ligand binding are in the orthosteric binding pocket formed by TM3, TM5, TM6, and TM7 — the site you would monitor for RMSD and contact analysis in Day 7 analysis

Unger 2020 adds dynamic context: serotonin reaches the 5-HT2A receptor in millisecond-scale transients, fluctuating between low nanomolar and potentially high micromolar concentrations during sustained neuronal firing. Your MD simulation snapshots a single concentration state; knowing the receptor normally encounters rapid concentration swings motivates thinking about whether to simulate the apo, agonist-bound, or antagonist-bound conformation.

### CHARMM-GUI Membrane Composition (Day 4)

Berger 2009's description of the 5-HT2A receptor's neuronal post-synaptic membrane environment directly informs your CHARMM-GUI lipid composition choice. A realistic neuronal post-synaptic density membrane should include:

- Phosphatidylcholine (PC) and phosphatidylethanolamine (PE) as major structural lipids
- Cholesterol at high mole fractions (30-40%) consistent with neuronal plasma membrane composition
- Some phosphatidylserine (PS) on the inner leaflet for asymmetry

This is more complex than the default POPC-only membrane but more biologically meaningful for a receptor whose behavior may depend on its specific lipid microenvironment.

---

## 6. Recommended Reading Order

**1. Berger 2009** — Start here for the widest biological context. Understanding that serotonin is a whole-body system with 15 receptor subtypes — and that the 5-HT2A receptor specifically is expressed on Layer V cortical neurons alongside its antagonist 5-HT1A — gives you the "why does this matter" foundation before you touch any simulation parameters.

**2. Shapiro 2003** — Read second to zoom in on the receptor itself. This paper establishes what 5-HT2A does when something binds to it (PI hydrolysis via Gq), introduces functional selectivity as a concept, and provides the pharmacological baseline for the receptor you are simulating. The aripiprazole story is also a masterclass in why systematic receptor profiling matters.

**3. Unger 2020** — Read third to understand what serotonin looks like from the receptor's perspective in real time. The sensor engineering is genuinely impressive, but for BioChemCore the key takeaway is behavioral and temporal: serotonin arrives at 5-HT2A in millisecond-scale bursts, and the concentration the receptor actually experiences varies enormously with firing state and behavioral context.

**4. NVIDIA 2025** — Read fourth, before you start running simulations. This is short, practically focused, and directly applicable to Days 5-6 of the BioChemCore schedule. The MPS setup requires only two shell commands, and understanding why it works (GPU underutilization in sub-million-atom systems) makes you a better user of the hardware you have.

**5. Votapka 2022** — Read last. This is the most technically dense paper in the group and the furthest from the immediate BioChemCore pipeline. It establishes milestoning as a rigorous method for computing drug binding kinetics — a natural follow-on capability once you have completed your production MD and want to ask deeper questions. The benchmark results (20-fold speedup, JAK2 residence time prediction of 6.3 hours vs. experimental 6.65 hours) are impressive evidence that the method works on real drug-protein systems.

---

## 7. Key Terms Quick Reference

**OpenMM** — Python-native, GPU-accelerated MD engine. The simulation platform for all BioChemCore computations. SEEKR2 runs as an OpenMM plugin; NVIDIA MPS optimization applies directly to OpenMM processes.

**MPS (Multi-Process Service)** — NVIDIA technology enabling multiple CUDA processes to run simultaneously on one GPU without context-switching overhead. Activated by two shell commands; provides meaningful throughput gains for membrane-protein-sized systems (80,000-150,000 atoms).

**Milestoning** — A computational strategy that divides a drug binding/unbinding pathway into short segments, simulates each independently, and reconstructs global kinetics (k_on, k_off, ΔG_bind). Implemented in SEEKR2 as MMVT (Markovian Milestoning with Voronoi Tessellations).

**HMR (Hydrogen Mass Repartitioning)** — Technique that increases hydrogen atom masses to allow a 4 fs timestep instead of 2 fs, roughly doubling simulation throughput. Validated to not compromise thermodynamic accuracy; kinetic accuracy on GPCRs not yet fully tested.

**Residence Time (tau)** — The average time a drug stays bound at its receptor, defined as tau = 1/k_off. Increasingly recognized as a better predictor of clinical efficacy than equilibrium binding affinity alone.

**5-HT2A receptor** — The primary postsynaptic serotonin receptor subtype on Layer V cortical pyramidal neurons; couples to Gq (PI hydrolysis); primary target of classical psychedelics (psilocybin, LSD). Your BioChemCore simulation target.

**Functional selectivity (biased agonism)** — The phenomenon where the same drug at the same receptor produces different signaling outputs depending on the cellular context (which G proteins and accessory proteins are present). Demonstrated pharmacologically by Shapiro 2003; now a central concept in GPCR drug design.

**Gq / PI hydrolysis** — The primary signaling pathway of 5-HT2A. Gq activation triggers phospholipase C, which cleaves PIP2 into IP3 and DAG, releasing calcium from intracellular stores. The functional readout used by Shapiro 2003 to measure 5-HT2A agonism/antagonism.

**Serotonylation** — Receptor-independent mechanism where serotonin is covalently attached to small GTPases (e.g., RhoA) by tissue transglutaminase, constitutively activating G protein signaling. Identified by Berger 2009; physiological importance relative to canonical receptor signaling remains unclear.

**iSeroSnFR** — Genetically encoded fluorescent serotonin sensor (Unger 2020) with millisecond temporal resolution, built by ML-guided directed evolution of a bacterial periplasmic binding protein. Affinity ~310 µM in purified protein; detects serotonin as low as 338 pM on cell surfaces due to large fluorescence response.

**k_on / k_off** — Association rate constant (M⁻¹s⁻¹; how fast a drug binds) and dissociation rate constant (s⁻¹; how fast it unbinds). Together determine K_D = k_off / k_on. SEEKR2 computes both from milestoning simulations.

**MMVT (Markovian Milestoning with Voronoi Tessellations)** — The specific milestoning flavor used in SEEKR2. Partitions binding pathway into Voronoi cells; short MD simulations run inside each cell with reflective boundary conditions; crossing statistics reconstruct global kinetics.

**Receptor reserve** — The fraction of receptors in a tissue that are "spare" — not needed to produce a maximal response. High receptor reserve makes partial agonists appear more efficacious; Shapiro 2003 argues brain 5-HT2A has low receptor reserve, making aripiprazole a net antagonist in vivo.

**SERT (Serotonin Transporter)** — Membrane protein that clears serotonin from synapses by reuptake. Target of SSRIs. Unger 2020 used iSeroSnFR to build a real-time functional SERT assay (OSTA) that directly quantified SSRI and cocaine inhibition kinetics.

---

*Synthesized for BioChemCore program — molecular dynamics simulations of the 5-HT2A serotonin receptor. Individual paper summaries: NVIDIA_2025_summary.md, Votapka_2022_summary.md, Berger_2009_summary.md, Shapiro_2003_summary.md, Unger_2020_summary.md*
