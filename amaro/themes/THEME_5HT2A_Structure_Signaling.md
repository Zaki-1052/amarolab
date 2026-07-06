# Master Thematic Summary: 5-HT2A Receptor Structure & Signaling

**Theme group:** 12 papers covering the structural biology, pharmacology, computational modeling, and in vivo pharmacology of the serotonin 2A receptor.

**Prepared for:** Zara — BioChemCore, UCSD Bioinformatics Year 2

---

## 1. Theme Overview

These twelve papers collectively build the scientific case for why the 5-HT2A receptor is one of the most consequential and actively studied membrane proteins in neuroscience. Together they span nearly two decades of work — from the first formal articulation of biased signaling as a concept (Urban 2007, Raote 2007) through a wave of cryo-EM structures (Cao 2022, Gumpper 2025, Xu 2026), computational dissections of receptor dynamics (Viohl 2025, Peeters 2025, Kossatz 2024, Wallach 2023), and emerging debates about which downstream pathway actually causes hallucinations (Wallach 2023 vs. Xu 2026). For BioChemCore, these papers are not just background reading — they define the exact structural features, key residues, and dynamic behaviors you will observe when you run your own MD simulation of this receptor.

---

## 2. The Narrative Arc

### The Foundation: A Single Receptor, Many Outputs (2007)

The story starts with a conceptual revolution. For decades, pharmacologists assumed that a drug's "intrinsic efficacy" at a receptor was a fixed, system-independent number — the same output regardless of which cell you measured it in. Urban 2007 (a landmark consensus paper signed by the era's leading GPCR pharmacologists) dismantled this assumption decisively. They showed, using the 5-HT2A and 5-HT2C receptors as their central examples, that the same drug at the same receptor can be a full agonist for one downstream pathway while being a partial agonist — or even an inverse agonist — for a completely separate pathway measured in the same cell. They named this **functional selectivity** (also called biased agonism).

Simultaneously, Raote 2007 provided the companion biological narrative. This book chapter laid out what the 5-HT2A receptor actually does in a neuron: it concentrates on apical dendrites of cortical pyramidal neurons, signals canonically through the Gq-PLC-IP3-calcium cascade, and has a remarkable ability to internalize via a beta-arrestin-independent mechanism. Crucially, Raote 2007 noted that hallucinogenic ligands like LSD and psilocybin do not produce their psychedelic effects simply by activating the IP3 pathway — the hallucinogenic response correlated better with arachidonic acid (AA) release, a distinct downstream cascade. The 5-HT2A receptor was thus from the very beginning a paradigm case for the idea that one receptor can feel pharmacologically like multiple different receptors depending on which drug binds it.

The Cummins 2025 review synthesizes this foundational thinking into its most mature form, placing atomic-resolution structural data alongside decades of mutagenesis, pharmacology, and behavioral studies to show exactly how the receptor's three binding pocket sub-regions — the orthosteric binding pocket (OBP), the extended binding pocket (EBP), and the ECL2 lid region — combine to determine which signaling pathway any given ligand will preferentially activate.

### The Structural Era Begins (2022–2025)

The conceptual framework of biased agonism demanded a structural explanation: what does the receptor actually look like in each signaling state, at atomic resolution? Cao 2022 delivered the first major answer. Working with the closely related 5-HT2B receptor (a validated structural model for 5-HT2A), the team solved three cryo-EM structures of the same receptor bound to LSD in its transducer-free, Gq-coupled, and beta-arrestin-coupled states. This was the first time any receptor had been captured in all three states with the same ligand. The findings were striking: beta-arrestin coupling requires a larger outward displacement of TM5 (1.7 Å extra) and TM6 (2.5 Å extra) compared to Gq coupling, because the bulkier helical finger loop of beta-arrestin needs more room than the thinner alpha-5 helix of the G protein. A single residue, N384 on helix 8, actually plays opposite roles in the two pathways — it hydrogen-bonds to Gq, but rotates to stack hydrophobically with beta-arrestin's finger loop. This was the first direct structural demonstration that biased signaling arises from distinct receptor conformations rather than simply different interaction partners competing for a fixed receptor shape.

Gumpper 2025 then expanded the structural atlas dramatically. Seven cryo-EM structures of 5-HT2A itself — bound to serotonin, psilocin, DMT, LSD, BOL, mescaline, and the arrestin-biased compound RS130-180 — were solved in a single internally consistent study. Several landmark findings emerged. All active ligands converge on the same orthosteric site. The ergoline LSD forms a "lid" with ECL2 through its L229 contact, explaining LSD's extraordinarily long receptor residence time. The non-hallucinogenic ergoline BOL is distinguished from LSD by a single bromine atom that contacts the I163/PIF motif, potentially interfering with full PIF conformational switching. Most significantly, RS130-180 (an arrestin-biased compound) was caught stabilizing a previously predicted but never experimentally observed **non-canonical (NC) state** — the receptor is partially activated but with the NPxxY motif shifted outward in an orientation incompatible with full Gq coupling. This NC state had only been inferred from MD simulations; Gumpper 2025 gave it a crystal-clear structural face.

### Computation Reveals What Structures Cannot (2024–2025)

Static cryo-EM structures are snapshots. What the field also needed was an understanding of how the receptor moves between those snapshots. Three computational papers address this directly, each from a different angle.

Viohl 2025 ran all-atom MD simulations comparing serotonin and psilocin binding across active and inactive receptor states, with and without the Gqα subunit present. Their most important finding is deceptively simple: the active, open conformation of 5-HT2AR is not thermodynamically stable without a bound G protein. In simulations without Gqα, the receptor collapses back toward the closed state within a few hundred nanoseconds — even with an agonist bound. This is not a simulation artifact; it reflects real physics captured by the CHARMM36m force field. Viohl 2025 also resolved a long-running structural debate by computing binding free energies via potential of mean force (PMF) calculations: serotonin and psilocin both prefer the OBP over the EBP by roughly 4–6 kcal/mol, making OBP occupancy 3–4 orders of magnitude more probable. A partially open intermediate state — corresponding to the pre-coupling R'' state in GPCR activation theory — was also identified, providing the missing mechanistic link between the agonist-bound and fully G-protein-stabilized active state.

Peeters 2025 took a comparative approach, running MD simulations of seven pharmacologically diverse ligands (from antagonists to hallucinogens to non-hallucinogenic partial agonists) under two conditions each — with and without a G protein construct at the intracellular face. This 2-condition design was key: it showed unambiguously that ligands cannot fully activate the receptor on their own, confirming Viohl 2025's finding from a different methodological angle. The PCA-based conformational analysis across all 15 simulations revealed that hallucinogens (LSD, 25CN-NBOH) consistently populate a conformational region with more complete NPxxY activation and full W336 toggle switch engagement, while non-psychedelic partial agonists occupy intermediate regions. A particularly novel finding was the "alternative" rotamer of W336 observed specifically with the non-psychedelic G-protein-biased compound (R)-69 — a conformation not seen with any hallucinogen and potentially exploitable as a drug design target.

Kossatz 2024 bridged computation and experiment in the most clinically grounded paper of the group. Using four structurally related serotonin analogs with systematically varied ECL2 contact patterns, the team showed that MD simulations predicted which compounds would have higher ECL2 contact frequency — and then confirmed that higher ECL2 contact strongly correlates with Gαi family coupling bias over Gαq. In live human postmortem prefrontal cortex tissue and in mice, the Gαi-preferring compounds drove head-twitch response (a psychosis proxy) while the Gαq-preferring compounds drove long-term memory deficits. Two distinct schizophrenia-relevant behavioral phenotypes were thus pharmacologically separated at a single receptor. This is one of the most complete demonstrations anywhere in the GPCR field of how a structural detail (ECL2 contact) connects unbroken to an in vivo behavioral outcome.

### The Mechanism Debate Crystallizes (2023–2026)

The field's most active current debate is: which downstream pathway actually causes hallucinations?

Wallach 2023 provided a major piece of evidence for the "Gq hypothesis." Using a carefully engineered series of N-benzyl phenethylamine analogs that span from fully balanced to arrestin-biased agonism, they showed that Gq Emax correlates directly with the head-twitch response (HTR, a mouse hallucinogenicity proxy) with a Spearman correlation of 0.82, while beta-arrestin2 efficacy shows essentially zero correlation with HTR. A clear threshold emerged: compounds with Gq efficacy below approximately 70% of serotonin's response do not produce head twitches. Pharmacological blockade of Gq-PLC signaling in vivo with YM-254890 and edelfosine abolished the HTR entirely. MD simulations revealed the structural mechanism: arrestin-biased compounds push W336^6.48 into an intermediate rotamer state that reduces TM6 outward displacement below what full Gq activation requires.

Then Xu 2026 arrived and complicated — or rather deepened — this picture significantly. Xu 2026 argues that it is actually Gi signaling, not Gq, that drives hallucinogenic effects. This conclusion comes from pharmacological profiling across psychedelics and non-hallucinogenic analogues (nHAs), showing that psychedelics activate Gi far more strongly than nHAs do, while Gq differences are less discriminating. Pertussis toxin (which inactivates Gi/o) attenuates the HTR in vivo, while YM-254890 (the Gq inhibitor) does not. Five new cryo-EM structures of 5-HT2AR in both Gi-coupled and Gq-coupled states revealed a key molecular mechanism: Gαi's αN helix positions 9 Å closer to ICL2 than Gαq does, and a salt bridge between R189^4.39 in ICL2 and Glu in Gαi is essential for Gi coupling. Critically, Xu 2026 also found that Gq signaling mediates the therapeutic antidepressant and anxiolytic effects — meaning that Gi drives hallucinations and Gq drives therapeutics, which is essentially the opposite assignment from what Wallach 2023 concluded.

These two high-quality papers reach different conclusions about which pathway causes hallucinations using complementary but distinct experimental designs. The current state of the field is that both Gq and Gi pathways appear necessary for the full psychedelic behavioral phenotype, and the relative contributions may depend on brain region, drug, dose, and timepoint. Ortiz 2026 provides useful methodological context here by reviewing how drug-target residence time (how long a drug stays bound) can also influence apparent pathway bias — a drug's signaling fingerprint changes over time, and static efficacy measurements at a single timepoint may not tell the full story.

Jastrzebski 2025 and Cummins 2025 both serve as synthetic reviews that sit above the active debate, integrating the structural, pharmacological, and behavioral evidence into a coherent framework while honestly flagging what remains unresolved. Both point to "location bias" — the idea that membrane-permeable synthetic psychedelics may activate intracellular receptor pools that the endogenous, membrane-impermeable serotonin cannot reach — as an underexplored dimension that could explain some of the discrepancies between signaling assays and in vivo behavior.

---

## 3. Key Concepts and Converging Evidence

These are the findings that multiple independent papers agree on. They represent the highest-confidence knowledge in this field.

**The OBP is the primary binding site for all active ligands.** Both Viohl 2025 (free energy calculations) and Gumpper 2025 (cryo-EM + docking) independently confirm that serotonin, psilocin, LSD, mescaline, and other active compounds all bind the deeper orthosteric pocket. The earlier suggestion that tryptamines sit in the EBP is not supported by either free energy data or biochemistry.

**D3.32 is the universal anchor.** Every paper that discusses binding contacts agrees: the conserved aspartate at position 3.32 forms a salt bridge with the protonated amine of essentially every 5-HT2A agonist. It is the indispensable anchor of ligand recognition.

**G protein presence is required to stabilize the fully active conformation.** Viohl 2025 and Peeters 2025 independently show — from different simulation setups — that the receptor cannot maintain the TM6-open, active conformation without a bound transducer. Agonist binding alone biases the conformational ensemble but does not lock in the active state.

**W6.48 is the central toggle switch.** Gumpper 2025, Peeters 2025, Wallach 2023, and Cummins 2025 all converge on the rotameric state of W336^6.48 (also written W6x48) as the key molecular switch. Its chi2 dihedral angle distinguishes inactive, active, and non-canonical receptor conformations. Ligands that physically contact W6.48 tend to be biased agonists.

**The NPxxY motif marks the distinction between psychedelic and non-psychedelic activation.** Peeters 2025 and Gumpper 2025 both show that psychedelic agonists stabilize the NPxxY motif in its active conformation more fully than non-psychedelic partial agonists. This motif's behavior is one of the most reliable computational metrics of receptor activation state.

**ECL2 is not just structural — it actively shapes signaling outcomes.** Kossatz 2024 and Gumpper 2025 independently demonstrate that ECL2 contacts (especially at L228-L229-A230) modulate G protein coupling selectivity and ligand kinetics. More ECL2 contact shifts preference toward Gαi signaling. ECL2 also forms the "lid" that explains LSD's long receptor residence time.

**The head-twitch response requires 5-HT2A receptor activation.** Kossatz 2024, Wallach 2023, and Xu 2026 all use HTR as the in vivo readout, and all confirm it is 5-HT2AR-dependent (absent in receptor knockout mice and blocked by antagonists).

---

## 4. Active Debates and Unresolved Questions

**The most important debate: which pathway causes hallucinations — Gq or Gi?**

Wallach 2023 provides strong evidence for Gq: beta-arrestin2-biased compounds fail to produce HTR; Gq efficacy above ~70% is the threshold for HTR; pharmacological Gq blockade abolishes HTR in vivo.

Xu 2026 provides strong evidence for Gi: psychedelics activate Gi much more strongly than non-hallucinogenic analogues; pertussis toxin (Gi/o blocker) attenuates HTR; Gq blockade does not prevent HTR but does prevent therapeutic effects.

These two papers are not simply contradictory — they may be capturing different aspects of the same complex phenomenon. Jastrzebski 2025 and Cummins 2025 both note that serotonin itself is a balanced agonist with high Gq efficacy but is not psychedelic, which challenges a simple "Gq = hallucination" rule. The most likely resolution is that both Gq and Gi activation are necessary components of the full psychedelic response, and that the apparent discrepancy arises from differences in the specific behavioral endpoints tested, the doses used, and the drugs chosen. This debate is genuinely unresolved as of 2026.

**Where exactly do tryptamines bind?**

Viohl 2025's free energy calculations clearly favor OBP binding for serotonin and psilocin, and Gumpper 2025's cryo-EM structures confirm OBP occupancy. An earlier structural report had suggested tryptamines sit in the EBP; both of these more recent, orthogonally validated papers argue against that interpretation. The OBP is now the consensus.

**Can therapeutic effects be separated from hallucinations?**

Xu 2026 says yes — by designing Gq-biased agonists, you can retain therapeutic Gq-mediated effects while avoiding Gi-driven hallucinations. Wallach 2023 implies the opposite — that partial Gq agonism below the ~70% threshold might retain neuroplasticity while avoiding hallucinations, but that both effects ultimately go through Gq. Jastrzebski 2025 is cautiously optimistic that separation is achievable but emphasizes that the data are preliminary and system-dependent. This question has enormous clinical stakes.

**Does the 70% Gq efficacy threshold from rodents translate to humans?**

Wallach 2023 establishes this threshold in mice. Cummins 2025 notes the single amino acid difference at position 5.46(242) between mouse (Ala) and human (Ser) 5-HT2A receptors creates order-of-magnitude differences in agonist pharmacology. The threshold may be real in mice but its human equivalent is unknown.

---

## 5. Direct BioChemCore Relevance

This section is a practical guide for using these papers in your own simulation work.

### Which PDB Structures to Use

| Purpose | PDB Code | Source Paper | Notes |
|---|---|---|---|
| Active state, Gq-coupled (5-HT2A, LSD) | 7RAN / 6WHA | Gumpper 2025 / Prior work | Best for Gq-coupled simulations; most cited active state |
| Active state, Gq-coupled (5-HT2A, serotonin) | 9ARX | Gumpper 2025 | Endogenous ligand in the Gq state |
| Active state, Gq-coupled (5-HT2A, psilocin) | 9AS7 | Gumpper 2025 | Psilocybin/psilocin target state |
| Non-canonical arrestin-biased state | 9AS9 / 9ASA | Gumpper 2025 | RS130-180 structure; useful to understand bias |
| Gi-coupled (5-HT2A, DOI) | 9LL7 | Xu 2026 | First structure in Gi-coupled state |
| Gi-coupled (5-HT2A, psilocin) | 9LL8 | Xu 2026 | Psychedelic in Gi-coupled state |
| 5-HT2B with LSD, Gq-coupled | 7SRR | Cao 2022 | Best 5-HT2B reference for comparison |
| 5-HT2B with LSD, beta-arrestin | 7SRS | Cao 2022 | Only structure in arrestin state with LSD |

Viohl 2025 used PDB 7RAN/6WHA (active, Gq-coupled) and 6A93 (inactive) as their starting structures — these are solid, well-validated choices for an apo or ligand-bound simulation.

### Key Residues to Monitor in Your Trajectory

These residues are the most informative structural sensors across all papers in this group.

**Primary binding pocket:**
- D3.32 (D155) — the universal amine anchor; watch for salt bridge integrity
- W6.48 (W336) — the toggle switch; monitor its chi2 dihedral angle (~120° inactive, ~50° active, ~-15° non-canonical)
- S3.36 (S159) — unique to 5-HT2A (vs. 5-HT2B/C); hydrogen bonds serotonin but not psilocin
- S5.46 (S242) — the TM5 "bulge" residue; hydrogen bond here is the G protein-biased vs. arrestin-biased switch per Peeters 2025; also the site of mouse/human pharmacological divergence
- F6.52 (F340) — contacts all three chemotype classes

**Activation state sensors:**
- R3.50 / E6.30 ionic lock (R173 / E318) — broken in active state; Viohl 2025 tracks this as a primary activation metric
- Q5.66 / E6.30 (Q262 / E318) distance — second Viohl 2025 activation distance metric
- F6.44 (F332) — PIF motif phenylalanine; its inward rotation follows W336 toggle
- Y7.53 (Y380/Y387) — NPxxY tyrosine; active position vs. inactive diverges between psychedelic and non-psychedelic ligands

**Extracellular gates:**
- L228, L229, A230 in ECL2 — Kossatz 2024 shows contact here predicts Gαi coupling
- ECL2 backbone generally — forms the LSD "lid"; highly dynamic

**G protein interface:**
- ICL2 (residues ~I181-I183) — Kossatz 2024 shows I181E shifts bias; Cao 2022 shows it mediates Gq alpha-N helix contact
- R189^4.39 (ICL2) — Xu 2026 shows this forms a salt bridge specific to Gi coupling
- Helix 8 / N384 — Cao 2022 shows this is the molecular switch that differs between Gq and arrestin coupling

### Membrane Composition

Peeters 2025 used the most biologically realistic membrane, modeled after synaptic vesicle composition:
- 57 POPC, 18 POPS, 8 PSM, 12 CER160, 52 POPE, 4 POPI, 42 cholesterol

If you want a simpler bilayer, Kossatz 2024 and Viohl 2025 both used pure POPC — acceptable for a first-pass simulation in BioChemCore.

Viohl 2025's membrane uses an asymmetric leaflet composition based on postsynaptic membrane lipidomics (outer leaflet: POPC-heavy; inner leaflet: POPS and POPE-enriched). This is the most anatomically accurate choice if you want to replicate real cortical dendrite membrane behavior. The EBP and side-extended pocket (SEP) of 5-HT2AR are naturally occupied by monoolein lipid in crystal structures (Viohl 2025) — a reminder that the extracellular face of the receptor interacts dynamically with lipids, not just ligands.

### Analysis Metrics

**Day 7 of BioChemCore focuses on RMSD, RMSF, and protein-lipid contacts.** Here is how the papers extend those basics:

- Track the **R173–E318 ionic lock distance** and **Q262–E318 distance** (Viohl 2025) as mechanistically interpretable activation metrics, rather than total backbone RMSD alone.
- Apply **PCA to a curated set of inter-helix distances and microswitch torsion angles** (the DOF approach from Peeters 2025). This lets you visualize where in conformational space your simulation sits relative to psychedelic vs. non-psychedelic receptor states.
- Monitor **W336 chi2 dihedral angle** over time (Wallach 2023, Peeters 2025) — it should converge on a stable rotameric state and can identify which functional state the simulation is sampling.
- Calculate **ECL2 contact frequency** with any bound ligand or lipid headgroup (Kossatz 2024).
- Compute the **A100 activation index** (Viohl 2025) — a weighted combination of six intramolecular Cα distances that categorizes the receptor as inactive, intermediate, or active at each trajectory frame.

If your simulation starts from the active state structure (6WHA or 7RAN) without a G protein construct, expect TM6 to partially close and the receptor to drift toward the partially-open intermediate described by Viohl 2025. This is not a failure — it is the partially-open R'' intermediate state, which is physically real and scientifically interesting.

---

## 6. Recommended Reading Order

Read the summaries in this sequence. Each one builds on the previous.

1. **Raote 2007** — Start here. This is the biological foundation: what 5-HT2A is, where it lives in neurons, what it signals through, and why it matters. Without this context, the structural and pharmacological papers are abstract.

2. **Urban 2007** — Read this immediately after Raote. Urban 2007 establishes the concept of functional selectivity/biased agonism from first principles and uses 5-HT2A as the central example. It explains why this receptor became the proving ground for a paradigm shift in pharmacology.

3. **Cummins 2025** — The most comprehensive review in the group, written by the leading synthetic chemist in psychedelic pharmacology. Read it as a bridge from the conceptual foundation (papers 1–2) to the structural era. It explains the binding pocket geometry, the three chemotype classes, and all the key microswitch motifs you will encounter in every subsequent paper.

4. **Cao 2022** — First cryo-EM paper and first triple-state structural comparison (unliganded, Gq-coupled, arrestin-coupled) with the same ligand. This is where the structural differences between Gq and arrestin signaling become concrete and measurable.

5. **Gumpper 2025** — The structural atlas: seven structures of 5-HT2A across all major chemotypes. Read this after Cao 2022 and you will see how the patterns from that paper extend across the full pharmacological landscape. The NC state and 3DFlex conformational ensemble analysis are the conceptual highlights.

6. **Viohl 2025** — Your first computational paper. It directly addresses the questions most relevant to BioChemCore: where do serotonin and psilocin actually bind (OBP vs. EBP), what happens to the receptor when Gqα is absent, and how do you interpret RMSD and conformational metrics. The methods section maps almost exactly onto what you will do.

7. **Peeters 2025** — The most BioChemCore-proximal paper. The exact same CHARMM-GUI preparation, CHARMM36m force field, and NPT production protocol as your simulation. Read this to understand how to go beyond simple RMSD: the PCA of DOFs and the two-condition design (with and without G protein) are directly replicable strategies.

8. **Wallach 2023** — The "Gq hypothesis" for hallucinations. By now you have enough structural background to follow the MD simulation in this paper (W336 rotamer analysis, TM6 displacement) and to evaluate the pharmacological evidence rigorously.

9. **Kossatz 2024** — The paper that connects ECL2 structural contacts to distinct G protein subtypes and distinct behavioral phenotypes (psychosis vs. memory deficits) in one experiment. The cleanest demonstration of the "one receptor, multiple behavioral outputs" principle.

10. **Xu 2026** — The "Gi hypothesis" for hallucinations. Read this after Wallach 2023 so you can see exactly where the two papers agree and where they diverge. The five cryo-EM structures of Gi-coupled vs. Gq-coupled 5-HT2A are the most recent and most mechanistically detailed structures available.

11. **Jastrzebski 2025** — A synthetic review that is explicitly designed to bridge structural data to clinical pharmacology. Read it near the end, when you have enough context to evaluate its synthesis critically. The TM7 dynamics, ICL3 phosphorylation, and location bias sections are the most original contributions.

12. **Ortiz 2026** — Read last. This minireview is the most methodologically abstract of the group, focused on drug-target residence time and enhanced sampling MD. It provides context for interpreting LSD's ECL2 lid effect and introduces τRAMD, metadynamics, and other simulation techniques that go beyond what BioChemCore covers but that you will encounter in the research literature going forward.

---

## 7. Key Terms Quick Reference

**5-HT2A receptor (5-HT2AR):** A seven-transmembrane G protein-coupled receptor expressed on cortical pyramidal neurons. The primary target of classical psychedelics (LSD, psilocybin, DMT, mescaline), atypical antipsychotics, and the subject of all 12 papers in this group.

**Biased agonism (functional selectivity):** When a ligand at a receptor preferentially activates one downstream signaling pathway over another. For 5-HT2AR, this most commonly describes Gq bias vs. beta-arrestin bias, or — in Xu 2026 — Gi bias vs. Gq bias.

**Gq/11 signaling:** The "canonical" 5-HT2AR pathway. Gq activates phospholipase C-beta (PLC-beta), which cleaves PIP2 into IP3 and diacylglycerol (DAG). IP3 releases calcium from the ER; DAG activates PKC. Xu 2026 argues this pathway mediates therapeutic effects; Wallach 2023 argues it mediates hallucinations.

**Gi signaling (non-canonical at 5-HT2AR):** Gi/o proteins inhibit adenylyl cyclase and activate MAPK pathways. Xu 2026 establishes that psychedelics engage this pathway far more strongly than non-hallucinogenic analogues, and argues Gi drives hallucinogenic effects.

**Beta-arrestin signaling:** Beta-arrestins bind phosphorylated GPCRs, terminate G-protein signaling, drive receptor internalization, and activate ERK independently. Cao 2022 provides the arrestin-bound receptor structure; Wallach 2023 shows arrestin efficacy does not correlate with hallucinogenicity.

**Orthosteric binding pocket (OBP):** The primary ligand binding site, deep within the TM bundle. All active ligands bind here. Anchored by D3.32. Viohl 2025 confirms thermodynamic preference for OBP over EBP by 4–6 kcal/mol.

**Toggle switch (W6.48 / W336):** The conserved tryptophan in TM6 whose chi2 dihedral angle reports receptor activation state: ~120° (inactive), ~50° (active), ~-15° (non-canonical/biased). The most practically useful single-residue conformational sensor in any 5-HT2AR simulation.

**NPxxY motif:** Asn-Pro-x-x-Tyr sequence in TM7. Its active conformation (tyrosine shifted inward, participating in a water-mediated hydrogen bond network) is diagnostic of full receptor activation. Psychedelic agonists stabilize it more completely than non-psychedelic partial agonists (Peeters 2025, Gumpper 2025).

**PIF motif:** Pro-Ile-Phe triad (P5.50, I3.40, F6.44) that rearranges during activation. F6.44 rotation following W6.48 toggle switch activation is a key step in propagating the activation signal from the binding pocket to the intracellular G-protein coupling surface.

**DRY / ionic lock:** Asp-Arg-Tyr sequence at the intracellular base of TM3 (R3.50) and a glutamate on TM6 (E6.30) form a salt bridge in the inactive state. Breaking this ionic lock — the R173–E318 distance increasing — is a hallmark of receptor activation. Viohl 2025 tracks this as a primary activation metric.

**ECL2 (extracellular loop 2):** The flexible extracellular loop above the binding pocket. It forms a "lid" over the OBP that modulates ligand residence time (LSD's slow dissociation: Gumpper 2025, Ortiz 2026) and shifts G protein subtype selectivity based on ligand contact frequency (Kossatz 2024).

**Non-canonical (NC) state:** A partial activation state intermediate between inactive and fully G-protein-coupled, stabilized by arrestin-biased agonists like RS130-180. First structurally observed in Gumpper 2025; predicted by prior MD simulations.

**Head-twitch response (HTR):** A rapid side-to-side head movement in rodents reliably induced by hallucinogenic 5-HT2AR agonists. Used by Wallach 2023, Kossatz 2024, and Xu 2026 as the primary in vivo readout for hallucinogenic potential. Blocked by 5-HT2AR antagonists; absent in receptor knockout mice.

**Drug-target residence time (tau, τ):** The average time a drug stays bound (1/k_off). Relevant to 5-HT2AR because LSD's notoriously slow dissociation is caused by ECL2 lid formation. Ortiz 2026 reviews mathematical and simulation-based methods for computing τ in GPCR systems.

---

*Synthesized from 12 individual paper summaries. All paper references use Author Year format. PDB codes verified against individual paper summaries. Written for BioChemCore program, UCSD Bioinformatics, June 2026.*
