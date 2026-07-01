proc distance {} {
#this script takes a hemagglutinin molecule and measures the distance 
# between the alpha carbons of Gly134 and Gln226 over the course 
# of a trajectory and outputs the distances
# to an output file whose title is determined by the name of the
# current molecule

#first choose the names of the outputs
set filename [molinfo top get name]
set namelen [string length $filename]
set nosuffixlen [expr $namelen - 8]
set newname [string range $filename 0 $nosuffixlen]
set cafilename "dist$newname.txt"

#initialize the selections,etc.

set GLYlocs {134 637 1140} 
set GLNlocs {226 729 1232}

#do the measurement analysis
set nf [molinfo top get numframes]

#open all files
set outfileca [open $cafilename w]
puts "Initializations complete"
#for each frame
for {set i 0} {$i < $nf} {incr i} {
  set cadistdatatot "" 
  #set the beginning of the line equal to empty string
  #puts "marker 2"
  for {set f 0} {$f < 3} {incr f} {
    set onGLY [lindex $GLYlocs $f]
    set onGLN [lindex $GLNlocs $f] 
    #first select the glycine alpha carbon
    set glysel [atomselect top "resid $onGLY and name CA"] 
    #glutamine alpha carbon
    set glnsel [atomselect top "resid $onGLN and name CA"]
    #puts "marker 3"
    #update the selection location for each of the carbons
    $glysel frame $i
    $glnsel frame $i
    #now obtain the center of mass for each atom
    set comGly [measure center $glysel weight mass]
    set comGln [measure center $glnsel weight mass]
    #now measure the distance
    set cadistdata [veclength [vecsub $comGly $comGln]]
    #puts $cadistdata
    #After the lines are finished, append them to respective files
    #append the new data to the line, plus a tab
    set sepchar ""
    if {$f>0} {set sepchar "\t"}
    set cadistdatatot "$cadistdatatot$sepchar$cadistdata"
  }
  
  puts $outfileca "$cadistdatatot"

}
#at the end of the loop, close the files
close $outfileca
puts "Complete"
}



#########################################################################################################################



proc pdbdistance {} {
  #initialize the selections,etc.

set ILElocs {68 455 842 1229}
set PROlocs {350 737 1124 1511}

set cddistdatatot ""
set cg1distdatatot ""
set cg2distdatatot ""
set cbdistdatatot ""

for {set f 0} {$f < 4} {incr f} {
  
  set onILE [lindex $ILElocs $f]
  set onPRO [lindex $PROlocs $f] 
  
  #first select the proline alpha carbon
  set prosel [atomselect top "resid $onPRO and name CA"] 
  #Isoleucine delta carbon
  set ileCDsel [atomselect top "resid $onILE and name CD1"]
  #ile gamma carbon 1
  set ileCG1sel [atomselect top "resid $onILE and name CG1"]
  #ile gamma carbon 2
  set ileCG2sel [atomselect top "resid $onILE and name CG2"]
  #ile beta carbon
  set ileCBsel [atomselect top "resid $onILE and name CB"]

  #now obtain the center of mass for each atom
  set comPro [measure center $prosel weight mass]
  set comileCD [measure center $ileCDsel weight mass]
  set comileCG1 [measure center $ileCG1sel weight mass]  
  set comileCG2 [measure center $ileCG2sel weight mass]
  set comileCB [measure center $ileCBsel weight mass]
  #now measure the distances
  set cddistdata [veclength [vecsub $comPro $comileCD]]
  set cg1distdata [veclength [vecsub $comPro $comileCG1]]
  set cg2distdata [veclength [vecsub $comPro $comileCG2]]
  set cbdistdata [veclength [vecsub $comPro $comileCB]]
  #append the new data to the line, plus a tab
  set sepchar ""
  if {$f>0} {set sepchar "\t"}
  set cddistdatatot "$cddistdatatot$sepchar$cddistdata"
  set cg1distdatatot "$cg1distdatatot$sepchar$cg1distdata"
  set cg2distdatatot "$cg2distdatatot$sepchar$cg2distdata"
  set cbdistdatatot "$cbdistdatatot$sepchar$cbdistdata"
  }
  #After the lines are finished, append them to the screen
puts "$cddistdatatot"
puts "$cg1distdatatot"
puts "$cg2distdatatot"
puts "$cbdistdatatot"
}
