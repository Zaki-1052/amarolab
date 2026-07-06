# Votapka et al. 2022 — SEEKR2: Versatile Multiscale Milestoning Utilizing the OpenMM Molecular Dynamics Engine

**Citation:** Votapka, L. W., Stokely, A. M., Ojha, A. A., & Amaro, R. E. (2022). SEEKR2: Versatile Multiscale Milestoning Utilizing the OpenMM Molecular Dynamics Engine. *J. Chem. Inf. Model.*, 62, 3253–3262.

---

## One-Sentence Takeaway

SEEKR2 is a revamped computational tool that uses a "divide and conquer" strategy called milestoning to calculate how fast drugs bind to and unbind from proteins — and its new OpenMM-powered engine makes those calculations roughly 20 times faster than the previous version while maintaining accuracy.

---

## Background & Motivation

One of the most practically important questions in drug discovery is not just whether a drug binds to its target protein, but *how fast* it binds and — critically — how long it stays bound. The residence time of a drug at its target (how long it sits in the binding site before falling off) has been shown to correlate with clinical efficacy more directly than simple binding affinity alone. To predict these kinetic quantities computationally, you need to simulate the full binding and unbinding process, which can take anywhere from milliseconds to hours in real biology — timescales that are completely inaccessible to standard molecular dynamics (MD) simulation, which typically covers nanoseconds to microseconds even on modern hardware.

The core challenge is a sampling problem. A ligand unbinding from a receptor is a rare event: the system spends most of its time sitting in the bound state, and unbinding events happen infrequently. Running brute-force MD long enough to catch many of these events is computationally intractable for most biologically relevant systems. This drives the need for enhanced sampling and multiscale methods.

SEEKR (Simulation-Enabled Estimation of Kinetic Rates) was developed by the Amaro lab at UCSD to address exactly this problem. It uses a framework called **milestoning**, which works by dividing the space between the bound and unbound states into a series of smaller regions, running many short simulations within each region independently, and then mathematically stitching those local statistics back together to reconstruct the global kinetics. SEEKR2 is the second major version, and its central upgrade is replacing the older NAMD simulation engine with **OpenMM** — a Python-native, GPU-accelerated MD engine that is increasingly the community standard for extensible, high-performance simulation.

---

## Approach & Methods

### The Milestoning Framework

The conceptual backbone of SEEKR2 is **Markovian Milestoning with Voronoi Tessellations (MMVT)**. Here is how to think about it intuitively. Imagine the binding pathway of a small molecule traveling from bulk solvent into a protein's binding pocket. Rather than simulating that entire journey in one continuous trajectory, MMVT partitions the space surrounding the binding site into concentric shells — like layers of an onion — defined by the distance between the center of mass of the ligand and the center of the binding site.

Each shell is a **Voronoi cell**, and the surfaces separating adjacent cells are the **milestones**. Short MD simulations are run independently within each cell. Whenever the simulation trajectory crosses a milestone boundary, the crossing event is logged (time, position, velocity), and the trajectory is reflected back into the cell. By accumulating statistics on how often the system crosses each boundary and how long it takes, the method can compute **mean first passage times** — the average time to travel between any two milestones — and from these, derive the macroscopic rate constants k_off (unbinding rate) and k_on (binding rate), as well as the free energy of binding ΔG_bind.

The cells in the outermost region, far from the binding site in bulk solvent, are handled by **Brownian dynamics (BD)** simulations instead of full atomistic MD. BD treats the solvent implicitly and models the ligand as a semi-rigid body diffusing through a continuum, which is orders of magnitude cheaper computationally. The SEEKR2 framework uses Browndye 2 for this BD component. The handoff between the BD (outer) and MD (inner) regions is one of the methodologically interesting aspects of SEEKR — determining the right boundary between these two regimes requires care, because the implicit solvent approximation in BD breaks down near the protein surface where atomic-level interactions dominate.

### The OpenMM Integration

The primary engineering contribution of SEEKR2 is a purpose-built **OpenMM plugin** written in Python (interface layer) and C++/CUDA (kernel layer). OpenMM's architecture supports custom force and integrator plugins, and the SEEKR2 plugin leverages this to implement MMVT milestoning logic directly in the simulation loop. This means milestone crossings can be detected and logged at every timestep with negligible overhead — in contrast to the NAMD implementation, which used a TCL scripting interface that incurred significant latency and could only evaluate milestones every 10 timesteps by default.

The practical consequence: SEEKR2 with OpenMM on a single V100 GPU runs at ~300 nanoseconds/day for the trypsin-benzamidine benchmark system (~23,000 atoms), compared to ~22 ns/day for NAMD2-based MMVT-SEEKR on a 10-GPU cluster. That is roughly a 13-fold improvement on a per-GPU basis and about 20-fold overall.

### Hydrogen Mass Repartitioning (HMR)

SEEKR2 also introduces support for **hydrogen mass repartitioning (HMR)**, a technique that artificially increases the mass of hydrogen atoms (by transferring mass from their bonded heavy atoms) without changing the system's physics. Because the fastest atomic motions in a simulation — the ones that constrain your timestep — involve light hydrogen atoms vibrating against heavier carbons, increasing hydrogen mass slows down these vibrations and allows a larger simulation timestep (up to 4 femtoseconds instead of the typical 2 fs). This roughly doubles simulation throughput with minimal effect on thermodynamics. The paper carefully tests whether HMR compromises kinetic accuracy — an open question in the field — and finds it does not significantly affect the predicted k_on, k_off, or ΔG_bind values.

### Benchmark Systems

The paper validates SEEKR2 on three test cases of increasing complexity:

- **Trypsin-benzamidine:** A classical benchmark system in computational biophysics — a small, well-characterized inhibitor binding to a serine protease. Experimental k_on, k_off, and ΔG_bind are well established.
- **Beta-cyclodextrin with seven small organic guest molecules:** A host-guest model system widely used to benchmark binding free energy and kinetics methods because the experimental data is clean and the system is small enough for extensive testing.
- **JAK2 kinase with inhibitor ligand 6:** A medically relevant system — JAK2 is a kinase in the JAK-STAT signaling pathway implicated in immune disorders and cancer. The inhibitor has a very long residence time (~6.65 hours experimentally), making it a challenging but important validation target.

---

## Key Findings

### Speed Improvements Are Dramatic

The benchmarking data in Table 1 tells a clear story. For the trypsin-benzamidine system:

- NAMD2-based MMVT-SEEKR on a 10-GPU cluster: **22 ns/day**
- NAMD2-based MMVT-SEEKR on a 68-CPU node: **47 ns/day**
- SEEKR2 with OpenMM on a single V100 GPU: **300 ns/day**
- Conventional OpenMM (no milestoning): **416 ns/day** (the ~25% overhead from SEEKR2's milestoning protocol is modest)
- SEEKR2 with HMR on one V100 GPU: **586 ns/day**

The OpenMM SEEKR2 implementation is nearly 20 times faster than the GPU-accelerated NAMD-MMVT-SEEKR setup, and SEEKR2 with HMR is over 26 times faster. This is not a trivial engineering win — it means calculations that previously required large multi-node HPC allocations can now run on a single GPU workstation.

### Kinetic Accuracy Is Preserved

SEEKR2 reproduces the experimental binding kinetics of trypsin-benzamidine within one order of magnitude. The experimental k_off is 600 ± 300 s⁻¹; SEEKR2 obtains 990 ± 130 s⁻¹ (slightly fast but within experimental error). The k_on from SEEKR2 is 2.4 × 10⁷ M⁻¹s⁻¹, close to the experimental 2.9 × 10⁷ M⁻¹s⁻¹. The ΔG_bind is −5.98 ± 0.09 kcal/mol versus experimental −6.71 ± 0.05 kcal/mol — about 0.7 kcal/mol off, which is typical for this class of methods.

### HMR Does Not Compromise Kinetic Accuracy

Using HMR for the trypsin-benzamidine system, SEEKR2 obtains k_off = 310 ± 30 s⁻¹ and k_on = 8.6 × 10⁶ M⁻¹s⁻¹, with ΔG_bind = −6.06 ± 0.08 kcal/mol. These values are all within experimental uncertainty, and the HMR calculation costs only half as much compute as the non-HMR run. This is an important validation because HMR had previously been shown to work for thermodynamic quantities but its effect on kinetics was debated.

### Host-Guest System: Correct Rank-Ordering

For the seven beta-cyclodextrin guest molecules, SEEKR2 is the only computational method tested (including brute-force MD) that correctly ranks the compounds by k_off according to experiment. For ΔG_bind, SEEKR2 predicts the correct ordering with the exception of the two most similar compounds (1-naphthyl ethanol and 2-naphthyl ethanol), which have nearly identical experimental values that are within each other's error bars. The k_on ranking is harder — SEEKR2 does not correctly rank all seven compounds, but this is true of all methods tested and likely reflects the difficulty of capturing the subtle long-range electrostatic differences that drive association rates.

### JAK2 Kinase: Challenging Long-Residence-Time Ligand

For the JAK2 inhibitor with an experimental residence time of 6.65 hours, SEEKR2 computes a residence time of 6.3 ± 0.1 hours across four independent runs. This is a remarkably close prediction for a system this complex. The fact that four independent runs with identical starting structures converge so closely also provides evidence that the calculation is numerically stable and well-converged for this system.

---

## Significance & Implications

This paper matters for several interconnected reasons.

**For drug discovery:** The ability to predict binding kinetics — not just affinity — computationally is increasingly recognized as important for drug development. A compound with high affinity but fast unbinding may be clinically inferior to one with slightly lower affinity but a long residence time. SEEKR2 makes these kinetic calculations practical on hardware that an academic lab can actually access.

**For the OpenMM ecosystem:** Because SEEKR2 is built as an OpenMM plugin with a Python API, it inherits all of OpenMM's extensibility. This means future milestoning studies can use custom force fields, polarizable water models, enhanced sampling integrators, or whatever new simulation methodology gets added to OpenMM without requiring changes to SEEKR2's milestoning logic. This is architecturally forward-thinking.

**For your BioChemCore work:** You are currently using OpenMM with the CHARMM36m force field for membrane protein simulations. SEEKR2 is a direct extension of that same computational toolkit — it runs MD through OpenMM and can use the CHARMM force field. If you were ever to compute binding kinetics for a ligand interacting with your membrane protein (for example, estimating how long a drug stays bound to a CNS receptor), SEEKR2 would be the natural tool to reach for. The milestoning approach is also relevant conceptually to understanding how your equilibration and production MD relate to the underlying energy landscape of your protein system.

**For the field of computational biophysics broadly:** SEEKR2 demonstrates that multiscale simulation — combining fast BD for long-range diffusion with detailed all-atom MD near the binding site — is not just theoretically sound but practically fast enough to be useful. The 20-fold speedup from the OpenMM integration effectively democratizes milestoning calculations.

---

## Limitations & Open Questions

**Milestone shape limitations in this study.** All milestoning in this paper uses concentric spherical surfaces defined by a single collective variable: the distance between the ligand's and receptor's centers of mass. This works well for small, roughly globular ligands binding to open pockets, but it is a poor approximation for elongated ligands, allosteric binding sites, or pathways that don't follow a simple radial coordinate. The paper acknowledges this and notes that SEEKR2's API already supports other milestone shapes (planar surfaces, RMSD-based surfaces, angle/dihedral milestones), but these are not validated in this work.

**The k_on difficulty.** For the host-guest system, no method tested — including brute-force MD — correctly ranks all compounds by k_on. The authors attribute this partly to the concentric sphere milestone shapes being a poor approximation of the committor function isosurfaces for this system. This is an important honest admission: milestoning theory is exact when milestones coincide with the true committor isosurfaces, but in practice they are always approximations.

**Convergence is non-trivial.** The authors note that at least 250 ns of MD per anchor is needed for converged SEEKR2 calculations, and often 500–1000 ns. For larger, more complex systems (membrane proteins, for example), this could become computationally demanding even with the OpenMM speedup.

**HMR on kinetics needs more testing.** The paper validates HMR kinetic accuracy only on trypsin-benzamidine and the host-guest systems. Whether HMR is appropriate for all milestoning calculations — particularly for systems with slower, more complex conformational dynamics — remains an open question that the authors explicitly flag.

**Force field dependence.** The JAK2 calculations use the AMBER ff14SB force field rather than CHARMM36m, and the host-guest systems use Q4MD. Systematic comparison of how force field choice affects SEEKR2-computed kinetics is not addressed.

---

## Key Terms & Concepts

**Milestoning:** A computational strategy for computing kinetic quantities (like rate constants) by dividing the reaction pathway into short segments, simulating each independently, and mathematically combining the local statistics. Think of it as timing how long a runner takes to cross each 100-meter stretch of a race and then adding up the times.

**Markovian Milestoning with Voronoi Tessellations (MMVT):** The specific flavor of milestoning used in SEEKR2, where the cells partitioning phase space are defined by Voronoi geometry — each region is the set of points closer to its own "seed" milestone than to any other.

**k_on and k_off:** The association rate constant (how fast the ligand binds, in M⁻¹s⁻¹) and dissociation rate constant (how fast it unbinds, in s⁻¹). Together they determine the equilibrium dissociation constant K_D = k_off / k_on, and the drug residence time τ = 1/k_off.

**Brownian Dynamics (BD):** A simulation method that models molecular diffusion without explicitly representing every solvent molecule, treating the solvent as a continuous viscous medium. Much cheaper than all-atom MD but less accurate near protein surfaces where atomic interactions matter.

**Hydrogen Mass Repartitioning (HMR):** A technique that increases hydrogen atom masses (redistributing mass from bonded heavy atoms) to allow larger simulation timesteps (up to 4 fs), roughly doubling throughput without meaningfully changing the physics.

**Mean First Passage Time (MFPT):** The average time it takes a system to travel from one defined state to another for the first time. In the context of SEEKR2, MFPTs between milestones are the primary computed quantities from which rate constants are derived.

**Voronoi Cell / Anchor:** In SEEKR2, each Voronoi cell defines a small region of configuration space around a central "anchor" point. MD simulations run within this cell and are reflected at the cell boundaries (milestones). Together, all cells tile the binding pathway from the bound state to bulk solvent.
