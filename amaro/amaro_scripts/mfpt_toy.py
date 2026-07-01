# mean passage time calc

from math import sqrt, pi
a = 6.0e-10
b = 10.0e-10
q = 11.0e-10

D = 3.99601886184e-10 #m^2 / s
D2 = D * 3.299
print "D:", D
print "D2:", D2

def conc_eq(r, const):
  ''' the mean-first-passage-time integral'''
  
  return 4.0 * pi * r**2 * ((1-const/r)*b/(b-const))

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


number1 = -4.0 * pi * (b/(b-a))*((-b**3/3.0) + (a*b**2/2.0) - (a**3/6.0))
print "number1:", number1
number2 = 4.0 * pi * (b/(b-q))*((-b**3/3.0) + (q*b**2/2.0) - (q**3/6.0))
print "number2:", number2
number = number1 + number2
print "number: ", number
number_numerical_a_to_b = simpsons_rule(conc_eq, a, b, 2000, a)
print "number_numerical_a_to_b: ", number_numerical_a_to_b
number_numerical_b_to_q = simpsons_rule(conc_eq, b, q, 2000, q)
print "number_numerical_b_to_q: ", number_numerical_b_to_q
number_numerical = number_numerical_a_to_b + number_numerical_b_to_q
print "number_numerical: ", number_numerical
flux_q = 4.0 * pi * D2 * b*q/(q-b)
print "flux_q: ", flux_q
flux_a = 4.0 * pi * D2 * b*a/(b-a)
print "flux_a: ", flux_a
total_flux = flux_a + flux_q
print "total_flux:", total_flux
beta = flux_a / total_flux
print "beta:", beta
total_time = number_numerical / total_flux
print "total_time:", total_time
time_q = number / flux_q
print "time_q:", time_q
time_a = number / flux_a
print "time_a:", time_a
