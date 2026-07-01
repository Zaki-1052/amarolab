# By Lane Votapka
# Amarolab 2011
# UC Irvine

'''
This script prepares all necessary files for a gromacs cluster run

Takes two inputs:
Argument 1: Trajectory pdb file
Argument 2: PDB file with active site (site to be clustered by)
Argument 3: (Optional) CA or all, CA will cluster by alpha carbons, all by every atom (default: CA)

'''

import os, sys
import re
from pprint import pprint


def makendx(numbers):
    '''takes a list of numbers and returns a list in ndx format'''
    if (type(numbers[1]) != str):
        numbers = map(str,numbers) #convert all values to a string
    maxwidth = len(numbers[-1]) #find the maximum string length of each number
    spaced_residue_lines = [] # list for number strings with spaces added
    growing_line = [] # the list that will be joined and appended to spaced_residue_lines for file
    counter = 0
    for string in numbers:
        curwidth = len(string)
        numspaces = maxwidth - curwidth #number of spaces we need to add
        spaces = ' '*numspaces # the string with the spaces
        newstring = ''.join((spaces,string))
        growing_line.append(newstring) # 
        counter += 1
        if (counter % 15 == 0) and (counter != 0):
            growing_line = ' '.join(growing_line)
            growing_line = growing_line + '\n'
            spaced_residue_lines.append(growing_line) # this list is every complete line so far
            growing_line = []
    growing_line = ' '.join(growing_line)
    growing_line = growing_line + '\n'
    spaced_residue_lines.append(growing_line)
    return spaced_residue_lines[:]


modify_traj = False # do we want to remove CRYST and change END to ENDMDL

if len(sys.argv) <= 2 or len(sys.argv) > 4: #if we have one argument or less, or 3 or more
    print __doc__ # just print the docstring
    print "Debug mode"
    trajfilename = '/scratch/lvotapka/projects/cpaf/ark/third.pdb'
    activesitefilename = '/scratch/lvotapka/projects/cpaf/ark/cluster_loops/allloops.pdb'
    #sys.exit()
else:
    trajfilename = sys.argv[1]
    activesitefilename = sys.argv[2] # pull out the arguments
    
try:
    arg3 = sys.argv[3]
except IndexError:
    print "No argument for cluster by selection"
    arg3 = 'CA'
        

trajlist = []
framecounter = 0 # counts how many frames in this trajectory, if it exceeds maxframes, then exit
maxframes = 40000
residloc = 5

#first remove all cryst headers and change all END to ENDMDL
if modify_traj:
    trajfile = open(trajfilename, 'r')
    crystpattern = re.compile('CRYST')
    endpattern = re.compile('END')
    print "Checking trajectory and removing all CRYST and changing END to ENDMDL..."
    
    for line in trajfile.xreadlines(): # for each line in the trajectory
        if not re.search(crystpattern, line): #as long as the line doesn't say CRYST, continue
            line = re.sub(endpattern,'ENDMDL',line) #replace END with ENDMDL
            trajlist.append(line) # append each new line to a list

    trajfile.close() #close it for reading
    trajfile = open(trajfilename,'w') # open it for writing
    trajfile.writelines(trajlist) # write the lines
    trajfile.close() # finally close the file

# Get the first frame of the trajectory and save it
print "Getting first frame of the trajectory file to write to first_frame.pdb"
trajfile = open(trajfilename, 'r')
firstframefile = open('first_frame.pdb','w')
firstframelist = []
endpattern = re.compile('END(MDL)?') # we're looking for an END or ENDMDL pattern
for line in trajfile.xreadlines():
    firstframefile.write(line)
    firstframelist.append(line)
    if re.search(endpattern,line): # if we find the pattern
        break
#trajfile.close()
firstframefile.close()

# make a file containing all the active site residue numbers
print "Now writing all residue numbers to resid_activesite.dat & active_site_correct_residues.pdb"
active_site = open(activesitefilename,'r')
residlist = set()
for line in active_site.xreadlines():
    if line[0:4] != "ATOM": continue
    line = re.sub(' +',' ', line)
    line = line.strip().split()
    resid = line[residloc] # + '\n'
    residlist.add(resid)

active_site.close()
#print residlist
# find all lines of the pdb that have the right residue names
active_site_correct = []
active_site_atom_indeces = []
all_atom_indeces = []
for line in firstframelist:
    if line[0:4] != "ATOM": continue
    sline = re.sub(' +',' ', line) # change any number of spaces into a single space
    sline = sline.strip().split()
    curresid = sline[residloc]
    if curresid in residlist:
        active_site_correct.append(line)
        active_site_atom_indeces.append(sline[1]) # now have all relevant atom indeces
    all_atom_indeces.append(sline[1]) # this should contain all atom indeces
#print active_site_atom_indeces
# now convert into .ndx format
CApattern = re.compile(' CA ')
if arg3 == 'all': # if we are clustering by every atom
    selected_residues = active_site_atom_indeces
else:
    selected_residues = []
    # then find every line with an alpha carbon
    for line in active_site_correct:
        if re.search(CApattern, line):
            atomnum = line[5:11].strip()
            selected_residues.append(atomnum)

spaced_residue_lines = makendx(selected_residues)

# convert entire protein into ndx format
spaced_entire_lines = makendx(all_atom_indeces)

print 'Now writing selection.ndx file'
#write this all to a file
selection = open('selection.ndx','w')
selection.write('[ All_Atoms ]\n')
selection.writelines(spaced_entire_lines)
selection.write('\n[ active_site ]\n')
selection.writelines(spaced_residue_lines)
selection.close()

#pprint(spaced_residue_lines)
#pprint(spaced_entire_lines)
print "Cluster preparations complete!"
print "Type: \n g_cluster -n selection.ndx -cutoff #### -f trajectory.pdb -s first_frame.pdb -method gromos -o -g -dist -ev -sz -tr -ntr -clid -cl"
