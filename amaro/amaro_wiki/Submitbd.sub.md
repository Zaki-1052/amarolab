# Submitbd.sub

1. #!/bin/bash
  2. #PBS -q #put in your TSCC usage, whether it is home-mccammon or hotel or condo etc
  3. #PBS -N name #name your job
  4. #PBS -l nodes=1:ppn=3:gpu #put in GPU jobs in multiples of three, or CPU jobs in multiples of 12
  5. #PBS -l walltime=192:00:00 #put in max walltime (192:00:00), if your job finishes before you reach the end of your allocation, it will terminate as normal and release the remaining hours
  6. #PBS -o name-out.txt #put in your own name
  7. #PBS -e name-err.txt #put in your own name
  8. #PBS -V #leave blank
  9. #PBS -M #if you want email updates about when you submit a job and it finishes, put in your email here
  10. #PBS -m abe #leave this as is
  11. #PBS -A mccammon-gpu #leave this as is for McCammon users


  1. INITDIR=path #replace path with the path to the directory you will run stuff in


  1. cd $INITDIR


  1. nam_simulation /home/cseitz/run/2hty-oseltamivir-simulation.xml


  1. #before running, do the command export MODULEPATH=/projects/builder-group/jpg/modulefiles/applications:$MODULEPATH; module load browndye
  2. #to load Browndye and be able to run it on TSCC



  


  1. #remove this comment and all the header numbers above
