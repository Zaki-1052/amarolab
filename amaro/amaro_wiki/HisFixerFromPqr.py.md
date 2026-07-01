# HisFixerFromPqr.py

`
    
    
    
    #by Lane Votapka
    #Amarolab at University of California, Irvine
    
    '''
    when a pdb is run through the pqr server, it often changes the last letter
    of the HIS protein name, to become either HID, HIE, or HIP in the pqr file.
    We want to change the PDB file so that every HIS says the same as the PQR
    
    commandline (3 script arguments):
    python hisFixerFromPqr.py <input pdb> <input pqr> <output pdb>
    
    '''
    #init
    import sys
    def HisFixer(pdb,pqr,output):
        print "Histidine Fixer Running..."
        import time
        import pprint
        starttime = time.time()
        srctargets = ('HID', 'HIE', 'HIP')
        desttarget = ['HIS']
        savedPQRline = ''
        pdbresidloc = 5
        pqrresidloc = 4
        pqrresnameloc = 3
        HISloc = 3
        newHIS = ''
        tResid = ''
        waitingpqr = False
        oResid = 0
    
        #first we load the necessary files
        #the template file: pqr
        templatefilename = pqr #"/home/lvotapka/projects/h3charge/pdb1hgdprotandwater.pqr"
        templatefile = open(templatefilename, 'r')
    
        #the old file: pdb
        oldfilename = pdb #"/home/lvotapka/projects/h3charge/pdb1hgdprotandwater2.pdb"
        oldfile = open(oldfilename, 'r')
    
        #the new file: pdb
        newfilename = output #"/home/lvotapka/projects/h3charge/pdb1hgdprotandwater3.pqr"
        newfile = open(newfilename, 'w')
    
        try:
    
            #run through oldfile to find all instances of changes
    
            for oline in oldfile:
                olineparts = oline.strip().split()
                if olineparts and (olineparts[0] == 'ATOM' ) and (olineparts[HISloc] in desttarget) and (oline):
                    whichdesttarget = desttarget.index(olineparts[HISloc])
    		#we've found a line that has HIS or CYS
                    if olineparts[pdbresidloc] <> oResid:
                        oResid = olineparts[pdbresidloc]
                        #only in this case would we reset the pqr list
                        waitingpqr = False
                    
    
                    if not waitingpqr:
                        if (savedPQRline) and (savedPQRline[pqrresidloc] == oResid) and (savedPQRline[pqrresnameloc] in srctargets):
                            newHIS = savedPQRline[HISloc]
                            savedPQRline = ''
                            
                        else:
                            foundHISspot = False #this is to make it loop to the HIS and through it, stopping when it gets to a new residue
                            #here we need to check to make sure we arent double-checking the
                            # HIS entries in the tfile
                            while 1:
                                tline = templatefile.readline()
                                if not tline: break #if tline has reached the end of the file or something
                                tlineparts = tline.strip().split()
                                if tlineparts[0] == 'ATOM':
                                    tResid = tlineparts[pqrresidloc]
                                    tResname = tlineparts[pqrresnameloc]
                                    if tResid == oResid and tResname in srctargets:
                                        if foundHISspot == False:
                                            #assign the new HIS value
                                            newHIS = tlineparts[HISloc]
                                            print "New HIS:", newHIS
                                            foundHISspot = True
                                    else:
                                        if foundHISspot:
                                            #we've reached the end of the residue and need to save the new line
                                            savedPQRline = tlineparts
                                            # we need to activate waiting variable
                                            waitingpqr = True
                                            break
    
                    #generate the new oline
                    oline = oline.replace(desttarget[whichdesttarget], newHIS) #replaced 'HIS' with 'HID/E/P' or 'CYS' with 'CYS/X'
                    #print oline
                    
                #write the oline to newfile
                newfile.write(oline)
                #print oline
    
        finally:
            #close all files
            templatefile.close()
            oldfile.close()
            newfile.close()
    
        #terminate
        endtime = time.time()
        print "Time elapsed: " + str(endtime - starttime)
        print "Complete"
    
    if __name__ == "__main__":
        #try:
        pdb = sys.argv[1]
        pqr = sys.argv[2]
        output = sys.argv[3]
        HisFixer(pdb,pqr,output)
        #except IndexError:
            #raise Exception "incorrect arguments entered."
        
    
    
    #BUG: when the search gets to the HIS on the PDB list, it searches through
    # the PQR list until it reaches the end of the residue, then it goes back to
    # the PDB. Unfortunately, at that point it starts the search through PQR again
    # We need to create a variable "waitingpqr", that is activated when PQR reaches
    # the end of its list, and is deactivated when oresid (pdb residue) is changed
    
    
    

`
