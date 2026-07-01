# Clustering

## Using binding site shape clustering script[edit](</mediawiki/index.php?title=Clustering&action=edit&section=1> "Edit section: Using binding site shape clustering script")]

### Modified script[edit](</mediawiki/index.php?title=Clustering&action=edit&section=2> "Edit section: Modified script")]

Located at /extra/banzai2/vfeher/lysozyme/nmih/working6.py 

Additions are commented with 3 hashes (###) 

## Preparing your structures[edit](</mediawiki/index.php?title=Clustering&action=edit&section=3> "Edit section: Preparing your structures")]

To use the binding site shape clustering algorithm (found at Schrodinger's [script center](<http://schrodinger.com/scriptcenter>) as **volume_cluster.py**), you can start off like so: 

If you have a trajectory file, you will first want to extract the frames you would like to study first (or you can look at all of them). In my example I took every 50 frames from a 500,000 frame simulation, ending up with 10,000 individual .pdb files. Here is my ptraj script that I used to do that. 
    
    
    # ptraj script to extract structures from a trajectory
    
    # every 50 frames out of the 50000 are collected
    trajin amd1/amd1.nc 1 50000 50
    
    # centering the protein so coordinates are similar
    center :1-164 mass origin
    image origin center familiar
    
    # reference PDB file
    reference /extra/banzai2/nmih/0_md_T4LA/build/wet.pdb
    
    # backbone RMSD based on secondary structure elements: http://www.rcsb.org/pdb/explore.do?structureId=1l63
    rms reference out rmsd-to-wet_T4L_amd1_amd1.dat :3-11@CA,:13-19@CA,:25-29@CA,:31-34@CA,:39-50@CA,:60-80@CA,:84-90@CA,:94-123@CA,:126-135@CA,:137-141@CA,:143-155@CA,:158-161@CA name rmsd-avffit
    
    # strip out waters so file size is smaller
    strip :WAT
    
    # write to file
    trajout /extra/banzai2/nmih/0_md_T4LA/extract/amd1_amd1.pdb pdb
    go

One caveat here is that with ptraj all your files will be named as NAME.pdb.FRAME#. The next script that we will use/Maestro in general won't like these file extensions, so I just added another .pdb to the end of everything with a little line in bash: 
    
    
    for file in *; do mv "${file}" "${file}.pdb"; done

Yet another caveat is that the next script doesn't like those frame numbers if they skip (for example, since mine was every 50 frames every pdb file would be 1, 51, 101, etc). Thus a quick and dirty workaround for me was to: 

  1. Load all structures into Maestro
  2. Save this as one big .mae file



## Running SiteMap on all your structures[edit](</mediawiki/index.php?title=Clustering&action=edit&section=4> "Edit section: Running SiteMap on all your structures")]

Next, we wish to calculate the binding site volume of your protein of interest. There are three things that can happen here: 

  1. You know your binding site of interest and there is a ligand present from your simulation
  2. You know your binding site of interest but there is no ligand present in the simulation
  3. You do not know the binding site of interest



For all three options, you can use the script called **trajectory_binding_site_volumes.py** , again found at the script center (it doesn't need to be downloaded though as it is in the suite). This script hasn't been integrated into Maestro yet so it will have to be run from the command line. Also, I believe it requires Schrodinger 2013 to run. 

Just running `$SCHRODINGER/run trajectory_binding_site_volumes.py -h` will tell you about the options it takes. The interesting ones are: 

  * -is: which will take our combined structure .mae file and run sitemap on each one (great!)
  * -s_la: the option to use if you have a ligand present in your simulation
  * -s_sa: the option to use if you don't have a ligand present but you know your binding site.



The -s_sa option is what I used, and it takes an ASL as input (ex: res.num 1, 3, 5, 6). The way it works is that it takes this expression and puts a fake one atom ligand at the centroid of these residues. This could lead to inconsistencies in the location of the site SiteMap finds if the binding site is flexible -- something to think about. 

Anyway, to run it on a .mae file you would do the following from the command line: 
    
    
    $SCHRODINGER/run trajectory_binding_site_volumes.py -is $INPUT_FILE_OR_SERIES.mae -s_sa $DEFINE_BINDING_SITE

One thing about the version of the script currently provided is that it decides to look at one frame, wait until the job is finished, and move on to the next frame. This became a little slow so I made it semi-parallel in its action by modifying the script so it can submit multiple jobs at once (see **/extra/banzai2/nmih/trajectory_binding_site_volumes_mult.py**). What I did exactly was allow it to submit multiple jobs, and also wait until everything was done to combine the outputs into one file (there are maybe better ways to do it, one that comes to mind is to check if there is an output in every frame and then just add when there is an output). Something that might go wrong: if there are other jobs running not related to this project, it will not combine the output files into one final file at the end. This is because it waits until all jobs are done to combine the outputs -- I didn't have time to think about how to do this better unfortunately. Improvements are welcome! 

### Script information[edit](</mediawiki/index.php?title=Clustering&action=edit&section=5> "Edit section: Script information")]

To adjust SiteMap options you need to go digging around in the script itself. In the function **run_sitemap** there is a "cmd = [sitemap_exe,..." line where you can input the usual options SiteMap takes as input. One thing that might be important is the addition of a temporary directory, especially since the files might get mixed up if multiple SiteMap jobs are being submitted at once. So to add that (-TMPDIR): 
    
    
    cmd = [sitemap_exe, "-TMPDIR", "/scratch/nmih/sitemaps/" + str(index), "-j", job_name, "-prot", prepared_protein, "-ligmae", prepared_ligand, "-sitebox", str(sitebox), "-maxsites", str(maxsites) ]]

would create temporary directories organized by the index (the frame number). Other options that can be added can be found in the SiteMap manual or the Schrodinger Job Control Manual. If you are adding things just add the option name surrounded by quotes (ie. "-HOST") followed by a comma and then the option's input. 

Another option for SiteMap is down in the main function where you can adjust the "sitebox," which is the box around the ligand the function should search for what it thinks may be a potential binding site. 
    
    
    job = run_sitemap(sitemap_jobname, sitemap_input_protein, sitemap_input_ligand, 6.0, 1, index)

The 6.0 is the default sitebox, which means it will look 6.0 A around the defined ligand for any potentials. The 1 is for the number of sites it should return -- if you are just looking at one binding site you probably just want one result per frame. However, increasing this number may find other interesting sites. 

  


##### Volume clustering[edit](</mediawiki/index.php?title=Clustering&action=edit&section=6> "Edit section: Volume clustering")]

Once the script is done running, you will have as output: 

  * Numbered folders each with the SiteMap output for the frame (sitemap site, protein input, ligand input, and associated files)
  * A combined output file that has all sitemap sites (just the sites)



We can then use this combined output file to run the volume clustering. There are two options: run from the command line or run from Maestro. I chose the GUI route this time. 

The script is located under: [![Volclus1.png](/mediawiki/images/e/eb/Volclus1.png)](</mediawiki/index.php/File:Volclus1.png>) and to input your file, select "file": 

[![Volclus2.png](/mediawiki/images/1/1a/Volclus2.png)](</mediawiki/index.php/File:Volclus2.png>)

and then click on "calculate volume overlap matrix". This will create a bunch of files, the most useful being the .csv file which is the volume overlap matrix used. This calculation takes quite a while, but after it is done you can then calculate the clustering. 

[![Volclus3.png](/mediawiki/images/9/95/Volclus3.png)](</mediawiki/index.php/File:Volclus3.png>)

The three tabs for the clustering are: 

  * Calculate: there are different ways to cluster, none of which I got to play around with (just used average)
  * Results: tells you the best number of clusters it thinks you should do, and some pretty pictures.
  * Apply: actually clusters the structures into different files.



There are then different options under the apply tab: If you used an existing .csv file there will be 2 options: 

  * Create representative file: which will contain the representative structures of each cluster
  * Files for each cluster: which will output X number of files which each contain all structures of the corresponding cluster.



And if you used the files in the project table in Maestro, the options are pretty self explanatory. 

Unfortunately these files won't have the actual structure, just dots that represent the site that was found. Thus, you will have to go back to the SiteMap outputs or the original extracted files (the numbered frames may not match up however to the original frames) to get the structures for analysis. To do so, open up either the representative file or the cluster file, and then open up the Project Table. You'll want to click "Show Family" > "SiteMap All", and look for the trajectory frame number on the far right of the table: 

[![Cluster00.png](/mediawiki/images/e/eb/Cluster00.png)](</mediawiki/index.php/File:Cluster00.png>)

So if all went well you now have a group of structures to analyze!
