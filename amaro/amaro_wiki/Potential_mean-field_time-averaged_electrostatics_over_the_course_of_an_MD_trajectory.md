# Potential mean-field (time-averaged) electrostatics over the course of an MD trajectory

## Potential mean-field electrostatics[edit](</mediawiki/index.php?title=Potential_mean-field_\(time-averaged\)_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=1> "Edit section: Potential mean-field electrostatics")]

[APBS User's Guide](<http://www.poissonboltzmann.org/apbs/user-guide>)

The adaptive Poisson-Boltzmann solver program package can compute protein electrostatics for a static conformation. What if you want the potential mean field of this protein? In other words, what if you want to know the average electrostatic field this protein exhibits over the course of an MD trajectory? Read on... 

Tutorial by Christian Seitz and Lane Votapka 6/25/2021 

### 1\. Create your MD trajectory[edit](</mediawiki/index.php?title=Potential_mean-field_\(time-averaged\)_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=2> "Edit section: 1. Create your MD trajectory")]

Load your topology/parameter and trajectory files into VMD, and save the full-length trajectory as a PDB trajectory. This will take up much more space than a normal trajectory file, so proceed with caution. 

### 2\. Split your trajectory into single frames[edit](</mediawiki/index.php?title=Potential_mean-field_\(time-averaged\)_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=3> "Edit section: 2. Split your trajectory into single frames")]

On the command line, do 
    
    
     awk '/END/{n++}{print > "test.pdb" n }' apbs.pdb 

where 
    
    
     test.pdb 

is the prefix and name you want to call all your single frame PDB files, which will result in files named something like 
    
    
     test.pdb1 test.pdb2 test.pdb3 

and so on, and 
    
    
     apbs.pdb 

is the PDB trajectory file created in step 1. This command doesn't give a number to the first frame, so you can do 
    
    
     mv test.pdb test.pdb0 

to give the first frame a number consistent with the rest of the files. This command also creates an empty file as the last file, so if you had 2000 frames in your PDB trajectory, you will create an empty 
    
    
     test.pdb2000 

file. You can either ignore or delete this file. 

### 3\. Create PQR files for each frame[edit](</mediawiki/index.php?title=Potential_mean-field_\(time-averaged\)_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=4> "Edit section: 3. Create PQR files for each frame")]

Load the amber module, then run 
    
    
     for i in {0..1999}; do echo $i; ambpdb -p phage.parm7 -c test.pdb$i -pqr > frame_$i.pqr ; done 

on the command line. This iterates over 2000 frames to create a PQR file for each one; obviously change the frame number to whatever you have, and change the parameter file to one from your own system. 

### 4\. Create an APBS input file[edit](</mediawiki/index.php?title=Potential_mean-field_\(time-averaged\)_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=5> "Edit section: 4. Create an APBS input file")]

For this tutorial, the APBS module on your workstation will not suffice, you will need to download the linux version from source forge: [APBS source forge download](<https://sourceforge.net/projects/apbs/>). The download should be called "/apbs/apbs-3.0/APBS-3.0.0_Linux.zip" or something similar; if that link doesn't work then you may find it on GitHub: [APBS GitHub download](<https://github.com/Electrostatics/apbs-pdb2pqr/releases>). Download this and unzip it. In the directory with all your PDB frame files, run this command 
    
    
      python2 /home/cseitz/Downloads/APBS-3.0.0.Linux/share/apbs/tools/manip/inputgen.py --space=1.0 --istrng=0.15 frame_0.pqr 

which defines the grid spacing as 1 angstrom, the ionic strength as 0.15 M NaCl, and creates a input file named frame_0.in based off of your frame_0.pqr file, which is fine. To see more options, run the inputgen.py command and do -h. For clarity, rename the frame_0.in as template.in or something like that. Obviously, change the path above to whatever is the path of your downloaded version of APBS. 

### 5\. Edit and configure your APBS input file[edit](</mediawiki/index.php?title=Potential_mean-field_\(time-averaged\)_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=6> "Edit section: 5. Edit and configure your APBS input file")]

Inside template.in, delete everything between the second "end" and "quit" at the bottom; the file natively contains two input files and we only need one. Also change the "mg_para" to "mg-auto" because our version of APBS isn't compiled with parallelization (we will work around this later). Finally, set the temperature to your desired temperature, change "frame_0.pqr" to "frame_INDEX.pqr" inside of template.in, and change "write pot dx pot" to "write pot dx frame_INDEX". 

### 6\. Create APBS input files for each frame[edit](</mediawiki/index.php?title=Potential_mean-field_\(time-averaged\)_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=7> "Edit section: 6. Create APBS input files for each frame")]

On the command line, run 
    
    
     for i in {0..1999} ; do echo $i ; cat template.in | sed "s/INDEX/$i/g" > frame_$i.in ; done 

to create APBS input files for every frame of your trajectory. 

### 7\. Run APBS calculations[edit](</mediawiki/index.php?title=Potential_mean-field_\(time-averaged\)_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=8> "Edit section: 7. Run APBS calculations")]

Now we can run the APBS calculations. On the command line, run 
    
    
     for i in {0..1999}; do echo $i; apbs frame_$i.in; done 

You will likely want to run this command on just 1 or 2 frames at the start to get an idea of how long it will take and how much memory will be required. Depending on how long your system will take, you may want to split this command up into several sections. For example, I had 2000 APBS calculations to run. I opened 10 new terminals and ran 200 calculations in each; for my large system this took ~80 GB of memory and lasted ~30 hours. Remember, our version of APBS runs in serial, so each new terminal that you open will be just one thread (one CPU). If you have 24 CPUs on your workstation, you can easily accommodate using 10 threads on 10 terminals to run your APBS calculations. 

### 8\. Average the electrostatic maps[edit](</mediawiki/index.php?title=Potential_mean-field_\(time-averaged\)_electrostatics_over_the_course_of_an_MD_trajectory&action=edit&section=9> "Edit section: 8. Average the electrostatic maps")]

While we can split up the creation of the electrostatic maps across CPUs, we cannot split up the averaging. Thankfully, this takes far less time. Inside your ~/.bashrc file, add 
    
    
     export LD_LIBRARY_PATH=/home/cseitz/Downloads/APBS-3.0.0.Linux/lib:$LD_LIBRARY_PATH 

to the bottom (and of course change the path to wherever your downloaded APBS directory is), save and source in the directory where you want to average your files. This allows APBS to find a library that it needs. Next, you need to create a template averaging file. Do it like this on the command line: 
    
    
     
    echo "frame_0.dx" > dxmath.in
    for i in {1..1999}; do echo $i; echo "frame_$i.dx +" >> dxmath.in; done 
    

This will create a file called dxmath.in, and will populate the inside of that file with the commands to average each frame. Note, this file works in Polish math notation, where the operator follows the operands. Now, at the bottom of your dxmath.in, add 
    
    
     2000 /
    averaged.dx =

Since I am wanting to average 2000 frames, this will tell the dxmath.in file to average over 2000, and to create an output file called averaged.dx. With this file properly formatted, you can run it to average all of your dx files into one with 
    
    
     /home/cseitz/Downloads/APBS-3.0.0.Linux/share/apbs/tools/bin/dxmath dxmath.in 

Finally, you can load the averaged.dx into VMD along with a topology file to visualize the averaged electrostatics! 

  
**EDIT 6/30/22 by Mia Rosenfeld:**

Unfortunately, the dxmath command in APBS has a limit of 20 calculations per execution. Therefore, you can only average 19 files at a time (adding each file counts as a calculation, then the averaging at the end counts as one calculation). 

I had to average 1259 frames, so here's a code that I wrote up with Fiona Kearns' help to generate automatic dxmath.in files for 19 frames at a time to iteratively average: 
    
    
    #!/bin/bash
    
    variant=${1}
    state=${2}
    #variant options: wt, delta, omicron
    #state options: open, closed
    mathfile=0
    
    for frame in {1..1259..19}; do
            num1=$((frame + 1))
            num2=$((num1 + 17))
            mathfile=$((mathfile + 1))
    
    
                                    echo "${variant}_spike_${state}_frame$frame.dx" > dxmath$mathfile.in
                                    for i in `seq $num1 1 $num2`; do echo $i; echo "${variant}_spike_${state}_frame$i.dx +" >> dxmath$mathfile.in ; done
    echo "
    
     19 /
    averaged_${variant}_${state}_$mathfile.dx =" >> dxmath$mathfile.in
    
    done

From there, you will acquire averages of 19 frames iterating through your entire trajectory. You can then average your averages. I know this is kinda nuts, but it's the only way to get around the 20 calculation limit of dxmath :)
