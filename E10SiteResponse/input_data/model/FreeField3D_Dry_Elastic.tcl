# ##########################################################
#                                                         #
# 3D site response analysis of a soil deposit on an       #
# elastic half-space.  Shaking is applied in a single     #
# plane, and the site has a slope out of the plane of     #
# shaking.  The finite rigidity of the underlying medium  #
# is considered through the use of a viscous damper at    #
# the base of the soil column.                            #
#                                                         #
#   Created by:  Chris McGann                             #
#                Pedro Arduino                            #
#              --University of Washington--               #
#                                                         #
#   Revamped by Alborz Ghofrani                           #
#                                                         #
###########################################################

wipe


# ------------------------------------------------
#  1. SETUP THE MODEL
# ------------------------------------------------
# site response configuration file


# general constants
set g     -9.81
set pi     3.141592654

# -----------------------------------------------------------------------------------------
#  1.1 DEFINE GEOMETRY
# -----------------------------------------------------------------------------------------
source freefield_config.tcl
# grade of slope (%)
set grade           0.0

# depth of water table
set waterTable      0.0

# -----------------------------------------------------------------------------------------
#  1.2 DEFINE FINITE ELEMENT MESH
# -----------------------------------------------------------------------------------------

# number of elements in horizontal direction
set nElemX  1
set nElemZ  1

# horizontal element size
set sElemX  1.0
set sElemZ  1.0

# -----------------------------------------------------------------------------------------
#  1.3 DEFINE MOTION
# -----------------------------------------------------------------------------------------

# number of directions for application of the motion
set numDir 1

# define motion time step
set useMotionDT true
# set motionDT 1000.0; # used if useMotionDT is false

# define base
set isRigidBase false

# if compliant define the base (used if isRigidBase is false)
set rockVP  3000.0

# -----------------------------------------------------------------------------------------
#  1.4. MODEL
# -----------------------------------------------------------------------------------------

# effective/total stress
set isEffetive false

# choose element type
set IsSSP true 

# RAYLEIGH DAMPING PARAMETERS
set damp    0.02
# set omega1  [expr 2.0 * $pi * 1.0]	
# set omega2  [expr 2.0 * $pi * 10.0]	

# set omega1  14.83	
# set omega2  74.14

# recorder time step
set useMotionDTforRec false
set recDT  0.001; # used if useMotionDTforRec is false

# -----------------------------------------------------------------------------------------
#  1.4 ANALYSIS OPTIONS
# -----------------------------------------------------------------------------------------

# gravity analysis
set grav_cons    "Penalty 1.0e15 1.0e15"
set grav_test    "NormDispIncr 1e-5 30 1"
set grav_algo    "KrylovNewton"
set grav_numb    "Plain"
set grav_syst    "SparseGeneral"
set grav_intg    "Newmark [expr 5.0/6.0] [expr 4.0/9.0]"
set grav_anls    "Transient"

set grav_elasticAnalysisDT 500.0
set grav_elasticAnalysisNo 20
set grav_plasticAnalysisDT 5.0e-2
set grav_plasticAnalysisNo 40


# transient analysis
set trans_cons    "Penalty 1.0e15 1.0e15"
set trans_test   "NormDispIncr 5.0e-6 30 1"
set trans_algo   "Newton"
set trans_numb   "Plain"
set trans_syst    "SparseGeneral"
set trans_intg   "Newmark 0.5 0.25"
set trans_anls   "Transient"


# number of nodes/elements in vertical direction in each layer
set nNodeT 0
set nElemT 0
for {set k 1} {$k < $numLayers} {incr k 1} {
    set nNodeY($k)  [expr 4*$nElemY($k)]
    puts "number of nodes in layer $k: $nNodeY($k)"
    set nNodeT  [expr $nNodeT + $nNodeY($k)]
	set nElemT  [expr $nElemT + $nElemY($k)]
}
set nNodeY($numLayers) [expr 4*($nElemY($numLayers) + 1)]
puts "number of nodes in layer $numLayers: $nNodeY($numLayers)"

set nNodeT  [expr $nNodeT + $nNodeY($numLayers)]
set nElemT  [expr $nElemT + $nElemY($numLayers)]
puts "total number of nodes:    $nNodeT"
puts "total number of elements: $nElemT"

# ------------------------------------------------
#  2. CREATE SOIL NODES AND BOUNDARY CONDITIONS
# ------------------------------------------------

model BasicBuilder -ndm 3 -ndf 3

set yCoord  0.0 
set count   0
set nodesInfo [open nodesInfo.dat w]
# loop over layers
for {set k 1} {$k <= $numLayers} {incr k 1} {
	# loop over nodes
	for {set j 1} {$j <= $nNodeY($k)} {incr j 4} {
		node  [expr $j+$count]    0.0      $yCoord  0.0
		node  [expr $j+$count+1]  0.0      $yCoord  $sElemZ
		node  [expr $j+$count+2]  $sElemX  $yCoord  $sElemZ
		node  [expr $j+$count+3]  $sElemX  $yCoord  0.0

		puts $nodesInfo "[expr $j+$count]    0.0      $yCoord  0.0"
		puts $nodesInfo "[expr $j+$count+1]  0.0      $yCoord  $sElemZ"
		puts $nodesInfo "[expr $j+$count+2]  $sElemX  $yCoord  $sElemZ"
		puts $nodesInfo "[expr $j+$count+3]  $sElemX  $yCoord  0.0"

		set yCoord  [expr $yCoord + $sElemY($k)]
	}
	set count  [expr $count + $nNodeY($k)]
}
close $nodesInfo
puts "Finished creating all soil nodes..."

fix 1 1 1 1 0
fix 2 0 1 0 0
fix 3 0 1 0 0
fix 4 0 1 0 0

equalDOF  1 2 1 3
equalDOF  1 3 1 3
equalDOF  1 4 1 3

# define periodic boundary conditions for remaining nodes
set count  0
for {set k 5} {$k <= [expr $nNodeT]} {incr k 4} {
	fix $k 0 1 0
	equalDOF  $k  [expr $k+1]  1 2 3
	equalDOF  $k  [expr $k+2]  1 2 3
	equalDOF  $k  [expr $k+3]  1 2 3
	puts "equalDOF  $k  [expr $k+1]  1 2 3"
	puts "equalDOF  $k  [expr $k+2]  1 2 3"
	puts "equalDOF  $k  [expr $k+3]  1 2 3"
}

puts "Finished creating all soil boundary conditions..."


# --------------------------------
#  4. CREATE SOIL MATERIALS
# --------------------------------

set slope [expr atan($grade/100.0)]

source freefield_material.tcl

set xWgt  [expr $g*sin($slope)]
set yWgt  [expr $g*cos($slope)]
set zWgt  0.0

for {set k 1} {$k <= $numLayers} {incr k} {
	eval "nDMaterial $mat($k)"
}
puts "Finished creating all soil materials..."

# ---------------------------------------
#  5. CREATE SOIL ELEMENTS
# ---------------------------------------
# set alpha value for SSP element
set count 0
set elemInfo [open elementInfo.dat w]

# loop over layers 
for {set k 1} {$k <= $numLayers} {incr k 1} {
    # loop over elements
    for {set j 1} {$j <= $nElemY($k)} {incr j 1} {
        set nI  [expr 4*($j+$count) - 3] 
        set nJ  [expr $nI + 1]
        set nK  [expr $nI + 2]
        set nL  [expr $nI + 3]
		set nM  [expr $nI + 4]
		set nN  [expr $nI + 5]
		set nO  [expr $nI + 6]
		set nP  [expr $nI + 7]
		if {$IsSSP} {
			element SSPbrick [expr $j+$count] $nI $nJ $nK $nL $nM $nN $nO $nP $k [expr $rho($k)*$xWgt] [expr $rho($k)*$yWgt] $zWgt
			puts $elemInfo "[expr $j+$count] $nI $nJ $nK $nL $nM $nN $nO $nP $k"
		} else {
			element stdBrick [expr $j+$count] $nI $nJ $nK $nL $nM $nN $nO $nP $k [expr $rho($k)*$xWgt] [expr $rho($k)*$yWgt] $zWgt
			puts $elemInfo "[expr $j+$count] $nI $nJ $nK $nL $nM $nN $nO $nP $k"
		}
		
	}
	set count [expr $count + $nElemY($k)]
}
close $elemInfo
puts "Finished creating all soil elements..."

# -----------------------------------------------------
#  8. CREATE GID FLAVIA.MSH FILE FOR POSTPROCESSING
# -----------------------------------------------------
 
set meshFile [open freeField3D.flavia.msh w]
puts $meshFile "MESH ffBrick dimension 3 ElemType Hexahedra Nnode 8"
puts $meshFile "Coordinates"
puts $meshFile "#node_number   coord_x   coord_y   coord_z"
set yCoord  0.0 
set count   0

# loop over layers
for {set k 1} {$k <= $numLayers} {incr k 1} {
	# loop over nodes
	for {set j 1} {$j <= $nNodeY($k)} {incr j 4} {
		puts $meshFile  "[expr $j+$count]    0.0      $yCoord  0.0"
		puts $meshFile  "[expr $j+$count+1]  0.0      $yCoord  $sElemZ"
		puts $meshFile  "[expr $j+$count+2]  $sElemX  $yCoord  $sElemZ"
		puts $meshFile  "[expr $j+$count+3]  $sElemX  $yCoord  0.0"

		set yCoord  [expr $yCoord + $sElemY($k)]
	}
	set count  [expr $count + $nNodeY($k)]
}
puts $meshFile "end coordinates"
puts $meshFile "Elements"
puts $meshFile "# element   node1   node2   node3   node4   node5   node6   node7   node8"
set count 0

# loop over layers 
for {set k 1} {$k <= $numLayers} {incr k 1} {
    # loop over elements
    for {set j 1} {$j <= $nElemY($k)} {incr j 1} {

        set nI  [expr 4*($j+$count) - 3] 
        set nJ  [expr $nI + 1]
        set nK  [expr $nI + 2]
        set nL  [expr $nI + 3]
		set nM  [expr $nI + 4]
		set nN  [expr $nI + 5]
		set nO  [expr $nI + 6]
		set nP  [expr $nI + 7]

        puts $meshFile  "[expr $j+$count] $nI $nJ $nK $nL $nM $nN $nO $nP"
    }
    set count [expr $count + $nElemY($k)]
}
puts $meshFile "end elements"
close $meshFile

# ---------------------------
#  7. GRAVITY RECORDERS
# ---------------------------

# record nodal displacments, velocities, and accelerations at each time step
recorder Node -file GdisplacementElasAct.out -time  -nodeRange 1 $nNodeT -dof 1 2 3 disp
recorder Node -file GvelocityElasAct.out     -time  -nodeRange 1 $nNodeT -dof 1 2 3 vel
recorder Node -file GaccelerationElasAct.out -time  -nodeRange 1 $nNodeT -dof 1 2 3 accel
recorder Node -file GreactionElasAct.out     -time  -nodeRange 1 $nNodeT -dof 1 2 3 4 reaction

# record stress and strain at each gauss point in the soil elements
if {$IsSSP} {	
	recorder Element -file Gstress2.out   -time  -eleRange  1   $nElemT  stress 6
	recorder Element -file Gstrain2.out   -time  -eleRange  1   $nElemT  strain
} else {
	recorder Element -file Gstress1.out   -time  -eleRange  1   $nElemT  material 1 stress 6
	recorder Element -file Gstress2.out   -time  -eleRange  1   $nElemT  material 2 stress 6
	recorder Element -file Gstress3.out   -time  -eleRange  1   $nElemT  material 3 stress 6
	recorder Element -file Gstress4.out   -time  -eleRange  1   $nElemT  material 4 stress 6
	recorder Element -file Gstress5.out   -time  -eleRange  1   $nElemT  material 5 stress 6
	recorder Element -file Gstress6.out   -time  -eleRange  1   $nElemT  material 6 stress 6
	recorder Element -file Gstress7.out   -time  -eleRange  1   $nElemT  material 7 stress 6
	recorder Element -file Gstress8.out   -time  -eleRange  1   $nElemT  material 8 stress 6
	
	recorder Element -file Gstrain1.out   -time  -eleRange  1   $nElemT  material 1 strain 
	recorder Element -file Gstrain2.out   -time  -eleRange  1   $nElemT  material 2 strain 
	recorder Element -file Gstrain3.out   -time  -eleRange  1   $nElemT  material 3 strain 
	recorder Element -file Gstrain4.out   -time  -eleRange  1   $nElemT  material 4 strain 
	recorder Element -file Gstrain5.out   -time  -eleRange  1   $nElemT  material 5 strain 
	recorder Element -file Gstrain6.out   -time  -eleRange  1   $nElemT  material 6 strain 
	recorder Element -file Gstrain7.out   -time  -eleRange  1   $nElemT  material 7 strain 
	recorder Element -file Gstrain8.out   -time  -eleRange  1   $nElemT  material 8 strain 
}
puts "Finished creating gravity recorders..."


# -------------------------
#  7. GRAVITY ANALYSIS
# -------------------------

# damping coefficients
# set a0      [expr 2*$damp*$omega1*$omega2/($omega1 + $omega2)]
# set a1      [expr 2*$damp/($omega1 + $omega2)]
set a0      0.0
set a1      0.0005
puts "damping coefficients: a_0 = $a0;  a_1 = $a1"

# update materials to consider elastic behavior
for {set k 1} {$k <= $numLayers} {incr k} {
    updateMaterialStage -material $k -stage 0
}

eval "constraints $grav_cons "
eval "test        $grav_test "
eval "algorithm   $grav_algo"
eval "numberer    $grav_numb"
eval "system      $grav_syst"
eval "integrator  $grav_intg  "
eval "rayleigh    $a0  $a1 0.0 0.0"
eval "analysis    $grav_anls"

set startT  [clock seconds]
if {$grav_anls == "Static"} {
	analyze $grav_elasticAnalysisNo
} else {
	analyze $grav_elasticAnalysisNo $grav_elasticAnalysisDT
}

puts "Finished with elastic gravity analysis..."

## update materials to consider plastic behaviour
#for {set k 1} {$k <= $numLayers} {incr k} {
#    updateMaterialStage -material $k -stage 1
#}
#
#
## plastic gravity loading
#if {$grav_anls == "Static"} {
#	analyze $grav_plasticAnalysisNo
#} else {
#	analyze $grav_plasticAnalysisNo $grav_plasticAnalysisDT
#}

puts "Finished with plastic gravity analysis..."

# -------------------------------------
#  8. CREATE POST-GRAVITY RECORDERS
# -------------------------------------
# reset time and analysis
setTime 0.0
wipeAnalysis
remove recorders

## record nodal displacments, velocities, and accelerations at each time step
recorder Node -file displacementElasAct.out -time -dT $recDT  -nodeRange 1 $nNodeT -dof 1 2 3 disp
recorder Node -file velocityElasAct.out     -time -dT $recDT  -nodeRange 1 $nNodeT -dof 1 2 3 vel
recorder Node -file accelerationElasAct.out -time -dT $recDT  -nodeRange 1 $nNodeT -dof 1 2 3 accel

recorder Node -file acceleration.out -time  -nodeRange 1 $nNodeT -dof 1 2 3 accel

# record stress and strain at each gauss point in the soil elements
if {$IsSSP} {
	recorder Element -file stressElasAct.out   -time -dT $recDT -eleRange  1   $nElemT  stress 6
	recorder Element -file strainElasAct.out   -time -dT $recDT -eleRange  1   $nElemT  strain
} else {
	recorder Element -file stress1.out  -time -dT $recDT -eleRange  1   $nElemT  material 1 stress 6
	recorder Element -file stress2.out  -time -dT $recDT -eleRange  1   $nElemT  material 2 stress 6
	recorder Element -file stress3.out  -time -dT $recDT -eleRange  1   $nElemT  material 3 stress 6
	recorder Element -file stress4.out  -time -dT $recDT -eleRange  1   $nElemT  material 4 stress 6
	recorder Element -file stress5.out  -time -dT $recDT -eleRange  1   $nElemT  material 5 stress 6
	recorder Element -file stress6.out  -time -dT $recDT -eleRange  1   $nElemT  material 6 stress 6
	recorder Element -file stress7.out  -time -dT $recDT -eleRange  1   $nElemT  material 7 stress 6
	recorder Element -file stress8.out  -time -dT $recDT -eleRange  1   $nElemT  material 8 stress 6

	recorder Element -file strain1.out  -time -dT $recDT -eleRange  1   $nElemT  material 1 strain
	recorder Element -file strain2.out  -time -dT $recDT -eleRange  1   $nElemT  material 2 strain
	recorder Element -file strain3.out  -time -dT $recDT -eleRange  1   $nElemT  material 3 strain
	recorder Element -file strain4.out  -time -dT $recDT -eleRange  1   $nElemT  material 4 strain
	recorder Element -file strain5.out  -time -dT $recDT -eleRange  1   $nElemT  material 5 strain
	recorder Element -file strain6.out  -time -dT $recDT -eleRange  1   $nElemT  material 6 strain
	recorder Element -file strain7.out  -time -dT $recDT -eleRange  1   $nElemT  material 7 strain
	recorder Element -file strain8.out  -time -dT $recDT -eleRange  1   $nElemT  material 8 strain
}
puts "Finished creating post-gravity recorders..."


# ------------------------------------
#  9. DEFINE DYNAMIC ANALYSIS PARAMETERS
# ------------------------------------


# read the motion
set channel [open $timeFile r]
set timeVec [split [read -nonewline $channel] \n]
set motionSteps [llength $timeVec]
set motionLen [lindex $timeVec [expr $motionSteps - 1]]
if {$useMotionDT} {
	set t1 [lindex $timeVec 0]
	set t2 [lindex $timeVec 1]
	set motionDT [expr $t2 - $t1]
} else {
	set motionSteps [expr int($motionLen / $motionDT)]
}
close $channel
puts "Number of motion steps: $motionSteps"
puts "Motion time step: $motionDT"
puts "Motion length: $motionLen"


# 4.1 Set basic properties of the base. 

set colThickness 1.0
set colArea [expr $sElemX*$colThickness]
set rockDen 2.5
set dashpotCoeff  [expr $rockVs*$rockDen]
uniaxialMaterial Viscous [expr $numLayers + 1] [expr $dashpotCoeff*$colArea] 1
set cFactor [expr $colArea*$dashpotCoeff]

node [expr $nP + 1] 0.0 0.0 0.0
node [expr $nP + 2] 0.0 0.0 0.0
node [expr $nP + 3] 0.0 0.0 0.0

fix [expr $nP + 1] 1 1 1
fix [expr $nP + 2] 0 1 1
fix [expr $nP + 3] 1 1 0

# 4.3 Apply equalDOF to the node connected to the column. 

equalDOF 1 [expr $nP + 2] 1
equalDOF 1 [expr $nP + 3] 3
remove sp 1 1
remove sp 1 3


# 4.5 Create the dashpot element. 

element zeroLength [expr $numLayers + 1] [expr $nP + 2] [expr $nP + 3] -mat [expr $numLayers + 1]  -dir 1
element zeroLength [expr $numLayers + 2] [expr $nP + 2] [expr $nP + 3] -mat [expr $numLayers + 1]  -dir 3

# ------------------------------------------------------------
# 5.1 Apply the rock motion                                    
# ------------------------------------------------------------


set mSeries "Path -dt $motionDT -filePath xInput.vel -factor $cFactor"
pattern Plain 10 $mSeries {
    load 1  1.0 0.0 0.0
}
if {$numEvt == 2} {
	set mSeriesx2 "Path -dt $motionDT -filePath yInput.vel -factor $cFactor"
	pattern Plain 11 $mSeriesx2 {
		load 1  0.0 0.0 1.0
	}
}


# # timeseries object for force history
# set mSeries1 "Path -fileTime $timeFile -filePath $dispFile2"
# if {$numEvt == 2} {
# 	set mSeries2 "Path -fileTime $timeFile -filePath $dispFile2"
# }
# # loading object
# # pattern UniformExcitation 10 1 -accel $mSeries
# 
# proc nodeLoadMSE {dof tag} {
# 
# 	# maingrid
# 	for {set j 1} {$j<= 4} {incr j 1} {
# 		imposedMotion $j $dof $tag 
# 		puts "imposedMotion $j $dof $tag "
# 	}
# 		
# }
# 	
# pattern MultipleSupport 10 {
# 	groundMotion 1 Plain -disp $mSeries1 [nodeLoadMSE 1 1]
# 	if {$numEvt == 2} {
# 		groundMotion 2 Plain -disp $mSeries2 [nodeLoadMSE 2 2]
# 	}
# }

	
puts "Dynamic loading created..."

eval "constraints $trans_cons "
eval "test        $trans_test "
eval "algorithm   $trans_algo"
eval "numberer    $trans_numb"
eval "system      $trans_syst"
eval "integrator  $trans_intg  "
eval "rayleigh    $a0  0.0 $a1 0.0"
eval "analysis    $trans_anls"


# Set number and length of (pseudo)time steps
set numStep $motionSteps
set dT 	    $motionDT

# Analyze and use substepping if needed
set remStep $numStep
set success 0
proc subStepAnalyze {dT subStep} {
        if {$subStep > 10} {
                return -10
        }
        for {set i 1} {$i < 3} {incr i} {
                puts "Try dT = $dT"
                set success [analyze 1 $dT]
                if {$success != 0} {
                        set success [subStepAnalyze [expr $dT/2.0] [expr $subStep+1]]
                        if {$success == -10} {
                                puts "Did not converge."
                                return $success
                        }
                } else {
                        if {$i==1} {
                                puts "Substep $subStep : Left side converged with dT = $dT"
                        } else {
                                puts "Substep $subStep : Right side converged with dT = $dT"
                        }
                }
        }
        return $success
}

puts "Start analysis"
set startT [clock seconds]

while {$success != -10} {
        set subStep 0
        set success [analyze $remStep  $dT]
        if {$success == 0} {
                puts "Analysis Finished"
                break
        } else {
                set curTime  [getTime]
                puts "Analysis failed at $curTime . Try substepping."
                set success  [subStepAnalyze [expr $dT/2.0] [incr subStep]]
        set curStep  [expr int($curTime/$dT + 1)]
        set remStep  [expr int($numStep-$curStep)]
                puts "Current step: $curStep , Remaining steps: $remStep"
        }
}
set endT [clock seconds]
puts "loading analysis execution time: [expr $endT-$startT] seconds."

wipe
