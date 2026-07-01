# By Lane Votapka
# Amaro lab 2013

'''
Contains functions designed to help with the learning and reasoning of a
Bayesian Net
'''

import sys, os, math
from math import sqrt, pi, exp, log
import numpy as np
import random

# Learning
                 #in #out
ML_training_data = [(np.array(()),0.0),] # data must be in this format
ML_training_data_test = [
(np.array((1,2,1)),0.1),
(np.array((2,3,1)),0.2),
(np.array((5,5,1)),0.3),  # NOTE: adding a 1 to the end of every data point allows for a k-intercept to the linear regression
(np.array((4,4,1)),0.4),
(np.array((4,100,1)),0.4),
]

sigmoid_training_data_test = [
(np.array((4.0,-5.0,1)),1),
(np.array((-4,2.0,1)),0),
(np.array((3,-0.1,1)),1),  # NOTE: adding a 1 to the end of every data point allows for a k-intercept to the linear regression
(np.array((2.0,4,1)),0),
(np.array((1.0,3,1)),0),
]

sigmoid_training_data_test_nointer = [
(np.array((4.0,-5.0)),1),
(np.array((-4,2.0)),0),
(np.array((3,-0.1)),1),  # NOTE: adding a 1 to the end of every data point allows for a k-intercept to the linear regression
(np.array((2.0,4)),0),
(np.array((1.0,3)),0),
]
# ML algorithm

def ML_continuous_linear(data):
  '''uses linear regression to estimate the output Y based on the input
  vector Xi
  '''
  #Must find E[Y] = sum wi*xi
  #p(Y=y|Xi=xi) = 1/sqrt(2*pi*sigma**2) * exp((-1/2*sigma**2)*(y-dot(w,x))**2)

  # need to learn parameters wi
  # have training examples (xt,yt) for t=1 to T
  # need to solve b = Aw, where b = sum(yt,xit) and A = sum(xt*xt.T)

  T = len(data) # the total number of training data points
  d = len(data[0][0]) # this is the length of the input vector x
  
  b = np.zeros(d)
  A = np.zeros((d,d))
  
  for t in range(T): # for all training data points
    xt = data[t][0] # a tuple
    yt = data[t][1] # a float value
    print "b:", b
    print "xt:", xt, "yt:", yt
    print "A:", A
    b += xt * yt
    A += np.outer(xt,xt)
  
  if T < d: # then the width of the vector exceeds the number of data points
    print "ML_continuous Alert: size of input vector exceeds training dataset size. Using Moore-Penrose pseudoinverse..."
    A_pinv = np.linalg.pinv(A) # need to get the pseudoinverse
    w = A_pinv*b
  else:
    w = np.linalg.solve(A,b) # solve the system of equations
  # Next: calculate sigma**2
  print "w:", w
  sigma_sum = 0.0
  for t in range(T):
    xt = data[t][0] # a tuple
    yt = data[t][1] # a float value
    y_avg = np.dot(w,xt)
    print "y_avg:", y_avg, "yt:", yt, "d_sigma:", (yt - y_avg)**2
    sigma_sum += (yt - y_avg)**2

  sigma_sq = sigma_sum / (2 * pi * T)
  return w, sigma_sq # E[Y] = sum wi*xi
    


def sig(z):
  '''calculates the value of the sigmoid function for z'''
  return 1 / (1 + exp(-z))

def sig_prime(z):
  '''calculates the derivative of the sigmoid function for z'''
  return sig(z)*sig(-z)

def sigmoid_learning_newton(data):
  '''uses logistic regression by means of Newtons method to learn the weights
   in a logistical model of the Baysian net by maximizing the log odds function L.

   NOTE: it can be proven that L has no spurious local maxima (L is convex!)
   so the global maximum will be found
   '''
  # belief network
  # a vector of real valued X's (parents)
  # a {1,0} value Y (child)
  # p(Y=1|X=x) = sig(w*x)
  # to find the max, must use Newton's method to find the zero of the derivative of L
  max_iter = 100 # how many iterations we should go before giving up on convergence
  max_error = 0.0000001 # the error to be satisfied within
  T = len(data) # the total number of training data points
  d = len(data[0][0]) # this is the length of the input vector x
  # first calculate random weights
  w = np.zeros(d)
  for i in range(d):
    w[i] = random.random() - 0.5
  L = 0
  
  for i in range(max_iter):
    #print "w:", w
    # calculate the Hessian matrix: 2nd deriv. of L with respect to all pairs of X variables
    H = np.zeros((d,d)) # width and height of Hessian equal to size of input vector
    old_L = L
    L = 0
    partial_L_partial_w = np.zeros(d) # vector of 1st derivs
    for t in range(T): # run thru the data
      xt = data[t][0] # a tuple
      yt = data[t][1] # a float value
      # get partial_L_partial_w
      partial_L_partial_w += (yt - sig(np.dot(w,xt))) * xt # difference between target value y and model's prediction
      H -= sig(np.dot(w,xt))*sig(-np.dot(w,xt))*np.outer(xt, xt)
      L += yt*log(sig(np.dot(w,xt))) + (1-yt)*sig(-np.dot(w,xt))
    #print "H:", H
    #print "partial_L_h:", partial_L_partial_w
    # now that we have the hessian, we must invert it
    H_inv = np.linalg.inv(H)
    #print "dot:", np.dot(H_inv,partial_L_partial_w)
    new_w = w - np.dot(H_inv,partial_L_partial_w)
    #print "diff:", new_w - w
    error = abs(L-old_L)
    print "i:", i, "w:", w, "new_w:", new_w, "L:", L, "error:", error
    if error < max_error: break # then exit the loop because we have found the optimal
    w = new_w
  return w

print "w:"
#print ML_continuous_linear(ML_training_data_test)
print sigmoid_learning_newton(sigmoid_training_data_test)

def EM_discrete_hardcode(theta0):
  '''uses the general EM algorithm to maximize the log probability of the data

hardcoded for the special case of one layer of hidden nodes

'''
  # L = sum ( log p(Vt = vt)) the log probability of the visible data
  #   = sum over data ( log sum over hidden ( p(Vt = vt, Ht = ht))
  # after lots of impressive math...
  # need to maximize the function F
  # F = sum over nodes i ( sum over data points t ( sum over hidden nodes h (...
  #   p(h|vt;theta0)log p(xi|pai;theta)

  # first the M step, that is, to estimate the probs of the hidden values given
  # the visible values

  max_tries = 100
  theta_t = theta0
  v1 = 6 # number of input nodes
  h = 3 # number of hidden nodes
  v2 = 1 # number of output nodes
  for iter in range(max_tries): # the number of times we iterate to reach the max

    # E step: compute p(h|v1, v2)
    # p(h|v1,v2) = p(v2|h)*p(h|v1) / sum over all h' p(v2|h')*p(h'|v1)
    p_h_given_v1_v2 = multiply_gaussians(p_v2_given_h , p_h_given_v1) #/ divided by integration over gaussian product = 1

    # M step 1: compute p(h|v1)
    # p(h|v1) = sum over all data, integrate over
