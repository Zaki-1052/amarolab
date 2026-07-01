# Schrodinger 3d.py

`
    
    
    
    # Time-dependent Schrodinger equation solver
    # By Lane Votapka
    
    import sys, os
    import numpy as np
    from scipy.sparse.linalg import eigsh
    from numpy import matrix
    from math import exp, pi, sqrt
    import math
    #import matplotlib.pyplot as plt
    #from matplotlib import cm
    #import mpl_toolkits.mplot3d.axes3d as p3
    #import matplotlib.animation as animation
    import dx
    import time
    #from mayavi import mlab
    
    k = 5.0
    hx = 1.0
    hy = 1.0
    hz = 1.0
    ax = -12.0
    ay = -12.0
    az = -12.0
    bx = 12.0
    by = 12.0
    bz = 12.0
    nx = int((bx-ax)/hx + 1) # number of data points in x direction
    ny = int((by-ay)/hy + 1) # number of data points in y direction
    nz = int((bz-az)/hz + 1) # number of data points in z direction
    n = nx * ny * nz
    m = 5.44e-4 #1.004 #amu
    #planks = 6.626e-34 J*s
    planks = 3.99e-5 #L*s
    h_bar = planks / (2*pi)
    imag = complex(0,1) # imaginary number
    omega = 1.0e-2
    #ulist = []
    frames = 200
    x_list = []
    phi_list = []
    phi_time = []
    V = []
    t=0
    arg_level = int(sys.argv[1])
    permittivity = 0.572779161 # permittivity of a vacuum in e^2 * fs^2 / amu * A^3
    
    
    
    def coulombic_potential(x, nuclear_chg=1.0, electron_chg=-1.0, t=0):
      r = np.linalg.norm(x) + 0.1
      return electron_chg * nuclear_chg / (4.0 * pi * permittivity * r * 100000.0)
    
    def init():
      line.set_data([],[])
      return line,
    
    def animate(i):
      #x = np.linspace(0,1,n)
      #y = np.sin(2 * np.pi * (x - 0.01 * i))
      line.set_data(x_list,phi_time[i])
      return line,
    
    
    def time_independent_3d (hx, hy, hz, V, ax, ay, az, bx, by, bz, num_evals, bordervalue = 0.0):
      # (H - E) * phi
      # first construct the kinetic energy part of the hamiltonian
      nx = int((bx-ax)/hx + 1) # number of data points in x direction
      ny = int((by-ay)/hy + 1) # number of data points in y direction
      nz = int((bz-az)/hz + 1) # number of data points in z direction
      n = nx * ny * nz
      print "n: %d, nx: %d, ny: %d, nz: %d" % (n, nx, ny, nz)
      kinetic = np.zeros((n,n))
      kinetic[0,0] = -6.0 # constructing the 2nd derivative
      #for i in range(1,n):
      #  kinetic[i,i] = -6.0
      #  kinetic[i-1,i] = 1.0
      #  kinetic[i,i-1] = 1.0
      for i in range(0,nx):
        for j in range(0,ny):
          for k in range (0,nz):
            index = k + (ny * j) + (i * nx * ny)
            index_x_minus_1 = index - (nx*ny)
            index_x_plus_1 = index + (nx*ny)
            index_y_minus_1 = index - ny
            index_y_plus_1 = index + ny
            index_z_minus_1 = index - 1
            index_z_plus_1 = index + 1
            kinetic[index,index] = -6.0
            if i > 0: kinetic[index,index_x_minus_1] = 1.0
            if i < nx-1: kinetic[index,index_x_plus_1] = 1.0
            if j > 0: kinetic[index,index_y_minus_1] = 1.0
            if j < ny-1: kinetic[index,index_y_plus_1] = 1.0
            if k > 0: kinetic[index,index_z_minus_1] = 1.0
            if k < nz-1: kinetic[index,index_z_plus_1] = 1.0
    
    
      kinetic *= -(planks**2 / (2.0*m)) # scaling the 2nd derivative
      print "kinetic:", kinetic[:3,:3]
      potential = np.zeros((n,n))
      for i in range(0,nx):
        for j in range(0,ny):
          for k in range(0,nz):
            index = k + (ny * j) + (i * nx * ny)
            x = np.array([ax + hx*i, ay + hy*j, az + hz*k])
            potential[index,index] = V(x)
      print "potential:", potential #[:3,:3]
      H = kinetic + potential
      time1 = time.time()
      #eigs = np.linalg.eigh(H)
      our_eig = np.linalg.eigh(H)
      time2 = time.time()
      #our_eig = eigsh(H, k=num_evals, which='SM', mode='cayley', sigma=-0.1)
      time3 = time.time()  
      print "eigh:", time2-time1
      print "sparse.eigh:", time3-time2
      return our_eig
    
    
    #V = square_well_potential
    #V = harmonic_potential
    V = coulombic_potential
    evals, evecs = time_independent_3d(hx, hy, hz, V, ax, ay, az, bx, by, bz, arg_level)
    
    # sorts the eigenvalues by the eigenvectors
    idx = evals.argsort()
    evals = evals[idx]
    evecs = evecs[:,idx]
    
    print "evals:", evals
    
    #print "evals:", evals
    
    for level in range(0,arg_level):
      E = evals[level]
      phi = evecs[:,level]
      phi_sq = phi*phi
      phi_sq = phi_sq / np.linalg.norm(phi_sq)
    
      #print "phi:", phi
      V_list = []
      for i in np.arange(ax,bx,hx):
        x_list.append(i)
        V_list.append(V(i))
    
      dx.make_dx("/scratch/lvotapka/projects/quantum_data/phi_sq_%d.dx" % level, phi_sq, nx, ny, nz, hx)
      dx.make_dx("/scratch/lvotapka/projects/quantum_data/phi_%d.dx" % level, phi, nx, ny, nz, hx)
      #dx.make_dx("pot.dx", V_list, nx, ny, nz, hx)
    
    '''
    # initialize the data
    for i in np.arange(a,b,h):
      if i == a or i == b:
        "i: %f, PHI: 0.0"
        PHI =0.0
      else:
        PHI = starting_phi(i)
        print "x: %f, PHI: %f" % (i, PHI*PHI)
      x_list.append(i)
      phi_list.append(PHI)
      V.append(potential(i))
    
    phi_sq = map(lambda y: abs(y)*abs(y), phi_list) # square all the absolute values
    phi_time.append(phi_sq)
    area = 0.0
    for phi_sq_i in phi_sq:
        area += phi_sq_i * h
    starting_area = area
    print "area:", area
    # advance time according to the time-dependent Schrodinger equation
    for i_t in range(frames):
      new_phi_list = []
      area = 0.0
      for i_x in range(len(x_list)):
        x = x_list[i_x]
    
        if x == a or i_x >= len(phi_list)-1:
          d_PHI = 0.0 # the derivative of PHI with respect to time
          new_phi_list.append(0.0)
        else:
          PHI = phi_list[i_x]
          d_d_PHI = (phi_list[i_x+1] - 2*phi_list[i_x] + phi_list[i_x-1]) / (h*h)
          #print "d_d_PHI: ", d_d_PHI
          d_PHI = (imag*h_bar/(2*m))*d_d_PHI - (imag/h_bar)*V[i_x]*PHI
          #print "d_PHI: ", d_PHI
          new_phi = phi_list[i_x] + (d_PHI)*k
          #print "PHI: ", PHI, "d_PHI: ", d_PHI, "d_d_PHI: ", d_d_PHI
          new_phi_list.append(phi_list[i_x] + (d_PHI)*k) # increment the value of the wavefunction linearly
    
    
      #print "area under PHI:", area
      phi_list = new_phi_list
      phi_sq = map(lambda x: abs(x)*abs(x), new_phi_list) # square all the absolute values
      for phi_sq_i in phi_sq:
        area += phi_sq_i * h
      factor = starting_area / area
      # scale by the area
      print "area step %i: %f" % (i_t,area)
      phi_time.append(phi_sq)
      t += k # advance time
    
    '''
    
    
    
    #print "len(x):", len(x_list)
    #print "len(phi_time[0]:", len(phi_time[0])
    
    #print "(imag*h_bar/2*m):", (imag*h_bar/(2*m))
    '''
    for p in phi_time[0]:
        print "phi_time[0]:", p
    
    for p in phi_time[-1]:
        print "phi_time[-1]:", p
    ''
    fig1 = plt.figure()
    ax = plt.axes(xlim=(-10,10),ylim=(-0.5,0.5))
    line, = ax.plot([],[],lw=2)
    
    plt.xlabel('x')
    plt.ylabel('PHI')
    plt.title("Time independent Schrodinger")
    plt.plot(x_list, V_list, 'r', x_list, phi, 'g', x_list, phi_sq, 'b')
    #line_ani = animation.FuncAnimation(fig1, animate, frames=frames, interval = 1, blit=True, init_func=init)
    plt.show()'''
    
    

`
