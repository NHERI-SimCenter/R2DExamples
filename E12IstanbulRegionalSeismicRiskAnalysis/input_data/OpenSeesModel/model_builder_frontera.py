#Modules for generating OpenSees
#Author: Peng-Yu Chen
#Date: 04/22/2021

#import packages
import pandas as pd
import numpy as np
import os

class Modeler(object):
    def __init__(self, buildID, outputpath, number_floor, number_span, span_length, floor_height, floor_area):
        self.BuildID = buildID
        self.output = outputpath
        self.number_floor = number_floor
        self.floor_height = floor_height
        self.number_span = number_span
        self.span_length = span_length
        self.floor_area = floor_area

    def main_process(self):
        #Modeling tcl
        filename = self.output+'/Build_frame.tcl'
        with open(filename, 'w') as tclfile:
            tclfile.write("# This file will be used to define all configurations. \n\n")

            #Basic setup
            tclfile.write("#SET UP \n")
            tclfile.write("wipe; \n")
            tclfile.write("model\tBasicBuilder\t-ndm\t%i\t-ndf\t%i; #Define degree of freedom\n" % (3,6))
            #tclfile.write("set\tdataDir\t$GMdir/Data; #Set output folder\n")
            tclfile.write("set\tdataDir\t./; #Set output folder\n") # KZ: changed to the current dir
            #tclfile.write("file\tmkdir\t$dataDir; #Create output folder\n") # KZ: commented
            #tclfile.write("set\tGMdir\t\"GMfiles\"; #Set GM file folder\n") # KZ: commented
            tclfile.write("source\tLibUnits.tcl; #Define units\n")
            tclfile.write("source\tBuildRCrectSection.tcl; #Define fiber section\n\n")

            #Frame Configuration
            tclfile.write("#Frame Configuration\n")
            tclfile.write("set\tNStory\t%i; #Define number of stories\n" %(self.number_floor))
            tclfile.write("set\tNBay\t%i; #Define number of spans in x direction\n" %(self.number_span))
            tclfile.write("set\tNBayZ\t%i; #Define number of spans in z direction\n" %(self.number_span))
            tclfile.write("set\tNFrame\t[expr\t$NBayZ + 1];\n\n")

            #Define geometry
            tclfile.write("#Frame Geometry\n")
            tclfile.write("set\tLCol\t[expr %i*$ft]; #Floor height\n" %(self.floor_height))
            tclfile.write("set\tLBeam\t[expr %i*$ft]; #Span length in x direction\n" %(self.span_length))
            tclfile.write("set\tLGird\t[expr %i*$ft]; #Span length in z direction\n\n" %(self.span_length))

            #Define nodal coordinate
            tclfile.write("#Define nodal coordinates\n")
            tclfile.write("set\tDlevel 10000; #numbering increment for new-level nodes\n")
            tclfile.write("set\tDframe 100; #numbering increment for new-frame nodes\n")
            tclfile.write("for\t{set\tframe\t1}\t{$frame\t<=[expr\t$NFrame]}\t{incr\tframe 1}\t{\n")
            tclfile.write("\tset\tZ\t[expr\t($frame-1)*$LGird];\n")
            tclfile.write("\tfor\t{set\tlevel 1}\t{$level <=[expr\t$NStory+1]}\t{incr\tlevel 1}\t{\n")
            tclfile.write("\t\tset\tY\t[expr\t($level-1)*$LCol];\n")
            tclfile.write("\t\tfor\t{set pier 1} {$pier <=[expr $NBay+1]} {incr pier 1} {\n")
            tclfile.write("\t\t\tset\tX\t[expr\t($pier-1)*$LBeam];\n")
            tclfile.write("\t\t\tset\tnodeID\t[expr\t$level*$Dlevel+$frame*$Dframe+$pier];\n")
            tclfile.write("\t\t\tnode\t$nodeID\t$X\t$Y\t$Z;\n")
            tclfile.write("\t\t};\n")
            tclfile.write("\t};\n")
            tclfile.write("};\n\n")

            #Rigid diaphragm
            tclfile.write("#Defin rigid diaphragm nodes\n")
            tclfile.write("set RigidDiaphragm ON ;\n")
            tclfile.write("set Xa [expr ($NBay*$LBeam)/2];\n")
            tclfile.write("set Za [expr ($NFrame-1)*$LGird/2];\n")
            tclfile.write("set iMasterNode \"\";\n")
            tclfile.write("for {set level 2} {$level <=[expr $NStory+1]} {incr level 1} {\n")
            tclfile.write("\tset Y [expr ($level-1)*$LCol];\n")
            tclfile.write("\t # rigid-diaphragm nodes in center of each diaphragm\n")
            tclfile.write("\tset MasterNodeID [expr 9900+$level];\n")
            tclfile.write("\tnode $MasterNodeID $Xa $Y $Za;\n")
            tclfile.write("\tfix $MasterNodeID 0  1  0  1  0  1;\n")
            tclfile.write("\tlappend iMasterNode $MasterNodeID\n")
            tclfile.write("\tset perpDirn 2;\n")
            tclfile.write("\tfor {set frame 1} {$frame <=[expr $NFrame]} {incr frame 1} {\n")
            tclfile.write("\t\tfor {set pier 1} {$pier <= [expr $NBay+1]} {incr pier 1} {\n")
            tclfile.write("\t\t\tset nodeID [expr $level*$Dlevel+$frame*$Dframe+$pier]\n")
            tclfile.write("\t\t\trigidDiaphragm $perpDirn $MasterNodeID $nodeID;\n")
            tclfile.write("\t\t}\n")
            tclfile.write("\t}\n")
            tclfile.write("}\n\n")

            #Ground motion input node
            tclfile.write("#Determine support nodes where ground motions are input\n")
            tclfile.write("set iSupportNode \"\"\n")
            tclfile.write("for {set frame 1} {$frame <=[expr $NFrame]} {incr frame 1} {\n")
            tclfile.write("\tset level 1\n")
            tclfile.write("\tfor {set pier 1} {$pier <= [expr $NBay+1]} {incr pier 1} {\n")
            tclfile.write("\t\tset nodeID [expr $level*$Dlevel+$frame*$Dframe+$pier]\n")
            tclfile.write("\t\tlappend iSupportNode $nodeID\n")
            tclfile.write("\t}\n")
            tclfile.write("}\n\n")

            #Boundary Conditions
            tclfile.write("#BOUNDARY CONDITIONS\n")
            #tclfile.write("fixY 0.0  1 1 1 0 1 0; #pin all Y=0.0 nodes\n\n")
            #KZ: update/correction from Wenyang
            tclfile.write("#fixY 0.0  1 1 1 0 1 0; #pin all Y=0.0 nodes\n\n")

            #EqualDOF
            tclfile.write("set origin [lindex $iSupportNode 0];\n")
            tclfile.write("fix $origin 1 1 1 1 1 1;\n")
            tclfile.write("for {set ii 1} {$ii < [llength $iSupportNode]} {incr ii 1} {\n")
            tclfile.write("\tset nodeId [lindex $iSupportNode $ii];\n")
            tclfile.write("\tequalDOF $origin $nodeId 1 2 3 4 5 6;\n")
            tclfile.write("};\n")

            #Define fiber section
            tclfile.write("#Define section tag\n")
            tclfile.write("set ColSecTag 1;\n")
            tclfile.write("set BeamSecTag 2;\n")
            tclfile.write("set GirdSecTag 3;\n")
            tclfile.write("set ColSecTagFiber 4;\n")
            tclfile.write("set BeamSecTagFiber 5;\n")
            tclfile.write("set GirdSecTagFiber 6;\n")
            tclfile.write("set SecTagTorsion 70;\n\n")

            #Define section properties
            tclfile.write("#Define Section Properties \n")
            tclfile.write("set HCol [expr 18*$in];\n")
            tclfile.write("set BCol $HCol;\n")
            tclfile.write("set HBeam [expr 24*$in];\n")
            tclfile.write("set BBeam [expr 18*$in];\n")
            tclfile.write("set HGird [expr 24*$in];\n")
            tclfile.write("set BGird [expr 18*$in];\n\n")

            #Define section input variables
            tclfile.write("#Define section mateial geometry and variables \n")
            tclfile.write("#MATERIAL parameters\n")
            tclfile.write("source LibMaterialsRC.tcl;\n")
            tclfile.write("# Column section geometry\n")
            tclfile.write("set cover [expr 2.5*$in];\n")
            tclfile.write("set numBarsTopCol 8;\n")
            tclfile.write("set numBarsBotCol 8;\n")
            tclfile.write("set numBarsIntCol 6;\n")
            tclfile.write("set barAreaTopCol [expr 1.*$in*$in];\n")
            tclfile.write("set barAreaBotCol [expr 1.*$in*$in];\n")
            tclfile.write("set barAreaIntCol [expr 1.*$in*$in];\n\n")

            tclfile.write("set numBarsTopBeam 6;\n")
            tclfile.write("set numBarsBotBeam 6;\n")
            tclfile.write("set numBarsIntBeam 2;\n")
            tclfile.write("set barAreaTopBeam [expr 1.*$in*$in];\n")
            tclfile.write("set barAreaBotBeam [expr 1.*$in*$in];\n")
            tclfile.write("set barAreaIntBeam [expr 1.*$in*$in];\n\n")

            tclfile.write("set numBarsTopGird 6;\n")
            tclfile.write("set numBarsBotGird 6;\n")
            tclfile.write("set numBarsIntGird 2;\n")
            tclfile.write("set barAreaTopGird [expr 1.*$in*$in];\n")
            tclfile.write("set barAreaBotGird [expr 1.*$in*$in];\n")
            tclfile.write("set barAreaIntGird [expr 1.*$in*$in];\n\n")

            tclfile.write("set nfCoreY 12;\n")
            tclfile.write("set nfCoreZ 12;\n")
            tclfile.write("set nfCoverY 8;\n")
            tclfile.write("set nfCoverZ 8;\n\n")

            tclfile.write("# rectangular section with one layer of steel evenly distributed around the perimeter and a confined core.\n")
            tclfile.write("BuildRCrectSection $ColSecTagFiber $HCol $BCol $cover $cover $IDconcCore  $IDconcCover $IDSteel $numBarsTopCol $barAreaTopCol $numBarsBotCol $barAreaBotCol $numBarsIntCol $barAreaIntCol  $nfCoreY $nfCoreZ $nfCoverY $nfCoverZ\n")
            tclfile.write("BuildRCrectSection $BeamSecTagFiber $HBeam $BBeam $cover $cover $IDconcCore  $IDconcCover $IDSteel $numBarsTopBeam $barAreaTopBeam $numBarsBotBeam $barAreaBotBeam $numBarsIntBeam $barAreaIntBeam  $nfCoreY $nfCoreZ $nfCoverY $nfCoverZ\n")
            tclfile.write("BuildRCrectSection $GirdSecTagFiber $HGird $BGird $cover $cover $IDconcCore  $IDconcCover $IDSteel $numBarsTopGird $barAreaTopGird $numBarsBotGird $barAreaBotGird $numBarsIntGird $barAreaIntGird  $nfCoreY $nfCoreZ $nfCoverY $nfCoverZ\n\n")

            tclfile.write("#Assign torsional Stiffness for 3D Model\n")
            tclfile.write("uniaxialMaterial Elastic $SecTagTorsion $Ubig\n")
            tclfile.write("section Aggregator $ColSecTag $SecTagTorsion T -section $ColSecTagFiber\n")
            tclfile.write("section Aggregator $BeamSecTag $SecTagTorsion T -section $BeamSecTagFiber\n")
            tclfile.write("section Aggregator $GirdSecTag $SecTagTorsion T -section $GirdSecTagFiber\n\n")

            tclfile.write("set GammaConcrete [expr 150*$pcf];\n")
            tclfile.write("set QdlCol [expr $GammaConcrete*$HCol*$BCol];\n")
            tclfile.write("set QBeam [expr $GammaConcrete*$HBeam*$BBeam];\n")
            tclfile.write("set QGird [expr $GammaConcrete*$HGird*$BGird];\n\n")

            #Define Element
            tclfile.write("#Define Elements\n")
            tclfile.write("set IDColTransf 1; # all columns\n")
            tclfile.write("set IDBeamTransf 2; # all beams\n")
            tclfile.write("set IDGirdTransf 3; # all girds\n")
            tclfile.write("set ColTransfType Linear ;\n")
            tclfile.write("geomTransf $ColTransfType  $IDColTransf  0 0 1;\n")
            tclfile.write("geomTransf Linear $IDBeamTransf 0 0 1\n")
            tclfile.write("geomTransf Linear $IDGirdTransf 1 0 0\n\n")

            #Columns
            tclfile.write("#Columns\n")
            tclfile.write("set numIntgrPts 5;\n")
            tclfile.write("set N0col [expr 10000-1];\n")
            tclfile.write("set level 0\n")
            tclfile.write("for {set frame 1} {$frame <=[expr $NFrame]} {incr frame 1} {\n")
            tclfile.write("\tfor {set level 1} {$level <=$NStory} {incr level 1} {\n")
            tclfile.write("\t\tfor {set pier 1} {$pier <= [expr $NBay+1]} {incr pier 1} {\n")
            tclfile.write("\t\t\tset elemID [expr $N0col  +$level*$Dlevel + $frame*$Dframe+$pier]\n")
            tclfile.write("\t\t\tset nodeI [expr  $level*$Dlevel + $frame*$Dframe+$pier]\n")
            tclfile.write("\t\t\tset nodeJ  [expr  ($level+1)*$Dlevel + $frame*$Dframe+$pier]\n")
            tclfile.write("\t\t\telement dispBeamColumn $elemID $nodeI $nodeJ $numIntgrPts $ColSecTag $IDColTransf;# columns\n")
            tclfile.write("\t\t}\n")
            tclfile.write("\t}\n")
            tclfile.write("}\n\n")

            #Beams
            tclfile.write("#Beams\n")
            tclfile.write("set N0beam 1000000;\n")
            tclfile.write("for {set frame 1} {$frame <=[expr $NFrame]} {incr frame 1} {\n")
            tclfile.write("\tfor {set level 2} {$level <=[expr $NStory+1]} {incr level 1} {\n")
            tclfile.write("\t\tfor {set bay 1} {$bay <= $NBay} {incr bay 1} {\n")
            tclfile.write("\t\t\tset elemID [expr $N0beam +$level*$Dlevel + $frame*$Dframe+ $bay]\n")
            tclfile.write("\t\t\tset nodeI [expr $level*$Dlevel + $frame*$Dframe+ $bay]\n")
            tclfile.write("\t\t\tset nodeJ  [expr $level*$Dlevel + $frame*$Dframe+ $bay+1]\n")
            tclfile.write("\t\t\telement dispBeamColumn $elemID $nodeI $nodeJ $numIntgrPts $BeamSecTag $IDBeamTransf;# beams\n")
            tclfile.write("\t\t}\n")
            tclfile.write("\t}\n")
            tclfile.write("}\n\n")

            #Girder
            tclfile.write("#Girders\n")
            tclfile.write("set N0gird 2000000;  # gird element numbers\n")
            tclfile.write("for {set frame 1} {$frame <=[expr $NFrame-1]} {incr frame 1} {\n")
            tclfile.write("\tfor {set level 2} {$level <=[expr $NStory+1]} {incr level 1} {\n")
            tclfile.write("\t\tfor {set bay 1} {$bay <= $NBay+1} {incr bay 1} {\n")
            tclfile.write("\t\t\tset elemID [expr $N0gird + $level*$Dlevel +$frame*$Dframe+ $bay]\n")
            tclfile.write("\t\t\tset nodeI [expr   $level*$Dlevel + $frame*$Dframe+ $bay]\n")
            tclfile.write("\t\t\tset nodeJ  [expr  $level*$Dlevel + ($frame+1)*$Dframe+ $bay]\n")
            tclfile.write("\t\t\telement dispBeamColumn $elemID $nodeI $nodeJ $numIntgrPts $GirdSecTag $IDGirdTransf;# Girds\n")
            tclfile.write("\t\t}\n")
            tclfile.write("\t}\n")
            tclfile.write("}\n\n")

            #Define gravity
            tclfile.write("#Define GRAVITY LOADS, weight and masses\n")
            tclfile.write("set Tslab [expr 6*$in];\n")
            tclfile.write("set Lslab [expr $LGird/2];\n")
            tclfile.write("set DLfactor 1.2;\n")
            tclfile.write("set Qslab [expr $GammaConcrete*$Tslab*$Lslab*$DLfactor]; \n")
            tclfile.write("set QdlBeam [expr $Qslab + $QBeam];\n")
            tclfile.write("set QdlGird $QGird;\n")
            tclfile.write("set WeightCol [expr $QdlCol*$LCol];\n")
            tclfile.write("set WeightBeam [expr $QdlBeam*$LBeam];\n")
            tclfile.write("set WeightGird [expr $QdlGird*$LGird];\n")
            tclfile.write("set iFloorWeight \"""\"\n")
            tclfile.write("set WeightTotal 0.0\n")
            tclfile.write("set sumWiHi 0.0;\n\n")

            tclfile.write("for {set frame 1} {$frame <=[expr $NFrame]} {incr frame 1} {\n")
            tclfile.write("\tif {$frame == 1 || $frame == $NFrame}  {\n")
            tclfile.write("\t\tset GirdWeightFact 1;\n")
            tclfile.write("\t} else {\n")
            tclfile.write("\t\tset GirdWeightFact 2;\n")
            tclfile.write("\t}\n")
            tclfile.write("\tfor {set level 2} {$level <=[expr $NStory+1]} {incr level 1} { ;\n")
            tclfile.write("\t\tset FloorWeight 0.0\n")
            tclfile.write("\t\tif {$level == [expr $NStory+1]}  {\n")
            tclfile.write("\t\t\tset ColWeightFact 1;\n")
            tclfile.write("\t\t} else {\n")
            tclfile.write("\t\t\tset ColWeightFact 2;\n")
            tclfile.write("\t\t}\n")
            tclfile.write("\t\tfor {set pier 1} {$pier <= [expr $NBay+1]} {incr pier 1} {;\n")
            tclfile.write("\t\t\tif {$pier == 1 || $pier == [expr $NBay+1]} {\n")
            tclfile.write("\t\t\t\tset BeamWeightFact 1;\n")
            tclfile.write("\t\t\t} else {;\n")
            tclfile.write("\t\t\t\tset BeamWeightFact 2;\n")
            tclfile.write("\t\t\t}\n")
            tclfile.write("\t\t\tset WeightNode [expr $ColWeightFact*$WeightCol/2 + $BeamWeightFact*$WeightBeam/2 + $GirdWeightFact*$WeightGird/2]\n")
            tclfile.write("\t\t\tset MassNode [expr $WeightNode/$g];\n")
            tclfile.write("\t\t\tset nodeID [expr $level*$Dlevel+$frame*$Dframe+$pier]\n")
            tclfile.write("\t\t\tmass $nodeID $MassNode 0.1 $MassNode 0.1 0.1 0.1;\n")
            tclfile.write("\t\t\tset FloorWeight [expr $FloorWeight+$WeightNode];\n")
            tclfile.write("\t\t}\n")
            tclfile.write("\t\tlappend iFloorWeight $FloorWeight\n")
            tclfile.write("\t\tset WeightTotal [expr $WeightTotal+ $FloorWeight]\n")
            tclfile.write("\t\tset sumWiHi [expr $sumWiHi+$FloorWeight*($level-1)*$LCol];\n")
            tclfile.write("\t}\n")
            tclfile.write("}\n")
            tclfile.write("set MassTotal [expr $WeightTotal/$g];\n\n")

            #Eigen analysis
            tclfile.write("#Eigenvalue analysis\n")
            tclfile.write("set numModes 2\n")
            tclfile.write("set lambda [eigen  $numModes];\n")
            tclfile.write("set omega {}\n")
            tclfile.write("set f {}\n")
            tclfile.write("set T {}\n")
            tclfile.write("set pi 3.141593\n")
            tclfile.write("foreach lam $lambda {\n")
            tclfile.write("\tlappend omega [expr sqrt($lam)]\n")
            tclfile.write("\tlappend f [expr sqrt($lam)/(2*$pi)]\n")
            tclfile.write("\tlappend T [expr (2*$pi)/sqrt($lam)]\n")
            tclfile.write("}\n")
            #tclfile.write("puts \"periods are $T\"\n\n")

            #recorder
            tclfile.write("#Write all recorders\n")
            tclfile.write("#Define all nodes\n")
            tclfile.write("set SupportNodeFirst [lindex $iSupportNode 0];\n")
            if self.number_floor>1:
                for i in range(2,self.number_floor+2):
                    tclfile.write("set NodeID_%i [expr $NFrame*$Dframe+(%i)*$Dlevel+($NBay+1)];\n" %(i,i))
                tclfile.write("\n#Drift\n")
                tclfile.write("recorder Drift -file $dataDir/NodeDrift_2_x.out -time -iNode $SupportNodeFirst  -jNode $NodeID_2 -dof 1 -perpDirn 2;\n")
                tclfile.write("recorder Drift -file $dataDir/NodeDrift_2_y.out -time -iNode $SupportNodeFirst  -jNode $NodeID_2 -dof 3 -perpDirn 2;\n")
                tclfile.write("recorder EnvelopeDrift -file $dataDir/NodeDriftEnv_2_x.out -iNode $SupportNodeFirst  -jNode $NodeID_2 -dof 1 -perpDirn 2;\n")
                tclfile.write("recorder EnvelopeDrift -file $dataDir/NodeDriftEnv_2_y.out -iNode $SupportNodeFirst  -jNode $NodeID_2 -dof 3 -perpDirn 2;\n")
                for i in range(3,self.number_floor+2):
                    tclfile.write("recorder Drift -file $dataDir/NodeDrift_%i_x.out -time -iNode $NodeID_%i -jNode $NodeID_%i -dof 1 -perpDirn 2;\n"%(i,i-1,i))
                    tclfile.write("recorder Drift -file $dataDir/NodeDrift_%i_y.out -time -iNode $NodeID_%i -jNode $NodeID_%i -dof 3 -perpDirn 2;\n"%(i,i-1,i))
                    tclfile.write("recorder EnvelopeDrift -file $dataDir/NodeDriftEnv_%i_x.out -iNode $NodeID_%i -jNode $NodeID_%i -dof 1 -perpDirn 2;\n"%(i,i-1,i))
                    tclfile.write("recorder EnvelopeDrift -file $dataDir/NodeDriftEnv_%i_y.out -iNode $NodeID_%i -jNode $NodeID_%i -dof 3 -perpDirn 2;\n"%(i,i-1,i))
            else:
                tclfile.write("set NodeID_2 [expr $NFrame*$Dframe+(2)*$Dlevel+($NBay+1)];\n")
                tclfile.write("recorder Drift -file $dataDir/NodeDrift_2_x.out -time -iNode $SupportNodeFirst  -jNode $NodeID_2 -dof 1 -perpDirn 2;\n")
                tclfile.write("recorder Drift -file $dataDir/NodeDrift_2_y.out -time -iNode $SupportNodeFirst  -jNode $NodeID_2 -dof 3 -perpDirn 2;\n")
                tclfile.write("recorder EnvelopeDrift -file $dataDir/NodeDriftEnv_2_x.out -iNode $SupportNodeFirst  -jNode $NodeID_2 -dof 1 -perpDirn 2;\n")
                tclfile.write("recorder EnvelopeDrift -file $dataDir/NodeDriftEnv_2_y.out -iNode $SupportNodeFirst  -jNode $NodeID_2 -dof 3 -perpDirn 2;\n")

            tclfile.write("\n#Write Node Acceleration\n")
            for i in range(2, self.number_floor+2):
                tclfile.write("recorder\tNode\t-file")
                tclfile.write("\t$dataDir/NodeAcceleration_%i.out" % i)
                tclfile.write("\t-time\t-node")
                tclfile.write("\t$NodeID_%i" % (i))
                tclfile.write("\t-dof\t1\t3\taccel; \n")

                tclfile.write("recorder\tEnvelopeNode\t-file")
                tclfile.write("\t$dataDir/NodeAccelerationEnv_%i_x.out" % i)
                tclfile.write("\t-node")
                tclfile.write("\t$NodeID_%i" % (i))
                tclfile.write("\t-dof\t1\taccel; \n")

                tclfile.write("recorder\tEnvelopeNode\t-file")
                tclfile.write("\t$dataDir/NodeAccelerationEnv_%i_y.out" % i)
                tclfile.write("\t-node")
                tclfile.write("\t$NodeID_%i" % (i))
                tclfile.write("\t-dof\t3\taccel; \n")

            #Gravity
            tclfile.write("\n#Gravity analysis\n")
            tclfile.write("pattern Plain 101 Linear {\n")
            tclfile.write("\tfor {set frame 1} {$frame <=[expr $NFrame]} {incr frame 1} {\n")
            tclfile.write("\t\tfor {set level 1} {$level <=$NStory} {incr level 1} {\n")
            tclfile.write("\t\t\tfor {set pier 1} {$pier <= [expr $NBay+1]} {incr pier 1} {\n")
            tclfile.write("\t\t\t\tset elemID [expr $N0col  + $level*$Dlevel +$frame*$Dframe+$pier]\n")
            tclfile.write("\t\t\t\teleLoad -ele $elemID -type -beamUniform 0. 0. -$QdlCol;\n")
            tclfile.write("\t\t\t}\n")
            tclfile.write("\t\t}\n")
            tclfile.write("\t}\n")
            tclfile.write("\tfor {set frame 1} {$frame <=[expr $NFrame]} {incr frame 1} {\n")
            tclfile.write("\t\tfor {set level 2} {$level <=[expr $NStory+1]} {incr level 1} {\n")
            tclfile.write("\t\t\tfor {set bay 1} {$bay <= $NBay} {incr bay 1} {\n")
            tclfile.write("\t\t\t\tset elemID [expr $N0beam + $level*$Dlevel +$frame*$Dframe+ $bay]\n")
            tclfile.write("\t\t\t\teleLoad -ele $elemID  -type -beamUniform -$QdlBeam 0.;\n")
            tclfile.write("\t\t\t}\n")
            tclfile.write("\t\t}\n")
            tclfile.write("\t}\n")
            tclfile.write("\tfor {set frame 1} {$frame <=[expr $NFrame-1]} {incr frame 1} {\n")
            tclfile.write("\t\tfor {set level 2} {$level <=[expr $NStory+1]} {incr level 1} {\n")
            tclfile.write("\t\t\tfor {set bay 1} {$bay <= $NBay+1} {incr bay 1} {\n")
            tclfile.write("\t\t\t\tset elemID [expr $N0gird + $level*$Dlevel +$frame*$Dframe+ $bay]\n")
            tclfile.write("\t\t\t\teleLoad -ele $elemID  -type -beamUniform -$QdlGird 0.;\n")
            tclfile.write("\t\t\t}\n")
            tclfile.write("\t\t}\n")
            tclfile.write("\t}\n")
            tclfile.write("}\n\n")


            tclfile.write("set Tol 1.0e-8;\n")
            tclfile.write("variable constraintsTypeGravity Plain;\n")
            tclfile.write("if {  [info exists RigidDiaphragm] == 1} {\n")
            tclfile.write("\tif {$RigidDiaphragm==\"ON\"} {\n")
            tclfile.write("\t\tvariable constraintsTypeGravity Lagrange;\n")
            tclfile.write("\t};\n")
            tclfile.write("};\n")
            tclfile.write("constraints $constraintsTypeGravity;\n")
            tclfile.write("numberer RCM;\n")
            tclfile.write("system UmfPack;\n")#BandGeneral
            tclfile.write("test EnergyIncr $Tol 6;\n")
            tclfile.write("algorithm Newton;\n")
            tclfile.write("set NstepGravity 10;\n")
            tclfile.write("set DGravity [expr 1./$NstepGravity];\n")
            tclfile.write("integrator LoadControl $DGravity;\n")
            tclfile.write("analysis Static;\n")
            tclfile.write("analyze $NstepGravity;\n\n")

            tclfile.write("loadConst -time 0.0\n\n")

            #tclfile.write("puts \"Model Build\";\n")

            tclfile.close()

            #Dynamic Analysis TCLs
            filename = self.output+'/DynamicAnalysis.tcl'
            with open(filename, 'w') as tclfile:
                tclfile.write("# This file will be used to run time history analysis. \n\n")
                tclfile.write("# source file \n")
                # KZ: adding source the model file
                tclfile.write("source Build_frame.tcl; \n")
                tclfile.write("source LibAnalysisDynamicParameters.tcl; \n\n")

                tclfile.write("# Define ground motions file and direction. \n")
                h1 = str(self.BuildID+5824)+"_1"
                v = str(self.BuildID+5824)+"_2"
                h2 = str(self.BuildID+5824)+"_3"
                #tclfile.write("set iGMfile \"%s %s %s\";\n" %(h1,v,h2))
                #tclfile.write("set iGMdirection \"%s %s %s\";\n" %(1,2,3))
                #tclfile.write("set iGMfact \"%s %s %s\";\n\n" %(100,100,100))
                # KZ: modifying for user-provided records
                tclfile.write("set iGMfile ##iGMfile##;\n")
                tclfile.write("set iGMdirection ##iGMdirection##;\n")
                tclfile.write("set iGMfact ##iGMfact##;\n\n")

                tclfile.write("# set up ground motion analysis parameters\n")
                #tclfile.write("set DtAnalysis [expr 0.01*$sec];\n")
                #tclfile.write("set TmaxAnalysis [expr 30. *$sec];\n")
                #tclfile.write("set dt 0.01;\n\n")
                # KZ: modifying for user-provided records
                tclfile.write("set DtAnalysis ##DtAnalysis##;\n")
                tclfile.write("set TmaxAnalysis ##TmaxAnalysis##;\n")
                tclfile.write("set dt ##dt##;\n\n")

                tclfile.write("# Define damping\n")
                tclfile.write("set xDamp 0.02;\n")
                tclfile.write("set MpropSwitch 1.0;\n")
                tclfile.write("set KcurrSwitch 0.0;\n")
                tclfile.write("set KcommSwitch 1.0;\n")
                tclfile.write("set KinitSwitch 0.0;\n")
                tclfile.write("set nEigenI 1;\n")
                tclfile.write("set nEigenJ 2;\n")
                tclfile.write("set lambdaN [eigen [expr $nEigenJ]];\n")
                tclfile.write("set lambdaI [lindex $lambdaN [expr $nEigenI-1]];\n")
                tclfile.write("set lambdaJ [lindex $lambdaN [expr $nEigenJ-1]];\n")
                tclfile.write("set omegaI [expr pow($lambdaI,0.5)];\n")
                tclfile.write("set omegaJ [expr pow($lambdaJ,0.5)];\n")
                tclfile.write("set alphaM [expr $MpropSwitch*$xDamp*(2*$omegaI*$omegaJ)/($omegaI+$omegaJ)];\n")
                tclfile.write("set betaKcurr [expr $KcurrSwitch*2.*$xDamp/($omegaI+$omegaJ)];\n")
                tclfile.write("set betaKcomm [expr $KcommSwitch*2.*$xDamp/($omegaI+$omegaJ)];\n")
                tclfile.write("set betaKinit [expr $KinitSwitch*2.*$xDamp/($omegaI+$omegaJ)];\n")
                tclfile.write("rayleigh $alphaM $betaKcurr $betaKinit $betaKcomm;\n\n")

                tclfile.write("# performance dynamic analysis\n")
                tclfile.write("set IDloadTag 400;\n")
                tclfile.write("foreach GMdirection $iGMdirection GMfile $iGMfile GMfact $iGMfact {\n")
                tclfile.write("\tincr IDloadTag;\n")
                tclfile.write("\tset outFile $GMfile;\n")
                tclfile.write("\tset GMfatt [expr $GMfact];\n")
                #tclfile.write("\tset AccelSeries \"Series -dt $dt -filePath $outFile -factor    $GMfatt\";\n")
                #KZ: factors are already applied in the EVENT.json
                tclfile.write("\tset AccelSeries \"Series -dt $dt -filePath $outFile\";\n")
                tclfile.write("\tpattern UniformExcitation  $IDloadTag  $GMdirection -accel $AccelSeries;\n")
                tclfile.write("}\n\n")

                tclfile.write("set Nsteps [expr int($TmaxAnalysis/$DtAnalysis)];\n")
                tclfile.write("set ok [analyze $Nsteps $DtAnalysis];\n\n")

                tclfile.write("if {$ok != 0} {;\n")
                tclfile.write("\tset ok 0;\n")
                tclfile.write("\tset controlTime [getTime];\n")
                tclfile.write("\twhile {$controlTime < $TmaxAnalysis && $ok == 0} {\n")
                tclfile.write("\t\tset controlTime [getTime]\n")
                tclfile.write("\t\tset ok [analyze 1 $DtAnalysis]\n")
                tclfile.write("\t\tif {$ok != 0} {\n")
                #tclfile.write("\t\t\tputs \"Trying Newton with Initial Tangent ..\"\n")
                tclfile.write("\t\t\ttest NormDispIncr  $Tol 1000  0\n")
                tclfile.write("\t\t\talgorithm Newton -initial\n")
                tclfile.write("\t\t\tset ok [analyze 1 $DtAnalysis]\n")
                tclfile.write("\t\t\ttest $testTypeDynamic $TolDynamic $maxNumIterDynamic  0\n")
                tclfile.write("\t\t\talgorithm $algorithmTypeDynamic\n")
                tclfile.write("\t\t}\n")
                tclfile.write("\t\tif {$ok != 0} {\n")
                #tclfile.write("\t\t\tputs \"Trying Broyden ..\"\n")
                tclfile.write("\t\t\talgorithm Broyden 8\n")
                tclfile.write("\t\t\tset ok [analyze 1 $DtAnalysis]\n")
                tclfile.write("\t\t\talgorithm $algorithmTypeDynamic\n")
                tclfile.write("\t\t}\n")
                tclfile.write("\t\tif {$ok != 0} {\n")
                #tclfile.write("\t\t\tputs \"Trying NewtonWithLineSearch ..\"\n")
                tclfile.write("\t\t\talgorithm NewtonLineSearch .8\n")
                tclfile.write("\t\t\tset ok [analyze 1 $DtAnalysis]\n")
                tclfile.write("\t\t\talgorithm $algorithmTypeDynamic\n")
                tclfile.write("\t\t}\n")
                tclfile.write("\t}\n")
                tclfile.write("}\n\n")
                tclfile.write("wipe\tall")
                #tclfile.write("puts \"Ground Motion Done. End Time: [getTime]\";\n")
                tclfile.close()































