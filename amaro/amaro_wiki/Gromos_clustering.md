# Gromos clustering

Note: For a more complete description of cluster analysis, click ?. For another approach using _ptraj_ on clustering trajectories, please click [here](<https://www.nbcr.net/pub/wiki/index.php?title=Relaxed_Complex_Scheme%2C_Part_I:_Molecular_Dynamics_and_Clustering>). 

## Create Gromacs-Compatible Trajectory[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=1> "Edit section: Create Gromacs-Compatible Trajectory")]

### Preparing the Trajectory File[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=2> "Edit section: Preparing the Trajectory File")]

Gromacs does not read in MDCRD or DCD files, but multi-frame PDB files. We start by converting our trajectory into the appropriate PDB format. 

  * Open the DCD or MDCRD file in VMD, together with its parameter file.
  * Align the trajectory: It is typical to align the trajectory by certain atoms and then to do the clustering by another atom set. For example, one might choose to first align the trajectory by the protein alpha carbons, and then to cluster based on the positions of the residue atoms lining the active site. 
    * Within the VMD gui, click on Extensions => Analysis => RMSD Trajectory Tool.
    * The large text box initially contains the selection "protein." Change this to whatever atom selection you wish to use to align the trajectory. To align by all alpha carbons, for example, replace "protein" with "name CA".
    * Click on the "Align" button.
    * Your trajectory has now been aligned. 
  * Right click on the trajectory name in the VMD main menu.
  * Select "Save Coordinates..."
  * In the "Selected Atoms" field, type


    
    
     protein 

or whatever appropriate selection needed to isolate the objects you want to cluster. 

  * Click on the "Save..." button and save the PDB file trajectory.pdb
  * Edit the PDB file in something like gedit. 
    * Remove the VMD-generated header.
    * Note that VMD has separated every frame with "END". Gromacs does not accept this delimiter. Using the search and replace of your editor of choice (gedit?), change all the "END" to "ENDMDL", which gromacs does understand.



NOTE: It is considerably faster to edit a large trajectory file with shell commands. Replace END with ENDMDL using perl: 
    
    
    perl -pi -e 's/END/ENDMDL/g' trajectory.pdb 

Can be done with sed as well: 
    
    
    sed -i 's/END/ENDMDL/g' trajectory.pdb 

Check the start of the file with head. If there is an extra CRYST1 line, remove it with: 
    
    
    cat trajectory.pdb | grep -v CRYST1 > temp.pdb
    mv -f temp.pdb trajectory.pdb
    

You've successfully prepared your PDB trajectory file. 

### Preparing the PDB File[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=3> "Edit section: Preparing the PDB File")]

We also need to create a PDB file of the first frame of that trajectory. 

  * Open the DCD or MDCRD file in VMD, together with its parameter file.
  * Right click on the trajectory name in the VMD main menu.
  * Select "Save Coordinates..."
  * In the "Selected Atoms" field, type


    
    
    protein 

or whatever appropriate selection needed to isolate the objects you want to cluster (same as above). 

  * In the Frames section, set First and Last to 0, and Stride to 1.
  * Click on the "Save..." button and save the PDB file first_frame.pdb
  * Edit the PDB file in something like gedit. Remove the VMD-generated header.



Another way to create a PDB file of the first frame of the trajectory is to simply open "trajectory.pdb" in vi, move the cursor to the first "ENDMDL," and type in "d G" to delete everything from that line to the end of the file. Then save the truncated file as //first_frame.pdb// by typing in 
    
    
    :w first_frame.pdb 

## Identify the Protein Residues that Line the Active Site[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=4> "Edit section: Identify the Protein Residues that Line the Active Site")]

Typically when clustering protein trajectories for drug-design purposes, you want to know about the various configurations of the protein active site. Thus, the residues that line the active site must be identified. 

While there are various methods for identifying active-site residues, I typically start with the first frame of my trajectory (//first_frame.pdb//) and use VMD to identify all protein residues within 10 Angstroms of the ligand. 

Example of VMD Selection: 
    
    
    same residue as protein within 10 of resname LIG 

To get the indices of the atoms of the active-site residues, save a PDB file containing only the relevant active-site residues. 

  * Right click on the protein name in the VMD main menu.
  * Select "Save Coordinates..."
  * In the "Selected Atoms" field, type something like:


    
    
    same residue as protein within 10 of resname LIG 

  * Click on the "Save..." button to save the PDB file. Call in active_site.pdb.
  * Edit the PDB file in something like gedit to remove all lines but the coordinate data. Remove all HEADER data and END data.
  * Unfortunately, VMD reindexes all the atoms when you save a new pdb file, so atom indices in your new file (_active_site.pdb_) do not match the indices in the original PDB containing the entire protein (_trajectory.pdb_ or _first_frame.pdb_). Fortunately, the residue indices are not changed, so let's just save those. From the command line, extract just the residue index numbers like this:


    
    
    cat active_site.pdb | awk '{print $6}' | sort -n | uniq > resid_activesite.dat 

  * So now you have a file containing all the residue indices of the active-site residues. Let's pick out the lines of the original PDB file (_first_frame.pdb_) the have those same residue indices.


  * **WARNING: This will write an active_site_correct_residues.pdb file that could copy monomers you're not interested in. It'll copy all of the residues with that specific index numbers. Chances are, if you have a protein structure made up of monomers, multiple monomers will get copied over.**


    
    
    cat resid_activesite.dat | awk '{print "cat first_frame.pdb | awk STARTif ($6==" $1  ") print $0 END" }' | sed "s/START/'{/g" | sed         "s/END/}'/g"  | csh > active_site_correct_residues.pdb 

Note that you may get the following error: 
    
    
      awk: {if ($6==) print $0 }
      awk:          ^ syntax error
    

This error can be corrected if a blank line is removed from the resid_activesite.dat file. 

## Identify Key Atom Indices[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=5> "Edit section: Identify Key Atom Indices")]

We must identify the indices of all active-site atoms. This is because we want to cluster by all the atoms of the active site. 

To get the indices of all active-site atoms: 
    
    
     cat active_site_correct_residues.pdb  | awk '{printf $2 " "}' > active_site_atoms_indices.dat 

To get the indices in the ndx format 
    
    
    cat active_site_correct_residues.pdb | grep " CA " | awk '{ if ( NR%15 == 0){ {printf "%5i", $2} {printf "\n"} } else {printf "%5i ", $2} }' > active_site.ndx 

and 
    
    
    cat first_frame.pdb | grep " CA " | awk '{ if ( NR%15 == 0){ {printf "%5i", $2} {printf "\n"} } else {printf "%5i ", $2} }' > alpha_carbons_indices.ndx 

## Create Gromacs-Compatible Atom-Selection File[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=6> "Edit section: Create Gromacs-Compatible Atom-Selection File")]

Gromacs has a very specific file format (the ndx file) that it uses to read in atom selections. Here's the general format of this file: 
    
    
    [ SELECTION NAME 1 ]
    #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
    #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
    #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
    #### #### #### #### #### #### #### #### #### #### ####
    
    [ SELECTION NAME 2]
    #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
    #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
    #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
    #### #### #### #### #### #### #### #### #### #### ####
    

where the "####" represent the indices of the atoms of that selection. If any index has fewer than four digits, right justify by adding extra spaces (not tabs). We need to create two atom selections, one containing the indices of all the C-alpha carbons (contained in the file _alpha_carbons_indices.dat_), and one containing the indices of all the active-site atoms (contained in the file _active_site_atoms_indices.dat_). My file looks something like this: 
    
    
    [ C-alpha ]
       5   30   36   53   70   87  107  124  141  157  178  190  205  224  241
     258  278  297  316  331  346  365  380  399  421  441  453  470  490  496
     510  534  550  574  595  614  638  660  677  694  706  720  734  745  764
     771  778  800  821  835  859  866  885  899  915  934  946  962  972  987
    
    [ active_site ]
     835 1465 1519 1538 1555 1565 1582 1603 1622 1638 1653 1665 1677 1696 1713
    1725 1739 1750 1766 1780 1804 1871 1906 2078 2123 2130 2187 2628 2652 2668
    4335 4349 4361 4397 4419 4441 4452 4463 5759 5800
    

_Note that numbers are separated with spaces, not tabs._ _Note: For a very large system, a five digit format also works. Edit the awk lines above from %4i to %5i to create your .ndx files._

Save your selection file as "selection.ndx" 

## How to Run Gromacs to do Gromos Clustering[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=7> "Edit section: How to Run Gromacs to do Gromos Clustering")]

  * If you have more than ~40000 frames the program will choke (levi)
  * Do we need to be running with the double-precision -d option? (rommie)
  * The new executable located below implicitly is double-precision (levi)


    
    
    /net/linux/pkg-64/gromacs-4.0.4-intel-fftw-3.1.2/bin/g_cluster_d 

With all the files created, you're ready to start. Here's the file you run from the command line on the chemcca computers: 
    
    
    /net/home/swilliam/Software/gromacs-3.3.1/src/tools/g_cluster -n selection.ndx -cutoff 0.125 -f trajectory.pdb -s first_frame.pdb -method gromos -o -g -dist -ev -sz -tr -ntr -clid -cl 

An easier command to use is to enter 
    
    
    module load gromacs 

and then 
    
    
    g_cluster -n selection.ndx -cutoff 0.125 -f trajectory.pdb -s first_frame.pdb -method gromos -o -g -dist -ev -sz -tr -ntr -clid -cl 

change the cutoff and .pdb files to fit your system 

For information on each of these g_cluster parameters, see <http://www.gromacs.org/documentation/reference/online/g_cluster.html>

Two output files are always written: -o writes the RMSD values in the upper left half of the matrix and a graphical depiction of the clusters in the lower right half. 

Additionally, a number of optional output files can be written: -dist writes the RMSD distribution. -ev writes the eigenvectors of the RMSD matrix diagonalization. -sz writes the cluster sizes. -tr writes a matrix of the number transitions between cluster pairs. -ntr writes the total number of transitions to or from each cluster. -clid writes the cluster number as a function of time. -cl writes average (with option -av) or central structure of each cluster or writes numbered files with cluster members for a selected set of clusters (with option -wcl, depends on -nst and -rmsmin). 

After running the above from the command line, you'll get a lot of text output ending in: 
    
    
    Opening library file /net/home/swilliam/Software/gromacs-3.3.1/share/top/aminoacids.dat
    Opening library file /net/home/swilliam/Software/gromacs-3.3.1/share/top/atommass.dat
    Opening library file /net/home/swilliam/Software/gromacs-3.3.1/share/top/vdwradii.dat
    Opening library file /net/home/swilliam/Software/gromacs-3.3.1/share/top/dgsolv.dat
    #Entries in atommass.dat: 82 vdwradii.dat: 26 dgsolv.dat: 7
    
    Select group for least squares fit and RMSD calculation:
    Group     0 (     C-alpha) has   367 elements
    Group     1 (active_site_CA) has    85 elements
    Select a group: 
    

The labeling text is misleading, apparently. You need to first select the atom group by which you wish to cluster. Type "1" and press enter. You're interested in the active-site configurations for drug-design purposes. (Note that the trajectory has already been aligned previously in VMD.) 

The following additional text appears: 
    
    
    Select group for output:
    Group     0 (     C-alpha) has   367 elements
    Group     1 (active_site_CA) has    85 elements
    Select a group:
    

Again, type "1" and press enter. Output will only be written for the active-site alpha carbons. (You'll be obtaining all-atom information another way, as described below.) 

**Note: It may be better to cluster by all active-site atoms, not just by the alpha carbons, depending on the question being asked. Think back on the question you are asking; if you're interested in drug discovery or asking questions about the active site, always group based on the active site. Be sure to consult the literature for residues/sequences that are crucial to the active site in question, and be sure it falls in the active_site_CA that you have determined! Use VMD to verify.**

g_cluster now does its thing. It produces a useful output file called "cluster.log". Here's what that file looks like: 
    
    
    Using gromos method for clustering
    Using RMSD cutoff 0.14 nm
    The RMSD ranges from 0.0637001 to 0.388457 nm
    Average RMSD is 0.20783
    Number of structures for matrix 1601
    Energy of the matrix is 126.831 nm
    
    Found 23 clusters
    
    Writing middle structure for each cluster to clusters.pdb
    Counted 268 transitions in total, max 30 between two specific clusters
    
    cl. | #st rmsd | middle rmsd | cluster members
      1 | 805 .141 |   1356 .120 |    640    641    644    645    649    650    651
        |          |             |    661    662    663    664    665    667    669
        |          |             |    670    671    677    682    683    684    691
      2 | 186 .141 |    184 .120 |     93     95     99    101    102    106    111
        |          |             |    116    117    118    119    120    121    123
      3 | 180 .141 |    459 .124 |    408    409    411    414    415    416    417
      4 |  84 .133 |    376 .117 |    293    294    301    304    305    312
      5 |  78 .134 |     50 .115 |     21     22     23     24     25
    

This file shows the results. For example, notice that cluster 1 (the most-populated cluster) has 805 members (not all shown). The central member of the cluster (i.e. the most representative frame) is the 1356 frame of the trajectory. Note that, paradoxically, gromacs starts numbering the frames with -1. VMD starts numbering with 0, so to convert one of these gromacs frame indecies to a VMD frame index, just add 1. 

## An Example: How to Identify the Best Cutoff[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=8> "Edit section: An Example: How to Identify the Best Cutoff")]

Notice above that the command line parameter "cutoff" was set to 0.125 nanometers (unfortunately, gromacs uses nanometers, not angstroms). This is not necessarily the best RMSD cutoff for the clustering. In reality, the cutoff parameter must be varied to find the ideal. In a recent project, for example, I varied the cutoff from 0.050 to 0.155. Here's a graph of the cutoff vs. the number of clusters gromacs found: 

[![Clustering graph.png](/mediawiki/images/3/37/Clustering_graph.png)](</mediawiki/index.php/File:Clustering_graph.png>)

In the example of the picture above, a cutoff of 0.14 was ultimately chosen. 

## How to Identify the Best Cutoff for your System[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=9> "Edit section: How to Identify the Best Cutoff for your System")]

To determine the best RMSD cutoff for your system, it's best to find a suitable range to narrow down. In the above example, an RMSD cutoff range was chosen from 0.050 nm to 0.155 nm. I found choosing a low end close to 0.0 nm (such as 0.050 nm) and a high end close to 0.175 nm works well. Keep the below points in mind: 

A RMSD cutoff should be chosen such that 

  * the total number of clusters is reasonable (perhaps 40 or fewer),
  * 90% of the trajectory is contained in even fewer clusters (less than 7ish),
  * visualize to confirm the top three to five centroids aren't highly similar,
  * and there are not many clusters that contain only 1 protein configuration.



You will find that approximately 0.0 nm will yield a huge amount of clusters, and the fewer the clusters, the better. Run different RMSD cutoffs that are larger and larger, and plot your results as you go. (For example, run 0.025 nm first, and if you find 0.025 nm is off the charts, follow with 0.075 nm, and smaller increments from there.) 

When you start to approach less than 40 clusters, keep going until 

  * only small changes in the amount of clusters (stays around 7 or so) when you change the RMSD cutoff by + or - 0.01 nm
  * there is HIGH overlap between the same centroid with different RMSD cutoffs (seen in the below figure):



[![Centroid overlap.jpg](/mediawiki/images/2/2f/Centroid_overlap.jpg)](</mediawiki/index.php/File:Centroid_overlap.jpg>)

It's helpful to visualize as you go. Upload each clusters.pdb file with different RMSD cutoffs that are + or - 0.01 nm of one another. **Color each centroid differently.** The first cluster (the first frame in VMD) should be so similar to one another of the different RMSD cutoffs that it should overlap so well that only a single color is showing. The further out you go, in frames, you should start to see less overlap. For the example in the above figure, I chose 0.105 nm RMSD cutoff. **The reason you see ONLY the gray 0.11 RMSD cutoff in centroid 1 is because centroid 1 for each RMSD cutoff are so similar. All RMSD cutoffs are uploaded, but 0.11 RMSD was the last to be uploaded, so it's the forefront color.**

## Verify that the Top Three Clusters are Unique[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=10> "Edit section: Verify that the Top Three Clusters are Unique")]

Once a cutoff is chosen by the criteria above, it's best to verify that the clusters actually represent distinct protein configurations. To verify this, the hydrogen-bond networks of the members of the top few clusters can be analyzed and compared. 

First, we need to create a PDB file containing all the frames of the trajectory, but containing only the active site residues. To analyze all the hydrogen bonds of the entire protein will take too long; we'll limit ourselves to the hydrogen bonds of the active site, since that's what we really care about for docking. 

  * Open the file _trajectory.pdb_ in VMD.
  * Right click on the trajectory name in the VMD main menu.
  * Select "Save Coordinates..."
  * In the "Selected Atoms" field, type


    
    
    resid ### ### ### ### 

where the ### represent the active-site residue indices, contained in the file _resid_activesite.dat_. 

  * Click on the "Save..." button and save the PDB file _trajectory_active_site.pdb_
  * Edit the PDB file in something like gedit. 
    * Remove the VMD-generated header.
    * Note that VMD has separated every frame with "END". Using the search and replace of your editor of choice (gedit?), change all the "END" to "ENDMDL".


    
    
    sed -i 's/END/ENDMDL/g' trajectory_active_site.pdb 

Now, we need to separate each of the frames of trajectory_active_site.pdb into its own file. 

  * First, create a directory called frames off of the directory containing the _trajectory_active_site.pdb_ file.


    
    
    mkdir frames 

  * Next, open _trajectory_active_site.pdb_ in an editor and count the number of filelines in each trajectory frame. To do this quickly in vi, launch the software in read-only mode by typing "view" rather than "vi". Then type ":set nu" to get line numbers. Typing "/ENDMDL" will move your cursor to the first "ENDMDL" and you can read the line number. (Other text editors can also be used to give the line number corresponding to the first "ENDMDL" in the file.)
  * Exit the text editor and return to the unix prompt. Change into the frames directory


    
    
    cd frames 

  * Now, split _trajectory_active_site.pdb_ into multiple files by using the following command:


    
    
    split -l ### -a 5 ../trajectory_active_site.pdb 

where ### is the number of filelines per trajectory frame, found previously. 

  * Now that each frame has been placed in its own file, we need to rename those frames so they're understandable. Type in this command in the frames directory:


    
    
    ls -1 | sort | awk '{t=t+1;print "mv " $1 " frame_" (t-2) ".pdb"}' | csh 

(Note that the first frame is named frame_-1.pdb. The indices correspond to the gromacs default, not the VMD default.) 

  * Now create three directories, _cluster1_ , _cluster2_ , and _cluster3_.
  * Notice in your _cluster.log_ file that the gromacs index numbers corresponding to the members of each cluster are listed. For each of the three most populated clusters, copy the corresponding PDB files in the _frames_ directory into _cluster1_ , _cluster2_ , and _cluster3_.


  * Now that you have three directories containing multiple files (corresponding to the frames of the 1st, 2nd, and 3rd most-populated cluster), merge the files of each _cluster#_ directory into one. In each directory, type the following:


    
    
    cat frame*.pdb > all.pdb 

Now that you have three pdb files (each named _all.pdb_) that contain all the frames of their corresponding clusters, you can analyze them using a script I wrote, called _id_hydrogen_bonds.php_. 
    
    
    <?php
    
    $seperator='ENDMDL';
    $dist_cutoff=3.0;
    $angle_cutoff=30;
    
    error_reporting(1);
    ini_set("memory_limit","2000000M");
    
    $filename=$argv[1];
    
    $file=file_get_contents($filename);
    $file=explode($seperator,$file);
    
    $results=array();
    
    for($t=0;$t<count($file);$t++) {
    
    	$frame=rtrim(trim($file[$t]));
    	$frame=explode("\n",$frame);
    	$pdb=LoadPDB_fromstringArray($frame);
    	for ($s=0;$s<count($pdb);$s++) {
    		$pdb[$s]['element']=get_element_from_name($pdb[$s]['name']);
    	}
    
    	//Now look through every possible hydrogen donor, see if it is connected to some hydrogen, then, if so, check against all other hydrogen acceptors
    	for ($s=0;$s<count($pdb);$s++) {
    		if (($pdb[$s]['element']=='N') || ($pdb[$s]['element']=='O')) { //Look for all the hydrogen bond donors
    			//Now search through the PDB to find near by hydrogens
    			for ($u=0;$u<count($pdb);$u++) {
    				if ($pdb[$u]['element']=='H') {
    					$dist=dist_point($pdb[$s],$pdb[$u]);
    					if ($dist<1.3) { //So now you've identified the hydrogen-bond donor and it's hydrogen
    						//Now search through all the hydrogen bond acceptors to see if any are in the right position.
    						for ($v=0;$v<count($pdb);$v++) {
    							if ($v!=$s) { //The donor and acceptor atom must not be the same.
    								if (($pdb[$v]['element']=='N') || ($pdb[$v]['element']=='O')) { //Look for all the hydrogen bond acceptors
    									$dist=dist_point($pdb[$s],$pdb[$v]);
    									if ($dist<=$dist_cutoff) { //Must satisfy distance cutoff
    										$angle=abs(180-angle_point($pdb[$s],$pdb[$u],$pdb[$v]));
    										if ($angle<=$angle_cutoff) { //Must satisfy angle cutoff
    											$results[$pdb[$s]['index']."-".$pdb[$u]['index']."-".$pdb[$v]['index']]++;
    										}
    									}
    								}
    							}
    						}
    					}
    				}
    			}
    		}
    	}
    }
    
    //Now display the results
    foreach ($results as $key => $value) {
        echo 'HBond: '.$key."\t".' Prevelance: '.(100*$value/count($file))."\n";
    }
    
    //Supporting functions
    
    function get_element_from_name($atomname) {
    	for ($t=0;$t<strlen($atomname);$t++) {
    		$letter=substr($atomname,$t,1);
    		if (!is_numeric($letter)) {
    			return strtoupper($letter);
    			break;
    		}
    	}
    }
    
    function LoadPDB_fromstringArray($file) {
            $PDB=array();
    
            $counter=0;
            for ($t=0;$t<count($file);$t++) {
                    $line=rtrim($file[$t]);
                    if ((substr($line,0,5)=="ATOM ") || (substr($line,0,7)=="HETATM ")) {
    			$name=trim(substr($line,12,4));
    			$index=trim(substr($line,6,6));
                            $resname=trim(substr($line,17,3));
                            $resindex=trim(substr($line,22,4));
                            $x=trim(substr($line,30,8));
                            $y=trim(substr($line,38,8));
                            $z=trim(substr($line,46,8));
                            $chain_id=trim(substr($line,21,1));
    
    			#Try to determine the element
    			$element=strtoupper($name);
    			for ($s=0;$s<=9;$s++) {$element=str_replace($s,'',$element);} #Strip numbers
    			#First check for atom names with two letters
    			if (substr($element,0,2)=='BR') {
    				$element='BR';
    			} elseif (substr($element,0,2)=='CL') {
                                    $element='CL';
                            } elseif (substr($element,0,2)=='BI') {
                                    $element='BI';
                            } elseif (substr($element,0,2)=='AS') {
                                    $element='AS';
                            } elseif (substr($element,0,2)=='HG') {
                                    $element='HG';
    			} else { #So, just assume it's the first letter.
    				$element=substr($element,0,1);
    			}
    
                            $PDB[$counter]['resname']=$resname;
                            $PDB[$counter]['resindex']=$resindex;
                            $PDB[$counter]['x']=$x;
                            $PDB[$counter]['y']=$y;
                            $PDB[$counter]['z']=$z;
                            $PDB[$counter]['chain_id']=$chain_id;
                            $PDB[$counter]['line']=$line;
    			$PDB[$counter]['name']=$name;
    			$PDB[$counter]['index']=$index;
    			$PDB[$counter]['element']=$element;
    
                            $counter++;
    
                    }
            }
    
            return $PDB;
    
    }
    
    function dist($x1,$y1,$z1,$x2,$y2,$z2) {
    	$deltax=abs($x1-$x2);
            $deltay=abs($y1-$y2);
            $deltaz=abs($z1-$z2);
    
    	return sqrt(pow($deltax,2)+pow($deltay,2)+pow($deltaz,2));
    
    }
    
    function dist_point($point1, $point2) {
    	return dist($point1['x'],$point1['y'],$point1['z'],$point2['x'],$point2['y'],$point2['z']);
    }
    
    function angle($x1,$y1,$z1,$x2,$y2,$z2,$x3,$y3,$z3) {
    	
    	$vector1['x']=$x1-$x2;
    	$vector1['y']=$y1-$y2;
    	$vector1['z']=$z1-$z2;
    
            $vector2['x']=$x3-$x2;
            $vector2['y']=$y3-$y2;
            $vector2['z']=$z3-$z2;
    
    	$dot=$vector1['x']*$vector2['x']+$vector1['y']*$vector2['y']+$vector1['z']*$vector2['z'];
    
    	$vector1_length=sqrt(pow($vector1['x'],2)+pow($vector1['y'],2)+pow($vector1['z'],2));
            $vector2_length=sqrt(pow($vector2['x'],2)+pow($vector2['y'],2)+pow($vector2['z'],2));
    
    
    	$angle=acos($dot/($vector1_length*$vector2_length))*180/pi();
    
    	return $angle;
    
    }
    
    function angle_point($point1, $point2, $point3) {
    	return angle($point1['x'],$point1['y'],$point1['z'],$point2['x'],$point2['y'],$point2['z'],$point3['x'],$point3['y'],$point3['z']);
    }
    
    ?>
    

To analyze the hydrogen bonds of the active sites of the proteins of cluster 1, for example, I would change the current directory to the cluster1 directory and then run the following command: 
    
    
    /PATH/TO/php /PATH/TO/SCRIPT/id_hydrogen_bonds.php all.pdb > hbond_analysis.dat 

The file _hbond_analysis.dat_ looks like this: 
    
    
    HBond: 101-102-175       Prevelance: 40
    HBond: 120-121-500       Prevelance: 80
    HBond: 163-164-106       Prevelance: 20
    HBond: 271-272-199       Prevelance: 60
    HBond: 324-325-199       Prevelance: 80
    HBond: 446-447-500       Prevelance: 20
    

In the first column, the hydrogen bond is identified by the index numbers of donor-hydrogen-acceptor. In the second column, the prevalence of the hydrogen bond is listed. So, for example, the hydrogen bond 120-121-500 was present in 80% of the frames (protein configurations) contained in _all.pdb_ (cluster 1). 

Perform this same analysis on clusters 2 and 3. Compare the hbond_analysis.dat file of each, perhaps in a spreadsheet. Here's a comparison I constructed using excel: 
    
    
    		cluster1 	cluster2 	cluster3
    H-Bond 1	0		33.15		0
    H-Bond 2	5.45		64.17		0
    H-Bond 3	0		18.18		0
    H-Bond 4	10.29		10.69		15.46
    H-Bond 5	61.78		62.56		31.87
    H-Bond 6	50.24		48.12		35.35
    H-Bond 7	16.50		9.09		6.07
    H-Bond 8	68.11		82.88		70.71
    

Notice that H-Bond 1 is absent from all the protein configurations of clusters 1 and 3, but is present in 33.15% of the protein configurations of cluster 2. This suggests that, overall, clusters 2 and 3 represent distinct protein configurations. 

On the other hand, notice that H-bond 6 is present in 50.24% of the members of cluster 1, but only 35.35% of the members of cluster 3. This suggests that, overall, clusters 1 and 3 also represent distinct protein configurations. 

## Working Only with the Central Members of each Cluster[edit](</mediawiki/index.php?title=Gromos_clustering&action=edit&section=11> "Edit section: Working Only with the Central Members of each Cluster")]

Once you've confirmed that your clusters are sufficiently unique, extract the "central member" of each cluster (see the _cluster.log_ file.) Remember that you've already created a single PDB file corresponding to the central member of each cluster (it's in the _frames_ directory, together with all the other protein configurations of your trajectory.) Each central member does a good job of representing all the protein configurations of the corresponding cluster. In performing relaxed-complex virtual screens, dock only to the central member of each cluster, and then perform a weighted mean based on the cluster population size. Good luck! 

This script will extract the central members of each cluster and number them by rank putting them in the folder "cluster_frames". Just edit the variable "pdbpath" to be your trajectory path and run from the folder that has the cluster.log file in it. *Note* this will recreate the "frames" directory, to save space you may want to delete this after running the script. 
    
    
    #!/bin/bash
    
    #this script extracts clusters from a pdb trajectory given a gromos output cluster.log file
    #the output is in cluster_frames/
    
    
    #*******************start script from in directory with log file and insert trajectory path below************************************************
    pdbpath=/Your/path/here/trajectory.pdb
    #**********************************************************************************************************************************************
    path=$(pwd)
    echo "$path"
    
    cat cluster.log | awk 'BEGIN{FS="|"}{if (NF==4) print $3}' | awk '{if ($1>0) print $1}' | grep -v "middle" |  awk '{printf "%i ",$1}' > clusterid
    
    count=0000
    
    echo "extracting clusters"
    cat clusterid
    
    mkdir frames
    mkdir cluster_frames
    
    
    
    cd frames
    numlines=$(grep -n "END" $pdbpath | cut -d":" -f1 | head -n 1)
    
    split -l "$numlines" -a 5 "$pdbpath"
    ls -1 | sort | awk '{t=t+1;print "mv " $1 " frame_" (t-2) ".pdb"}' | csh
    
    
    
    for i in `cat ""$path"/clusterid"`
    do
    
    let count++
    cp "$path"/frames/frame_"$i".pdb "$path"/cluster_frames/"$count"frame_"$i".pdb
    
    done
    

Copy and paste this into a shell script named "extract_central_members.sh" 

Add executable permission 
    
    
    chmod + x extract_central_members.sh 

And run as 
    
    
    ./extract_central_members.sh
