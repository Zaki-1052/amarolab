# Generate expanse gpu script.py

import os import sys from typing import Optional """ Module that can be used to make input scripts for Expanse GPU simulations. """ 

class ExpanseGpuSimulationParameters(object): 
    
    
       """
       Class that holds the parameters required to generate a GPU
       simulation script for the Expanse supercomputer at SDSC.
    
    
    
       Parameters
       ----------
       account_number : int
           Expanse account number
    
    
    
       gpu_partition : str
           GPU partition that the simulation is run on.
    
    
    
       num_tasks_per_node : int
           Number of tasks that are performed on each
           GPU node.
    
    
    
       memory : int
           Amount of memory that is allocated for the 
           simulation.
    
    
    
       num_gpus : int
           Number of gpus that are used to run the 
           simulation.
    
    
    
       num_nodes : int
           Number of gpu nodes that are used to run the 
           simulation.
    
    
    
       simulation_time : str
           Maxiumum amount of time that the simulation
           is allowed to run for. If the simulation 
           excedes this time, expanse will kill it :(.
    
    
    
       simulation_commands : str
           Commands that are required to run the simulation.
           Each line of commands is input as it's own string.
    
    
    
       output_name : str, optional
           Root name for both the output log file and the 
           simulation input script. 
    
    
    
       memory_unit : str, optional
           Unit that memory is defined in.
           Defaults to gigabytes (G). 
    
    
    
       output_extension : str, optional
           File extension of the output file.
           Defaults to log.
       
       simulation_index : int, optional
           Used to add an index suffix to the simulation
           script name. This is usually defined when 
           the user wants to create multiple simulation
           scripts that share the same stem part of the 
           script name.
       
       path : str, optional
           Simulation script path. By default the script is written
           to the current working directory.
           Defaults to ./
       
       """
       def __init__(
               self,
               account_number: int,
               gpu_partition: str,
               num_nodes: int,
               num_tasks_per_node: int,
               memory: int,
               num_gpus: int,
               simulation_time: str,
               output_name: str,
               *simulation_commands: str,
               memory_unit: Optional[str] = 'G',        
               output_extension: Optional[str] = 'log',        
               simulation_index: Optional[int] = _,_
               path: Optional[str] = './'
               ) -> None:
           self.account_number = account_number
           self.gpu_partition = gpu_partition
           self.num_nodes = num_nodes
           self.num_tasks_per_node = num_tasks_per_node
           self.memory = memory
           self.num_gpus = num_gpus
           self.simulation_time = simulation_time 
           self.output_name = output_name
           self.simulation_commands = simulation_commands
           self.memory_unit = memory_unit      
           self.output_extension = output_extension        
           self.simulation_index = simulation_index 
           self.simulation_index = simulation_index 
           self.path = path
    

  


  


def _make_expanse_gpu_simulation_script( 
    
    
           params: ExpanseGpuSimulationParameters,
           ) -> str:
       """
       Returns the string representation of an Expanse GPU
       simulation script.
    
    
    
       Parameters
       ----------
       params : ExpanseGpuSimulationParameters
           Instance of ExpanseGpuSimulationParameters which holds 
           all the necessary parameters required to generate an
           Expanse GPU simulation script.
    
    
    
       Returns
       -------
       script : str
           String representation of an Expanse GPU simulation script.
    
    
    
       """
       script = "#!/usr/bin/env bash\n\
       #SBATCH --job-name=14-rep3\n\
       #SBATCH --account=csd" + str(params.account_number) + "\n\
       #SBATCH --partition=" + str(params.gpu_partition) + "\n\
       #SBATCH --nodes=" + str(params.num_nodes) + "\n\
       #SBATCH --ntasks-per-node=" + str(params.num_tasks_per_node) + "\n\
       #SBATCH --mem=" + str(params.memory) + str(params.memory_unit) + "\n\
       #SBATCH --gpus=" + str(params.num_gpus) + "\n\
       #SBATCH --time=" + str(params.simulation_time) + "\n\
       #SBATCH --output=" + str(params.output_name) \
       + "." + str(params.output_extension) + "\n\
       \n\
       module purge\n\
       module load gpu\n\
       module load cpu/0.15.4\n\
       module load gcc/7.5.0\n\
       module load cuda10.2/blas/10.2.89\n\
       module load cuda10.2/fft/10.2.89\n\
       module load cuda10.2/nsight/10.2.89\n\
       module load cuda10.2/profiler/10.2.89\n\
       module load cuda10.2/toolkit/10.2.89\n\
       \n\
       export OPENMM_INSTALL_DIR=$HOME/bin/openmm\n\
       export OPENMM_LIB_PATH=$OPENMM_INSTALL_DIR/lib\n\
       export OPENMM_INCLUDE_PATH=$OPENMM_INSTALL_DIR/include\n\
       export OPENMM_PLUGIN_DIR=$OPENMM_LIB_PATH/plugins\n\
       export OPENMM_CUDA_COMPILER=$CUDA_ROOT/bin/nvcc\n\
       export LD_LIBRARY_PATH=$OPENMM_LIB_PATH:$OPENMM_PLUGIN_DIR:$LD_LIBRARY_PATH\n\
       export CUDA_CUDA_LIBRARY=$CUDA_ROOT/lib64/stubs/libcuda.so\n\
       \n"
       for line in params.simulation_commands:
           script += str(line) + "\n"
       script = script.replace('    ', _)_
       return script
    

def make_expanse_gpu_simulation_script( 
    
    
           params: ExpanseGpuSimulationParameters,
           ) -> None:
       """
       Generates an Expanse GPU simulation script using the string 
       returned by _make_expanse_gpu_simulation_script.
    
    
    
       Parameters
       ----------
       params : ExpanseGpuSimulationParameters
           Instance of ExpanseGpuSimulationParameters which holds 
           all the necessary parameters required to generate an
           Expanse GPU simulation script.
    
    
    
       Returns
       -------
           None
    
    
    
       Examples
       --------
       >>> sim_command1 = "cd /home/astokely/bin/openmmvt/openmmvt"
       >>> sim_commnand2 = "python prepare_1d_spherical.py " + str(5)
           + " /expanse/lustre/scratch/astokely/"
           + "temp_project/trypsin_benzamidine/model.xml"
       >>> params = ExpanseGpuSimulationParameters(
           373, 'gpu-shared', 4, 
           10, 93, 4, '48:00:00', 
           '1-butanol', sim_command1, sim_command2
       )
       >>> make_expanse_gpu_simulation_script(params)
       >>> #Run the simulation by typing "sbatch 'output_name'
           #in the terminal.
    
    
    
       """
       with open(
           str(params.path) 
           + str(params.output_name 
           + str(params.simulation_index)), 'w+'
       ) as simulation_script:
           simulation_script.write(_make_expanse_gpu_simulation_script(
               params
           ))
           simulation_script.close()
