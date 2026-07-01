# Virus async.bash

#!/bin/bash
    
    # This script creates and runs all the virus apbs files to generate the electrostatics volmaps
    
    NUMPROCS=6 # specify how many jobs to run at one time
    APBSDIR=apbs
    TOTALJOBS=$1 # user input
    
    
    APBS_TEMPLATE=$(echo "read
        mol pqr ../output.radii_fixed.pqr
    end
    elec
        mg-para
        dime 321 321 353
        pdime 9 9 9
        async ASYNCNUM
        ofrac 0.1
        cglen 1979.7486 1966.0483 2088.6064
        fglen 1184.5580 1176.4990 1248.5920
        cgcent mol 1
        fgcent mol 1
        mol 1
        lpbe
        bcfl sdh
        pdie 2.0000
        sdie 78.5400
        ion charge -1.00 conc 0.15 radius 1.8150
        ion charge 1.00 conc 0.15 radius 1.8750
        srfm spl2
        chgm spl2
        sdens 10.00
        srad 1.40
        swin 0.30
        temp 298.15
        calcenergy total
        calcforce no
        write pot dx potASYNCNUM_
    end
    quit")
    
    #mkdir infiles
    #cd infiles
    #for ((i=0; i<$TOTALJOBS; i++)); do
    #for i in {0..7}; do
      #mkdir apbs_async_all # create directory
      cd apbs_async_all
      echo 'echo "running all"'> run_all.bash
      #for f in {0..7}; do
        #echo 'echo "starting proc $i"'> proc${f}_script.bash
        for ((g=0; g<$TOTALJOBS ; g++)); do
          ASYNCNUM=$g #`echo "$g + ($f*8) + ($i*64)"|bc`
          #echo $g
          echo "$APBS_TEMPLATE" | sed "s/ASYNCNUM/$ASYNCNUM/" > apbs${ASYNCNUM}.in
          echo "echo 'now running apbs job $g'" >> run_all.bash
          echo "$APBSDIR apbs${ASYNCNUM}.in > apbs${ASYNCNUM}.out" >> run_all.bash # apbs command for this processor
          #echo $APBS_TEMPLATE > apbs${ASYNCNUM}.in
        done
         echo "exit" >> run_all.bash
        #echo "bash proc${f}_script.bash &" >> run_all.bash
      #done
      #cd .. # back out of that one
    #done
    cd ..
