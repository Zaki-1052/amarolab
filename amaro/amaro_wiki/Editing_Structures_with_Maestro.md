# Editing Structures with Maestro

## Adding missing residues[edit](</mediawiki/index.php?title=Editing_Structures_with_Maestro&action=edit&section=1> "Edit section: Adding missing residues")]

### Capping your protein and locating the C-terminus[edit](</mediawiki/index.php?title=Editing_Structures_with_Maestro&action=edit&section=2> "Edit section: Capping your protein and locating the C-terminus")]

In your terminal, write: 
    
    
    > maestro 

Hit the Protein Prep Wiz option and import your structure from the PDB database. 

After you import your protein, use the Preprocess options. 

Click whichever options you prefer, but **not** _fill in missing loops using Prime_. _Definitely_ click _Cap termini_ because this will make adding fragments much easier in the next step 

Since we chose the Cap termini option, we now have NMA (N-terminal cap) at the very end of our protein. To add missing fragments, you have to find the end of your protein, so locate that in whatever way is best for you. 

I like to use the "Show Ribbons for All Residues" option. This turns the protein into a ribbon structure that uses the color of the rainbow to mark the relative location of the sequences. Red is the very beginning of the protein; orange follows; then yellow, etc. You can follow the rainbow pattern to the end of the rainbow protein and easily find your C terminus or nicks in the protein. 

Once you find the C terminal end, use your mouse to locate the bond between the last carbonyl carbon (C=O) and the NMA cap nitrogen. If you have located the atoms, at the bottom of your screen, you will see: 

_**For Carbonyl Carbon**_ \- (Atom number) : (Chain ID) : (Residue Name): **(C) C**

_**For NMAcap Nitrogen**_ \- (Atom number) : (Chain ID) : (NMA)  : **(N) N**

### Building your fragment[edit](</mediawiki/index.php?title=Editing_Structures_with_Maestro&action=edit&section=3> "Edit section: Building your fragment")]

Now, to build the missing amino acid residues, you must again use the **Build** option. Choose **Fragments:** **Amino acids**. 

Click the _Grow_ option and under **Define grow bond** , click the _Pick_ option and select _Bonds_. 

Choose the new terminal Carbonyl carbon-NMAcap nitrogen bond (that we just created). 

  
Simply choose the amino acid sequence that you would like to to add from the available options.
