# Drawing vectors

This page will walk you through how to draw vectors in your system. To draw vectors you will be working in your VMD TkConsole. For your SEEKR simulation you will want to draw vectors coming out of the center of the indices. Assuming you know the correct residue IDs, you can create a variable to store these values by typing: 
    
    
    set site [atomselect 0 "name CA and redid 35 42 77 91 122 168 169"]
    

  
Make sure that the number typed after atomselect is the ID of your molecule in VMD and that the resid numbers are specific to your simulation. After creating a variable that holds your indices, you can set the origin at the center of these points by typing: 
    
    
    set origin [measure center $site]
    

  
The word written after the $ should be the variable you defined to store your indices. This command will set the origin at the center of your indices and it will return the coordinates of this point. After defining the origin you will be able to draw it in your system. To do this type: 
    
    
    draw color green
    draw sphere $origin radius 1.0
    

  
It is important to indicate what color you want VMD to draw, because you will have multiple vectors and it will be easier to tell them apart if they are different colors. This command will draw a green sphere of radius 1.0 at the origin of your system. Next, you will want to draw vectors coming out of the origin. To do this you will source eye_vec.tcl into your console. 
    
    
    source ~/scripts/eye_vec.tcl
    

  
To draw a vector, the command is simple. Type eye_vec followed by the variable of the origin: 
    
    
    eye_vec $origin
    

  
This will give you a vector coming out of the origin and will return the coordinates of the vector. 

  
For your SEEKR simulation you will need at least two sequential vectors coming out of the origin. To add a sequential vector type: 
    
    
    set vec1 "coordinates of the origin"
    set vec1_normed [vecnorm $vec1]
    set vec1_4 [vecscale $vec_normed 4.0]
    set step1 [vecadd $origin $vec1_4]
    draw color blue
    draw sphere $step1 radius 1.0
    eye_vec $step1
    

  
The first line of this command sets the variable vec1 to hold the coordinates of the origin. Make sure that you copy the coordinates of the origin into the quotes of this command. The second line sets the variable vec1_normed to the vector of the origin shortened to one unit. The third line sets the variable vec1_4 to the coordinates 4 units away from the origin. The forth line adds vec1_4 to the origin and sets it to the variable step1. After changing the color, you draw a new sphere 4 units away from the origin in the sixth line of the command. Finally, you can get the second sequential vector by using the command in the seventh line. 

  
This will give you enough vectors for your SEEKR simulation, but you can add vectors as many times as you want.
