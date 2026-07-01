# Ligalign.py

`
    
    
    
    #Lane Votapka
    #Amarolab UCI
    #2011
    
    '''
    LigAlign - INCOMPLETE
    
    A program that takes two pdbs as input, each containing a 'residue' that is a
    ligand.
    
    If the ligands are identical, but they are separately labelled, this program
    labels one of them in accordance with the other. So really the only thing
    that changes is the order and name of the atoms
    
    invokation:
    
    python ligalign.py <static>.pdb <static resname> <dynamic>.pdb <dynamic resname>
    
    '''
    
    import sys
    import time
    from math import sqrt
    from pprint import pprint
    
    print "running..."
    
    #staticfilename = sys.argv[1]
    staticfilename = '/home/lvotapka/Desktop/cpafdock/omuralide.pdb'
    #staticresname = sys.argv[2]
    staticresname = 'LAS'
    
    #dynamicfilename = sys.argv[3]
    dynamicfilename = '/scratch/lvotapka/projects/cpaf/3DPM.pdb'
    #dynamicresname = sys.argv[4]
    dynamicresname = 'LAS'
    
    #PDB field designation constants
    fieldrecord, fieldatomnum, fieldatomname, fieldresname, fieldchain, fieldresnum, fieldx, fieldy, fieldz, fieldtemp, fieldoccupancy = range(11)
    
    class Atom(): #the atom superclass
        def __init__(self): #initialize the variables
            self.ident = ''
            self.connections = []
            self.maxconnections = 0
            self.minconnections = 0
            self.coords = (0,0,0)
            self.maxradius = 0.0
        def connect(self, otheratom):   #make a new connection to a new atom
            if len(self.connections) < self.maxconnections:
                self.connections.append(otheratom)
        def setident(self,newident):
            self.ident = newident
        def setcoords(self,coords):
            self.coords = coords
        def getcoords(self):
            return self.coords
    
    class Carbon(Atom):
        def __init__(self): #initialize the variables
            self.ident = ''
            self.connections = []
            self.maxconnections = 4
            self.minconnections = 2
            self.coords = (0,0,0)
            self.maxradius = 0.80
    class Nitrogen(Atom):
        def __init__(self): #initialize the variables
            self.ident = ''
            self.connections = []
            self.maxconnections = 3
            self.minconnections = 1
            self.coords = (0,0,0)
            self.maxradius = 0.70
    class Oxygen(Atom):
        def __init__(self): #initialize the variables
            self.ident = ''
            self.connections = []
            self.maxconnections = 2
            self.minconnections = 1
            self.coords = (0,0,0)
            self.maxradius = 0.65
    class Sulfur(Atom):
        def __init__(self): #initialize the variables
            self.ident = ''
            self.connections = []
            self.maxconnections = 2
            self.minconnections = 1
            self.coords = (0,0,0)
            self.maxradius = 1.05
    class Chlorine(Atom):
        def __init__(self): #initialize the variables
            self.ident = ''
            self.connections = []
            self.maxconnections = 1
            self.minconnections = 1
            self.coords = (0,0,0)
            self.maxradius = 0.0
    class Fluorine(Atom):
        def __init__(self): #initialize the variables
            self.ident = ''
            self.connections = []
            self.maxconnections = 1
            self.minconnections = 1
            self.coords = (0,0,0)
            self.maxradius = 0.0
    class Phosphorous(Atom):
        def __init__(self): #initialize the variables
            self.ident = ''
            self.connections = []
            self.maxconnections = 3
            self.minconnections = 1
            self.coords = (0,0,0)
            self.maxradius = 0.0
    
    def parsepdb(line):
        #returns a tuple containing everything we need to know
        record = line[0:7].strip()
        atomnum = line[7:13].strip()
        atomname = line[13:17].strip()
        resname = line[17:20].strip()
        chain = line[20:21].strip()
        resnum = line[21:30].strip()
        x = line[30:38].strip()
        y = line[38:46].strip()
        z = line[46:54].strip()
        temp = line[54:60].strip()
        occupancy = line[60:66].strip()
        return (record,atomnum,atomname,resname,chain,resnum,x,y,z,temp,occupancy)
    
    def _loadproperlines(filename,ligresname,noH=True):
        xlist = []
        for line in open(filename):
            line = parsepdb(line)
            if line[fieldrecord] == "ATOM" or line[fieldrecord] == "HETATM":
                if line[fieldresname] == ligresname: #check if its a ligand atom
                    if line[fieldatomname][0] <> 'H' or noH == False: #make sure we arent adding a hydrogen
                        #now add it
                        xlist.append(line)
            if line[fieldrecord] == "END" or line[fieldrecord] == "ENDMDL": break #if this is the end of a molecule, then this is all we need
        #return the entire list
        #print xlist
        return xlist[:]
    
    def _createatom(atomtype,atomname):
        atomtype = atomtype.lower()
        if atomtype == "c": #its a carbon atom
            atom = Carbon()
        elif atomtype == "n": #nitrogen
            atom = Nitrogen()
        elif atomtype == "o": #oxygen
            atom = Oxygen()
        elif atomtype == "x": #chlorine
            atom = Chlorine()
        elif atomtype == "f": #fluorine
            atom = Fluorine()
        elif atomtype == "p": #phosphorous
            atom = Phosphorous()
        else:
            atom = Atom()
        atom.setident(atomname)
        return atom
    
    def vecdist(v1,v2):
        #each vector is a tuple containing a point
        assert len(v1) == len(v2), "Vecdist function: the vectors must be of equal dimensionality"
        vd = [] #this list will contain the difference coords
        for i in range(len(v1)):
            diff = v1[i] - v2[i]
            vd.append(diff*diff)
        distance = reduce(lambda x,y: x+y, vd)
        return sqrt(distance)
        
    
    #step 1: information parsing ======================================
    
    #first load the pdb files
    staticligandraw=_loadproperlines(staticfilename,staticresname)
    dynamicligandraw=_loadproperlines(dynamicfilename,dynamicresname)
    
    #pprint(dynamicligandraw)
    #pprint(staticligandraw)
    #setting the two atoms to be of identical length
    if len(staticligandraw)>len(dynamicligandraw): staticligandraw = staticligandraw[:len(dynamicligandraw)]
    if len(dynamicligandraw)>len(staticligandraw): dynamicligandraw = dynamicligandraw[:len(staticligandraw)]
    staticligandatoms = []
    for i in staticligandraw:
        atomname=i[fieldatomname]
        atomtype = atomname[0]
        atomcoords = (float(i[fieldx]),float(i[fieldy]),float(i[fieldz]))
        #print "atom coords:", atomcoords
        atom = _createatom(atomtype,atomname)
        atom.setcoords(atomcoords)
        #print "atom coords:", atom.getcoords()
        staticligandatoms.append(atom)
    dynamicligandatoms = []
    for i in dynamicligandraw:
        atomname=i[fieldatomname]
        atomtype = atomname[0]
        atomcoords = (float(i[fieldx]),float(i[fieldy]),float(i[fieldz]))
        atom = _createatom(atomtype,atomname)
        atom.setcoords = atomcoords
        dynamicligandatoms.append(atom)
    
    #print dynamicligandatoms
    #print staticligandatoms
    
    
    #Step 2: making the bonds =========================================
    def isbond(distance,a1radius,a2radius):
        if distance <= a1radius + a2radius:
            return True
        else:
            return False
    
    def rankbonds(pair,xlist):
        #we pass a duet tuple to this function
        #if the list is empty
        if len(xlist) == 0:
            xlist.append(pair)
        else: #otherwise, then go through the list until we find a distance larger than the pair's
            for i in range(len(xlist)):
                newdist = pair[0]
                idist = xlist[i][0]
                if newdist < idist:
                    #then insert this value just before it
                    xlist.insert(i,pair)
                    break
            if pair not in xlist: xlist.append(pair) #if it isnt added yet, then add it now
        return xlist[:]
    #now we need to go through all the atoms and find all their connections
    def _findallbonds(xlist):
        #print xlist
        for atom in xlist: #for each atom in xlist
            atomcoords = atom.getcoords()
            #print atomcoords
            likelybonds = []
            distlist = []
            for compatom in xlist: #for each atom again
                #we need to compare the coordinates
                compatomcoords = compatom.getcoords()
                distance = vecdist(atomcoords,compatomcoords)
                if (atom is compatom): continue #then its finding itself
                #check to see if there is a bond between these two atoms
                distlist = rankbonds((distance,compatom),distlist)
                #print distlist
    
                if isbond(distance,atom.maxradius,compatom.maxradius):
                    #then there is likely a connection
                    likelybonds=rankbonds((distance,compatom),likelybonds) #insert the new distance into the list in the properly ordered place
                    while len(likelybonds) > atom.maxconnections: likelybonds.pop() #if there are too many bonds, then pop the furthest ones until the atom has a proper number of bonds    
            if len(likelybonds)<atom.minconnections:likelybonds=distlist[atom.minconnections] #if there are too few bonds then slice the beginning of the destlist until we have enough
            #print len(distlist)
            print likelybonds
            atom.connections=likelybonds[:]
    #print "Check distance function 1: ", vecdist((0,0,0),(0,0,0))
    #print "Check distance function 2: ", vecdist((0,0,0),(1,0,0))
    #print "Check distance function 3: ", vecdist((0,0,0),(1,1,1))
    #print "Check distance function 4: ", vecdist((-10.468,7.633,20.193),(-13.456,14.798,24.856))
    _findallbonds(staticligandatoms)
    print "static ligand atom connections: ", staticligandatoms[13].connections
    
    print "INCOMPLETE"
    
    print "complete"
    
    

`
