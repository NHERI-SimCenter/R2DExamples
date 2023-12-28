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
import pandas as pd
import datetime
import math

def parse_GI(GI_in):
    """
    Parses the information provided in the AIM model.

    The parameters below list the expected inputs

    Parameters
    ----------
    stories: str
        Number of stories
    yearBuilt: str
        Year of construction.
    roofType: {'hip', 'hipped', 'gabled', 'gable', 'flat'}
        One of the listed roof shapes that best describes the building.
    occupancy: str
        Occupancy type.
    buildingDescription: str
        MODIV code that provides additional details about the building
    structType: {'Stucco', 'Frame', 'Stone', 'Brick'}
        One of the listed structure types that best describes the building.
    V_design: string
        Ultimate Design Wind Speed was introduced in the 2012 IBC. Officially
        called “Ultimate Design Wind Speed (Vult); equivalent to the design
        wind speeds taken from hazard maps in ASCE 7 or ATC's API. Unit is
        assumed to be mph.
    area: float
        Plan area in ft2.
    z0: string
        Roughness length that characterizes the surroundings.

    Returns
    -------
    GI_ap: dictionary
        Parsed building characteristics.
    """

    # maps roof type to the internal representation
    ap_RoofType = {
        'hip'   : 'hip',
        'hipped': 'hip',
        'Hip'   : 'hip',
        'gabled': 'gab',
        'gable' : 'gab',
        'Gable' : 'gab',
        'flat'  : 'flt',
        'Flat'  : 'flt'
    }
    # maps roof system to the internal representation
    ap_RoofSyste = {
        'Wood': 'trs',
        'OWSJ': 'ows',
        'N/A': 'trs'
    }
    roof_system = GI_in.get('RoofSystem','Wood')
    if pd.isna(roof_system):
        roof_system = 'Wood'

    # maps number of units to the internal representation
    ap_NoUnits = {
        'Single': 'sgl',
        'Multiple': 'mlt',
        'Multi': 'mlt',
        'nav': 'nav'
    }
    # maps for split level
    ap_SplitLevel = {
        'NO': 0,
        'YES': 1
    }
    # maps for design level (Marginal Engineered is mapped to Engineered as default)
    ap_DesignLevel = {
        'E': 'E',
        'NE': 'NE',
        'PE': 'PE',
        'ME': 'E'
    }
    design_level = GI_in.get('DesignLevel','E')
    if pd.isna(design_level):
        design_level = 'E'

    foundation = GI_in.get('FoundationType',3501)
    if np.isnan(foundation):
        foundation = 3501

    nunits = GI_in.get('NoUnits',1)
    if np.isnan(nunits):
        nunits = 1

    # Average January Temp.
    ap_ajt = {
        'Above': 'above',
        'Below': 'below'
    }

    # Year built
    alname_yearbuilt = ['YearBuiltNJDEP', 'yearBuilt', 'YearBuiltMODIV', 'YearBuilt']
    yearbuilt = None
    try:
        yearbuilt = GI_in['YearBuilt']
    except Exception as e:
        for i in alname_yearbuilt:
            if i in GI_in.keys():
                yearbuilt = GI_in[i]
                break

        # if none of the above works, set a default
        if yearbuilt is None:
            yearbuilt = 1985

    # Number of Stories
    alname_nstories = ['stories', 'NumberofStories0', 'NumberofStories1']
    nstories = None
    try:
        nstories = GI_in['NumberOfStories']
    except Exception as e:
        for i in alname_nstories:
            if i in GI_in.keys():
                nstories = GI_in[i]
                break

        # if none of the above works, we need to raise an exception
        if nstories is None:
            raise e from None

    # Plan Area
    alname_area = ['area', 'PlanArea1', 'Area', 'PlanArea0']
    area = None
    try:
        area = GI_in['PlanArea']
    except Exception as e:
        for i in alname_area:
            if i in GI_in.keys():
                area = GI_in[i]
                break

        # if none of the above works, we need to raise an exception
        if area is None:
            raise e from None

    # Occupancy Class
    alname_occupancy = ['occupancy']
    oc = None
    try:
        oc = GI_in['OccupancyClass']

    except Exception as e:
        for i in alname_occupancy:
            if i in GI_in.keys():
                oc = GI_in[i]
                break

        # if none of the above works, we need to raise an exception
        if oc is None:
            raise e from None

    # if getting RES3 then converting it to default RES3A
    if oc == 'RES3':
        oc = 'RES3A'

    # maps for flood zone
    ap_FloodZone = {
        # Coastal areas with a 1% or greater chance of flooding and an
        # additional hazard associated with storm waves.
        6101: 'VE',
        6102: 'VE',
        6103: 'AE',
        6104: 'AE',
        6105: 'AO',
        6106: 'AE',
        6107: 'AH',
        6108: 'AO',
        6109: 'A',
        6110: 'X',
        6111: 'X',
        6112: 'X',
        6113: 'OW',
        6114: 'D',
        6115: 'NA',
        6119: 'NA'
    }
    if type(GI_in['FloodZone']) == int:
        # NJDEP code for flood zone (conversion to the FEMA designations)
        floodzone_fema = ap_FloodZone[GI_in['FloodZone']]
    else:
        # standard input should follow the FEMA flood zone designations
        floodzone_fema = GI_in['FloodZone']

    # maps for BuildingType
    ap_BuildingType = {
        # Coastal areas with a 1% or greater chance of flooding and an
        # additional hazard associated with storm waves.
        'Wood': 3001,
        'Steel': 3002,
        'Concrete': 3003,
        'Masonry': 3004,
        'Manufactured': 3005
    }
    if type(GI_in['FloodZone']) == str:
        # NJDEP code for flood zone (conversion to the FEMA designations)
        buildingtype = ap_BuildingType[GI_in['BuildingType']]
    else:
        # standard input should follow the FEMA flood zone designations
        buildingtype = GI_in['BuildingType']

    # first, pull in the provided data
    GI_ap = GI_in.copy()
    GI_ap.update(dict(
        OccupancyClass=str(oc),
        YearBuilt=int(yearbuilt),
        NumberOfStories=int(nstories),
        PlanArea=float(area),
        occupancy_class=str(oc),
        bldg_type=int(buildingtype),
        year_built=int(yearbuilt),
        # double check with Tracey for format - (NumberStories0 is 4-digit code)
        # (NumberStories1 is image-processed story number)
        stories=int(nstories),
        area=float(area),
        flood_zone=floodzone_fema,
        V_ult=float(GI_in['DSWII']),
        avg_jan_temp=ap_ajt[GI_in.get('AvgJanTemp','Below')],
        roof_shape=ap_RoofType[GI_in['RoofShape']],
        roof_slope=float(GI_in.get('RoofSlope',0.25)), # default 0.25
        sheathing_t=float(GI_in.get('SheathingThick',1.0)), # default 1.0
        roof_system=str(ap_RoofSyste[roof_system]), # only valid for masonry structures
        garage_tag=float(GI_in.get('Garage',-1.0)),
        lulc=GI_in.get('LULC',-1),
        z0 = float(GI_in.get('z0',-1)), # if the z0 is already in the input file
        Terrain = GI_in.get('Terrain',-1),
        mean_roof_height=float(GI_in.get('MeanRoofHt',15.0)), # default 15
        design_level=str(ap_DesignLevel[design_level]), # default engineered
        no_units=int(nunits),
        window_area=float(GI_in.get('WindowArea',0.20)),
        first_floor_ht1=float(GI_in.get('FirstFloorHt1',10.0)),
        split_level=bool(ap_SplitLevel[GI_in.get('SplitLevel','NO')]), # dfault: no
        fdtn_type=int(foundation), # default: pile
        city=GI_in.get('City','NA'),
        wind_zone=str(GI_in.get('WindZone', 'I'))
    ))

    # add inferred, generic meta-variables

    # Hurricane-Prone Region (HRP)
    # Areas vulnerable to hurricane, defined as the U.S. Atlantic Ocean and
    # Gulf of Mexico coasts where the ultimate design wind speed, V_ult is
    # greater than a pre-defined limit.
    if GI_ap['year_built'] >= 2016:
        # The limit is 115 mph in IRC 2015
        HPR = GI_ap['V_ult'] > 115.0
    else:
        # The limit is 90 mph in IRC 2009 and earlier versions
        HPR = GI_ap['V_ult'] > 90.0

    # Wind Borne Debris
    # Areas within hurricane-prone regions are affected by debris if one of
    # the following two conditions holds:
    # (1) Within 1 mile (1.61 km) of the coastal mean high water line where
    # the ultimate design wind speed is greater than flood_lim.
    # (2) In areas where the ultimate design wind speed is greater than
    # general_lim
    # The flood_lim and general_lim limits depend on the year of construction
    if GI_ap['year_built'] >= 2016:
        # In IRC 2015:
        flood_lim = 130.0 # mph
        general_lim = 140.0 # mph
    else:
        # In IRC 2009 and earlier versions
        flood_lim = 110.0 # mph
        general_lim = 120.0 # mph
    # Areas within hurricane-prone regions located in accordance with
    # one of the following:
    # (1) Within 1 mile (1.61 km) of the coastal mean high water line
    # where the ultimate design wind speed is 130 mph (58m/s) or greater.
    # (2) In areas where the ultimate design wind speed is 140 mph (63.5m/s)
    # or greater. (Definitions: Chapter 2, 2015 NJ Residential Code)
    if not HPR:
        WBD = False
    else:
        WBD = (((GI_ap['flood_zone'].startswith('A') or GI_ap['flood_zone'].startswith('V')) and
                GI_ap['V_ult'] >= flood_lim) or (GI_ap['V_ult'] >= general_lim))

    # Terrain
    # open (0.03) = 3
    # light suburban (0.15) = 15
    # suburban (0.35) = 35
    # light trees (0.70) = 70
    # trees (1.00) = 100
    # Mapped to Land Use Categories in NJ (see https://www.state.nj.us/dep/gis/
    # digidownload/metadata/lulc02/anderson2002.html) by T. Wu group
    # (see internal report on roughness calculations, Table 4).
    # These are mapped to Hazus defintions as follows:
    # Open Water (5400s) with zo=0.01 and barren land (7600) with zo=0.04 assume Open
    # Open Space Developed, Low Intensity Developed, Medium Intensity Developed
    # (1110-1140) assumed zo=0.35-0.4 assume Suburban
    # High Intensity Developed (1600) with zo=0.6 assume Lt. Tree
    # Forests of all classes (4100-4300) assumed zo=0.6 assume Lt. Tree
    # Shrub (4400) with zo=0.06 assume Open
    # Grasslands, pastures and agricultural areas (2000 series) with
    # zo=0.1-0.15 assume Lt. Suburban
    # Woody Wetlands (6250) with zo=0.3 assume suburban
    # Emergent Herbaceous Wetlands (6240) with zo=0.03 assume Open
    # Note: HAZUS category of trees (1.00) does not apply to any LU/LC in NJ
    terrain = 15 # Default in Reorganized Rulesets - WIND
    AIM_LULC = GI_ap['lulc']
    AIM_terrain = GI_ap['Terrain']
    if (GI_ap['z0'] > 0):
        terrain = int(100 * GI_ap['z0'])
    elif (AIM_LULC > 0):
        if (GI_ap['flood_zone'].startswith('V') or GI_ap['flood_zone'] in ['A', 'AE', 'A1-30', 'AR', 'A99']):
            terrain = 3
        elif ((AIM_LULC >= 5000) and (AIM_LULC <= 5999)):
            terrain = 3 # Open
        elif ((AIM_LULC == 4400) or (AIM_LULC == 6240)) or (AIM_LULC == 7600):
            terrain = 3 # Open
        elif ((AIM_LULC >= 2000) and (AIM_LULC <= 2999)):
            terrain = 15 # Light suburban
        elif ((AIM_LULC >= 1110) and (AIM_LULC <= 1140)) or ((AIM_LULC >= 6250) and (AIM_LULC <= 6252)):
            terrain = 35 # Suburban
        elif ((AIM_LULC >= 4100) and (AIM_LULC <= 4300)) or (AIM_LULC == 1600):
            terrain = 70 # light trees
    elif (AIM_terrain > 0):
        if (GI_ap['flood_zone'].startswith('V') or GI_ap['flood_zone'] in ['A', 'AE', 'A1-30', 'AR', 'A99']):
            terrain = 3
        elif ((AIM_terrain >= 50) and (AIM_terrain <= 59)):
            terrain = 3 # Open
        elif ((AIM_terrain == 44) or (AIM_terrain == 62)) or (AIM_terrain == 76):
            terrain = 3 # Open
        elif ((AIM_terrain >= 20) and (AIM_terrain <= 29)):
            terrain = 15 # Light suburban
        elif (AIM_terrain == 11) or (AIM_terrain == 61):
            terrain = 35 # Suburban
        elif ((AIM_terrain >= 41) and (AIM_terrain <= 43)) or (AIM_terrain in [16, 17]):
            terrain = 70 # light trees

    GI_ap.update(dict(
        # Nominal Design Wind Speed
        # Former term was “Basic Wind Speed”; it is now the “Nominal Design
        # Wind Speed (V_asd). Unit: mph."
        V_asd = np.sqrt(0.6 * GI_ap['V_ult']),

        # Flood Risk
        # Properties in the High Water Zone (within 1 mile of the coast) are at
        # risk of flooding and other wind-borne debris action.
        flood_risk=True,  # TODO: need high water zone for this and move it to inputs!

        HPR=HPR,
        WBD=WBD,
        terrain=terrain,
    ))

    return GI_ap

