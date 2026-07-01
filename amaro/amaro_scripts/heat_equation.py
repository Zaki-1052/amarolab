# Solver for the 2-dimensional heat equation using finite-difference
# (and maybe later, finite element)

import numpy as np
from numpy import matrix
import math
import matplotlib.pyplot as plt
from matplotlib import cm
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
#from mayavi import mlab

k = 0.001
h = 0.1
ulist = []
frames = 20000
n = 50
width = 10


def forward_euler_1d(u, k, h):
  #awful method
  unext = np.zeros(len(u))
  lam = k / h**2 # lambda
  for i in range(len(u)): # for each element in this array
    nextindex = i+1
    if nextindex >= len(u):
      nextindex = 0 # impose periodic boundary conditions
    unext[i] = lam*u[i-1] + (1 - 2*lam)*u[i] + lam*u[nextindex]
  return unext

def forward_euler_2d(u,k,h):
  unext = np.zeros(np.shape(u))
  lam = k / h**2 # lambda
  for i in range(np.shape(u)[0]): # for every row
    inext = i+1
    iprev = i-1
    if inext >= np.shape(u)[0]:
      inext = 0 # impose periodic boundary conditions
    for f in range(np.shape(u)[1]): # for every col
      fnext = f+1
      fprev = f-1
      if fnext >= np.shape(u)[1]:
        fnext = 0 # impose periodic boundary conditions
      unext[i,f] = lam*(u[iprev,f] + u[inext,f] + u[i,fprev] + u[i,fnext]) + (1-4*lam)*u[i,f]
  return unext    

def dufort_frankel_1d(u, uprev, k, h):
  #better method
  unext = np.zeros(len(u))
  lam = k / h**2 # lambda
  alph = 2*lam
  for i in range(len(u)): # for each element in this array
    inext = i+1
    iprev = i-1
    if inext >= len(u):
      inext = 0 # impose periodic boundary conditions
    unext[i] = ((1-alph)/(1+alph))*uprev[i] + (alph/(1+alph))*(u[iprev] + u[inext])
  return unext

def backward_euler_1d(u,k,h):
  '''u is the starting vector, k is the timestep, h is the distance step'''
  lam = k / h**2 # lambda
  diag = 1 + 2*lam # what goes on the main diagonal
  B = matrix(np.zeros([len(u),len(u)])) # form matrix to solve next step
  for i in range(len(u)):
    B[i,i] = diag # set the main diagonal
    if i > 0: # if we arent on the leftmost edge
      B[i, i-1] = -lam
    if i < len(u)-1: # if we arent on the rightmost edge
      B[i, i+1] = -lam
  unext = np.linalg.solve(B, u) # solve the system for unext
  return unext # return solution

def system_ODE_RK(u0, A, N, h=1.0):
  '''uses Runge-Kutta to solve a system of differential equations
  u0: the initial values
  A: matrix describing transition rates
  N: number of iterations to proceed
  h: timestep size
  '''
  result = u0
  m = u0.size
  u=u0
  for i in range(N):
    k1 = h * (u * A)
    k2 = h * ((u + 0.5*k1) * A)
    k3 = h * ((u + 0.5*k2) * A)
    k4 = h * ((u + k3) * A)
    u = u + (k1 + 2*k2 + 2*k3 + k4)/6
    #print "u:",u
    result = np.concatenate((result, u), axis=0)
  return matrix(result)


def init():
  line.set_data([],[])
  return line,

def animate(i):
  x = np.linspace(0,1,n)
  #y = np.sin(2 * np.pi * (x - 0.01 * i))
  line.set_data(x,ulist[i])
  return line,

#def heat_eq_1d_anim(n, width=10):
#  global line
u = np.zeros((n,n))
u[n/2-n/width:n/2+n/width,n/2-n/width:n/2+n/width] = 1.0 # set a range of spots in the middle equal to 1.0
'''
for i in range(frames):
  unext = forward_euler_2d(u,k,h)
  ulist.append(unext)
  uprev = u
  u = unext
x = np.arange(0,n,1)
y = np.arange(0,n,1)
x,y = np.mgrid[0.:n:1, 0.:n:1]
print u
from numpy import pi, sin, cos, mgrid
dphi, dtheta = pi/250.0, pi/250.0
[phi,theta] = mgrid[0:pi+dphi*1.5:dphi,0:2*pi+dtheta*1.5:dtheta]
m0 = 4; m1 = 3; m2 = 2; m3 = 3; m4 = 6; m5 = 2; m6 = 6; m7 = 4;
r = sin(m0*phi)**m1 + cos(m2*phi)**m3 + sin(m4*theta)**m5 + cos(m6*theta)**m7
x = r*sin(phi)*cos(theta)
y = r*cos(phi)
z = r*sin(phi)*sin(theta)

#s = mlab.surf(x,y,ulist[0])
#mlab.show()
'''
#print 'now plotting animation'

'''
ms = s.mlab_source
for i in range(frames):
  ms.set(z = ulist[i])
  '''
'''fig = plt.figure()
ax = fig.gca(projection='3d')

r = np.sqrt((x*0.05)**2 + (y*0.05)**2)
z = np.sin(r)

line = ax.plot_surface(x,y,u, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
ax.set_zlim(0.0,1.0)
line_ani = animation.FuncAnimation(fig, animate, frames=frames, interval = 10, blit=True)

plt.show()



u = np.zeros(n)
u[n/2-n/width:n/2+n/width] = 1.0 # set a range of spots in the middle equal to 1.0
ulist.append(u)
for i in range(frames):
  unext = backward_euler_1d(u,k,h)
  ulist.append(unext)
  uprev = u
  u = unext

fig1 = plt.figure()
ax = plt.axes(xlim=(0,1),ylim=(0,1))
line, = ax.plot([],[],lw=2)

plt.xlabel('position')
plt.ylabel('heat')
plt.title("heat equation")
line_ani = animation.FuncAnimation(fig1, animate, frames=frames, interval = 10, blit=True, init_func=init)
plt.show()
'''
print "now plotting system of differential equations using Runge_Kutta"
N=10000 # number of iterations
u0 = np.matrix([[1,0,0]])
A = np.matrix([[-0.005,0.002,0],[0.005,-0.003,0],[0,0.001,0]])
result = system_ODE_RK(u0, A.T, N)
x = range(result.shape[0])
for i in range(result.shape[1]):
  y=result[:,i]
  plt.plot(x,y)

plt.show
# calculate MFPT

tau = 0.0
for i in range(A.shape[0]-1): # for every element on the diagonal, but the last
  t=-1.0/A[i,i] # mfpt for this state
  area = 0.0
  for f in range(result.shape[0]): # for every timestep
    area+=result[f,i]
  print "time for state",i,":",area
  tau += area # add total area under this curve to the final tau calculation
  
print "total MFPT: ", tau
