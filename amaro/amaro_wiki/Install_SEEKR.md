# Install SEEKR

This page tells you how to get SEEKR installed and up and running. It is assumed that you have installed and successfully run OpenMM. With your SEEKR environment activated, you should be able to run the following command without errors in a python shell: 
    
    
    from simtk import openmm
    

If that works, you should be able to install SEEKR 

First, add the following line to your .bashrc file: 
    
    
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/home/*username*/bin/openmm/lib"
    

This, of course, assumes that you have installed OpenMM in /home/*username*/bin/openmm. 

Source your .bashrc 
    
    
    source ~/.bashrc
    

Next, navigate to any directory (~/ directory is good) and run the following commands in a bash shell: 
    
    
    git clone https://github.com/lvotapka/openseekr.git
    cd openseekr/plugin
    mkdir build
    cd build
    ccmake ..
    

Now press the 'c' key. You should see the ccmake GUI appear. Modify all the variables as necessary *MAKE SURE THAT THE CMAKE_INSTALL_PREFIX AND OPENMM_DIR VARIABLES ARE CORRECT*. 

Now press 'c' again and then 'g', which should close the gui. Now execute the following commands: 
    
    
    make
    make install
    make PythonInstall
    

Now you should be able to use the openseekr plugin in openmm. You can test it by opening another python shell and typing: 
    
    
    import seekrplugin
    

## Other necessary programs[edit](</mediawiki/index.php?title=Install_SEEKR&action=edit&section=1> "Edit section: Other necessary programs")]

With your conda environment active, you should install some extra programs using the following commands: 
    
    
    pip install parmed
    pip install mdtraj
    

## Troubleshooting[edit](</mediawiki/index.php?title=Install_SEEKR&action=edit&section=2> "Edit section: Troubleshooting")]

If you get an error about "file not found: openmm/Context.h", that means you need to make sure that the CMAKE_INSTALL_PREFIX and OPENMM_DIR variables are correct during the ccmake step. 

If you see an error about libSeekrPlugin.so not found, then you need to add the LD_LIBRARY_PATH line to your .bashrc file, as mentioned above.
