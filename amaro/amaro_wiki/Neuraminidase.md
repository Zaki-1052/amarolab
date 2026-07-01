# Neuraminidase

For each of the systems, the following analysis were performed. Below is an example for 2hu4_tami_tet system. 

## Prepare one DCD file for easy manipulation in VMD[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=1> "Edit section: Prepare one DCD file for easy manipulation in VMD")]

DCDs are compressed files, much quicker to read, so we create one here for easy viewing in VMD 
    
    
    ./catdcd -otype dcd -o 3nss_tami_st100.dcd -stride 100 -netcdf md_prod_0-5ns.netcdf md_prod_5-10ns.netcdf    md_prod_10-15ns.netcdf md_prod_15-20ns.netcdf md_prod_20-25ns.netcdf md_prod_25-30ns.netcdf md_prod_30-35ns.netcdf md_prod_35-40ns.netcdf md_prod_40-45ns.netcdf md_prod_45-50ns.netcdf md_prod_50-55ns.netcdf md_prod_55-60ns.netcdf md_prod_60-65ns.netcdf md_prod_65-70ns.netcdf md_prod_70-75ns.netcdf md_prod_75-80ns.netcdf md_prod_80-85ns.netcdf md_prod_85-90ns.netcdf md_prod_90-95ns.netcdf md_prod_95-100ns.netcdf 

## Prepare the MDCRD and PDB files for each chain[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=2> "Edit section: Prepare the MDCRD and PDB files for each chain")]

  * Use catdcd to concatenate the NETCDF files by typing:


    
    
     catdcd -o md_total.mdcrd -otype crd -stride 10 -netcdf md_prod_0-5ns.netcdf md_prod_5-10ns.netcdf md_prod_10-15ns.netcdf md_prod_15-20ns.netcdf (....) md_prod_95-100ns.netcdf
    

  * Open the MDCRD file in VMD, together with its parameter file. 
    * Check how many residues there are in each chain, from which to which residue
  * Right click on the molecule name on the VMD Main, select "Save Coordinates..." 
    * Selected atoms: resid 1 to 385
    * File type: crd
  * Repeat the step above to save a PDB file for chain A\\\
  * Repeat for each of the chain.
  * Create the prmtop file for the monomer.


    
    
    xleap
    source leaprc.ff99SB
    source leaprc.gaff
    loadamberparams frcmod-1.tam
    loadoff tam-rea.lib
    loadamberprep cal.prep
    pdb = loadpdb chainA.pdb
    saveamberparm pdb monomer.prmtop monomer.inpcrd
    

  * Below is the summary for the residue numbers for each of the chain in each system (the numbers in parentheses are the residues for tamiflu G39): 
    * 1nn2: 
      * Chain A: 1-388 (1553)
      * Chain B: 389-776 (1554)
      * Chain C: 777-1164 (1555)
      * Chain D: 1165-1552 (1556)
    * 2hu4_tami: 
      * Chain A: 1-385 (1541)
      * Chain B: 386-770 (1542)
      * Chain C: 771-1155 (1543)
      * Chain D: 1156-1540 (1544)
    * 3nss: 
      * Chain A: 1-387 (1553)
      * Chain B: 388-774 (1555)
      * Chain C: 775-1161 (1554)
      * Chain D: 1162-1548 (1556)



## RMSD of the Tetramer[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=3> "Edit section: RMSD of the Tetramer")]

  * Write _rmsd_tet.ptraj_


    
    
    trajin md_total.mdcrd
    rms first out rmsd_tet.dat @CA 
    
    
    ptraj 2hu4_tami_tet.prmtop rmsd_tet.ptraj 

  * Plot using Matlab


    
    
    matlab &
    load rmsd_tet.dat
    plot(rmsd_tet(:1), rmsd_tet(:,2)) 

## RMSD of 150 loop[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=4> "Edit section: RMSD of 150 loop")]

  * Load the MDCRD of chain A along with its parameter file (monomer.prmtop) into VMD. _[atomselect 0]_
  * Load the reference PDB file for the open conformation. _[atomselect 1]_
  * In VMD Main >> Extensions >> Tk Console
  * Source the below open_rmsd.tcl file to get the RMSD of the 150 loop with respect to the open conformation for chain A:


    
    
    set file [open open_chainA.dat w]
    set ref [atomselect 1 "alpha"]
    set traj [atomselect 0 "resid 1 to 385 and alpha"]
    set 150loop_ref [atomselect 1 "resid 146 to 152 and alpha"]
    set 150loop [atomselect 0 "resid 63 to 69 and alpha"]
    set nframes 4999
    for {set frame 0} {$frame < $nframes} {incr frame} {
      $traj frame $frame
      $150loop frame $frame
      $traj move [measure fit $traj $ref]
      set rms [measure rmsd $150loop $150loop_ref]
      puts $file $rms
      }
    close $file
    

  * For the RMSD of 1500 loop of chain A with respect to the closed conformation, repeat the same steps using the closed conformation reference. Make sure to change the name of the file, molecule ID...
  * Repeat the same steps for other chains.
  * Plot using Matlab


    
    
    matlab &
    load open_chainA.dat
    plot(open_chainA(:,1),'r')
    hold
    load closed_chainA.dat
    plot(closed_chainA(:,2),'k')
    

## RMSF[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=5> "Edit section: RMSF")]

  * Write rmsf_ABCD.ptraj


    
    
     
    trajin md_total.mdcrd
    rms first @CA
    atomicfluct out rmsf_ABCD.dat @CA byres
    
    
    
    ptraj 2hu4_tami_tet.prmtop rmsf_ABCD.ptraj 

  * Plot using Matlab


    
    
    matlab &
    load rmsf_ABCD.dat
    plot(rmsf_ABCD(:,1), rmsf_ABCD(:,2))
    

  * Similar scripts can be used to calculate the rmsf for each of the chain separately by specifying the residue numbers for that chain. For example:


    
    
    trajin md_total.mdcrd
    atomicfluct out rmsf_A.dat :1-385@CA byres
    
    
    
    ptraj 2hu4_tami_tet.prmtop rmsf_A.ptraj 

## RMSF Difference[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=6> "Edit section: RMSF Difference")]

  * The rmsf_ABCD.dat files for both apo and tami are created, each in the format:


    
    
        
        0   0.00
        1   0.30
        2   2.34
        3   1.00
        ....
    

  * Type the command below:


    
    
    paste rmsf_ABCD_tami.dat  rmsf_ABCD_apo.dat  > temp.dat\ 

  * This will create a a file in the format:


    
    
        
        0   0.00   0   0.00
        1   2.30   1   0.30
        2   3.00   2   2.34
        3   0.50   3   1.00
        ....
    

  * Type the command below:


    
    
    awk     '{print $1    "      "    $2-$4}'    temp.dat > rmsf_tami_minus_apo.dat 

  * Plot using Matlab


    
    
        matlab &
        plot(rmsf_tami_minus_apo(:,1), rmsf_tami_minus_apo(:,2))
    

## PCA[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=7> "Edit section: PCA")]

  * Write _evec.ptraj_


    
    
        trajin chainA.mdcrd
        trajin chainB.mdcrd
        trajin chainC.mdcrd
        trajin chainD.mdcrd
        rms first *
        matrix covar name mcovar
        analyze matrix mcovar out evec.pev vecs 25
        go
    
    
    
    ptraj monomer.prmtop evec.ptraj 

  * **evec.pev** is created.


  * Write _proj.ptraj_


    
    
        trajin chainA.mdcrd
        trajin chainB.mdcrd
        trajin chainC.mdcrd
        trajin chainD.mdcrd
        rms first *
        projection modes evec.pev out proj.ppj beg 1 end 25
        go
    
    
    
     ptraj monomer.prmtop proj.ptraj 

  


  * **proj.ppj** is created.
  * Use perl command and _parse.pl_ to write out _avg.txt_ , _eval.txt_ , _evec.txt_ , and _**proj.txt**_.
  * Below is the script for _parse.pl_ :


    
    
        # component analysis. 
        # Input:
        #    1. evec_in --> evec.pev
        #    2. proj_in --> proj.ppj
        # Output:
        #    1. evec.txt --> a Mx3N rectangular matrix, where N is the number of atoms 
        used in the PCA and M is the number of eigenvectors
        #    2. proj.txt --> a TxM rectangular matrix, where T is the number of 
        configurations(snapshots or trajectory frames) used in the PCA
        #    3. avg.txt --> a 1x3N row vector that contains coordinates {xi, yi, zi} of 
        the trajectory average configuration
        #    4. eval.txt --> a Mx1 column vector.  Row i contains the eigenvalue associated
        with eigenvector i.
        ###################################################################################
        $evec_in = "./evec.pev ";
        $eval_out = "./eval.txt";
        $evec_out = "./evec.txt";
        $avg_out = "./avg.txt";
        $proj_in="./proj.ppj";
        $proj_out="./proj.txt";
        open (EVEC, $evec_in);
        open (EVAL_OUT, ">$eval_out");
        open (EVEC_OUT, ">$evec_out");
        open (AVG_OUT, ">$avg_out");
        open (PROJ_IN, $proj_in);
        open (PROJ_OUT, ">$proj_out");
        ############################################################################
        # Parse first 25 eigenvectors, eigenvalues and extract the average structure 
        ############################################################################
        @lines = <EVEC>;
        @ncoords=split(/\s+/,$lines[1]);
        $indexlimit=int(0.5+$ncoords[1]/7);
        for($n=2; $n < ($indexlimit+2); $n++) {
          chomp $lines[$n];
          print AVG_OUT "$lines[$n]";
        }
        for($n=0; $n <=$#lines; $n++) {
          if ($lines[$n] =~ /\*/) {
            @eval = split(/\s+/, $lines[$n+1]);
            print EVAL_OUT "$eval[2]\n";
            for ($j=0; $j<$indexlimit; $j++) {
              @evec = split(/\s+/, $lines[$n+2+$j]);
              for($i=1;$i<=$#evec;$i++){
                 printf EVEC_OUT "%9.5f", $evec[$i];
              }
            if ($j==($indexlimit-1)) {
              print EVEC_OUT "\n"
            }
            }
          }
        }
        ############################################################################
        # Parse projections
        ############################################################################
        chomp(@data = <PROJ_IN>);
        for($j=2; $j<=$#data; $j++) {
          @lines=split(/\s+/,@data[$j]);
          for($i=2; $i<=$#lines; $i++){
            if($i==$#lines){
              printf PROJ_OUT "%9.3f\n", $lines[$i];
            }else{
              printf PROJ_OUT "%9.3f", $lines[$i];
            }
          }
        }
        close (PROJ_OUT);
        close (EVEC);
        close (EVAL_OUT);
        close (EVEC_OUT);
    
    
       * Plot **''proj.txt''** using Matlab
        
        matlab &
        load proj.txt
        plot(proj.txt(1:5000), proj.txt(1:5000), 'x')
        hold
        plot(proj.txt(5001:10000), proj.txt(5001:10000), 'xr')
        plot(proj.txt(10001:15000), proj.txt(10001:15000), 'xg')
        plot(proj.txt(15001:20000), proj.txt(15001:20000), 'xm')
    

## Clustering[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=8> "Edit section: Clustering")]

(Source: mccammon wiki) 

### Prepare the PDB trajectory file[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=9> "Edit section: Prepare the PDB trajectory file")]

  * First, prepare the trajectory file. Gromacs does not read in MDCRD or DCD files, but multi-frame PDB files. Start by converting the trajectory into the appropriate PDB format.
  * Open the DCD or MDCRD file in VMD, together with its parameter file.
  * Align the trajectory: It is typical to align the trajectory by certain atoms and then to do the clustering by another atom set. For example, one might choose to first align the trajectory by the protein alpha carbons, and then to cluster based on the positions of the residue atoms lining the active site. 
    * Within VMD, click on Extensions => Analysis => RMSD Trajectory Tool.
    * The large text box initially contains the selection "protein". Change this to whatever atom selection you wish to use to align the trajectory. To align by all alpha carbons, for example, replace "protein" with "name CA". For all NA systems, the following selection was used: "alpha and resid 35 to 37 51 to 56 64 to 70 74 97 98 114 to 118 141 to 146 161 to 165 195 196 211 213 262 to 265 286 319 320 344 to 359".
    * Click on the "Align" button.
    * Your trajectory has now been aligned.
  * Right click on the trajectory name in the VMD main menu.
  * Select "Save Coordinates..."
  * In the "Selected Atoms" field, type "protein" or whatever appropriate selection needed to isolate the objects you want to cluster.
  * Click on the "Save..." button and save the PDB file **_trajectory.pdb_ **


  * Edit the PDB file. 
    * Remove the VMD-generated header.
    * Note that VMD has separated every frame with "END". Gromacs does not accept this delimiter. Change all the "END" to "ENDMDL", which gromacs does understand.
    * Check the start of the file with head. If there is an extra CRYST1 line, remove it.
  * On terminal, type:


    
    
    cat trajectory.pdb | grep -v 'CRYST' | sed 's/END/ENDMDL/' > temp.pdb
    mv temp.pdb trajectory.pdb
    

### Prepare a PDB file of the first frame of that trajectory[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=10> "Edit section: Prepare a PDB file of the first frame of that trajectory")]

  * Open the trajectory file generated above in VMD.
  * Right click on the trajectory name in the VMD main menu.
  * Select "Save Coordinates..."
  * In the "Selected Atoms" field, type "protein"
  * In the Frames section, set First and Last to 0, and Stride to 1.
  * Click on the "Save..." button and save the PDB file _**first_frame.pdb**_



### Prepare _selection.ndx_[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=11> "Edit section: Prepare selection.ndx")]

  * Open the DCD or MDCRD file in VMD, together with its parameter file.
  * Within VMD, click on Extensions => Tk Console
  * Source "GetIndeces.tcl" to generate **_selection.ndx_ ** file.
  * Below is the script for _GetIndeces.tcl_


    
    
       #open files for ouput
       set OUT_INDEX_LIST [open "selection.ndx" w]
       #map crystal structure residue numbering to amber numbering and extract atom numbers
       set activesiteindeces [[atomselect top "protein and resid 35 to 37 51 to 56 64 to 70 74 97 98 
       114 to 118 141 to 146 161 to 165 195 196 211 213 262 to 265 286 319 320 344 to 359"] get serial]
       #output active site atom numbering in gromos ndx format
       puts $OUT_INDEX_LIST "\n"
       puts $OUT_INDEX_LIST {[ active_site ]}
       set i 1
       foreach asite $activesiteindeces {
         set parsed [split $asite " "]
         foreach index $parsed {
           if {[expr $i%15] == 0} {
             puts $OUT_INDEX_LIST [format "%+4s " "$index"]
           } else {
             puts -nonewline $OUT_INDEX_LIST [format "%+4s " "$index"]
           }
           set i [expr $i + 1]
         }
       }
          close $OUT_INDEX_LIST
    

### Clustering[edit](</mediawiki/index.php?title=Neuraminidase&action=edit&section=12> "Edit section: Clustering")]

  * A RMSD cutoff should be chosen such that: 
    * The total number of clusters is reasonable (perhaps 40 or fewer),
    * 90% of the trajectory is contained in even fewer clusters (less than 7ish),
    * There are not many clusters that contain only 1 protein configuration.
  * For this particular system, the cutoff was set to 0.150 to match with previous findings.


    
    
    module load gromacs
    which g_cluster
    g_cluster -n selection.ndx -cutoff 0.150 -f trajectory.pdb -s first_frame.pdb -method gromos -o -g -dist
