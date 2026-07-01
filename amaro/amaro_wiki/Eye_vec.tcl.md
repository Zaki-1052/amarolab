# Eye vec.tcl

proc eye_vec {coords {molid 0}} {
      # coordinates of the atom
      #set coords [lindex [$sel get {x y z}] 0]
      set ourmol $molid ;#[$sel molid]
      # position in world space
      set mat [lindex [molinfo $ourmol get view_matrix] 0]
      set world [vectrans $mat $coords]
    
      # since this is orthographic, I just get the projection
      lassign $world x y
      # get a coordinate behind the eye
      set world2 "$x $y 5"
    
      # convert back to molecule space
      # (need an inverse, which is only available with the measure command)
      set inv [measure inverse $mat]
      set coords2 [vectrans $inv $world2]
      draw cylinder $coords $coords2 radius 0.3
      return [vecsub $coords2 $coords]
    }
