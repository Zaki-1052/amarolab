proc mat_trace {mat} {
  set tr 0
  set len [llength $mat]
  for {set i 0} {$i < $len} {incr i} {
    set value [lindex [lindex $mat $i] $i]
    set tr [expr "$tr + $value"]
  }
  return $tr
}

proc mat_to_quat {mat} {
  # Given a 4x4 matrix, will convert to a quaternion and return
  set q {0 0 0 0} ;# initiate quaternion
  set tr [mat_trace $mat]  ;# sum the diagonal of the matrix
  if { $tr > [lindex [lindex $mat 3] 3] } {
    lset q 0 $tr
    lset q 3 [expr "[lindex [lindex $mat 1] 0] - [lindex [lindex $mat 0] 1]"]
    lset q 2 [expr "[lindex [lindex $mat 0] 2] - [lindex [lindex $mat 2] 0]"]
    lset q 1 [expr "[lindex [lindex $mat 2] 1] - [lindex [lindex $mat 1] 2]"]
  } else {
    set i 1; set j 2; set k 3
    if {[lindex [lindex $mat 1] 1] > [lindex [lindex $mat 0] 0]} {set i 2; set j 3; set k 1}
    if {[lindex [lindex $mat 2] 2] > [lindex [lindex $mat $i] $i]} {set i 3; set j 1; set k 2}
    set var1 [lindex [lindex $mat $i] $i]; set var2 [lindex [lindex $mat $j] $j];
    set var3 [lindex [lindex $mat $k] $k]; set var4 [lindex [lindex $mat 3] 3]; 
    set tr [expr "$var1 - ($var2 + $var3) + $var4"]
    lset q $i $tr
    lset q $j [expr "[lindex [lindex $mat $i] $j] + [lindex [lindex $mat $j] $i]"]
    lset q $k [expr "[lindex [lindex $mat $k] $i] + [lindex [lindex $mat $i] $k]"]
    lset q 3 [expr "[lindex [lindex $mat $k] $j] - [lindex [lindex $mat $j] $k]"]
    for {set f 0} {$f < 4} {incr f} {
      set qval [lindex $q $f]
      lset q $f[expr "$q_val * 0.5 / sqrt($tr * [lindex [lindex $mat 3] 3])"]
    }
  }
  return [vecnorm $q]
}
