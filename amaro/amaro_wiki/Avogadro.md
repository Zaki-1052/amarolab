# Avogadro

# Avogadro[edit](</mediawiki/index.php?title=Avogadro&action=edit&section=1> "Edit section: Avogadro")]

Avogadro is a molecular visualization program that is particularly useful for Gamess, and can generate Gamess input. 

## Install Avogadro with Apt-get[edit](</mediawiki/index.php?title=Avogadro&action=edit&section=2> "Edit section: Install Avogadro with Apt-get")]
    
    
    sudo apt-get update
    sudo apt-get install avogadro
    

  


## Installing Avogadro from source[edit](</mediawiki/index.php?title=Avogadro&action=edit&section=3> "Edit section: Installing Avogadro from source")]

Follow the instructions in the Avogadro installation guide, but first install the necessary packages: 
    
    
    sudo apt-get install openbabel
    sudo apt-get install libopenbabel-dev
    

Install Eigen2, not Eigen3! 
    
    
    sudo apt-get install libeigen2-dev
    

Follow instructions below to install Qt4 

  
To install wxMacMolPlt: 

install wxWidgets: 
    
    
    sudo apt-get install wx-common
    

  
Download wxMacMolPlt at <https://brettbode.github.io/wxmacmolplt/downloads.html>

untar the tar.gz file 
    
    
    tar -xzf wxmacmolplt-7.7.tar.gz
    

Then follow the instructions in the INSTALL file. 

## Qt Installation[edit](</mediawiki/index.php?title=Avogadro&action=edit&section=4> "Edit section: Qt Installation")]

  * "When I installed Avogadro I also had to install Qt 4.8.5(this is listed in the INSTALL instructions). This was kind of confusing, but I finally was able to get it to work by following the steps below.


    
    
             1. Download Qt 4.8.5 using this link <https://download.qt.io/archive/qt/4.8/4.8.5/> 
    
    
    
             2. cd Downloads
          
             3. tar -zxvf qt-everywhere-opensource-src-4.8.5.tar.gz
    
    
    
             4. cd qt-everywhere-opensource-src-4.8.5 
    
    
    
             5. cd  ~/qt-everywhere-opensource-src-%VERSION%
    
    
    
             6. Its going to ask you something about agreeing to the terms and you just type yes.
    
    
    
             7. ./configure  
    
    
    
             8. make     
    
    
    
             9. sudo make install"
    

-Andy
