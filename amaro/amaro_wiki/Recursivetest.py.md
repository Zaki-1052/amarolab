# Recursivetest.py

`
    
    
    
    def findcombosinset(iset,combolen,depth=0,index=0,triangle=[]):
        '''
        NOTE: nonfunctional
        this function finds all triplet combinations in a set
    
        then returns a list of all combinations
        '''
        setlen = len(iset)
        if depth == 0: #we're just starting
            trianglelist = []
            depth = 0
            
            triangle = []
        
        #depth += 1 #if the depth is zero(top of list) we are not checking element #1
        if (depth == combolen): #then we have three of our elements
            print triangle
            triangle.pop()
            return
        else:
            for i in range(index,setlen):
                triangle.append(iset[i])
                findcombosinset(iset,combolen,depth+1,i+1,triangle)
            if triangle: triangle.pop()
    
    
    newset = ['A','B','C','D','E','F']
    findcombosinset(newset,4)
    
    

`
