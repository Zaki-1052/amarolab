#!/usr/bin/python

'''
a 1-D solver for the Poisson-Boltzmann equation
'''

import numpy as np
from numpy import matrix, arange
from numpy.linalg import inv

# PB Equation:
#  d( epsilon d( phi )) = rho
# or in alternative notation:
#  -(au')' = f
# where a is the dielectric constant and f is the charge distribution

# the variational formulation of this equ.:
#  a(u, phi) = (f,phi)
# where:
#  a(v,w) = integral_gamma (av'w' + cvw)dx and (f,v) = integral_gamma fv dx

'''def discreet_variational_right(gamma, f, v): # gamma, f, and v must be equal
  for i in len(gamma): # for every member of gamma
    f[i] * v[i]'''

# we introduce a partition of gamma
M = 100 # fineness of our grid
h = 1.0/M # space between data
#gamma = range(0,1+h,h) # if we want a uniform grid

gamma = arange(0, M+h, h)
epsilon = [1.0] * (M+1)

#Goal: to get stiffness matrix A, and load vector b to solve

b = [[0.0]*(M/2) + [1.0] + [0.0]*(M/2)] # integral under dirac delta function
# if b = (f,phi) analytically, then
# bi = sum(j) f(i) * PHI(i)
# which in the case of a dirac delta function, will simplify to the integral of
#  the dirac function itself, which in my simplified case, is equal to
#  the atomic charge
# sum (1 to M) Uj * a(PHIj, PHIi) = (f, PHIi), for i = 1 to M-1
# need to make A using hat functions
#  which is made up of aij = a(PHIj, PHIi)
# when PHIi and PHIj equal each other, then we have
#  integral_gamma (a PHIi'PHIj' + 0*PHIi*PHIj)
# I need to find integral_gamma (a*PHIi'*PHIj')
# At PHIi' = 0; for x < i-h1
#          = 1/h1; for i-h1 < x < i
#          =-1/h2; for i < x < i+h2
#          = 0; for x > i+h2
# if i == j,
#  PHIi'PHIj' = 0; for x < i-h1
#             = 1/(h1**2); for i-h1 < x < i
#             = 1/(h2**2); for i < x < i+h2
#             = 0; for x > i+h2
#  so integral_gamma (a*PHIi'*PHIj') = (1/(h1**2) * h1) + (1/(h2**2) * h2)
#   = a(1/h1 + 1/h2)
# if i = j-1:
#  int PHIi'PHIj' = 0; for x < i
#                 = -1/h1; for i < x < j, because the triangle in between
#                 = 0; for x > j
#  so the integral is -a/h1

# get stiffness matrix
A = []
for i in range(M+1):
  row = []
  for j in range(M+1):
    if i == 0:
      invh1 = gamma[i+1] - gamma[i]
    else:
      invh1 = gamma[i] - gamma[i-1]
    if i == M:
      invh2 = gamma[i] - gamma[i-1]
    else:
      invh2 = gamma[i+1] - gamma[i]
    if j == i:
      area = epsilon[i] * (invh1 + invh2) # find area under superimposed hat
    elif (i == j-1):
      area = -epsilon[i] * invh2
    elif (i == j+1):
      area = -epsilon[i] * invh1
    else:
      area = 0.0
    row.append(area)
  A.append(row)

A = matrix(A)
print A
b = matrix(b).T
Ainv = inv(A)
