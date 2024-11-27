#import packages
import numpy as np
#from mpi4py import MPI
import pandas as pd
import shutil
import os

#import module
import model_builder_frontera


def custom_analysis(AIM, EVENT, SAM, EDP):

    # Modeling parameters from AIM
    dict_GI = AIM.get("GeneralInformation", None)
    if dict_GI is None:
        print('Please check input AIM information, no GeneralInformation found.')
        return 1
    
    floor_area = float(dict_GI.get('PlanArea', 1000))
    number_floor = int(dict_GI.get('NumberOfStories'))
    blvd_id = int(dict_GI.get('AIM_id', "1"))

    # Building model
    dimension = np.floor(np.sqrt(floor_area))
    span_length = 24 #default:24ft
    number_span = int(np.ceil(dimension/span_length))
    folder = os.getcwd()
    outputpath = folder
    inputpath = AIM.get('commonFileDir',folder)
    model = model_builder_frontera.Modeler(buildID = blvd_id,
                                      outputpath = outputpath,
                                      number_floor = number_floor,
                                      number_span = number_span,
                                      span_length = span_length,
                                      floor_height = 14,
                                      floor_area = floor_area)

    model.main_process()

    # Copy TCLs
    source1 = os.path.join(inputpath,'source/LibUnits.tcl')
    source2 = os.path.join(inputpath,'source/LibMaterialsRC.tcl')
    source3 = os.path.join(inputpath,'source/LibAnalysisDynamicParameters.tcl')
    source4 = os.path.join(inputpath,'source/BuildRCrectSection.tcl')
    shutil.copyfile(source1,os.path.join(outputpath,os.path.basename(source1)))
    shutil.copyfile(source2,os.path.join(outputpath,os.path.basename(source2)))
    shutil.copyfile(source3,os.path.join(outputpath,os.path.basename(source3)))
    shutil.copyfile(source4,os.path.join(outputpath,os.path.basename(source4)))

    # Prepare ground motion input
    gm_filename_dir = ['GM_X','GM_Y']
    scaling_fact = []
    for j in range(2):
        gm_filename = gm_filename_dir[j]+'.txt'
        # Extract dt and scale factor for desired ground motion
        dt = EVENT.get('dT', None)
        if dt is None:
            dt = EVENT['timeSeries'][j].get('dT')
        SF = EVENT.get('unitScaleFactor', None)
        if SF is None:
            SF = EVENT['timeSeries'][j].get('factor', 1.0)
        else:
            SF_user = SF.get('TH_file', 1.0)
            SF_unit = SF.get('factor', 1.0)
            SF = SF_user * SF_unit
        scaling_fact.append(SF)
        # Get gm number of points
        npts = EVENT.get('numSteps', None)
        if npts is None:
            npts = EVENT['timeSeries'][j].get('numSteps')
        print('GM written path: ', os.getcwd())
        # dump the GM data to the GM file
        with open(gm_filename, 'w') as f:
            for val in EVENT['timeSeries'][j]['data']:
                f.write(str(val))
                f.write("\n")

    # Prepare analysis script
    template_analysis_script  = 'DynamicAnalysis.tcl'
    iGMfile = "{} {}".format(gm_filename_dir[0]+'.txt', gm_filename_dir[1]+'.txt')
    iGMdirection = "1 3"
    iGMfact = "{} {}".format(scaling_fact[0], scaling_fact[1])
    DtAnalysis = dt
    TmaxAnalysis = npts*dt

    with open(template_analysis_script, 'r') as f:
            data_batch = f.read()
        
    # Replace placeholders
    data_batch = data_batch.replace("##iGMfile##", "{"+iGMfile+"}")
    data_batch = data_batch.replace("##iGMdirection##", "{"+iGMdirection+"}")
    data_batch = data_batch.replace("##iGMfact##", "{"+iGMfact+"}")
    data_batch = data_batch.replace("##DtAnalysis##", str(DtAnalysis))
    data_batch = data_batch.replace("##TmaxAnalysis##", str(TmaxAnalysis))
    data_batch = data_batch.replace("##dt##", str(dt))

    destination_path = os.getcwd()
    with open(os.path.join(destination_path, "DynamicAnalysis.tcl"), 'w') as f:
        f.write(data_batch)
    
    # Run analysis
    os.system('OpenSees DynamicAnalysis.tcl')
    
    # Collect results
    # generating edp names
    edp_names = []
    for i in range(number_floor):
        edp_names.append("1-PID-{}-1".format(i+1))
        edp_names.append("1-PID-{}-2".format(i+1))
        if i == 0:
            edp_names.append("1-PFA-{}-1".format(i))
            edp_names.append("1-PFA-{}-2".format(i))
        edp_names.append("1-PFA-{}-1".format(i+1))
        edp_names.append("1-PFA-{}-2".format(i+1))
        edp_names.append("1-PFD-{}-1".format(i+1))
        edp_names.append("1-PFD-{}-2".format(i+1))
    edp_names.append('1-PRD-1-1')
    edp_names.append('1-PRD-1-2')
    # looping over edps to collect data
    response = []
    for cur_edp in edp_names:
        if 'PID' in cur_edp:
            if int(cur_edp[-1]) == 1:
                cur_record_file = 'NodeDriftEnv_{}_x.out'.format(int(cur_edp[-3]))
            else:
                cur_record_file = 'NodeDriftEnv_{}_y.out'.format(int(cur_edp[-3]))
        elif 'PFA' in cur_edp:
            if int(cur_edp[-1]) == 1:
                cur_record_file = 'NodeAccelerationEnv_{}_x.out'.format(int(cur_edp[-3]))
            else:
                cur_record_file = 'NodeAccelerationEnv_{}_y.out'.format(int(cur_edp[-3]))
        elif 'PFD' in cur_edp:
            if int(cur_edp[-1]) == 1:
                cur_record_file = 'NodeDispEnv_{}_x.out'.format(int(cur_edp[-3]))
            else:
                cur_record_file = 'NodeDispEnv_{}_y.out'.format(int(cur_edp[-3]))
        else:
            if int(cur_edp[-1]) == 1:
                cur_record_file = 'RoofDrift_1_x.out'
            else:
                cur_record_file = 'RoofDrift_1_y.out'
        last_line = "0"
        if os.path.exists(cur_record_file):
            with open(cur_record_file) as f:
                for line in f:
                    try:
                        float(line)  # only place if can convert to float (avoid blank spaces in the file)
                        if line == '\n':
                            last_line = last_line
                        else:
                            last_line = line
                    except:
                        last_line = last_line
        response.append(np.abs(float(last_line)))

    #return a dictionary of EDPs
    result = {edp_name: edp_val for edp_val, edp_name in
              zip(response, edp_names)}

    print(result)

    #### visualization ####
    # create pd dataframe (optional)
    #df = pd.DataFrame([response_bidirection],
    #    columns = column_names_bidirection, index = [gm_filename_dir[dir_i]])

    return result