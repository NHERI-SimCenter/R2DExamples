# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Leland Stanford Junior University
# Copyright (c) 2018 The Regents of the University of California
#
# This file is part of the SimCenter Backend Applications
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# You should have received a copy of the BSD 3-Clause License along with
# this file. If not, see <http://www.opensource.org/licenses/>.
#
# Contributors:
# Adam Zsarnóczay
# Kuanshi Zhong
# Frank McKenna
#
# Based on rulesets developed by:
# Karen Angeles
# Meredith Lockhead
# Tracy Kijewski-Correa

import random
import numpy as np
import datetime
import math

from MetaVarRulesets import parse_BIM
from BldgClassRulesets import building_class
from WindWSFRulesets import WSF_config
from WindWMUHRulesets import WMUH_config

def auto_populate(BIM):
    """
    Populates the DL model for hurricane assessments in Atlantic County, NJ

    Assumptions:
    - Everything relevant to auto-population is provided in the Buiding
    Information Model (BIM).
    - The information expected in the BIM file is described in the parse_BIM
    method.

    Parameters
    ----------
    BIM_in: dictionary
        Contains the information that is available about the asset and will be
        used to auto-popualate the damage and loss model.

    Returns
    -------
    BIM_ap: dictionary
        Containes the extended BIM data.
    DL_ap: dictionary
        Contains the auto-populated loss model.
    """

    # parse the BIM data
    BIM_ap = parse_BIM(BIM, location="LA", hazards=['wind',])

    # identify the building class
    bldg_class = building_class(BIM_ap, hazard='wind')
    BIM_ap.update({'HazusClassW': bldg_class})

    # prepare the building configuration string
    if bldg_class == 'WSF':
        bldg_config = WSF_config(BIM_ap)
    elif bldg_class == 'WMUH':
        bldg_config = WMUH_config(BIM_ap)
    else:
        raise ValueError(
            f"Building class {bldg_class} not recognized by the "
            f"auto-population routine."
        )

    DL_ap = {
        '_method'      : 'HAZUS MH HU',
        'LossModel'    : {
            'DecisionVariables': {
                "ReconstructionCost": True
            },
            'ReplacementCost'  : 100
        },
        'Components'   : {
            bldg_config: [{
                'location'       : '1',
                'direction'      : '1',
                'median_quantity': '1.0',
                'unit'           : 'ea',
                'distribution'   : 'N/A'
            }]
        }
    }

    # drop keys of internal variables from BIM_ap dict
    internal_vars = ['V_ult', 'V_asd']
    for var in internal_vars:
        try:
            BIM_ap.pop(var)
        except:
            pass

    return BIM_ap, DL_ap
