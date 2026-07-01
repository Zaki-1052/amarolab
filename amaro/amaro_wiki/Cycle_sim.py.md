# Cycle sim.py

`
    
    
    
    #!/usr/bin/python
    
    # given a cyclic economy, is there a pattern to buy/sell that optimizes returns
    from math import sin, pi
    import time
    #import pygame
    #from pygame.locals import *
    
    
    
    timesteps = 513
    amp = 1.0
    freq = pi / 256
    y_offset = 1.5
    
    start_money = 10000
    ideal_prop = 0.70 # ideal: 70% in market
    total_assets = start_money
    
    volume = 0.0
    money = start_money
    price = y_offset
    amount_spending = money * ideal_prop
    amount_buying = amount_spending / price
    volume = amount_buying
    money = money - amount_spending
    equities = volume * price
    total_assets = equities + money 
    
    print "money: %f, volume: %f, price: %f, total_assets: %f" % (money, volume, price, total_assets)
    
    
    def sinusoidal_cycle(t, amp, freq):
        return amp * sin(t*freq)
    
    #def buy_sell(money, price):
        #prop = 
    
    for step in range(int(timesteps)):
        price = y_offset + sinusoidal_cycle(step, amp, freq)
        #print price
        equities = volume * price
        total_assets = equities + money # once we know the price, we know how much our total assets are worth
        prop = equities / total_assets
        # if the proportion is not ideal, then rebalance
        #if prop > ideal_prop: # then we need to sell enough so that we get back to the ideal proportion
        # first we need to calculate how many equities to sell that will set the balance right
        ideal_equities = total_assets * ideal_prop
        
        eq_diff = ideal_equities - equities # how much money I'm putting up
        # now make up the difference
        
        amount_buying = eq_diff / price # the number of equities I'm buying
        #print "price: %f, eq_diff: %f, amount_buying: %f" % (price, eq_diff, amount_buying)
        volume = volume + amount_buying # buying/selling the equities
        money = money - eq_diff # rebalance the money
        equities = volume * price
        total_assets = equities + money
        
        print "money: %f, volume: %f, price: %f, prop: %f, total_assets: %f, eq_diff: %f" % (money, volume, price, prop, total_assets, eq_diff)
    
    

`
