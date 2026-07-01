proc NeurSASA {} {

#This script takes a trajectory, goes frame by frame, and measures the solvent-accessible surface of
# a specified series of residues. It then parses these into a tabulated file

puts "Starting..."

#first choose the names of the output file
set filename [molinfo top get name]
set namelen [string length $filename]
set nosuffixlen [expr $namelen - 8]
set newname [string range $filename 0 $nosuffixlen]
set realfilename "$newname.sasa.txt"

#assign the residues around which to perform the SASA
set sresids1 "(resid 37 or resid 38 or resid 53 or resid 68 or resid 69 or resid 70 or resid 71 or resid 75 or resid 98 or resid 99 or resid 142 or resid 143 or resid 144 or resid 145 or resid 147 or resid 162 or resid 164 or resid 165 or resid 166 or resid 194 or resid 196 or resid 197 or resid 212 or resid 214 or resid 263 or resid 264 or resid 265 or resid 266 or resid 287 or resid 321 or resid 346)"
set sresids2 "(resid 424 or resid 425 or resid 440 or resid 442 or resid 455 or resid 456 or resid 457 or resid 458 or resid 462 or resid 485 or resid 486 or resid 529 or resid 530 or resid 531 or resid 532 or resid 534 or resid 549 or resid 551 or resid 552 or resid 553 or resid 581 or resid 583 or resid 584 or resid 599 or resid 601 or resid 650 or resid 651 or resid 652 or resid 653 or resid 674 or resid 708 or resid 733)"
set sresids3 "(resid 811 or resid 812 or resid 827 or resid 829 or resid 842 or resid 843 or resid 844 or resid 845 or resid 849 or resid 872 or resid 873 or resid 874 or resid 888 or resid 916 or resid 917 or resid 918 or resid 919 or resid 921 or resid 936 86 or resid 988 or resid 1037 or resid 1038 or resid 1039 or resid 1040 or resid 1061 or resid 1095 or resid 1120)"
set sresids4 "(resid 1198 or resid 1199 or resid 1214 or resid 1229 or resid 1230 or resid 1231 or resid 1232 or resid 1236 or resid 1259 or resid 1260 or resid 1303 or resid 1304 or resid 1305 or resid 1306 or resid 1308 or resid 1323 or resid 1325 or resid 1326 or resid 1327 or resid 1355 or resid 1357 or resid 1358 or resid 1373 or resid 1375 or resid 1424 or resid 1425 or resid 1426 or resid 1427 or resid 1448 or resid 1482 or resid 1507)"

set sresidlist { $sresids1 $sresids2 $sresids3 $sresids4 }

#get the number of total frames
set nf [molinfo top get numframes]

#open the write-to file
set outfile [open $realfilename w]

#now make the selections that will be needed later

#set resids1 [atomselect top [format "protein and %s" $sresids1]] 
#set resids2 [atomselect top [format "protein and %s" $sresids2]]
#set resids3 [atomselect top [format "protein and %s" $sresids3]]
#set resids4 [atomselect top [format "protein and %s" $sresids4]]

set residlist [list]

#puts "checkpoint 1"
set count 0
foreach i $sresidlist {
  set vali [expr $i]
  #puts [format "protein and %s" [expr $i]]
  set temp [atomselect top [format "protein and %s" [expr $i]]]
  
  #set residlist($count) $temp
  #lappend residlist $temp
  
  #set count [expr $count + 1]
#}

#puts $residlist


#set i 0
for {set i 0} {$i < $nf} {incr i} { 
#each frame
  #the beginning of the line in the output file
  set sasadatatot ""
  
  set count 0
  foreach f $sresidlist {
    #for each of the monomers
    #puts "checkpoint 2"
    #update the frame
    
    #reselect the atoms
    set protein [atomselect top "protein"]
    set temp [atomselect top [format "protein and %s" [expr $f]]]
    $temp frame $i
    $protein frame $i
    #puts "checkpoint 3"
    #calculate the surface area data
    set sasadata [measure sasa 1.4 $protein -restrict $temp]
    #puts $sasadata
    set sepchar ""
    if {$count>0} {set sepchar "\t"}
    #making the output line
    set sasadatatot "$sasadatatot$sepchar$sasadata"
    set count [expr $count + 1]
    #puts $f
    
  }
  if {[expr $i % 10]==0} {
    puts "now processing frame $i of $nf"
  }
  puts $outfile "$sasadatatot"
  #puts $sasadatatot
  
}
close $outfile
puts "Complete"
}
