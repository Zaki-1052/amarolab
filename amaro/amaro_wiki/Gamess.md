# Gamess

# Gamess[edit](</mediawiki/index.php?title=Gamess&action=edit&section=1> "Edit section: Gamess")]

Gamess is a free and powerful quantum chemistry software package. 

## Installation[edit](</mediawiki/index.php?title=Gamess&action=edit&section=2> "Edit section: Installation")]

How to install GAMESS on Linux (for more detailed instructions, use readme.unix in the gamess directory). 

Register and download the tarball from the GAMESS website. Under source code distrubition, select the following options: GAMESS version February 14, 2018 R1 for 64 bit (x86_64 compatible) under Linux with gnu compilers and GAMESS+LIBCCHEM version February 14, 2018 R1 for NVIDIA GPUs. Then unpack the tarball. 
    
    
    tar -xzf gamess-current.tar.gz
    cd gamess/
    gedit machines/readme.unix &
    

Follow instructions in readme.unix 

Change the following scripts to have the header: `#!/bin/tcsh`

  * config 
  * compall 
  * comp 
  * lked 
  * rungms 
  * runall



Make sure the following software is installed by typing the following commands: 

If liblapack3 isn't install, then type: 
    
    
    apt-get install liblapack3
    

install atlas if its not installed: 
    
    
    sudo apt-get install libatlas-base-dev
    

type: 
    
    
    ./config
    

Choose linux64 

Choose whatever GAMESS directory you want 

I don't think version number matters 

Choose gfortran/gcc option 

I don't think version number matters 

To find the location of liblapack3, type: 

dpkg -L liblapack3 

Then tell GAMESS to refer to the directory where it was installed (maybe /usr/lib/atlas-base) 

You can install LIBCHEM later once this first installation was successful 

Next: 
    
    
    cd ddi
    ./compddi
    mv ddikick.x ..
    
    cd ..
    ./compall >& compall.log
    

Search for errors by typing: 
    
    
    grep error compall.log
    
    ./lked gamess 01 >& lked.log
    

edit rungms and change SCR equal to somewhere accessible on your system (like /home/yourname/tmp). Of course, the directory must exist. Also change USERSCR to be somewhere also, like /home/yourname/log???). Change GMS path to (home/yourname/Downloads) 

Then go to the gamess/ directory and do: 
    
    
    ./runall
    

which should take a while 

then check all the output with ./tests/standard/checktst 

If they all passed, you're good! 

Open your ~/.bashrc and add: 
    
    
    alias gms='/path/to/gamess/rungms'
    

Obviously, replace the path with the actual one. 

## Installation with CUDA for fast GPU quantum calcs[edit](</mediawiki/index.php?title=Gamess&action=edit&section=3> "Edit section: Installation with CUDA for fast GPU quantum calcs")]

**WORK IN PROGRESS: THIS DOESN'T WORK YET**

If you want to be able to install Gamess to run on our GPU, then go into the Gamess directory. The README file contains useful information that you should follow. Better yet, **use aaa.readme.1st**. 

The boost compilation may not work. If not, then download a later version of boost: 
    
    
    wget -O boost_1_55_0.tar.gz https://sourceforge.net/projects/boost/files/boost/1.55.0/boost_1_55_0.tar.gz/download
    tar xzvf boost_1_55_0.tar.gz
    cd boost_1_55_0/
    sudo apt-get update
    sudo apt-get install build-essential g++ python-dev autotools-dev libicu-dev build-essential libbz2-dev libboost-all-dev
    ./bootstrap.sh --prefix=/home/lvotapka/Downloads/gamess/libcchem/boost
    ./b2
    ./b2 install
    

The GA installation went fine for me. 

I had to install HDF5 manually: 

First, I had to install SZIP from [[1]](<https://support.hdfgroup.org/ftp/lib-external/szip/2.1.1/src/szip-2.1.1.tar.gz>)

Then untar and install 
    
    
    gunzip szip-2.1.1.tar.gz
    tar -xf szip-2.1.1.tar
    cd szip-2.1.1
    ./configure --prefix=/usr/local/szip
    make
    sudo make install
    

Download the HDF5 "tar" file for UNIX from [[2]](<https://support.hdfgroup.org/HDF5/release/obtainsrc518.html#conf>)
    
    
    tar -xf hdf5-1.8.20.tar
    hdf5-1.8.20
    ./configure --prefix=/usr/local/hdf5 --enable-fortran --enable-cxx --with-szlib=/usr/local/szip
    make
    make check                # run test suite.
    sudo make install
    sudo make check-install        # verify installation.
    

Now, inside the gamess/libcchem directory, I entered the following commands to configure and make: 
    
    
    ./configure --prefix=$PWD --with-gamess --with-blas --with-ga=$HOME/Downloads/gamess/ga --with-boost=$PWD/boost --with-hdf5=/usr/local/hdf5 --with-cuda=/usr/lib/cuda --with-gpu=pascal --with-libint=/home/lvotapka/Downloads/libint --with-math=atlas CXXFLAGS="-O3 -msse3" # CC=cc CXX=CC
    make
    make install
    
    

This may or may not work, you can also try to reinstall GAMESS, but choose to install LIBCCHEM. It might ask you if you want to install LIBINT. I recommend "no" 

~~Go to<https://gmplib.org/> and download the tar 
    
    
    sudo apt-get install libgmp-dev
    
    
    
    sudo apt-get install automake
    git clone https://github.com/evaleev/libint.git
    cd libint
    ./autogen.sh
    mkdir build
    cd build
    ../configure
    make
    make check
    make install
    

~~ You may also have to install Eigen. Just download the source, unpack, and use that directory as the place where to look for Eigen.
