# for vmd

set PI 3.141592

proc ghostspin {filename n axis} {
  variable PI
  mol representation Licorice
  #makes a ghostly image as if the molecule were spinning
  set theta [expr "1.0 * $PI / $n"]
  set curmol [mol new $filename]
  mol representation Licorice
  mol modrep 0 $curmol
  
  for {set i 0} {$i < $n} {incr i} {
    # for each rotation
    
    # calculate our math
    set ourtheta [expr "$theta * $i"]
    puts "ourtheta : $ourtheta"
    # load our new molecule
    set curmol [mol new $filename]
    set sel [atomselect $curmol all]
    set ourcenter [measure center $sel]
    set rot [trans center $ourcenter axis $axis $ourtheta rad]
    
    $sel move $rot
    catch {material add "trans$i"}
    
    material change opacity "trans$i" [expr "(0.2/$n) * ($n - $i)"]
    #vmd_draw_arrow $curmol $ourcenter
    mol representation Licorice
    mol modrep 0 $curmol
    mol modmaterial 0 $curmol "trans$i"
    
  }
  return
}
    
proc draw_points_in_ellipse {molec a b c x y z increment} {
  set startx [expr "$x - $a"]
  set starty [expr "$y - $b"]
  set startz [expr "$z - $c"]
  set endx   [expr "$x + $a"]
  set endy   [expr "$y + $b"]
  set endz   [expr "$z + $c"]
  set counter 0
  
  set tempatomselection "index 0"
  set cutoff 3.0
  
  set tempatom [atomselect $molec $tempatomselection]
  set oldcoords [$tempatom get {x y z}]
  puts "oldcoords: $oldcoords"
  
  for {set i $startx} {$i <= $endx} {set i [expr "$i + 2"]} {
    for {set f $starty} {$f <= $endy} {set f [expr "$f + 2"]} {
      for {set g $startz} {$g <= $endz}  {set g [expr "$g + 2"]} {
        if {[expr "sqrt((($i - $x)**2 / ($a**2)) + (($f - $y)**2 / ($b**2)) + (($g - $z)**2) / ($c**2))"] <= 1.0 } {
          #puts [expr "sqrt((($i - $x)**2 / ($a**2)) + (($f - $y)**2 / ($b**2)) + (($g - $z)**2) / ($c**2))"]
          $tempatom set {x y z} [list "$i $f $g"]
          set closeatoms [atomselect $molec "not $tempatomselection and within $cutoff of $tempatomselection"]
          set closeindices [$closeatoms get index]
          if {[llength $closeindices] > 0} {continue} ;# then there are close atoms and we should not draw or count this point
          
          incr counter
          graphics $molec sphere "$i $f $g" radius 0.25 resolution 6
        }
      }
    }
  }
  $tempatom set {x y z} $oldcoords
  puts $counter
}

proc radial_to_cartesian {theta phi radius} {
  set x [expr "$radius * sin($theta) * cos($phi)"]
  set y [expr "$radius * sin($theta) * sin($phi)"]
  set z [expr "$radius * cos($theta)"]
  #puts "x: $x, y: $y, z: $z"
  return "$x $y $z"
}

proc open_dxfile {dxfilename} {
   #  Slurp up the data file
  set fp [open $dxfilename r]
  set file_data [read $fp]
  close $fp
  
   #  Process data file
   set data [split $file_data "\n"]
   set delta {}
   set mode "header"
   set dxdata {}
   set zline {}; set zcount 0
   set yline {}; set ycount 0
   set max -9999999999
   set min 9999999999
   foreach line $data {
     if {$mode == "header"} {
       if {[lrange $line 0 1] == "object 1"} { set counts [lrange $line 5 7] }
       if {[lindex $line 0] == "origin"} { set origin [lrange $line 1 3] }
       if {[lindex $line 0] == "delta"} {lappend delta [lindex $line [expr "1 + [llength $delta]"]]}
       if {[lrange $line 0 1] == "object 3"} {set mode "data"}
     } elseif {$mode == "data"} {
       if { ([lindex $line 0] == "object") || ([lindex $line 0] == "attribute") } {set mode "footer"; break}
       foreach entry $line {
         if {$entry < $min} {set min $entry}
         if {$entry > $max} {set max $entry}
         lappend zline $entry; incr zcount
         if {$zcount >= [lindex $counts 2]} {
           lappend yline $zline
           incr ycount
           set zcount 0
           set zline ""
         }
         if {$ycount >= [lindex $counts 1]} {
           lappend dxdata $yline
           incr xcount
           set ycount 0
           set yline ""
         }
         
       }
     }
   }
  #puts "origin: $origin"
  #puts "counts: $counts"
  #puts "delta: $delta"
  #puts "max: $max"
  #puts "min: $min"
  ##puts "dxdata: $dxdata"
  #puts "first row of data: [lindex $dxdata 0]" ;#[lindex [lindex $dxdata 0] 0]"
  return "{$origin} {$counts} {$delta} $max $min {$dxdata}"
}

proc get_dxvalue { dxset location {out_of_bounds 0.0}} {
  # given a point in space, will interpolate between the 4 closest data points
  set origin [lindex $dxset 0]
  set counts [lindex $dxset 1]
  set delta [lindex $dxset 2]
  set max [lindex $dxset 3]
  set min [lindex $dxset 4]
  set dxdata [lindex $dxset 5]
  #puts "origin: $origin"
  #puts "location: $location"
  # first check the bounds
  if { [lindex $location 0] < [lindex $origin 0] } { return $out_of_bounds }
  if { [lindex $location 1] < [lindex $origin 1] } { return $out_of_bounds }
  if { [lindex $location 2] < [lindex $origin 2] } { return $out_of_bounds }
  if { [lindex $location 0] > [vecadd [lindex $origin 0] [expr "([lindex $counts 0] - 1) * [lindex $delta 0]"] ] } { return $out_of_bounds }
  if { [lindex $location 1] > [vecadd [lindex $origin 1] [expr "([lindex $counts 1] - 1) * [lindex $delta 1]"] ] } { return $out_of_bounds }
  if { [lindex $location 2] > [vecadd [lindex $origin 2] [expr "([lindex $counts 2] - 1) * [lindex $delta 2]"] ] } { return $out_of_bounds }
  
  # find the 8 closest points
  set px [expr "([lindex $location 0] - [lindex $origin 0]) / [lindex $delta 0]"]
  set py [expr "([lindex $location 1] - [lindex $origin 1]) / [lindex $delta 1]"]
  set pz [expr "([lindex $location 2] - [lindex $origin 2]) / [lindex $delta 2]"]
  set p1x [expr "int(floor( $px ))"]
  set p1y [expr "int(floor( $py ))"]
  set p1z [expr "int(floor( $pz ))"]
  set weightedval 0.0
  set totaldist 0.0
  set skipval "False"
  foreach i "0 1" {
    if {$skipval == "True"} {break}
    foreach j "0 1" {
      if {$skipval == "True"} {break}
      foreach k "0 1" {
        set x [expr "$p1x + $i"]
        set y [expr "$p1y + $j"]
        set z [expr "$p1z + $k"]
        #puts "indeces: $x $y $z"
        set pointval [lindex [lindex [lindex $dxdata $x] $y] $z]
        
        set dist [vecdist "$x $y $z" "$px $py $pz"]
        #rputs "pointval: $pointval, dist: $dist"
        if {$dist < 0.00001} { ;# then the point lies right on a grid value
          set skipval "True"
          set totaldist 1.0
          set weightedval $pointval
          break
        } else {
          set weightedval [expr "$weightedval + ($pointval / $dist)"]
          set totaldist [expr "$totaldist + (1.0 / $dist)"]
        }
      }
    }
  }
  set val [expr "$weightedval / $totaldist"]
  
  #puts "p1: $p1x $p1y $p1z"
  #set p1val [lindex [lindex [lindex $dxdata $p1z] $p1y] $p1x]
  #puts "val: $val"
  return $val
}

proc draw_multicolored_sphere {molec dxfile x y z radius {mincolor 0} {resolution 256} {colorfactor 1.0}} {
  global PI
  set mincolor 33
  set maxcolor 1056
  # load dx file
  set dxset [open_dxfile $dxfile]
  set origin [lindex $dxset 0]
  set counts [lindex $dxset 1]
  set delta [lindex $dxset 2]
  set max [lindex $dxset 3]
  set min [lindex $dxset 4]
  set dxdata [lindex $dxset 5]
  # draws a sphere whose facets are colored by a dx file
  set dtheta [expr "$PI / $resolution"]
  set oldtheta 0.0 ;# the last row's theta value
  for {set i [expr "$oldtheta + $dtheta"]} {$i < $PI} {set i [expr "$i + $dtheta"]} {
    set oldphi 0.0
    for {set f $dtheta} {$f < [expr "2.0 * $PI + $dtheta"]} {set f [expr "$f + $dtheta"]} {
      # draw two triangles
      set p1 [vecadd "$x $y $z" [radial_to_cartesian $i $f $radius]]
      set p2 [vecadd "$x $y $z" [radial_to_cartesian $i $oldphi $radius]]
      set p3 [vecadd "$x $y $z" [radial_to_cartesian $oldtheta $f $radius]]
      set p4 [vecadd "$x $y $z" [radial_to_cartesian $oldtheta $oldphi $radius]]
      set midpoint [vecscale [vecadd [vecadd $p1 $p4] [vecadd $p2 $p3]] 0.25]
      set val [get_dxvalue $dxset $midpoint]
      set colorval [expr "$colorfactor * (($val - $min) / ($max - $min)) * ($maxcolor - $mincolor) + $mincolor"]
      if {$colorval > $maxcolor} {set colorval $maxcolor}
      # ADJUST GRAPHICS COLOR
      if {($colorval > $mincolor) && ([lindex $midpoint 2] > -2.9)} {
        graphics $molec color $colorval
        graphics $molec triangle $p1 $p2 $p3
        graphics $molec triangle $p2 $p4 $p3
        #graphics $molec color red
        #graphics $molec sphere $midpoint radius 0.5
      }
      set oldphi $f
    }
    set oldtheta $i
  }
}
