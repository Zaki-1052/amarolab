# Homology Modeling

## Preface[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=1> "Edit section: Preface")]

We study proteins. To study proteins, we need their structures. X-Ray crystallographers are our friends. X-Ray crystallographers give us nice structures. We are happy. 

One day we start a new project. Protein XYZ interests us. Protein XYZ is a pain in the arse. The X-Ray crystallographers don't like Protein XYZ. We are stuck. 

Comparative protein modelling is a family of techniques for generating protein structures based on their similarity to known protein structures. There are two main interrelated methods available to us. Homology modelling relies on detectable sequence homology correlating with structural homology. When sequence homology is not apparent, inverse folding detects structures which are compatible with the sequence we wish to model. Once we have a predicted structure, it is important to check that it is potentially a valid structure. 

## Features of Protein Structure[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=2> "Edit section: Features of Protein Structure")]

[![Phipsi.jpg](/mediawiki/images/5/5d/Phipsi.jpg)](</mediawiki/index.php/File:Phipsi.jpg>)

The polymer backbone of proteins can, in theory, exhibit an almost unrestricted set of conformations, with each peptide unit containing two fully rotatable backbone torsion angles, φ and ψ. 

It has been recognized that these two torsion angles are generally found in certain well-defined ranges [Ramachandran1968]. This is primarily a result of the protein forming well-defined local structure, i.e. particular favorable conformations resulting from the interactions between residues close in sequence space. These conformations can be characterized by their associated φ and ψ angles and each class is termed a type of "secondary structure". These secondary structure elements pack together to provide the overall 3D structure, or fold, of the protein. Native Folds 

The native conformation of a protein is often considered to be at the global energy minimum. Anfinsen's thermodynamic hypothesis states that the native folded protein exists in the global minimum free energy state [Anfinsen1973]. This is not necessarily the case. It is estimated that proteins fold too quickly to reach the global minima. A native fold may instead be the lowest energy state that is kinetically accessible [Levinthal1969]. In many cases, such as for proteins which may unfold and refold while maintaining activity, it is likely that a global minima is found. 

It is possible that local interactions dominate early in the folding process and therefore contribute greatly to the final outcome. On this basis, it is reasonable to assume that the use of secondary structure predictions as the foundation for models is reasonable. 

The folding of soluble proteins is generally agreed to be driven by the hydrophobic effect and the increase in entropy associated with burying hydrophobic residues into the protein interior. Within the hydrophobic protein core, van der Waals (VDW) interactions provide significant contributions to the tightly packed geometries found in folded protein structures. 

## Protein Modelling and Structure Prediction[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=3> "Edit section: Protein Modelling and Structure Prediction")]

As is clear from even a cursory glance at the PDB, proteins with similar sequences or function often adopt the same overall fold. It is interesting to observe that proteins with no sequence similarity and with different functions may also exhibit the same fold; it has been suggested that there are a limited number of fold "super-families" [Orengo1994]? to which proteins may belong. These two observations form the basis for the two most successful, and widely applied, protocols for modelling proteins: homology modelling and protein threading. 

In simple terms, when a homologous structure is known, homology modelling uses that as a template to build the model structure. When a homologous structure is not known, protein threading endeavors to find a protein fold which is compatible with the model sequence. 

When the above pair of methods is inappropriate, fully de novo approaches need to be used to construct models from sequence data alone. One approach is to consider secondary structure components, as rigid entities that may be packed together to provide the complete tertiary structure. Alternatively, first principles must be used to predict the 3D structure, termed ab initio protein folding. Ab initio protein folding is, without a doubt, an intractable problem for realistic target proteins. Ab initio protein folding methods attempt to locate the native structure either by mimicking the natural folding processes, or by some totally independent search procedure. 

The whole topic of protein modelling forms a fairly mature field of research, with numerous protein modelling techniques described in the literature. A number of "blind" protein modelling contests have been held to gauge the state of protein structure prediction techniques. The main conclusions drawn from the recent contests are that a good homology model can be as good as or even better than a experimental X-Ray structure. Threading can produce models that are equally as good, but may more easily contain significant errors. Ab initio modelling is much more expensive and produces less reliable, although very promising, results. 

## Modelling by Homology[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=4> "Edit section: Modelling by Homology")]

The basis for modelling proteins by homology, as depicted in Figure 1, is founded upon comparisons showing that the tertiary structures of evolutionary related proteins are better conserved than their primary structures [Bashford1987] [Vriend1991] [Holm1992a]. Differences between three-dimensional structures are known to increase with decreasing sequence identity and the corresponding accuracy of models built by homology also decreases [Chothia1987] [Sander1991]. 

[![Homologyschematic.png](/mediawiki/images/b/bd/Homologyschematic.png)](</mediawiki/index.php/File:Homologyschematic.png>)

Homology modelling is now a routine procedure, being fully automated by a number of software packages including MODELLER [Sali1993], Sybyl [Sybyl], INSIGHT II [InsightII], and even on a freely accessible world-wide web server, Swiss-Model [Peitsch1996]. A typical homology modelling protocol is based upon a number of distinct steps: 

  * Sequence alignment.
  * Evaluation of structurally conserved regions (SCRs).
  * Build core backbone using defined SCRs.
  * Build the variable regions.
  * Build sidechains.
  * Refine model.
  * Verify model and return to any step above, as appropriate.



## Sequence Alignment[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=5> "Edit section: Sequence Alignment")]

Multiple sequence alignment of the target sequence against known homologous sequences, or against complete sequence databases is performed to detect potential homologies. Numerous software packages are available for sequence alignments, Clustal [Thompson1994], CAMELEON [cameleon] and for scanning sequence databases, BLAST [Altenbach1997], FASTA [Pearson1988]. The alignment may be used to determine the proportion of residues which exactly match between a pair of protein sequences. If any structures are known for homologous proteins, then homology modelling may proceed. 

The errors in a model built on the basis of a structure with 90% sequence identity will be as low as the errors in crystallographically determined structures, providing that the initial sequence alignment is accurate [Chothia1987] [Blundell1987]. Known structures, if built from another known structure, indicate that in the case of 50% sequence identity the root mean squared (RMS) error in the modelled coordinates will be in the order of 1.5 &angstrom;, with considerably larger local errors at the more variable regions. These less accurate regions are usually located in loops at the protein surface. In regular secondary structure elements such as α-helices and β-strands, and in the hydrophobic core, model structures are usually more accurate. If the percentage sequence identity between the structure and the sequence to be modelled is between about 25% and 45% then the quality of the sequence alignment is the main factor limiting the quality of the overall model. If the sequence identity is only around 25%, the alignment is the main bottleneck for model building by homology, and large errors often occur. With less than 25% sequence identity any homology is difficult to detect. It has been shown that a similarity of 25% identity is possible from random matches [Feng1987] so any true sequence database hits will be masked by additional random hits. 

Besides providing a means to overlaying a target sequence onto a template structure, or as a means to locating homologous proteins with solved structures, multiple sequence alignments also highlight highly conserved residues. Experience has shown that highly conserved residues often play an important structural or functional role in proteins. This is valuable information when verifying the constructed model. 

## Structurally Conserved Regions[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=6> "Edit section: Structurally Conserved Regions")]

Regions of the template structure, or structures, which are rigid and well-defined need to be delineated. In realistic cases, the sequence alignment will indicate required deletions and insertions, which should not occur in these so called, structurally conserved regions, or SCRs. These are the portions of structure which can be incorporated directly into a model structure and typically consist of clearly defined secondary structure. In the case that more than one homologous structure is available, then SCRs are determined by aligning these structures based on the sequence alignments. It is usual to select the most representative structure, although many people advocate the generation of an average structure. In the case that only one homologous structure is known, the SCRs are usually defined as the regions which do not contain insertions or deletions in the sequence alignment. 

## Variable Regions[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=7> "Edit section: Variable Regions")]

Modelling the portions of structure which connect the SCRs? are more complicated. Variable regions are typically located at the protein surface and are often termed "loops". The insertion of loops is one of the main problematic issues for homology modelling. The template can not be used to model loops, so techniques other than modelling by homology have to utilised. 

Building loops is usually performed by one of two broad approaches. This first is to search databases for loops with end points that match with the fixed residues in the structure where the loop needs to be inserted [JonesTA1986]?. Many molecular graphics and modelling programs use this technique including, WHAT_IF [Vriend1990]?, QUANTA [Quanta98]?, and Insight II [InsightII]?. Alternatively, ab initio building can be performed by following one of several available procedures. These generally rely on the geometric matching of the loop's end points with the fixed residues to which they connect to reduce the search space. Steric clashes must be prevented. Producing loops with correct stereochemistry and energetics is an extremely difficult problem. Many articles have been published about this topic [Moult1986]? [Fine1986]? [Bruccoleri1987]? [Havel1991]? [Sippl1992]?. One particularly interesting technique is the so-called "Random tweak algorithm" [Shenkin1987]?. This calculates the necessary changes in the backbone φ and ψ dihedrals that will adjust a randomly generated loop conformation to fit the relevant distance constraints. Since it scales with the number of constraints rather than the chain length, it is very fast. One disadvantage is that the remainder of the protein is not considered, so it is usual to generate a set of possible loop conformations and then select one which fits well when inserted into the protein. 

## Side-chain Modelling[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=8> "Edit section: Side-chain Modelling")]

With the backbone of the model constructed, the next stage is to convert this into a full atomic model. Typically, the side-chain of each residue is built into in the model by a, so-called, rotamer search. See SideChainModelling. 

## Refinement[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=9> "Edit section: Refinement")]

Refinement, or optimisation, of the model is needed relax the structure, mainly to remove any high-energy contacts. Refinement is usually performed using a mixture of molecular mechanics minimisation and molecular dynamics. 

## Verification[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=10> "Edit section: Verification")]

It is also important to confirm that the structure could be a valid protein. This is discussed, in depth, below. This structure validation usually takes two forms, firstly checking local structure such as backbone dihedrals to confirm that they are consistent with known structures, and secondly global fold assessment to discriminate between native-like folds and misfolded structures which molecular mechanics forcefields are unable to do. This will give an indication of the confidence that may be placed on the model. 

## Modelling by Inverse Folding[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=11> "Edit section: Modelling by Inverse Folding")]

As mentioned above, it is often difficult to detect remote homologies. It is observed that proteins with no homology may still exhibit identical folds. It is believed that there is a limit to the number of stable folds despite the diversity in protein sequences [Bowie1991]. As a result of these two facts, there may be cases where an available structure is similar to a target model, but homology modelling is not applicable. 

A range of methods have been developed to check whether a particular sequence is compatible with a given fold, known as "inverse folding". By taking a large set of folds, ideally every known fold, and in each case threading a sequence through each fold in turn, it is possible to discover which fold is most likely to adopted by that sequence. 

The whole threading procedure is automated by several software packages, including THREADER [JonesDT1992] Sausage [Huber1999], and PROSPECT [Xu2000]. Sausage is also available via a web interface. 

## Fold Databases[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=12> "Edit section: Fold Databases")]

[![Threadingschematic.png](/mediawiki/images/0/05/Threadingschematic.png)](</mediawiki/index.php/File:Threadingschematic.png>)

The structures in the PDB have been analyzed to find all known folds, and searchable databases are freely accessible including SCOP [Murzin1995] and CATH [Orengo1997]. During the year 2000 approximately 7 000 new structures were discovered, however, only 8% of those contributed a previously unknown fold. A current problem is the under-representation of certain structural classes in the PDB. TM proteins are, of course, almost completely absent. This not only causes the obvious problem that there are no TM-protein folds to match against, but more importantly, the assessment of sequence to fold compatibility is always parameterized for soluble proteins. The result is that even when the correct TM-fold is present in the database, it is not selected as compatible. Fold Compatibility Assessment 

An early method applied the structural profile method of Eisenberg's group which was originally designed to verify the quality of model structures [Bowie1991] [Luthy1992] [Eisenberg1992]. The observation that so-called 3D profiles could distinguish between folded and misfolded structures led to the development of a method which assessed a wide range of possible folds for a given sequence. These possible folds are generated by superimposing the target sequence onto fold templates. 

A large number of assessment functions have been published [Sippl1992] [JonesDT1992] [Godzik1993] [JonesDJ1996] [Miyazawa1996] [Moult1997] [Xu2000]. These all need to be highly efficient functions since many thousands of folds will be checked and, depending on the exact protocol, the sequence must be threaded through single residue increments in each case. 

## Side-chain Modelling, Refinement and Verification[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=13> "Edit section: Side-chain Modelling, Refinement and Verification")]

Once the backbone model is selected, the remainder of the threading process matches the homology modelling protocol. 

## Validation and Verification[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=14> "Edit section: Validation and Verification")]

(incomplete section) 

## Available Software[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=15> "Edit section: Available Software")]

Much of the software required to perform comparative modelling as described in this document is readily available within the McCammon lab: 

  * ClustalX - Multiple sequence alignment.
  * Sybyl - Composer Module, MatchMaker Module
  * Insight II - Homology Module, Modeler Module
  * MOE
  * WHAT_IF, WHAT_CHECK - (Ask Jens)
  * PROCHECK - Protein structure validation.
  * Swiss-Model - An Automated Comparative Protein Modelling Server for homology modelling.
  * Sausage - The Sausage Machine Server for threading.
  * Thræd - Stewart's threading software.
  * (And many, many more)



RPMs for installation of some of the above software on the McCammon lab's x86/Alpha Linux machines are available from <http://mccammon.ucsd.edu/~adcock/restricted/softwarearchive.html>. 

## Bibliography and Suggested Reading[edit](</mediawiki/index.php?title=Homology_Modeling&action=edit&section=16> "Edit section: Bibliography and Suggested Reading")]

(Not complete) 

  * Altenbach, C. and Madden, T. L and Schaffer, A. A. and Zhang, J. and Zhang, Z. and Miller, W. and Lipman, D. J. "Gapped BLAST and PSI-BLAST: a new generation of protein database search programs", Nucleic Acids Research, 25:3389-3402 (1997)
  * Anfinsen, C. B. "Principles that govern the folding of protein chains", Science, 181:223-230 (1973)
  * Bashford, D., Chothia, C., and Lesk, A. M. "Determinants of a protein fold: Unique features of the globin amino acid sequences", Journal of Molecular *Biology, 196:199-216 (1987)
  * Bowie, J. A. and Luthy, R. and Eisenberg, D. "A Method to Identify Protein Sequences That Fold into a Known Three-Dimensional Structure", Science, *:253:164-170 (1991)
  * CAMELEON appears to be a victim of the formation of Accelrys from Oxford Molecular. The original CAMELEON reference was: W. R. Taylor, Methods Enzymol., *:183:456-474 (1990)
  * Chothia, C. and Lesk, A. M. "The relation between the divergence of sequence and structure in proteins", EMBOJ, 5:823-826 (1987)
  * Eisenberg, D. and Bowie, J. U. and Luthy, R. and Choe, S. "Three-dimensional Profiles for Analysing Protein Sequence-Structure Relationships", Faraday * *:Discussions, 93:25-34 (1992)
  * Feng, D. F. and Doolittle, R. F. "Progressive sequence alignment as a prerequisite to correct phylogenetic trees", Journal of Molecular Evolution, *:25:351-360 (1987)
  * Huber, T. and Russel, A. J. and Ayers, D. and Torda A. E. "Sausage: protein threading with flexible force fields", Bioinformatics, 15:1064-1065 (1999)
  * Insight II Accelrys Inc., 9685 Scranton Road, San Diego, CA 92121-3752, USA
  * Jones, D. T. and Taylor, W. R. and Thornton, J. "A New Approach to Protein Fold Recognition", Nature, 358:86-89 (1992)
  * Jones, D. J. and Thornton, J. M. "Potential energy functions for threading", Nature, 358:86-89 (1992)
  * Levinthal, C. in "Mossbaur Spectroscopy in Biological Systems", University of Illinois Press, 22-24 (1969)
  * Luthy, R. and Bowie, J. U. and Eisenberg, D. "Assessment of protein models with three-dimensional profiles", Nature, 356:83-85 (1992)
  * Moult, J. "Comparison of database potentials and molecular mechanics force fields", Current Opinions in Structural Biology, 7:194-199 (1997)
  * Murzin, A. G. and Brenner, S. E. and Hubbard, T. and Chothia, C. "SCOP: A structural classification of proteins database for the investigation of *:sequences and structures", Journal of Molecular Biology, 247:536-540 (1995)
  * Miyazawa, S. and Jernigan, R. L. "Residue-residue potentials with a favorable contact pair term and an unfavorable high packing density term, for *:simulation and threading.", Journal of Molecular Biology, 256:623-644 (1996)
  * Orengo, C. A. and Jones, D. T. and Thornton, J. M. "Protein Superfamilies and Superfolds", Nature 372:631-634 (1994)
  * Orengo, C. A. and Michie, A. D. and Jones, S. and Jones, D. T. and Swindells, M. B. and Thornton, J. M. "CATH - a heirachical classification of protein *:domain structures", Structure, 5:1093-1108 (1997)
  * Pearson, W. R. and Lipman, D. J "Improved Tools for Biological Sequence Analysis", PNAS, 85:2444-2448 (1988)
  * Quanta Accelrys Inc., 9685 Scranton Road, San Diego, CA 92121-3752, USA
  * Sybyl Tripos, Inc. 1699 South Hanley Road St. Louis, MO 63144
  * Shenkin PS, Yarmush DL, Fine RM, Wang H, Levinthal C. "Predicting antibody hypervariable loop conformation I. Ensembles of random conformations for *:ringlike structures", Biopolymers 26:2053-2085 (1987)
  * Sander C. and Schneider R. "Database of homology-derived protein structures", Proteins: Structure, Function and Genetics, 9:56-68 (1991)
  * Sali, A. and Blundell, T. L. "Comparative Protein Modelling by Satisfaction of Spatial Restraints", Journal of Molecular Biology, 234:779-815 (1993)
  * Ramachandran, G. N. and Ramakrishnan, C. and Sasisekharan, V. "Conformation of poypeptides and proteins", Adv. Protein Chem., 28:283-437 (1968)
  * Xu, Y. and Xu, D. "Protein Threading using PROSPECT: Design and Evaluation", Proteins:Structure, Function and Genetics, 40:343-354 (2000)
