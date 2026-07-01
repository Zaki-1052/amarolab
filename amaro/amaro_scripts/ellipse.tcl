## 
## Contributed by chris forman <cjf41@cam.ac.uk>
##

proc f {a u v} {
  expr {$a*sin($u) * cos($v)} 
}  

proc g {b u v} {
  expr {$b*cos($u) * cos($v)}
}

proc h {c u v} {
  expr {$c*sin($v)} 
}

# a = semi-axis in x direction
# b = semi-axis in y direction
# c = semi-axis in z direction
# phi = first rotation about z axis in xy plane  [see http://mathworld.wolfram.com/EulerAngles.html]
# theta = second rotation about x axis in zy plane.
# psi = third rotation about z' axis in x'y' plane.
# x = translation in x direction.
# y = translation in y direction
# z = translation in z direction
# eColour is the colour of the ellipse in VMD colour table.

proc draw_ellipsoid { a b c phi theta psi x y z eColour} {
  set PI 3.14159
  set phi [expr $phi*$PI/180]
  set theta [expr $theta*$PI/180]
  set psi [expr $psi*$PI/180]

  set minu 0
  set maxu [expr $PI * 2]
  set stepu [expr $maxu / 50]
  set minv [expr -1*$PI]
  set maxv [expr $PI]
  set stepv [expr $maxv / 50]

  # first, get the data (this isn't the most data efficient way of   
  # doing things)   
  for {set u $minu} {$u <= $maxu} {set u [expr $u + $stepu]} {
    for {set v $minv} {$v <= $maxv} {set v [expr $v + $stepv]} {
      set fdata($u,$v) [f $a $u $v]
      #puts $u 
      #puts $v
      set gdata($u,$v) [g $b $u $v]
      set hdata($u,$v) [h $c $u $v]     
    }
  }

  # compute rotation matrix to get desired orientation
  set a11 [expr {cos($psi)*cos($phi)-cos($theta)*sin($phi)*sin($psi)}]
  set a12 [expr {cos($psi)*sin($phi)+cos($theta)*cos($phi)*sin($psi)}]
  set a13 [expr {sin($psi)*sin($theta)}]
  set a21 [expr {-1*sin($psi)*cos($phi)-cos($theta)*sin($phi)*cos($psi)}]
  set a22 [expr {-1*sin($psi)*sin($phi)+cos($theta)*cos($phi)*cos($psi)}]
  set a23 [expr {cos($psi)*sin($theta)}]
  set a31 [expr {sin($theta)*sin($phi)}]
  set a32 [expr {-1*sin($theta)*cos($phi)}]
  set a33 [expr {cos($theta)}]

  #perform rotation and translation
  for {set u $minu} {$u <= $maxu} {set u [expr $u + $stepu]} {
    for {set v $minv} {$v <= $maxv} {set v [expr $v + $stepv]} {
      set fdata_r($u,$v) [expr {($fdata($u,$v)*$a11+$gdata($u,$v)*$a21+$hdata($u,$v)*$a31) + $x}]       
      set gdata_r($u,$v) [expr {($fdata($u,$v)*$a12+$gdata($u,$v)*$a22+$hdata($u,$v)*$a32) + $y}]
      set hdata_r($u,$v) [expr {($fdata($u,$v)*$a13+$gdata($u,$v)*$a23+$hdata($u,$v)*$a33) + $z}]
      #puts "u: $u, v: $v, fdata_r: $fdata_r($u,$v), gdata_r: $gdata_r($u,$v), hdata_r: $hdata_r($u,$v)"
      if {$u == 0.1256636} {puts $v}
    }
  }

  # make another pass through to plot it   
  set cnum [colorinfo num]
  set cmax [colorinfo max]
  draw color $eColour
  for {set u $minu} {$u < $maxu} {set u [expr $u + $stepu]} {
    for {set v $minv} {$v < $maxv} {set v [expr $v + $stepv]} {
      # get the next two corners       
      set u2 [expr $u + $stepu]
      set v2 [expr $v + $stepv]
      if {$u2 > $PI} {set u2 [expr "($u2 - $PI) / 2"]}
      if {$v2 > $PI} {set v2 [expr "-$PI"]}
      #if {$u == 8.881784197001252e-16} {set u 0} ;#[expr "($v2 - $PI) / 2"]
      #if {$u2 == 8.881784197001252e-16} {set u2 0} ;#[expr "($v2 - $PI) / 2"]

      # draw color [expr $cnum + (int($cmax * $u / $maxu) + int($cmax * $v / $maxv)) % $cmax]
      
      draw triangle "$fdata_r($u,$v)  $gdata_r($u,$v)  $hdata_r($u,$v)" \
                    "$fdata_r($u2,$v)  $gdata_r($u2,$v)  $hdata_r($u2,$v)" \
                    "$fdata_r($u2,$v2) $gdata_r($u2,$v2) $hdata_r($u2,$v2)"
      draw triangle "$fdata_r($u2,$v2) $gdata_r($u2,$v2) $hdata_r($u2,$v2)" \
                    "$fdata_r($u,$v2) $gdata_r($u,$v2) $hdata_r($u,$v2)" \
                    "$fdata_r($u,$v)  $gdata_r($u,$v)  $hdata_r($u,$v)"
    }
  }
}
