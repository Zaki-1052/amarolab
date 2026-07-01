# Example input.xml

`
    
    
    
    <root>
    
     <solvent>
        <dielectric> 78 </dielectric>
        <debye-length>  8.01121 </debye-length>
        <kT>1.04</kT>
      </solvent>
    
      <output> results.xml </output>
      <start-at-site>false</start-at-site>
      <trajectory-file>trajectory</trajectory-file>
      <include-desolvation-forces>false</include-desolvation-forces>
      <hydrodynamic-interactions>false</hydrodynamic-interactions>
      <n-trajectories> 500000 </n-trajectories>
      <n-threads> 10 </n-threads>
      <n-steps-per-output> 1000000 </n-steps-per-output>
      <molecule0>
        <prefix> virus </prefix>
        <atoms>  virus.pqrxml </atoms>
        <all-in-surface> false </all-in-surface>
        <apbs-grids>
           <!-- innermost grid is first, followed by outer grids -->
           <grid> virus.dx </grid>
        </apbs-grids>
        <solute-dielectric> 2.0 </solute-dielectric>
      </molecule0>
    
      <molecule1>
        <prefix> ligand </prefix>
        <atoms>  ligand.pqrxml </atoms>
        <all-in-surface> false </all-in-surface>
        <apbs-grids>
           <grid> ligand.dx </grid>
        </apbs-grids>
        <solute-dielectric> 2.0 </solute-dielectric>
      </molecule1>
    
      <time-step-tolerances>
      <minimum-dx> 1.0 </minimum-dx>
      </time-step-tolerances>
      <reactions> rxns.xml </reactions>
    
      <seed> 115631 </seed>
      <n-trajectories-per-output> 200 </n-trajectories-per-output>
    
      <n-copies> 200 </n-copies>
      <n-bin-copies> 200 </n-bin-copies>
      <n-steps> 1000000 </n-steps>
      <n-we-steps-per-output> 1000 </n-we-steps-per-output>
      <max-n-steps> 100000000 </max-n-steps>
    
    </root>
    
    

`
