#!/usr/bin/python

'''This script sorts and squashes a series of 3 or more numbers that are all within 
 1 of the number on either side, and represents this series with a "x to y" statement'''

import sys, os, re

def makeourstring (streak, firstx, oldx):
	if oldx - firstx < 1:
		ourstring = str(oldx)
	elif oldx - firstx == 1: # then don't put a 'to' in there
		ourstring = "%d %d" % (firstx, oldx)
	elif oldx - firstx >= 2: # then put a 'to' in there
		ourstring = "%d to %d" % (firstx, oldx)
	return ourstring

srcfile = sys.argv[1]
src = open(srcfile,'r')

linelist = []
for line in src:
	linelist.append(line) # get every line

bigstring = ''.join(linelist) # make one big string
bigstring = re.sub('\n', ' ', bigstring) # convert all newlines into spaces
bigstring = re.sub('\s+', ' ', bigstring)

# the string is now standardized
biglist = bigstring.strip().split()
try:
	biglist = map(int,biglist)
except ValueError:
	print "A value in the input file cannot be converted to an integer."
	sys.exit()

biglist.sort()
firstx = None
oldx = None
streak = 0

#biglist = "1 2 3 4 5 7 8 9 11 12 13 19 20 21 22 23 56 234".split() # just a test.


finallist = []
for number in biglist:
	ourstring = ''
	x = int(number)
	#print x
	if oldx == None: # then we are starting an entirely new list
		firstx = x
		oldx = x
		streak = 1
	else: # we are running through later members of a list
		if oldx + 1 >= x: # if the elements are equal or plus one, we're on a streak
			streak = streak + 1
		else: # we're ending this streak and starting a new one
			ourstring = makeourstring(streak, firstx, oldx)
			streak = 1
			firstx = x
			finallist.append(ourstring)
		oldx = x

finallist.append(makeourstring(streak, firstx, oldx))

for i in finallist:
	print i,
