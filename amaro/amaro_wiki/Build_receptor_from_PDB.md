# Build receptor from PDB

## Compute salinity from triclinic box vector[edit](</mediawiki/index.php?title=Build_receptor_from_PDB&action=edit&section=1> "Edit section: Compute salinity from triclinic box vector")]

The length of a side of the triclinic box can be found by using the following formulas. 

Assuming that the length of the triclinic (truncated octahedral) box is "a". You can find "a" as the first number in the last line of the inpcrd file. 

First, the volume of the box in L = a^3 * 0.768979 * 10^-27 

Next, find the number of salt molecules that go in: # molecules = 6.022*10^23 * desired molarity * volume of box in Liters 

Next, multiply the number of salt molecules times the number of moles of each ion per dissolved salt molecule. (For NaCl, this is just 1 for both Na+ and Cl-) 

Example calculation: 

I want to use physiological salinity of 0.15M. 

The last line in the inpcrd file is: 
    
    
    83.9827776  83.9827776  83.9827776 109.4712190 109.4712190 109.4712190
    

Volume in Liters = (83.9827776^3) * 0.768979 * 10^-27 = 4.5549662 * 10^-22 

salt molecules = 41.145009 

We can round down to 41. There will be 41 Na+ and 41 Cl-. 

## Compute Triclinic box vectors from .RST7 file[edit](</mediawiki/index.php?title=Build_receptor_from_PDB&action=edit&section=2> "Edit section: Compute Triclinic box vectors from .RST7 file")]

See this page for additional reference (<https://lammps.sandia.gov/doc/Howto_triclinic.html>). 

Assume that your .rst7 (.inpcrd) file is named "myfile.rst7". Type: 
    
    
    tail myfile.rst7
    

You should see something like the following: 
    
    
    ...
      44.0005374  57.4933941  -9.9067969  36.2571155  57.3778598  -6.1570097
      35.5071375  57.9167476  -5.9024512  36.6000616  57.8016216  -6.9433124
      36.2045766  57.5007426  -6.2255990
     101.9105962 101.9105962 101.9105962 109.4712190 109.4712190 109.4712190
    

You want the final numbers in this file. Let's label them "a", "b", "c", "alpha", "beta", "gamma". 

In particular, the number "101.9105962"; the number 'a' 

The first vector is simply this number in the 'x' position, with zeros in the 'y' and 'z' positions. 
    
    
    [101.9105962, 0, 0]
    

The next vector is the length 'b' times cos(gamma) = cos(109.4712190) = -0.33333333*b in degrees for 'x', and the length 'b' times sin(gamma) = sin(109.4712190) = 0.9428090511*b in degrees for 'y', and 0.0 for 'z' 
    
    
    [-33.97019599, 96.0822325, 0.0]
    

The next vector is the length 'c' times cos(beta) = cos(109.4712190) = -0.33333333*c in degrees for 'x' again. Then length 'c' times(cos(alpha) - cos(beta)*cos(gamma))/sin(gamma) 

which equals 'c' times (cos(109.4712190) - cos(109.4712190)^2)/sin(109.4712190) = -0.4714044685*c for 'y'. Finally, 'z' equals sqrt(a^2 - x^2 - y^2) = 0.8164966221*a 
    
    
    [-33.97019599, -48.04111044, 83.20965755]
    

The units in the parm7 file are in Angstroms. To convert to nm, divide all numbers by 10. 
    
    
    [10.19105962, 0, 0]
    [-3.397019599, 9.60822325, 0.0]
    [-3.397019599, -4.804111044, 8.320965755]
    

  
You can add the following line to your OpenMM script: 
    
    
    simulation.context.setPeriodicBoxVectors((10.19105962, 0, 0), (-3.397019599, 9.60822325, 0.0), (-3.397019599, -4.804111044, 8.320965755)
