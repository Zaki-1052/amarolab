# Jacob Durrant Project Ideas

Please let me know if any of these catch your attention. I'm happy to collaborate. (Also, please veto anything you don't like, Rommie.) Sorry for the stream-of-consciousy descriptions. 

## Potential Future Projects[edit](</mediawiki/index.php?title=Jacob_Durrant_Project_Ideas&action=edit&section=1> "Edit section: Potential Future Projects")]

  1. Simple script that filters a Vina virtual screen and extracts only poses with specific interactions. No exactly restrained docking, but same idea.
  2. I've got a pretty massive database of protein-ligand interactions with associated experimentally measured binding affinities. I'd like to use an artificial-intelligence technique called a “decision tree” to extract useful general rules from this data to guide drug optimization. Fortunately, I've found a nice python module that includes decision trees (scikit-learn).  
  
Preliminary analysis suggests that most of the main rules are going to be obvious to any medicinal chemist (i.e. lots of hydrophobic contacts are good for affinity). But there might be some less intuitive rules that could be more interesting. Overall a fairly high-risk project, but the database is already created, so I think the hard part is finished.
  3. As part of a larger paper describing a new chemical library (from the Distributed Drug Discovery/D3 initiative), I'd like to create an online Opal service that can compare two large compounds libraries (SMILES strings) and find molecules that are common to both. It will involve using open babel, the apbs batch queue system, Opal, and some fancy scripting, but shouldn't be too tricky. (Making Opal apps isn't as tricky as you might think.)
  4. A few years ago I worked on a program called CrystalDock that uses a database derived from PDB crystal structures to identify possible pocket-binding fragments. Aaron Freidman, ex-McCammonite who is now working with Craig Venter to try to make us all immortal, was working on version 2.0, with substantial improvements. But apparently he thinks immortality is more important and wants to dedicate more time to his new job, so he asked me to see if anyone would like to pick up where he left off.  
  
One of the major barriers to widespread adoption is that this program is several gigabytes. It really should be implemented as an online server to encourage broader use. 
  5. I've got some pretty long simulations of hemagglutinin (including the stalk) embedded in a lipid bilayer. I extracted conformations from these simulations and incorporated them into my whole-virion model, but there must be more we can get out of them than that. Electrostatics or dynamics analyses or something. I don't know much about HA, so I could certainly use the help.
  6. Machine-learning technique that can identify a correctly docked pose from among incorrectly docked poses. A big part of why my NNScore functions don't perform as well on docked poses as they do on crystal structures is because the docked poses are wrong. I should focus on improving the prediction of docked poses too.



## Ongoing Projects[edit](</mediawiki/index.php?title=Jacob_Durrant_Project_Ideas&action=edit&section=2> "Edit section: Ongoing Projects")]

  1. (Tavina) I recently performed three virtual screens on the estrogen receptor, two using NNScore and one using Schrodinger Glide. The top compounds were tested by an experimentalist, who identified a 120 nM inhibitor. I thought that was pretty cool, but apparently low nanomolar ER inhibitors are a dime a dozen.   
  
What was significant, though, is that NNScore performed about as well as Glide. I want to encourage wider adoption of NNScore, so I was thinking about a paper emphasizing the comparable performance, entitled something like “NNScore is Awesome so Use it Already.”  
  
The screens have already been done, but I could use some help with the data analysis, background research for the Intro, and writing. Maybe this would be good for an undergrad?
  2. (Rommie giving thought to possible collaborator) PyMolecule 2.0 needs to be finalized and written up. I want to make it compatible with other similar tools like MolKit and MDAnalysis. Basically, I'd like to have PyMolecule functions that can read and write to the classes that store molecular data in those other modules. Also, I'd like to benchmark PyMolecule 2.0 vs. 1.0, and could use some help writing the paper.
  3. (Chris is working on coarse-grained solutions. Will likely be collaborating with Klaus' group too) I'm getting pretty sick of lipid bilayers with holes in them. Simulations of bilayers generated with my LipidWrapper program sometimes rip apart a little. It would be great if there were a utility that could identify the holes and fill them with lipids from the other parts of the bilayer. I think other bilayer modeling programs have the same problem, so it could have more general applicability. It would be great if it were PyMolecule based. Let me know if you're willing to take on this unholy holey mess. (One perk of the project is that you get to make jokes like this all the time. Speaking of unholy, wouldn't this be a good project for you, Lane? Ha. Ha. )



## Completed Projects From This List[edit](</mediawiki/index.php?title=Jacob_Durrant_Project_Ideas&action=edit&section=3> "Edit section: Completed Projects From This List")]

  1. (Sophie knows about this... need to ask her.) Not a paper, but it would be really great if someone in the lab, perhaps an undergraduate or a summer student, became an expert in Blender and taught the rest of us. Not only could we make incredible pictures for our papers, but Blender has a lot of other scientific applications too.



## Abandoned Ideas (No Longer Interested)[edit](</mediawiki/index.php?title=Jacob_Durrant_Project_Ideas&action=edit&section=4> "Edit section: Abandoned Ideas \(No Longer Interested\)")]

  1. (Decided jMol is sufficiently awesome) It recently occurred to me that by running VMD server side, exporting the VMD scene as a VRML or other 3D model, and using ThreeJS client side, it would be pretty easy to make a dumbed-down web version of VMD. Being able to visualize whole proteins in your browser by leveraging everything VMD can do would be pretty awesome. Those visualizations could be incorporated into other chemistry-based web apps, for example.   
  
Not sure it's worth it, though, because there's a similar program called JsMol. On the other hand, in my experience JsMol isn't so good at surface representations, and, because it generates the 3D images in the user's browser (instead of server side), it can be pretty slow. May or may not be worth pursuing.
