# -*- coding: utf-8 -*-
# myownBD.py
# By Lane Votapka
# Amaro lab 2014

'''
Runs a very simple BD simulation of a diffusing particle in an unforced sphere


'''
import random
from numpy import sqrt, pi
import numpy
import sys

forces = int(sys.argv[1])

startx = 10.0 # e-10
starty = 0.0 # particle starting position
startz = 0.0

D = 1.33e-1 # A**2/ps #1.33e-9 # m**2/s # diffusion coefficient
kB_metric = 1.3806488e-23 # m^2 * kg * s^-2 * K^-1
kB_factor = 1e20 * 6.022e26 * 1e-24 # A^2 per m^2 * amu per kg * s^2 per ps^2
#otherkB = kB_metric * kB_factor
#print "otherkB:", otherkB
kB = 8.3144621454689521e-01; # Boltzmann's const in A^2 * amu / ps^2 * K
T = 300.0

dt = 0.01 #ps #e-12 # timestep size

a = 6.0 # A #e-10 # inner ending radius
b = 10.0
q = 11.0 # A #e-10 # outer ending radius

ntrajs = 1000000 # total number of trajectories
max_steps = 10000000
permittivity_metric = 8.8541878e-12 # the permittivity in metric units (C^2 * m^-2 * N^-1) = C^2 * m^-3 * kg^-1 * s^2, to be converted to custom units
permittivity_factor = (6.241e18)**2 * 1e-30 * 1e24 / (6.022e26)   # electrons per C ^ 2 * meters per A * (ps per s)**2 / amu per kg

permittivity = permittivity_metric * permittivity_factor # permittivity of a vacuum
dielectric = 92.0
print "permittivity:", permittivity
coulombs_const = 1 / (4.0 * pi * permittivity * dielectric) # get coulombs constant
coulombs_const_metric = 8.987551e9 # N * m^2 * C^-2 = kg * m^3 * s^-2 * C^-2
coulombs_factor = 6.022e26 * 1e30 / (1e24 * (6.241e18)**2)
coulombs_const_other = coulombs_const_metric * coulombs_factor
print "coulombs_const:", coulombs_const
print "coulombs_const_other:", coulombs_const_other

#forces = 0 # 0 = off, 1 = coulombic
#exit()
def coulombic_force(rx, ry, rz, q1=1.0, q2=-1.0): # returns
  r_dist_2_inv = 1 / (rx*rx + ry*ry + rz*rz) # inverted squared distance between particles
  r_dist_inv = sqrt(r_dist_2_inv) # get the inverted distance
  r_hat_x = rx * r_dist_inv
  r_hat_y = ry * r_dist_inv # using an inverted distance allows us to save on computation
  r_hat_z = rz * r_dist_inv
  force_mag = coulombs_const * q1 * q2 * r_dist_2_inv
  #print "force_mag:", force_mag
  return r_hat_x * force_mag, r_hat_y * force_mag, r_hat_z * force_mag

n_a = 0
n_q = 0
total_time = 0.0
mu = 0.0
sigma = sqrt(2.0 * D * dt)
total_j = 0

#print "coulombs:", coulombic_force(startx, starty, startz)
for i in range(ntrajs): # run all trajectories
  rx = startx
  ry = starty
  rz = startz
  t = 0.0
  j = 0
  stopping = False
  while j < max_steps: # take a bunch of timesteps
    if forces == 1:
      fx, fy, fz = coulombic_force( rx, ry, rz)
    else:
      fx, fy, fz = 0.0, 0.0, 0.0 # no forces
    
    # find the change in position
    #print "fx:", fx, "fy:", fy, "fz:", fz
    #print "t*D*fx/(kB*T):", t*D*fx/(kB*T)
    #print "sigma:", sigma
    drx = dt*D*fx/(kB*T) + numpy.random.normal(mu, sigma)
    dry = dt*D*fy/(kB*T) + numpy.random.normal(mu, sigma) # find change in position
    drz = dt*D*fz/(kB*T) + numpy.random.normal(mu, sigma)
    
    rx += drx
    ry += dry # change the position
    rz += drz
    t += dt
    # check the particle's position for a reaction
    if rx*rx+ry*ry+rz*rz <= a*a: # then there is an interior reaction
      n_a += 1
      stopping = True
    elif rx*rx+ry*ry+rz*rz >= q*q:
      n_q += 1
      stopping = True

    if stopping:
      total_time += t
      total_j += j
      break
    
    j += 1 # in case the particle gets stuck

n = (float(n_a)+float(n_q))
beta = float(n_a) / n
avg_time = total_time / n

print "n_a:", n_a
print "n_q:", n_q
print "n:", n
print "beta:", beta
#print "expected beta:", -a*(q-b) / (q*(a-b) - a*(q-b))
print "avg_time:", avg_time
#print "expected_time:", (b-a)*(q-b)/(2.0*D) # 1D
#print "expected_time:", (-b**3 - a*q*(a+q) + b*(a*a + a*q + q*q)) / (6.0*D*b)
print "avg_j:", total_j / n


'''
n = 100000000

testgauss = 0.0
for i in range(n):
  testgauss += random.gauss(0.0,1.0)

print "random.gauss:", testgauss

testgauss = 0.0
for i in range(n):
  testgauss += random.normalvariate(0.0,1.0)

print "random.normalvariate:", testgauss

testgauss = 0.0
for i in range(n):
  testgauss += numpy.random.gauss(0.0,1.0)

print "numpy.random.gauss:", testgauss

testgauss = 0.0
for i in range(n):
  testgauss += numpy.random.normal(0.0,1.0)

print "numpy.random.normal:", testgauss
'''
