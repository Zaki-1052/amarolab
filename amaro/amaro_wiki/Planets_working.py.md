# Planets working.py

`
    
    
    
    # planet numerical simulator
    # by Lane Votapka
    
    
    from math import pi
    from time import time
    from numpy import array, matrix
    import numpy
    
    import pygame
    from pygame.locals import *
    
    class Body():
      def __init__(self, x0, y0, vx0, vy0, mass, radius, name=''):
        '''creates a celestial body given position vector, velocity vector, mass,
    and radius'''
        self.pos = numpy.array([x0, y0])
        #self.nextpos = numpy.array([0.0,0.0]) # this cannot be updated here
        self.vel = numpy.array([vx0, vy0]) * timezoom
        self.nextvel = numpy.array([vx0,vy0]) * timezoom
        self.acc = numpy.array([0.0,0.0])
        self.nextacc = numpy.array([0.0,0.0])
        self.mass = mass
        self.radius = radius
        self.name = name
        
        self.nextpos = self.pos + self.vel*starting_timestep + 0.5*self.acc*starting_timestep*starting_timestep # must be updated here to have an initial acceleration
        return
        
      def verlet(self,timestep):
        '''performs the velocity-verlet algorithm to integrate planetary motion'''
        self.nextvel = self.vel + 0.5*(self.acc + self.nextacc)*timestep # find the velocity of the next step
        # now update all values
        self.pos = self.nextpos
        self.vel = self.nextvel
        self.acc = self.nextacc
        # find the position of the next step
        self.nextpos = self.pos + self.vel*timestep + 0.5*self.acc*timestep*timestep # position portion of the verlet alg
    
    def physics(timestep, bodylist):
      # first get all the accelerations
      
      for i in range(len(bodylist)):
        
        for f in range(i+1,len(bodylist)): # compare to all other bodies
          #if i == f: # then we are just comparing to ourselves
            #continue
          # implement the law of gravitation
          dist = numpy.linalg.norm(bodylist[i].nextpos - bodylist[f].nextpos) # distance between the two bodies
          #print 'dist', bodylist[f].name, bodylist[i].name, dist
          #print 'dists', bodylist[i].name, bodylist[f].name, dist
          force_mag = (g*(timezoom**2)*bodylist[f].mass*bodylist[i].mass)/(dist**2)
          #print 'forcemag', bodylist[f].name, bodylist[i].name, force_mag
          force = ((bodylist[f].nextpos - bodylist[i].nextpos)/dist) * force_mag
          #print 'force', bodylist[f].name, bodylist[i].name, force
          bodylist[i].nextacc += force / bodylist[i].mass # increment the forces upon each body
          bodylist[f].nextacc -= force / bodylist[f].mass
        #print 'acc', bodylist[i].name, bodylist[i].nextacc
        #print 'nextacc', bodylist[i].name, bodylist[i].nextacc
        bodylist[i].verlet(timestep)
      for body in bodylist: # set all accelerations to zero
        body.nextacc = numpy.array([0,0])
        
      return
    
    def graphics(bodylist,center, zoom=100000.0):
      '''draws all the planets'''
      inv_zoom = 1/zoom
      #offsetvec = (center.pos*inv_zoom)
      background.fill((250,250,250))
      for body in bodylist:
        drawvec = ((body.pos - center.pos) * inv_zoom) + numpy.array([screenwidth*0.5,screenheight*0.5])
        #print 'drawvec', drawvec
        
        
        pygame.draw.circle(background, 0, drawvec, 2.0, 1)
      #background.blit(text, (0,0))
      
      screen.blit(background,(0,0))
      pygame.display.flip()
      return
        
    #def timeloop(bodylist):
    #  '''the main simulation loop'''
      
    #  t = t+1
    
    
    # initialize the simulation
    screenwidth = 800
    screenheight = 600
    framerate = 0.030 #fps
    
    # physical constants
    g = 6.67384e-20 # km^3 kg^-1 s^-2
    timezoom = 100000000
    timestep = 0.0001
    starting_timestep = timestep
    
    # create all the celestial bodies
    bodylist = []
    bodylist.append(Body(x0=0.0, y0=0.0, vx0=0.0, vy0=0.0, mass=1.9891e30, radius=695500, name='sun'))
    bodylist.append(Body(x0=149669180, y0=0.0, vx0=0.0, vy0=29.8072, mass=5.97219e24, radius=6378.1, name='earth'))
    bodylist.append(Body(x0=150053580, y0=0.0, vx0=0.0, vy0=30.8302, mass=7.34767e22, radius=1737.4, name='moon'))
    center = bodylist[1] # the body that recieves the focus of the display
    zoom = 500000.0
    
    # initialize pygame
    pygame.init
    #physicsclock = pygame.time.Clock()
    #frameclock = pygame.time.Clock()
    screen = pygame.display.set_mode((screenwidth, screenheight))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250,250,250))
    #font = pygame.font.Font(None,12)
    screen.blit(background, (0,0))
    pygame.display.flip()
    
    # loop preparations
    lasttime = time()
    lastframe = lasttime
    pticks = 0
    quitting = False
    
    # main loop
    while not quitting:
      curtime = time()
      ptick = curtime - lasttime # how much time has elapsed since the last physics
      ftick = curtime - lastframe
      pticks += 1
      physics(ptick * timestep, bodylist) # update the physics
      if ftick >= framerate: # then update the graphics
        graphics(bodylist, center, zoom)
        lastframe = curtime # the last time we updated was now
        print 'pticks', pticks
        pticks = 0
        
        #quitting = True
      lasttime = curtime
      # handle pygame events
      for event in pygame.event.get():
        if event.type == QUIT:
          quitting = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
          quitting = True
      #quitting = True
        
    
    

`
