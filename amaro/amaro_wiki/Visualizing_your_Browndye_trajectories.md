# Visualizing your Browndye trajectories

# Visualizing your Browndye trajectories[edit](</mediawiki/index.php?title=Visualizing_your_Browndye_trajectories&action=edit&section=1> "Edit section: Visualizing your Browndye trajectories")]

You have used Browndye to get kinetic data, but what if you want to visualize your trajectories? Fear not, it is possible. Tutorial by Christian Seitz~ 

## The necessary links:[edit](</mediawiki/index.php?title=Visualizing_your_Browndye_trajectories&action=edit&section=2> "Edit section: The necessary links:")]

  * [Browndye documentation](<https://browndye.ucsd.edu/browndye/doc/manual.html>)
  * [Browndye visualization script (process_trajectories.py)](<https://wiki.amaro.ucsd.edu/mediawiki/index.php/ScriptsMain>)



## The necessary files:[edit](</mediawiki/index.php?title=Visualizing_your_Browndye_trajectories&action=edit&section=3> "Edit section: The necessary files:")]

  * protein dx
  * protein xml
  * input xml (input for Browndye runs)
  * ligand dx
  * ligand xml
  * rxns xml (file containing the reaction pairs and their distances)



## Procedure[edit](</mediawiki/index.php?title=Visualizing_your_Browndye_trajectories&action=edit&section=4> "Edit section: Procedure")]

### Prepare Browndye to run[edit](</mediawiki/index.php?title=Visualizing_your_Browndye_trajectories&action=edit&section=5> "Edit section: Prepare Browndye to run")]

According to the Browndye documentation, you need to tell Browndye to create the nonstandard files you need to visualize your trajectories. Assuming you are using nam_simulation and not weighted ensemble, you need to add the flags 

  * <n-trajectories-per-output> number </n-trajectories-per-output> (This tells you how many trajectories in between an update of the output file; I set this to 1.)


  * <n-steps-per-output> number </n-steps-per-output> (change the number to whatever number you want, this tells you how many time steps per update of the output file; I set this to 1.)


  * <trajectory-file> trajectory </trajectory-file> (this is the prefix affixed to all your output trajectory files needed for visualization, so you can change "trajectory" to any other word you wish)



Run the command 

bd_top input.xml 

where input.xml is whatever your input file is named. This will give you the files needed for simulation. Then run your simulation with 

nam_simulation 2hty-oseltamivir-simulation.xml 

where the .xml file is the *-simulation.xml file created from the bd_top command. This runs your simulation, and can take time depending on the other parameters you used in your simulation. Note: This can create huge amounts of data (for my project, I created ~60 TB across all my systems). After the simulation finishes, create some directory for temporary files (I named mine temp). Then you can create visualization files with 

python2 process_trajectories.py -i input.xml -n 0 -o output.pqr -x all -w temp -s 10 -c 

I downloaded the script by creating a new script called process_trajectories.py, going into edit mode for the script on the wiki, copying everything and removing the 
    
    
     and 

. Here is what the arguments mean: 

-i #this is your input file 

-n #this is the trajectory number in the file you want to start with - it follows python indexing so -n 10:20:2 means use trajectories 10 through 20 with a stride of 2 

-o #this is the name of your output receptor, you can all it anything you want 

-x #this is whatever name you gave to signify a reaction outcome - -x all automatically selects all reaction outcomes 

-w #directory for temporary files you will not use, call it anything you want 

-s #stride of your trajectories 

-c #write a structure receptor, does not need an argument 

You can change the -o output.pqr to be any output name you like. For this page, I used output.pqr which gives and output of output.pqr0.pdb. The one other thing to change in this is the -x flag. To see all trajectories (even ones where the ligand didn't find the binding site) leave this at "all". To only see trajectories resulting in a successful association, you will need to change "all" to something else. In my rxns file, I denoted "association" to mean an association reaction. 

<name> association </name>

However, you can name this anything you like, which comes in handy if you have multiple different association events you are looking at in the rxns file. To see that association (or other) event happening in your visualization, simply change "all" to whatever you named that event in the rxns file. Most simulations you run will have very few successful association events, so if you want to see what your ligand is doing when it is not successfully associating, use "all" and you will very likely see only nonbinding trajectories. 

### FAQ[edit](</mediawiki/index.php?title=Visualizing_your_Browndye_trajectories&action=edit&section=6> "Edit section: FAQ")]

**Q** : How do I change the number of trajectory output files I am getting from Browndye? What if I want there to be one trajectory output file for each trajectory instead of a concatenation of trajectory outputs? 

**A** : Each thread you use runs different Browndye trajectories. Thus, each thread will create a different trajectory output file and concatenate each trajectory it runs into that file. So if you are using 40 threads, you will get 40 trajectory output files. If you are running 80 trajectories, each output file will likely be a concatenation of two trajectories. If you are running 400 trajectories, each output file will likely be the concatenation of 20 trajectories. 

  
**Q** : I am getting trajectory output files, but the file sizes are too large. I want to keep the full number of trajectories, but I want to decrease the number of frames in them to save space. How do I do that? 

**A** : If you have a large number of trajectories, you can change the n-steps-per-output to a large number. The tradeoff is that your trajectory files will have few frames to them. If you have lots of storage space, you can keep this at a smaller number. For example, if you are running a number of trajectories and have n-steps = 1000 and n-steps-per-output = 500, then each trajectory will have two frames. Alternatively, you can stride your trajectory files, explained below. 

  
**Q** : I don't want to use all of my trajectories, but I don't want to decrease the number of frames in my trajectories. I want to use a smaller number of trajectories but each with the full amount of frames to save space. How do I do that? 

**A** : You can stride your trajectories to use a smaller number of them. Use any n number above 1 to pick the nth number of trajectories to use for analysis. 

  
**Q** : How can I see more options for the process_trajectories.py script? 

**A** : Run python2 process_trajectories.py -h to see a full list of options. 

  
**Q** : I only want to use a certain subsection of my trajectories, but within that subsection, I want to use all the trajectories and all the frames. How do I do that? 

**A** : When you run process_trajectories.py, change the -n flag from 0 (as shown above) to the subsection you want, with striding if you want. The syntax uses python indexing. For example, -n 50 takes trajectory 50 and all after it. -n 1:6 takes trajectories 1-6. -n 10:20:2 takes trajectories 10-20, with a stride of 2 (so it takes trajectory 10, 12, 14, 16, 18, 20). 

  
**Q** : I need more detail from my trajectories. How can I get more frames in my trajectories? 

**A** : Decrease the n-steps-per-output number. This will increase the file size but you will get more frames in your trajectories. 

  
**Q** : Help! My files are so large that VMD won't open them! 

**A** : You should either stride your files (use fewer trajectories) or reduce the number of frames. Both can be done by rerunning process_trajectories.py with different arguments. 

### Common error[edit](</mediawiki/index.php?title=Visualizing_your_Browndye_trajectories&action=edit&section=7> "Edit section: Common error")]

If you have changed "all" to "association" in the command above, and get the error 

Traceback (most recent call last): 
    
    
     File "process_trajectories.py", line 356, in <module>
       cmd = "xyz_trajectory -mol0 %s -mol1 %s -trajf %s -pqr > %s" % (inputdict['mol0'], emptyname, xmltrajfilename, pqrfile)
    

NameError: name 'xmltrajfilename' is not defined 

This means that in your initial Browndye simulation, you did not have any successful association reactions. Either use all your trajectories in visualizing your output, or rerun your Browndye simulation with relaxed parameters to get a successful association. 

### Visualize the trajectories in VMD[edit](</mediawiki/index.php?title=Visualizing_your_Browndye_trajectories&action=edit&section=8> "Edit section: Visualize the trajectories in VMD")]

The process_trajectories.py will give you an output.pqr0.pdb and an output.pqrreceptor.pqr. In VMD, open the output.pqrreceptor.pqr. As a new molecule, open your ligand pqr. The load the output.pqr0.pdb into your ligand pqr, and watch the ligand move while the protein stays static. 

### Occupied volume of the trajectories[edit](</mediawiki/index.php?title=Visualizing_your_Browndye_trajectories&action=edit&section=9> "Edit section: Occupied volume of the trajectories")]

You can use the VolMap extension in VMD to see what sort of volume your ligand is occupying during its trajectories. Depending on how you created your trajectory outputs, this will either show you what volume is occupied on the path to the binding site, or what volume is occupied during unsuccessful trajectories and where the ligand often heads away from the protein. 

In VMD, open your output.pqr0.pqr, output.pqrreceptor.pqr and ligand pqr as above. Then do VMD -> Extensions -> Analysis -> VolMap. In "selection", do 

resname LIG 

where LIG is whatever is the resname of your ligand pqr. You can see this if you vi into your ligand pqr. Then create the map. Note: this shows only where your ligand is going, not how often it is going there. To see relative occupancies, you should also use Volume Slice, described below. 

### Relative occupancies of your ligand[edit](</mediawiki/index.php?title=Visualizing_your_Browndye_trajectories&action=edit&section=10> "Edit section: Relative occupancies of your ligand")]

You can use VMD's Volume Slice to see relative occupancies of your ligand. After opening up your receptor, ligand and trajectories in VMD as described previously, create the occupied volume as described above. Then go to VMD -> Graphics -> Representations. With your ligand pqr as the "Selected Molecule" in the graphical representation window, change Drawing Method -> Volume Slice. The "Slice Axis" is on the x-axis by default. Create more identical representations for the y-axis and the z-axis. Next, you need to adjust Graphical Representations -> Slice Offset and adjust it so that it is over your ligand, or protein, or whatever you want to be analyzing. Do this for the y-axis representation and the z-axis representation too. You should get different colors based on the occupancies of your ligand (red=no occupancy, blue=occupancy). You can also change the color scale under Graphical Representations -> Trajectory -> Color Scale Data Range. Adjust as necessary to be able to see areas of occupancy and no occupancy, but you will likely need to decrease the color range. For example, for my system I needed to change the range from 0 - 6.22 to be from 0 - 0.5 or 0 - 0.05 to better display contrasts.
