# Catdcd

First create a symbolic link: 
    
    
    sudo ln -s /lib/x86_64-linux-gnu/libexpat.so.1 /lib/x86_64-linux-gnu/libexpat.so.0
    

Then you should find catdcd in the VMD directory. Example: 
    
    
    ~/Downloads/vmd-1.9.3/plugins/LINUXAMD64/bin/catdcd5.1
    

Copy this over to a directory that is included in $PATH. For example, if ~/bin is in $PATH, run the following: 
    
    
    cp ~/Downloads/vmd-1.9.3/plugins/LINUXAMD64/bin/catdcd5.1/catdcd ~/bin
