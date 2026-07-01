# SEEKR submission scripts page

This page contains scripts that may be used to submit SEEKR jobs to some common computing resources. 

## Getting Started[edit](</mediawiki/index.php?title=SEEKR_submission_scripts_page&action=edit&section=1> "Edit section: Getting Started")]

Presumably, you've locally run the preparation stage of your SEEKR calculation (for instance, the prepare_1d_spherical.py script). 

Let us assume that your SEEKR root directory is named "my_seekr_project", which contains your model.xml file and your anchor directories. 

Now, you need to create a tarball of your project: 
    
    
    tar -czf my_seekr_project.tgz my_seekr_project/
    

It is recommended that you use Globus (instead of SCP or SFTP) to transfer large files, like your SEEKR calculation tarball. (If it's not large yet, it soon will be). 

[How to Install and Use Globus](</mediawiki/index.php/Globus> "Globus")

Once the transfer is complete, you can untar your project on the supercomputer or cluster: 
    
    
    tar -xzf my_seekr_project.tgz
    

## Expanse Interactive Shell[edit](</mediawiki/index.php?title=SEEKR_submission_scripts_page&action=edit&section=2> "Edit section: Expanse Interactive Shell")]
    
    
    srun --partition=gpu-debug  --pty --account=csd373 --nodes=1 --ntasks-per-node=10 --mem=96G --gpus=1  -t 00:30:00 --wait=0 --export=ALL /bin/bash
    

## Expanse Submission Script[edit](</mediawiki/index.php?title=SEEKR_submission_scripts_page&action=edit&section=3> "Edit section: Expanse Submission Script")]

Assume this file is named job_script.sh 
    
    
    #!/bin/bash
    #SBATCH --job-name="my-seekr-project"
    #SBATCH --output="my-seekr-project.%j.%N.out"
    #SBATCH --partition=gpu
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=32
    #SBATCH --gpus=4
    #SBATCH --mem=374G
    #SBATCH --account=csd373
    #SBATCH --no-requeue
    #SBATCH -t 48:00:00
    
    module purge
    module load gpu
    module load slurm
    module load cuda10.2/blas/10.2.89
    module load cuda10.2/fft/10.2.89
    module load cuda10.2/nsight/10.2.89
    module load cuda10.2/profiler/10.2.89
    module load cuda10.2/toolkit/10.2.89
    
    SEEKR_DIR="/home/username/openmmvt/openmmvt"
    # Make sure your project root directory is NOT in home, but in SCRATCH or WORK
    PROJECT_ROOT_DIR="/expanse/lustre/scratch/username/temp_project/my_seekr_project"
    
    python $SEEKR_DIR/runner_openmm.py 0 $PROJECT_ROOT_DIR/model.xml -f -c 0 &
    python $SEEKR_DIR/runner_openmm.py 1 $PROJECT_ROOT_DIR/model.xml -f -c 1 &
    python $SEEKR_DIR/runner_openmm.py 2 $PROJECT_ROOT_DIR/model.xml -f -c 2 &
    python $SEEKR_DIR/runner_openmm.py 3 $PROJECT_ROOT_DIR/model.xml -f -c 3 &
    wait
    

Submission command: 
    
    
    sbatch job_script.sh
    

## TSCC Submission Script[edit](</mediawiki/index.php?title=SEEKR_submission_scripts_page&action=edit&section=4> "Edit section: TSCC Submission Script")]

Assume this file is named job_script.sh 
    
    
    #!/bin/bash
    #PBS -q home-hopper
    #PBS -N my-seekr-project
    #PBS -l nodes=1:ppn=4:gpu3090
    #PBS -l walltime=48:00:00
    #PBS -o "my-seekr-project.%j.%N.out"
    #PBS -e "my-seekr-project.%j.%N.err"
    #PBS -A amaro-hopper
    
    source  /home/ux453813/pkg/cuda.sh
    
    SEEKR_DIR="/home/username/openmmvt/openmmvt"
    # Make sure your project root directory is NOT in home, but in SCRATCH or WORK
    PROJECT_ROOT_DIR="/oasis/tscc/scratch/username/my_seekr_project"
    
    python $SEEKR_DIR/runner_openmm.py 0 $PROJECT_ROOT_DIR/model.xml -f -c 0 &
    python $SEEKR_DIR/runner_openmm.py 1 $PROJECT_ROOT_DIR/model.xml -f -c 1 &
    python $SEEKR_DIR/runner_openmm.py 2 $PROJECT_ROOT_DIR/model.xml -f -c 2 &
    python $SEEKR_DIR/runner_openmm.py 3 $PROJECT_ROOT_DIR/model.xml -f -c 3 &
    wait
    

Submission command: 
    
    
    qsub job_script.sh
