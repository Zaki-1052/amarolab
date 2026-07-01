'''
virus_rxn_find.py
By Lane Votapka
Amaro Lab 2014

This program takes reaction criteria for the viral particle, and returns a Browndye Reaction file



'''

import pdb2 as pdb
import sys, re
from cStringIO import StringIO # NOTE: may want to change this to cStringIO if more speed is needed in the future
import numpy as np
import argparse
import time
import xml.sax as sax

def fix_resname(atom_resname):
  if atom_resname in ['HSE','HSD','HSP']: # fix the histidines
    return "HIS"
  else:
    return atom_resname

starttime = time.time()
print "Parsing arguments"
# parse the arguments
parser = argparse.ArgumentParser(description="Takes reaction criteria: residue names, numbers and generates a Browndye reaction file")
parser.add_argument('-r', '-rec', dest="rec", type=str, help="name of pqr file containing receptor")
parser.add_argument('-l', '-lig', dest="lig", type=str, help="name of pqr file containing ligand")
parser.add_argument('-n', '-n_needed', dest="n_needed", type=str, default="1", help="number of contacts before reaction occurs")
parser.add_argument('-o', '-out', dest="out", type=str, help="name of the output rxn xml file")
parser.add_argument('-x', '-rxn', dest="rxn", type=str, help="string defining all reaction pairs. Format: 'REC_RESNAME1-REC_RESID1-REC_ATOM_NAME:LIG_RESNAME1-LIG_RESID1-LIG_ATOM_NAME,...'")
parser.add_argument('-d', '-dist', dest="dist", type=str,  help="reaction criteria distance")
parser.add_argument('-s', '-simple', dest="simple", default=False, help="whether to write nonspecific reaction file output", action="store_true")

args = parser.parse_args() # parse the args into a dictionary
args = vars(args)
rec_pqr_filename = args['rec']
lig_pqr_filename = args['lig']
out_filename = args['out']
distance = args['dist']
n_needed = args['n_needed']
simple_output = args['simple'] # then we are looking for simple reaction file output
rxn_string = args['rxn']

assert distance != None, "A nonzero distance must be set."
assert rxn_string != None, "A string of reaction pairs must be defined."

# parse the rxn string
rxn_pairs_tmp = rxn_string.split(',')
rxn_pairs = [] # a nested list of all reaction criteria
rec_strs = [] # a list of all the strings containing resname, resid, and atomname
lig_strs = []
num_pairs = len(rxn_pairs_tmp) # the number of pairs per molecule/peptide
atoms_found = {} # keep track of all pairs found or not
for pair_str in rxn_pairs_tmp:
  # first parse the receptor side
  rec_side = pair_str.split(':')[0]
  rec_strs.append(rec_side) # but save a copy of the string
  rec_name_id = rec_side.split('-') # [RESNAME, RESID, NAME]

  # then parse the ligand side
  lig_side = pair_str.split(':')[1]
  lig_strs.append(lig_side) # but save a copy of the string
  lig_name_id = lig_side.split('-') # [LIGNAME, LIGID, NAME]

  atoms_found[rec_side] = 0
  atoms_found[lig_side] = 0

  rxn_pairs.append([rec_name_id, lig_name_id]) # ([rec_name_id,lig_name_id]) # [[[RECNAME1, RECID1, ATOMNAME],[LIGNAME1, LIGID1, ATOMNAME]], [[RECNAME2, RECID2, ATOMNAME],[LIGNAME2, LIGID2, ATOMNAME]], ...]

#rec_indeces = [] # a list of all atom ids in the receptor that are part of a reaction
#lig_indeces = []

all_pairs = [] # a list of all atom pairs to be put into the rxn xml

# read the pqr files,
print "Opening ligand pqr file... time:", time.time() - starttime
parser=pdb.Big_PDBParser()
lig_pqr = parser.get_structure('lig pqr file',lig_pqr_filename, preserve_index = True, preserve_resid = True, pqr=True)
print "Opening receptor pqr file... time:", time.time() - starttime
#parser=pdb.Big_PDBParser()
rec_pqr = parser.get_structure('rec pqr file',rec_pqr_filename, preserve_index = True, preserve_resid = True, pqr=True)

print "Looping thru atoms to find those involved with reactions... time:", time.time()-starttime

ligdict = {} # a dictionary relating ligand resname and resid to the atom index
for ligstr in lig_strs: # keeping track of all ligand atoms of interest
  ligdict[ligstr] = [] # initialize with an empty list

recdict = {} # a dictionary relating receptor resname and resid to the atom index
for recstr in rec_strs: # keeping track of all ligand atoms of interest
  recdict[recstr] = [] # initialize with an empty list

# find all relevant ligand atom ids

for atom in lig_pqr.atoms:
  rxn_pair_index = 0
  for rxn_pair in rxn_pairs:
    [check_resname, check_resid, check_name] = rxn_pair[1] # decompose the ligand info into three variables
    if check_resname == atom.resname and check_resid == atom.resid and check_name == atom.name: # then we have a match!
      ligstr = '-'.join((check_resname, check_resid, check_name)) # recreate the string
      atoms_found[ligstr] = 1
      ligdict[ligstr].append(atom.index) # store this index for later
      
    rxn_pair_index += 1
# NOTE: need to check to make sure that none of the pairs are missing from this stucture

# find all relevant receptor atom ids
for atom in rec_pqr.atoms:
  for rxn_pair in rxn_pairs:
    [check_resname, check_resid, check_name] = rxn_pair[0] # decompose the receptor info into three variables
    #atom_resname = atom.resname[:3] # because we probably don't care about the 4 letter resnames (GLUP, ASPP, etc.)
    atom_resname = atom.resname
    atom_resname = fix_resname(atom_resname)
    
    #if atom.index > 13693753: # HACK!! delete later, applies to hemagg H5N1 sialic
    #  continue
    
    #if atom.index < 13600000: # HACK!! delete later, applies to 2ndary site H1N1 sialic
    #  continue
    
    #if atom.index < 13597806: # HACK!! delete later, applies to 2ndary site mix1 sialic
    #  continue
    
    if atom_resname.startswith(check_resname) and check_resid == atom.resid and check_name == atom.name: # then we have a match!
      recstr = '-'.join((check_resname, check_resid, check_name)) # recreate the string
      atoms_found[recstr] = 1
      recdict[recstr].append(atom.index) # store this index for later

# construct the sites
sites = [] # a list of all sites and their indeces
num_pairs = len(recdict.keys()) # the number of reaction pairs
first_pair = recdict.keys()[0] # get the first pair, whatever that would be
allsame = True
oldnum = None

for i in range(len(recdict.keys()) ):
  pair = recdict.keys()[i]
  num = len(recdict[pair])
  print "number of sites in", pair, ":", num, "first receptor index:", recdict[pair][0], "last receptor index:", recdict[pair][-1]
  if oldnum != None:
    if oldnum != num:
      allsame = False
  oldnum = num
  
  
assert allsame == True, "The number of pairs is different between the different sites. There may be more residues with this name or designation in this structure."
num_sites = len(recdict[first_pair]) # get the number of sites total
print "number of sites:", num_sites
print "recdict:", recdict
for i in range(num_sites): # for each site
  site_pairs = []
  for f in range(num_pairs): # for each pair in the site
    #lig_key = ligdict.keys()[f]
    #rec_key = recdict.keys()[f] # the pair that we need to retrieve. PROBLEM!!! DICTIONARY INDEXING OUT OF ORDER
    lig_key = lig_strs[f]
    rec_key = rec_strs[f]
    lig_id = ligdict[lig_key][0]
    rec_id = recdict[rec_key][i] # the indeces for this pair in this site
    site_pairs.append([rec_id,lig_id]) # append this pair
  sites.append(site_pairs) # append this particular site

# check to see which atoms were specified as reactive but not found in the pqrs

print "Processing results to generate rxn file", time.time()-starttime
print "ligdict values:", ligdict
print "recdict values:", recdict

#print "sites:", sites

# now iterate thru the possibilities to generate the reaction file
for atomkey in atoms_found.keys():
  if atoms_found[atomkey] == 0: # then this one was not actually found in the structure
    print "ALERT: the reaction string: %s was not found in any of the provided structures." % atomkey

# generate xml

outfile = open(out_filename, 'w')
outfile.write('''<roottag>
  <first-state>
    start
  </first-state>
  <reactions>\n''')
  
if simple_output:
  outfile.write('''    <reaction>
      <name>
        site_1
      </name>
      <state-before>
        start
      </state-before>
      <state-after>
        end
      </state-after>
      <criterion>
        <n-needed> %s </n-needed>\n''' % (n_needed,))
  
#pair_counter = 0
index_counter = 0
i = 0
for site in sites:
  
  if not simple_output:
    outfile.write('''    <reaction>
      <name>
        site_%d
      </name>
      <state-before>
        start
      </state-before>
      <state-after>
        end
      </state-after>
      <criterion>
        <n-needed>
          %s
        </n-needed>''' % (i, n_needed))
  f = 0
  for pair in site:
    
    #recstr = '-'.join(pair[0])
    #ligstr = '-'.join(pair[1])
  #for recatom in recdict[recstr]: # get the list of recatoms
    #f = 0
    #for ligatom in ligdict[ligstr]: # get the list of ligatoms
    #  all_pairs.append('%d %d '%(recatom,ligatom)) # a list of all atom pairs in string form for easy insertion into xml
    recatom = pair[0]
    ligatom = pair[1]
    recstr = rec_strs[f]
    ligstr = lig_strs[f]
    outfile.write('''
        <pair> <!-- %s to %s -->
          <atoms>
            %d %d
          </atoms>
          <distance>
            %s
          </distance>
        </pair>''' % (recstr, ligstr, recatom, ligatom, distance))
    f += 1
  
  if not simple_output:
    outfile.write('''
      </criterion>
    </reaction>\n''')
    index_counter += 1
    #f += 1
  i += 1
  #pair_counter += 1

if simple_output:
  outfile.write('''      </criterion>
    </reaction>\n''')
outfile.write('''  </reactions>
</roottag>\n''')
outfile.close()
print "Complete. time:", time.time()-starttime
