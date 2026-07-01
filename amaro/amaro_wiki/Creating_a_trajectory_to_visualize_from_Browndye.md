# Creating a trajectory to visualize from Browndye

# Visualizing your Browndye trajectories[edit](</mediawiki/index.php?title=Creating_a_trajectory_to_visualize_from_Browndye&action=edit&section=1> "Edit section: Visualizing your Browndye trajectories")]

You have used Browndye to get kinetic data, but what if you want to visualize your trajectories? Fear not, it is possible. 

# = The necessary links:[edit](</mediawiki/index.php?title=Creating_a_trajectory_to_visualize_from_Browndye&action=edit&section=2> "Edit section: = The necessary links:")]

  * [Browndye documentation](<https://browndye.ucsd.edu/browndye/doc/manual.html>)
  * [Browndye visualization script (process_trajectories.py)](<https://wiki.amaro.ucsd.edu/mediawiki/index.php/ScriptsMain>)



## The necessary files:[edit](</mediawiki/index.php?title=Creating_a_trajectory_to_visualize_from_Browndye&action=edit&section=3> "Edit section: The necessary files:")]

  * protein dx
  * protein xml
  * input xml (input for Browndye runs)
  * ligand dx
  * ligand xml
  * rxns xml (file containing the reaction pairs and their distances)



## Procedure[edit](</mediawiki/index.php?title=Creating_a_trajectory_to_visualize_from_Browndye&action=edit&section=4> "Edit section: Procedure")]

### Prepare Browndye to run[edit](</mediawiki/index.php?title=Creating_a_trajectory_to_visualize_from_Browndye&action=edit&section=5> "Edit section: Prepare Browndye to run")]

According to the Browndye documentation, you need to tell Browndye to create the nonstandard files you need to visualize your trajectories. Assuming you are using nam_simulation and not weighted ensemble, you need to add the flags 

<n-trajectories-per-output> number </n-trajectories-per-output> (change number to whatever number you want, this tells you how many trajectories in between an update of the output file) <n-steps-per-output> number </n-steps-per-output> (change the number to whatever number you want, this tells you how many time steps per update of the output file) <trajectory-file> trajectory </trajectory-file> (this is the prefix affixed to all your output trajectory files needed for visualization, so you can change "trajectory" to any other word you wish) 

Run the command 

bd_top input.xml 

where input.xml is whatever your input file is named. This will give you the files needed for simulation. Then run your simulation with 

nam_simulation 2hty-oseltamivir-simulation.xml 

where the .xml file is the *-simulation.xml file created from the bd_top command. This runs your simulation, and can take a long time depending on the other parameters you used in your simulation. After the simulation finishes, create the final visualization files with 

python2 process_trajectories.py -i input.xml -n 0 -o output.pqr -x all -w temp -s 1 -c 

The one thing to change in this is the -x flag. To see all trajectories (even ones where the ligand didn't find the binding site) leave this at "all". To only see trajectories resulting in a successful association, change "all" to "association". 

### Common error[edit](</mediawiki/index.php?title=Creating_a_trajectory_to_visualize_from_Browndye&action=edit&section=6> "Edit section: Common error")]

If you have changed "all" to "association" in the command above, and get the error
