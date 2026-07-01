# Useful TCL scripts for analyzing trajectory data

set PI [expr "acos(-1)"] ;# pi

proc get_number_of_frames {sel} {
  # given an atomselection, will return the number of frames that the molecule object has
  set our_molid [$sel molid]
  return [molinfo $our_molid get numframes]
}

proc range {start finish step} {
  # generates a range of numbers between 'start' and 'finish' with an increment of 'step'
  set rangelist {}
  for {set i $start} {$i < $finish} {set i [expr "$i + $step"]} {
    lappend rangelist $i
  }
  return $rangelist
}



proc velocity_dist {veltraj {lower -0.02} {upper 0.02} {interval 0.0005} } {
  # given a velocity trajectory 'veltraj', will generate a x,y,z velocity distribution between 'lower' and 'upper' with bins of size 'interval'
  set half_interval [expr "$interval / 2.0"] ;# we are going to bin by a half interval in order to get the closest number we are trying to approximate
  set numbins [expr "($upper - $lower) / $interval"]
  set count_dist []
  for {set i 0} {$i <= $numbins} {incr i} {lappend count_dist "0"} ;# create an empty list of bins
  set N [$veltraj num] ;# number of atoms in veltraj
  set numframes [get_number_of_frames $veltraj]
  for {set i 0} {$i < $numframes} {incr i} { ;# for every frame
    if {[expr "$i % 100"] == 0} {puts "now analyzing frame $i"}
    $veltraj frame $i
    set vels [concat [$veltraj get x] [$veltraj get y] [$veltraj get z]] ;# include x, y, and z together
    foreach vel $vels {
      set place [expr "int(($vel + half_interval - $lower) / $interval)"]
      lset count_dist $place [expr "1 + [lindex $count_dist $place]"]
    }
  
  }
  return $count_dist
}

proc pair_distribution { traj edgesize {numframes 1000} {upper 12.0} {interval 0.01} } {
  # given a position trajectory 'traj', will generate a pair distribution function between 0.0 and 'upper' with bins of size 'interval'. 'edgesize' gives the width of one edge of the cube. 'upper' is the maximum distance between two atoms that will be evaluated for the distribution.
  global PI
  set V [expr "$edgesize * $edgesize * $edgesize"] ;# volume of box
  set numbins [expr "$upper / $interval"]
  set count_dist [] ;# these are the two distributions
  set g []
  for {set i 0} {$i <= $numbins} {incr i} {lappend count_dist "0"; lappend g "0"} ;# create empty bins
  set N [$traj num] ;# number of atoms in veltraj
  set totalframes [get_number_of_frames $traj] ;# total number of frames in molecule
  set counter 0
  set startframe 0
  for {set i $startframe} {$i < $totalframes} {set i [expr "$i + (($totalframes-$startframe) / $numframes)"]} { ;# walk thru the frames
    puts "now analyzing frame $i"
    $traj frame $i
    set x0 [$traj get x]
    set y0 [$traj get y]
    set z0 [$traj get z]
    for {set j 0} {$j < $N} {incr j} { ;# pick an atom
      if {([lindex $x0 $j] < [expr "0.0 + $upper"]) || ([lindex $y0 $j] < [expr "0.0 + $upper"]) || ([lindex $z0 $j] < [expr "0.0 + $upper"])} {continue}
      if {([lindex $x0 $j] > [expr "34.7786 - $upper"]) || ([lindex $y0 $j] > [expr "34.7786 - $upper"]) || ([lindex $z0 $j] > [expr "34.7786 - $upper"])} {continue} ;# if there are going to be edge effects because we will be looking at atoms that are further than the closest point on an edge of the box, then we have to skip this atom
      set refpos "[lindex $x0 $j] [lindex $y0 $j] [lindex $z0 $j]" ;# position of our reference atom
      set addedone False ;# to see whether we have even counted this reference atom
      for {set k 0} {$k < $N} {incr k} { ;# loop thru other atoms to see if we can plot the interatomic distance
        if {$j == $k} {continue}
        set otherpos "[lindex $x0 $k] [lindex $y0 $k] [lindex $z0 $k]" ;# position of the other atom
        #if {[expr "[lindex $refpos 0] - [lindex $otherpos 0]"] > $upper} { lset otherpos 0 [expr "[lindex $otherpos 0] + $edgesize"]} ;# in case we want to move atoms to the other side for periodic boundary; we don't right now
        #if {[expr "[lindex $refpos 1] - [lindex $otherpos 1]"] > $upper} { lset otherpos 1 [expr "[lindex $otherpos 1] + $edgesize"]}
        #if {[expr "[lindex $refpos 2] - [lindex $otherpos 2]"] > $upper} { lset otherpos 2 [expr "[lindex $otherpos 2] + $edgesize"]}
        #if {[expr "-[lindex $refpos 0] + [lindex $otherpos 0]"] < $upper} { lset otherpos 0 [expr "[lindex $otherpos 0] - $edgesize"]}
        #if {[expr "-[lindex $refpos 1] + [lindex $otherpos 1]"] < $upper} { lset otherpos 1 [expr "[lindex $otherpos 1] - $edgesize"]}
        #if {[expr "-[lindex $refpos 2] + [lindex $otherpos 2]"] < $upper} { lset otherpos 2 [expr "[lindex $otherpos 2] - $edgesize"]}
        set pairdist [vecdist $refpos $otherpos] ;# measure distance between the two atoms
        set place [expr "round($pairdist / $interval)"]
        if { $pairdist >= $upper } {continue}
        set addedone True ;# we have counted this reference atom, so we can consider its influence
        lset count_dist $place [expr "1 + [lindex $count_dist $place]"]
        
      }
      if {$addedone == True} {incr counter} ;# if we've actually used this atom, then increment the counter
    }
  }
  
  puts " now we have the distribution of counts, need to get the radial distribution function"
  set r 0.0
  set i 0
  # now we have to convert the count distribution to a radial distribution
  foreach entry $count_dist {
    if {($entry == 0) || ($r == 0)} {
      set g_entry 0.0 
    } else {
      set g_entry [expr "($V/($N * $counter)) * ($entry / (4 * $PI * $r * $r * $interval))"]
    }    
    lset g $i $g_entry
    set r [expr "$r + $interval"]
    incr i
  }
  
  return $g ;# return the radial distribution
}

proc mean_value_displacement {traj ourtime n} {
  # finds the mean value of the even power 'n' of the displacements
  # given a velocity trajectory and time, will calculate the velocity autocorrelation function for each particle
  set starttime 0
  set numframes 10 ;#[expr "[get_number_of_frames $veltraj] - $time - 1"]
  set mvpsum 0.0
  set curtime 0
  set N [$traj num] ;# number of atoms in veltraj
  set totalframes [get_number_of_frames $traj] ;# total number of frames in molecule
  
  for {set f $starttime} {$f < $totalframes} {set f [expr "$f + (($totalframes-$starttime) / $numframes)"]} {
    set nexttime [expr "$f + $ourtime"]
    
    $traj frame $f
    set x0 [$traj get x]
    set y0 [$traj get y]
    set z0 [$traj get z]
    $traj frame $nexttime
    set x1 [$traj get x]
    set y1 [$traj get y]
    set z1 [$traj get z]
    
    for {set i 0} {$i < $N} {incr i} {
      set vec0 "[lindex $x0 $i] [lindex $y0 $i] [lindex $z0 $i]"
      set vec1 "[lindex $x1 $i] [lindex $y1 $i] [lindex $z1 $i]"
      set diff [vecsub $vec0 $vec1 ]
      set even_power [expr "pow([veclength2 $diff],$n)"]
      set mvpsum [expr "$mvpsum + $even_power"]
    }
  }
  
  return [expr "$mvpsum / ($N*$numframes)"]
}

proc velocity_autocorrelation {veltraj ourtime} {
  # given a velocity trajectory and time, will calculate the velocity autocorrelation function for each particle
  #set trajlen [$veltraj frames]
  set starttime 100
  set numframes 10 ;#[expr "[get_number_of_frames $veltraj] - $time - 1"]
  set velsum 0.0
  set N [$veltraj num] ;# number of atoms in veltraj
  for {set curtime 0} {$curtime < $numframes} {incr curtime} {
    #puts "now working on time: $curtime"
    set nexttime [expr "$starttime + $curtime + $ourtime"]
    # get the coordinates at time 0 and time 'ourtime'
    $veltraj frame [expr "$starttime + $curtime"]
    set x0 [$veltraj get x]
    set y0 [$veltraj get y]
    set z0 [$veltraj get z]
    $veltraj frame $nexttime
    set x1 [$veltraj get x]
    set y1 [$veltraj get y]
    set z1 [$veltraj get z]
    #puts "nexttime: $nexttime"
    for {set i 0} {$i < $N} {incr i} {
      #puts "{[lindex $x0 $i] [lindex $y0 $i] [lindex $z0 $i]} {[lindex $x1 $i] [lindex $y1 $i] [lindex $z1 $i]}"
      set vec0 "[lindex $x0 $i] [lindex $y0 $i] [lindex $z0 $i]"
      #puts "veclens: [llength $x1] [llength $y1] [llength $z1]"
      #puts "vec1: [lindex $x1 $i] [lindex $y1 $i] [lindex $z1 $i]"
      set vec1 "[lindex $x1 $i] [lindex $y1 $i] [lindex $z1 $i]"
      set veclen [expr "([veclength $vec0] * [veclength $vec1])"]
      if { $veclen == 0.0} { 
        set dot 0.0
      } else {
        set dot [expr "[vecdot $vec0 $vec1 ] / $veclen"]
      }
      #"dot: $dot"
      #puts "velsum: $velsum"
      set velsum [expr "$velsum + $dot"]
     }
  }
  #puts "N & numframes: $N * $numframes)"
  set correl [expr "$velsum / ($N * $numframes)"]
  return $correl
}

proc time_dependent_pair_correlation {traj edgesize ourtime {interval 0.01}} {
  # given a position trajectory, will find the pair correlation function G(r,t); if at time 'time' n(r,t) particles are situated at a distance between r and r+dr from the position that was occupied by a certain atom at time 0
  set numframes 100
  set V [expr "$edgesize * $edgesize * $edgesize"]
  set upper 12.0 ;#[expr "$edgesize / 2.0"]
  set starttime 0
  global PI
  set numbins [expr "int($upper / $interval)"]
  puts "numbins: $numbins"
  set count_dist []
  set g []
  for {set i 0} {$i <= $numbins} {incr i} {lappend count_dist "0"; lappend g "0"} ;# create an empty list of bins
  
  set N [$traj num] ;# number of atoms in veltraj
  set totalframes [get_number_of_frames $traj]
  
  set counter 0
  
  for {set i $starttime} {$i < [expr "$totalframes - $ourtime"]} {set i [expr "$i + (($totalframes-$ourtime) / $numframes)"]} {
    puts "now analyzing frame $i"
    set t [expr "$i + $ourtime"]
    $traj frame $i
    set x0 [$traj get x]
    set y0 [$traj get y]
    set z0 [$traj get z]
    $traj frame $t
    set x1 [$traj get x]
    set y1 [$traj get y]
    set z1 [$traj get z]
    
    for {set j 0} {$j < $N} {incr j} {
      if {([lindex $x0 $j] < [expr "0.0 + $upper"]) || ([lindex $y0 $j] < [expr "0.0 + $upper"]) || ([lindex $z0 $j] < [expr "0.0 + $upper"])} {continue}
      if {([lindex $x0 $j] > [expr "34.7786 - $upper"]) || ([lindex $y0 $j] > [expr "34.7786 - $upper"]) || ([lindex $z0 $j] > [expr "34.7786 - $upper"])} {continue}
      set refpos "[lindex $x0 $j] [lindex $y0 $j] [lindex $z0 $j]" ;# position of our reference
      set addedone False
      for {set k 0} {$k < $N} {incr k} {
        if {$j == $k} {continue}
        set otherpos "[lindex $x1 $k] [lindex $y1 $k] [lindex $z1 $k]" ;# position of the other atom
        #puts "refpos - otherpos: [lindex $refpos 0] - [lindex $otherpos 0]"
        #if {[expr "[lindex $refpos 0] - [lindex $otherpos 0]"] > $upper} { lset otherpos 0 [expr "[lindex $otherpos 0] + $edgesize"]}
        #if {[expr "[lindex $refpos 1] - [lindex $otherpos 1]"] > $upper} { lset otherpos 1 [expr "[lindex $otherpos 1] + $edgesize"]}
        #if {[expr "[lindex $refpos 2] - [lindex $otherpos 2]"] > $upper} { lset otherpos 2 [expr "[lindex $otherpos 2] + $edgesize"]}
        #if {[expr "-[lindex $refpos 0] + [lindex $otherpos 0]"] > $upper} { lset otherpos 0 [expr "[lindex $otherpos 0] - $edgesize"]}
        #if {[expr "-[lindex $refpos 1] + [lindex $otherpos 1]"] > $upper} { lset otherpos 1 [expr "[lindex $otherpos 1] - $edgesize"]}
        #if {[expr "-[lindex $refpos 2] + [lindex $otherpos 2]"] > $upper} { lset otherpos 2 [expr "[lindex $otherpos 2] - $edgesize"]}
        set pairdist [vecdist $refpos $otherpos] ;# measure distance between the two atoms
        set place [expr "round($pairdist / $interval)"]
        if { $place >= $numbins } {continue}
        set addedone True
        lset count_dist $place [expr "1 + [lindex $count_dist $place]"]
        
        
      }
      if {$addedone == True} {incr counter} ;# if we've actually used this atom, then increment the counter
    }
  }
  set r 0.0
  set i 0
  # now we have to convert the count distribution to a radial distribution
  foreach entry $count_dist {
    if {($entry == 0) || ($r == 0)} {
      set g_entry 0.0 
    } else {
      set g_entry [expr "($V/($N * $counter)) * ($entry / (4 * $PI * $r * $r * $interval))"]
    }    
    lset g $i $g_entry
    set r [expr "$r + $interval"]
    incr i
  }
  
  return $g
}
