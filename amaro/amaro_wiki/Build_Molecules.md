# Build Molecules

## Preface[edit](</mediawiki/index.php?title=Build_Molecules&action=edit&section=1> "Edit section: Preface")]

The purpose of this tutorial is to explain, in simple terms, the important processes and considerations required for construction of small molecule structures. "Small molecule" would typically mean a known drug-like compound. Finding or generating a 3D model is a pre-requisite for numerous common tasks, including docking studies and simulation. Some of the software and example scripts described within this tutorial are available from this restricted access directory for use in the Mccammon Lab. Consider what you need from this structure 

It is relatively straightforward to generate a 3D structure of a drug-like molecule. However, it is also straightforward to not think about your problem and thus generate something that is totally inappropriate. You need to be able to answer these questions. 

  * Do you need a single structure or a set of all possible conformations?
  * Do you just need a geometrically valid structure? Or, the global energy minimum structure? In vacua? In ionic solution?
  * Chirality?
  * Does you molecule need to be neutral? Or charged????
  * Do you need to assign atomic partial charges to your molecule?
  * Do you need to assign the correct atom types with respect to some forcefield?



## Repositories[edit](</mediawiki/index.php?title=Build_Molecules&action=edit&section=2> "Edit section: Repositories")]

There are two significant online resources which may offer a suitable structure for a given molecule. 

  * The Brookhaven Protein Databank, with a local mirror.
  * The Cambridge Crystallographic Databank.



## Graphical molecule builders[edit](</mediawiki/index.php?title=Build_Molecules&action=edit&section=3> "Edit section: Graphical molecule builders")]

Numerous software packages have facilities for the user to "sketch" a molecule which is used to create a clean 3D structure. As with all CompChem? software, the robustness (Computationally and scientifically) of these packages is highly variable. The general advice would be to use any of these packages that happen to be convenient, but always export and check the resulting structures before using them. 

## Coarse structure generation or sampling[edit](</mediawiki/index.php?title=Build_Molecules&action=edit&section=4> "Edit section: Coarse structure generation or sampling")]

There are at least three very easy to use packages for producing very reasonable structures. I would advise that one of these should be used in preference to any home-brewed approach. Just use which ever is available. 

  * Concord - ideal for generating a single, good, structure. Very fast. Included as part of Sybyl.
  * Corina - comparable to Concord, but not so fast. Reportedly more robust. Unfortunately this is no longer sold seperately.
  * Omega - rapidly produces comprehensive sets of conformations.



The structures produced by these software packages are perfectly suited for docking studies or as starting structures for simulation or further optimisation. These structures (without further optimistation) will not be suitable for evaluating physical or chemical properties. You should read the appropriate user manual if you decide to use any of the above packages. An example using Concord may be found here. 

## Semi-empirical optimisation[edit](</mediawiki/index.php?title=Build_Molecules&action=edit&section=5> "Edit section: Semi-empirical optimisation")]

Semi-empicial chemistry codes, for example MOPAC or VAMP, are able to optimise structures to close to ab initio quality in a fraction of the time. This can be very useful when applied correctly, but there are a few important things to consider. The choice of theory and parameters are critical. If you aren't sure about what to do, then ask someone who is. In the best case you'll just waste your time. In the worst case you'll produce structures that are worse than those produced by the above "coarse" approaches. As an example, consider PM3. PM3 may be used to rapidly and robustly optimise poor structures with very good results. Unfortunately, certain structural features will be wrong. Trigonal-planar nitrogen groups will be predicted as pyrimidal. As another example consider AM1. Structures will not be completely wrong, but predicted bond lengths will be no better than those derived from simple MM forcefields (as is done in the "coarse" approaches). Parameters for simulation 

For certain tasks, just having the structure is insufficient. Often "atomic charges" are required, but it should be noted that these often depend upon the molecular conformation. For molecular dynamics, forcefield parameters will also be required, and if you have just generated the structure it is likely that no parameters are directly available. Obviously your particular requirements will dictate the procedure required. 

Atomic partial charges may be estimated by semi-empicial and ab initio chemistry codes, however these may be overkill for your needs, and are generally highly conformation dependent. An alternative is to use one of the published rapid estimation algorithms. My personal choice is the "Partial Equilibration of Orbital Electronegativity" of Gasteiger and Marsili. This is a simple, and therefore fast, algorithm which produces good, but not perfect, results for organic molecules. I can offer code (or a really unreliable standalone program) upon request, but most modelling packages can assign charges using this approach too. 

If using CHARMM parameters, then the Quanta parameter selection tool may be useful. 

  


## File Formats[edit](</mediawiki/index.php?title=Build_Molecules&action=edit&section=6> "Edit section: File Formats")]

Recipe: E for docking 

It is trivial to write the structure of E using the linear SMILES notation. 

Recipe: LSD for simulation 

Bibliography and Links
