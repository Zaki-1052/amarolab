#!/usr/bin/python

# script to test the monte-carlo matrix sampler function
# by Lane Votapka

import numpy as np
from math import exp, log
import random
import sys

import matplotlib.pyplot as plt

if len(sys.argv) > 1:
  num_to_run = int(sys.argv[1])
else: 
  num_to_run = 20
  
if len(sys.argv) > 2:
  skip = int(sys.argv[2])
else:
  skip = 1

def count_mat_to_rate_mat(count_matrix, avg_t):
  ''' converts a count matrix to a markov rate matrix (where each entry is an effective kinetic rate constant)'''
  n = np.shape(count_matrix)[0]
  rate_matrix = np.matrix(np.zeros((n,n)))
  sum_vector = np.zeros(n)
  for i in range(n): # first make the sum of all the counts
    for f in range(n):
      sum_vector[f] += count_matrix[i,f]
      
      
  for i in range(n):
    for f in range(n):
      if f == i: continue
      if sum_vector[f] == 0 or avg_t[f] == 0.0:
        rate_matrix[i,f] = 0.0
      else:
        rate_matrix[i,f] = count_matrix[i,f] / (sum_vector[f] * avg_t[f])
      rate_matrix[f,f] -= rate_matrix[i,f]
  
  return rate_matrix, sum_vector



def rate_mat_to_prob_mat(rate_matrix):
  n = rate_matrix.shape[0]
  P = np.matrix(np.zeros((n,n)))
  prob_matrix = np.matrix(np.zeros((n,n)))
  sum_vector = np.zeros(n)
  avg_t = np.zeros(n)
  for i in range(n): # first make the sum of all the rates
    for j in range(n):
      if j == i: continue
      sum_vector[j] += rate_matrix[i,j]
      
      
  for i in range(n):
    for j in range(n):
      if j == i: continue
      if sum_vector[j] == 0:
        prob_matrix[i,j] = 0.0
        #avg_t[j] = 0.0
      else:
        prob_matrix[i,j] = rate_matrix[i,j] / sum_vector[j]
      
    if sum_vector[i] != 0.0:
      avg_t[i] = 1.0 / sum_vector[i]
  
  return prob_matrix, avg_t

  
  
  
def monte_carlo_milestoning_nonreversible_error(N, avg_t, num = 20, skip = 0):
  ''' Samples a distribution of rate matrices that are nonreversible
      using Markov Chain Monte Carlo method
      
      The distribution being sampled is:
      p(Q|N) = p(Q)p(N|Q)/p(N) = p(Q) PI(q_ij**N_ij * exp(-q_ij * N_i * t_i))
      
      N = count matrix
      avg_t = incubation times
      
  '''
  Q0, N_sum = count_mat_to_rate_mat(N, avg_t) # get a rate matrix and a sum of counts vector
  m = N.shape[0] # the size of the matrix
  Q = Q0
  Q_mats = []
  
  for counter in range(num*(skip+1)):
    Qnew =  np.matrix(np.zeros((m,m))) #np.matrix(np.copy(T))
    for i in range(m): # rows
      for j in range(m): # columns
        Qnew[i,j] = Q[i,j]
        
    for i in range(m): # rows
      for j in range(m): # columns
        if i == j: continue
        if Qnew[i,j] == 0.0: continue
        if Qnew[j,j] == 0.0: continue
        delta = random.expovariate(1.0/(Qnew[i,j])) - Qnew[i,j] # so that it's averaged at zero change, but has a minimum value of changing Q[j,j] down only to zero
        
        if np.isinf(delta): continue
        r = random.random()
        
        # NOTE: all this math is being done in logarithmic form first (log-likelihood)
        new_ij = N[i,j] * log(Qnew[i,j] + delta) - ((Qnew[i,j] + delta) * N_sum[j] * avg_t[j])
        old_ij = N[i,j] * log(Qnew[i,j]) - ((Qnew[i,j]) * N_sum[j] * avg_t[j])
        #new_jj = N[j,j] * log(-(Qnew[j,j] - delta)) + ((Qnew[j,j] - delta) * N_sum[j] * avg_t[j])
        #old_jj = N[j,j] * log(-(Qnew[j,j])) + ((Qnew[j,j]) * N_sum[j] * avg_t[j])
        
        p_acc = (new_ij - old_ij) # + (new_jj - old_jj)
        #p_acc = (exp(new_jj)/exp(old_jj))*(exp(new_ij)/exp(old_ij))
        if log(r) <= p_acc: # this can be directly compared to the log of the random variable
          Qnew[j,j] = Qnew[j,j] - delta
          Qnew[i,j] = Qnew[i,j] + delta
        
    if skip == 0 or counter % skip == 0: # then save this result for later analysis
      Q_mats.append(Qnew)
    Q = Qnew
  return Q_mats
  
def sample_milestoning_distribution(x, y, N, sum_vector, avg_t):
  ''' samples the value at a particular point in a distribution'''
  #print "N:", N
  #print "int(N[0,1]):", int(N[0,1])
  #print "int(N[1,0]):", int(N[1,0])
  #print "avg_t[0]:", int(avg_t[0])
  #print "sum_vector[0]:", int(sum_vector[0])
  #print "avg_t[1]:", int(avg_t[1])
  #print "sum_vector[1]:", int(sum_vector[1])
  N01 = int(N[0,1])
  N10 = int(N[1,0])
  t0 = int(avg_t[0])
  t1 = int(avg_t[1])
  N0 = int(sum_vector[0])
  N1 = int(sum_vector[1])
  L = x**N01 * y**N10 * np.exp(-x*t1*N1 - y*t0*N0)
  return L
  
  

N = np.matrix([[1e99, 102, 0],
     [0, 0 ,0 ],
     [0, 706, 1e99]])
     
avg_t = np.matrix([[0], [7338.8], [0]])
'''
N = np.matrix([[0, 12],
               [30, 0]])
avg_t = np.matrix([[500.0], [100.0]])
'''
m = N.shape[0]

Q, sum_mat = count_mat_to_rate_mat(N, avg_t)

print "Q:", Q
print "sum_mat:", sum_mat

Q_mats = monte_carlo_milestoning_nonreversible_error(N, avg_t, num_to_run, skip)

#print "Q_mats:", Q_mats

# now calculate quantities from it

P, new_avg_t = rate_mat_to_prob_mat(Q)
print "P:", P
print "new_avg_t:", new_avg_t

I_K = np.matrix(np.identity(m) - P.T) # solve the sinked matrix
mfpt = np.linalg.solve(I_K, new_avg_t)

print "mfpt:", mfpt

betas = []
mfpts = []
x = []
y = []

for i in range(num_to_run): # run through our distribution of rate matrices
  Q1 = Q_mats[i]
  P1, mc_new_avg_t = rate_mat_to_prob_mat(Q1)
  beta = P1[0,1]
  #print "P:", P1
  #print "beta:", beta
  #print "new_avg_t:", mc_new_avg_t
  I_Kmc = np.matrix(np.identity(m) - P1.T) # solve the sinked matrix
  mfptmc = np.linalg.solve(I_Kmc, mc_new_avg_t)
  #print "mfpt[%d]:" % i, mfptmc[1]
  betas.append(beta)
  #x.append(Q1[0,1])
  #y.append(Q1[1,0])
  mfpts.append(mfptmc[1])

print "avg beta:", np.mean(betas)
print "std beta:", np.std(betas)
print "avg mfpt:", np.mean(mfpts)
print "std mfpt:", np.std(mfpts)
'''

print "mean x:", np.mean(x)
print "mean y:", np.mean(y)
xmin = 0.001
xmax = 0.025
ymin = 0.001
ymax = 0.004
# plot the 2d histogram

plt.hexbin(x,y, gridsize=(60,50), cmap=plt.cm.jet) # YlOrRd_r
plt.axis([xmin, xmax, ymin, ymax])
plt.show()


plt.subplots_adjust(hspace=0.0)
plt.subplot(121) # a 1x2 set of plots, first of them
plt.hexbin(x,y, gridsize=40, cmap=plt.cm.jet) # YlOrRd_r
plt.axis([xmin, xmax, ymin, ymax])
plt.title("MC binning")
#cb = plt.colorbar()
#cb.set_label('counts')

# plot the true distribution
x_linspace = np.linspace(xmin, xmax, 100)
y_linspace = np.linspace(ymin, ymax, 100)
x_index, y_index = np.meshgrid(x_linspace, y_linspace)
z = sample_milestoning_distribution(x_index, y_index, N, sum_mat, avg_t)

plt.subplot(122) # a 1x2 set of plots, second of them
plt.pcolor(x_index, y_index, z, cmap=plt.cm.jet )  # YlOrRd_r
#plt.hexbin(x,y,bins='log', cmap=plt.cm.YlOrRd_r)
plt.axis([xmin, xmax, ymin, ymax])
plt.title("Actual Dist")
#cb = plt.colorbar()
#cb.set_label('log10(N)')

plt.show()



'''
