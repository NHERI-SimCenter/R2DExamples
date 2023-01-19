# -*- coding: utf-8 -*-

# Contributors:
# Stevan Gavrilovic
# Example 9 Tsunami, Seaside


def auto_populate(BIM):
    """
    Populates the DL model for tsunami example using custom fragility functions

    Assumptions:
    - Everything relevant to auto-population is provided in the Buiding Information Model (BIM).
    - The information expected in the BIM file is described in the parse_BIM
    method.

    Parameters
    ----------
    BIM_in: dictionary
        Contains the information that is available about the asset and will be
        used to auto-populate the damage and loss model.

    Returns
    -------
    BIM_ap: dictionary
        Contains the extended BIM data.
    DL_ap: dictionary
        Contains the auto-populated loss model.
    """

    # parse the BIM data
    #print(BIM) # Look in the BIM.json file to see what you can access here
    
    # BIM_ap is the 'extended BIM data - this case no extended BIM data
    BIM_ap = BIM
    
    # Get the number of Stories - note the column heading needs to be 'NumberOfStories' and nothing else.
    # A HAZUS type assessment in Pelicun will require this attribute to be provided.
    nstories = BIM.get('NumberOfStories', None)
    if nstories is None:
        return
        
    # Get the fragility tag according to some building attribute; the NumberOfStories in this case
    # The fragility tag needs to be unique, i.e., one tag for each fragility group
    # The fragility tag has to match the file name of the json file in the 'ComponentDataFolder' (without the .json suffix)
    fragility_function_tag = ""
    
    if nstories == 1:
        fragility_function_tag = 'building-1-Story'
    elif nstories == 2:
        fragility_function_tag = 'building-2-Storeys'
    elif nstories >= 3:
        fragility_function_tag = 'building-3andAbove-Storeys'
    else:
        print("The number of storeys ",nstories," is not a valid input")
    
    # print('*********fragility_tag',fragility_tag)
                
    # Populate the DL_ap
    # Select the DL method supported by Pelicun: '_method'  : 'HAZUS MH EQ' or 'HAZUS MH HU' or 'HAZUS MH FL' or 'HAZUS MH TN'
    # 'ComponentDataFolder' is the path to the folder where the custom fragility functions are located
    DL_ap = {
        '_method'      : 'HAZUS MH TN',
        'LossModel'    : {
            'DecisionVariables': {
                "ReconstructionCost": True
            },
            'ReplacementCost'  : 1.0
        },
        'Components'   : {
            fragility_function_tag: [{
                'location'       : '1',
                'direction'      : '1',
                'median_quantity': '1.0',
                'unit'           : 'ea',
                'distribution'   : 'N/A'
            }]
        }
    }

    return BIM_ap, DL_ap
