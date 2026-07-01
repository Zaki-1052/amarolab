#moduseful.py
# by Lane Votapka

#this module contains useful code snippets for python scripts

import time
import math


class Logger:
    '''
    this class is for creating and writing to a logfile for debugging
    purposes. It opens and closes the file each time so that the file
    never gets stuck without having been closed
    '''
    def __init__(self, filename):
        self.filename = filename
    def __call__(self, string):
        ifile = open(self.filename, 'a')
        ifile.write(''.join(('[',time.asctime(),']\n',string,'\n')))
        ifile.close()

        
def uniq(series):
        '''
        similar to the UNIX command 'uniq', will return the list/tuple with only unique elements
        '''
        series = tuple(series)
        idict = {}
        for item in series:
            idict[item]=''
        return idict.keys()

def _getstartlines(ifile):
    """Return a list of offsets where newlines are located. Used in the tail function""" 
    offsets = [-1] 
    i = 0 
    while True: 
        byte = ifile.read(1) 
        if not byte: #if it hits the end of the file
            break 
        elif byte == '\n': 
            offsets.append(i) 
        i += 1 
    return offsets
def tail(filename,lines=10,backwards=False):
    '''
    returns the last lines of a file
    filename: the path to the file
    lines: how many lines to return
    backwards: inverts the order of lines returned

    NOTE: this function is a generator, but it could be modified to return a
    list if necessary
    '''

    ifile = open(filename,'r')
    startlines = _getstartlines(ifile)
    neededlines = startlines[-lines:]
    if backwards == True:
        neededlines.reverse()
    for i in neededlines:
        ifile.seek(i+1)
        curline = ifile.readline()
        yield curline


def better_tail(f, window=20):
    ''' a better function than the function 'tail' above because it uses less memory '''
    BUFSIZ = 1024
    f.seek(0, 2)
    bytes = f.tell()
    size = window
    block = -1
    data = []
    while size > 0 and bytes > 0:
        if (bytes - BUFSIZ > 0):
            # Seek back one whole BUFSIZ
            f.seek(block*BUFSIZ, 2)
            # read BUFFER
            data.append(f.read(BUFSIZ))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            data.append(f.read(bytes))
        linesFound = data[-1].count('\n')
        size -= linesFound
        bytes -= BUFSIZ
        block -= 1
    return '\n'.join(''.join(data).splitlines()[-window:])

def length(ituple):
    '''
    takes a tuple or list of numbers, and finds the pythagorean distance between them and the origin
'''
    summation = 0
    for variable in ituple:
        square = variable * variable
        summation += square
    return math.sqrt(summation)

def transpos(ilist):
    '''transposes (reflects) a 2D list, returns the resulting list'''
    if not ilist: return ilist
    newlist = []
    height = len(ilist)
    width = len(ilist[0])
    for x in xrange(width):
        newline = []
        for y in xrange(height):
            newline.append(ilist[y][x])
        newlist.append(newline)
    return newlist[:]
    
def list_map(function,list1,list2):
    from types import ListType, TupleType
    '''
    takes two lists, and maps a function, which takes two variables, to each element in them.
    the lists may be multidimensional, but the two MUST be exactly the same dimensions
    '''
    #error checking first
    assert len(list1) == len(list2), "Error in list_map function: argument lists must be of identical size and dimensionality."
    #first we need to check if individual elements of our list aren't lists themselves
    if (isinstance(list1[0], ListType)) or (isinstance(list1[0], TupleType)):
        bottomlevel = False
    else:
        bottomlevel = True #default that we are at the bottom level of our function

    
    if bottomlevel == True: #if indeed we are at the lowest dimension of our list
        newlist = []
        for i in range(0,len(list1)):
            #apply the function to each element of the lists, saving it to newlist
            result = apply(function,(list1[i],list2[i])) #apply the function to our two numbers
            newlist.append(result)
        return newlist[:]
    else: #then we need to go deeper with the next dimension
        newlist = []
        for i in range(0,len(list1)): #for each list in this dimension
            newlist.append(list_map(function,list1[i],list2[i])) #call this function recursively
        return newlist[:] #move up a level
    
if __name__ == "__main__": #testing area
    pass
