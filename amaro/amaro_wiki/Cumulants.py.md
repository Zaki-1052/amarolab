# Cumulants.py

`
    
    
    
    # cumulants
    import random
    from math import exp
    
    
    n = 1000000
    cumulant = 0.0
    u = 1.0
    num_moments = 4
    moments = []
    for i in range(num_moments):
      moments.append(0.0)
      
    for i in range(n):
      xsi = int(random.random()*2)
      #print "xsi:", xsi
      #cumulant += exp( # involves imaginary numbers :/
      for f in range(num_moments):
        moments[f] += xsi**(f+1)
    
    
    for i in range(num_moments):
      moments[i] = moments[i]/n
    
    print "moments:", moments
    
    

`
