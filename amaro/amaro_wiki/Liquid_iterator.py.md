# Liquid iterator.py

`
    
    
    
    # by Lane Votapka
    # Amarolab 2015
    
    '''
    This is an experimental program that will attempt to create a density distribution
    of a number of atoms with additive potential energies.
    
    For this first implementation, it is one-dimensional with only one type of atom
    
    rho = exp(-U(x)/kB*T)
    
    '''
    
    import numpy as np
    from math import exp, log, sin, cos
    import matplotlib.pyplot as plt
    from matplotlib import cm
    import mpl_toolkits.mplot3d.axes3d as p3
    import matplotlib.animation as animation
    
    h = 0.1 # resolution of the spacial grid
    N = 100 # total number of data points
    max_x = N * h
    U = np.zeros(N) # the potential energy grid
    U_orig = np.zeros(N)
    rho = np.zeros(N) # the density grid
    kB = 1.3806488e-23 #m^2 * kg * s^-2 * K^-1
    T = 300.0
    kT = 1.0 #kB * T
    x_list = np.arange(0,max_x, h)
    charge = 1.0
    radius = 1.5
    num_iter = 1
    
    #N = 10 # the number of particles to attempt to add
    
    def normalize(dist, dx): # normalize a distribution
      num = dist.shape[0]
      normdist = np.zeros(dist.shape) # create our normalized distribution
      total_area = 0.0
      for j in range(num-1): # get the total area underneath
        area = dx * 0.5 * (dist[j] + dist[j+1])
        total_area += area
    
      for j in range(num): # normalize
        normdist[j] = dist[j] / total_area
      return normdist
    
    def pot_energy(x1, x2, q1=1.0, q2=1.0, radius=0.5, epsilon=0.0000001):
      # returns the potential energy function of two particles
      if abs(x1-x2) < radius:
        return 9e99
      else:
        return q1 * q2 * epsilon / abs(x1-x2)
    
    # place the first particle
    for j in range(N):
      x = j*h
      if x > radius: # if we are outside the range of the coulombic particle
        rho[j] = 1.0 # integrate and normalize
        U_orig[j] = -1.0 / x
      else:
        rho[j] = 0.0
        U_orig[j] = 9e99
    
    rho = normalize(rho, h)
    #U = normalize(U,h)
    rhos = [rho]
    for iteration in range(num_iter):
      # now find the potential given rho
      rho_new = np.zeros(rho.shape) # the exponents of a new rho
      new_U = np.zeros(U.shape)
      for j in range(N):
        
        for k in range(N): # variable over which we are integrating
          #print "U_orig[j]:", U_orig[j]
          #print "rho[k]*pot_energy(j*h, k*h):", rho[k]*pot_energy(j*h, k*h)
          total_U_k = U_orig[j] + rho[k]*pot_energy(j*h, k*h)
          #print "total_U_k:", total_U_k
          #print "rho[k]:", rho[k]
          #print "exp(-total_U_k / kT):", exp(-total_U_k / kT)
          #rho_new[j] += rho[k] * exp(-total_U_k / kT)
          rho_new[j] += exp(-total_U_k / kT)
          #print "rho_new[j];", rho_new[j]
          new_U[j] += rho[k]*pot_energy(j*h, k*h)
      
        #print "new_U[j]:", new_U[j]
        #print "rho_new[j]:", rho_new[j]
        
      rho = normalize(rho_new,h)
      #rho = rho+rho_new
      rhos.append(rho)
    
    # plot
    # plot the starting figure
    fig1 = plt.figure()
    ax = plt.axes(xlim=(0,max_x),ylim=(-1.0,1.0))
    line, = ax.plot([],[],lw=2)
    
    plt.xlabel('x')
    plt.ylabel('vals')
    plt.title("liquid iterator")
    plt.plot(x_list, U_orig, 'r', x_list, rhos[0], 'g', x_list, rhos[1], 'b', x_list, new_U, 'c')
    plt.show()
    
    
    #for i in range(N):
    for i in range(N): # for each position in space
      pass
    
      
      # find the probability that B is in location y P(B=y) = rho[y]
      
      # prob that we put a particle A at x given that B is at y P(A=x|B=y) = exp(-U(x,y)/(kB*T))
      
      # prob that we put a particle A at x and there is a particle B at y P(A=x,B=y) or P(A=x,B=y) = P(A|B) * P(B) = exp(-U(x,y)/(kB*T)) * rho[y]
      
      # the probability that we put a particle A at x: P(A=x) = sum over y: P(A=x,B=y)
    
      # P(A) = sum over y: exp(-U(x,y)/(kB*T)) * rho[y]
    
      # PB eq: div( diel * grad(psi(x))) = charge_density(x) = exp(-psi(x)/kB*T)
    
      # - or -
    
      # rho[x] = exp(-U(rho[x])/kT)
    
      
      # we want the probability P that we will put our new particle there
      # P = exp(-U/(kB*T))
      
    
    

`
