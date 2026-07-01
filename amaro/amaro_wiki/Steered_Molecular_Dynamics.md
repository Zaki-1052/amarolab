# Steered Molecular Dynamics

## Steered Molecular Dynamics[edit](</mediawiki/index.php?title=Steered_Molecular_Dynamics&action=edit&section=1> "Edit section: Steered Molecular Dynamics")]

In its most general sense, SMD, or Steered Molecular Dynamics, means to guide your simulation with some sort of externally applied forces. There are at least four different ways to do SMD in NAMD, all documented in the [Applied Forces and Analysis](<http://www.ks.uiuc.edu/Research/namd/2.6/ug/node32.html>) section of the User's Guide. 

Dozens of [articles](<http://www.ks.uiuc.edu/Publications/Papers/SMD/>) about SMD have been published by the [Schulten group](<http://www.ks.uiuc.edu/>). 

## General Questions[edit](</mediawiki/index.php?title=Steered_Molecular_Dynamics&action=edit&section=2> "Edit section: General Questions")]

**How can I control the temperature?**

Pulling on atoms in your simulation means you are heating up the system. If you are doing a constant energy simulation (i.e., no temperature control), you'll see the total energy and temperature rise as the simulation progresses. This can be to your advantage: the difference in temperature between the start and finish of your simulation tells you exactly how much work you did on the system (you'll want to take an average before and after the SMD run to accurately measure the temperature). 

If you don't care to heat up your system, then you need a [temperature control](<http://www.ks.uiuc.edu/Research/namd/2.6/ug/node29.html>). 

  
**Which atoms should I constrain?**

That's up to you, but in general, select just enough of the backbone atoms to keep your system immobilized. 

  
**Should I use fixed atoms or restrained atoms?**

That depends. If the number of atoms you want to constrain makes up a substantial fraction of the entire system, using fixed atoms will give you a performance benefit. Restrained atoms, on the other hand, will leave the system more flexible, which might be important to you. 

  
**Which atoms should I pull?**

This is often the hardest part to get right. Expect to try several different combinations of atoms until you find one that leads to minimal distortion. 

  
**Should I pull with constant velocity or constant force?**

In constant velocity pulling, you attach dummy atoms to part of your system with springs, then drag the dummy atoms at constant speed. The nice thing about constant velocity pulling is that you'll always get to the final state in a known amount of time. Constant velocity pulling is also amenable to potential of mean force analysis; see below. The downside is that the size of the forces can get large as you go over barriers, leading to distortion of the system and/or poor sampling of the reaction path following the barrier due to inertia. If this happens you can either find a better reaction path, or else pull slower so that the system has time to sample alternative pathways around the barrier. 

In a constant force simulation, you'll spend most of your time waiting for the system to hop over a barrier. If you perform multiple runs, you can use this waiting time to estimate the size of the free energy barrier. 

  
**How do I compute potentials of mean force?**

You basically have two options, related to how you deal with irreversible work. 

  * Explicitly discounted irreversible work. If you assume a constant friction coefficient g, you can explicitly discount the irreversible work done on the system by subtracting the integral of gv over the reaction path, where v is the velocity. The potential can then be determined from a constant velocity SMD simulation by [integrating the force](<http://www.ks.uiuc.edu/Publications/Papers/paper.cgi?tbcode=BALS97>) or by [finding a potential](<http://www.ks.uiuc.edu/Publications/Papers/paper.cgi?tbcode=GULL99>) that best fits the position and force time series. A very nice and very general result for the possible precision of an constant velocity SMD simulation was obtained by Balsera et al. who showed that the variance in the PMF is proportional to the amount of irreversible work discounted.


  * Jarzynski's identity. If you do work on a system to bring it from state A to state B in a finite time, the average work will always exceed the free energy difference F between the two states: >= F. ?(in the limit of infinitely slow transitions, approaches F)?. Jarzynski derived an eqaulity: < exp(W) > = exp(F), i.e. the exponential average of W equals F. This equality has been exploited both [theoretically](<http://www.ks.uiuc.edu/Publications/Papers/paper.cgi?tbcode=JENS2002>) as well as [experimentally](<http://www.sciencemag.org/cgi/content/full/296/5574/1832>).



  
**How many runs should I do?**

If you want to make any sort of sense out of your SMD simulation, you really should plan to do it more than once, starting from the same initial conditions. This is a simple consequence of the irreversible work you are doing by driving the system far from equilibrium. Roughly speaking, the more irreversible work you do, the more irreproducible your simulation is. 

For constant velocity pulling, doubling the number of runs or halving the speed of the runs will reduce the variance in the potential of mean force estimated from the applied force by a factor of two. 

  
**Isn't umbrella sampling more efficient?**

Not according to this paper where it is shown that umbrella sampling and Jarzynski's identity have comparable efficiencies. Umbrella sampling may be more well suited for multi-dimensional PMF's.
