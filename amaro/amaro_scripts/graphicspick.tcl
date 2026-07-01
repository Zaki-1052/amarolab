##
## Example illustrating the use of user-defined graphics picking
##
## Requires VMD 1.8.5 or later
##




proc draw_spheres { } {
  global spheres 
  global grIDs

  draw color blue
  for { set i 0 } { $i < 10 } { incr i } {
    set spheres($i) [list [expr $i * 2.0] 0.0 0.0 2.0]
    set sid [draw sphere [lrange $spheres($i) 0 2] \
      radius [lindex $spheres($i) 3]]

    set pid [draw pickpoint [lrange $spheres($i) 0 2]]
    set grIDs($sid) $i
    set grIDs($pid) $i
  }
}

proc del_spheres { } {
  global spheres
  global grIDs

  array startsearch grIDs
  foreach gid [array names grIDs] {
    draw delete $gid
  }
}

proc draw_highlight { sphereid } {
  global spheres
  global grIDs
  global highlightID

  puts "drawing highlight for sphere $sphereid"

  draw color yellow 
  set highlightID [draw sphere [lrange $spheres($sphereid) 0 2] \
    radius [expr 1.1 * [lindex $spheres($sphereid) 3]] ]
}

proc del_highlight { } {
  global highlightID

  if { $highlightID > -1 } {
    draw delete $highlightID
    set highlightID -1
  }
}

proc do_graphics_pick_client { args } {
  global vmd_pick_graphics
  global grIDs

  puts "user-defined graphics pick: $vmd_pick_graphics"

  set mol [lindex $vmd_pick_graphics 0]
  set tag [lindex $vmd_pick_graphics 1]
  set btn [lindex $vmd_pick_graphics 2]
  set shf [lindex $vmd_pick_graphics 3]
  puts "molecule: $mol  tag: $tag  button: $btn  shift state: $shf"
  
  set sid $grIDs($tag)
  puts "Sphere ID picked: $sid"
  del_highlight
  draw_highlight $sid
}

trace add variable vmd_pick_graphics write do_graphics_pick_client

set highlightID -1
draw_spheres
scale by 0.1
