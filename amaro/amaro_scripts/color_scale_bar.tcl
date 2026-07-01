## NAME: color_scale_bar
## 
## SYNOPSIS:
##   color_scale_bar draws a color bar on the screen to show all of the
##   current colors (colorid 17~1040). It also shows labels beside the 
##   color bar to show the range of the mapped values.
##
## VERSION: 1.0
##    Uses VMD version:  VMD Version 1.7 or greater
##    Ease of use: 2. need to understand some Tcl and a bit about how VMD
##                 works
## 
## PROCEDURES:
##      color_scale bar
## 
## DESCRIPTION:
##      To draw a color scale bar with length=1.5, width=0.25, the range of
##      mapped values is 0~128, and you want 8 labels.
##      color_scale_bar 1.5  0.25  0  128 8
## 
## COMMENTS: The size of the bar also depends on the zoom scale.
## 
## AUTHOR:
##      Wuwei Liang (gtg088c@prism.gatech.edu)
## 

# This function draws a color bar to show the color scale
# length = the length of the color bar
# width = the width of the color bar
# min = the minimum value to be mapped
# max = the maximum mapped value
# label_num = the number of labels to be displayed

proc color_scale_bar {length width min max label_num } {

display update off

# draw the color bar
set start_y [expr -0.5 * $length]
set step [expr $length / ([colorinfo max] * 1.0) ]

for {set colorid [colorinfo num] } { $colorid <= [colorinfo max] } {incr colorid 1 } {
	draw color $colorid
	set cur_y [ expr $start_y + ($colorid - [colorinfo num]) * $step ]
	draw line " 0 $cur_y 0 "  " $width  $cur_y  0 "
}

# draw the labels
set coord_x [expr 1.2*$width];
set step_size [expr $length / $label_num]
set color_step [expr ([colorinfo max] * 1.0)/$label_num]
set value_step [expr ($max - $min ) / double ($label_num)]

for {set i 0} {$i <= $label_num } { incr i 1} {

	set cur_color_id white
	draw color $cur_color_id
	set coord_y [expr $start_y+$i * $step_size ]
	set cur_text [expr $min + $i * $value_step ]
	draw text  " $coord_x $coord_y 0"  [format %6.2f  $cur_text]
}

display update on
}
