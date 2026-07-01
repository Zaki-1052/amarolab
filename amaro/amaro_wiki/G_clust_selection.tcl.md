# G clust selection.tcl

`
    
    
    
    set OUT_CLUSTERING_SERIAL [open "Active_site_serial.dat" w]
    set OUT_NDX [open "selection.ndx" w]
    
    set clustering_resids [atomselect top "protein and resid 17 18 21 22 23 24 28 66 69 70 71 72 73 74 75 76 77 139 140 141 142 144 145 148 210 211 212 252 253 254 255 256 257 258 259 260 261 293 294 295 296 297 298 299 300 301 302 303 304 305 307 308 319 321 323 324 329 358 394 395 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 442 443 444 445 446 447 448 449 450 451 452 453 454 455 464 465 466 467 468 469 470 471 472 474 480 481 482 483 484 485"]
    
    set clustering_serial_list [ $clustering_resids get serial]
    
    #output active site atom serials in gromos ndx format
    puts $OUT_NDX "\n"
    puts $OUT_NDX {[ active_site ]}
    set i 1
    foreach asite $clustering_serial_list {
      set parsed [split $asite " "]
      foreach index $parsed {
        if {[expr $i%15] == 0} {
          puts $OUT_NDX [format "%+4s " "$index"]
        } else {
          puts -nonewline $OUT_NDX [format "%+4s " "$index"]
        }
        set i [expr $i + 1]
      }
    }
    
    #output active site serials for comparison   
    foreach asite $clustering_serial_list {
      puts $OUT_CLUSTERING_SERIAL $asite
    }
    
    close $OUT_CLUSTERING_SERIAL
    close $OUT_NDX
    
    

`
