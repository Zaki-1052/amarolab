# Make adams tcl code.py

`
    
    
    
    linelist='''set argstr [concat $argstr "-node_definition $::wisp::node_def"]
      set argstr [concat $argstr "-contact_map_distance_distance_limit $::wisp::contact_map_dist"]
      set argstr [concat $argstr "-load_matrix $::wisp::load_matrix"]
      set argstr [concat $argstr "-matrix_filename $::wisp::matrix_filename"]
      set argstr [concat $argstr "-desired_number_of_paths $::wisp::desired_num_paths"]
      set argstr [concat $argstr "-number_processors $::wisp::number_processors"]
      set argstr [concat $argstr "-num_frames_to_load_before_processing $::wisp::num_frames_to_load_b4_proc"]
      set argstr [concat $argstr "-shortest_path_radius $::wisp::shortest_path_radius"]
      set argstr [concat $argstr "-longest_path_radius $::wisp::longest_path_radius"]
      set argstr [concat $argstr "-spline_smoothness $::wisp::spline_smoothness"]
      set argstr [concat $argstr "-vmd_resolution $::wisp::vmd_resolution"]
      set argstr [concat $argstr "-node_sphere_radius $::wisp::node_sphere_radius"]
      set argstr [concat $argstr "-shortest_path_r $::wisp::shortest_path_r -shortest_path_g $::wisp::shortest_path_g -shortest_path_b $::wisp::shortest_path_b"]
      set argstr [concat $argstr "-longest_path_r $::wisp::longest_path_r -longest_path_g $::wisp::longest_path_g -longest_path_b $::wisp::longest_path_b"]
      set argstr [concat $argstr "-shortest_path_opacity $::wisp::shortest_path_opacity -longest_path_opacity $::wisp::longest_path_opacity"]
      set argstr [concat $argstr "-simply_formatted_paths_filename $::wisp::simply_formatted_paths_filename"]
      set argstr [concat $argstr "-seconds_to_wait_before_parallelization_path_finding $::wisp::seconds_to_wait_before_parallelizing_path_finding"]
      set argstr [concat $argstr "-functionalized_correlation_matrix_filename $::wisp::functionalized_correlation_matrix_filename"]
      set argstr [concat $argstr "-contact_map_filename $::wisp::contact_map_filename"]'''
    
    varlist=[]
    
    linelist=linelist.split('\n')
    for line in linelist:
      word_list=line.split()
      for word in word_list:
        if word.startswith("$::"):
          word = word.strip(']').strip('"')
          varlist.append(word)
          
    for var in varlist:
      end = var.split(':')[-1]
      
      
      print '''
    	frame $settings_win.leftcol.%s
    	pack [label $settings_win.leftcol.%s.caption -text "%s"] -side left -anchor w
    	pack [entry $settings_win.leftcol.%s.textbox -width 20 -textvariable ::wisp::%s_temp] -side right -anchor w
    	pack $settings_win.leftcol.%s -side top -anchor w -pady 5
    	''' % (end, end, end, end, end, end)
    	
      #print "\t\tset ::wisp::%s_temp %s" % (end, var)
      
      
    '''
    frame $settings_win.leftcol.wisp_dir
    	pack [label $settings_win.leftcol.wisp_dir.caption -text "WISP location"] -side left -anchor w
    	pack [entry $settings_win.leftcol.wisp_dir.textbox -width 20 -textvariable ::wisp::wispdir_temp] -side right -anchor w
    	pack $settings_win.leftcol.wisp_dir -side top -anchor w -pady 10'''
    
    

`
