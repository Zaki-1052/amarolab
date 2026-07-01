# for calculating the diffusion coefficient of Ca++

import math
from math import pi, exp, log, sqrt
import numpy as np

#kB = 8.3144621454689521e-07 # Boltzmann's const in A^2 * amu / fs^2 * K
kB = 1.3806488e-23 #m^2 * kg * s^-2 * K^-1
T = 298
#eta = 0.0535 # amu / A * fs #
eta = 8.9e-4 # N * m^-2 * s = kg / m * s = J * m^-3 * s
#eta = 9.998e-4 # gary's viscosity kg / m * s
Ca_radius = 3.5e-10 #1.183e-10 # m #1.183 #
#O_radius = 1.8675e-10
#prot_radius = 15.4491
permittivity_vacuum = 8.854e-12 # C^2 * N^-1 m^-2#0.572779 #8.854e-12 # C^2 * N^-1 m^-2
dielectric = 78
proton_charge = 1.6021e-19 # C
q1 = -0.0 * proton_charge
q2 = 2.0 * proton_charge
avo = 6.022e23
liter_per_m2 = 1000
monovalent_conc = 0.0 # mol/liter
debye_length = 9e99 #7.0e-10
#kappa = sqrt((2.0* (monovalent_conc * (proton_charge)**2.0)) * 4.0 * pi / (kB * T * dielectric * permittivity_vacuum))
rxn = 6.0e-10
b_surf = 10.0e-10
q_surf = 11.0e-10
# 6349.0/10000.0
'''
K = np.matrix([[0, 1, 0],[(3651.0/10000.0), 0, 6349.0/10000.0],[0, 1, 0]])
p = np.matrix([[0, 1, 0]])

pi = p
for i in range(10):
  qi = pi * K**i
  print "q%d:"%i,qi


print "K:", K
print "eigs:", np.linalg.eig(K)


I_K = np.identity(3) - K
#print "I_K:", I_K
#I_K_inv = np.identity(3) - K.T
#I_K_inv = np.matrix(np.linalg.inv(I_K.T))
#q = np.linalg.solve(I_K, np.zeros(3))
#print "q:", q

t = np.matrix([[0, 516.191, 0]])
p = np.matrix([[0, 1, 0]])
#tau = np.linalg.solve(I_K, t.T)
tau = p * I_K_inv * t.T

#print "t:", t
#print "p:", p
#print "tau:", tau


'''


permit_ps_A = permittivity_vacuum * kB*T / (1e10*proton_charge**2)
print "permittivity in ps, A, kT:", permit_ps_A
visc_ps_A = eta * 1e12/ (kB * T * 1e30)
print "viscosity in ps, A:", visc_ps_A
garys_visc = 0.243 * kB * T * 1e30 / 1e12
print "Gary's viscosity in N * m-2 * s:", garys_visc



def coulombs(r, debye_len=9e99):
  ''' returns answer in joules '''
  #print "COULOMBS: q1:", q1, "q2:", q2, "pi:", pi, "permittivity_vacuum:", permittivity_vacuum, "dielectric:", dielectric
  pot_const = q1 * q2 * exp(-r/debye_len) / (4.0 * pi * permittivity_vacuum * dielectric)
  #print "pot*r", pot_const
  pot = pot_const / r
  return pot

def smol_eq(r):
  #print "SMOL EQ: q1:", q1, "q2:", q2, "pi:", pi, "permittivity_vacuum:", permittivity_vacuum, "dielectric:", dielectric
  #const =  q1 * q2 / (4.0 * pi * permittivity_vacuum * dielectric * kB * T)
  #print "const:", const, " r:", r
  #smol = exp(const * exp(-r/debye_length) / r) / (r*r)
  #print "smol1:", smol
  smol = exp(coulombs(r, debye_length) / (kB * T)) / (r*r)
  #print "smol2:", smol
  return smol


def mfpt_eq(r, const):
  ''' the mean-first-passage-time integral'''
  mfpt_inner_integral = simpsons_rule(smol_eq, const, r, 2000)
  return r*r*exp(-coulombs(r) / (kB * T)) * mfpt_inner_integral

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

def romberg(MAX=100):
  s = [1]*(MAX-1) # generate a list of length MAX
  for k in range(1,MAX):
    for i in range(1,k):
      if i == 1:
        pass

def density_func(r, base):
  return r*r*exp(-coulombs(r) / (kB*T)) * simpsons_rule(smol_eq, base, r, 2000)

D_Ca = kB*T/(6 * pi * eta * Ca_radius)
#D_prot = kB*T/(4 * pi * eta * prot_radius)
#print "D_Ca:", D_Ca, "m^2 / s"
D_Ca = 6.73e-10 # m^2/s
D_O2minus = 1.5e-9 # m^2/s
hydro_rad = kB*298/(6 * pi * garys_visc * D_O2minus)
print "hydro_rad:", hydro_rad
raise "DIE!!"

#print "D_prot:", D_prot, "m^2 / s"
#print "D_Ca:", D_Ca / 10e-8, "10-4 cm^2 / s"
#D_Ca += D_prot
#D_Ca = 6.73e-10
#Ca_radius = kB*T/(D_Ca * 4.0 * pi * eta)
#print "Ca_radius:" , Ca_radius
#integral = simpsons_rule(smol_eq, 6.0e-10, 1.0e-6, 20000000)
#print "integral",integral
#print "k(b)numerical integral: %3.2e" % (4.0*pi*D_Ca*avo*liter_per_m2/integral)

k_on_chg = {}
k_on_unchg = {}
#b = 1e-9
for b in [rxn, b_surf, q_surf, 54.35e-10]:
  k_on_unchg[b] = 4.0 * pi * D_Ca * b * avo * liter_per_m2
  print "uncharged K_on at radius %3.2em: %6.4e M^-1 * s^-1" % (b, (k_on_unchg[b]))

B_unchg = 0.130
B_inf_unchg = B_unchg / (1.0 - (1.0 - B_unchg)*(k_on_unchg[b_surf]/k_on_unchg[q_surf]))
print "B_inf uncharged:", B_inf_unchg

for b in [rxn, b_surf, q_surf, 54.35e-10]:
  if q1 == 0 or q2 == 0:
    k_on_chg[b] = 4.0 * pi * D_Ca * b
  else:
    k_on_chg[b] = - D_Ca / ((1 - exp(q1*q2 / (4.0*pi*permittivity_vacuum*dielectric*kB*T*b)))*(permittivity_vacuum*dielectric*kB*T / (q1*q2)))
  print "k_on for radius %3.2em: %6.4e M^-1 * s^-1" % (b, (k_on_chg[b]*avo*liter_per_m2))

#print "k_on:", k_on, "A^3/fs"
B_chg = 0.1205
B_inf_chg = B_chg / (1.0 - (1.0 - B_chg)*(k_on_chg[b_surf]/k_on_chg[q_surf]))
print "B_inf charged:", B_inf_chg

print "potential at corner:", coulombs(12.99e-10) / (kB *T / proton_charge)

print "kT/e per J/C:", 1.0 * (kB *T / proton_charge)

print "\nSphere rates\n"
#k1 = k_on_chg[11.0e-10]*avo*liter_per_m2
k1 = k_on_chg[q_surf] * avo * liter_per_m2
print "k1:%6.4e" % k1
# rate from 11A to inf

integral = simpsons_rule(smol_eq, q_surf, 1.0e-6, 20000000)
#k_1 = (4.0*pi*D_Ca*avo*exp(coulombs(11.0e-10)/(kB*T))/integral)
k_1 = (4.0*pi*D_Ca*exp(coulombs(q_surf)/(kB*T))/integral) * avo * liter_per_m2
print "k-1:%6.4e" % k_1

integral = simpsons_rule(smol_eq, b_surf, q_surf, 2000000)
#k2 = (4.0*pi*D_Ca*avo*exp(coulombs(11.0e-10)/(kB*T))/integral)
k2 = (4.0*pi*D_Ca*exp(coulombs(q_surf)/(kB*T))/integral) * avo * liter_per_m2
print "k2:%6.4e" % k2

# ideal: 29.40
k_2 = 874 #1 / (40.1209 * 1e-12)
#k_2 = 1 / (29.40 * 1e-12) # ideal situation
print "k_2:%6.4e" % k_2
integral = simpsons_rule(smol_eq, b_surf, q_surf, 2000000)
#analytic_k_2 = (4.0*pi*D_Ca*avo*exp(coulombs(10.0e-10)/(kB*T))/integral)
analytic_k_2_flux = (4.0*pi*D_Ca*exp(coulombs(b_surf)/(kB*T))/integral)* avo * liter_per_m2
print "analytic_k_2_flux: %6.4e" % analytic_k_2_flux
#print "analytic_k_2: %6.4e" % analytic_k_2
# ideal: 130.23
k3 = 126 #(1) / (104.927 * 1e-12)
#k3 = 1 / (130.23 * 1e-12) # ideally
print "k3:%6.4e" % k3
integral = simpsons_rule(smol_eq, b_surf, rxn, 2000000)
#analytic_k3 = -(4.0*pi*D_Ca*avo*exp(coulombs(10.0e-10)/(kB*T))/integral)
analytic_k3_flux = -(4.0*pi*D_Ca*exp(coulombs(b_surf)/(kB*T))/integral) * avo * liter_per_m2
print "analytic_k3_flux: %6.4e" % analytic_k3_flux


# first find the flux across the rxn_surfaces
A_one_rxn = exp(coulombs(b_surf, debye_length) / (kB * T)) / (simpsons_rule(smol_eq, rxn, b_surf, 20000))
print "A_one_rxn:", A_one_rxn
A_one_q = exp(coulombs(b_surf, debye_length) / (kB * T)) / (simpsons_rule(smol_eq, b_surf, q_surf, 20000))
print "A_one_q:", A_one_q
current_rxn = 4.0 * pi * A_one_rxn
print "current_rxn:", current_rxn
current_q = 4.0 * pi * A_one_q
print "current_q:", current_q
# then find the total concentration in the region we are talking about
num_in_rxn_b = A_one_rxn * simpsons_rule(density_func, rxn, b_surf, 2000, rxn)
print "num_in_rxn_b:", num_in_rxn_b
num_in_b_q = A_one_q * simpsons_rule(density_func, q_surf, b_surf, 2000, q_surf)
print "num_in_b_q:", num_in_b_q
num_particles = 4.0 * pi * (num_in_rxn_b + num_in_b_q)
print "num_particles:", num_particles


mfpt3 = num_particles / (D_Ca * 2.0 * current_rxn)
mfpt_2 = num_particles / (D_Ca * 2.0 * current_q)
mfpt_total = num_particles / (D_Ca * (current_rxn + current_q))
analytic_k3 = 1.0 / mfpt3
analytic_k_2 = 1.0 / mfpt_2
print "mfpt3:", mfpt3
print "mfpt_2:", mfpt_2
print "mfpt_total:", mfpt_total

time_integral_1 = simpsons_rule(mfpt_eq, rxn, b_surf, 2000, rxn)
print "time_integral_1:", time_integral_1
time_integral_2 = -simpsons_rule(mfpt_eq, b_surf, q_surf, 2000, q_surf)
print "time_integral_2:", time_integral_2
avg_time = (time_integral_1 + time_integral_2) / D_Ca
print "avg_time:", avg_time, " k3_analytic:", 1.0 / avg_time

print "analytic_k_2: %6.4e" % analytic_k_2
print "analytic_k3: %6.4e" % analytic_k3
print "ratio: ", analytic_k_2 / analytic_k3
keff = k1 * k2 * k3 / ( k2*k3 + k_2*k_1 + k3*k_1 )
keff_analytic = k1 * k2 * analytic_k3 / ( k2*analytic_k3 + analytic_k_2*k_1 + analytic_k3*k_1 )
keff_analytic_flux = k1 * k2 * analytic_k3_flux / ( k2*analytic_k3_flux + analytic_k_2_flux*k_1 + analytic_k3_flux*k_1 )
print "keff:%6.4e"% keff, "numerator:", k1 * k2 * k3, "denominator:", ( k2*k3 + k_2*k_1 + k3*k_1 )
print "keff_analytic: %6.4e" % keff_analytic, "numerator:", k1 * k2 * analytic_k3, "denominator:", ( k2*analytic_k3 + analytic_k_2*k_1 + analytic_k3*k_1 )
print "keff_analytic_flux: %6.4e" % keff_analytic_flux
