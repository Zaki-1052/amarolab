# MultiWFN

First of all, OpenMotif needs to be installed: 

Open a terminal and go into ~/Downloads or something 

NOTE: some of these steps take a long time... 

~~
    
    
    git clone https://git.code.sf.net/p/motif/code motif-code
    cd motif-code
    sh autogen.sh
    LIBS=-lXt ./configure
    make
    make check
    make install
    

~~
    
    
    sudo apt-get install libmotif-dev
    

Download the MultiWFN binary from <http://sobereva.com/multiwfn/> into Downloads or somewhere. Go to that directory. 
    
    
    unzip Multiwfn_3.6_dev_bin_Linux.zip
    cd Multiwfn_3.6_dev_bin_Linux/
    chmod u+x Multiwfn
    ./Multiwfn
