# Comparecellvalues.py

`
    
    
    
    #By Lane Votapka
    #Amarolab UCI Pharm Sci
    
    '''
    Script for comparing cells of individual files, choosing one of the cells, and
    placing them into an equivalent spot in a new file
    
    Each input file must be of the same length and width
    
    this python script takes any number of files for arguments. It then uses a
    comparison function of some kind to choose one of the cells to place into the
    new file
    
    format: python comparecellvalues.py outputfile input1 input2 [input3...]
    
    By Lane Votapka
    Amarolab UCI Pharm Sci
    
    '''
    import sys
    
    
    sepval='\t'
    
    def lowest(inputlist):
        '''
        this function accepts a list/tuple as an argument and returns the lowest value
        '''
        inputlist=map(float,inputlist)
        inputlist=list(inputlist)
        inputlist.sort()
        finalval = inputlist[0] #this will give you the lowest value in the list
        return str(finalval)
    
    outputfilename=sys.argv[1] #the name of the output file
    #'/scratch/lvotapka/projects/N1pocketanalysis/3nss_apo_tet.lowest.txt'#
    inputfilename=sys.argv[2:] #a list containing the names of the input files
    #['/scratch/lvotapka/projects/N1pocketanalysis/3nss_apo_tet.cb.txt','/scratch/lvotapka/projects/N1pocketanalysis/3nss_apo_tet.cc1.txt','/scratch/lvotapka/projects/N1pocketanalysis/3nss_apo_tet.cc2.txt','/scratch/lvotapka/projects/N1pocketanalysis/3nss_apo_tet.cd.xls']
    
    numinputfiles=len(inputfilename)
    
    inputfiles=[]
    for filename in inputfilename: #for each input file
        inputfiles.append(open(filename,'r'))   #open all of them inside a list
    
    outputfile=open(outputfilename,'w')
    
    #assuming all the input files are the same length, just read them line by line
    for line in inputfiles[0].readlines(): #open the first one
        lines = [line.strip().split(sepval)] #add the first one to the 'lines' list
        for i in range(1,numinputfiles):
            lines.append(inputfiles[i].readline().strip().split(sepval)) #add the rest of the lines to the lines list
        #print lines[1]
        #now run through each of the indeces
        bests=[]
        for index in range(len(lines[0])):
            units=[]
            #for each of the units in the lines list
            for unit in lines:
                units.append(unit[index])
            best=lowest(units) #best contains the one we want at this particular index
            bests.append(best)
        #bests now is a list that contains the numbers we want
        bests.append('\n') #add a newline
        newline='\t'.join(bests)
        #now write the newline
        outputfile.write(newline)
        # print newline
    
    outputfile.close()
                
        
    
    

`
