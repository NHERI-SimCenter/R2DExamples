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
#
# Based on rulesets developed by:
# Karen Angeles
# Meredith Lockhead
# Tracy Kijewski-Correa

import random
import numpy as np
import datetime


def building_class(BIM):
    """
    Short description

    Long description

    Parameters
    ----------
    BIM: dictionary
        Information about the building characteristics.

    Returns
    -------
    bldg_class: str
        One of the standard building class labels from HAZUS
    """

    if BIM['bldg_type'] == 3001:
        if ((BIM['occupancy_class'] == 'RES1') or
            ((BIM['roof_shape'] != 'flt') and (BIM['occupancy_class'] == ''))):
            # BuildingType = 3001
            # OccupancyClass = RES1
            # Wood Single-Family Homes (WSF1 or WSF2)
            # OR roof type = flat (HAZUS can only map flat to WSF1)
            # OR default (by '')
            if BIM['roof_shape'] == 'flt': # checking if there is a misclassication
                BIM['roof_shape'] = 'gab' # ensure the WSF has gab (by default, note gab is more vulneable than hip)
            return 'WSF'
        else:
            # BuildingType = 3001
            # OccupancyClass = RES3, RES5, RES6, or COM8
            # Wood Multi-Unit Hotel (WMUH1, WMUH2, or WMUH3)
            return 'WMUH'
    elif BIM['bldg_type'] == 3002:
        if ((BIM['design_level'] == 'E') and
            (BIM['occupancy_class'] in ['RES3A', 'RES3B', 'RES3C', 'RES3D',
                                            'RES3E', 'RES3F'])):
            # BuildingType = 3002
            # Steel Engineered Residential Building (SERBL, SERBM, SERBH)
            return 'SERB'
        elif ((BIM['design_level'] == 'E') and
              (BIM['occupancy_class'] in ['COM1', 'COM2', 'COM3', 'COM4', 'COM5',
                                          'COM6', 'COM7', 'COM8', 'COM9','COM10'])):
            # BuildingType = 3002
            # Steel Engineered Commercial Building (SECBL, SECBM, SECBH)
            return 'SECB'
        elif ((BIM['design_level'] == 'PE') and
              (BIM['occupancy_class'] not in ['RES3A', 'RES3B', 'RES3C', 'RES3D',
                                          'RES3E', 'RES3F'])):
            # BuildingType = 3002
            # Steel Pre-Engineered Metal Building (SPMBS, SPMBM, SPMBL)
            return 'SPMB'
        else:
            return 'SECB'
    elif BIM['bldg_type'] == 3003:
        if ((BIM['design_level'] == 'E') and
            (BIM['occupancy_class'] in ['RES3A', 'RES3B', 'RES3C', 'RES3D',
                                         'RES3E', 'RES3F', 'RES5', 'RES6'])):
            # BuildingType = 3003
            # Concrete Engineered Residential Building (CERBL, CERBM, CERBH)
            return 'CERB'
        elif ((BIM['design_level'] == 'E') and
              (BIM['occupancy_class'] in ['COM1', 'COM2', 'COM3', 'COM4', 'COM5',
                                          'COM6', 'COM7', 'COM8', 'COM9','COM10'])):
            # BuildingType = 3003
            # Concrete Engineered Commercial Building (CECBL, CECBM, CECBH)
            return 'CECB'
        else:
            return 'CECB'
    elif BIM['bldg_type'] == 3004:
        if BIM['occupancy_class'] == 'RES1':
            # BuildingType = 3004
            # OccupancyClass = RES1
            # Masonry Single-Family Homes (MSF1 or MSF2)
            return 'MSF'
        elif ((BIM['occupancy_class'] in ['RES3A', 'RES3B', 'RES3C', 'RES3D',
                                        'RES3E', 'RES3F']) and (BIM['design_level'] == 'E')):
            # BuildingType = 3004
            # Masonry Engineered Residential Building (MERBL, MERBM, MERBH)
            return 'MERB'
        elif ((BIM['occupancy_class'] in ['COM1', 'COM2', 'COM3', 'COM4',
                                        'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                                        'COM10']) and (BIM['design_level'] == 'E')):
            # BuildingType = 3004
            # Masonry Engineered Commercial Building (MECBL, MECBM, MECBH)
            return 'MECB'
        elif BIM['occupancy_class'] in ['IND1', 'IND2', 'IND3', 'IND4', 'IND5', 'IND6']:
            # BuildingType = 3004
            # Masonry Low-Rise Masonry Warehouse/Factory (MLRI)
            return 'MLRI'
        elif BIM['occupancy_class'] in ['RES3A', 'RES3B', 'RES3C', 'RES3D',
                                        'RES3E', 'RES3F', 'RES5', 'RES6', 'COM8']:
            # BuildingType = 3004
            # OccupancyClass = RES3X or COM8
            # Masonry Multi-Unit Hotel/Motel (MMUH1, MMUH2, or MMUH3)
            return 'MMUH'
        elif ((BIM['stories'] == 1) and
                (BIM['occupancy_class'] in ['COM1', 'COM2'])):
            # BuildingType = 3004
            # Low-Rise Masonry Strip Mall (MLRM1 or MLRM2)
            return 'MLRM'
        else:
            return 'MECB' # for others not covered by the above
        #elif ((BIM['occupancy_class'] in ['RES3A', 'RES3B', 'RES3C', 'RES3D',
        #                                'RES3E', 'RES3F', 'RES5', 'RES6',
        #                                'COM8']) and (BIM['design_level'] in ['NE', 'ME'])):
        #    # BuildingType = 3004
        #    # Masonry Multi-Unit Hotel/Motel Non-Engineered
        #    # (MMUH1NE, MMUH2NE, or MMUH3NE)
        #    return 'MMUHNE'
    elif BIM['bldg_type'] == 3005:
        return 'MH'

    else:
        return 'WMUH'
        # if nan building type is provided, return the dominant class

