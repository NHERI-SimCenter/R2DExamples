
E20 - Possible Worlds MDOF Building Response
===========================================

+-----------------+-----------------------------------------------------===============--+
| Download files  | :examplesgithub:`Download <E20PossibleWorldsMDOFBuildingResponse/>`  |
+-----------------+----------------------------------------------------------------------+

This, like example E19, is an update to an existing example, E2, to demonstrate the use of multiple possible worlds. As in E19, certain properties for specific buildings contained in the geojson file are uncertain. Unlike E19, this example runs a nonlinear finite element analysis for each building. As a consequence, additional changes are required than those of E19, as the **DL** tab must also be modified. Here **num_Realizations** must be set to **1**. The reason being that the damage and loss must now be done on the results of each nonlinear analysis. This is due to fact that both the EDP for a and the inputs to the DL application for the building can change between relizations.

The changing input panels:

#. **ASD** In the asset definition panel, the path to the ``AnchorageBuilding.csv`` file is specified. Once this file is loaded, the user can select which particular assets will be included in the analysis by entering a valid range (e.g., 1-50) in the form and clicking **Select**. The ``AnchorageBuilding.csv`` includes parameters for the damage and loss assessment (i.e., number of stories, year of built, occupancy class, structure type, and plan area) for more than 80,000 buildings in the community.

   .. figure:: figures/r2dt-0002-ASD.png
      :width: 600px
      :align: center


#. **DL** The damage and loss panel is now used to configure the **Pelicun3** backend. The **HAZUS MH EQ Story** damage and loss method is selected and configured as shown in the following figure:

   .. figure:: figures/r2dt-0002-DL.png
      :width: 600px
      :align: center


#. **RES** The analysis outputs for the selected 50 buildings are shown in the figure below. 

   .. figure:: figures/r2dt-0002-RES.png
      :width: 600px
      :align: center
