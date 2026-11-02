
E20 - MDOF Building Response with Possible Worlds
=================================================

+-----------------+----------------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E20PossibleWorldsMDOFBuildingResponse/>`  |
+-----------------+----------------------------------------------------------------------+

This example updates E2 to demonstrate the use of multiple possible worlds. As in E19, certain properties of specific buildings in the GeoJSON file are uncertain. Only buildings 1 and 2 have uncertain properties. Building 1 has two possible values for **NumberOfStories**. Building 2 has two possible values for each of **NumberOfStories**, **OccupancyClass** and **StructureType**.

Unlike E19, this example runs a nonlinear finite element analysis for each building, so the **DL** panel must also be modified: the **Sample size** must be set to **1**, rather than the **1000** used in E2. Both the EDPs for a building and the inputs to the damage and loss application can change between realizations, so damage and loss must be evaluated on the results of each nonlinear analysis.

The results presented herein are only for demonstrating the use of R2DTool and do not serve as an accurate representation of the real losses resulting from the earthquake.

The panels that differ from E2 are described below. The user is referred to E2 for discussion of all other inputs.

#. **ASD** In the asset definition panel, the application selected is **GeoJSON to Asset**. As discussed in E19, three inputs are required: 1) the path to the GeoJSON file, ``AnchorageBuildings.geojson``, 2) the coordinate reference system, **OGC:CRS84**, and 3) the assets to analyze, here **1-5** to limit the run time.

   .. figure:: figures/E20ASD.png
      :width: 600px
      :align: center


#. **DL** In the damage and loss panel, the **Pelicun3** application is selected, with **Hazus Earthquake - Stories** as the damage and loss method. **Importantly**, the **Sample size** is set to **1** for this workflow.

   .. figure:: figures/E20DL.png
      :width: 600px
      :align: center


#. **RES** The analysis outputs for the selected **5** buildings are shown in the figure below. 

   .. figure:: figures/E20RES.png
      :width: 600px
      :align: center
