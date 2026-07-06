# Summary: Maximizing OpenMM Molecular Dynamics Throughput with NVIDIA MPS

**Citation:** Hsu, D., Clark, D., & Paulsen, J. (2025, June 4). *Maximizing OpenMM Molecular Dynamics Throughput with NVIDIA MPS*. NVIDIA Technical Blog. https://developer.nvidia.com/blog/maximizing-openmm-molecular-dynamics-throughput-with-nvidia-mps/

---

## One-Sentence Takeaway

Running multiple OpenMM MD simulations concurrently on a single GPU using NVIDIA's Multi-Process Service (MPS) can more than double total simulation throughput compared to running one simulation at a time, with minimal code changes required.

---

## Background & Motivation

When you run an MD simulation in OpenMM, the simulation engine sends computational work to the GPU in bursts. The problem is that most simulations — especially those of small-to-medium sized systems like a single membrane protein — do not generate enough computational work to keep a modern GPU fully occupied at all times. This is called GPU underutilization. Think of it like hiring a construction crew with 10,000 workers but only ever sending 2,000 of them to the job site: the other 8,000 are idle, wasting your resources.

This matters practically because GPU time is expensive, whether you are renting cloud compute or working within an HPC cluster allocation. If your membrane protein system (say, ~90,000 atoms for a GPCR in a lipid bilayer) only saturates 40% of a high-end GPU's compute capacity, then running just one simulation at a time wastes ~60% of what you are paying for.

The traditional approach to running multiple simulations on a GPU is CUDA's default context-switching mechanism, where the GPU switches back and forth between simulations one at a time, much like a single-core CPU rapidly switching between tasks. This incurs overhead from loading and unloading state each time the GPU switches. NVIDIA MPS is the solution: it allows truly simultaneous execution of multiple CUDA processes on the same GPU, eliminating that switching overhead.

---

## Approach & Methods

The authors benchmarked MPS performance using OpenMM 8.2.0, CUDA 12, and Python 3.12. They tested three molecular systems of increasing size, chosen specifically to span the range of systems researchers commonly simulate:

- **DHFR** (Dihydrofolate reductase): 23,236 atoms — a small, well-established MD benchmark protein
- **ApoA1** (Apolipoprotein A-I): 92,236 atoms — a medium-sized system representative of a lipid-associated protein
- **Cellulose**: 408,609 atoms — a large system pushing the upper limits of single-GPU simulation

They ran 1, 2, 4, and 8 concurrent simulations on a range of NVIDIA GPUs (including the L40S and H100), measuring total throughput in nanoseconds per day summed across all concurrent simulations. The key benchmark script came from the OpenMM GitHub repository, and simulations were launched as separate processes with the `CUDA_VISIBLE_DEVICES` environment variable pinning each process to a specific GPU.

Enabling MPS requires only two shell commands — one to start the MPS daemon and one to stop it — making it an unusually low-barrier optimization. No changes to the OpenMM Python scripts themselves are needed.

The authors then investigated a second tuning knob: `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE`, an environment variable that caps the fraction of GPU compute threads any single MPS process can use. The intuition here is that when multiple simulations run simultaneously, they can fight over GPU resources and interfere with each other. By capping each process to 200/NSIMS percent of the GPU (so each of 4 simulations gets 50%, for example), you prevent one simulation from monopolizing hardware when the other simulations are doing compute-intensive work.

Finally, they applied MPS to free energy perturbation (FEP) calculations using OpenFreeEnergy (OpenFE), which runs replica-exchange MD (REMD) — a method that requires many parallel simulations at slightly different thermodynamic conditions.

---

## Key Findings

**GPU utilization is the key variable.** The core finding is consistent across all benchmarks: the smaller the system, the greater the throughput gain from MPS. Smaller systems underutilize the GPU more severely per simulation, so adding concurrent simulations recovers more of that idle capacity.

**DHFR (23K atoms) showed the largest gains.** Because this small system leaves most of the GPU idle, running multiple concurrent simulations dramatically increased total throughput. The paper reports that total throughput could more than double on high-end GPUs like the L40S and H100 compared to running a single simulation.

**ApoA1 (92K atoms) — the most relevant size for membrane protein work.** At this scale, representative of a GPCR or similar CNS membrane protein embedded in a lipid bilayer, MPS still provided meaningful throughput improvements, though smaller than for DHFR. This is the size range most relevant to the BioChemCore program.

**Cellulose (408K atoms) saw less benefit.** Large systems already saturate a single GPU more fully, so adding concurrent simulations helps less. MPS still helped even here on high-end GPUs, but the gains were modest.

**`CUDA_MPS_ACTIVE_THREAD_PERCENTAGE` provides an additional boost.** Setting this variable to cap each process at 200/NSIMS percent of available threads reduced destructive interference between concurrent simulations. The authors found this increased throughput by roughly 10–15% further on top of base MPS gains for optimal simulation counts. Setting `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE=$(( 200 / NSIMS ))` is the recommended formula.

**The key trade-off is speed vs. throughput.** Each individual simulation runs slower when sharing the GPU — MPS does not make any single simulation faster. The gain is in how much total simulation time you generate per unit of wall-clock time across all parallel simulations. If you need to finish one specific trajectory as fast as possible, MPS is not helpful. If you need to explore conformational space across multiple replicas or run parameter screens, MPS is a significant win.

**OpenFE free energy calculations saw a 36% speedup.** FEP with REMD requires 12 replicas at different lambda windows (thermodynamic states). Without MPS, OpenFE uses CUDA context switching, running only one replica at a time. With MPS, all 12 replicas run simultaneously on one GPU. The authors observed 36% higher throughput for the full FEP calculation (12 * 100 ps windows per GPU). This is a substantial win given that FEP calculations are already computationally expensive and widely used in drug discovery pipelines.

---

## Significance & Implications

This paper is directly relevant to what you are doing in BioChemCore. When you run production MD on your membrane protein system in OpenMM, your system will likely be in the 80,000–150,000 atom range (protein + lipid bilayer + water + ions). That puts you squarely in the ApoA1-like size regime where MPS provides real but not maximal gains.

The practical implications are significant. If you are running multiple equilibration trajectories to check convergence, or running multiple replicas of the same system to improve statistics, MPS lets you use the same GPU allocation more efficiently. On a shared HPC cluster, this means completing more science per GPU-hour, which matters when you have limited allocation.

For the broader field, this connects to a trend in computational biology: as GPU hardware becomes more powerful and biomolecular systems of interest remain in the sub-million atom range, single-simulation GPU utilization is becoming the bottleneck rather than raw compute power. MPS is a systems-level solution to that mismatch.

The FEP result is particularly interesting from a drug discovery angle. The serotonin receptor papers in your collection involve comparing binding affinities of psychedelic vs. non-hallucinogenic agonists — FEP is exactly the computational technique used to calculate those relative binding free energies. A 36% speedup in FEP throughput is meaningful for that kind of work.

**Connection to BioChemCore curriculum:** On Day 6 (production MD) and Day 7 (analysis), you may want to launch multiple short production runs rather than one long one, both for practical reasons (if one crashes, you haven't lost everything) and scientific ones (independent trajectories are statistically more valuable than one long trajectory for many analyses). MPS is the tool that makes running those multiple trajectories simultaneously cost-effective rather than wasteful.

---

## Limitations & Open Questions

**This is a technical blog post, not a peer-reviewed paper.** The benchmarks are credible and the methodology is clearly described, but the results have not gone through formal peer review. The figures are partially obscured in the available screenshots, which limits precise quantitative interpretation of the throughput numbers.

**System-specific optimal NSIMS is not always obvious.** The authors show that the optimal number of concurrent simulations varies by GPU model and system size. There is no universal formula beyond "more simulations helps small systems on powerful GPUs." Users need to benchmark their specific system-GPU combination to find the sweet spot.

**The thread percentage tuning requires experimentation.** While the `200/NSIMS` formula is a good starting point, the paper notes this is heuristic. For systems that differ substantially from the three benchmarks, users may need to sweep values to find optimal settings.

**MPS has security implications in multi-user environments.** MPS processes share GPU memory space, which means one process can theoretically read another's GPU memory. The authors mention that MPS requires root privileges in some configurations (though regular user privilege works in others). On shared HPC clusters, MPS availability may be restricted by cluster administrators for this reason.

**No benchmarks on multi-GPU scaling.** The paper focuses on single-GPU optimization. For truly large systems or very long simulations, multi-GPU runs are more relevant, and MPS behavior across multiple GPUs is not addressed here.

---

## Key Terms & Concepts

**CUDA (Compute Unified Device Architecture):** NVIDIA's programming framework for running parallel computations on GPU hardware. OpenMM uses CUDA to offload the computationally expensive force calculations in MD to the GPU.

**MPS (Multi-Process Service):** An NVIDIA technology that allows multiple separate CUDA processes to execute simultaneously on the same GPU, sharing hardware resources without context switching overhead. Enabling it requires running `nvidia-cuda-mps-control -d`.

**GPU context switching:** The default behavior where a GPU can only execute one CUDA process at a time, rapidly switching between processes much like a CPU multitasks. This introduces overhead and leaves compute capacity idle between switches.

**GPU utilization:** The fraction of a GPU's computational capacity that is actually doing useful work at any given moment. Small MD systems typically have low GPU utilization because they don't generate enough parallel work to fill all the GPU's processing cores.

**Throughput vs. latency:** In MD, throughput means total nanoseconds of simulation produced per day across all running simulations; latency means how fast any single simulation runs. MPS improves throughput at the cost of individual simulation latency.

**CUDA_MPS_ACTIVE_THREAD_PERCENTAGE:** An environment variable that caps the maximum fraction of GPU compute threads a single MPS process can use, preventing one simulation from monopolizing resources when running concurrently with others.

**Free Energy Perturbation (FEP):** A rigorous computational method for calculating the difference in binding free energy between two ligands (e.g., a drug variant vs. a reference compound). It requires running many short simulations at intermediate thermodynamic states (lambda windows) and is widely used in drug discovery to rank drug candidates.

**Replica-Exchange MD (REMD):** A sampling strategy that runs multiple copies (replicas) of a simulation at different conditions (temperature, lambda values, etc.) and periodically swaps configurations between replicas. This helps the simulation escape local energy minima and sample conformational space more completely.
