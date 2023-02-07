#Istanbul Topographic Project Main Script
#Author: Peng-Yu Chen
#Date: 04/22/2021

#import packages
import numpy as np
from mpi4py import MPI
import pandas as pd
import shutil
import os

#import module
import model_builder_frontera


#mpi information
comm = MPI.COMM_WORLD
size = comm.Get_size() #how many core you are using
rank = comm.Get_rank() #assign id to each core

def static_partition(tasks):
    segsize = (len(tasks)+size-1) // size
    start = rank * segsize
    stop = min(len(tasks), start+segsize)
    return tasks[start:stop]

def main():
    Building = pd.read_csv('BIM.csv')
    floor_area = Building['Area_ft2'].values
    number_floor = Building['Floors'].values
    number_blvd = len(Building)
    all_house_id = np.arange(number_blvd)
    i_house_id = static_partition(all_house_id)

    for i in i_house_id:
        dimension = np.floor(np.sqrt(floor_area[i]))
        span_length = 24 #default:24ft
        number_span = int(np.ceil(dimension/span_length))

        folder = os.getcwd()+'/Model/Blvd_'+str(i+1)

        if not os.path.exists(folder):
            os.makedirs(folder)

        outputpath = folder

        model = model_builder_frontera.Modeler(buildID = i,
                                      outputpath = outputpath,
                                      number_floor = number_floor[i],
                                      number_span = number_span,
                                      span_length = span_length,
                                      floor_height = 14,
                                      floor_area = floor_area[i])
        model.main_process()


        #copy TCLs
        source1 = os.getcwd()+'/source/LibUnits.tcl'
        source2 = os.getcwd()+'/source/LibMaterialsRC.tcl'
        source3 = os.getcwd()+'/source/LibAnalysisDynamicParameters.tcl'
        source4 = os.getcwd()+'/source/BuildRCrectSection.tcl'

        #paste TCLs
        shutil.copyfile(source1,os.path.join(outputpath,os.path.basename(source1)))
        shutil.copyfile(source2,os.path.join(outputpath,os.path.basename(source2)))
        shutil.copyfile(source3,os.path.join(outputpath,os.path.basename(source3)))
        shutil.copyfile(source4,os.path.join(outputpath,os.path.basename(source4)))

        #Read GM
        # for gm in range(57):
        for gm in (5, 7):
            GM = folder+'/GMfiles_'+str(gm)
            if not os.path.exists(GM):
                os.makedirs(GM)

            filename = '../Istanbul_sim'+str(gm+1)+'/outputfiles/stations_fullDomain/station.'+str(i+5824)
            data = np.loadtxt(filename)
            h1 = pd.DataFrame(data[:,-2])
            v = pd.DataFrame(data[:,-1])
            h2 = pd.DataFrame(data[:,-3])
           
            path = GM+'/'
            x = path+"/"+str(i+5824)+"_1.txt"
            y = path+"/"+str(i+5824)+"_2.txt"
            z = path+"/"+str(i+5824)+"_3.txt"

            h1.to_csv(x, index=None, header=None)
            v.to_csv(y, index=None, header=None)
            h2.to_csv(z, index=None, header=None)



if __name__=="__main__":
    main()
