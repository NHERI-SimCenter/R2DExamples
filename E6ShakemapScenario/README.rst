
E6 - ShakeMap Scenario
========================

+-----------------+-----------------------------------------------------+
| Download files  | :examplesgithub:`Github <E6ShakemapScenario/>`      |
+-----------------+-----------------------------------------------------+

This example demonstrates HAZUS earthquake damage and loss assessment capabilities with a USGS ShakeMap as an input. Building-level Damage and Losses (D&L) are calculated directly from an Intensity Measures (IM) grid for a Mw7.8 Scenario Earthquake - North San Andreas + North Coast + Peninsula + Santa Cruz Mountain scenario earthquake. Approximately 21,000 buildings are considered in the city of San Mateo, CA. The ShakeMap for this example can be downloaded `here <https://earthquake.usgs.gov/scenarios/eventpage/nclegacynpsanandreassansapsasm7p8_se/shakemap/>`_. 

.. figure:: r2dt-0006.png
   :width: 400px
   :alt: This image depicts a cartographic map highlighting the San Mateo area with superimposed data points. The data points appear as small blue markers densely packed across a section of the map, indicating a form of data collection or analysis focused on that particular urban area. There are lines crossing through the map, with a prominently marked Arthur Younger Freeway. The map also includes topographical features, main roads, and neighborhood names such as Burlingame, Foster City, and Belmont, suggesting this could be a tool for urban planning, data visualization, or geographic analysis.
   :align: center

#. **VIZ** This example illustrates the PGA contours of a ShakeMap scenario earthquake, i.e., one that has not occurred, on the San Andreas fault. In addition, it shows the buidling assets available in San Mateo, CA. 

   .. figure:: figures/r2dt-0006-VIZ.png
      :width: 600px
   :alt: Screenshot of a GIS (Geographic Information System) software interface with a map displaying overlaid earthquake risk zones along a coast, likely the San Andreas Fault, denoted by colored contours representing varying degrees of peak ground acceleration (PGA). The interface contains various toolbars and panels for navigation, layer visibility, adding data sources, and analysis functions. The left panel shows a list of layers such as 'Most Likely Critical,' 'Results,' and 'PGA Contours' with specific PGA values ticked, and a section at the bottom with options to add assets to an analysis list.
      :align: center


#. **GI** First, the unit system and asset type are prescribed in this panel, and we're interested in the building engineering demand parameters, damage measures, and the resulting decision variables.

   .. figure:: figures/r2dt-0006-GI.png
      :width: 600px
   :alt: Screenshot of a software interface with a sidebar and a main content section. The sidebar includes tabs labeled VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES. The main content section is titled "General Information" with "Analysis Name" displaying "E6 - ShakeMap." Below, it gives options for "Units" including "Force" in Kips, "Length" in Feet, and "Time" in Seconds. A checked checkbox next to "Buildings" and various unchecked checkboxes for "Soil," "Gas Network," "Water Network," "Waste Network," and "Transportation Network" are listed under "Asset Layers." Under "Output Settings," checkboxes for "Engineering demand parameters (EDP)," "Damage measures (DM)," "Decision variables (DV)," "Output EDP, DM, and DV every sampling realization," "Output Asset Information Model (AIM)," and "Output site IM" are selected and checked.
      :align: center


#. **HAZ** The **ShakeMap Earthquake Scenario** input panel allows for the import of a USGS ShakeMap, as shown with the SanAdreasM7.8 ShakeMap selected here. To load a ShakeMap a user must specify the path to a folder containing the ShakeMap files. At a minimum, the folder must contain a ``grid.xml`` file. More than one ShakeMap can be loaded at once. The ShakeMap that is selected on the list seen on the right side of the figure below will be employed in the analysis. 

   .. figure:: figures/r2dt-0006-HAZ.png
      :width: 600px
   :alt: Screenshot of a computer program interface titled "Hazard Selection" with an option for ShakeMap Earthquake Scenario. Instructions are provided on how to import ShakeMap files, including a file path and a 'Browse' and 'Load' button for file selection. Next to the instructions is a box titled "List of Imported ShakeMaps" with a single entry named "SanAndreasM7.8." A vertical navigation bar with various abbreviations such as VIZ, GI, HAZ, and ASD is visible on the left-hand side of the screen, indicating different modules or sections of the program. The overall color scheme is minimalistic with blues and grays.
      :align: center


#. **ASD** In the asset definition panel, the path to the ``San_Mateo_buildings.csv`` file is specified. Once this file is loaded, the user can select which particular assets will be included in the analysis by entering a valid range (e.g., 1-50) in the form and clicking **Select**. The ``San_Mateo_buildings.csv`` includes parameters for the damage and loss assessment (i.e., number of stories, year of built, occupancy class, structure type, and plan area) for more than 20,000 buildings in the community.

   .. figure:: figures/r2dt-0006-ASD.png
      :width: 600px
   :alt: Screenshot of an application interface showing a "Regional Building Inventory" with a table of building data. Columns include 'id', 'Latitude', 'Longitude', 'PlanArea', 'NumberOfStories', 'YearBuilt', 'OccupancyClass', 'ReplacementCost', and 'StructureType'. The table displays rows of numerical and text data corresponding to various buildings, with the first five asset IDs ranging from 1 to 5 listed for analysis. Options for exporting data and filters like 'Advanced Filter' and 'Clear Selection' are visible above the table.
      :align: center


#. **HTA** Next, a hazard mapping algorithm is specified using the **Nearest Neighbor** method and the **SimCenterEvent** application, which are configured as shown in the following figure with **100** samples in **4** neighbors, i.e., randomly sampling 100 ground motions from the nearest four stations (each station has one ground motion recording specified in the **HAZ**).

   .. figure:: figures/r2dt-0006-HTA.png
      :width: 600px
   :alt: Screenshot of a software interface with a panel titled "Building Mapping." The panel includes options for 'Number of samples' set to 100, 'Number of neighbors' set to 4, and a 'Seed' value of 447. Above the panel, 'Nearest Neighbour' is selected from a dropdown menu. To the left, there is a vertical navigation bar with various abbreviated options highlighted, like VIZ, GI, HAZ, ASD, with HTA currently selected. The interface has a minimalistic design with a color palette of gray, black, and a touch of teal.
      :align: center


#. **MOD** In the building modeling panel, simply leave the first dropdown box set to **None**.

   .. figure:: figures/r2dt-0006-MOD.png
      :width: 600px
   :alt: Screenshot of a software interface with a menu on the left side showing various options like VIZ, GI, HAZ, ASD, HTA, MOD (highlighted in blue), ANA, DL, UQ, RV, and RES. On the right side, there is a header titled "Building Modeling" with a dropdown menu set to "None," and a help icon at the top right corner. The rest of the interface is largely empty.
      :align: center


#. **ANA** In the analysis panel, **IMasEDP** is selected from the primary dropdown.

   .. figure:: figures/r2dt-0006-ANA.png
      :width: 600px
   :alt: A user interface with a menu on the left side with various abbreviated options such as VIZ, GI, HAZ, ASD, and others. The highlighted option is ANA. On the top right, there is a title "Building Analysis Engine" with a loading bar below it. The rest of the interface appears under construction or not loaded, with no discernable content displayed on the right side of the screen.
      :align: center


#. **DL** The damage and loss panel is now used to configure the **Pelicun3** backend. The **HAZUS MH EQ** damage and loss method is selected and configured as shown in the following figure:

   .. figure:: figures/r2dt-0006-DL.png
      :width: 600px
   :alt: Screenshot of a user interface for the "Building Damage & Loss Application" named Pelicun3. The interface displays an open tab with options for "Pelican Damage and Loss Prediction Methodology." Options shown include the Damage and Loss Method set to "HAZUS MH EQ IM," Event time is "off," and Number of realizations is "100." Checkboxes for "Output detailed results" and "Include ground failure" are unchecked, while "Log file" and "Coupled EDP" are checked. On the left sidebar, icons and abbreviations for different sections like VIZ, GI, HAZ, ASD, and others are visible, with the "DL" option highlighted.
      :align: center


#. **UQ** For this example the **UQ** dropdown box should be set to **None**.

   .. figure:: figures/r2dt-0006-UQ.png
      :width: 600px
   :alt: Screenshot of a user interface with a vertical navigation menu on the left side with several acronyms like VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ highlighted, RV, and RES. The top center of the screen has a header titled "UQ Application" with dropdown selection set to "None". The overall color scheme includes shades of blue and gray, and there is a settings icon in the top right corner.
      :align: center
	  
#. **RV**

   The random variable panel will be left empty for this example.

#. **RES** The analysis outputs for the selected buildings are shown in the figure below. It is important to note that the results are based on an approximate characterization of the ground motions and preliminary buildings data that has not been curated or verified thoroughly yet. The results presented herein are only for demonstrating the use of R2DTool and do not serve as an accurate representation of the real losses resulting from the earthquake.

   .. figure:: figures/r2dt-0006-RES.png
      :width: 600px
   :alt: Screenshot of a geographic information system (GIS) interface displaying a regional map with simulated earthquake damage using the SanAndreasM7.8 scenario. The map shows varying degrees of critical damage in different areas, highlighted in colors, with options to display Peak Ground Acceleration (PGA) contours, a grid, buildings, and an Open Street Map base layer. A key on the left-hand side indicates the severity levels of the critical damage. Note that the image includes a disclaimer emphasizing that the simulation results are not representative of any individual building's response and should not be used for predicting safety or outcomes without consulting a professional structural engineer.
      :align: center
