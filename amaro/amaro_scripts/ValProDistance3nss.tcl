proc distance {} {
#this script takes a neuraminidase molecule and measures the distance 
# between every gamma carbon of VAL149 and the alpha carbon 
# of PRO431 over the course of a trajectory and outputs the distances
# to an output file whose title is determined by the name of the
# current molecule
#NOTE: this script is based on a earlier script that measured between ILE149 and PRO431
# thus it has those old variable names

#first choose the names of the outputs
set filename [molinfo top get name]
set namelen [string length $filename]
set nosuffixlen [expr $namelen - 8]
set newname [string range $filename 0 $nosuffixlen]
#set cdfilename "$newname.cd.txt"
set cg1filename "$newname.cc1.txt"
set cg2filename "$newname.cc2.txt"
set cbfilename "$newname.cb.txt"

#initialize the selections,etc.

set ILElocs {68 455 842 1229}
set PROlocs {350 737 1124 1511}



#do the measurement analysis
set nf [molinfo top get numframes]

#open all files
#set outfilecd [open $cdfilename w]
set outfilecg1 [open $cg1filename w]
set outfilecg2 [open $cg2filename w]
set outfilecb [open $cbfilename w]

#for each frame
for {set i 0} {$i < $nf} {incr i} {
  #set cddistdatatot ""
  set cg1distdatatot ""
  set cg2distdatatot ""
  set cbdistdatatot ""
  
  #loop through all four monomers
  for {set f 0} {$f < 4} {incr f} {
  
    set onILE [lindex $ILElocs $f]
    set onPRO [lindex $PROlocs $f] 
  
    #first select the proline alpha carbon
    set prosel [atomselect top "resid $onPRO and name CA"] 
    #Isoleucine delta carbon
    #set ileCDsel [atomselect top "resid $onILE and name CD1"]
    #ile gamma carbon 1
    set ileCG1sel [atomselect top "resid $onILE and name CG1"]
    #ile gamma carbon 2
    set ileCG2sel [atomselect top "resid $onILE and name CG2"]
    #ile beta carbon
    set ileCBsel [atomselect top "resid $onILE and name CB"]

  
    #update the selection location for each of the carbons
    $prosel frame $i
    #$ileCDsel frame $i
    $ileCG1sel frame $i
    $ileCG2sel frame $i  
    $ileCBsel frame $i
    #now obtain the center of mass for each atom
    set comPro [measure center $prosel weight mass]
    #set comileCD [measure center $ileCDsel weight mass]
    set comileCG1 [measure center $ileCG1sel weight mass]  
    set comileCG2 [measure center $ileCG2sel weight mass]
    set comileCB [measure center $ileCBsel weight mass]
    #now measure the distances
    #set cddistdata [veclength [vecsub $comPro $comileCD]]
    set cg1distdata [veclength [vecsub $comPro $comileCG1]]
    set cg2distdata [veclength [vecsub $comPro $comileCG2]]
    set cbdistdata [veclength [vecsub $comPro $comileCB]]
    #append the new data to the line, plus a tab
    set sepchar ""
    if {$f>0} {set sepchar "\t"}
    #set cddistdatatot "$cddistdatatot$sepchar$cddistdata"
    set cg1distdatatot "$cg1distdatatot$sepchar$cg1distdata"
    set cg2distdatatot "$cg2distdatatot$sepchar$cg2distdata"
    set cbdistdatatot "$cbdistdatatot$sepchar$cbdistdata"
    }
  #After the lines are finished, append them to respective files
  #puts $outfilecd "$cddistdatatot"
  puts $outfilecg1 "$cg1distdatatot"
  puts $outfilecg2 "$cg2distdatatot"
  puts $outfilecb "$cbdistdatatot"
}
#at the end of the loop, close the files
#close $outfilecd
close $outfilecg1
close $outfilecg2
close $outfilecb
}
