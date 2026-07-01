# Memb analyze.py

`
    
    
    
    #!/usr/bin/python
    
    ''' given a file where we have a record of all grid transitions, will construct the milestoning reaction kernels for kinetic/thermodynamic analysis'''
    
    import os, sys, math
    from math import exp, log
    from pprint import pprint
    import numpy as np
    from scipy import linalg
    from copy import deepcopy
    import matplotlib.pyplot as plt
    k = 1.3806488e-23
    T = 300
    
    
    
    infilename = "memb_h2o_trans.txt"
    infile = open(infilename, 'r')
    
    def make_K_matrix(Kcount,n,n2):
      K=[]
      for i in range(n2): 
        K_row = []
        for j in range(n2):
          K_row.append(0.0)
        K.append(K_row)
     #   avg_t.append([])
      for i in range(n): # for every row
        denom = reduce(lambda x, y: x+y, Kcount[(n-1)-i])
        for j in range(n): # for every element in the matrix
          if denom == 0: continue
          if i==n-1: # then we are in the middle state
            K[n2/2][n2/2-1] = K[n2/2][n2/2+1] = 0.0
            #otherK[n2/2][n2/2-1] = otherK[n2/2][n2/2+1] = 0.5/avg_t[i]
          prob = float(Kcount[(n-1)-i][(n-1)-j]) / denom
          #prob2 = prob/avg_t[i]
          K[i][j] = K[(n2-1)-i][(n2-1)-j] = prob
     #     otherK[i][j] = otherK[(n2-1)-i][(n2-1)-j] = prob2
      return K
    
    class Transition():
      # a class for all the transitions
      def __init__(self, src, dest, inc_time, abs_time):
        self.src = src
        self.dest = dest
        self.time = inc_time
        self.abs_time = abs_time
    
    unsorted_translist = [] # a list of all the grid transitions
    
    
    for line in infile:
      # process each line
      if not line.startswith("TCL SCRIPT: GRID TRANSITION: "):
        print "Alert: nonstandard line found:", line
        continue # skip this line
      else: # parse the line
        linetail = line[29:-1] # just take the last bit of the line, the important part, but not the endline
        #print linetail
        if linetail.startswith("source:"):
          src = linetail.split()[1]
        elif linetail.startswith("destination:"):
          dest = linetail.split()[1]
        elif linetail.startswith("current step"):
          abs_time = int(linetail.split()[-1])
        elif linetail.startswith("incubation time"):
          time = linetail.split()[-2]
    
          # also, log this entry
          #print "src: %s dest: %s time %s" % (src,dest,time)
          unsorted_translist.append(Transition(src,dest,time, abs_time))
    
    infile.close()
    
    # sort the translist 
    translist=[]
    translist = sorted(unsorted_translist, key=lambda trans: trans.abs_time)
    
    # now loop thru all the transitions, and fill out the matrices
    
    n = 23
    n2 = 45
    started_list = [False]*n
    Kcount = []
    K = []
    avg_t = []
    avg_t_mat = []
    for i in range(n):
      Kcount_row = []
      for j in range(n):
        Kcount_row.append(0)
      Kcount.append(Kcount_row)
      avg_t_mat.append([]) # append rows to the time vector
    
    K_converge_count=[]
    K_converge = []
    avg_t_conv_list = []
    
    for i in range(n2): 
      K_row = []
      for j in range(n2):
        K_row.append(0.0)
      K.append(K_row)
      avg_t.append([])
       
    counter=0
    for trans in translist:
      src = int(trans.src) + 1
      dest = int(trans.dest) + 1
      time = int(trans.time)
      abs_time = int(trans.abs_time)
      if time < 100 or abs_time < 100: # skip
        continue
      if started_list[src] == False: # then this is the first transition, disregard
        started_list[src] = True
        continue
      #print "%d %d %d" % (src, dest, time)
      Kcount[src][dest] += 1
      avg_t_mat[src].append(time)
      if counter % 100 == 0: # I don't want to save these too often
        K_converge_count.append(deepcopy(Kcount)) # copy the count matrix to be used for convergence analysis later
        avg_t_conv = deepcopy(avg_t)
        try:
          for i in range(1,len(avg_t_mat)-1):
            avg_t_conv[(n2/2)+i] = avg_t_conv[(n2/2)-i] = reduce(lambda x, y: y+x,avg_t_mat[i])/len(avg_t_mat[i])
          avg_t_conv[n-1]=10000
          avg_t_conv[0]=avg_t_conv[-1]=avg_t_conv[1]
          avg_t_conv_list.append(avg_t_conv)
        except TypeError:
          avg_t_conv_list.append(np.zeros(n2).tolist())
    
      counter+=1
      
    #pprint(avg_t_mat)
    
    Kcount[0][1] = Kcount[1][2]
    Kcount[-1][-2]=Kcount[-2][-1]
    #pprint(Kcount)
    
    
    for i in range(1,len(avg_t_mat)-1):
      avg_t[(n2/2)+i] = avg_t[(n2/2)-i] = reduce(lambda x, y: y+x,avg_t_mat[i])/len(avg_t_mat[i])
      
    # a hack because I never simulated this part
    avg_t[n-1]=10000
    avg_t[0]=avg_t[-1]=avg_t[1]
    
    #print "incubation time vector"
    #pprint(avg_t)
    
    # calculate K matrix
    '''
    otherK = deepcopy(K) # make another copy of K
    for i in range(n): # for every row
      denom = reduce(lambda x, y: x+y, Kcount[(n-1)-i])
      for j in range(n): # for every element in the matrix
        if denom == 0: continue
        if i==n-1: # then we are in the middle state
          K[n2/2][n2/2-1] = K[n2/2][n2/2+1] = 0.0
          otherK[n2/2][n2/2-1] = otherK[n2/2][n2/2+1] = 0.5/avg_t[i]
        prob = float(Kcount[(n-1)-i][(n-1)-j]) / denom
        prob2 = prob/avg_t[i]
        K[i][j] = K[(n2-1)-i][(n2-1)-j] = prob
        otherK[i][j] = otherK[(n2-1)-i][(n2-1)-j] = prob2
     '''
    K = make_K_matrix(Kcount,n,n2)
    
    #for i in range(n):
    #  otherK[i][i] = 1 - reduce(lambda x,y: x+y, otherK[i])
     # otherK[-1-i][-1-i] = otherK[i][i]
    
    K[n2/2][n2/2-1] = K[n2/2][n2/2+1] = 0.5
    
    
    K = np.matrix(K)
    Ktau = deepcopy(K)
    Ktau[-1,-2] = 0.0
    
    #print "Kcount"
    #pprint(Kcount)
    print "K"
    pprint(K)
    
    #for i in range(n2):
      #print reduce(lambda x,y: x+y, K[i].tolist())
    
    print "Thermodynamics:"
    #Kinf = otherK ** 10000000
    #for i in Kinf[0].tolist()[0]
    #  print i
    
    eigs = linalg.eig(K, left=True, right=False)
    reals = []
    for i in eigs[0].tolist():
      reals.append(i.real)
    eval_index = reals.index(max(reals))
    evec = eigs[1][:,eval_index]
    qstat = evec
    #print "qstat:", qstat
    pstat = np.array(qstat)*avg_t
    fat_pstat = pstat/pstat[0]
    pstat = pstat/sum(pstat)
    print "pstat:", pstat
    
    def energy(prob):
      return -k*T*log(prob.real)
    PMF = map(energy, fat_pstat)
    print "PMF:"
    print PMF
    print "==============="
    print "Kinetics"
    one_side_pstat = np.zeros(n2)
    one_side_pstat[0] = 1.0
    print "one_side_pstat:", one_side_pstat
    #print "avg_t:", np.matrix([avg_t]).T
    I_Kinv = np.linalg.inv(np.identity(45) - Ktau)
    tau = np.matrix([one_side_pstat]) * I_Kinv * np.matrix([avg_t]).T
    print "MFPT (in femtoseconds):", tau
    print "MFPT (in cm/s):", (46/tau)*(1e5)
    
    print "==============="
    print "Convergence"
    
    
    pstat_conv = []
    qstat_conv = []
    mfpt_conv = []
    log_plot = []
    counter = 0
    for K_conv_count in K_converge_count:
      K_conv = np.matrix(make_K_matrix(K_conv_count,n,n2)) # make each K matrix
      K_conv[n2/2,n2/2-1] = K_conv[n2/2,n2/2+1] = 0.5
      K_conv[0,1] = K_conv[-1,-2] = 1.0
      try:
        eigs = linalg.eig(K_conv, left=True, right=False)
        reals = []
        for i in eigs[0].tolist():
          reals.append(i.real)
        eval_index = reals.index(max(reals))
        evec = eigs[1][:,eval_index]
        qstat = evec
        #print "qstat:", qstat
        pstat = np.array(qstat)*avg_t
        fat_pstat = pstat/pstat[0]
        pstat = pstat/sum(pstat)
        #print "pstat:", pstat
        pstat_conv.append(pstat)
        qstat_conv.append(qstat)
        Ktau_conv = K_conv
        Ktau_conv[-1,-2] = 0.0
      
        I_Kinv = np.linalg.inv(np.identity(45) - Ktau_conv)
        tau = np.matrix([pstat]) * I_Kinv * np.matrix([avg_t_conv_list[counter]]).T
        mfpt_conv.append(float(tau))
        if tau > 0.0:
          log_plot.append(log(float(tau)))
        else:
          log_plot.append(0.0)
      except:
        pstat_conv.append(np.zeros(n2))
        qstat_conv.append(np.zeros(n2))
        mfpt_conv.append(0.0)
        log_plot.append(0.0)
      counter+=1
    
    middle_prob = []
    for i in range(len(K_conv_count)):
        middle_prob.append(pstat_conv[i].tolist()[22])
    
    x1 = np.arange(0,len(mfpt_conv)) * (1000.0/len(mfpt_conv))
    y1 = np.array(log_plot)
    y2 = np.array(mfpt_conv)
    #plt.plot(x1,y2)
    #plt.yscale('log')
    plt.plot(x1[150:],y2[150:]/1000000)
    plt.xlabel('simulation time per milestone (ps)')
    plt.ylabel('mean first passage time across membrane (ns)')
    plt.title('Convergence of MFPT')
    plt.show()
    
    

`
