# 5-HT2A Receptor MD Simulation -- BioChemCore / Amaro Lab

All-atom molecular dynamics simulation of the psilocin-bound 5-HT2A serotonin receptor (PDB 9AS8) in a realistic neuronal membrane, built as part of the BioChemCore program in the Amaro Lab at UC San Diego.

## System

- **Protein:** 5-HT2AR + mini-Gq heterotrimer (chains A-D), bound to psilocin (+1 charge)
- **Source structure:** PDB 9AS8 (cryo-EM, psilocin-bound, 5-HT2AR + mini-GaqiN + Gb1 + Gg2)
- **Membrane:** Asymmetric neuronal bilayer (585 lipids, Ingolfsson Brain PM composition)
- **System size:** 280,277 atoms, 128.4 x 128.4 x 181.3 A box
- **Force field:** CHARMM36m + WYF cation-pi + HMR (4 fs production timestep)
- **Engine:** OpenMM 8.1 with Metal GPU backend (Apple M4)
- **Temperature:** 310.15 K (37 C), 150 mM NaCl, NPT ensemble
- **Production:** 10 ns (10 x 1 ns blocks)

## Directory structure

```
amarolab/
  sims/                     # Upstream structure preparation
    9AS8.pdb                  # Original PDB deposit
    9AS8_fixed.pdb            # PDBFixer output (4 chains, gaps modeled)
    9AS8_complex.pdb          # Protein + psilocin merged for CHARMM-GUI
    psilocin.pdb              # Ligand binding-pose coordinates
    psilocin_cgenff.pdb       # Ligand with CGenFF atom names, superposed
    charmm-gui-run-1/         # CGenFF ligand parameterization (correct run)
    *.py                      # Structure prep scripts

  charmm-gui/               # CHARMM-GUI Membrane Builder output (Job 8190629385)
    step1_pdbreader.*         # PDB reading, protonation, disulfide, capping
    step2_orient.*            # PPM orientation (flipped: G protein below)
    step3_*                   # Lipid composition, packing, system sizing
    step4*                    # Lipid building, waterbox, ions
    input.config.dat          # Full CHARMM-GUI configuration record
    lig/                      # CGenFF topology and parameters for psilocin
    amber/                    # Amber input files (alternative engine)
    charmm_openmm/            # CHARMM/OpenMM input files (alternative)

  openmm/                   # OpenMM simulation files
    step5_input.psf           # System topology (47 MB)
    step5_input.crd           # Initial coordinates (38 MB)
    toppar.str                # CHARMM36m + CGenFF parameter stream
    sysinfo.dat               # Box dimensions
    openmm_run.py             # Main run script (modified: Metal/HIP priority)
    omm_*.py                  # OpenMM support modules
    step6.*_equilibration.inp # Equilibration parameters (6-step restraint release)
    step7_production.inp      # Production run parameters
    step6.*_equilibration.out # Equilibration logs (convergence data)
    step7_*.out               # Production logs
    run_production.sh         # Production run wrapper
    expanse_production.sb     # SDSC Expanse SLURM batch script
    restraints/               # Restraint definitions

  analysis/                 # Trajectory analysis (7 phases)
    phase1_visual/            # VMD snapshots and visualization
    phase2_rmsd/              # RMSD time series
    phase3_rmsf/              # RMSF per-residue flexibility
    phase4_psilocin/          # Psilocin binding pose stability
    phase5_lipid_order/       # Lipid order parameters (Scd)
    phase6_contacts/          # Protein-lipid contacts
    phase7_summary/           # Summary snapshots and report
    p_crossphase.py           # Cross-phase correlation analysis
    rmsf_vs_contacts.png      # RMSF vs lipid contacts overlay

  envs/                     # Conda environment specifications
    biochemcore_env.yml       # Local environment (macOS/M4)
    biochemcore_expanse.yml   # HPC environment (SDSC Expanse)

  amaro_scripts/            # Amaro Lab shared script library
  amaro_wiki/               # Amaro Lab internal wiki (Obsidian export)
```

## Key parameters and decisions

### Structure preparation (Day 3)
- Removed chain E (scFv16 crystallization artifact)
- Modeled 6 short gaps, skipped 4 long disordered regions (N/C-termini, ICL3, His-tag)
- Chain A numbering offset: -78 from literature (C148/C227 literature = C70/C149 here)
- Disulfide: C70-C149 (TM3-ECL2), verified at 2.0 A

### Ligand parameterization (Day 4a)
- Psilocin parameterized via RCSB Ligand ID 91Q in CGenFF
- Manually protonated dimethylamine (+1 charge, pKa ~8.5-9)
- Parameter penalties: 0.600 (params), 0.437 (charges) -- both excellent
- Atom names mapped and superposed onto binding-pose coordinates (RMSD 0.87 A)

### CHARMM-GUI Membrane Builder (Days 4b-4d)
- pH 7.4, PROPKA protonation (PROF GLU 196 -> GLUP only)
- All 10 segments capped ACE/CT2 (no native termini)
- Orientation flipped via PPM 2.0 (G protein intracellular, below membrane)
- Lipid composition from Ingolfsson et al. 2017 (Biophys. J. 113:2271)
- XY = 120 A initial, yielding 128.4 x 128.4 A box
- 285 upper / 300 lower leaflet lipids, ~46% cholesterol both leaflets
- Asymmetric: PE enriched inner, PS inner-only, SM enriched outer, GalCer outer-only
- NaCl 150 mM (238 Na+ / 193 Cl-)

### Simulation protocol
- Equilibration: 6-step restraint release, 1.875 ns total
  - Steps 6.1-6.2: NVT, 1 fs
  - Steps 6.3-6.6: NPT, 1-2 fs, decreasing restraints
- Production: NPT, 4 fs (HMR), semi-isotropic barostat, 10 ns
- Platform: HIP (Metal) on Apple M4, ~69 ns/day on 92K benchmark

## Trajectory data

DCD trajectory files and RST restart checkpoints are excluded from this repo
(~2 GB total). They live in the original working directory at:
`biochemcore/charmm-gui-8190629385/openmm/`

## References

- Ingolfsson HI et al. (2017) Computational Lipidomics of the Neuronal Plasma Membrane. Biophys. J. 113:2271-2280.
- Viohl N et al. (2024) Molecular insights into the modulation of the 5HT2A receptor. bioRxiv 10.1101/2024.07.23.604750.
- Chao KW et al. (2026) Human class B1 GPCR modulation by plasma membrane lipids. Commun. Biol. 9:317.
