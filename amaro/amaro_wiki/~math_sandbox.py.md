# ~math sandbox.py

`
    
    
    
    #!/usr/bin/python
    ''' a little script to mess around with mathematical functions'''
    
    import sys, os
    # import numpy as np
    
    from numpy import array, arange
    
    def f0 (x, y, z):
    	''' a field equation'''
    	vecx = 0
    	vecy = 0
    	vecz = 0
    	vector = array([vecx, vecy, vecz])
    	return vector
    
    def f1 (x, y, z):
    	''' a field equation'''
    	vecx = x
    	vecy = y
    	vecz = z
    	vector = array([vecx, vecy, vecz])
    	return vector
    	
    def f2 (x, y, z):
    	''' a field equation'''
    	vecx = -y
    	vecy = x
    	vecz = 0
    	vector = array([vecx, vecy, vecz])
    	return vector
    
    def func_to_field(func, x1, y1, z1, x2, y2, z2, scale):
    	'''fills a field with values from the provided equation'''
    	xbox = []
    	for x in arange(x1, x2 + scale, scale):
    		yrect = []
    		for y in arange(y1, y2 + scale, scale):
    			zrow = []
    			for z in arange(z1, z2 + scale, scale):
    				curvec = func(x, y, z)
    				zrow.append(curvec)
    			yrect.append(array(zrow)) # add the z row to every column of y
    		xbox.append(array(yrect))
    	return array(xbox)
    		
    		
    #print func_to_field(f2,-10,-10,-10,10,10,10,scale=1.0)
    
    def divergence(vec_field):
    	'''calculates the divergence of a vector field: converts the vector field into a scalar field'''
    	scalar_field = []
    	for xrect in vec_field:
    		for yrow in xrect:
    			for vector in yrow:
    				pass
    				
    
    #========= interpolation ======
    
    # Lagrange's formula: Pn(x) = sigma(i=0 to n) yi*li(x)
    
    # Newton's method: Pn(x) = a0 + (x-x0)a1 + (x-x0)(x-x1)a2 + ... + (x-x0)(x-x1)...((x-xn
    
    

`
