# Inouttest.py

`
    
    
    
    #This script is a test of stdin and stdout of a program
    import sys
    xfile = sys.argv[1]
    for line in open(xfile):
        y = ' '.join((line,'pyralis'))
        print y
    
    

`
