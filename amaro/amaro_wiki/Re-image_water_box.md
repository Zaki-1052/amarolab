# Re-image water box

One problem you may encounter with your wet structures is that the water box is in an incovenient or ugly location, and you want the waterbox centered over a molecule or particular part of your protein. 

[![Waterbox problem.png](/mediawiki/images/e/e8/Waterbox_problem.png)](</mediawiki/index.php/File:Waterbox_problem.png>)

Notice that the protein is sticking out of the box. If you try to run a simulation now, the box will wrap, and the simulation will blow up. We need a way to center the box on a selection of atoms. To do this, you will need to install AmberTools: 

[AmberTools](</mediawiki/index.php/AmberTools> "AmberTools")

We will use the 'cpptraj' program. 

Let's say that we have a file 'barnase_wet.pdb' that we need imaged on atom indices 833 and 549. The following script will perform that task: 
    
    
    parm barnase_wet.parm7
    box x 68.4319487803 y 68.4319487803 z 68.4319487803 alpha 109.4712190 beta 109.4712190 gamma 109.4712190
    trajin barnase_wet.pdb
    autoimage @833,549
    trajout barnase_wet_reimaged.pdb
    go
    quit
    

Name this script 're_image.cpptraj'. 

Notice the 'autoimage' command takes an argument for where to center the water box. No arguments for 'autoimage' will cause it to center on the first protein in the pdb file. See the 'cpptraj' manual for more details of how to center the water box on different atom selections based on, for instance, ranges of indices, residues, etc. 

Run the cpptraj program on this script: 
    
    
    cpptraj < re_image.cpptraj
    

Now the image should be better centered. 

[![Waterbox fixed.png](/mediawiki/images/0/05/Waterbox_fixed.png)](</mediawiki/index.php/File:Waterbox_fixed.png>)
