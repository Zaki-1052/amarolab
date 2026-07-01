# Checkbarriers.tcl

`
    
    
    
    #set numatoms 1231 	 
    
    set atoms {} 	 
    for { set i 1 } { $i <= $numatoms } { incr i } { 	 
    lappend atoms $i 	 
    } 	 
    
    foreach atom $atoms { 	 
    addatom $atom 	 
    }
    
    print "\nnumatoms: $numatoms\n\n"
    
    

`
