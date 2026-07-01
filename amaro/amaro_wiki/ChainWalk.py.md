# ChainWalk.py

`
    
    
    
    import numpy as np
    import random
              #left, right
    actions = [0   , 1   ]
    states = [1,2,3,4]
    reward = [0,1,1,0]
    
    
    def learn():
      learningRate = .9
      numTrain = 50
      d = 6
    
      training = trainingTup(numTrain)
      w = initW(d)
      print w
      for itter in range(5):
    
        aMat = []
        for (s,aDrop,r,sPrime) in training:
          w_dot_phiMat = [np.dot(w, phi(sPrime,a) ) for a in actions]
          #print w_dot_phiMat
          aMat.append( np.argmax(w_dot_phiMat) )
    
        print aMat
    
        bigPhi = []
        PPhi = []
        R = []
        for i in xrange(numTrain):
          s = training[i][0] 
          a = training[i][1]
          sPrime = training[i][3]
          aPrime = aMat[i]
    
          bigPhi.append( phi(s,a)  )
          PPhi.append( phi(sPrime,aPrime) )
          R.append(training[i][2])
    
        bigPhi = np.array(bigPhi)
        PPhi = np.array(PPhi)
    
        w = np.dot( bigPhi.T, bigPhi - learningRate*PPhi)
        w = np.dot( np.dot( np.linalg.pinv( w ) , bigPhi.T) , R)
        print w
        print '\n'
    
    def trainingTup(d):
      training = []
      for i in xrange(d):
        s = random.choice(states)
        a = random.choice(actions)
        r = random.choice(reward)
        sPrime = random.choice(states)
        training.append( (s,a,r,sPrime )  )
    
      return training
    
    
    
    def initW(d):
      nums = [random.uniform(0,1) for x in range(0,d)]
      sums = reduce(lambda x,y: x+y, nums)
      norm = np.array([x/sums for x in nums] )
      return norm
    
    
    
    
    
    
    
    
    
    
    
    
    def phi(s,a):
      
      isLeft = isRight = 1
      if a == 0:
        isLeft = 0
      else:
        isRight = 0
    
    
      basis =         ([ 
                        isLeft * 1,
                        isLeft * s,
                        isLeft * s**2,
    
                        isRight * 1,
                        isRight * s,
                        isRight * s**2
                      ])
    
      return basis
    
    
    

`
