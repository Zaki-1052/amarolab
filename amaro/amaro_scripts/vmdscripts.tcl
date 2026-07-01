#Name: 
# animatepdbs 
#Synopsis:
#  A Tcl script to load a consecutively numbered 
#  sequence of PDB files into VMD for animation purposes.
#Version:
# 1.0
#Uses VMD Version:
# 1.1
#Parameters:
#  start  - "frame number" of first PDB file in sequence
#  end    - "frame number" of last PDB file in sqeuence
#  format - a Tcl format string which describes the filename/numbering
#           used.
#
#Examples:
#  To load a sequence of PDB files named 0.pdb 1.pdb 2.pdb 3.pdb 
#  one would call this proc with:  animatepdbs 0 3 "%d.pdb"
#
#  To load a sequence of PDB files named foo0000.pdb foo0001.pdb foo0002.pdb
#  one would call this proc with:  animatepdbs 0 2 "foo%04d.pdb"
#
#Author:
# John Stone $lt;johns@ks.uiuc.edu&gt;
#

source ~/src/vmdplugins/la1.0/la.tcl

proc animatepdbs {start end fileformat {stride 1}} {
  #loads a series of pdbs in like a trajectory
  #input: 
  #  start: first number in the numbered pdbs
  #  end: last number in the numbered pdbs
  #  fileformat: the name of the pdb files, with a %0(n)d representing the number (NOTE: "n" refers to the field length)
  set filename [format $fileformat [expr $start]]
  puts "Reading initial frame in PDB sequence $filename. Stride: $stride"
  mol load pdb $filename

  puts "Reading PDB files as an animation..."
  for {set i $start} {$i <= $end} {set i [expr {$i + $stride}]} {
    puts "i: $i"
    set filename [format $fileformat [expr $i]]
    puts "filename: $filename"
    animate read pdb $filename
  }
}


##########################################################################################################################

proc setbetatouser {fname} {
  #get the number of frames
  set num_frames [molinfo $fname get numframes]
  set all [atomselect top "all"]
  set occupancy {}
  
  #we've got to reset everything
  set num_atoms [molinfo $fname get numatoms]
  for {set f 0} {$f < $num_atoms} {incr f} {
    set cur [atomselect top {index $f}]
    $cur set occupancy 0
    $cur set user2 0
  }  
  
  for {set i 0} {$i < $num_frames} {incr i} {
    #now for each atom, we have to get the occupancy and append it to a list
    $all frame $i
    #set all [atomselect top "all"]
    set occupancy [$all get occupancy]
    #set num_atoms [molinfo $fname get numatoms]
    #for {set f 0} {$f < $num_atoms} {incr f} {
    #  set cur [atomselect top {index $f}]
    #  $cur get occupancy
    #  lappend occupancy [$cur]
    #}
    #we now have a list of all occupancies
    #if {[expr $i % 2] == 0} {
      $all set user2 $occupancy
    #} #else {
      #$all set user 0
    #}
  }
}

############################################################################
proc find_traj_center {gr_mol selection} {
  #this function finds the center of mass of an atom selection over the course of a trajectory
  #input:
  #  gr_mol: index for the molecule in question
  #  selection: atoms we are finding the center of mass for
  #output:
  #  writes the coords for the avg position
  # make the list of coordinates
  set num_frames [molinfo $gr_mol get numframes]
  set coords {}
  for {set i 0} {$i < $num_frames} {incr i} {
    $selection frame $i
    #$selection update
    # compute the center of mass and save it on the list
    lappend coords [measure center $selection weight mass]
  }
  #and now a loop to run through the entire list, add them up, and divide the length of the list
  set sum {0 0 0}
  for {set i 0} {$i < $num_frames} {incr i} {
    #run through every element of the coords list 
    set curvec [lindex $coords $i]
    set sum [vecadd $curvec $sum]
  }
  set scale [expr 1.0/$num_frames]
  set avgvec [vecscale $scale $sum]
  puts $avgvec  
  
}
#########################################################################

proc drawdots {gr_mol selection {rescolor 4} {filename 0}} {
  #for every frame in a trajectory, a dot will be drawn/saved at the 
  #center of mass for "selection"
  #input:
  #  gr_mol: the molecule number
  #  selection: the atoms representing what we get the center of mass for
  #  filename: the name of the file where coords for the dots will go
  #output:
  #  draws dots on the screen
  #  outputs a file
  
  #change color
  graphics top color $rescolor
  puts Mark1
  #create the file
  if {$filename != 0} { set destfile [open $filename w]}
  puts Mark2
  set num_frames [molinfo $gr_mol get numframes]
  #loop through the entire trajectory
  for {set i 0} {$i < $num_frames} {incr i} {
    $selection frame $i
    #selection now has been updated for frame i
    #draw the point
    set coords [measure center $selection weight mass]
    #puts $coords
    graphics top point $coords
    #write to the file, if one is specified
    if {$filename != 0} {
      puts $destfile "$coords"
    }
  }
  close $destfile
}

proc morph_linear {t N} {
  return [expr {double($t) / double($N)}]
}
proc morph_cycle {t N} {
  global M_PI
  return [expr {(1.0 - cos( $M_PI * double($t) / ($N + 1.0)))/2.0}]
}
proc morph_sin2 {t N} {
  global M_PI
  return [expr {sqrt(sin( $M_PI * double($t) / double($N) / 2.0))}]
}

######################################################################################################

proc morph {molid N {morph_type morph_linear}} {
    # make sure there are only two animation frames
    if {[molinfo $molid get numframes] != 2} {
	error "Molecule $molid must have 2 animation frames"
    }
    # workaround for the 'animate dup' bug; this will translate
    # 'top' to a number, if needed
    set molid [molinfo $molid get id]

    # Do some error checking on N
    if {$N != int($N)} {
	  error "Need an integer number for the number of frames"
    }
    if {$N <= 2} {
	  error "The number of frames must be greater than 2"
    }

    # Get the coordinates of the first and last frames (there are only 2)
    set sel1 [atomselect $molid "all" frame 0]
    set sel2 [atomselect $molid "all" frame 1]
    set x1 [$sel1 get x]
    set y1 [$sel1 get y]
    set z1 [$sel1 get z]
    set x2 [$sel2 get x]
    set y2 [$sel2 get y]
    set z2 [$sel2 get z]

    # Make N-2 new frames (copied from the last frame)
    for {set i 2} {$i < $N} {incr i} {
	  animate dup frame 1 $molid
    }
    # there are now N frames

    # Do the linear interpolation in steps of 1/N so
    # f(0) = 0.0 and f(N-1) = 1.0
    for {set t 0} {$t < $N} {incr t} {
	  # Here's the call to the user-defined morph function
	  set f [$morph_type $t $N]
	  # calculate the linear interpolation for each coordinate
	  # go to the given frame and set the coordinates
	  $sel1 frame $t
      $sel1 set x [vecadd [vecscale [expr {1.0 - $f}] $x1] [vecscale $f $x2]]
      $sel1 set y [vecadd [vecscale [expr {1.0 - $f}] $y1] [vecscale $f $y2]]
      $sel1 set z [vecadd [vecscale [expr {1.0 - $f}] $z1] [vecscale $f $z2]]
   } 
}

proc planar_regression {atomsel {dep_axiz z}} {
  # given an atomselection, will calculate and draw a planar regression
  set allcoords [$atomsel get {x y z}]
  set sumx2 0.0
  set sumy2 0.0
  set sumxy 0.0
  set sumxz 0.0
  set sumyz 0.0
  set sumx 0.0
  set sumy 0.0
  set sumz 0.0
  set n [llength $allcoords]
  foreach coord $allcoords {
    set x [lindex $coord 0]
    set y [lindex $coord 1]
    set z [lindex $coord 2]
    set sumx2 [expr "$sumx2 + ($x ** 2)"]
    set sumy2 [expr "$sumy2 + ($y ** 2)"]
    set sumxy [expr "$sumxy + ($x * $y)"]
    set sumxz [expr "$sumxz + ($x * $z)"]
    set sumyz [expr "$sumyz + ($y * $z)"]
    set sumx [expr "$sumx + $x"]
    set sumy [expr "$sumy + $y"]
    set sumz [expr "$sumz + $z"]
  }
  # matrix A: 3x3 matrix
  set A "2 3 3 $sumx2 $sumxy $sumx $sumxy $sumy2 $sumy $sumx $sumy $n"
  set b "2 3 1 $sumxz $sumyz $sumz"
  #show $A
  #show $b
  set soln [La::msolve $A $b]
  return [lrange $soln 3 end]
}

proc draw_planar_regress {atomsel {width 50} {zoffset 0.0}} {
  set soln [planar_regression $atomsel]
  puts "regression values: $soln"
  set a [lindex $soln 0]
  set b [lindex $soln 1]
  set c [expr "[lindex [measure center $atomsel weight [$atomsel get mass]] 2] + $zoffset"] ;#[lindex $soln 2]
  set z1 [expr "$a * -$width + $b * -$width + $c"]
  set z2 [expr "$a * -$width + $b * $width + $c"]
  set z3 [expr "$a * $width + $b * -$width + $c"]
  set z4 [expr "$a * $width + $b * $width + $c"]
  draw triangle "-$width -$width $z1" "-$width $width $z2" "$width -$width $z3" 
  draw triangle "$width $width $z4" "-$width $width $z2" "$width -$width $z3" 
  
}

proc trajectory_planar_regress {atomsel } {
  set planes {}
  set sel_frame [$atomsel frame]
  set gr_mol [$atomsel molindex]
  set num_frames [molinfo $gr_mol get numframes]
  for {set i 0} {$i < $num_frames} {incr i} {
    $atomsel frame $i
    lappend [planar_regression $atomsel]
    draw_planar_regress $atomsel
  }
}
