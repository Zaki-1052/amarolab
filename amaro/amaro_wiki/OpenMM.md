# OpenMM

# OpenMM[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=1> "Edit section: OpenMM")]

OpenMM is a very well-made program that we will be using to run our molecular dynamics simulations. 

## Local Installation from Conda[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=2> "Edit section: Local Installation from Conda")]

If you don't need to install from source, You can refer to OpenMM's manual for how to install using Conda: <http://docs.openmm.org/latest/userguide/application.html#installing-openmm>

### Install SEEKR from Conda[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=3> "Edit section: Install SEEKR from Conda")]

See the instructions in the SEEKR2 documentation for how to install SEEKR2 with Conda alone: <https://seekr2.readthedocs.io/en/latest/>

## Local Installation From Source[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=4> "Edit section: Local Installation From Source")]

Unfortunately, the only difficult thing about OpenMM is its installation from source. 

One may follow the official guide from OpenMM here: <http://docs.openmm.org/6.1.0/userguide/library.html>

Or, one may follow the procedure that I followed below (which is very similar): 

Download Conda from <https://conda.io/en/latest/miniconda.html>

Run the script and fill out the prompts. 

Test Conda by running: 
    
    
    which conda
    

If you want you can create a conda environment, but I just install all packages straight to the base environment. In this case, you would skip all future commands to run `source activate SEEKR`. 

See the Cuda installation section below if Cuda is not installed (You can 'ls' to directory /usr/local/ to see if Cuda8.0 is installed.) 
    
    
    conda install numpy scipy netcdf4 mpi4py swig
    

Make sure 'git' is installed. 
    
    
    conda install git
    

Make sure ccmake is installed. (You'll need sudo privileges) 
    
    
    which ccmake
    # If a path to ccmake appears, you're good and you can skip to the next step
    # If a path doesn't appear you'll have to do the following command:
    sudo apt-get install cmake-curses-gui
    

  
Make sure 'doxygen' is installed. 
    
    
    conda install -c conda-forge doxygen
    

Install Cython: 
    
    
    pip install --upgrade cython
    

Clone OpenMM and cd into OpenMM directory, then perform necessary build steps. 
    
    
    git clone https://github.com/openmm/openmm.git
    cd openmm
    mkdir build
    cd build
    ccmake ..
    

The ccmake gui should come up. Press 'c' and then 't' 

Check all the variables, and then type 'c' to configure. If there are any problems, it will let you know. 

You should modify the following variables: 

CMAKE_INSTALL_PREFIX: change to a local directory that exists (example: /home/username/bin/openmm). If such a directory doesn't exist, then make one. 

When the configuration is successful, type 'g' to generate. Then ccmake should close on its own. 

If you are having trouble with assigning a variable, like CUDA_CUDA_LIBRARY-NOTFOUND, then run 'cmake' (instead of 'ccmake') and assign the missing variable using the -D argument: 

cmake -DCMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs .. 

Next, type: 
    
    
    make -j 4
    make install
    make PythonInstall
    make test
    

If the PythonInstall step fails, then make sure you have installed cython 
    
    
    pip install --upgrade cython
    

Hopefully, with the final step, all the tests pass. If a few fail, then determine if those failures will be necessary for our calculations. If several or all fail, then you'll need to be sure that you fix whatever problem caused those failures. 

Try to see if the python interface works. Inside a python shell, try: 
    
    
    from simtk import openmm
    

### Install SEEKR2 Locally from Source[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=5> "Edit section: Install SEEKR2 Locally from Source")]

If you need to install SEEKR2 locally, you can perform the following steps (after installing OpenMM from the steps above): 
    
    
    git clone https://github.com/seekrcentral/seekr2_openmm_plugin.git
    cd seekr2_openmm_plugin/seekr2plugin
    mkdir build
    cd build
    ccmake ..
    

Now press the 'c' key. You should see the ccmake GUI appear. Modify all the variables as necessary *MAKE SURE THAT THE CMAKE_INSTALL_PREFIX AND OPENMM_DIR VARIABLES ARE CORRECT*. They should point to the value you chose for the OpenMM CMAKE_INSTALL_PREFIX: a local directory that exists (example: /home/username/bin/openmm). 

Now press 'c' again and then 'g', which should close the gui. Now execute the following commands: 
    
    
    make
    make install
    make PythonInstall
    make test # (optional)
    

Now you should be able to use the seekr2_openmm_plugin in openmm. You can test it by opening another python shell and typing: 
    
    
    import seekr2plugin
    

Next, install the SEEKR2 python package. 
    
    
    cd /path/to/seekr2
    python setup.py install
    python setup.py test
    

## TSCC Hopper Installation from Source[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=6> "Edit section: TSCC Hopper Installation from Source")]

Log into TSCC. 

You should run all of these commands in an interactive node to avoid clogging up the login nodes. 
    
    
    qsub -I -q home-hopper -A amaro-hopper -l nodes=1:ppn=4:gpu3090 -l walltime=2:00:00
    

(NOTE: you will need CUDA 11 to use the 3090 GPUs) 

Once you get to through the queue and the node become available, load the necessary modules: 
    
    
    module load cmake
    # gcc 7.3.1 
    source /home/ux453813/pkg/devtoolset-7/enable
    # cuda 11.1
    source  /home/ux453813/pkg/cuda.sh
    

In your home directory, make sure bin/ directory exists: 
    
    
    mkdir ~/bin
    

install conda: 
    
    
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    sh Miniconda3-latest-Linux-x86_64.sh
    

Follow the prompts to install Conda 

Install other dependencies: 
    
    
    conda install numpy scipy netcdf4 mpi4py swig
    conda install -c conda-forge doxygen
    pip install --upgrade cython
    

Get OpenMM source code. 
    
    
    git clone https://github.com/openmm/openmm.git
    cd openmm
    
    export OPENMM_INSTALL_DIR=$HOME/bin/openmm
    export OPENMM_LIB_PATH=$OPENMM_INSTALL_DIR/lib
    export OPENMM_INCLUDE_PATH=$OPENMM_INSTALL_DIR/include
    export OPENMM_PLUGIN_DIR=$OPENMM_LIB_PATH/plugins
    export OPENMM_CUDA_COMPILER=$CUDA_HOME/bin/nvcc
    export LD_LIBRARY_PATH=$OPENMM_LIB_PATH:$OPENMM_PLUGIN_DIR:$LD_LIBRARY_PATH
    export CUDA_CUDA_LIBRARY=$CUDA_HOME/lib64/stubs/libcuda.so
    
    mkdir build
    cd build
    ccmake ..
    

Press 'c' to begin the configure. 

Modify CMAKE_INSTALL_PREFIX to /home/YOUR_USERNAME/bin/openmm 

Press 'c' to configure and then press 'g' to generate. 
    
    
    make -j 4
    make install
    make PythonInstall
    make test
    

Make sure that it works in Python: 
    
    
    cd ~
    

within a python prompt: 
    
    
    >>> from simtk import openmm
    

Be sure that 
    
    
    source  /home/ux453813/pkg/cuda.sh
    export OPENMM_CUDA_COMPILER=$CUDA_HOME/bin/nvcc
    export OPENMM_INSTALL_DIR=$HOME/bin/openmm
    export OPENMM_LIB_PATH=$OPENMM_INSTALL_DIR/lib
    export OPENMM_PLUGIN_DIR=$OPENMM_LIB_PATH/plugins
    export LD_LIBRARY_PATH=$OPENMM_LIB_PATH:$OPENMM_PLUGIN_DIR:$LD_LIBRARY_PATH
    

is in your .bashrc file, and that all necessary modules are loaded for your submission scripts. 

### Install SEEKR2 on TSCC Hopper from Source[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=7> "Edit section: Install SEEKR2 on TSCC Hopper from Source")]

If you need to install SEEKR2 on TSCC, you can perform the following steps (after installing OpenMM from the steps above): 

Make sure that your .bashrc contains the necessary "source" and "export" commands. If not, then you'll need to call them explicitly. Also, be sure that you're running these commands in an interactive GPU node, not the login node (see "qsub" command near top of previous section). 
    
    
    git clone https://github.com/seekrcentral/seekr2_openmm_plugin.git
    cd seekr2_openmm_plugin/seekr2plugin
    mkdir build
    cd build
    ccmake ..
    

Now press the 'c' key. You should see the ccmake GUI appear. Modify all the variables as necessary *MAKE SURE THAT THE CMAKE_INSTALL_PREFIX AND OPENMM_DIR VARIABLES ARE CORRECT*. 

Now press 'c' again and then 'g', which should close the gui. Now execute the following commands: 
    
    
    make
    make install
    make PythonInstall
    make test # (optional)
    

Now you should be able to use the seekr2_openmm_plugin in openmm. You can test it by opening another python shell and typing: 
    
    
    import seekr2plugin
    

Next, install the SEEKR2 python package. 
    
    
    cd /path/to/seekr2
    python setup.py install
    python setup.py test
    

## SDSC Expanse Installation from Source[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=8> "Edit section: SDSC Expanse Installation from Source")]

Log into SDSC Expanse: 
    
    
    ssh username@login.expanse.sdsc.edu
    

In your home directory, make sure bin/ directory exists: 
    
    
    mkdir ~/bin
    

install conda if not already installed: 
    
    
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    sh Miniconda3-latest-Linux-x86_64.sh
    

Follow the prompts to install Conda 

If you want, you can create a new Conda environment 
    
    
    conda create -y --name SEEKR python=3.8 # optional
    conda activate SEEKR # optional
    

Next, install dependencies and necessary upgrades: 
    
    
    conda install -y git numpy scipy netcdf4 mpi4py swig
    conda install -y -c conda-forge liblapack 
    conda install -y -c conda-forge doxygen
    pip install --upgrade cython
    

Get OpenMM source code. 
    
    
    git clone https://github.com/openmm/openmm.git
    cd openmm
    

You should run the next commands in an interactive node to avoid clogging up the login nodes and to gain access to the GPU libraries and architecture. 
    
    
    srun --partition=gpu-debug  --pty --account=csd373 --nodes=1 --ntasks-per-node=10 --mem=96G --gpus=1  -t 00:30:00 --wait=0 --export=ALL /bin/bash
    

(you may need to submit this multiple times to complete the entire compilation since 30 minutes is a pretty short amount of time.) 
    
    
    module purge
    module load gpu/0.15.4
    module load gcc/7.2.0
    module load cmake
    module load cuda/11.0.2
    export OPENMM_CUDA_COMPILER=`which nvcc`
    export OPENMM_INSTALL_DIR=$HOME/bin/openmm
    export OPENMM_LIB_PATH=$OPENMM_INSTALL_DIR/lib
    export OPENMM_PLUGIN_DIR=$OPENMM_LIB_PATH/plugins
    export LD_LIBRARY_PATH=$OPENMM_LIB_PATH:$OPENMM_PLUGIN_DIR:$LD_LIBRARY_PATH
    mkdir build
    cd build
    

Now configure and make the program: 
    
    
    cmake -DCMAKE_INSTALL_PREFIX=$OPENMM_INSTALL_DIR ..
    make -j 4
    

(The job is likely to run out of time on this step. If it does, just rerun the "module load" and "export" commands and run "make -j 4" again, it will pick up where it left off.) 
    
    
    make install
    make PythonInstall
    make test # (optional)
    ./TestCudaLangevinIntegrator # (quicker test for successful CUDA install)
    

Make sure that it works in Python: 
    
    
    cd ~
    

within a python prompt: 
    
    
    >>> from simtk import openmm
    >>> openmm.Platform.getPlatformByName("CUDA")
    

Be sure that 
    
    
    
    module load gpu/0.15.4
    module load gcc/7.2.0
    module load cmake
    module load cuda/11.0.2
    export OPENMM_CUDA_COMPILER=`which nvcc`
    export OPENMM_INSTALL_DIR=$HOME/bin/openmm
    export OPENMM_LIB_PATH=$OPENMM_INSTALL_DIR/lib
    export OPENMM_PLUGIN_DIR=$OPENMM_LIB_PATH/plugins
    export LD_LIBRARY_PATH=$OPENMM_LIB_PATH:$OPENMM_PLUGIN_DIR:$LD_LIBRARY_PATH
    

is in your .bashrc file, and that all necessary modules are loaded for your submission scripts. 

### Install SEEKR2 on SDSC Expanse from Source[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=9> "Edit section: Install SEEKR2 on SDSC Expanse from Source")]

If you need to install SEEKR2 on Expanse, you can perform the following steps (after installing OpenMM from the steps above): 

Make sure that your .bashrc is contains the necessary "module loads" and "export" commands. If not, then you'll need to call them explicitly. Also, be sure that you're running these commands in an interactive GPU node, not the login node (see "srun" command near top of previous section). 
    
    
    git clone https://github.com/seekrcentral/seekr2_openmm_plugin.git
    cd seekr2_openmm_plugin/seekr2plugin
    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX=$OPENMM_INSTALL_DIR -DOPENMM_DIR=$OPENMM_INSTALL_DIR ..
    make
    make install
    make PythonInstall
    make test # (optional)
    

Now you should be able to use the seekr2_openmm_plugin in openmm. You can test it by opening another python shell and typing: 
    
    
    import seekr2plugin
    

Next, install the SEEKR2 python package. 
    
    
    cd /path/to/seekr2
    python setup.py install
    python setup.py test
    

## PSC Bridges2 Installation from Conda[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=10> "Edit section: PSC Bridges2 Installation from Conda")]

First, launch an interactive job to avoid clogging the login node 
    
    
    interact -p "GPU-shared" --gres=gpu:v100-32:1
    

## OLD Tips for getting CUDA to work:[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=11> "Edit section: OLD Tips for getting CUDA to work:")]

This is the hardest and most frustrating piece of software, so tread carefully and good luck. 

### Turn off secure boot[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=12> "Edit section: Turn off secure boot")]

During startup, hit the 'del' key to get to the BIOS. Once in the BIOS, hit the 'f7' key to enter advanced mode. 

Select the 'boot' menu. Scroll down to 'Secure Boot' and click it. Select 'Key Management'. Click 'Clear Secure Boot Keys'. 

Then save and exit the BIOS. 

### Now try to install CUDA[edit](</mediawiki/index.php?title=OpenMM&action=edit&section=13> "Edit section: Now try to install CUDA")]

First, purge all nvidia drivers from your system: 
    
    
    sudo apt-get purge cuda*
    sudo apt-get autoremove
    sudo apt-get autoclean
    sudo rm -rf /usr/local/cuda*
    

DO NOT REBOOT UNTIL YOU INSTALL THE NEW VERSION OF CUDA 

Go to the link: <https://developer.nvidia.com/cuda-80-ga2-download-archive>

And follow the necessary instructions. 

  * ~~install nvidia-387~~
  * install Cuda 8.0
