# Glide

**Glide** is a program in Maestro that can be used to do ligand [docking](</mediawiki/index.php/Docking_Programs> "Docking Programs"). Before you begin docking though, you must prepare your receptor, prepare your ligand(s), and make a grid. 

## Protein preparation[edit](</mediawiki/index.php?title=Glide&action=edit&section=1> "Edit section: Protein preparation")]

Open the Protein Preparation Wizard by searching for it under Tasks. Under Preprocess the Workspace structure, enter your desired pH for Generate het states using Epik. Also select the checkboxes for filling in missing side chains and loops if needed. If your structure contains any water molecules, go to the Refine tab and adjust the pH as needed. Then hit run. 

## Ligand preparation[edit](</mediawiki/index.php?title=Glide&action=edit&section=2> "Edit section: Ligand preparation")]

You must prepare your ligands before docking them. Open LigPrep from the Tasks search bar. Choose the ligands that you wish to prepare, either from file or by selecting them from the workspace. A commonly used ligand library is the UCSD CDDI [[1]](<http://cddi.ucsd.edu>) library. Choose your desired pH from which to generate possible states of the ligand. 

For the number of stereoisomers, the maximum can be left at the default of 32 per ligand. 

## Receptor grid generation[edit](</mediawiki/index.php?title=Glide&action=edit&section=3> "Edit section: Receptor grid generation")]

Open the Receptor Grid Generation window, which will open to the Receptor tab. If your structure contains a ligand, you will first need to select the ligand so that Glide will know what to exclude from the receptor during docking. 

Next, select the Site tab. A purple box will appear on top of your structure. The box defines the limits of where the ligand can be docked. Define the center of the box using one of the three options. 

You may also need to adjust the size of the box by changing the maximum size of a docked ligand. Lastly, under Advanced Settings..., you can create an inner box (displayed in green), in which the center of your docked ligands must remain. This may be useful if, after having docked a set of ligands, you notice that the ligands are not binding to the correct site. 

## Ligand docking[edit](</mediawiki/index.php?title=Glide&action=edit&section=4> "Edit section: Ligand docking")]

Now you're ready to actually dock some ligands (all that prep is going to finally pay off!). Open the Ligand Docking window. First select the receptor grid that you previously generated. Also select the ligands you would like to dock. 

There are several parameters you can play around with. Under Settings, the default is standard precision, which can be changed to extra precision as needed. Ligand sampling can be flexible or rigid. Finally, under the Output tab, the number of poses produced can be increased to increase the amount of ligand sampling reported.
