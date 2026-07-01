#!/usr/bin/python
'''
Name: dxfixer.py
Author: Lane Votapka
Usage:

python dxfixer.py filename.dx

This script takes unconventional formats of a .dx file and converts it to exactly the same format put out by APBS

For instance; OpenBabel puts out a form of .dx file that Browndye cannot read. The .dx is changed by dxfixer.py 
'''

import sys, re, os, fileinput

debug = False

if len(sys.argv) <= 1: 
  print __doc__
  exit()

#assert len(sys.argv) == 2, "This script takes exactly one argument"
#ourfile = open(sys.argv[1], 'r+')

changed_header = False
noncomment_line = 1
for line in fileinput.input(inplace = not debug): # if debug is set to false, then the file will overwrite itself, otherwise it will print to standard output
  if fileinput.isfirstline() == True: # then we are at a new file
    changed_header = False
    noncomment_line = 1
  line = line.rstrip() # strip whitespace
  if not line: # if the line is empty
    continue # skip the entire thing
  if line.lstrip()[0] == '#': # if the first character is a hash, then its a comment; print the line exactly the way it is
    if changed_header == False: # ...unless its the first hash, then we can add some 'recognition'...
      changed_header = True
      if not line.endswith('dxfixer.py'): # but only if the recognition hasn't been already given
        line = line + ' modified by dxfixer.py'
  else: # then its not a comment
    line = line.split()
    if noncomment_line == 1: # first noncomment line of the header
      newline = ['object', line[1], 'class', 'gridpositions', 'counts',] + line[5:8]
    elif noncomment_line == 2:
      newline = ['origin',] + line[1:4]
    elif noncomment_line in (3, 4, 5):
      newline = ['delta',] + line[1:4]
    elif noncomment_line == 6:
      newline = ['object', line[1], 'class', 'gridconnections', 'counts',] + line[5:8]
    elif noncomment_line == 7:
      newline = ['object', line[1], 'class', 'array', 'type', line[5], 'rank', line[7], 'items', line[9], 'data follows',]
     
    # NOTE: More terms may need to be added to the file's footer
    else:
      newline = line
      
    line = newline
    line = ' '.join(line) # separate everything only by a space
    
    noncomment_line += 1
    
  print line
