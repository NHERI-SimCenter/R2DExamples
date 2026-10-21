
E19 - Basic HAZUS with Possible Worlds
======================================

+-----------------+------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E19PossibleWorldsBasicHAZUS/>`  |
+-----------------+------------------------------------------------------------+

This earthquake example demonstrates how include uncertainty related to asset attributes in the workflows.

In the GeoJSON form of an asset input, the properties of each asset are specified in the **properties** section. In an asset inventory with no uncertainty, each individual property has a single value. To express uncertainty in this property, the values are instead placed in a list. As an example, the following text is extracted from the SanFranciscoBuildings.json file. It shows the properties information for buildings **1** and **2**. Building **1** has no uncertain properties, building **2** has two uncertain properties (number of floors, and structure type) each with three possible values.

.. code-block:: json
   :force:

   "features": [
     {
       "type": "Feature",
       "id": 1,
       ...
       "properties": {
         "Latitude": 37.796739,
         "Longitude": -122.403859,
         "HeightClass": "Low-Rise",
         "DesignLevel": "Pre-Code",
         "PlanArea": 7752,
         "NumberOfStories": 2,
         "YearBuilt": 1906,
         "ReplacementCost": 1022488.8,
         "StructureType": "C1",
         "OccupancyClass": "COM4",
         "type": "Building"
       }
     },
     {
       "type": "Feature",
       "id": 2,
       "properties": {
         "Latitude": 37.7996,
         "Longitude": -122.419356,
         "HeightClass": "",
         "DesignLevel": "Pre-Code",
         "PlanArea": 3600,
         "NumberOfStories": [3,2,1],
         "YearBuilt": 1931,
         "ReplacementCost": 6843570.3,
         "StructureType": ["W2","W1","W1"],
         "OccupancyClass": "RES3",
         "type": "Building"
       }
     },
     ...
   ]

.. NOTE::

   #. The current workflow assumes that if any asset has more than one uncertain quantitaties in lists, that the length of these lists is the same for that asset.
   #. BRAILS++ will generate such inputs when num_possible worlds is set to > 1 for properties of assets for which inputation is required or for properties of assets for which validators have been used and these validators have worked with imputed data.

The difference in inputs provided to R2D between this example and E1 are in the Asset Description Panel, **ASD**. The user is referred to E1 for discussion on all other inputs.

	      
#. **ASD** In the asset definition panel, the **GeoJSON to Asset** option is used to provide information on the assets as opposed to the **CSV. Two inputs are required: 1) The path to the csv file, :examplesgithub:`SanFranciscoBuildings.json <E19PossibleWorldsBasicHAZUS/input_data/SanFrancisco_buildings.json>`. The files contains **id,Latitude,Longitude,PlanArea,NumberOfStories,YearBuilt,ReplacementCost,StructureType,OccupancyClass,Footprint** and 2) the range of assets to be analyzed. In the figure only buildings **8000-8024** have only been selected.

   .. note::

      1. The range of assets uses the id's of the buildings provided in the asset inventory file.
      2. By defauult **NO ASSETS** will be analyzed unless the range is filled in.
      3. The user can provide a comma seperated list of assets that includes ranges, e.g. 1,2,3,5-10,100-1000.
      2. Once the range has been filled in, the user can view the selected buildings by going to the **VIZ** panel, looking at the buildings layer and selecting the **Selected Buildings**, and de-selecting **All Buildings**.
      3. If user does not like the selections, the **Clear Selections** button in the ASD panel can be pressed.

   .. figure:: figures/r2dt-0001-ASD.png
      :width: 600px
      :align: center


#. **RES**

   Once the user has run the example, by using the **RUN** button, or the **RUN at DesignSafe** and **Get from DesignSafe** buttons, the results panel will be automatically shown. In the **Buildings** tab are two windows, which can both be seperated from the main application. The first displays the QGIS window now showing should the **VIZ** panel be selected, to which a new **layer** has been added, the **Resulta** layer and by delselecting the other layers in this QGIS window, the most likely damage state for the 25 buildings (buildings 8000-8024 in the **ASD** panel) selected to be analyzed can be reviewed. The second window shows, in tabular form, the results for each building. By left or right clicking in any of the columns of the table, statistical data for the entries, e.g. min, max, mean, mode and histograms, may be obtained.
   
   .. figure:: figures/r2dt-0001-RES.png
      :width: 600px
      :align: center   
