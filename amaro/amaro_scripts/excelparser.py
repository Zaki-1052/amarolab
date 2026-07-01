#by Lane Votapka
#Amarolab at University of California, Irvine

#this script takes an input file, which contains references to
# comma separated values(.csv) files, and places them into
# an excel spreadsheet (or series of sheets) in a way specified
# by the input file. If necessary, it also can load zinc 
# pictures from the cactus server if zinc numbers and smile
# strings are provided

#input consists of paths to the source .csv's, which columns
# of those .csv's to include, picture information such as smile
# strings, zincs, and specified column, and lastly the column
# that specifies multiple sheets to be created

#===================================================================
#__doc__ string
#===================================================================
"""
by Lane Votapka
Amarolab at University of California, Irvine

This script takes one or more simple text files (.csv,.txt,etc...) and parses
them into an excel workbook according to instructions on an input file (.in)

the script should be executed directly from the shell according to this
format:

python excelfileparser.py <path to input file> <path to output .xls>

Input file format:
 Pathblock commands(can set one or more of these, each block must contain its
 own set of commands, separated by the 'path' command:
  - path <path to .csv files>
  - columns (optional) :<destination of specified column(optional)>
  - ids (optional) <column containing identification (ZINC) for pulling picture from online database
  - smiles (optional) <column containing smile strings for pulling picture from online database>
  - decomp (optional) <column containing which column will be sorted and the rest of the information placed into separate spreadsheets>
  - separator (optional; default-',') <a single separator character>
 Global commands should be placed at the end of the input file:
  - picture (optional) <dest column for picture>
  - picturewidth (optional: default=200) <desired width of pictures>
  - pictureheight (optional: default= 200) <desired height of pictures>
  - picturepath (optional) <path specifying location to upload pictures>
  - savepictures (optional) <no arguments, toggles whether to retain pictures in the picturepath once they have been uploaded. If this command is left out, they will be deleted from the file system>

 all input files must end with the character '/' on its own line
 any line that begins with the character '#' is considered a comment within the input file

NOTE: currently all columns must be specified by letter index (A,B,F,AD) as
found in an excel file. Number indeces are not currently supported

Please see Amarolab wiki for more information and sample input files

Warning: if multiple instances of this script is run, where pictures are
saved initially, but the script is run again with the same ID names
and pictures are not specified to be saved, then this script will delete
the older set of pictures as well

"""

#===================================================================
#imports
#===================================================================

import time
import sys
import os
import pprint
#import Image #this library is imported later, only if the user needs a picture
import xlwt
from xlwt import Workbook, easyxf, Bitmap
#import xlrd
#from xlrd import open_workbook,cellname
import StringIO
#import moduseful
from tempfile import TemporaryFile
import subprocess
import shlex
import urllib
#===================================================================
#the pathblock class
#===================================================================
class Pathblock(object):
  #init
  def __init__(self):
    self.path = ''
    self.srccolumns = ['all']
    self.destcolumns = ['all']
    self.picture = ''
    self.ids = ''
    self.smiles = ''
    self.decomp = ''
    self.separator = defaultseparator
  #sets
  def setpath(self,pathname):
    self.path = pathname
  def setsrccolumns(self,srccolumnslist):
    self.srccolumns = srccolumnslist[:]
  def setdestcolumns(self,destcolumnslist):
    self.destcolumns = destcolumnslist[:]
  def setpicture(self,picturecol):
    self.picture = picturecol
  def setids(self,idscol):
    self.ids = idscol
  def setsmiles(self,smilescol):
    self.smiles = smilescol
  def setdecomp(self,decompcol):
    self.decomp = decompcol
  def setseparator(self,separator):
    self.separator = separator
  def seteverything(self,params):
    self.path,self.srccolumns,self.destcolumns,self.picture,self.ids,self.smiles,self.decomp,self.separator = params
  #gets
  def getpath(self):
    return self.path
  def getsrccolumns(self):
    return self.srccolumns
  def getdestcolumns(self):
    return self.destcolumns
  def getpicture(self):
    return self.picture
  def getids(self):
    return self.ids
  def getsmiles(self):
    return self.smiles
  def getdecomp(self):
    return self.decomp
  def getseparator(self):
    return self.separator
  def geteverything(self):
    return self.path,self.srccolumns,self.destcolumns,self.picture,self.ids,self.smiles,self.decomp,self.separator
  
  block = property(geteverything,seteverything)
  
#===================================================================
# subroutines
#===================================================================
def exceltoindexconvert(column):
  """this function takes a string value from an excel spreadsheet
  and returns an index value. if given an integer, it returns it
  
  example:
  A returns 0
  B returns 1
  ...
  Z returns 25
  AA returns 26
  """
  alphabetnum = 26
  firsta = 97
  if column == '': return column
  if isinstance(column,int):
    return column
  
  assert isinstance(column,str), "The input file's column specifier must have an integer or string index"
  
  value = 0
  for i in range(len(column)):
    letter = column[-i -1].lower()
    ascii = ord(letter) - 97
    value += ((ascii+1) * (alphabetnum ** i))
  return value-1

def img2bmp(path):
  import Image
  """
  This function takes a non-bitmap image file, opens it,
  and feeds an output string as a bitmap file-like-object

  """
  try:
  	img = Image.open(path)
  	f = StringIO.StringIO()
  	img.save(f, "bmp")
  except IOError:
  	print "unable to open picture: " + path
  	f=''
  return f

#===================================================================
#Phase 1: Initializations
#===================================================================


#NOTE: need to allow input for picture file width and height
global picturewidth
picturewidth = 200
global pictureheight
pictureheight = 200
requiredos = ('posix',)
#global defaultseparator
defaultseparator = ',' #the character that represents a separation in columns

#official stuff
__all__ = ["Main", "exceltoindexconvert","createcsvtable", "img2bmp","Pathblock"]

#mastercoldict = {} #contains the items(destination columns) and a tuple containing: (the source file, the source column)


def _init(inputpath):
  global picturepath
  picturepath = sys.path[0]
  global deletepicturewhenfinished
  deletepicturewhenfinished = True
  
#===================================================================
#Phase 2: Input file
#===================================================================
#srcpath = []
pathblocklist = [] #list that contains every Pathblock class member
#firstpathblock = True
global defaultcommandlist
defaultcommandlist = ['','all','all','','','','',defaultseparator] #default command list
#commandlist = defaultcommandlist #the command list that will be fed into the Pathblock class
#command list indeces
pathcmd = 0
srccolumnscmd = 1
destcolumnscmd = 2
picturecmd = 3
idscmd = 4
smilescmd = 5
decompcmd = 6
separatorcmd = 7

def _newpathblock(cmdlist):
  #this code is called when a new path block is found
  curpathblock = Pathblock() #new Pathblock class instance
  curpathblock.block = tuple(cmdlist) #assign all values to the Pathblock class member
  pathblocklist.append(curpathblock) #add it to the main pathblock list


def _infilecode(line,firstpathblock,commandlist):
  global deletepicturewhenfinished
  global picturepath
  curpath = '' #the path for which the sublines will concern
  subline = False #determines whether this is a command concerning a given path
  #print line
  if line[0] == " ": subline = True #we are manipulating the aspects of a given path
  line = line.strip()
  if (not line) or (line[0] == "#") or (line[0] == '\n'):
    #its just a comment or empty line, skip this one
    return firstpathblock, commandlist
  if line[0] == '/':
    #last line of file, end the path block
    _newpathblock(commandlist)
    return firstpathblock, commandlist
  #now split each line by spaces
  cmdline = line.split()
  #command represents the first word of the line
  print cmdline
  command = cmdline[0].lower()
  
  #pathblock commands
  
  if command == 'path':
    #specifying a path now
    #if this isn't the first path block, call newpathblock() to save the previous path block
    if not firstpathblock:
      _newpathblock(commandlist)
      commandlist = defaultcommandlist[:]
    else:
      #don't call newpathblock, but set variable so it will go from now on
      firstpathblock = False
    #save the path portion of the pathblock
    curpath = cmdline[1]
    commandlist[pathcmd] = curpath #assign field 0 to be the path value
    
  elif command == 'columns': #specifies which columns to include in the final excel file, and where to put them
    rawcollist = cmdline[1].strip().split(',') #first we get a list containing the individual column lettering
    srclist = []
    destlist = []
    #rawcollist = map(exceltoindexconvert,rawcollist)
    for i in rawcollist:
      #this could be only the source, or source and destination together, only colons will tell
      i=i.split(':')
      if i[0].lower <> 'none': srclist.append(exceltoindexconvert(i[0])) #make sure the user wants to include some of the columns
      if len(i) == 1:
        #then there is only a source specified
        destlist.append('')
      elif len(i) == 2:
        #then a source and a dest are specified
        destlist.append(exceltoindexconvert(i[1]))
    commandlist[srccolumnscmd] = srclist
    commandlist[destcolumnscmd] = destlist
    
  elif command == 'picture': #specifying where to place the picture
    picloc = exceltoindexconvert(cmdline[1]) #convert the excel column identifier to a number index
    commandlist[picturecmd] = picloc
    #print "picloc: ", picloc
    
  elif command == 'ids': #specifying the column where the ID information is located
    idsloc = exceltoindexconvert(cmdline[1]) #convert the excel column identifier to a number index
    commandlist[idscmd] = idsloc
    
  elif command == 'smiles': #specifying the column where the Smile strings are located
    smilesloc = exceltoindexconvert(cmdline[1]) #convert the excel column identifier to a number index
    commandlist[smilescmd] = smilesloc
    
  elif command == 'decomp': #specifying which column determines how multiple spreadsheets are created
    decomploc = exceltoindexconvert(cmdline[1]) #convert the excel column identifier to a number index
    commandlist[decompcmd] = decomploc
    
  elif command == 'separator': #setting the new separator value for the pathblock
    sepval = cmdline[1]
    if sepval == '\\t': sepval = '\t' #reset the escape for tab
    if sepval == '\\s': sepval = ' '
    commandlist[separatorcmd] = sepval
    
  #global commands
  elif command == 'picturewidth': #specifies the desired width of the picture file to be obtained
    try:
      global picturewidth
      picturewidth = int(cmdline[1])
    except TypeError: #if the user didn't enter a number after the command
      'Warning: error in input file specifying picture width, resorting to default picture width...'
      
  elif command == 'pictureheight':
    try:
      global pictureheight
      pictureheight = int(cmdline[1])
    except TypeError: #if the user didn't enter a number after the command
      'Warning: error in input file specifying picture height, resorting to default picture height...'
      
  elif command == 'picturepath': #setting the path for the pictures to be uploaded into
    picturepath = cmdline[1]

  elif command == 'savepictures': #setting not to delete pictures after uploading them
    deletepicturewhenfinished = False
    
  else:
    print 'unknown command: ', command
  
  return firstpathblock, commandlist
  
  
  
def createcsvtable(csvpath,sepchar):
  #first open the file
  coltable = [] #this is what we want to return
  rowtable = [] #a temporary table that will be converted to a column-based table
  maxcols = 0 #this keeps track of the amount of columns so that we can have a rectangular table
  #now open the file etc
  #print 'csvpath: ', csvpath
  csvfile = open(csvpath)
  for line in csvfile:
    linelist = line.strip().split(sepchar) #split the row by commas
    if len(linelist) > maxcols: maxcols = len(linelist) #if we reach a longer line, then count the columns
    rowtable.append(linelist[:]) #copy the contents of linelist into the rowtable
  csvfile.close()
  #now we have a list by rows, as well as its maximum width, we need to convert it to a column-table
  for i in range(maxcols): #make sure that we add something up to the width of the widest row
    #rowf = 0
    newcol = []
    for row in rowtable:
      try:
        newcol.append(row[i])
      except IndexError:
        newcol.append('')
    coltable.append(newcol[:])
  return coltable
      
  
  
def _newinput(infilepath):
  firstpathblock = True
  coltablelist = []
  commandlist = defaultcommandlist[:] #the command list that will be fed into the Pathblock class
  #first load the specified input file
  try:
    infile = open(infilepath, 'r')
  except IOError:
    #if the file doesn't exist or they entered something wrong for the first field of argv
    raise Exception, "nonexistant or incorrect input file path specified."
  #now walk through the infile, line by line and decipher the code
  for line in infile:
    firstpathblock, commandlist = _infilecode(line,firstpathblock,commandlist)
  for i in pathblocklist:
    #print i.block
    #now we need to open each of the files and sort them by columns
    coltable = createcsvtable(i.getpath(),i.getseparator())
    coltablelist.append(coltable[:])
    #print coltable
  #pprint.pprint(coltablelist)
  print 'input file successfully processed'
  return coltablelist
    
  #if firstpathblock == False: #this is only needed if there isnt a '/' at the last line of the input file

#===================================================================
#Phase 3: obtaining pictures
#===================================================================

def _handlepictures(coltablelist):
  #babel="/scratch/bin/Babel/bin/babel" #NOTE: assign this to input file later
  nopic = False
  i=0
  for pathblock in pathblocklist:
    picloc = pathblock.getpicture() #this variable will hold the column where the picture should go
    print "picloc: ", picloc
    if pathblock.getsmiles() <> '': 
      smiloc = pathblock.getsmiles() #holds where the smile string is located
      smitable = i #the table where smiles are located
    if pathblock.getids() <> '': 
      idsloc = pathblock.getids() #holds the identification of the picture
      idstable = i #the table where ids are located
    i+=1
  if picloc == '': 
    print "Warning: Picture will not be included: No picture destination column specified"
    nopic = True
  if smiloc == '':
    print "Warning: Picture will not be included: No smile string column identified"
    nopic = True
  if idsloc == '':
    print "Warning: Picture will not be included: No ID column identified"
    nopic = True
  if os.name not in requiredos:
    print "Warning: Picture will not be included: Unable to run necessary system command with current OS."
    nopic = True
  if nopic:
    return picloc,[]

  import Image
  #now we have to locate the needed columns
  print coltablelist
  smilist = coltablelist[smitable][smiloc]
  idslist = coltablelist[idstable][idsloc]
  #and write the .os commands to find the pictures
  i = 0
  ifinal = len(idslist)
  for eachid in idslist:
    smi = smilist[i] #using the index to obtain the proper smile
    #now creating a list of commands to feed the os
    #command1 = 'echo "%s" > ghost%s.smi' % (smi,eachid) #create a smile file to feed to babel
    
    #command2 = "echo \"%s\" | babel -ismi -oinchi 2>/dev/null | awk '{print $1;}'" % smi
    #p = subprocess.Popen(command2,stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True,shell=True) #feed the smile file to babel, output to a variable
    #inchi=p.stdout.read()
    #command3 = 'echo "$inchi" > ghost%s.inchi' % eachid #place the value of inchi into another file
    #URLinchi=urllib.quote(inchi,'()/') #create the URLinchi variable which will be fed to the url
    #command4 = "URLinchi=`echo \"$inchi\" |  perl -MURI::Escape -lne 'print uri_escape($_)' | sed -e's/%2F/\//g'`" 
    #URLinchi=URLinchi.replace('%0A','')
    #oldurl = "http://cactus.nci.nih.gov/chemical/structure/%s/image?format=png&height=%i&width=%i&showstereo=0" % (URLinchi,picturewidth,pictureheight) #now access the online database for a picture according to these specifications
    url = "http://cactus.nci.nih.gov/chemical/structure/%s/image?format=png&height=%i&width=%i&showstereo=0" % (smi,picturewidth,pictureheight) #now access the online database for a picture according to these specifications
    #print 'command5:', command5
    #command6 = 'rm ghost%s.smi ; rm ghost%s.inchi' % (eachid,eachid) #delete the .inchi and .smi files, now unnecessary
    #allcommand = '\n'.join((command5,)) #splice the commands together
    #print allcommand
    if i%100 == 0: print 'obtaining picture %i out of %i' % (i,ifinal) #keep the user updated every 100 pictures
    try:  #all this is creating the temporary picture files
      picurl=urllib.urlopen(url)  #first stream the picture information from offline
      pngfileobjecttuple=picurl.readlines() #now read the information into a tuple
      pngfileobject=''.join(pngfileobjecttuple) #join the tuple into a string
      pngfileout=open('%s/%s.png' % (picturepath,eachid),'wb')
      pngfileout.write(pngfileobject)
      pngfileout.close()
    except:
      print "Warning: unable to download picture: %s" % eachid
    #os.system(command5) #feed the spliced commands into the os
    
    i += 1
  print 'picture uploads successful'
  #now all the pictures are available
  return picloc,idslist

#===================================================================
#Phase 4: creating the excel spreadsheet
#===================================================================
def _checkifcolistakenfromsource(oncoltable,onsrccolumn):
  includedcols = pathblocklist[oncoltable].getsrccolumns()
  #print pathblocklist[oncoltable].getdestcolumns()
  #print includedcols
  if includedcols == 'all': #then automatically this source column is included
    return True
  else: #otherwise this column must be in the specified list to be included
    if onsrccolumn not in includedcols:
      return None
    else:
      return includedcols.index(onsrccolumn)
    
def _checkifcolhasdest(oncoltable,includesrccol):
  destcollist = pathblocklist[oncoltable].getdestcolumns()
  #print 'destcollist: ', destcollist
  if destcollist == 'all': return None #otherwise this function will return a boolean
  destcol = destcollist[includesrccol]
  #print 'destcol: ', destcol
  if destcol == '':
    return None
  else:
    return destcol
  
def _createmasterdestlist(coltablelist):
  #this creates a list of every destination column, so that we can look at this list and be sure that we don't write anything to a reserved column
  masterdestlist = []
  for pathblock in pathblocklist:
    newdestlist = pathblock.getdestcolumns()
    #print 'newdestlist: ', newdestlist
    if (newdestlist) and (newdestlist <> 'all'):
      masterdestlist.extend(newdestlist)
      #print 'masterdestlist: ',masterdestlist
  return masterdestlist
    

def _createspreadsheet(coltablelist,picloc,idslist,destpath):
  #destpath = '/home/lvotapka/Desktop/xltest.xls'
  destbook = Workbook() #now we need to open a new excel workbook
  sheet = destbook.add_sheet('Sheet 1',cell_overwrite_ok=False) #select a sheet in the new workbook
  masterdestlist = _createmasterdestlist(coltablelist)
  #print 'masterdestlist: ', masterdestlist
  oncoltable = 0
  ondestcolumn=0
  if masterdestlist:
    while (ondestcolumn in masterdestlist) or (ondestcolumn == picloc): ondestcolumn += 1
  for coltable in coltablelist:
    onsrccolumn=0
    #first handle adding the verbal information
    for column in coltable:
      oncell=0
      #first see if this on dest column is the same location as the picture
      while ondestcolumn == picloc:
        #then skip this column
        ondestcolumn += 1
      #check if this column needs to be taken from the source
      includesrccol = _checkifcolistakenfromsource(oncoltable,onsrccolumn)
      #print 'includesrccol: ', includesrccol
      if includesrccol <> None:
        #check if this source column needs to be placed anywhere or skipped:
        specifieddest = _checkifcolhasdest(oncoltable,includesrccol)
        #print 'specifieddest: ', specifieddest
        if specifieddest == None:
          #then we are not going to have to add this source to the proper column
          propercolumn = ondestcolumn
        else:
          propercolumn = specifieddest
        #print 'propercolumn: ', propercolumn
        for cell in column:
          #print 'adding to sheet: ', onsrccolumn,oncell,ondestcolumn,propercolumn,cell
          sheet.write(oncell,propercolumn,cell)
          oncell+=1
        #onsrccolumn+=1
        if specifieddest == None: ondestcolumn+=1
        if masterdestlist:
          while (ondestcolumn in masterdestlist) or (ondestcolumn == picloc): ondestcolumn += 1 #we will skip this column because it is reserved for later
      onsrccolumn +=1
    oncoltable+=1
  #now handle adding the pictures
  i=0
  print 'directory: ', sys.path[0]
  if picloc <> '':
    print 'now adding pictures...'
    sheet.col(picloc).width = (picturewidth*50)
    #print 'picturepath: ', picturepath
    #print 'deletepictures: ', deletepicturewhenfinished
    for eachid in idslist: #for each id
      indpngpath = ''.join((picturepath,'/',eachid,'.png')) #create the path
      #print 'indpngpath: ', indpngpath
      #print 'picturepath: ', picturepath
      bmpIOstream = img2bmp(indpngpath)
      if bmpIOstream <> '': #if there is a picture to get
      	sheet.insert_bitmap(bmpIOstream,i,picloc) #insert the picture into the spreadsheet
      if deletepicturewhenfinished: os.system('rm %s' % (indpngpath)) #delete pictures from the directory if indicated
      i += 1
      
  
  tmp_file = StringIO.StringIO()
  destbook.save(tmp_file)
  destbook.save(destpath)
  destbook.save(TemporaryFile())
  return
  

#===================================================================
#Phase 5: module or script
#===================================================================

def main(infilepath,destpath):
  """
  This function is the main subroutine that executes the program


  """
  
  print "Running..."
  starttime = time.time()
  
  #the main subroutine, can be called from the python command line
  _init(infilepath)
  coltablelist=_newinput(infilepath)
  #now we have a list with all the columns and a list of pathblock information
  #now see if we need to get picture information, and if so then get it
  picloc,idslist=_handlepictures(coltablelist)
  #if this returns true, then pictures have been obtained
  #if applicable, the .png files are now located in the folder
  _createspreadsheet(coltablelist,picloc,idslist,destpath)
  
  
  endtime = time.time()
  print "Time elapsed: ", endtime-starttime
  print "Complete"
  

if __name__ == '__main__':
  #then this file is being run as a script
  try:
    #inputpath = '/home/lvotapka/scripts/sample.in'
    inputpath = sys.argv[1]
    #outputpath = '/home/lvotapka/desttest.xls'
    outputpath = sys.argv[2]
  except IndexError:
    raise Exception, "No input or no output file specified in command line."
  main(inputpath,outputpath)
