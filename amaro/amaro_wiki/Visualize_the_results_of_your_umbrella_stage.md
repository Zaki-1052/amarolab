# Visualize the results of your umbrella stage

Once you've finished your umbrella stage, it can be helpful to visualize the results to make sure they worked OK. 

Let's assume that you've run a calculation on milestone 14 of a system. First, 'cd' into that milestone's directory: 
    
    
    cd anchor_14_14_0_53.2_30.8_34.3/md/
    

Once inside, open up VMD, loading the holo prmtop and the NVT umbrella dcd. 
    
    
    vmd building/holo.parm7 -dcd umbrella/umbrella2.dcd
    

We are assuming that umbrella1.dcd was a short NPT simulation, and we only need to open umbrella2.dcd, the longer NVT stage. 

[![Seekr vis umbrella1.png](/mediawiki/images/c/c8/Seekr_vis_umbrella1.png)](</mediawiki/index.php/File:Seekr_vis_umbrella1.png>)

It can be helpful to visualize the protein using NewCartoon and the ligand as Licorice. In the VMD "Graphical Representations" window. Change "Drawing Method" from "Lines" to "NewCartoon". Then click "Create Rep", change "Selected Atoms" to select your ligand (in my case, to "resname GDM"), then change "Drawing Method" to "Licorice". 

[![Seekr vis umbrella2.png](/mediawiki/images/d/dd/Seekr_vis_umbrella2.png)](</mediawiki/index.php/File:Seekr_vis_umbrella2.png>)

Now, in the "VMD Main" window menu, select "Extensions->TkConsole". 

Within the "VMD TkConsole" window, create a selection named "lig" using your own ligand indices: 
    
    
    set lig [atomselect top "index 3352 3353 3354 3355 3356 3357 3358 3359 3360 3361 3362 3363 3364 3365 3366 3367 3368 3369 3370 3371 3372 3373 3374 3375 3376 3377 3378 3379 3380 3381 3382 3383 3384 3385 3386 3387 3388 3389 3390 3391"]
    

You will need to change the "index" numbers to the receptor indeces you used for your own system. You can find these in your SEEKR umbrella script. 

[![Seekr vis umbrella3.png](/mediawiki/images/f/f9/Seekr_vis_umbrella3.png)](</mediawiki/index.php/File:Seekr_vis_umbrella3.png>)

Next, align your protein by the active site itself. In the "VMD Main" window menu, select "Extensions->Analysis->RMSD Trajectory Tool". A new window will open 

[![Seekr vis umbrella4.png](/mediawiki/images/4/48/Seekr_vis_umbrella4.png)](</mediawiki/index.php/File:Seekr_vis_umbrella4.png>)

In the white box in that window, enter the selection of the receptor active site: "index 659 673 695 707 748 1333 1366 1392 1455 1519 1533 1602 1935 1942 1958 1965 2650". 

Obviously, you will need to change these numbers to your own system as well. 

Click "Align". You should see that your protein has aligned to the first frame. 

No go back to the "VMD TkConsole" window and type the following command: 
    
    
    for {set i 0} {$i < [molinfo top get numframes]} {incr i} {$lig frame $i; draw point [measure center $lig weight [$lig get mass]]}
    

Now you should see that a bunch of points are drawn along the milestone. If you want a different color, say green points, then run the following command before you run the "for" command: 
    
    
    draw color Green
    

Obviously, you can change Green to a different color. 

[![Seekr vis umbrella5.png](/mediawiki/images/d/d6/Seekr_vis_umbrella5.png)](</mediawiki/index.php/File:Seekr_vis_umbrella5.png>)

As you can see from the image above, the ligand center of mass appears to be sampling the surface of a sphere, and appears to have spread out over almost the entire span of the active site.
