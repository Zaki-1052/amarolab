# Chemistry.py

`
    
    
    
    # chemistry functions
    
    import math
    
    def quad(a,b,c):
      '''quadratic formula'''
      assert b*b -4*a*c > 0, "no roots can be found "
      n1 = math.sqrt(b*b -4*a*c)
      ans1 = (-b + n1) / (2*a)
      ans2 = (-b - n1) / (2*a)
      return ans1, ans2
    
    def get_Im(ionlist):
      '''Calculates the ionic strength (Im) for a Debye Huckel solvation theory calculation '''
      ans = 0.0
      for ion in ionlist:
        charge = ion[0]
        molality = ion[1]
        ans += charge*charge*molality
      return 0.5 * ans
      #return 0.2
    
    def get_gamma(zplus, zminus, mplus, mminus):
      ''' find an activity coefficient for the solution '''
      ionlist = [(zplus, mplus),(zminus,mminus)]
      Im = get_Im(ionlist)
      print "Im", Im
      log10gamma = -0.51 * zplus * abs(zminus) * (( math.sqrt(Im) / (1+math.sqrt(Im))) - 0.30*(Im))
      gamma = 10 ** log10gamma
      return gamma
    
    def acid_iterate(Ka, m0, Error=0.0001):
      ''' an iterative solution for finding the activity coefficient (gamma) of a solution '''
      gamma = 1.0
      for i in range(100):
        a = 1
        b = Ka / (gamma*gamma)
        c = - b * m0
        root = quad(a,b,c)[0] # get the positive root
        print "gamma = %f, m(H+) = %f" % (gamma,root)
        newgamma = get_gamma(1,-1,root,root)
        if abs(newgamma - gamma) < Error:
          break
        gamma = newgamma
    
    

`
