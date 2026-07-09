# 5-HT2A Receptor MD Simulations -- BioChemCore / Amaro Lab

All-atom molecular dynamics simulations of the psilocin-bound 5-HT2A serotonin receptor in a realistic neuronal membrane, built as part of the BioChemCore program in the Amaro Lab at UC San Diego.

Two systems were simulated with identical membrane composition and force field to compare G protein coupling: the original Gq-coupled receptor (PDB 9AS8) and a Gi-coupled receptor (PDB 9LL8). Both trajectories were analyzed through a 10-phase pipeline and compared side by side.

## Systems

### Gq-coupled (primary)

- **Protein:** 5-HT2AR + mini-Gq heterotrimer (chains A-D), bound to psilocin (+1 charge)
- **Source structure:** PDB 9AS8 (cryo-EM, psilocin-bound, 5-HT2AR + mini-GaqiN + Gb1 + Gg2)
- **System size:** 280,277 atoms, 128.4 x 128.4 x 181.3 A box

### Gi-coupled (comparison)

- **Protein:** 5-HT2AR + Gai1 heterotrimer (chains R/A/B/G), bound to psilocin (+1 charge)
- **Source structure:** PDB 9LL8 (cryo-EM, psilocin-bound, 5-HT2AR + Gai1 + Gb1 + Gg2)
- **System size:** 270,555 atoms

### Shared parameters

- **Membrane:** Asymmetric neuronal bilayer (585 lipids, Ingolfsson Brain PM composition)
- **Force field:** CHARMM36m + WYF cation-pi + HMR (4 fs production timestep)
- **Engine:** OpenMM 8.1 with Metal GPU backend (Apple M4)
- **Temperature:** 310.15 K (37 C), 150 mM NaCl, NPT ensemble
- **Production:** 10 ns (10 x 1 ns blocks)

## Directory structure

```
amarolab/
  setup/                      # Structure preparation files
    9AS8.pdb                    # Original PDB deposit
    9AS8_fixed.pdb              # PDBFixer output (4 chains, no ligand)
    9AS8_complex.pdb            # Protein + psilocin, uploaded to CHARMM-GUI
    psilocin.pdb                # Ligand binding-pose coordinates (RCSB naming)
    psilocin_cgenff.pdb         # Ligand with CGenFF atom names, superposed
    process_pdb.py              # PDBFixer cleanup script
    find_gaps.py, pdb_gaps.py   # Gap identification utilities
    charmm-gui-run-1/           # CGenFF topology/parameters for psilocin (lig.rtf, lig.prm)

  openmm/                   # OpenMM simulation files
    step5_input.psf           # System topology (47 MB)
    step5_input.crd           # Initial coordinates (38 MB)
    toppar.str                # CHARMM36m + CGenFF parameter stream
    sysinfo.dat               # Box dimensions
    openmm_run.py             # Main run script (modified: Metal/HIP priority)
    omm_*.py                  # OpenMM support modules
    step6.*_equilibration.*   # Equilibration inputs, logs, DCDs, restarts
    step7_*                   # Production inputs, logs, DCDs, restarts
    step6.*_equilibration.inp # Equilibration parameters (6-step restraint release)
    step7_production.inp      # Production run parameters
    step6.*_equilibration.out # Equilibration logs (convergence data)
    step7_*.out               # Production logs
    run_production.sh         # Production run wrapper
    expanse_production.sb     # SDSC Expanse SLURM batch script
    restraints/               # Restraint definitions
  charmm-gui/                 # CHARMM-GUI Membrane Builder output (Job 8190629385)
    step1_pdbreader.*           # PDB reading, protonation, disulfide, capping
    step2_orient.*              # PPM orientation (flipped: G protein below)
    step3_*                     # Lipid composition, packing, system sizing
    step4*                      # Lipid building, waterbox, ions
    step5_assembly.*            # Final assembled system
    input.config.dat            # Full CHARMM-GUI configuration record
    lig/                        # CGenFF topology and parameters for psilocin
    amber/                      # Amber input files (alternative engine)
    charmm_openmm/              # CHARMM/OpenMM input files (alternative)

  openmm/                     # OpenMM simulation files (Gq system)
    step5_input.psf             # System topology
    step5_input.crd             # Initial coordinates
    step5_input.pdb             # Initial structure (PDB format)
    toppar.str                  # CHARMM36m + CGenFF parameter stream
    sysinfo.dat                 # Box dimensions
    openmm_run.py               # Main run script (modified: Metal/HIP priority)
    omm_*.py                    # OpenMM support modules
    step6.*_equilibration.*     # Equilibration inputs, logs, DCDs, restarts
    step7_*                     # Production inputs, logs, DCDs, restarts (10 blocks)
    run_production.sh           # Production run wrapper
    expanse_production.sb       # SDSC Expanse SLURM batch script
    restraints/                 # Restraint definitions

  new-Gi/                     # Gi-coupled comparison system (PDB 9LL8)
    9LL8.pdb                    # Original PDB deposit
    9LL8_fixed.pdb              # PDBFixer output
    9LL8_complex.pdb            # Protein + psilocin for CHARMM-GUI
    psilocin_cgenff_9LL8.pdb    # Ligand with CGenFF names (reused from Gq)
    process_pdb.py              # Structure preparation script
    load.py                     # PyMOL loading script
    charmm-gui-8313215931/      # CHARMM-GUI build (same membrane composition)
    analysis/                   # Full 10-phase analysis pipeline (mirrored from Gq)

  analysis/                   # Trajectory analysis (Gq system, 10 phases)
    phase1_visual/              # VMD snapshots and visualization
    phase2_rmsd/                # RMSD time series
    phase3_rmsf/                # RMSF per-residue flexibility
    phase4_psilocin/            # Psilocin binding pose stability
    phase5_lipid_order/         # Lipid order parameters (Scd)
    phase6_contacts/            # Protein-lipid contacts
    phase7_summary/             # Summary snapshots and report
    phase8_hbonds/              # Hydrogen bond analysis
    phase9_aromatics/           # Aromatic ring rotation dynamics
    phase10_rotamers/           # Side-chain rotamer analysis (W336 toggle switch)
    p_crossphase.py             # Cross-phase correlation analysis
    rmsf_vs_contacts.png        # RMSF vs lipid contacts overlay
    gq_vs_gi_comparison.md      # Side-by-side Gq vs Gi comparison report
    gq_vs_gi_comparison.html    # Comparison report (formatted)

  docs/                       # Session logs and reference documents
    day-3-session.md            # Structure preparation (PDBFixer)
    4a-session-log.md           # Ligand parameterization (CGenFF)
    4b-session-log.md           # CHARMM-GUI Steps 1-2 (PDB reader, orientation)
    4c-session-log.md           # CHARMM-GUI Step 3 (lipid composition)
    4d-session-log.md           # CHARMM-GUI Steps 4-6 (build, input generation)
    5-session-log.md            # Equilibration and production
    5b-session-log.md           # Additional production session
    9LL8-*.md                   # Gi system setup documentation (5 files)
    GUIDE.md                    # Lab onboarding guide
    SUMMARY.md                  # MPro thesis defense walkthrough
    REFERENCE.md                # Quick-lookup glossary and repo map
    PLAN-analyses-downstream.md # Downstream analysis planning
    analyses-overview.md        # Analysis pipeline overview
    results-interpretation.md   # Trajectory results interpretation
    metal-fix.md                # OpenMM Metal plugin build notes
    model-rework.md             # Model revision notes
    sim-walkthrough.md          # Simulation protocol walkthrough
    thesis_defense.md           # Raw defense transcript

  presentation/               # Presentation materials
    pymol/                      # PyMOL rendering screenshots

  demo/                       # MOR/naloxone demo system (tutorial reference)
    9PXY.cif                    # Mu-opioid receptor structure
    step5_assembly.*            # Demo assembled system
    vmd_membrane_render.tcl     # VMD rendering script

  envs/                       # Conda environment specifications
    biochemcore_env.yml         # Local environment (macOS/M4)
    biochemcore_expanse.yml     # HPC environment (SDSC Expanse)

  amaro/                      # Amaro Lab reference materials
    amaro_scripts/              # Shared script library
    amaro_wiki/                 # Internal wiki (Obsidian export)
    OVERVIEW_All_Themes.md      # BioChemCore reading list (33 papers, 4 themes)
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
- 16 lipid species total (POPC, DOPC, POPE, POPS, POPI, SAPI, PAPC, PAPE, PAPS, SDPC, SDPE, SDPS, PSM, SSM, GalCer, cholesterol)
- NaCl 150 mM (238 Na+ / 193 Cl-)

### Simulation protocol

- Equilibration: 6-step restraint release, 1.875 ns total
  - Steps 6.1-6.2: NVT, 1 fs
  - Steps 6.3-6.6: NPT, 1-2 fs, decreasing restraints
- Production: NPT, 4 fs (HMR), semi-isotropic barostat, 10 ns
- Platform: HIP (Metal) on Apple M4, ~69 ns/day on 92K benchmark

## Analysis pipeline

Ten analysis phases were run on both trajectories, with results compared across the two G protein coupling conditions.

| Phase | Analysis | Key finding |
|---|---|---|
| 1 | Visualization | VMD/PyMOL snapshots at 0, 5, 10 ns |
| 2 | RMSD | Receptor stable at 1.3-1.5 A (Gq) / 0.8-1.1 A (Gi); Gq G protein never equilibrates |
| 3 | RMSF | Classic 7-TM flexibility pattern; D77 (salt bridge anchor) among 15 most rigid residues |
| 4 | Psilocin binding | Salt bridge intact all 100 frames (2.86 A mean); ligand RMSD 0.77 A |
| 5 | Lipid order (Scd) | Cholesterol condensing effect visible; DHA sawtooth profile correct |
| 6 | Protein-lipid contacts | 4 cholesterol binding grooves identified; TM4-TM5 groove densest |
| 7 | Summary snapshots | Exportable PDB snapshots for figures and MegaMembrane |
| 8 | Hydrogen bonds | Binding pocket H-bond network characterization |
| 9 | Aromatic rotations | Ring dynamics of binding pocket aromatic cage |
| 10 | Rotamers | W336 toggle switch chi2 dihedral analysis |

## Trajectory data

DCD trajectory files and RST restart checkpoints are excluded from this repo (~2 GB per system). They live in the original working directories at:
- Gq: `biochemcore/charmm-gui-8190629385/openmm/`
- Gi: `biochemcore/amarolab/new-Gi/charmm-gui-8313215931/openmm/`

## References

- Ingolfsson HI et al. (2017) Computational Lipidomics of the Neuronal Plasma Membrane. Biophys. J. 113:2271-2280.
- Viohl N et al. (2024) Molecular insights into the modulation of the 5HT2A receptor. bioRxiv 10.1101/2024.07.23.604750.
- Chao KW et al. (2026) Human class B1 GPCR modulation by plasma membrane lipids. Commun. Biol. 9:317.
- Gumpper et al. (2025) PDB 9AS8: psilocin-bound 5-HT2AR with mini-GaqiN.
- Xu et al. (2026) PDB 9LL8: psilocin-bound 5-HT2AR with Gai1.
