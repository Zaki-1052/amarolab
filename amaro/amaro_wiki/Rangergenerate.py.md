# Rangergenerate.py

`
    
    
    
    #Lane Votapka
    #UCI Amarolab
    
    '''
    This script generates ranger input files and scripts for ease of use in ranger
    
    takes as input:
    
    python rangergenerate.py <base> <number> <topology> <coord> <number of steps>
    
    base: the base name of these files to be used
    number: which round of dynamics are we at now
    topology: the name of the parm/top file
    coord: the restart file
    numberofsteps: the total number of steps the trajectory will take
    
    What it does:
    Ranger has the unfortunate problem that a submitted job will not usually run to
    completion in a single run. It is a nuisance to submit multiple times, changing
    the firsttimestep variable etc. in the input file
    This script takes templates for a ranger submission script and NAMD input file
    as well as (optionally) the previous submission and input files and quickly generates
    he next step in the NAMD runs.
    At that point, all you should need to do is check the status of your job, and if it
    has timed out, you simply run this script, with a changed number, and submit the next step in the MD
    
    NOTE the first run of this script requires that you manually change the PMEgridSize variables
    in the input file to their proper values. After this, those numbers should be automatically
    detected from previously generated input files
    
    How it works:
    This program takes two template files: an input file and a submit file, each has variables
    denoted by <names within corner brackets> that the script will automatically change in the
    output scripts. Therefore these template files can be easily customized by you.
    
    The script detects the values of these variables automatically based on the script arguments
    and information from previous runs (if present)
    
    
    '''
    def _getstartlines(ifile):
        """Return a list of offsets where newlines are located.""" 
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
    
        
    
    def findlasttimestep(filename,expr):
        '''
        takes a filename as an argument, searches for a specific string
        indicating the final time step and returns the final time step
        '''
        #search the file bottom up for any line containing value of expr
        rightline = None
        #open the file
        ifile = open(filename,'r')
        startlines = _getstartlines(ifile) #get the location of every newline character
        startlines.reverse()#reverse the locations
        #print startlines
        for i in startlines:
            ifile.seek(i+1)
            curline = ifile.readline()
            if re.search(expr,curline): break
            #i+=1
        lasttimestep = re.sub(expr,'',curline)
        #print lasttimestep
        lasttimestep = lasttimestep.strip() #remove excess white spaces
        return lasttimestep
    
    #==============================================================================
    #variables that need to be changed
    # <path> to the current location
    # <inputfile> the input .inp file
    # <outputfile> the output .out file
    
    # <inptraj> input trajectory filename
    # <outtraj> output trajectory filename
    # <firsttimestep> final time step from previous output file
    # <prmtop> parmtop file
    # <inpcrd> coordinate/restart file
    # <numsteps> number of steps in the simulations in fs
    # <PMEGridSizeX>
    # <PMEGridSizeY>
    # <PMEGridSizeZ>
    
    import sys, time, os
    import re
    
    #assign variables
    success = True
    path = os.getcwd() + '/' #our current directory
    base = sys.argv[1] #the base name; example: HK, MS, ...
    number = sys.argv[2] #the number of this dynamics run
    prevnumber = str(int(number)-1)
    
    outtraj = '%s-eq%s' % (base, number)
    previousoutputfilename = '%s/%s%s.out' % (path, base, prevnumber) #output file name
    if prevnumber > 0:
        inptraj = '%s-eq%s' % (base, prevnumber)
        previousinputfilename = '%s/%s%s.inp' % (path, base, prevnumber) #output file name
    else: #then this is the first time
        print "This is the first run. You will need to go into the input file and change <inptraj> and <inputfile> manually."
        inptraj = '<inptraj>'
        previousinputfilename = '<inputfile>'
    prmtop = sys.argv[3] #the prmtop file
    inpcrd = sys.argv[4] #the inpcrd file
    numsteps = sys.argv[5] #number of steps
    
    templateinpfilename = sys.path[0] + '/' + inputtemplate.txt#'/home/lvotapka/Desktop/inputtemplate.txt' #the location of the template input and bash files
    templatebashfilename = sys.path[0] + '/' + submittemplate.txt#'/home/lvotapka/Desktop/submittemplate.txt'
    
    #==============================================================================================
    #NOTE: modify these strings if you want them to have a different naming scheme
    destinpfilename = '%s%s%s.inp' % (path, base, number) #input file name
    inpfile = '%s%s.inp' % (base,number)
    outputfilename = '%s%s%s.out' % (path, base, number) #output file name
    outfile = '%s%s.out' % (base,number)
    destbashfilename = '%s%s%s.bash' % (path, base, number)
    #==============================================================================================
    #print destinpfilename
    #print destbashfilename
    
    templateinp = open(templateinpfilename,'r')
    templatebash = open(templatebashfilename, 'r')
    
    destinp = open(destinpfilename,'w')
    destbash = open(destbashfilename, 'w')
    
    #try to find the previous time step
    #previousoutputfilename = '%s/%s%s.out' % (path, base, prevnumber) #output file name
    firsttimestepexpr='WRITING VELOCITIES TO RESTART FILE AT STEP '
    pmegridsizexexpr ='PMEGridSizeX '
    pmegridsizeyexpr ='PMEGridSizeY '
    pmegridsizezexpr ='PMEGridSizeZ '
    try:
        #print "Setting first time step to: ", firsttimestep
        firsttimestep = findlasttimestep(previousoutputfilename,firsttimestepexpr)
        if firsttimestep < numsteps: #then it hasn't run to completion
            print "Setting first time step to: ", firsttimestep
        else:
            print "ALERT! Trying to generate input files for a finished trajectory. It is recommended that you set your <number of steps> argument to a higher value if you want to continue this simulation."
            success = False
    except IOError:
        print "Previous output file not found. setting first time step to zero"
        firsttimestep = '0'
    #try to find the PME grid sizes using the previous input file
    try:
        pmegridsizex = findlasttimestep(previousinputfilename,pmegridsizexexpr)
        pmegridsizey = findlasttimestep(previousinputfilename,pmegridsizeyexpr)
        pmegridsizez = findlasttimestep(previousinputfilename,pmegridsizezexpr)
    except IOError:
        print "Unable to locate PMEGridSize variables in the previous input file; the file may not exist. You will need to go back and change them manually"
        pmegridsizex = '<pmegridsizex>'
        pmegridsizey = '<pmegridsizey>'
        pmegridsizez = '<pmegridsizez>'
    #now generate the accession dictionary
    filters = {
        '<path>':path,
        '<inputfile>':inpfile,
        '<outputfile>':outfile,
        '<inptraj>':inptraj,
        '<outtraj>':outtraj,
        '<firsttimestep>':firsttimestep,
        '<prmtop>':prmtop,
        '<inpcrd>':inpcrd,
        '<numsteps>':numsteps,
        '<PMEGridSizeX>':pmegridsizex,
        '<PMEGridSizeY>':pmegridsizey,
        '<PMEGridSizeZ>':pmegridsizez
        }
    
    
    for line in templateinp: #run through each line in the input file template
        #replace any regular expressions
        newstring = line
        for pair in filters: #run through every pair in the dictionary
            newstring = re.sub(pair,filters[pair],newstring)
        print newstring
        #place the line into the new output file
        destinp.write(newstring)
    
    for line in templatebash:
        #replace any regular expressions
        newstring = line
        for pair in filters: #run through every pair in the dictionary
            newstring = re.sub(pair,filters[pair],newstring)
        #print newstring
        #place the line into the new output file
        destbash.write(newstring)
    
    destinp.close()
    destbash.close()
    #findlasttimestep('/home/lvotapka/Desktop/inputtemplate.txt', 'PMEGridSizeZ')
    if success == True:
        print "Submission script and Input File successfully created! Enter 'qsub %s%s.bash' to run your job now." % (base, number)
    
    

`
