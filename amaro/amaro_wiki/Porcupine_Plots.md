# Porcupine Plots

## Perform the Principle Component Analysis[edit](</mediawiki/index.php?title=Porcupine_Plots&action=edit&section=1> "Edit section: Perform the Principle Component Analysis")]

I use _ptraj_ , part of the Amber package. First, I create an _ptraj_ input file called _step1.ptraj_ that looks like this: 
    
    
    trajin mydcd.dcd
    rms first @CA
    matrix covar @CA name mcovar
    analyze matrix mcovar out evec.pev vecs 25
    go 
    

I then run _ptraj_ using this input file: 
    
    
     $AMBERHOME/exe/ptraj myparam.prmtop < step1.ptraj
    

This produces a file called _evec.pev_. 

## Generate the Average Structure[edit](</mediawiki/index.php?title=Porcupine_Plots&action=edit&section=2> "Edit section: Generate the Average Structure")]

I also use _ptraj_ to generate the average structure from the trajectory. Here's the input file, called _get_average.ptraj_ : 
    
    
    trajin mydcd.dcd
    average average.pdb pdb
    go
    

I then run _ptraj_ using this input file: 
    
    
    $AMBERHOME/exe/ptraj myparam.prmtop < get_average.ptraj
    

This generates an average structure, _average.pdb_. 

## PHP Script to Generate TCL Script that Draws Porcupine Plot[edit](</mediawiki/index.php?title=Porcupine_Plots&action=edit&section=3> "Edit section: PHP Script to Generate TCL Script that Draws Porcupine Plot")]

Here's a PHP script I wrote to generate the porcupine plots: 
    
    
    <?php 
    
    error_reporting(0);
    ini_set("memory_limit","12M");
    
    if (($argv[1]=='') || ($argv[2]=='')) {
        echo 'FILE.php {EIGEN.FILE} {EIGEN.INDEX}'."\n";die();
    }
    
    $file=file_get_contents($argv[1]);
    
    $file=explode('****',$file);
    
    //First, process the initial coordinates
    $file[0]=explode("\n",$file[0]);
    $file[0][0]='';
    $file[0][1]='';
    $file[0]=trim(implode("\n",$file[0]));
    
    while (strstr($file[0],'  ')) {
        $file[0]=str_replace('  ',' ',$file[0]);
    }
    
    $file[0]=str_replace("\n "," ",$file[0]);
    
    $file[0]=explode(" ",$file[0]);
    $orig=array();
    $count=0;
    for ($t=0;$t<count($file[0]);$t=$t+3) {
        $orig[$count]['x']=$file[0][$t];
        $orig[$count]['y']=$file[0][$t+1];
        $orig[$count]['z']=$file[0][$t+2];
        $count++;
    }
    
    for ($t=0;$t<count($orig);$t++) {
        echo 'draw sphere {'.$orig[$t]['x'].' '.$orig[$t]['y'].' '.$orig[$t]['z'].'} radius 2 resolution 50'."\n";
    }
    
    //Now process each of the eigenvectors
    $eigen=array();
    $count1=0;
    for ($t=1;$t<count($file);$t++) {
        $file[$t]=explode("\n",$file[$t]);
        $file[$t][0]='';
        $file[$t][1]='';
        $file[$t]=trim(implode(" ",$file[$t]));
        while (strstr($file[$t],'  ')) {
                $file[$t]=str_replace('  ',' ',$file[$t]);
        }
    
        $file[$t]=explode(" ",$file[$t]);
        $count2=0;
        for ($s=0;$s<count($file[$t]);$s=$s+3) {
                $eigen[$count1][$count2]['x']=$file[$t][$s];
                $eigen[$count1][$count2]['y']=$file[$t][$s+1];
                $eigen[$count1][$count2]['z']=$file[$t][$s+2];
                $count2++;
        }
    
        $count1++;
    }
    
    $index=$argv[2]-1;
    
    $arrow_scale=25;
    $new=array();
    for ($t=0;$t<count($eigen[$index]);$t++) {
        $new['x']=$orig[$t]['x']+$arrow_scale*$eigen[$index][$t]['x'];
            $new['y']=$orig[$t]['y']+$arrow_scale*$eigen[$index][$t]['y'];
            $new['z']=$orig[$t]['z']+$arrow_scale*$eigen[$index][$t]['z'];
    
        $normalize_fact=2/sqrt(pow($eigen[$index][$t]['x'],2)+pow($eigen[$index][$t]['y'],2)+pow($eigen[$index][$t]['z'],2));
        $point_tip['x']=$new['x']+$normalize_fact*$eigen[$index][$t]['x'];
            $point_tip['y']=$new['y']+$normalize_fact*$eigen[$index][$t]['y'];
            $point_tip['z']=$new['z']+$normalize_fact*$eigen[$index][$t]['z'];
    
    echo 'draw cylinder {'.$orig[$t]['x'].' '.$orig[$t]['y'].' '.$orig[$t]['z'].'} {'.$new['x'].' '.$new['y'].' '.$new['z'].'} radius 0.5 resolution 50'."\n";
    
    echo 'draw cone {'.$new['x'].' '.$new['y'].' '.$new['z'].'} {'.$point_tip['x'].' '.$point_tip['y'].' '.$point_tip['z'].'} radius 0.75 resolution 50'."\n";
    }
    ?>
    

To run this script, type in 
    
    
    php make_porcupine_tcl.php evec.pev # > draw_porc.tcl
    

where '#' is the number of the PCA mode you wish to visualize (1 being the mode corresponding to the largest eigenvector). Note that you can also modify the _$arrow_scale_ variable, which modifies the length of the "spines" of the porcupine plot. 

## Visualizing the Porcupine Plots[edit](</mediawiki/index.php?title=Porcupine_Plots&action=edit&section=4> "Edit section: Visualizing the Porcupine Plots")]

  * Open up the average structure in VMD. Change the appearance of the protein as desired through the _Graphical Representations_ window.
  * Click on the _Extensions_ menu, then the _Tk Console_ item.
  * Within the _Tk Console_ , type in source _draw_porc.tcl_.



Your porcupine plot will appear. 

## Additional Comments[edit](</mediawiki/index.php?title=Porcupine_Plots&action=edit&section=5> "Edit section: Additional Comments")]

You can also modify the _draw_porc.tcl_ file in your favorite text editor like _gedit_. The blue spheres placed at the alpha carbons could be deleted, for example, or their radii could be modified.
