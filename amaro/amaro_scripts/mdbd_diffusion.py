# this script takes arguments D (diffusion coefficient), and tmin (minimum time allowed) and finds the optimal grid size

from sympy import symbols, exp, pi, diff


'''
def func():
  return diff(F,x)

def funcprime():
  return diff(diff(F,x),x)
'''
arg_D = 0.065
arg_tmin = 1.0


F,dF,ddF,x,tmin,D,p = symbols('F,dF,ddF,x,tmin,D,p')
newtonF, newtondF = symbols('newtonF,newtondF')


F = x**2/(6*D) * (1/(1-exp(-x**2/(4*D*tmin))))
dF = diff(F,x)
ddF = diff(dF,x)
  
print "dF:",dF
print "ddF:",ddF

guess = 1.0
tol = 0.00001
diff = 9999999999.9
root = 0.0


while diff > tol:
  newtonF = dF.xreplace({x:guess, D:arg_D, tmin:arg_tmin})
  newtondF = ddF.xreplace({x:guess, D:arg_D, tmin:arg_tmin})
  root = guess - (newtonF / newtondF)
  diff = abs(guess - root)
  print "F:", newtonF, "dF:",newtondF,"root:",root,"diff:",diff
  guess = root


print "root:",root
