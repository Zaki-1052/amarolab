# Gamess.py

#BY ANDY STOKELY
    #GAMESS AUTOMATION SCRIPT THAT EXECUTES GAMESS INPUT FILES AND DELETES RESIDUAL GAMESS FILES FOLLOWING A FAILED SIMULATION
    
    import os
    import re
    import pwd
    import random
    
    def sim(input_name, path):
    
    	
    	#The input name (str) is the name of the .inp file.
    	#The path (str) is the path where the .inp file is located.
    	
    
    	check_path = os.listdir(path)
    	old_runs = []
    	for sim_file in check_path:
    		old_runs.append(sim_file)
    	for sim_file in old_runs:
    		if input_name in sim_file:
    			os.system('rm' + ' ' +path+input_name+'.log')
    			os.system('cd /tmp/ ; rm *' + input_name + '*')
    	def find_gamess(path):
    		os.system('locate /gamess/rungms | tee _/tmp/In_this_crazy_world_of_choices_Ive_only_got_a_few_Either_youre_coming_with_me_or_Im_coming_with_you_Cause_I_finally_found_I_finally_found_you.txt > /dev/null')_
    		with open('/tmp/In_this_crazy_world_of_choices_Ive_only_got_a_few_Either_youre_coming_with_me_or_Im_coming_with_you_Cause_I_finally_found_I_finally_found_you.txt', 'r+') as gamess_path:
    			rungms_path = gamess_path.readlines()
    			gamess_path.close()
                    global rungms
    		rungms = rungms_path[0]
    		rungms = str(rungms)
    		return 
    	find_gamess(path)
    	print(rungms)
    	run_gamess = os.system(rungms + ' ' + input_name + ' ' + '>&' + ' ' + input_name + '.log')
    	gamess_output = open(path + input_name + '.log')
    	log = gamess_output.readlines()
    	gamess_output.close()
    	error_tracker = []
    	for line in log:
    		if 'error' in line:
    			error_tracker.append('errors')
    	if len(error_tracker) > 0:
    		os.system('rm' + ' '  + path + input_name + '.log')
    		os.system('cd ' + path + ' ; rm *' + input_name + '* ')		
    	else:
    		pass
    	return
    
    
    #sim('carb', '/home/astokely/quantum/')
