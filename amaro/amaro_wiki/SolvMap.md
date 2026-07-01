# SolvMap

Solvent Mapping Using FTMap Web Server: 

  
1\. The web server address is <http://ftmap.bu.edu/home.php>

  
2\. First create an account for yourself using the link at the bottom of the webpage 

  
3\. After you log in with your account, click on the Submit tab. 

  
4\. Upload your pdb file, enter the chain ID in the relevant box, click on the boxes for "Protein Surface Mode" and "Deposit the result in the mapping database". And type in a job name you like before you submit. 

  
5\. You can follow all the jobs you submitted from the Queue tab. (And if you go to the Help tab, there is info about the abbreviations used for the status of your jobs). 

  
6\. Once your job finishes, the results are available to download in the Results tab. 

  
How to Modify Your Pdb File for FTMap: 

  
1\. Make sure that all non-protein atoms have "HETATM", and not "ATOM" in the first column in pdb. 

  
2\. Make sure that all protein residue names are standard residue names (e.g. FTMap doesn't like HIE, HID, HIP, replace all those with HIS). 

  
3\. Make sure you have protein residues hydrogenated properly. (The program doesn't like missing hydrogens.)
