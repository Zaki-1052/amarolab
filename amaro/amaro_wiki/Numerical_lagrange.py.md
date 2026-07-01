# Numerical lagrange.py

`
    
    
    
    # numerical optimization of a Lagrange multiplier
    
    # given a function f, and constraints g, will find the minimum value
    #  of a Lagrangian, which contains the function and the constraints
    
    import numpy as np
    from math import sqrt
    import random
    
    # Simple example
    
    # L(x,lambda) = f(x) + lam*g(x)
    # f = x**2
    # g = x**2 - 1
    
    # using Newton's method:
    
    # G(x) = x - J(x)**-1 * F(x)
    max_iter = 100
    x = np.matrix([[2,2]]).T # initial guess
    TOL = 0.0001 # tolerance
    F = np.matrix(np.zeros((2,1))) # a vector of function values
    J = np.matrix(np.zeros((2,2))) # a Jacobian for the function
    
    print "One-D example"
    for k in range(max_iter):
      print "step:", k, "x:", x
      # calculate function values
      F[0,0] = 2*x[0] + 2*x[0]*x[1]
      F[1,0] = x[0]**2 - 1
    
      # calculate Jacobian
      J[0,0] = 2+2*x[1]
      J[0,1] = 2*x[0]
      J[1,0] = 2*x[0]
      J[1,1] = 0
    
      y = np.linalg.solve(J, -F)
      x = x+y
      if np.linalg.norm(y) < TOL: break
    
    print "Finished.\n\n"
    
    # 2D optimal rotation example
    print "Two-D optimal rotation example"
    
    max_iter = 100
    x = np.matrix(np.ones((7,1))) # initial guess
    for i in range(7):
      x[i,0] = i/6.0 - 2
    right_angle = 1 #sqrt(2)/2
    #x[0] = right_angle; x[1] = right_angle; x[2] = right_angle; x[3] = -2*right_angle
    TOL = 0.0001 # tolerance
    F = np.matrix(np.zeros((7,1))) # a vector of function values
    J = np.matrix(np.zeros((7,7))) # a Jacobian for the function
    
    for k in range(max_iter):
      print "step:", k, "x:", x
      '''
      # original F and J: f includes only dot product: WARNING: gives wrong answer
      # calculate function values
      F[0,0] = 1 + 2*x[4]*x[0] + x[6]*x[1]
      F[1,0] = 1 + 2*x[5]*x[1] + x[6]*x[0]
      F[2,0] = 1 + 2*x[4]*x[2] + x[6]*x[3]
      F[3,0] = 1 + 2*x[5]*x[3] + x[6]*x[2]
      F[4,0] = x[0]**2 + x[2]**2 - 1
      F[5,0] = x[1]**2 + x[3]**2 - 1
      F[6,0] = x[0]*x[1] + x[2]*x[3]
      
    
      J = np.matrix(np.zeros((7,7))) # zero the Jacobian
      # calculate Jacobian
      J[0,0] = 2*x[4]; J[0,1] = x[6]; J[0,4] = 2*x[0]; J[0,6]=x[1]
      J[1,0] = x[6]; J[1,1] = 2*x[5]; J[1,5] = 2*x[1]; J[1,6]=x[0]
      J[2,2] = 2*x[4]; J[2,3] = x[6]; J[2,4] = 2*x[2]; J[2,6]=x[3]
      J[3,2] = x[6]; J[3,3] = 2*x[5]; J[3,5] = 2*x[3]; J[3,6]=x[2]
      J[4,0] = 2*x[0]; J[4,2] = 2*x[2]
      J[5,1] = 2*x[1]; J[5,3] = 2*x[3]
      J[6,0] = x[1]; J[6,1] = x[0]; J[6,2] = x[3]; J[6,3] = x[2]
      '''
      '''
      # dot product squared. WARNING: degenerate
      # calculate function values
      F[0,0] = 2*x[0] + 2*x[4]*x[0] + x[6]*x[1]
      F[1,0] = 2*x[1] + 2*x[5]*x[1] + x[6]*x[0]
      F[2,0] = 2*x[2] + 2*x[4]*x[2] + x[6]*x[3]
      F[3,0] = 2*x[3] + 2*x[5]*x[3] + x[6]*x[2]
      F[4,0] = x[0]**2 + x[2]**2 - 1
      F[5,0] = x[1]**2 + x[3]**2 - 1
      F[6,0] = x[0]*x[1] + x[2]*x[3]
      
    
      J = np.matrix(np.zeros((7,7))) # zero the Jacobian
      # calculate Jacobian
      J[0,0] = 2+2*x[4]; J[0,1] = x[6]; J[0,4] = 2*x[0]; J[0,6]=x[1]
      J[1,0] = x[6]; J[1,1] = 2+2*x[5]; J[1,5] = 2*x[1]; J[1,6]=x[0]
      J[2,2] = 2+2*x[4]; J[2,3] = x[6]; J[2,4] = 2*x[2]; J[2,6]=x[3]
      J[3,2] = x[6]; J[3,3] = 2+2*x[5]; J[3,5] = 2*x[3]; J[3,6]=x[2]
      J[4,0] = 2*x[0]; J[4,2] = 2*x[2]
      J[5,1] = 2*x[1]; J[5,3] = 2*x[3]
      J[6,0] = x[1]; J[6,1] = x[0]; J[6,2] = x[3]; J[6,3] = x[2]
      '''
    
      # f is the sum of M**-2
      # calculate function values
      F[0,0] = -2*x[0]**-3 + 2*x[4]*x[0] + x[5]*x[1]
      F[1,0] = -2*x[1]**-3 + 2*x[6]*x[1] + x[5]*x[0]
      F[2,0] = -2*x[2]**-3 + 2*x[4]*x[2] + x[5]*x[3]
      F[3,0] = -2*x[3]**-3 + 2*x[6]*x[3] + x[5]*x[2]
      F[4,0] = x[0]**2 + x[2]**2 - 1
      F[6,0] = x[1]**2 + x[3]**2 - 1
      F[5,0] = x[0]*x[1] + x[2]*x[3]
      
    
      J = np.matrix(np.zeros((7,7))) # zero the Jacobian
      # calculate Jacobian
      J[0,0] = 6*x[0]**-4 + 2*x[4]; J[0,1] = x[5]; J[0,4] = 2*x[0]; J[0,5]=x[1]
      J[1,0] = x[5]; J[1,1] = 6*x[1]**-4 + 2*x[6]; J[1,6] = 2*x[1]; J[1,5]=x[0]
      J[2,2] = 6*x[2]**-4 + 2*x[4]; J[2,3] = x[5]; J[2,4] = 2*x[2]; J[2,5]=x[3]
      J[3,2] = x[5]; J[3,3] = 6*x[3]**-4 + 2*x[6]; J[3,6] = 2*x[3]; J[3,5]=x[2]
      J[4,0] = 2*x[0]; J[4,2] = 2*x[2]
      J[6,1] = 2*x[1]; J[6,3] = 2*x[3]
      J[5,0] = x[1]; J[5,1] = x[0]; J[5,2] = x[3]; J[5,3] = x[2]  
      y = np.linalg.solve(J, -F)
      x = x+y
      if np.linalg.norm(y) < TOL: break
      #print "F(before):", F
      #print "J(before):", J
      #break
    
    print "Finished.\n\n"
    print "x(before):", x
    
    
    # N-D optimal rotation example
    d = 8 # number of dimensions
    print "%d-D optimal rotation example" % d
    num_eqs = d**2 + (d+1)*d/2 # number of nonlinear equations
    lambda_start = d**2 # where the matrix variables end and the lamda vars start
    max_iter = 100
    x = np.matrix(np.ones((num_eqs,1))) # initial guess
    
    for n in range(d):
      for m in range(d):
        if n==m and m!= 0:
          x[n*d + m] = -sqrt(1.0/d) #-0.5# * random.random()
        else:
          x[n*d + m] = sqrt(1.0/d) #0.5 # * random.random()
    
    for i in range(lambda_start,num_eqs):
      x[i] = i
      pass
    
    #for i in range(7):
    #  x[i,0] = i/6.0 - 2
    
    right_angle = 1 #sqrt(2)/2
    
    #x[0] = right_angle; x[1] = right_angle; x[2] = right_angle; x[3] = -2*right_angle
    TOL = 0.0001 # tolerance
    F = np.matrix(np.zeros((num_eqs,1))) # a vector of function values
    F_true = np.matrix(np.zeros((num_eqs,1))) #an explicitly found vector F
    J = np.matrix(np.zeros((num_eqs,num_eqs))) # a Jacobian for the function
    J_true = np.matrix(np.zeros((num_eqs,num_eqs))) # an explicitly found Jacobian
    print "lambda_start:", lambda_start
    
    
    
    for num_iter in range(max_iter):
      #print "step:", num_iter #, "x:", x
      f = 0.0
      # f is the sum of M**-2
      # calculate function values for the rotation matrix
      for n in range(d): # for each member of matrix M
        for m in range(d):
          n_m = d*n + m # get a 1d index for n and m
          sum_over_k = 0.0
          for k in range(0,d):
            
            k_m = d*k + m
            n_k = d*n + k
            if k <= m:
              lambda_k_m = lambda_start + (d)*k + m - ((k+1)*k)/2 # counts upper triangular, off-diagonal
            else:
              lambda_k_m = lambda_start + (d)*m + k - ((m+1)*m)/2
            #lambda_k_m = lambda_start + (d)*k + m - (k+1)*k/2
            #print "k_m:", k_m, " n_k:", n_k, " lambda_k_m:", lambda_k_m
            #print "m:", m, " k:", k, " lambda_k_m:", lambda_k_m
            #lambda_m_m = lambda_start + d*m
            if k == m:
              sum_over_k += 2 * x[lambda_k_m]*x[n_k]
            else:
              sum_over_k += x[lambda_k_m]*x[n_k]
            
          F[n_m] = -2*x[n_m]**-3 + sum_over_k
          f += x[n_m]**-2
      print "step:", num_iter, "f:", f
      # calculate the function values for the multipliers Lambda
      for k in range(d):
        for m in range(0,d):
          if k <= m:
            lambda_k_m = lambda_start + (d)*k + m - (k+1)*k/2 # counts upper triangular, off-diagonal
          else:
            lambda_k_m = lambda_start + (d)*m + k - (m+1)*m/2 
          #print "lambda_k_m:", lambda_k_m
          sum_over_n = 0.0
          for n in range(d):
            n_k = d*n + k
            n_m = d*n + m
            sum_over_n += x[n_k] * x[n_m]
          if k==m:
            sum_over_n -= 1.0
          F[lambda_k_m] = sum_over_n
    
      F_true[0,0] = -2*x[0]**-3 + 2*x[9]* x[0] + x[10]*x[1] + x[11]*x[2]
      F_true[1,0] = -2*x[1]**-3 + x[10]*x[0] + 2*x[12]*x[1] + x[13]*x[2]
      F_true[2,0] = -2*x[2]**-3 + x[11]*x[0] + x[13]*x[1] + 2*x[14]*x[2]
      F_true[3,0] = -2*x[3]**-3 + 2*x[9]* x[3] + x[10]*x[4] + x[11]*x[5]
      F_true[4,0] = -2*x[4]**-3 + x[10]*x[3] + 2*x[12]*x[4] + x[13]*x[5]
      F_true[5,0] = -2*x[5]**-3 + x[11]*x[3] + x[13]*x[4] + 2*x[14]*x[5]
      F_true[6,0] = -2*x[6]**-3 + 2*x[9]* x[6] + x[10]*x[7] + x[11]*x[8]
      F_true[7,0] = -2*x[7]**-3 + x[10]*x[6] + 2*x[12]*x[7] + x[13]*x[8]
      F_true[8,0] = -2*x[8]**-3 + x[11]*x[6] + x[13]*x[7] + 2*x[14]*x[8]
      F_true[9,0] = x[0]**2 + x[3]**2 + x[6]**2 - 1
      F_true[10,0] = x[0]*x[1] + x[3]*x[4] + x[6]*x[7]
      F_true[11,0] = x[0]*x[2] + x[3]*x[5] + x[6]*x[8]
      F_true[12,0] = x[1]**2 + x[4]**2 + x[7]**2 - 1
      F_true[13,0] = x[1]*x[2] + x[4]*x[5] + x[7]*x[8]
      F_true[14,0] = x[2]**2 + x[5]**2 + x[8]**2 - 1
    
      #print "F_true:", F_true
      #print "F:", F
      #break
      #print "x:", x
      J = np.matrix(np.zeros((num_eqs,num_eqs))) # zero the Jacobian
      # calculate Jacobian
      for n in range(d):
        for m in range(d):
          n_m = d*n + m
          lambda_m_m = lambda_start + (d)*m + m - (m+1)*m/2
          #print "lambda_m_m:", lambda_m_m
          J[n_m,n_m] = 6*x[n_m]**-4 + 2*x[lambda_m_m]
          for k in range(0,d):
            if k == m: continue # skip whenever k equals m
            n_k = d*n + k
            if k <= m:
              lambda_k_m = lambda_start + (d)*k + m - (k+1)*k/2
            else:
              lambda_k_m = lambda_start + (d)*m + k - (m+1)*m/2
            #print "lambda_k_m:", lambda_k_m
            J[n_m,n_k] = x[lambda_k_m]
            J[n_k,n_m] = x[lambda_k_m]
            J[n_m,lambda_k_m] = x[n_k]
            J[lambda_k_m, n_m] = x[n_k]
            J[n_k,lambda_k_m] = x[n_m]
            J[lambda_k_m, n_k] = x[n_m]
          J[n_m,lambda_m_m] = 2*x[n_m]
          J[lambda_m_m, n_m] = 2*x[n_m]
      '''
      print "J:", J
      J[0,0] = 6*x[0]**-4 + 2*x[9] ; J[0,1] = x[10]; J[0,2] = x[11]; J[0,9] = 2*x[0]; J[0,10] = x[1]; J[0,11] = x[2];
      J[1,1] = 6*x[1]**-4 + 2*x[12]; J[1,0] = x[10]; J[1,2] = x[13]; J[1,10] = x[0]; J[1,12] = 2*x[1]; J[1,13] = x[2];
      J[2,2] = 6*x[2]**-4 + 2*x[14]; J[2,0] = x[11]; J[2,1] = x[13]; J[2,11] = x[0]; J[2,13] = x[1]; J[2,14] = 2*x[2];
      J[3,3] = 6*x[3]**-4 + 2*x[9] ; J[3,4] = x[10]; J[3,5] = x[11]; J[3,9] = 2*x[3]; J[3,10] = x[4]; J[3,11] = x[5];
      J[4,4] = 6*x[4]**-4 + 2*x[12]; J[4,3] = x[10]; J[4,5] = x[13]; J[4,10] = x[3]; J[4,12] = 2*x[4]; J[4,13] = x[5];
      J[5,5] = 6*x[5]**-4 + 2*x[14]; J[5,3] = x[11]; J[5,4] = x[13]; J[5,11] = x[3]; J[5,13] = x[4]; J[5,14] = 2*x[5];
      J[6,6] = 6*x[6]**-4 + 2*x[9] ; J[6,7] = x[10]; J[6,8] = x[11]; J[6,9] = 2*x[6]; J[6,10] = x[7]; J[6,11] = x[8];
      J[7,7] = 6*x[7]**-4 + 2*x[12]; J[7,6] = x[10]; J[7,8] = x[13]; J[7,10] = x[6]; J[7,12] = 2*x[7]; J[7,13] = x[8];
      J[8,8] = 6*x[8]**-4 + 2*x[14]; J[8,6] = x[11]; J[8,7] = x[13]; J[8,11] = x[6]; J[8,13] = x[7]; J[8,14] = 2*x[8];
      J[9,0] = 2*x[0]; J[9,3] = 2*x[3]; J[9,6] = 2*x[6]
      J[10,0]= x[1];   J[10,1]= x[0];   J[10,3]= x[4];  J[10,4]=x[3];  J[10,6]=x[7]; J[10,7]=x[6]
      J[11,0]= x[2];   J[11,2]= x[0];   J[11,3]= x[5];  J[11,5]=x[3];  J[11,6]=x[8]; J[11,8]=x[6]
      J[12,1] =2*x[1]; J[12,4] = 2*x[4]; J[12,7] = 2*x[7]
      J[13,1]= x[2];   J[13,2]= x[1];   J[13,4]= x[5];  J[13,5]=x[4];  J[13,7]=x[8]; J[13,8]=x[7]
      J[14,2] =2*x[2]; J[14,5] = 2*x[5]; J[14,8] = 2*x[8]
      '''
      
      
      #print "J_true:", J
      #break
      y = np.linalg.solve(J, -F)
      x = x+y
      if np.linalg.norm(y) < TOL: break
    
    print "Finished.\n\n"
    print "x:", x
    
    M = np.matrix(np.zeros((d,d)))
    for n in range(d):
      for m in range(d):
        n_m = n*d + m
        M[n,m] = x[n_m]
    
    print "rotation matrix:"
    print M
    
    

`
