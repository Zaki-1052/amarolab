# Merops.py

`
    
    
    
    #Lane Votapka
    #Amarolab UCI
    
    #NOTE: because this script uses html screen-scraping techniques, it is extremely
    # brittle. MEROPS should make their database xml based
    
    '''
    obtains small molecule inhibitors from MEROPS and returns smile strings
    
    input: file of merops accession numbers separated by newline
    output: file of chemical lines that indicate the structure
    
    '''
    
    import urllib
    #import urllib2
    import re
    
    
    def getmerops(meropsid):
        '''
        retrieves info from the merops website
        '''
        base = 'http://merops.sanger.ac.uk/cgi-bin/smi_summary?mid=%s'
        url = base % meropsid
        return urllib.urlopen(url)
    
    def parsemerops(webpage):
        '''parses the merops webpage and returns specified information'''
        #to find
        information = {}
        getcommonnameline = 0 #if the indicator is on current line, then count down to significant line
        for line in webpage:
            #analyze the line
            #for the PubChem id:
            chemidpattern = '<a href="http://pubchem.ncbi.nlm.nih.gov'
            if re.search(chemidpattern,line):
                #then the chemid number is in this line
                chemid = re.findall('cid=[0-9]{6}',line)[0][4:] #the last index is to cut off
                information['chemid'] = chemid
            
            #for the chEBI id
            chEBIpattern = '<a href="http://www.ebi.ac.uk/chebi/'
            if re.search(chEBIpattern,line):
                #then the chemid number is in this line
                chEBI = re.findall('CHEBI:[0-9]{6}',line)[0][6:] #the last index is to cut off
                information['chEBI'] = chEBI
    
            #for the name of the compound
            if getcommonnameline == 1: #then here is the name line
                getcommonnameline = 0
                name = re.sub(r' *<.*?> *', '', line)
                information['name'] = name[:-1] #leave out the newline character at the end
            elif getcommonnameline > 1:
                getcommonnameline -= 1
            namepattern = 'Common name'
            if re.search(namepattern,line):
                getcommonnameline = 1 #its one line down
            #more such methods can be used to get other info
    
            #for the  name of the compound
        return information
    
    def pubchem(chemid):
        '''
        retrieves info from the pubchem website
        '''
        base = 'http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid=%s'
        url = base % chemid
        return urllib.urlopen(url)
    
    def parsepubchem(webpage):
        return information
    
    
    if __name__ == "__main__": #then we are running this as a script
        webpage = getmerops('J00043')
        meropsinformation = parsemerops(webpage)
        print meropsinformation
    
    

`
