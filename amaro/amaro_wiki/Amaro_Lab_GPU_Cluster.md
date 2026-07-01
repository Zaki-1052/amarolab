# Amaro Lab GPU Cluster

## Hardware Spec[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=1> "Edit section: Hardware Spec")]

There are a total of 6 to 8 compute nodes, each have: 

  * 2 x Intel Xeon processor E5-2640v2, 8 Cores, 2.00 GHz
  * 64 GB DDR3 1600 MHz ECC/Registered RAM
  * 2 x NVidia Tesla K20 (total of 4 GPU per node)
  * 2 TB hard disk



The head node: 

  * 2 x Intel Xeon E5-2620 2.00 Ghz Six Core Processor
  * 32 GB DDR3 1600 MHz ECC/Registered RAM
  * 15 TB user storage



The cluster runs Bright Cluster Manager 6.1 with the SLURM scheduler 

## Quick Overview[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=2> "Edit section: Quick Overview")]

  * Request an account from TSCC by sending an email to [TSCC-Support Team](<mailto:TSCC-Support@sdsc.edu>) (Remember to CC Rommie)
  * Login to using ssh to: gpu.amaro.ucsd.edu 
    *       * are you having trouble ssh-ing into the Amaro Lab GPU Cluster from your laptop at home? Make sure you're on the UCSD VPN! 
  * This machine is meant for running MD simulations using AMBER on GPUs.
  * GROMACS simulations can also be run on the GPU cluster; however, you will get better performance for example with Keck2 (<http://keck2.ucsd.edu/dokuwiki/doku.php/start>).



## Optimal performance[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=3> "Edit section: Optimal performance")]

  * It is optimal to use just a single GPU per run (and run many seeds of your system)
  * A job should at most use two GPUs - there is no scaling beyond this even for large systems
  * There are system size limitations due to memory on the GPU cards, see [AMBER GPU System size limits](<http://ambermd.org/gpus/#system_size_limits>)
  * Read the AMBER page on GPU performance and features (it is updated more often than the manual) [AMBER GPU page](<http://ambermd.org/gpus/>)



## Queueing[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=4> "Edit section: Queueing")]

Updated by SPH on December 2022 

  * The AmaroLab GPU cluster uses the SLURM scheduler
  * For more information of how to use the commands for the SLURM Workload manager, use [the SLURM start guide](<https://slurm.schedmd.com/quickstart.html>)
  * The cluster has two queues; normal and a high priority queue (for folks running jobs related to the machines grant can run on a high priority queue - access by request to Rommie).
  * The normal queue has a 24h wall clock - the other queue is unrestricted
  * You can string together a series of jobs using dependencies (_eg._ "sbatch --dependency=afterany:JOBID submit02.sh", where JOBID is equal to the jobid of the previously submitted job in this series.
  * To all the jobs currently running and scheduled to run:


    
    
      squeue
    

  * To view the jobs submitted by a user:


    
    
      squeue -u <username>
    

  * To cancel one job:


    
    
      scancel <jobid>
    

  * To cancel all the jobs for a user:


    
    
      scancel -u <username>
    

  * To cancel all the pending jobs for a user:


    
    
      scancel -t PENDING -u <username>
    

  * To cancel one or more jobs by name:


    
    
      scancel --name myJobName
    

  * To hold a particular job from being scheduled:


    
    
      scontrol hold <jobid>
    

  * To release a particular job to be scheduled:


    
    
      scontrol release <jobid>
    

  * To requeue (cancel and rerun) a particular job:


    
    
      scontrol requeue <jobid>
    

The above commands have been added to the page as they were listed on [FAS RC Docs Harvard Page](<https://docs.rc.fas.harvard.edu/kb/convenient-slurm-commands>)

## Running jobs[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=5> "Edit section: Running jobs")]

To submit a job, create a script using the following as examples. 

The job is submitted using the command: 
    
    
      sbatch yourscriptname.sh
    

See this page on [running standard amber simulations](</mediawiki/index.php/Running_standard_amber_simulations> "Running standard amber simulations")

### Single GPU AMBER job[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=6> "Edit section: Single GPU AMBER job")]

For a single-GPU run use "srun" in front of pmemd.cuda 
    
    
    #!/bin/bash
    #SBATCH --get-user-env
    #SBATCH --gres=gpu:1
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=1
    #SBATCH --time=24:00:00
    #SBATCH --job-name=JOBNAME
    #SBATCH --output=JOBNAME.out
    #SBATCH --error=JOBNAME.err
    #SBATCH --mail-type=ALL
    #SBATCH --mail-user=USERNAME@UCSD.EDU
    #SBATCH --share
    
    echo $CUDA_VISIBLE_DEVICES
    
    srun $AMBERHOME/bin/pmemd.cuda -O -i md1.conf  -o md1.out -p system.prmtop -c min5.rst -ref min5.rst -r md1.rst  -x md1.nc 
    

### Dual GPU AMBER job[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=7> "Edit section: Dual GPU AMBER job")]

For a dual-GPU run use "mpirun" in front of pmemd.cuda.mpi 
    
    
    #!/bin/bash
    #SBATCH --get-user-env
    #SBATCH --gres=gpu:2
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=1
    #SBATCH --time=24:00:00
    #SBATCH --job-name=JOBNAME
    #SBATCH --output=JOBNAME.out
    #SBATCH --error=JOBNAME.err
    #SBATCH --mail-type=ALL
    #SBATCH --mail-user=USERNAME@UCSD.EDU
    #SBATCH --share
    
    echo $CUDA_VISIBLE_DEVICES
    
    mpirun -np 2 $AMBERHOME/bin/pmemd.cuda.MPI -O -i md1.conf  -o md1.out -p system.prmtop -c min5.rst -ref min5.rst -r md1.rst  -x md1.nc
    

### Saving AMBER trajectories locally[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=8> "Edit section: Saving AMBER trajectories locally")]

Updated 10/15/20 by Christian. If you are running a multi-GPU job, it may be faster to use pmemd.cuda.MPI instead of pmemd.cuda, but I have not tested this... 
    
    
    #!/bin/bash
    #SBATCH --get-user-env
    #SBATCH --gres=gpu:1
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=1
    #SBATCH --time=24:00:00
    #SBATCH --job-name=MyJobName
    #SBATCH --output=MyJobName.out
    #SBATCH --error=MyJobName.err
    #SBATCH --mail-type=ALL
    #SBATCH --mail-user=USERNAME@UCSD.EDU
    #SBATCH --share
    
    module load amber/18
    
    # Output the CUDA device IDs on the node
    echo $CUDA_VISIBLE_DEVICES
    
    # Define unique scratch directory path using the job id
    SCRATCH_DIRECTORY=/local/${USER}/${SLURM_JOBID}
    
    # Create the scratch directory
    mkdir -p ${SCRATCH_DIRECTORY}
    
    # Run our command-ref min5.rst
    srun $AMBERHOME/bin/pmemd.cuda -O -i md1.conf -o ${SCRATCH_DIRECTORY}/md1.out -p system.prmtop -c min5.rst -ref min5.rst -r ${SCRATCH_DIRECTORY}/md1.rst -x ${SCRATCH_DIRECTORY}/md1.nc
    
    # Copy the scratch directory on the node to the directory we submitted the job from
    cp -r ${SCRATCH_DIRECTORY} ${SLURM_SUBMIT_DIR}
    
    # Delete the scratch directory on the node
    rm -rf ${SCRATCH_DIRECTORY}
    
    # Exit from script
    exit 0
    

## How to run AMBER simulations locally on a node[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=9> "Edit section: How to run AMBER simulations locally on a node")]

**1\. Set up your system, and write a submit script to run jobs.**

  * Most users should use the "Saving AMBER trajectories locally" submit script just above. Simply copy that script into some text document in your terminal, and save it with whatever name you choose. Since you will run it with the sbatch command (see below) you might want to call it name.sb, where name is whatever you choose. Some details about that script:


  * A scratch directory needs to be defined ("SCRATCH_DIRECTORY") and needs to be created in the node ("mkdir -p ${SCRATCH_DIRECTORY}") to temporarily house the generated simulation files.


  * The files need to be copied back to the network drive from the node's local hard drive, when the AMBER simulation has finished ("cp -r ${SCRATCH_DIRECTORY} ${SLURM_SUBMIT_DIR}"). 


  * After copying the files to the network home, the simulation files need to be removed from the local drive ("rm -rf ${SCRATCH_DIRECTORY}"). 


  * It is also paramount that you make sure that all the files are removed from the node's local hard drive, when the simulation has ended. 


  * The email flags in the submit script are optional, keep them if you prefer to get email updates of your jobs. The rest of the flags and commands are recommended.



**2\. Benchmark your system. This is critical so you can set your run to finish BEFORE the 24 hour wall clock limit (see below).**

  * Benchmarking: You need to know how many steps AMBER will likely produce with your system on the GPU cluster before starting to use the node's local drive in your simulations. Running your simulation for 2000 steps will give you a reasonable benchmark speed.


  * Set each simulation to end before the walltime (e.g. time=24:00:00) runs out by fixing the time in the input file (nstlim in md1.conf) based on your benchmarking. Leave some time for transferring the files back to the network drive. If you do not do this, your files will not get transferred back to your directory and will be lost.



**3\. Run your job!**

  * Again, this GPU cluster runs a SLURM scheduling system, so you can run your job with sbatch submitscript.sb, where submitscript is whatever you want to call your submit script.


  * As mentioned above, you can string together a series of jobs using dependencies (_eg._ "sbatch --dependency=afterany:JOBID submit02.sb", where submit02 is the name of your submit script, and JOBID is equal to the jobid of the previously submitted job in this series. The JOBID can be found from checking your queue status (see "Other notes" below).



**4\. Other notes**

  * By default you are running the simulations using the network drive (/home/USERNAME/), which means that the files produced by the simulations are not written locally in the node.


  * To assure good performance in all conditions, you can save your simulations first locally in the representative node and then transfer the files back to your folder in the network drive.


  * When writing dense output files or when the cluster is saturated with many calculations, the limited connection between the nodes and the network drive could prove to be a performance bottleneck.


  * You can see which node is used for each simulation using "squeue -a" or "squeue -u USERNAME" command, where USERNAME is your normal username that you used to access this GPU cluster. The former command will show all users and jobs on the queue, so you can see if others are using the GPU cluster or trying to access it.


  * The individual nodes can be accessed using SSH (e.g. "ssh node001") and their performance can be monitored (e.g. "top"). Each node has /local folder where the simulations should be stored temporarily.


  * The normal queue can run 20 jobs at a time amongst all lab members. If others need to use it, don't hog them all for yourself!



## Running GROMACS jobs[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=10> "Edit section: Running GROMACS jobs")]

GROMACS (VERSION 5.0.4) should be run using a single GPU and 8 CPU threads on the GPU cluster. 

### GPU job 1[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=11> "Edit section: GPU job 1")]
    
    
    #!/bin/bash
    #SBATCH --get-user-env
    #SBATCH --gres=gpu:1
    #SBATCH --cpus-per-task=8
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=1
    #SBATCH --time=24:00:00
    #SBATCH --job-name=JOBNAME
    #SBATCH --output=JOBNAME.out
    #SBATCH --error=JOBNAME.err
    #SBATCH --mail-type=END
    #SBATCH --mail-user=USERNAME@UCSD.EDU
    #SBATCH --share
    
    echo $CUDA_VISIBLE_DEVICES
    
    module load gromacs
    mkdir -p /local/USERNAME/JOBNAME
    mdrun -nt 8 -deffnm /local/USERNAME/JOBNAME/md -s md.tpr -v -maxh 23.8
    cp /local/USERNAME/JOBNAME/* .
    rm -rf /local/USERNAME/JOBNAME
    

## How to run GROMACS simulation locally on a node[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=12> "Edit section: How to run GROMACS simulation locally on a node")]

  * To use the submission script you need to substitute USERNAME and JOBNAME with your information.


  * You need to load the GROMACS environment with "module load gromacs" command.


  * To assure fast simulation speed, you should save the simulation results locally to the node instead of writing directly to the home network drive (default is /home/USERNAME/). For this purpose you need to generate a temporary folder ("mkdir -p /local/USERNAME/JOBNAME"). 


  * When running the simulation you need to specify that eight CPU threads are used with both mdrun (-nt 8) and SBATCH options (#SBATCH --cpus-per-task=8). 


  * All the files generated by the mdrun (md.xtc, md.trr, md.edr, md.gro etc.) need to have the node's local path (/local/USERNAME/JOBNAME/) to assure that they are indeed written locally into the node. 


  * The generated files need to be copied back to the network drive from the node's local hard drive, when the simulation has finished ("cp /local/USERNAME/JOBNAME/* ."). 


  * To make automatic copying possible, the MD simulation has to stop before the walltime (e.g. time=24:00:00) ends. The simulation can be stopped before the walltime runs out easily using -maxh command (e.g. -maxh 23.8). 


  * If the simulation files are particularly large, one might need to reserve more time for the copying them back to the network home than what is used in the example submission script.


  * After copying the files to the network home, the simulation files need to be removed from the local drive ("rm -rf /local/USERNAME/JOBNAME"). 


  * Although using more than eight CPU threads (e.g. -nt 32) might make the simulation faster, this approach slows down the overall performance of the whole node.


  * You can see which node is used for each simulation using "squeue -a" or "squeue -u USERNAME" command. 


  * The individual nodes can be accessed using SSH (e.g. "ssh node001") and their performance can be monitored (e.g. "top"). Each node has /local folder where the simulations should be stored temporarily.



## Running NAMD jobs[edit](</mediawiki/index.php?title=Amaro_Lab_GPU_Cluster&action=edit&section=13> "Edit section: Running NAMD jobs")]

You can use NAMD 2.13 to run GPU jobs; however, running on them on this cluster is about 4x slower than on Comet or Bridges. Using more GPUs or more CPUs will not appreciably increase NAMD performance on the Amaro GPU cluster (I have tested this). To run a NAMD GPU job, follow the steps under "How to run AMBER simulations locally on a node" but then use this submit script: 
    
    
    #!/bin/bash
    #SBATCH --get-user-env
    #SBATCH --gres=gpu:1
    #SBATCH --cpus-per-task=8
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=1
    #SBATCH --time=00:55:00
    #SBATCH --job-name=09-rep1
    #SBATCH --output=output.out
    #SBATCH --error=error.err
    #SBATCH --share
    
    # Output the CUDA device IDs on the node
    echo $CUDA_VISIBLE_DEVICES
    
    # Define unique scratch directory path using the job id
    SCRATCH_DIRECTORY=/local/${USER}/${SLURM_JOBID}
    
    # Create the scratch directory
    mkdir -p ${SCRATCH_DIRECTORY}
    
    # Run our command
    /cm/shared/apps/namd/2.13/namd2 +p8 +devices 0 prod1.conf > prod1.log
    
    # Copy the scratch directory on the node to the directory we submitted the job from
    cp -r ${SCRATCH_DIRECTORY} ${SLURM_SUBMIT_DIR}
    
    # Delete the scratch directory on the node
    rm -rf ${SCRATCH_DIRECTORY}
    
    # Exit from script
    exit 0
