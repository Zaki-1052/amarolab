# Rangerautosubmit.py

`
    
    
    
    #Lane Votapka
    # Amarolab UCI
    
    '''
    Script for automatic resubmission to the queue on ranger once a job finishes
    
    NOTE: run this job in the background or "nice" mode
    '''
    
    import sys, os
    
    waitseconds = 1200 #every 20 minutes
    
    def qstat():
        '''
        mimics the shell "qstat" command. Returns a list of running jobs on a grid
        '''
        qstatlist = []
        qstatFLO = os.popen('qstat') #this returns a file-like object containing the contents of qstat
        for i in qstatFLO:
            #make it a list of strings, each containing a line from qstat
            string = i.strip'\n'
            try:
                #we need to see if the beginning of the line is a series of numbers, if so, then its a line that we want
                int(string[:3])
                qstatlist.append(string)
            except ValueError: #then it doesn't start with a number and we can skip it
                pass
            return qstatlist
    
    
    #first we need to use the qstat command to get an idea of how the queue looks
    #right now. Later, when we compare, we can find out what is missing and run that
    #job anew
    
    oldqstat = tuple(qstat()) #our first template qstat file
    
    while 1: #loop forever, or until program is aborted internally or externally
        os.system('sleep %s' % str(waitseconds))
        newqstat = tuple(qstat())
        
    
    

`
