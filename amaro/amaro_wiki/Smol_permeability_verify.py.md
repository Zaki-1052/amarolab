# Smol permeability verify.py

`
    
    
    
    # Lane Votapka
    '''
    validates the 1D permeability calculation
    '''
    import math
    from math import pi, exp, log, sqrt
    import numpy as np
    kB = 1.3806488e-23 #m^2 * kg * s^-2 * K^-1
    T = 300.0
    #eta = 0.0535 # amu / A * fs #
    #eta = 8.9e-4 # N * m^-2 * s = kg / m * s = J * m^-3 * s
    eta = 9.998e-4 # gary's viscosity
    Ca_radius = 5.5e-10 #1.183e-10 # m #1.183 #
    #O_radius = 1.8675e-10
    #prot_radius = 15.4491
    permittivity_vacuum = 8.854e-12 # C^2 * N^-1 m^-2#0.572779 #8.854e-12 # C^2 * N^-1 m^-2
    dielectric = 92.0
    proton_charge = 1.6021e-19 # C
    q1 = -1.0 * proton_charge # charge of sphere
    q2 = 1.0 * proton_charge # charge of calcium
    avo = 6.022e23
    liter_per_m2 = 1000.0
    monovalent_conc = 0.0 # mol/liter
    debye_length = 9e99 #7.0e-10
    D_Ca = kB*T/(6 * pi * eta * Ca_radius)
    D_Na = 1.33e-9 # experimentally measured in m^2 / s
    Na_radius = kB*T/(6 * pi * eta * D_Na)
    D = 1.0
    
    #print "Na_radius:", Na_radius, "m^2/s"
    
    def pmf(z, domain = [10.0,20.0]): # gives a PMF value for location z
      if z > domain[0] and z < domain[1]:
        result = (-(z-10)**2 + 10*(z-10))/23.0e20# parabolic PMF
        #print "result:", result
      else:
        result = 0.0
      return result
    
    def smol_eq(z):
      pmf_z = float(pmf(z))
      #print "pmf_z:", pmf_z
      try:
        smol = exp(pmf_z / (kB * T))
      except OverflowError:
        print "overflow: pmf_z:", pmf_z / (kB * T)
        return 0.0
      #print "smol:", smol
      return smol
    
    
    def simpsons_rule(f, a, b, n, const=None):
      h = (b-a)/n
      if const:
        XI0 = f(a, const) + f(b, const)
      else:
        XI0 = f(a) + f(b)
      XI1 = 0
      XI2 = 0
      for i in range(n):
        X = a + i*h
        if i%2 == 0:
          if const:
            XI2 = XI2 + f(X, const)
          else:
            XI2 = XI2 + f(X)
        else:
          if const:
            XI1 = XI1 + f(X, const)
          else:
            XI1 = XI1 + f(X)
        #print "x:", X, " f(x):", smol_eq(X)
      XI = h * (XI0 + 2.0*XI2 + 4.0*XI1)/3.0
      return XI
    
    
    a = 20.0
    b = 10.0
    q = 5.0
    # analytic result
    
    analytic_permeability = (simpsons_rule(smol_eq, 0.0, a, 1000000) / D)**-1
    print "analytic permeability:", analytic_permeability
    
    integral_b_to_a = simpsons_rule(smol_eq, b, a, 1000000)
    print "integral_b_to_a:", integral_b_to_a
    integral_b_to_q = simpsons_rule(smol_eq, b, q, 1000000)
    print "integral_b_to_q:", integral_b_to_q
    
    flux_a = smol_eq(a) / integral_b_to_a
    flux_q = -smol_eq(q) / integral_b_to_q
    print "flux_a:", flux_a
    print "flux_q:", flux_q
    beta = flux_a / (flux_a + flux_q)
    print "beta:", beta
    
    calc_permeability = D * beta / (b - (1-beta)*q)
    print "calculated Permeability:", calc_permeability
    print "difference:", analytic_permeability - calc_permeability
    
    

`
