# Master Thematic Summary: Neuroplasticity Mechanisms & Membrane Lipid Biology

**BioChemCore Reading Group | 6 Papers | Zara Alibhai**

---

## 1. Theme Overview

This group of six papers provides the biological foundation for everything you are building in BioChemCore. The neuroplasticity papers explain *why* the 5-HT2A receptor matters — it is the upstream gatekeeper of a signaling cascade that physically rebuilds atrophied neurons in the prefrontal cortex, and psychedelics exploit this to produce lasting antidepressant effects. The membrane lipid papers explain *where* 5-HT2A lives — a highly specific, compositionally tuned lipid environment in the neuronal plasma membrane that actively shapes receptor behavior. Together, these two lines of evidence transform your MD simulation from "spinning a receptor in lipid soup" into a biologically grounded model of a therapeutically critical protein in its real membrane context.

---

## 2. The Narrative Arc

### Part 1 — Neuroplasticity: How the Field Got Here

The story starts with a clinical observation that could not be explained by conventional neuroscience. Classical antidepressants (SSRIs, SNRIs) take weeks to work and must be taken daily. Ketamine, a dissociative anesthetic, produces antidepressant effects within hours after a single dose, and those effects persist. Then, in the 2010s, clinical trials for psilocybin showed similar durability — one or two sessions producing measurable relief from depression, PTSD, and addiction for weeks to months afterward. Why?

Ly et al. (2018) provided the pivotal answer: psychedelics are *psychoplastogens*. They coined this term to classify compounds that rapidly promote structural and functional neuroplasticity — meaning they physically rebuild atrophied neurons in the prefrontal cortex. Using cultures of rat cortical neurons, Golgi-Cox staining in live rodents, and super-resolution microscopy, Ly 2018 showed that LSD, DMT, and DOI all promoted dendritic arbor growth, spine formation, and new synapse assembly at levels matching or exceeding ketamine. Crucially, blocking the 5-HT2A receptor with ketanserin abolished all of these effects, placing 5-HT2A as the essential upstream switch. Blocking TrkB (the BDNF receptor) or mTOR (the master growth kinase) produced the same result — defining the signaling chain as 5-HT2A → TrkB → mTOR → dendritic growth.

Olson (2022) then took that empirical finding and asked the harder question: which specific downstream signaling pathway at 5-HT2A is responsible for plasticity, and can we separate it from the pathway responsible for hallucinations? This is therapeutically critical — if you could promote neuroplasticity without the perceptual effects, you would have a drug that rebuilds broken neural circuits while keeping patients fully functional. The concept of biased agonism, or functional selectivity, becomes central here: different ligands stabilize distinct conformations of 5-HT2A that preferentially activate different downstream arms (Gq, beta-arrestin, Gi). The psychLight biosensor — a circularly permuted GFP inserted into the third intracellular loop (ICL3) of 5-HT2A — demonstrated that hallucinogenic and non-hallucinogenic compounds produce physically different receptor conformations. And the compound tabernanthalog (TBG) proved the concept experimentally: a non-hallucinogenic ligand that still promotes plasticity, showing the two phenomena can be separated.

Kwan et al. (2022) completed the picture by zooming out from molecular signaling to the entire nervous system. This *Nature Neuroscience* review spans pharmacophore chemistry, receptor structure, single-neuron electrophysiology, and whole-brain fMRI, synthesizing evidence across roughly 157 studies. It confirmed that 5-HT2A is the necessary receptor for both acute perceptual effects and long-lasting structural plasticity, and it described the binding pocket geometry in atomic detail — the D155 aspartate salt bridge, hydrophobic contacts, the two-carbon pharmacophore linker — giving the MD field specific structural targets to analyze. It also cataloged the major competing theories of psychedelic action (CSTC, REBUS, SP, CCC), making explicit where mechanistic consensus exists and where significant debate remains.

By reading these three papers in order, you trace the field's trajectory: from "psychedelics promote neuroplasticity, and here is the receptor" (Ly 2018), to "here is the mechanistic debate about which signaling pathway matters" (Olson 2022), to "here is the whole-system picture, from binding pocket to brain network" (Kwan 2022).

### Part 2 — Membrane Lipids: The Environment Is Not Passive

In parallel, the lipid biology papers establish that the membrane in which 5-HT2A sits is not a generic backdrop. It is a precisely engineered, compositionally specific structure that actively shapes what the receptor can do.

Calderon et al. (1995) made the foundational observation that lipid composition differs dramatically between different neuronal compartments. Working with physically separated cell bodies and neurite extensions from cultured dorsal root ganglia, they showed that neurites — which approximate the post-synaptic membrane environment of dendritic spines — are enriched in cholesterol (C/phospholipid ratio ~0.74 vs. ~0.52 in soma), sphingomyelin, phosphatidylserine, and complex gangliosides (GM1, GM2, and GM3 are completely absent from neurites; only complex GD and GT species appear there). The co-enrichment of cholesterol and sphingomyelin is a direct signature of liquid-ordered lipid raft microdomains in the neurite membrane. This paper gave the field its first quantitative baseline for what the neuritic plasma membrane looks like chemically.

Harayama and Riezman (2018) then provided the comprehensive molecular framework for understanding why that composition exists and why it matters. Their *Nature Reviews Molecular Cell Biology* review established three principles with direct MD relevance. First, membrane physical properties — thickness, fluidity, curvature, lateral pressure — are determined by specific lipid molecular structures, and single differences (one double bond, one carbon, one headgroup) produce measurable consequences. Second, hydrophobic mismatch between a transmembrane protein's hydrophobic domain and the local bilayer thickness is a primary mechanism for protein sorting and conformational modulation. Third, lipid composition is maintained by active homeostatic mechanisms, not passive assembly, which means the composition you observe in a resting neurite is there by regulated design.

Lim and Wenk (2009) completed the lipid arc by giving quantitative composition data for actual neuronal membranes at the synapse — specifically for purified synaptic vesicles (PC ~28.6%, PE ~26.6%, cholesterol ~21.4%, PS ~9.6%, ceramide + glucosylceramide ~6.0%, SM ~4.3%, PI ~2.1%). Beyond composition, they documented the functional roles of each lipid: PI(4,5)P2 recruits endocytosis machinery; PS provides the electrostatic scaffold for C2-domain proteins; PE and plasmalogens facilitate membrane fusion; cholesterol modulates rigidity and microdomain formation. Each lipid has a specific mechanistic role, not just a structural filler function.

---

## 3. Key Concepts and Converging Evidence

Several findings are reinforced independently across multiple papers, giving them high confidence.

**5-HT2A is the required upstream receptor for psychedelic plasticity.** Ly 2018 showed ketanserin blockade abolishes all psychoplastogenic effects in cell culture. Olson 2022 confirmed 5-HT2A genetic knockout eliminates the effect in vivo. Kwan 2022 provided the human pharmacology confirmation: ketanserin pre-treatment blocks both subjective and neuroimaging effects in clinical studies. This three-way convergence is as close to a settled fact as this field has produced.

**The TrkB-mTOR axis is required downstream of 5-HT2A.** Ly 2018 provided direct pharmacological evidence. Olson 2022 placed this in a broader signaling framework involving BDNF, AMPA receptors, and a potential glutamate burst. Both papers agree that mTOR inhibition (rapamycin) completely blocks structural plasticity.

**Cholesterol and sphingomyelin co-enrichment defines the neurite/dendritic plasma membrane.** Calderon 1995 measured this directly in isolated neuronal fractions. Harayama 2018 explains the physical basis: these two lipid classes preferentially co-partition into liquid-ordered phases. Lim 2009 confirms both are present in significant quantities at the synapse. All three papers independently support the conclusion that the post-synaptic membrane has a liquid-ordered character distinct from bulk ER membranes.

**Lipid asymmetry between leaflets is functionally critical.** Harayama 2018 establishes this as a general principle. Lim 2009 gives specific mechanistic examples: PS on the inner leaflet is the electrostatic scaffold for synaptotagmin and PKC-alpha. Calderon 1995 documents elevated PS in neurites, implying more inner-leaflet signaling capacity in the dendritic compartment.

**Biased agonism at 5-HT2A separates hallucination from neuroplasticity.** Both Olson 2022 and Kwan 2022 develop this concept, with Olson providing the psychLight biosensor evidence for distinct receptor conformations, and Kwan providing the pharmacological evidence that different ligands produce different pathway activation ratios. Both cite TBG as the clearest experimental proof of dissociation.

---

## 4. Active Debates and Unresolved Questions

Not everything in this group of papers is settled. Here are the live debates you should be aware of.

**Is a large glutamate burst necessary for psychoplastogenesis?** Olson 2022 presents this as a likely step in the pathway — 5-HT2A activation triggers presynaptic glutamate release, AMPA activation, and then BDNF secretion. But he also notes that non-hallucinogenic psychoplastogens (which presumably do not trigger the same glutamate burst as classical psychedelics) still produce equivalent plasticity. The necessity of the glutamate step for serotonergic psychedelics has not been tested with direct AMPA blockade in the way TrkB and mTOR have. Kwan 2022 sidesteps this question, focusing instead on receptor-level evidence.

**Is 5-HT2A required for psilocybin-induced spine growth specifically?** Kwan 2022 flags an important discrepancy: some studies show ketanserin pretreatment does not block psilocybin-evoked spine growth, while others using knockout animals suggest it is essential. The ketanserin problem is likely methodological (poor brain penetration at standard doses achieves only ~30% receptor occupancy, per Olson 2022), but it leaves ambiguity in the specific spine remodeling arm of the pathway.

**Which 5-HT2A signaling pathway is causally responsible for neuron growth?** Olson 2022 is explicit that this has not been resolved: Gq, Gi, G12/13, beta-arrestin, and phospholipase A2 are all candidates, but none has been definitively established as the plasticity-driving arm. The psychLight evidence suggests distinct conformations exist, but conformational difference does not yet map to specific downstream pathway identity for plasticity.

**Do lipid rafts in the dendritic membrane dynamically cluster 5-HT2A?** Calderon 1995 and Lim 2009 both describe cholesterol-sphingomyelin co-enrichment consistent with raft formation. Harayama 2018 notes that in living cells, these are more likely dynamic nanodomains than stable large phases. Whether 5-HT2A preferentially partitions into raft or non-raft regions — and whether this affects its signaling bias — is not resolved by any of these papers. This is an open question that MD simulations are well-positioned to probe.

**Does the CNS vs. PNS lipid composition difference matter for your model?** Calderon 1995 explicitly uses dorsal root ganglia, a PNS system, because of methodological convenience. The authors acknowledge that CNS neurons interact with oligodendrocytes rather than Schwann cells, and CNS myelin composition differs. Lim 2009 provides SV data from CNS synapses, which is more directly applicable. The two datasets are broadly consistent but not identical — particularly in ganglioside complexity and galactolipid ratios.

---

## 5. Direct BioChemCore Relevance

This section maps paper findings directly to your MD simulation pipeline.

### Day 3 (Maestro Structure Preparation)

When you clean your 5-HT2A structure in Maestro, the papers tell you which regions to scrutinize most carefully. Kwan 2022 identifies the D155 aspartate in the binding pocket as the key electrostatic anchor for all psychedelic ligands. Olson 2022 identifies the third intracellular loop (ICL3, connecting TM5 and TM6) as the conformational readout for biased agonism — this is where psychLight inserts, and where G protein coupling occurs. These two structural loci should be checked carefully: correct protonation of D155 and correct loop modeling of ICL3 are not cosmetic — they are functionally critical.

### Day 4 (CHARMM-GUI Membrane Builder)

This is where the lipid papers have the most direct impact. Use the following composition as your starting reference, drawing from the SV data in Lim 2009 and the neuritic membrane data in Calderon 1995.

**Inner leaflet (cytoplasmic face):**
- POPC or DPPC as the dominant PC species
- PE enriched, with plasmalogen-PE (pPE) if available in your force field
- PS enriched (inner leaflet only) — the Calderon 1995 data shows 2.3-fold more PS in neurites than soma
- PI and PI(4,5)P2 at low concentrations (~2% total)

**Outer leaflet (extracellular face):**
- PC dominant
- Sphingomyelin enriched (C18 species where possible, per Harayama 2018's note about C18 specificity in sphingolipid-protein interactions)
- Cholesterol distributed across both leaflets (~21% total, per Lim 2009)

The most important practical warning from Harayama 2018: do not use a generic DPPC/cholesterol membrane for a plasma membrane protein. A 70/30 DPPC/cholesterol bilayer is too ordered and poorly models a biological plasma membrane. Target 30–40 mol% cholesterol, mixed PC species (at least one with an unsaturated sn-2 chain), and include at least a small PE fraction for curvature character.

Leaflet asymmetry: CHARMM-GUI supports asymmetric bilayer construction. Setting up PS on the inner leaflet only is both biologically accurate and mechanistically important if you want to see any PS-mediated contacts with cytoplasmic loops of the receptor in your trajectory.

### Day 5–6 (Minimization, Equilibration, Production)

During convergence monitoring, track membrane thickness as part of your equilibration check. Harayama 2018 explains that hydrophobic mismatch between TM domain length and bilayer thickness is a primary source of artifacts. If the membrane is too thin (under-equilibrated, wrong lipid composition), you may see artificial tilting of TM helices.

### Day 7 (Analysis)

**Residues to monitor in the receptor:**
- D155 (TM3): The aspartate that anchors all psychedelic ligands. Track its distance to the protonated amine of any bound ligand.
- ICL3 (TM5-TM6 intracellular loop): RMSD and RMSF of this loop discriminates G protein coupling conformations from non-coupling conformations. This is what psychLight measures.
- TM5-TM6 interface: The region that shifts most dramatically during GPCR activation. Distance between cytoplasmic ends of TM5 and TM6 is a classic activation metric.

**Lipid analysis:**
- Lipid order parameters (Scd) by lipid species: Compare ordered vs. disordered regions near the receptor vs. bulk bilayer.
- Protein-lipid contact analysis: With PS on the inner leaflet and cholesterol in both leaflets, look for preferential residence of cholesterol or PS near specific TM helices. Enrichment of cholesterol around particular TM segments is a signature of potential raft-partitioning behavior.
- Cholesterol tilt angle relative to membrane normal.

---

## 6. Recommended Reading Order

Start with the neuroplasticity papers to build the biological motivation, then move to lipids.

1. **Ly 2018** — Start here. It is the primary research paper that launched the psychoplastogen concept, it is clearly structured around a testable hypothesis, and it gives you the specific pharmacological evidence for 5-HT2A's role before you read any review paper. Every subsequent paper references it or assumes you know it.

2. **Kwan 2022** — Read this second because it provides the broadest and most rigorous survey of the entire field, including the binding pocket geometry, receptor signaling arms, network-level effects, and theoretical frameworks. It is a *Nature Neuroscience* review, so it is comprehensive and well-sourced. Reading it after Ly 2018 means you already have context for the primary data it cites.

3. **Olson 2022** — Read this third. It is the mechanistically focused review that digs deepest into the unresolved downstream signaling debate and introduces psychLight and TBG. It is most useful after you have the big picture from Kwan 2022, because you can then place each unresolved question in its proper context.

4. **Calderon 1995** — The oldest and most technically specific paper. Read it fourth because it gives you the quantitative lipid composition data for the neuronal compartments, building the empirical foundation for the more conceptual papers that follow. The methods are straightforward and the findings are clean.

5. **Lim 2009** — Read fifth. It gives the most complete functional picture of lipid roles at the synapse, including quantitative SV composition data. Calderon 1995 tells you what lipids are where; Lim 2009 tells you why each one is there and what happens if it is missing.

6. **Harayama 2018** — Read last. It is the most conceptually ambitious and broad of the lipid papers, covering diversity generation, membrane physics, protein-lipid interactions, and homeostasis across all membrane types. It is most valuable as a synthesizing framework after you have already encountered specific lipids in Calderon and Lim.

---

## 7. Key Terms Quick Reference

**Psychoplastogen** — A compound that rapidly promotes structural and functional neuroplasticity in cortical neurons (dendritic growth, spine formation, synapse assembly) with effects that persist long after the drug has been cleared. Coined by Ly 2018 to classify ketamine, classical psychedelics, and non-hallucinogenic analogs by shared biological action.

**5-HT2A receptor** — A Class A GPCR (7-transmembrane helix, Gq-coupled) expressed postsynaptically on cortical pyramidal neurons, densely concentrated in apical dendrites. The primary molecular target of classical serotonergic psychedelics and the essential upstream switch for psychoplastogenesis.

**Biased agonism (functional selectivity)** — The property of a ligand-receptor system where different ligands at the same receptor stabilize distinct receptor conformations that preferentially activate different downstream signaling pathways. At 5-HT2A, this is the mechanistic basis for why some ligands hallucinate, some promote plasticity, and some do neither.

**TrkB / BDNF** — TrkB is the high-affinity receptor tyrosine kinase for brain-derived neurotrophic factor (BDNF). TrkB activation downstream of 5-HT2A is required for all tested psychoplastogenic effects; blocking TrkB (with ANA-12) eliminates structural plasticity even in the presence of psychedelics.

**mTOR** — Mechanistic target of rapamycin. A serine/threonine kinase acting as a master regulator of protein synthesis, activated downstream of TrkB/BDNF. Rapamycin blockade of mTOR completely prevents psychedelic-induced neuritogenesis. Required for local dendritic protein synthesis that supports structural remodeling.

**psychLight** — A genetically encoded fluorescent biosensor built by inserting a circularly permuted GFP into ICL3 of the 5-HT2A receptor. Its fluorescence signal correlates with hallucinogenic potency across chemically diverse ligands, providing optical evidence for distinct receptor conformations induced by hallucinogenic vs. non-hallucinogenic compounds.

**Liquid-ordered (Lo) phase** — A membrane phase state in which acyl chains are tightly packed (ordered) but lipids retain lateral mobility (liquid). Promoted by the co-enrichment of cholesterol and sphingomyelin. The biophysical basis of lipid rafts; the dominant phase expected in the cholesterol- and sphingomyelin-rich neurite plasma membrane described by Calderon 1995.

**Hydrophobic mismatch** — The energetic penalty arising when the length of a transmembrane protein's hydrophobic domain does not match the bilayer's hydrophobic thickness. Drives protein sorting, conformational adjustment, or local membrane deformation. A primary concern for MD simulation accuracy: wrong membrane thickness produces artifactual receptor dynamics.

**Leaflet asymmetry** — The unequal distribution of lipid species between the inner (cytoplasmic) and outer (extracellular) monolayers of a bilayer. PS and PE are enriched in the inner leaflet; PC, sphingomyelin, and glycolipids dominate the outer leaflet. This asymmetry is actively maintained by flippases and is mechanistically important for cytoplasmic loop protein interactions.

**Phosphatidylserine (PS)** — An anionic glycerophospholipid confined to the inner leaflet of the plasma membrane under normal conditions. Elevated in neurites relative to soma (Calderon 1995). Provides the electrostatic scaffold for C2-domain proteins like synaptotagmin. Serves as a DHA reservoir in neurons.

**PI(4,5)P2** — Phosphatidylinositol-4,5-bisphosphate. Present at ~2% of total synaptic lipid but acts as a master regulator of endocytosis by recruiting AP2, clathrin, and dynamin. Also the precursor for DAG (which recruits MUNC-13 for vesicle priming) and IP3 (which triggers calcium release). Its cleavage product DAG is generated by PLC-beta activation downstream of Gq — the canonical 5-HT2A signaling arm.

**Ganglioside** — A complex glycolipid with a ceramide lipid anchor and one or more sialic acid residues on a sugar headgroup. Qualitatively sorted between neuronal compartments: monosialogangliosides (GM1, GM2, GM3) are present in soma but completely absent from neurites, which contain only complex GD and GT series species (Calderon 1995). Active sorting, not passive diffusion, is implied.

**Pharmacophore** — The minimal chemical scaffold responsible for receptor binding activity. For classical psychedelics at 5-HT2A: an aromatic ring separated from a protonatable basic amine by a two-carbon linker. The basic nitrogen forms a salt bridge with D155 in the binding pocket; shortening the linker by one carbon converts agonist to antagonist.

---

*Prepared for BioChemCore — Zara Alibhai, UCSD Bioinformatics Year 2. This document synthesizes summaries of Ly 2018, Olson 2022, Kwan 2022, Calderon 1995, Harayama 2018, and Lim 2009.*
