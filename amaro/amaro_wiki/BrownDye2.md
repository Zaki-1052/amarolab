# BrownDye2

## Install Browndye2[edit](</mediawiki/index.php?title=BrownDye2&action=edit&section=1> "Edit section: Install Browndye2")]

Follow install instructions on the Browndye website: <https://browndye.ucsd.edu/index.html>

## Troubleshooting[edit](</mediawiki/index.php?title=BrownDye2&action=edit&section=2> "Edit section: Troubleshooting")]

Be sure to hit "make clean" to start a clean install after you implement any of these solutions. 

### Vector.hh Error[edit](</mediawiki/index.php?title=BrownDye2&action=edit&section=3> "Edit section: Vector.hh Error")]

If you encounter the following error: 
    
    
    src/input_output/../lib/vector.hh:6:20: fatal error: optional: No such file or directory
    

Then your gcc and/or g++ has too low of a version: 

try: 
    
    
    gcc --version
    

In Ubuntu, you can follow these steps to install: 
    
    
    sudo add-apt-repository ppa:ubuntu-toolchain-r/test
    sudo apt-get update
    sudo apt-get install gcc-7 g++-7
    gcc-7 --version
    

But then you'll need to change source/Makefile to point to "g++-7" instead of "g++" 

### H.find_opt Error[edit](</mediawiki/index.php?title=BrownDye2&action=edit&section=4> "Edit section: H.find opt Error")]

If you encounter an error like this: 
    
    
    Error: Unbound value H.find_opt
    Hint: Did you mean find_all?
    Makefile:9: recipe for target 'protein_test_charges.cmx' failed
    

This is because you need a newer version of OCAML. If you're using Ubuntu 16.04, then you cannot use "apt-get" to install OCAML. You should instead use Conda. 

With a Conda environment installed: 
    
    
    conda install -c conda-forge/label/cf201901 ocaml
