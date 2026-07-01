# script for messing with the symbolic python utility

from sympy import *
from sympy.integrals.quadrature import gauss_legendre

#k=1.3806488e-23 # boltzmann's const.
#T=300

dih = symbols('dih')
k, T , beta = symbols ('k T beta')
S, E, A, P = symbols('S E A P')

k=1.3806488e-23 # boltzmann's const.
T=300

# the entropy formula
beta = (1/(k*T))
E = cos(dih)
denom = Integral(exp(-E*beta), (dih, 0, 1.5*pi))
denom_n = denom.as_sum(4, method='midpoint')
print "denom_n", denom_n
P = exp(-E*beta)/ denom_n.n()
print "P =", P

S = k * integrate(P * log(P), P)
