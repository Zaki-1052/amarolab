# Cube file grid compare.py

`
    
    
    
    # script for comparing two cube files, one a big and one a little
    
    big_cube_filename  = "/extra/amarolab1/delphi_0.5.cube"
    little_cube_filename = "/extra/amarolab1/delphi_1.0.cube"
    out_filename = "/extra/amarolab1/diffmap.cube"
    big_grid_size = 191
    little_grid_size = 95
    
    
    def load_cube(filename):
        valuelist = []
        cubefile = open(filename, 'r')
        for line in cubefile.readlines():
            linelist = line.strip('\n').strip().split(' ')
            if not linelist[0]: continue
            #print linelist
            linelist = map(float,linelist)
            valuelist += linelist
        return valuelist[:]
    
    
    
    def convert_big(bigcube,little_grid_size):
        newcube = []
        index = 0
        print "len(bigcube):", len(bigcube)
        for i in range(1,little_grid_size+1):
            for j in range(1, little_grid_size+1):
                for k in range(1, little_grid_size+1):
                    index += 1
                    # if anything is even then skip it
                    if (i % 2 == 0) or (j % 2 == 0) or (k % 2 == 0): continue
                    newcube.append(bigcube[index])
        print "len(newcube):", len(newcube)
        return newcube[:]
                    
    
    def cube_compare(cube1, cube2):
        diffcube = []
        maxdiff = 0
        maxreldiff = 0
        cube1len = len(cube1)
        cube2len = len(cube2)
        if cube1len != cube2len:
            print "Error: the calculation did not result in cube files of the same length"
            print "len cube1: ", cube1len
            print "len cube2: ", cube2len
            return
        for i in xrange(cube1len):
            curdiff = cube1[i] - cube2[i]
            if curdiff > maxdiff: maxdiff = curdiff
            reldiff = curdiff / cube1
            if reldiff > maxreldiff: maxreldiff = reldiff
            diffcube.append(curdiff)
        print "The largest difference is: ", maxdiff
        print "The largest relative difference is: ", maxreldiff
        return diffcube[:]
    
    def writecube(cubelist, N, outfilename):
        outfile = open(outfilename, 'w')
        j=0
        k=0
        for i in range(0,N*N*N):
            S=str(cubelist[i])+(10-len(str(cubelist[i])))*' '
            outfile.write(S)
            j=j+1
            k=k+1
            if j>10:
                outfile.write('\n')
                j=0
            if k==N:
                outfile.write('\n\n')
                k=0
                j=0
        
        outfile.close()
        
    
    bigcube = load_cube(big_cube_filename)
    littlecube = load_cube(little_cube_filename)
    newcube = convert_big(bigcube,little_grid_size)
    # now compare the new cube to the little cube
    diffcube = cube_compare(newcube,littlecube)
    #writecube(diffcube, little_grid_size, out_filename)
    
    

`
