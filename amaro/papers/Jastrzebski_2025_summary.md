# Biased Signaling via Serotonin 5-HT2A Receptor: From Structural Aspects to In Vitro and In Vivo Pharmacology

**Citation:** Jastrzębski MK, Wójcik P, Grudzińska A, et al. *Acta Pharmaceutica Sinica B* 2025;15(9):4438–4455. https://doi.org/10.1016/j.apsb.2025.07.002

---

## One-Sentence Takeaway

The 5-HT2A serotonin receptor can be pharmacologically steered to activate only specific intracellular pathways — a phenomenon called biased agonism — and understanding its structural basis through crystallography, cryo-EM, and molecular dynamics simulations is the key to designing safer antidepressants and antipsychotics that harness therapeutic benefits without causing hallucinations.

---

## Background & Motivation

G protein-coupled receptors (GPCRs) are the most heavily targeted class of proteins in medicine: roughly 30–40% of all drugs on the market work by binding to one. For decades, the textbook model of GPCR function was simple — a ligand binds, the receptor changes shape, a G protein activates, and a downstream cascade fires. But this picture turned out to be incomplete. Receptors don't just toggle between "on" and "off." They can adopt many distinct conformational states, and different states preferentially engage different intracellular partners, producing qualitatively different cellular outcomes from the same receptor.

This property — called **functional selectivity** or **biased agonism** — is especially consequential for the serotonin 5-HT2A receptor. This receptor sits at the intersection of two major drug problems. On one hand, it mediates the antidepressant and anxiolytic effects that make it a compelling psychiatric drug target. On the other hand, its activation by classical psychedelics like LSD and psilocybin is responsible for hallucinations — the side effect that has historically blocked the therapeutic use of 5-HT2A agonists. For many years, these two outcomes seemed inseparable. The insight that drives this entire review is that they might not have to be: if hallucinations and therapeutic effects are mediated by different downstream signaling branches, a carefully designed biased agonist could activate one while sparing the other.

The 5-HT2A receptor couples primarily to two downstream effector systems. The first is the Gq/11 protein pathway, which activates phospholipase C and triggers a cascade involving IP3, diacylglycerol (DAG), calcium release, and protein kinase C. The second is the beta-arrestin pathway, which desensitizes the receptor, drives its internalization, and activates MAP kinase/ERK signaling through a G-protein-independent mechanism. Evidence now points to Gq activation as the primary driver of hallucinogenic effects, while beta-arrestin recruitment is associated with antidepressant-like outcomes without psychoactive properties. This is the core therapeutic logic of the entire field.

---

## Approach & Methods

This is a comprehensive review paper, not a single experimental study. The authors synthesize findings from multiple lines of investigation: structural biology (X-ray crystallography and cryo-electron microscopy of 5-HT2A receptor complexes), computational approaches (molecular dynamics simulations, molecular docking, virtual screening), in vitro pharmacological assays, and in vivo behavioral studies in rodents.

The structural work is foundational because it provides the molecular-level picture of what "biased agonism" actually looks like physically — which residues move, which loops shift, how transmembrane helices reorient when a biased versus a balanced agonist binds. The computational work extends this by exploring dynamic receptor behavior that static crystal structures cannot capture, and by enabling rational design of new ligands. The assay work validates computational predictions in cells. The behavioral work (head twitch response, forced swim test, tail suspension test) translates cellular findings into organism-level outcomes that are clinically relevant.

A key methodological emphasis of the review is the challenge of measuring biased signaling accurately. Assays that detect only one pathway at a time (like the classic IP3 accumulation assay) can miss the full picture. The authors detail several more sophisticated approaches: BRET (bioluminescence resonance energy transfer) assays that detect G protein coupling or beta-arrestin recruitment in real time; TRUPATH and ONE-GO platforms that simultaneously monitor up to 14 G protein pathways; PRESTO-TANGO for arrestin-biased signal detection; and the biosensor psychLight for detecting hallucinogenic potential in cells.

---

## Key Findings

### The Two Primary Signaling Branches and Their Consequences

The most clinically important organizing principle is the divergence between Gq/11 and beta-arrestin signaling. When the 5-HT2A receptor activates Gq/11, phospholipase C cleaves PIP2 into IP3 and DAG. IP3 releases Ca2+ from the endoplasmic reticulum, and this calcium signal activates calmodulin, transglutaminase, and PKC, among other effectors. Gq activation also feeds into MAP kinase/ERK signaling and is essential for the hallucinogenic Head Twitch Response (HTR) in rodents — a widely used proxy for psychedelic activity. In mice where Gq is genetically ablated or pharmacologically blocked, psychedelics lose their HTR-inducing property, confirming the causal link.

Beta-arrestin recruitment does the opposite: it terminates G protein signaling by sterically blocking Gq coupling (desensitization), promotes receptor internalization, and independently activates ERK1/2, Raf-1, and MEK1 through a G-protein-independent mechanism. Importantly, beta-arrestin-biased ligands such as IHCH-7086 and IHCH-7079 produce antidepressant-like effects in rodent forced swim and tail suspension tests without generating hallucinogenic psychoactive effects. This directly supports the therapeutic hypothesis.

### Structural Determinants of Bias

Several structural features of the receptor are responsible for routing signaling toward one pathway or the other.

**Transmembrane helix 7 (TM7)** is a critical switch. In GPCRs generally, TM7 contains a conserved proline kink (P7.50) and a functionally critical NPxxY motif. In the Gq-coupled (balanced) conformation, TM7 adopts one orientation; when the receptor shifts toward arrestin-biased signaling, TM7 twists counterclockwise (as viewed from outside the cell) and moves the intracellular end of TM7 closer to TM3. This repositioning specifically enables beta-arrestin docking. The W6.48 "toggle switch" residue in TM6 also plays a central role: it induces a cascade of conformational changes in TM5, TM6, and TM7 that produce the distinct non-canonical intermediate state associated with arrestin bias.

**The third intracellular loop (ICL3)** makes direct contacts with arrestin and is essential for functional selectivity. Phosphorylation of Ser280 in ICL3 differentiates receptor molecules activated by hallucinogenic agonists (like DOI) from those activated by non-hallucinogens (like lisuride) — this is a molecular barcode written in post-translational modifications that directs the receptor toward different downstream fates.

**The second intracellular loop (ICL2)** further modulates bias. An I181E mutation in ICL2 simultaneously reduces Gaq coupling and increases beta-arrestin interaction, underscoring that a single residue can quantitatively shift the bias ratio between the two pathways.

**The second extracellular loop (ECL2)** influences which G protein subtype gets activated. Ligand interactions with ECL2 primarily determine whether Gaq, Gai, or another subtype is preferentially engaged.

### Computational Insights from Molecular Dynamics

Molecular dynamics (MD) simulations have been especially powerful for understanding how the receptor behaves dynamically — something static crystal structures fundamentally cannot show. Perez-Aguilar et al. used MD to show that the ICL2 of the 5-HT2A receptor adopts a distinct "outward-upward" conformation when hallucinogenic compounds are bound, a shape not seen with non-hallucinogens. This conformation involves critical residues D1723.49 and H1833.52. Marti-Solano et al. went further, using MD to learn structural patterns from known biased ligands and then design new ones. They identified hotspot residues: binding with N6.55 promotes arachidonic acid signaling, while binding with S5.46 promotes inositol phosphate signaling. Multiple novel biased ligands were designed this way and validated in vivo as potential antipsychotics.

Kaplan et al.'s virtual screen of 75 million tetrahydropyridine compounds against a 5-HT2A receptor model generated two lead agonists, (R)-69 and (R)-70, with EC50 values of 41 and 110 nmol/L. Both showed Gq-biased signaling, high brain permeability, and — critically — no psychedelic activity in vivo while retaining antidepressant-like effects.

### Clinical Drug Landscape

The review provides a detailed map of how currently approved drugs relate to the biased signaling framework (Table 1). Classical antipsychotics like risperidone, clozapine, olanzapine, and haloperidol all function as inverse agonists that broadly inhibit 5-HT2A signaling. Pimavanserin — the only FDA-approved drug acting specifically on 5-HT2A without dopamine D2 receptor activity — is an inverse agonist at the 5-HT2A–Gq pathway and shows inverse agonism at the 5-HT2A–Gi1 pathway. Its unique selectivity for serotonin over dopamine receptors makes it valuable for treating Parkinson's disease psychosis without worsening motor symptoms.

For antidepressants, the current landscape (MAOIs, SSRIs, SNRIs) works indirectly by modulating serotonin availability. Biased agonism offers a different mechanism: directly activating the receptor's beta-arrestin pathway to achieve antidepressant effects without triggering the Gq-mediated psychedelic cascade.

### Psychedelics and the Separation of Therapeutic from Hallucinogenic Effects

The question of whether hallucinogenic and therapeutic effects can be separated is not fully settled. Strong evidence supports Gq as the driver of hallucinations (HTR in rodents requires Gq; beta-arrestin-biased ligands reduce HTR while maintaining antidepressant effects). However, some complexity remains. Serotonin itself is a balanced agonist with high potency for both G protein and beta-arrestin pathways, yet it does not produce psychedelic effects — a puzzle that has led to the concept of "location bias," where membrane-permeable ligands (like synthetic psychedelics) can engage intracellular pools of the receptor that serotonin (membrane-impermeable) cannot reach, producing different downstream outcomes from the same receptor. This suggests the signaling geography (where in the cell the receptor is activated) may matter as much as which pathway is activated.

---

## Significance & Implications

### Direct Relevance to Your BioChemCore Work

This paper is deeply relevant to your MD simulation project on the 5-HT2A receptor. The structural features discussed — TM7 dynamics, the NPxxY motif, the toggle switch residue W6.48, the role of ICL2 and ICL3 — are exactly the kinds of motions you will observe (or fail to observe, depending on timescale) in your MD trajectories. When you analyze RMSD and RMSF, these are the residues and loops you want to pay attention to. The paper also gives you a clear framework for interpreting what conformational changes mean biologically: if TM7 rotates and the NPxxY motif shifts position, that corresponds to a shift toward arrestin-biased signaling.

The MD simulations described in the paper (particularly Perez-Aguilar et al. showing the ICL2 outward-upward conformation in hallucinogen-bound receptor) are exactly the kind of analysis you could replicate or extend. The fact that the paper identifies specific residues (D172, H183 in ICL2; W6.48 toggle switch; N1.50, W6.48, N7.49 in the NPxxY/NP region) gives you concrete hypotheses to test in your own trajectory — do these residues move? Do they change their hydrogen bonding patterns or contact distances?

### Broader Scientific Significance

This review represents a paradigm shift in how we think about GPCRs as drug targets. The old model was "activate receptor = one outcome." The new model is "activate receptor in a specific conformational state = specific subset of outcomes." This is functionally similar to the concept of allosteric modulation but at the level of the receptor's own signaling machinery.

The practical payoff is enormous. If the separation of hallucinogenic from antidepressant effects is reliable and robust across compounds, it would open the door to a new generation of serotonergic antidepressants, anxiolytics, and antipsychotics that work more precisely and produce fewer side effects than existing drugs. The fact that multiple independent research groups have now identified beta-arrestin-biased 5-HT2A agonists with antidepressant-like effects in rodents is encouraging.

---

## Limitations & Open Questions

**The separation is not clean.** The evidence that Gq drives hallucinations and beta-arrestin drives antidepressant effects is compelling but not complete. The fact that serotonin is a balanced agonist but is not psychedelic suggests that location bias, receptor trafficking, and cellular context all contribute. The field does not yet have a simple predictive rule for what makes a compound hallucinogenic.

**Rodent behavioral models have limits.** The HTR is a widely used proxy for hallucinogenic potential in humans, but it is not a perfect one. Translational validity from mouse behavioral assays to human psychedelic experience requires caution.

**Measuring bias is genuinely hard.** Bias factors depend heavily on which assay is used, which cell line, which reference compound is chosen for normalization. A compound that looks "beta-arrestin biased" in one assay system may not be in another. The review acknowledges this directly.

**Most novel biased ligands are preclinical.** The exciting compounds — IHCH-7086, IHCH-7079, (R)-69, (R)-70, 25CN-NBOH — are research tools or early-stage investigational compounds, not approved drugs. The path from a biased agonist in a mouse forced swim test to an approved antidepressant is long.

**The Gi pathway is undercharacterized.** The review focuses primarily on Gq and beta-arrestin, but the 5-HT2A receptor also signals through G12/13 and Gi/o proteins, phospholipase A2, and phospholipase D. These pathways receive much less attention and their roles in therapeutic versus adverse effects are unclear.

---

## Key Terms & Concepts

**Biased agonism (functional selectivity):** The ability of a ligand to preferentially activate one downstream signaling pathway over another at the same receptor, by stabilizing a particular receptor conformation that couples more efficiently to one effector protein.

**Gq/11 signaling:** The "canonical" 5-HT2A pathway in which receptor activation stimulates phospholipase C, producing IP3 and DAG, releasing intracellular calcium, and activating PKC. This pathway is causally linked to hallucinogenic effects.

**Beta-arrestin:** An intracellular scaffold protein that binds to phosphorylated, activated GPCRs. It desensitizes G-protein signaling, promotes receptor internalization, and independently activates ERK/MAPK cascades. Beta-arrestin recruitment at 5-HT2A is associated with antidepressant effects without hallucinations.

**NPxxY motif:** A highly conserved sequence in transmembrane helix 7 of Class A GPCRs that acts as a structural switch during receptor activation. Its repositioning is a key physical signature of the transition toward arrestin-biased signaling states.

**Toggle switch (W6.48):** The tryptophan residue at position 6.48 in TM6 whose rotation triggers a cascade of conformational changes in TM5, TM6, and TM7, moving the receptor into a non-canonical intermediate state associated with arrestin bias.

**BRET (Bioluminescence Resonance Energy Transfer):** An assay technique used to detect protein-protein interactions (like receptor-arrestin or receptor-G protein coupling) in living cells by fusing one protein to a luciferase donor and the other to a fluorescent acceptor — energy transfer only occurs when the two are within ~115 Å of each other.

**Head Twitch Response (HTR):** A rapid, high-frequency rotational head movement in rodents reliably induced by 5-HT2A agonists with hallucinogenic properties. It requires Gq activation and is used as a standard behavioral readout for hallucinogenic potential in drug screening.

**Location bias:** The hypothesis that membrane-permeable ligands can activate intracellular (endosomal or ER-localized) pools of GPCRs that endogenous, membrane-impermeable ligands like serotonin cannot reach, producing distinct signaling signatures from the same receptor protein.
