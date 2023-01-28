# --------------------------------------------------------------------------------------------------
# LibUnits.tcl -- define system of units
#		Silvia Mazzoni & Frank McKenna, 2006
#

# define UNITS ----------------------------------------------------------------------------
set cm 1.;				# define basic units -- output units
set kgf 1.;				# define basic units -- output units
set sec 1.; 			# define basic units -- output units
set m [expr $cm*100];
set tf [expr $kgf*1000]
set in [expr $cm*2.54]; 				# define basic units -- output units
set kip [expr $tf*0.45]; 			# define basic units -- output units

set LunitTXT "cm";			# define basic-unit text for output
set FunitTXT "kgf";			# define basic-unit text for output
set TunitTXT "sec";			# define basic-unit text for output

set ft [expr 12.*$in]; 		# define engineering units
set ksi [expr $kip/pow($in,2)];
set psi [expr $ksi/1000.];
set lbf [expr $psi*$in*$in];		# pounds force
set pcf [expr $lbf/pow($ft,3)];		# pounds per cubic foot
set psf [expr $lbf/pow($ft,3)];		# pounds per square foot
set in2 [expr $in*$in]; 		# inch^2
set in4 [expr $in*$in*$in*$in]; 		# inch^4
set PI [expr 2*asin(1.0)]; 		# define constants
set g [expr 32.2*$ft/pow($sec,2)]; 	# gravitational acceleration
set Ubig 1.e10; 			# a really large number
set Usmall [expr 1/$Ubig]; 		# a really small number
