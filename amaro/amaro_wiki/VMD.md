# VMD

# VMD[edit](</mediawiki/index.php?title=VMD&action=edit&section=1> "Edit section: VMD")]

## Installation[edit](</mediawiki/index.php?title=VMD&action=edit&section=2> "Edit section: Installation")]

Visit the UIUC VMD download page and download the latest version of VMD. Register with UIUC, accept the user agreement, and begin the download. 

NOTE: If you need to use CUDA 8 make sure you choose a download that uses CUDA 8. 

<https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=VMD>

After the download is complete, cd where the download is and untar: 
    
    
    tar -xzf vmd-x.x.x.x-whatever.tar.gz
    

Your file will have a different name, so use 'ls' to see the name of the file. 

cd into the new vmd folder. 

Follow the steps in the README "Quick Installation Instructions". 

Be sure to set "$install_bin_dir" equal to "/home/USERNAME/bin" 

Also, set "$install_library_dir" equal to "/home/USERNAME/lib/$install_name" 

If /home/USERNAME/bin and /home/USERNAME/lib don't exist, then create them using the mkdir command. 

Add the following line to your .bashrc: 
    
    
    export VMDMSMSUSEFILE="on"
    

## Troubleshooting[edit](</mediawiki/index.php?title=VMD&action=edit&section=3> "Edit section: Troubleshooting")]

If you get an error concerning OSPRay, try to use VMD version 1.9.2 or lower.
