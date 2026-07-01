# SuperComputing

Welcome to the Amaro Lab Supercomputing Resources page. 

## External Resources[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=1> "Edit section: External Resources")]

Watch a [video on how to use the Delta Supercomputer](<https://youtu.be/H5dgLIoVgGk>) and download the PDF from the presentation [Media:Supercomputer_tutorial_2023.pdf](</mediawiki/images/f/f6/Supercomputer_tutorial_2023.pdf> "Supercomputer tutorial 2023.pdf"). 

### XSEDE/ACCESS Computing Resources[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=2> "Edit section: XSEDE/ACCESS Computing Resources")]

Account Setup: Go to this website [ACCESS Page](<https://access-ci.org/>) and create a new account. Then ask either Rommie or Lane to be added to the lab allocation. Note: Before starting any project calculations you NEED to estimate the SU (service units = CPU or GPU hours) cost and get approval from Rommie. For more information on calculating SU costs, see the Benchmarking section below. 

SLURM User Guide: 

  * <https://slurm.schedmd.com/>



Computing Resources: 

  * dt-login01.delta.ncsa.illinois.edu [Delta User Guide](<https://wiki.ncsa.illinois.edu/display/DSC/Delta+User+Guide>)
  * anvil.rcac.purdue.edu [Anvil User Guide](<https://www.rcac.purdue.edu/knowledge/anvil>)
  * login.expanse.sdsc.edu [Expanse User Guide](<https://www.sdsc.edu/support/user_guides/expanse.html>)
  * bridges2.psc.xsede.org [Bridges2 User Guide](<https://www.psc.edu/resources/bridges-2/user-guide-2-2/>)



OLD computing resources (no longer available): 

  * stampede.tacc.utexas.edu [TACC Stampede2 User Guide](<https://www.tacc.utexas.edu/user-services/user-guides/stampede-user-guide>) or [XSEDE Stampede2 User Guide](<https://portal.xsede.org/tacc-stampede2>)
  * comet.sdsc.edu [SDSC Comet User Guide](<https://www.sdsc.edu/support/user_guides/comet.html>) or [XSEDE Comet User Guide](<https://portal.xsede.org/sdsc-comet>)
  * bridges.psc.xsede.org [PSC Bridges User Guide](<https://www.psc.edu/bridges/user-guide>) or [XSEDE Bridges User Guide](<https://portal.xsede.org/psc-bridges>)



  
Storage Ressources: 

  * ranch.tacc.utexas.edu - [Ranch User Guide ](<https://www.tacc.utexas.edu/user-services/user-guides/ranch-user-guide>)



## Local Resources[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=3> "Edit section: Local Resources")]

### Amaro Lab GPU Cluster[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=4> "Edit section: Amaro Lab GPU Cluster")]

Internal GPU cluster earmarked for cancer and workflow activities. Surplus time can be utilized by the Amaro Lab. 

For more information visit [Amaro Lab GPU Cluster](</mediawiki/index.php/Amaro_Lab_GPU_Cluster> "Amaro Lab GPU Cluster")

### CTBP[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=5> "Edit section: CTBP")]

Center for Theoretical Biophysics has a CPU and a GPU cluster. 

For more information visit: [CTBP Computing](<https://ctbp.ucsd.edu/resources.html>) or these links to either the [CPU Cluster Wiki](<https://ctbp.ucsd.edu/computing/wiki/introduction_to_ctbp_cluster_computing>) or [GPU Cluster Wiki](<https://ctbp.ucsd.edu/computing/wiki/computing_on_gpu_cluster>)

### NBCR[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=6> "Edit section: NBCR")]

The National Biomedical Computation Resource has a GPU cluster (kivid) CPU cluster (rocce) as well as a web-services cluster. However, kivid has died (rip). 

For more information visit: [NBCR Wiki](<http://nbcr.ucsd.edu/wiki/index.php/Main_Page>)

### Keck2[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=7> "Edit section: Keck2")]

The W. M. Keck Laboratory for Integrated Biology II has CPU and GPU resources available. These resources are physical workstations that are used for teaching and other things, meaning the resources are not always available. 

For more information visit: [Keck2 Computing](<http://keck2.ucsd.edu/dokuwiki/doku.php/start>)

### Hopper[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=8> "Edit section: Hopper")]

(Updated by SPH December 2022) 

The Amaro lab has GPU and CPU resources available on TSCC (SDSC). 

  * Request an account from TSCC by sending an email to [TSCC-Support Team](<mailto:TSCC-Support@sdsc.edu>) (Remember to CC Rommie)


  * To login to the machine use your UCSD username and the following ssh command: 


    
    
     ssh username@tscc-login.sdsc.edu
    

  * Copy your files to and run your jobs from the following directory:


    
    
     /oasis/tscc/scratch/username
    

Make certain to move your files to home, as scratch is deleted every 90 days. 

Here are three helpful commands from Robert Konecny: 

1\. Run this on the command line. 
    
    
     lsjobs --property=hopper-node
    

This will show the hopper GPUs and CPUs, and will show you their current load. This can help you decide how many GPUs or CPUs you want to use in your submission script to reduce queue time. Make sure you do not have a conda environment active, or you will get an error! ( 

2\. If you want to schedule a single GPU job to one of the Hopper nodes use this, ddd this to your submit script. 
    
    
     #PBS -A amaro-hopper-gpu
     #PBS -q home-hopper
     #PBS -l nodes=1:ppn=4:gpu3090
    

If your job keeps getting sent to a node that is crashing, notify TSCC immediately. Until they fix it, you can specify what node to send your job to. Here, I am sending a job to GPU node 5-0. 

3\. Run any of the following on the command line to show your current SU allocation. 
    
    
     /opt/gold/bin/gbalance -p amaro-hopper-gpu
     /opt/gold/bin/gbalance -p amaro-hopper
     /opt/gold/bin/gbalance -p mccammon-hopper-gpu
     /opt/gold/bin/gbalance -p mccammon-hopper  
    

These will tell you the current GPU and CPU balance for the Amaro and McCammon accounts. This can help you decide where to run your job, and under what allocation (if you are a part of multiple allocations). 

4\. Another way of looking at your allocations balance is execute: 
    
    
     gbalance -u username
    

5\. If you want to see information about a particular node, such as node tscc-3-28, run this on the command line 
    
    
     pbsnodes tscc-3-28
    

## Fast log-in to remote machines using RSA keys[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=9> "Edit section: Fast log-in to remote machines using RSA keys")]

Tutorial created by Christian, Updated by SPH December 2022. If you want to log onto an external resource (such as one of the XSEDE supercomputers) without having to use a password, follow the steps below. In this example, I am working on Delmar and trying to set up an automatic log on for Comet without having to use a password. I ran these commands from my downloads folder but it doesn't matter where you run them from. 

Note: If you have already set this up for one connection, you only need to repeat steps #2 and #3, using the new address you would like to connect to. 

I used these links: 

<https://www.tecmint.com/ssh-passwordless-login-using-ssh-keygen-in-5-easy-steps/>

<https://help.github.com/en/articles/error-agent-admitted-failure-to-sign>

<https://stackoverflow.com/questions/2135644/how-can-i-define-a-bash-alias-as-a-sequence-of-multiple-commands>

### Create authentication ssh keys[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=10> "Edit section: Create authentication ssh keys")]

To generate an RSA pair on the machine from which you will be logging on. 
    
    
      ssh-keygen -t rsa
    

Hit enter, to overwtrite the existing id_rsa file 
    
    
      Overwrite (y/n)? y
    

Hit Enter (twice) to bypass the passphrase requirement 
    
    
     Enter passphrase (empty for no passphrase): (press enter)
     Enter same passphrase again: (press enter)
    

Your RSA pair will be generated and saved 
    
    
     Your identification has been saved in /home/username/.ssh/id_rsa.
     Your public key has been saved in /home/username /.ssh/id_rsa.pub.
     The key fingerprint is:
     c5:2b:f4:12:1d:da:f5:ec:40:93:6a:9c:83:da:46:67 username@hostname
     The key's randomart image is:
     +--[ RSA 2048]----+
     |        . +.     |
     |       = +.+     |
     |      +o=o. o    |
     |     .ooEo o     |
     |     +o+S.  .    |
     |    . oo         |
     |     .    o      |
     |                 |
     |                 |
     +-----------------+
    

### Create an ssh directory on the external resource[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=11> "Edit section: Create an ssh directory on the external resource")]
    
    
     ssh username@hostname.remotehost.org.ext mkdir -p .ssh
          Password: (Put in my password for remotehost here)
    

### Upload your generated public keys to the external resource[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=12> "Edit section: Upload your generated public keys to the external resource")]
    
    
     cat ~/.ssh/id_rsa.pub | ssh username@remotehostname.remotehost.org.ext 'cat >> .ssh/authorized_keys'
          Password: (Put in password for remotehost here)
    

This same file and step can be copied to other remote hosts without re-doing the previous steps. 

### Fix a keyloading error[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=13> "Edit section: Fix a keyloading error")]
    
    
     eval "$(ssh-agent -s)"
          Agent pid 18049
     ssh-add
          Identity added: /home/username/.ssh/id_rsa (/home/username/.ssh/id_rsa)
    

### Set permissions on your home workstation[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=14> "Edit section: Set permissions on your home workstation")]
    
    
     SSH_AUTH_SOCK=0 ssh username@remotehost.remotehost.org.ext "chmod 700 .ssh; chmod 640 .ssh/authorized_keys"
    

### Create an alias to ssh into the external resource[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=15> "Edit section: Create an alias to ssh into the external resource")]
    
    
     vi ~/.alias 
    

(now inside vi, in insert mode) 
    
    
     alias my_remotehost_alias="ssh-add; ssh -X username@remotehost.remotehost.org.ext"
    

Source your alias file 
    
    
     source ~/.alias
    

  


### Log on to the external resource with one command! Voilà![edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=16> "Edit section: Log on to the external resource with one command! Voilà!")]
    
    
     my_remotehost_alias
    
    
    
           Last login: Tue Jun  4 11:43:27 2019 from hostname.amaro.ucsd.edu
           Rocks 6.2 (SideWinder)
           Profile built 16:45 08-Feb-2016
           Kickstarted 17:27 08-Feb-2016
                                                                                  
                                 WELCOME TO 
                 __________________  __  _______________
                   -----/ ____/ __ \/  |/  / ____/_  __/
                     --/ /   / / / / /|_/ / __/   / /
                      / /___/ /_/ / /  / / /___  / /
                      \____/\____/_/  /_/_____/ /_/
           
           *******************************************************************************
           
           [1] Example Scripts: /share/apps/examples
           
           [2] Filesystems:
           
                (a) Lustre scratch filesystem : /oasis/scratch/comet/$USER/temp_project
                    (Preferred: Scalable large block I/O)
                       *** Meant for storing data required for active simulations
                       *** Not backed up and should not be used for storing data long term
                       *** Periodically clear old data not required for active simulations
           
                (b) Compute/GPU node local SSD storage: /scratch/$USER/$SLURM_JOBID
                    (Meta-data intensive jobs, high IOPs)
           
                (c) Lustre projects filesystem: /oasis/projects/nsf
                
                (d) /home/$USER : Only for source files, libraries, binaries.
                    *Do not* use for I/O intensive jobs.
          
           [3] Comet User Guide: <http://www.sdsc.edu/support/user_guides/comet.html>
            ******************************************************************************
    

# Running jobs - submit scripts[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=17> "Edit section: Running jobs - submit scripts")]

## Hopper[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=18> "Edit section: Hopper")]

### Using the PBS Scheduler[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=19> "Edit section: Using the PBS Scheduler")]

(Updated by SPH December 2022) 

There are a number of schedulers and submission engines used on supercomputer machines. TSCC Hopper uses the PBS Scheduler. Here you will find instructions for using the various commands. This page has been adapted from the [NASA.gov website](<https://www.nas.nasa.gov/hecc/support/kb/commonly-used-pbs-commands_174.html>) instructions for using a PBS scheduler. 

To submit a batch job to the PBS scheduler: 
    
    
     qsub yourjobscript.sh
    

To submit to a specified queue: 
    
    
     qsub -q queue_name job_script 
    

Queue names on include normal, debug, long, devel, and low. When queue_name is omitted, the job is routed to the default queue, which is the normal queue. 

To submit an interactive PBS job: 
    
    
     qsub -I -q queue_name -l resource_list 
    

No job_script should be included when submitting an interactive PBS job. 

  
See man pbs_resources for more information on what resources can be specified. 

Note: If -l resource_list is omitted, the default resources for the specified queue is used. When queue_name is omitted, the job is routed to the default queue, which is the normal queue. 

  
To display queue information for the entire queue: 
    
    
     qstat
    

To display jobs submitted under your username: 
    
    
     qstat -u username
    

  
To delete a job with a specific job ID: 
    
    
     qdel job_id
    

To delete a series of jobs within a range of job_id-y to job_id_y: 
    
    
     qdel {job_id-x..job_id_y)
    

### NAMD on Amaro Hopper GPU cluster[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=20> "Edit section: NAMD on Amaro Hopper GPU cluster")]

2/19/2021 by Ozlem. 

The below script uses NAMD2.14. 

If you want to use NAMD3, change the export path command for NAMD2.14 in the script to the below one: 

export PATH=/home/ux453813/pkg/NAMD_3.0alpha8_Linux-x86_64-multicore-CUDA:${PATH} 

And change the execution command line to: 

namd3 +p $PBS_NUM_PPN +setcpuaffinity +idlepoll +devices 0 filename.conf > filename.log 
    
    
    
    #!/bin/bash
    #
    #PBS -A amaro-hopper
    #PBS -q home-hopper
    #PBS -l nodes=1:ppn=4:gpu3090
    #PBS -l walltime=48:00:00
    #PBS -N n102
    #PBS -o pbs-${PBS_JOBID}.out
    #PBS -e pbs-${PBS_JOBID}.err
    #PBS -V
    #
    
    set -xv
    
    # function to copy files back from /scratch to initial directory
    copy_back() {
        rsync -av $TMPDIR $PBS_O_WORKDIR/
    }
    
    # create a bash function which will do the cleanup (file copying) if the 
    # job is killed due to exceeding the wallclock
    exit_cleanup() {
        echo "This job was killed by PBS on" `date`
        echo "Copying files back after job cancellation ..."
        while true ; do
            sleep 5
            echo "Trying rsync ... "
            copy_back
            if [ $? -eq 0 ] ; then break ; fi
        done
        echo "Finished cleanup on" `date`
        exit 0
    }
    
    # catch SIGTERM and do clean up
    trap exit_cleanup SIGTERM
    
    echo "Started on" `date`
    
    # copy input files from current dir ($PBS_O_WORKDIR) to /scratch ($TMPDIR)
    rsync -av $PBS_O_WORKDIR/* $TMPDIR/
    
    cd $TMPDIR
    
    echo "Using $PBS_NUM_PPN CPU cores."
    export PATH=/home/ux453813/pkg/NAMD_2.14_Linux-x86_64-multicore-CUDA:${PATH}
                                                                                   
    namd2 +p $PBS_NUM_PPN +setcpuaffinity +idlepoll +devices 0 filename.conf > filename.log
    
    echo "Finished on" `date`
    echo "Copying files back after job's normal termination ..."
    copy_back
    

### NAMD on Amaro Hopper AMD CPU nodes[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=21> "Edit section: NAMD on Amaro Hopper AMD CPU nodes")]

2/19/2021 by Ozlem. 

Log in to your SDSC / TSCC account. 

Currently there are 4 nodes with 64 CPUs each. It is possible to run on all 4 nodes simultaneously, but it may increase queue time. 

The fastest way to run on these CPU nodes is to submit from /scratch directories. 
    
    
    
    #!/bin/bash
    #
    # rok Last modified: 2021-02-10 21:09:53
    #
    #PBS -A amaro-hopper
    #PBS -q home-hopper
    #PBS -l nodes=1:ppn=64:ib
    #PBS -l walltime=48:00:00
    #PBS -N namd2-cpu-ib-hopper
    #PBS -o pbs-${PBS_JOBID}.out
    #PBS -e pbs-${PBS_JOBID}.err
    #PBS -V
    #
    
    set -xv
    
    echo "Started on" `date`
    
    cd $PBS_O_WORKDIR
    
    echo "Using $PBS_NUM_NODES nodes and $PBS_NUM_PPN CPU cores/node ($PBS_NP total)."
    NAMD2_PATH=/home/ux453813/pkg/NAMD_2.14_Linux-x86_64-verbs-smp
    export PATH=${NAMD2_PATH}:${PATH}
    
    
    # Generate charmrun nodelist
    NODELIST=./nodelist.${PBS_JOBID}
    for host in $(uniq ${PBS_NODEFILE}) ; do
        echo "host ${host} ++cpus ${PBS_NUM_PPN}" >> ${NODELIST}
    done
    
    ${NAMD2_PATH}/charmrun ++verbose ++nodelist ${NODELIST} \
        ++scalable-start ++p ${PBS_NP} ++ppn ${PBS_NUM_PPN} \
        ${NAMD2_PATH}/namd2 +setcpuaffinity +idlepoll filename.conf > filename.log
    
    echo "Finished on" `date`
    
    

### Amber on Amaro Hopper GPU nodes v1[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=22> "Edit section: Amber on Amaro Hopper GPU nodes v1")]

1/25/2021 by Ozlem. (Thanks to Robert Konecny for input about system details.) 

Log in to your SDSC / TSCC account. 

To take advantage of the new GPUs your software must be compiled with CUDA version at least 11. Here you can download a precompiled Amber20 pmemd.cuda with CUDA 11.1: 

<https://morgan.ucsd.edu/downloads/amber20+cuda11.tar.gz>

Install it somewhere in your $HOME directory and then use this path in your PBS submission script (below). 

The nodes have very fast /scratch disk installed so make sure you run your jobs from there rather than from /oasis or $HOME which is much slower and could potentially slow down your jobs. 

To make sure that your output files are copied back from /scratch to your working directory, run a short benchmark for your system and make sure the simulation time you request can complete in the wallclock time limit you have on your submission script. Otherwise, the script might stop abruptly when time runs out and fail to copy the output files back. 
    
    
    
    #!/bin/bash
    #PBS -m e
    #PBS -o a3b_j.out
    #PBS -e a3b_j.err
    #PBS -V
    #PBS -N a3b                              # Job name 
    #PBS -l walltime=10:00:00       # wallclock time
    #PBS -M XXX@gmail.com        #your email address
    
    #PBS -W group_list=hopper-group
    #PBS -A amaro-hopper
    #PBS -q home-hopper
    #PBS -l nodes=1:ppn=4:gpu3090
    
    source /home/demir/amber20+cuda11/amber+cuda.sh    # change this path with your own Amber path
    
    # # Copy all your input files to /scratch ($TMPDIR is created by PBS)
    cp $HOME/a3b_benchmark/a3b_apo_5td5.top $HOME/a3b_benchmark/md4.rst $HOME/a3b_benchmark/md5.in $TMPDIR
    
    cd $TMPDIR
    $AMBERHOME/bin/pmemd.cuda -O -i md5.in -o md5.out -p a3b_apo_5td5.top -c md4.rst -r md5.rst -x md5.nc
    
    # # Copy your files back. Double-check your path below is correct.
    cp * $HOME/a3b_benchmark/
    
    

Submit your script with the command line below: 

qsub submission_script_file_name 

### Amber on Amaro Hopper GPU nodes v2[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=23> "Edit section: Amber on Amaro Hopper GPU nodes v2")]

Updated 3/23/21 by Christian. This is a script from Robert Konecny for running Amber on the Hopper TSCC GPU nodes. With this script, all the files will stay on scratch, and thus be inaccessible to the user, until the job finishes. If the job does not finish and copy back all of your files from scratch by the time you reach your wallclock limit, your files will be lost. This version should be marginally faster than v3, but the downside is that you cannot check the progress of your simulation. In practice, it seems sometimes the simulation may not run on hopper but the job will continue, so being able to see the job progress through the mdinfo or mdout file is valuable. Thus, I would recommend using v3 for amber on hopper. 
    
    
    #!/bin/bash
    #
    # rok Last modified: 2021-02-19 14:20:20
    #
    #PBS -A amaro-hopper
    #PBS -q home-hopper
    #PBS -l nodes=1:ppn=4:gpu3090
    #PBS -l walltime=216:00:00
    #PBS -N amber-hopper
    #PBS -o pbs-${PBS_JOBID}.out
    #PBS -e pbs-${PBS_JOBID}.err
    #PBS -V
    #
    
    set -xv
    
    # function to copy files back from /scratch to initial directory
    copy_back() {
        rsync -av $TMPDIR $PBS_O_WORKDIR/
    }
    
    # create a bash function which will do the cleanup (file copying) if the 
    # job is killed due to exceeding the wallclock
    exit_cleanup() {
        echo "This job was killed by PBS on" `date`
        echo "Copying files back after job cancellation ..."
        while true ; do
            sleep 5
            echo "Trying rsync ... "
            copy_back
            if [ $? -eq 0 ] ; then break ; fi
        done
        echo "Finished cleanup on" `date`
        exit 0
    }
    
    # catch SIGTERM and do clean up
    trap exit_cleanup SIGTERM
    
    echo "Started on" `date`
    
    # copy input files from current dir ($PBS_O_WORKDIR) to /scratch ($TMPDIR)
    rsync -av $PBS_O_WORKDIR/* $TMPDIR/
    
    cd $TMPDIR
    
    echo "Using $PBS_NUM_PPN CPU cores."
    source /home/ux453813/pkg/amber20/amber-cuda.sh
    
    $AMBERHOME/bin/pmemd.cuda -O -i prod.in -p MOL_solv.prmtop -c MOL_solv_prod.rst -r prod1.rst -x prod1.nc
    
    echo "Finished on" `date`
    echo "Copying files back after job's normal termination ..."
    copy_back
    

### Amber on Amaro Hopper GPU nodes v3[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=24> "Edit section: Amber on Amaro Hopper GPU nodes v3")]

Updated 3/23/21 by Christian. This is an updated script to run Amber on the Hopper TSCC GPU nodes. Importantly, this script will copy back all files except for the .nc trajectory file. This caused a slowdown for my system, from ~8.5 ns/day to ~8.2 ns/day (~3% decrease) but I believe being able to check on the progress of your simulation is worth the slowdown. This is the version of the amber script I would recommend using. 
    
    
    #!/bin/bash
    #
    # rok Last modified: 2021-02-19 14:20:20
    #
    #PBS -A amaro-hopper
    #PBS -q home-hopper
    #PBS -l nodes=1:ppn=4:gpu3090
    #PBS -l walltime=180:00:00
    #PBS -N amber-hopper
    #PBS -o pbs-${PBS_JOBID}.out
    #PBS -e pbs-${PBS_JOBID}.err
    #PBS -V
    #
    
    set -xv
    
    # function to copy files back from /scratch to initial directory
    copy_back() {
        rsync -av $TMPDIR/cmd.nc $PBS_O_WORKDIR/
    }
    
    # create a bash function which will do the cleanup (file copying) if the 
    # job is killed due to exceeding the wallclock
    exit_cleanup() {
        echo "This job was killed by PBS on" `date`
        echo "Copying files back after job cancellation ..."
        while true ; do
            sleep 5
            echo "Trying rsync ... "
            copy_back
            if [ $? -eq 0 ] ; then break ; fi
        done
        echo "Finished cleanup on" `date`
        exit 0
    }
    
    # catch SIGTERM and do clean up
    trap exit_cleanup SIGTERM
    
    echo "Started on" `date`
    
    # copy input files from current dir ($PBS_O_WORKDIR) to /scratch ($TMPDIR)
    #rsync -av $PBS_O_WORKDIR/* $TMPDIR/
    
    #cd $TMPDIR
    
    echo "Using $PBS_NUM_PPN CPU cores."
    source /home/ux453813/pkg/amber20/amber-cuda.sh
    
    cd $PBS_O_WORKDIR
    
    $AMBERHOME/bin/pmemd.cuda -O -i prod.in -p MOL_solv.prmtop -c MOL_solv_prod.rst -r prod1.rst -x $TMPDIR/prod1.nc
    
    echo "Finished on" `date`
    echo "Copying files back after job's normal termination ..."
    copy_back
    

### Schrodinger Glide HTVS on hopper[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=25> "Edit section: Schrodinger Glide HTVS on hopper")]

Updated 4/20/22 by Christian. You should have the processors and localhost be the same number. The njobs is how many jobs to split your docking into, so this should be 2-4x the number of localhost/processors. Each processor will take 4 SP docking licenses (210 available), 1 Glide Main license (75 available), and 4 Glide suite licenses (180 available). Since other people are using Glide as well, I would not recommend over 40 processors at a time; the maximum allowed amount if no other users are using Glide is nominally 52 processors but in practice seems to be 44. The SCHRODINGER_TMPDIR should be set to somewhere in your Oasis scratch space. 

You can check the available tokens with this: 
    
    
    
    $SCHRODINGER/licadmin STAT
    
    

and how many tokens each process takes with this 
    
    
    
    $SCHRODINGER/utilities/licutil -jobs
    
    
    
    
    
    #!/bin/bash
    #PBS -A amaro-hopper
    #PBS -q home-hopper
    #PBS -l nodes=1:ppn=40:ib
    #PBS -l walltime=270:00:00
    #PBS -N htvs1
    #PBS -o pbs-${PBS_JOBID}.out
    #PBS -e pbs-${PBS_JOBID}.err
    #PBS -V
    #
    
    set -xv
    
    export SCHRODINGER=/home/ux453813/pkg/schrodinger2021-1
    export SCHRODINGER_TMPDIR=/oasis/tscc/scratch/cseitz/docking/mpro/enamine/htvs
    
    cd ${PBS_O_WORKDIR}
    "${SCHRODINGER}/glide" -WAIT glide-dock_HTVS_1.in -OVERWRITE -adjust -HOST localhost:40 -NJOBS 40 -NOLOCAL
    
    
    

### Schrodinger Glide IFD on hopper[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=26> "Edit section: Schrodinger Glide IFD on hopper")]

Updated 4/20/22 by Christian. You should have the processors, Glide CPU and Prime CPU be the same number. We only have a large enough license for the Amaro, McCammon and Gilson groups to be doing 3 IFD jobs at a time. This means one person can use 3 Prime CPUs, three different people can each use 1 Prime CPU etc. You can slightly speed things up by requesting more processors and more glide CPUs for the glide docking at the end of an IFD job as we have more of those available, but you cannot request more Prime CPUs. Note: each processor uses 8 Glide suite and 8 PSP_PLOP licenses (30 available for each), it does not use SP or XP docking licenses. Also, set the SCHRODINGER_TMPDIR to be somewhere in your Oasis scratch space. You shouldn't run more than maybe 30 ligands per IFD job as this will become too large and apparently cause the memory to crash. By 30 ligands I mean 30 unique structures that you put through ligprep, which will turn into ~1000 conformations to be run through IFD. 

You can check the available tokens with this: 
    
    
    
    $SCHRODINGER/licadmin STAT
    
    

and how many tokens each process takes with this 
    
    
    
    $SCHRODINGER/utilities/licutil -jobs
    
    
    
    
    
    #!/bin/bash
    #PBS -A amaro-hopper
    #PBS -q home-hopper
    #PBS -l nodes=1:ppn=8:ib
    #PBS -l walltime=270:00:00
    #PBS -N ifd1
    #PBS -o pbs-${PBS_JOBID}.out
    #PBS -e pbs-${PBS_JOBID}.err
    #PBS -V
    #
    
    set -xv
    
    export SCHRODINGER=/home/ux453813/pkg/schrodinger2021-1
    export SCHRODINGER_TMPDIR=/oasis/tscc/scratch/cseitz/vedran/active_site_IFD/6LU7_dimer_apo_top_A_71/ifd
    
    cd ${PBS_O_WORKDIR}
    "${SCHRODINGER}/ifd" -WAIT -NGLIDECPU 8 -NPRIMECPU 3 InducedFit_1.inp -NOLOCAL -HOST localhost -SUBHOST localhost -TMPLAUNCHDIR
    
    

## TSCC[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=27> "Edit section: TSCC")]

### NAMD GPU on TSCC[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=28> "Edit section: NAMD GPU on TSCC")]

Updated 10/20/20 by Christian. Here are two sample scripts to run NAMD GPU on TSCC. To run 1 GPU, you MUST request as shown here (1 node, 3 ppn) otherwise you will really mess up the nodes ([as described here](<https://www.sdsc.edu/support/user_guides/tscc.html>)). This uses the pbs system, so submit the job as qsub namd.pbs or whatever you want to call it. You have two options to run your system, depending on the file size you will encounter. The first script is for smaller file sizes, and is faster. This is because it uses the $TMPDIR, which is fast. It is a local directory on a compute node, which does not have a file quota but does have a size limit of ~200 GB. This should be run from your home directory. It will copy your files onto a compute node, run them, and return them. The cuda visible devices is needed so that if there is a problem with one GPU on the node, your job can be directed to a working GPU on the node. 
    
    
    
    #!/bin/bash
    #PBS -q home-mccammon
    #PBS -N 08-rep3
    #PBS -l nodes=1:ppn=3:gpu
    #PBS -l walltime=48:00:00
    #PBS -o prod1.out
    #PBS -V
    #PBS -A mccammon-gpu
    
    module load namd/2.13
    
    current_dir='pwd'
    cp * $TMPDIR
    cd $TMPDIR
    
    export CUDA_VISIBLE_DEVICES=0,1,2,3
    
    namd2.cuda +idlepoll +p3 +devices 0 prod1.conf > prod1.log
    
    cp * $current_dir
    
    

If you need more space than this, than use this script, which runs on oasis. This should be run from your directory on oasis. NOTE: Oasis gets purged 90 days after starting on it and does not get backed up so please remove all your files within 90 days. Importantly, the qsub will always revert back to your home directory to start. That means you need to put in the cd <path-to-directory> to get to your working directory with all your files, configuration file, protein structure file, etc as has been done in this script. 
    
    
    
    #!/bin/bash
    #PBS -q home-mccammon
    #PBS -N 08-rep3
    #PBS -l nodes=1:ppn=3:gpu
    #PBS -l walltime=48:00:00
    #PBS -o prod1.out
    #PBS -V
    #PBS -A mccammon-gpu
    
    module load namd/2.13
    
    cd /oasis/tscc/scratch/cseitz/kevin/08_MET87_ALA/rep3
    
    export CUDA_VISIBLE_DEVICES=0,1,2,3
    
    namd2.cuda +idlepoll +p3 +devices 0 prod1.conf > prod1.log
    
    

  


## Expanse[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=29> "Edit section: Expanse")]

### Interactive CPU node on Expanse[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=30> "Edit section: Interactive CPU node on Expanse")]
    
    
    srun --partition=debug  --pty --account=csd373 --nodes=1 --ntasks-per-node=10 --mem=96G -t 00:30:00 --wait=0 --export=ALL /bin/bash
    

### Interative GPU node on Expanse[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=31> "Edit section: Interative GPU node on Expanse")]
    
    
    srun --partition=gpu-shared  --pty --account=csd373 --nodes=1 --ntasks-per-node=10 --mem=95G --gpus=1  -t 00:30:00 --wait=0 --export=ALL /bin/bash
    

### NAMD GPU on Expanse[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=32> "Edit section: NAMD GPU on Expanse")]

Updated 7/6/2023 by Lane and previously 12/17/20 by Christian. After logging onto expanse, more examples can be found at /cm/shared/examples/sdsc. Note: NAMD2.13 or NAMD2.14 is not properly installed on Expanse. One can download it from [here](<https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=NAMD>) and downloaded the "Version 2.13 (2018-11-09) or version 2.14 Platforms: Linux-x86_64-multicore-CUDA". Then one can put it in one's home directory and [added it to one's path](<https://linuxize.com/post/how-to-add-directory-to-path-in-linux/>). 
    
    
    
    #!/usr/bin/env bash
    
    #SBATCH --job-name=JOB_NAME_HERE
    #SBATCH --account=csd373
    #SBATCH --partition=gpu-shared
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=10
    #SBATCH --mem=50G
    #SBATCH --gpus=1
    #SBATCH --time=48:00:00
    #SBATCH --output=prod1.log
    
    # Make sure to ALWAYS use input/output from the scratch directory
    SCRATCH_DIR="/expanse/lustre/scratch/username/temp_project/
    cd SCRATCH_DIR
     
    /path/to/installed/namd2 +p10 +idlepoll +devices 0 namd_script.namd
    

### AMBER on Expanse GPU[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=33> "Edit section: AMBER on Expanse GPU")]

Updated on July 6 2023 by Lane Votapka. 
    
    
    #!/bin/bash
    #SBATCH --job-name="amber_job_name"
    #SBATCH --output="amberjob.%j.%N.out"
    #SBATCH --partition=gpu-shared
    #SBATCH --nodes=1
    #SBATCH --gpus=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --mem=50G
    #SBATCH --account=csd373
    #SBATCH --no-requeue
    #SBATCH -t 48:00:00
    
    module purge
    module load cpu/0.15.4
    module load gcc/10.2.0
    module load mvapich2/2.3.6
    module load gpu/0.15.4
    module load slurm
    module load openmpi/4.0.4		
    module load amber
    pmemd.cuda -O -i mdin.GPU -o mdout-OneGPU.$SLURM_JOBID -p prmtop -c inpcrd
    

### SEEKR2 on Expanse GPU[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=34> "Edit section: SEEKR2 on Expanse GPU")]

Update on Oct 12 2022 by Lane Votapka. This will run 4 SEEKR2 jobs concurrently on a 4-GPU node. 
    
    
    #!/bin/bash
    #SBATCH --job-name="compound22_0_1_2_3"
    #SBATCH --output="compound22_0_1_2_3.%j.%N.out"
    #SBATCH --partition=gpu
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=4
    #SBATCH --gpus=4
    #SBATCH --mem=374G
    #SBATCH --account=csd373
    #SBATCH --no-requeue
    #SBATCH -t 24:00:00
    
    module purge
    module load gpu/0.15.4
    module load slurm
    module load cuda/11.0.2
    
    export OPENMM_CUDA_COMPILER=`which nvcc`
    
    SEEKR_DIR="/home/lvotapka/seekr2/seekr2"
    PROJECT_ROOT_DIR="/expanse/lustre/scratch/lvotapka/temp_project/hsp90_wade/compound22"
    
    python $SEEKR_DIR/run.py 0 $PROJECT_ROOT_DIR/model.xml -c 0 &
    python $SEEKR_DIR/run.py 1 $PROJECT_ROOT_DIR/model.xml -c 1 &
    python $SEEKR_DIR/run.py 2 $PROJECT_ROOT_DIR/model.xml -c 2 &
    python $SEEKR_DIR/run.py 3 $PROJECT_ROOT_DIR/model.xml -c 3 &
    wait 
    
    

## Anvil[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=35> "Edit section: Anvil")]

### Interactive GPU node on Anvil[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=36> "Edit section: Interactive GPU node on Anvil")]
    
    
    sinteractive --partition=gpu-debug --gres gpu:1 --nodes=1 --ntasks-per-node=1 --gpus-per-node=1 -t 00:30:00 --wait=0 -A che060063-gpu
    

### SEEKR2 on Anvil[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=37> "Edit section: SEEKR2 on Anvil")]

Update on Feb 16 2022 by Lane Votapka. This will run 4 SEEKR2 jobs concurrently on a 4-GPU node. 
    
    
    #!/bin/bash
    #SBATCH --job-name="c9_e5_0"
    #SBATCH --output="c9_e5_0.%j.%N.out"
    #SBATCH --partition=gpu
    #SBATCH --gres gpu:4
    #SBATCH --gpus-per-node=4
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=4
    #SBATCH --no-requeue
    #SBATCH -t 40:00:00
    #SBATCH --export=ALL
    #SBATCH -A che060063-gpu
    
    module load modtree/gpu
    
    export OPENMM_CUDA_COMPILER=`which nvcc`
    
    SEEKR_DIR="$HOME/seekr2/seekr2"
    SEEKRTOOLS_DIR="$HOME/seekrtools/seekrtools"
    EXPERIMENT_NAME="six_compounds_exp5"
    COMPOUND_NAME="compound_9"
    PROJECT_ROOT_DIR="/anvil/scratch/x-lvotapka/hsp90_wade/$EXPERIMENT_NAME/roots/$COMPOUND_NAME/"
    
    python $SEEKR_DIR/run.py 0 $PROJECT_ROOT_DIR/model.xml -c 0 &
    python $SEEKR_DIR/run.py 1 $PROJECT_ROOT_DIR/model.xml -c 1 &
    python $SEEKR_DIR/run.py 2 $PROJECT_ROOT_DIR/model.xml -c 2 &
    python $SEEKR_DIR/run.py 3 $PROJECT_ROOT_DIR/model.xml -c 3 &
    wait
    
    sleep 60
    
    

## Delta[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=38> "Edit section: Delta")]

Access to NCSA Delta must be set up by opening a ticket using the [ticket link](<https://support.access-ci.org/open-a-ticket>) Make sure you activate DUO authentication 

Upon activating your account, changing your password, and activating DUO authentication, you may log into NCSA Delta by running the following command and approving the log-in with DUO: 
    
    
     username@dt-login01.delta.ncsa.illinois.edu
    

The location of your home directory is not the best place to run your jobs, but you can store your files and software there 
    
    
     /u/username
    

Your jobs should be run from the group account (kif) scratch directory: 
    
    
     /scratch/kif/
    

Delta uses a SLURM scheduler. The following are the most important commands you should know 

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

### Interactive GPU node on Delta[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=39> "Edit section: Interactive GPU node on Delta")]
    
    
    srun --account=kif-delta-gpu --partition=gpuA40x4-interactive   --nodes=1 --gpus-per-node=1 --tasks=1   --tasks-per-node=1 --cpus-per-task=1 --mem=20g   --pty bash
    

### AMBER GPU on Delta[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=40> "Edit section: AMBER GPU on Delta")]

Updated Jan 2023 by LWV 

Amber22 GPU can be run on NCSA Delta using the following submission script as a template: 
    
    
     #!/bin/bash
     #SBATCH --job-name=yourJobName
     #SBATCH --output=yourJobName.out
     #SBATCH --error=yourJobName.err
     #SBATCH --partition=gpuA100x4
     #SBATCH --mem=55G
     #SBATCH --nodes=1
     #SBATCH --ntasks-per-node=1  
     #SBATCH --cpus-per-task=16   
     #SBATCH --constraint="scratch"
     #SBATCH --gpus-per-node=1
     #SBATCH --gpu-bind=closest  
     #SBATCH --account=kif-delta-gpu #Our account name
     #SBATCH --no-requeue
     #SBATCH -t 24:00:00
     
     module load nccl
     source /projects/kif/software/amber/amber22/amber.sh
     
     DIR="/scratch/kif/username/your/path/here"
     #Running Production MD
     $AMBERHOME/bin/pmemd.cuda -O -i $DIR/md5.in -o $DIR/md5.out -p $DIR/system.top -c $DIR/md4.rst -ref $DIR/md4.rst -r $DIR/md5.rst -x $DIR/md5.nc
     
     
     # Exit from script
     exit 0
    

### SEEKR2 on Delta[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=41> "Edit section: SEEKR2 on Delta")]

Update on Oct 12 2022 by Lane Votapka. This will run 4 SEEKR2 jobs concurrently on a 4-GPU node. It assumes that a conda environment named SEEKR3 exists. 
    
    
    #!/bin/bash
    #SBATCH --job-name="tryp_ben_1"
    #SBATCH --output="tryp_ben_1.%j.%N.out"
    #SBATCH --partition=gpuA100x4
    #SBATCH --mem=220G
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=4
    #SBATCH --cpus-per-task=16   # spread out to use 1 core per numa
    #SBATCH --constraint="scratch"
    #SBATCH --gpus-per-node=4
    #SBATCH --gpu-bind=closest   # select a cpu close to gpu on pci bus topology
    #SBATCH --account=kif-delta-gpu
    #SBATCH --exclusive  # dedicated node for this job
    #SBATCH --requeue # SEEKR can pick right up where it left off
    #SBATCH -t 12:00:00
    
    source $HOME/.bashrc
    conda activate SEEKR3
    export OPENMM_CUDA_COMPILER=`which nvcc`
    SEEKR_DIR="$HOME/seekr2/seekr2"
    PROJECT_ROOT_DIR="/scratch/kif/lvotapka/tryp_ben_mmvt_seekr2_many_frames"
    
    python $SEEKR_DIR/run.py 0 $PROJECT_ROOT_DIR/model.xml -c 0 &
    python $SEEKR_DIR/run.py 1 $PROJECT_ROOT_DIR/model.xml -c 1 &
    python $SEEKR_DIR/run.py 2 $PROJECT_ROOT_DIR/model.xml -c 2 &
    python $SEEKR_DIR/run.py 3 $PROJECT_ROOT_DIR/model.xml -c 3 &
    wait
    
    sleep 60
    
    

## Bridges2[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=42> "Edit section: Bridges2")]

### Interactive GPU node on Bridges2[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=43> "Edit section: Interactive GPU node on Bridges2")]
    
    
    interact -p GPU-shared -t 30:00 -N 1 --gres=gpu:v100-32:1
    

### SEEKR2 on Bridges2[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=44> "Edit section: SEEKR2 on Bridges2")]

Edited by Lane on July 6 2023. This script assumes that a conda environment named "SEEKR" has been created. 
    
    
    #!/bin/bash
    #SBATCH --job-name="cmp17_0_7"
    #SBATCH --output="cmp17_0_7.%j.%N.out"
    #SBATCH --partition=GPU
    #SBATCH --gres=gpu:v100-32:8
    #SBATCH --nodes=1
    #SBATCH -t 23:30:00
    
    date
    conda activate SEEKR
    module load cuda
    export OPENMM_CUDA_COMPILER=`which nvcc`
    
    SEEKR_DIR="$HOME/seekr2/seekr2"
    SEEKRTOOLS_DIR="$HOME/seekrtools/seekrtools/"
    PROJECT_ROOT_DIR="$PROJECT/ten_compounds/roots/compound17"
    
    python $SEEKR_DIR/run.py 0 $PROJECT_ROOT_DIR/model.xml -c 0 &
    python $SEEKR_DIR/run.py 1 $PROJECT_ROOT_DIR/model.xml -c 1 &
    python $SEEKR_DIR/run.py 2 $PROJECT_ROOT_DIR/model.xml -c 2 &
    python $SEEKR_DIR/run.py 3 $PROJECT_ROOT_DIR/model.xml -c 3 &
    python $SEEKR_DIR/run.py 4 $PROJECT_ROOT_DIR/model.xml -c 4 &
    python $SEEKR_DIR/run.py 5 $PROJECT_ROOT_DIR/model.xml -c 5 &
    python $SEEKR_DIR/run.py 6 $PROJECT_ROOT_DIR/model.xml -c 6 &
    python $SEEKR_DIR/run.py 7 $PROJECT_ROOT_DIR/model.xml -c 7 &
    wait
    
    

## Archiving Data[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=45> "Edit section: Archiving Data")]

### Backing up to Ranch[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=46> "Edit section: Backing up to Ranch")]

Ranch is a teragrid utility for storing massive amounts of data in archive. This is intended to be a cursory description. Click here for the [[Ranch User's Guide](<http://services.tacc.utexas.edu/index.php/ranch-user-guide%7CFull>)]. 

To log into Ranch from your account on Ranger, enter this command: 
    
    
    login3$: ssh $ARCHIVER
    

To copy files from Ranger to Ranch, type this: 
    
    
    login3$: rsync -ruvzpDlth filename $ARCHIVER:$ARCHIVE/newfilename
    

Remember that the argument -r will copy entire directories! 

To log into Ranch from any other machine, type this: 
    
    
    $: ssh yourusername@ranch.tacc.utexas.edu
    

and enter your password. 

Since my username is "lvotapka", I would type: lvotapka@ranch.tacc.utexas.edu 

To transfer files to Ranch from another machine, here's an example of what I would type: 
    
    
    $ scp filename lvotapka@ranch.tacc.utexas.edu:/home3/01624/lvotapka/newfilename
    

Of course, your login name, filenames, and destination directory will be different. Simply login to Ranch and type "pwd" to find out your destination directory. 

### Staging[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=47> "Edit section: Staging")]

Ranch will sometimes write your files from the disk to a tape, especially if they haven't been accessed in awhile. You must 'stage' such data. 

To see which data has been placed onto the tape, type: 
    
    
    $ sls
    

If you see a big "O" at the first character spot below the name, then the file has been placed on the tape. Whereas a regular "-" means that it has not been placed on the tape. 

Use the "stage" command to prepare a file for retrieval: 
    
    
    $ stage filename
    

## Comet (Deprecated)[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=48> "Edit section: Comet \(Deprecated\)")]

### Running on Comet[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=49> "Edit section: Running on Comet")]

We have ~500 GB of storage for our entire project allocation. Each of our users has 100 GB of storage in their home directory, and ~10 TB storage in the scratch directory. The home directory is backed up, but the project and scratch directories are not. Thus, here is how to run these jobs: 

Run jobs from the /oasis/scratch/comet location. Just make sure you don't leave data sitting there for the long term since Comet needs to keep space available for scratch usage. Typically this is what I would suggest: 

[1] Run simulations from the Lustre scratch location (/oasis/scratch/comet/$USER/temp_project) 

[2] Complete any post-processing you need to do in the same location. 

As long as (1) and (2) are ongoing you can keep your data in the location. Once (1) and (2) are done: 

(3) Copy any files you would need online for the remainder of your allocation period to the Lustre projects area (/oasis/projects/nsf location). For example if some of the results may be needed for some other analysis in this project at a later date. 

(4) Make an offsite copy of any important data in both Lustre locations. Both /oasis/scratch/comet and /oasis/projects/nsf are *not* backed up. So it is critical you make copies of important datasets elsewhere. 

(5) Delete the files in /oasis/scratch/comet once they are no longer needed. 

### Gaussian on Comet GPU[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=50> "Edit section: Gaussian on Comet GPU")]

Updated 7/26/20 by Christian. This is for running Gaussian on Comet GPU, but you can also run Gaussian on Comet CPU, you would just need a different script for that. 
    
    
    
    #!/bin/bash
    #SBATCH --job-name="2NN"
    #SBATCH --output="2NN_energy2.%j.%N.out"
    #SBATCH --partition=gpu-shared
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=18
    #SBATCH --gres=gpu:3
    #SBATCH --export=ALL
    #SBATCH -t 48:00:00
    #SBATCH --no-requeue
    filename=hemedquintet_nop_nowat_energy.com
    export MODULEPATH=/share/apps/compute/modulefiles/applications:$MODULEPATH
    export GAUSS_SCRDIR=/scratch/$USER/$SLURM_JOBID
    module load gaussian/16.C.01
    exe=`which g16`
    bash /share/apps/examples/gaussian/16_revC_cpu/getcpusets $$
    cat $$.out $filename >file.tmp.$$
    /usr/bin/time $exe < file.tmp.$$ > hemedquintet_nop_nowat_energy.out
    rm -f $$.out file.tmp.$$
    
    

### Gaussian on Comet[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=51> "Edit section: Gaussian on Comet")]

Updated 1/6/21 by Christian. 
    
    
    
    #!/bin/bash
    #SBATCH --job-name="andyfreqdn"
    #SBATCH --output="gauss.%j.%N.out"
    #SBATCH --partition=compute
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=24
    #SBATCH --export=ALL
    #SBATCH -t 48:00:00
    filename=MOL_small_fc.com
    export MODULEPATH=/share/apps/compute/modulefiles/applications:$MODULEPATH
    export GAUSS_SCRDIR=/scratch/$USER/$SLURM_JOBID
    module load gaussian/16.C.01
    exe=`which g16`
    bash /share/apps/examples/gaussian/16_revC_cpu/getcpusets $$
    cat $$.out $filename >file.tmp.$$
    /usr/bin/time $exe < file.tmp.$$ > MOL_small_fc.out
    rm -f $$.out file.tmp.$$
    
    

### AMBER on Comet[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=52> "Edit section: AMBER on Comet")]

Updated 4/15/2020 by Christian. Find more examples for Comet under /share/apps/examples on Comet. I have not tested this, but it may be faster to use pmemd.cuda instead of pmemd.cuda.MPI since this is a single GPU job...This script is for running on 1 GPU on Comet, under the shared GPU partition. This is what you should change to fit your own system: 

  
rep1 

continueMD.in 

step3_charmm2amber.parm7 

run4/step5_production4.rst 

run5/step5_production5.rst 

run5/step5_production5.nc 

run5 

If you wish to use p100 GPUs instead of k80s, then change that too. Here is what the flags mean: 

-i this is your input script for AMBER. It should say how many steps you are running, what temperature, etc. 

-p this is your initial coordinate file, it is the same thing as a .prmtop. It should come from before your minimization and equilibration. Once you put in your initial coordinate file, do not change it during the course of your simulations. 

-c this is your input restart file. It should either come from your equilibration or your previous MD simulations on Comet. 

-r this is your output restart file. 

-x this is your output trajectory file. 

-o this is your output log file. 

I direct my inputs and outputs from specific directories, hence the run4 and run5 below. You can choose to do this or keep everything in one directory. 

You also need to run your simulations in the right place. Please do not run any simulations on the head node. I run my simulations under 
    
    
    
    /oasis/projects/nsf/csd373/cseitz/
    
    

You would change csd373 to the current XSEDE allocation, and then use your own username. Save the script below as a .sb file, and run with sbatch yourscript.sb, where yourscript is the name you gave to it. 
    
    
    
    #!/bin/bash
    #SBATCH --nodes=1
    #SBATCH --tasks-per-node=6
    #SBATCH -t 48:00:00
    #SBATCH -o test.%j.%N.out
    #SBATCH --gres=gpu:k80:1
    #SBATCH --job-name="rep1"
    #SBATCH -p gpu-shared
    #SBATCH --export=ALL
    module purge
    module load amber
    module load cuda
    mpirun -np 6 pmemd.cuda.MPI -O -i continueMD.in -p step3_charmm2amber.parm7 -c run4/step5_production4.rst -r run5/step5_production5.rst -x run5/step5_production5.nc -o run5/log.$SLURM_JOB_ID.out
    
    

### NAMD GPU on Comet[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=53> "Edit section: NAMD GPU on Comet")]

Updated 7/26/20 by Christian. This is for running NAMD GPU using 1 GPU on Comet, using more GPUs doesn't seem to change performance. However, p100 GPUs seem to give much better performance than k80 GPUs, without much of a difference in queue time. If you want to run multiple GPUs, you need to add the +setcpuaffinity tag after +p7, and add GPUs to the +devices (for example, using four GPUs would be +devices 0,1,2,3). 
    
    
    #!/usr/bin/env bash
    
    #SBATCH --job-name=06-rep1
    #SBATCH --partition=gpu-shared
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=7
    #SBATCH --cpus-per-task=1
    #SBATCH --gres=gpu:p100:1
    #SBATCH --time=48:00:00
    #SBATCH --output=prod2.log
    
    module purge
    module load namd/2.13
    module load cuda/10.1
    module list
    printenv
    
    time -p namd2.cuda +p7 +devices 0 prod2.conf
    

### NAMD on Stampede[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=54> "Edit section: NAMD on Stampede")]

Be sure to change the job name, output and error file names, and the account number below. 
    
    
    #!/bin/bash
    #SBATCH -J HA_run_1        # Job Name
    #SBATCH -o HA_run_1.o%j    # Output and error file name (%j expands to jobID)
    #SBATCH -e free_run_1.e%j
    #SBATCH -n 4096           # Total number of mpi tasks requested
    #SBATCH -p normal  # Queue (partition) name -- normal, development, etc.
    #SBATCH -t 24:00:00     # Run time (hh:mm:ss) - 1.5 hours
    #SBATCH -A TG-CHE060073N
    
    module load namd
    
    export VIADEV_RENDEZVOUS_THRESHOLD=50000
    
    ibrun namd2 system-eq.namd > system-eq.namd.out
    

### GROMACS on Comet[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=55> "Edit section: GROMACS on Comet")]

Updated 10/10/2020 by Christian. Here is a sample script of running GROMACS 2018. Be careful with the balance between the -resetstep and the -nsteps. I had a bunch of problems with load balancing if I got the balance wrong? Someone who uses GROMACS more would have a better idea of what to do here, but this script worked for me. 
    
    
    
    #!/usr/bin/env bash
                                                                                                           
    #SBATCH --job-name=gromacs-gpu-shared                                                                                   
    #SBATCH --account=csd373
    #SBATCH --partition=gpu-shared
    #SBATCH --nodes=1                                                                                                       
    #SBATCH --ntasks-per-node=6
    #SBATCH --gres=gpu:1
    #SBATCH --time=00:05:00
    #SBATCH --output=gromacs-gpu-shared.o%j.%N
    
    module purge
    export MODULEPATH="/share/apps/compute/modulefiles/applications:${MODULEPATH}"
    module load gromacs
    module list
    source "${GROMACSHOME}/bin/GMXRC"
    printenv
    
    time -p mpirun -np 1 gmx_mpi grompp -f gromacs/step5_production.mdp -o gromacs/step5_production1.tpr -c gromacs/step4.1_equilibration.gro -p gromacs/topol.top -po gromacs/mdout.mdp
    time -p mpirun gmx_mpi mdrun -nb gpu -pin on -resethway -noconfout -resetstep 5000 -nsteps 8000 -cpo state.cpt -e ener.edr -g md.log -v -s gromacs/step5_production1.tpr
    
    

-f This is the run parameters file (.mdp) 

-o This is the output (or perhaps input?) structure/mass file, which is also an input file (.tpr) 

-c This is the configuration file (.conf) 

-p This is the topology file (.top) 

-po This is the output run parameters file (.mdp) 

-cpr This is the output checkpoint file (cpt) 

-e This is the output portable energy file (edr) 

-g This is the output log file with the run outputs (different from the md outputs) 

-s This is the output structure/mass file (.tpr) 

## Bridges (Deprecated)[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=56> "Edit section: Bridges \(Deprecated\)")]

### NAMD on Bridges[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=57> "Edit section: NAMD on Bridges")]

Here is a sample script of running NAMD 2.10 using 80 nodes, 27 processors per node. There are 28 processors per node in Bridges, but I found that leaving one processor out actually work better. If you use up all processor and leave none for operation, it actually drastically decrease the processing speed. 
    
    
    #!/bin/bash
    #SBATCH -N 80 --tasks-per-node=27
    #SBATCH -t 48:00:00
    #
    # Setup the module command
    set echo
    set -x 
    source /usr/share/Modules/init/bash
    # Load the needed modules
    module load fftw3
    #
    
    cd $SLURM_SUBMIT_DIR
    echo "$SLURM_NPROCS=" $SLURM_NPROCS
    export BINDIR=/opt/packages/namd_mpi/Linux-x86_64-MPI
    
    mpirun -np $SLURM_NPROCS $BINDIR/namd2 +pemap 0-27 md1_eq.in > md1_eq.log
    mpirun -np $SLURM_NPROCS $BINDIR/namd2 +pemap 0-27 md2_eq.in > md2_eq.log
    mpirun -np $SLURM_NPROCS $BINDIR/namd2 +pemap 0-27 md3_eq.in > md3_eq.log
    mpirun -np $SLURM_NPROCS $BINDIR/namd2 +pemap 0-27 md4_eq.in > md4_eq.log
    mpirun -np $SLURM_NPROCS $BINDIR/namd2 +pemap 0-27 md5_new.in > md5_new.log
    

### NAMD GPU on Bridges[edit](</mediawiki/index.php?title=SuperComputing&action=edit&section=58> "Edit section: NAMD GPU on Bridges")]

Updated 9/20/20 by Christian. Here is a sample script to run NAMD GPU on Bridges. I have found occasional segmentation faults though so there could be an error with this (maybe in the number of CPUs requested?). 
    
    
    
    #!/bin/bash
    #SBATCH --job-name="02-rep3"
    #SBATCH --output="prod1.out"
    #SBATCH -N 1
    #SBATCH -p GPU-shared
    #SBATCH --tasks-per-node=32
    #SBATCH -t 47:00:00
    #SBATCH --gres=gpu:p100:1
    
    #set the module command
    set echo
    set -x
    
    #load the module
    module load namd/2.13_gpu
    
    cd $SLURM_SUBMIT_DIR
    nvidia-smi
    
    $BINDIR/namd2 +p $SLURM_NPROCS +pemap 0-15+16 prod1.conf >prod1.log
