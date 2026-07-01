'''
Created on Jul 2, 2014

creates a simulation of a free particle

@author: lvotapka
'''

import sys, os
import numpy as np
from numpy import matrix
from numpy import exp, pi, sqrt, sin, cos
import math
from math import pow
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib import cm
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


k = 0.1
h = 0.1
a = -20.0
b = 20.0
n = (b-a)/h
m = 5.44e-4 #1.004 #amu
#planks = 6.626e-34 J*s
planks = 3.99e-5 #L*s
h_bar = planks / (2*pi)
imag = complex(0,1) # imaginary number
omega = 1.0e-2
#ulist = []
frames = 100
x_list = []
phi_list = []
phi_time = []
V = []
t=0
#level = int(sys.argv[1])
permittivity = 0.572779161 # permittivity of a vacuum in e^2 * fs^2 / amu * A^3

def gaussian(x, a=0.25):
  return pow((2.0 * a / pi),0.25) * exp(-a * x * x)

def normalize(f):
  '''normalizes a function'''
  area = 0.0
  for x in np.arange(a,b,h):
    fx = abs(f(x))
    area += h * fx * fx
  return area

squigglyarea_inv = 1.0
def squiggly(x, a1=0.25, b1=10.0):
  #normed = normalize
  global squigglyarea_inv
  return squigglyarea_inv * exp(-a1 * x * x) * sin(b1 * x)

print "normalize(squiggly)", normalize(squiggly)
squigglyarea_inv = sqrt(1.0 / normalize(squiggly))
print "squigglyarea_inv:", squigglyarea_inv
#exit()

def fourier_transform(f, a, b, h):
  result = []
  prefix = 1.0 / sqrt(2.0 * pi)
  for k in np.arange(a,b,h): # move piece by piece over the function from a to b
    value_at_k = 0.0
    for x in np.arange(a,b,h): # iterate over all values of x
      value_at_k += (f(x) * (cos(k*x) - imag*sin(k*x)) * h)
    result.append(prefix * value_at_k)
  return result

def inv_fourier_transform(phi, t, a, b, h):
  result = []
  prefix = 1.0 / sqrt(2.0 * pi)
  for x in np.arange(a,b,h): # move piece by piece over the function from a to b
    value_at_x = 0.0
    counter = 0
    for k in np.arange(a,b,h): # iterate over all values of x
      interior = k*x - planks*k*k*t/(2.0*m)
      value_at_x += (phi[counter] * (cos(interior) - imag*sin(interior)) * h)
      counter += 1
    result.append(prefix * value_at_x)
  return result

def init():
  line.set_data([],[])
  return line,

def animate(t):
  #x = np.linspace(0,1,n)
  #y = np.sin(2 * np.pi * (x - 0.01 * i))
  line.set_data(x_list,inv_fourier_transform(phi_k, t*4.0, a, b, h))
  return line,

x_list = []
for i in np.arange(a,b,h):
  x_list.append(i)
psi_0 = gaussian # the starting wavefunction

psi_0_vals =[]
for x in np.arange(a,b,h):
  psi_0_vals.append(psi_0(x))

print "psi_0"
pprint(psi_0_vals)




phi_k = fourier_transform(psi_0, a, b, h)

t = 20.0
psi_t = inv_fourier_transform(phi_k, t, a, b, h)

print "phi_k"
pprint(phi_k)

phi_real = []
counter = 0
for i in np.arange(a,b,h):
  #phi_real.append(phi_k[counter])
  phi_real.append(abs(psi_0_vals[counter] * psi_0_vals[counter]))
  counter += 1

# plot the starting figure
fig1 = plt.figure()
ax = plt.axes(xlim=(a,b),ylim=(-2.5,2.5))
line, = ax.plot([],[],lw=2)

plt.xlabel('x')
plt.ylabel('PHI')
plt.title("Free particle")
plt.plot(x_list, psi_0_vals, 'r', x_list, phi_real, 'g', x_list, psi_t, 'b')
line_ani = animation.FuncAnimation(fig1, animate, frames=frames, interval = 20.0, blit=True, init_func=init)
plt.show()

if __name__ == '__main__':
    pass
