#modscience:
# useful science functions

#import Bio
import urllib
import numpy


def calc_salt_atoms(volume, molarity=0.02):
    ''' given a volume and molarity of a waterbox, will return the number of salt atoms for that molarity'''
    #molarity = 0.02
    LperAng = 1e-27
    Avos = 6.022e23
    return volume*molarity*LperAng*Avos


def residconvert(factor,resids=None):
    ''' increments the values of resids by a certain factor'''
    if resids==None: resids = "117 to 119, 133 to 138, 146 to 152, 156, 178 to 180, 196 to 200, 223 to 227, 243 to 247, 276 to 278, 293 to 295, 346 to 350, 368 to 371, 325, 403 to 406 and 426 to 441"
    resids = resids.replace(',','')
    reslist = resids.split()
    newreslist=[]
    for res in reslist:
        #check if its numeric
        try:
            resnum = int(res)
            newreslist.append(resnum - 82 + factor)
        except:
            newreslist.append(res)

    newreslist = map(str,newreslist)
    newreslist.remove('and')
    newstring = ' '.join(newreslist)

    return newstring

def getpdb(ident,filename):
    '''retrieves a pdb file from the online database and writes it to a separate file
        ident = pdb ID number
        filename = destination file address
    '''
    import urllib
    base = 'http://www.rcsb.org/pdb/files/%s.pdb'
    fullurl = base % ident #generate our url address
    page = urllib.urlopen(fullurl) #file handler for the page
    pdbfile = open(filename,'w') #open our file
    for line in page:
        pdbfile.write(line) #copy every line to the file
    pdbfile.close() #close our file
    return
    
    

def getpdbs(filename=None):
    '''filename contains a list of pdbs to retrieve'''
    if filename == None: filename='/home/lvotapka/Desktop/projects/cpaf/homologs/structures.txt'
    pdblist = []
    for line in open(filename): pdblist.append(line.replace('\n','')) #add the pdb file to the list
    for item in pdblist:
        destfilename = "%s.pdb" % item
        getpdb(item,destfilename)
    return
    
def quaternion_to_euler(q):
    ''' converts a quaternion to Euler angles '''
    #import numpy as np
    from math import atan, acos, asin
    q0 = q[0]
    q1 = q[1]
    q2 = q[2]
    q3 = q[3]
    phi = atan(2 * (q0*q1 + q2*q3) / (1 - (2 * (q1**2 + q2**2))))
    theta = asin(2 * (q0*q2 - q3*q1))
    psi = atan(2 * (q0*q3 + q2*q1) / (1 - (2 * (q2**2 + q3**2))))
    return [theta, phi, psi]

protfilename = '/soft/linux/pdb2pqr-1.8/dat/CHARMM.DAT' # straight from pdb2pqr data

def get_radii(datfile=protfilename):
    ''' gets radii data from a forcefield .DAT file '''
    sizdict = {}
    protfile = open(datfile, 'r')
    for line in protfile.xreadlines():
        if line == "\n" or line[0] == "#": continue
        #splitline = line.strip().split()
        #atomname = splitline[0]
        line = line.split('\t')
        atomname = line[1].strip()
        
        resname = line[0].strip()
        if resname == "HSD":
            resname = "HIS"
        
        crg = line[2]
        siz = line[3]
        
        if resname not in sizdict.keys():
            sizdict[resname] = {}
        sizdict[resname][atomname] = siz
    return sizdict


def normalize_vector(array, axis=-1):
    """
    Normalize the vectors of A in the direction of axis. This means that each
    vector will have length 1. The default axis is the last.
    
    Arguments:
    
        - array (``numpy.ndarray``) A numpy array.
        - axis (``int``) The axis which will have vectors of lenght 1.
    """
    shape = list(array.shape)
    shape[axis] = 1
    length = numpy.sqrt((array*array).sum(axis))   
    out = array / length.reshape(shape)
    return out

def interp_sphere(four_coords, guess):
    '''input: 4 coordinate values
        and an array/matrix of length 4, will be the guessed center/rad of sphere
        '''
    fc = four_coords # coordinates lying on the surface of the sphere
    F = numpy.zeros([4,1]) # vector created by guess and nonlinear system
    J = numpy.zeros([4,4]) # Jacobian matrix of nonlinear system
    for i in range(4):
        F[i,0] = (guess[0] - fc[i][0])**2 + (guess[1] - fc[i][1])**2 + (guess[2] - fc[i][2])**2 - guess[3]**2
        for f in range(3):
            J[i,f] = 2 * (guess[f] - fc[i,f])
        J[i,3] = -2 * guess[3]
    return F, J
                          
def newton_nonlinear_system(F, params, init_guess=None, err=0.0001, max_iter=1000):
    '''given a nonlinear system of functions F and
    function parameters, will use Newton's method
    to try to converge the solution'''
    if init_guess == None: init_guess=numpy.ones([len(params),1])
    x = init_guess
    for k in range(max_iter):
        nonlinsys, jacobian = F(params, x) # get F and J
        y = numpy.linalg.solve(jacobian, -nonlinsys) # solve the system
        x = x + y # increment the answer
        ynorm = numpy.linalg.norm(y) # get the norm of y
        if ynorm < err:
            return x # break out, we have converged a solution
    print "Alert: newton_nonlinear_system unable to converge"
    return
        
def shape_intersects_sphere(sphere, shape):
  ''' Determines whether a shape intersects the shell of a sphere.
  
  sphere: a dictionary containing 'x','y','z', & 'radius' indeces
  shape: a list of 3-tuples of the points defining a shape 
  '''
  pass
