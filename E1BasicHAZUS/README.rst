
E1 - Basic HAZUS
===========================

+-----------------+---------------------------------------------+
| Download files  | :examplesgithub:`Download <E1BasicHAZUS/>`  |
+-----------------+---------------------------------------------+

This earthquake example demonstrates rapid analysis capabilities with the HAZUS earthquake damage and loss assessment methodology. Building-level Damage and Losses (D&L) are calculated directly from Intensity Measures (IM) for 25 assets. The IM field that represents peak ground acceleration in the city of San Francisco, CA, from an Mw7.2 event on the San Andreas fault, was obtained from Probabilistic Seismic Hazard Analysis (PSHA).

.. figure:: r2dt-0001.png
   :width: 400px
   :alt: A map overlaid with blue rectangles representing data points or geographical areas, possibly highlighting specific attributes or zones, concentrated in an urban grid layout that appears to represent a section of a coastal city. Some labels and streets are visible through the overlay, suggesting it could be a data-driven map of a city like San Francisco.
   :align: center

This study will be defined by sequentially traversing the input panels of the **R2D** interface. However, as outlined in the online user's manual, these procedures can be serialized to and loaded immediately from a JSON file, which for this example may be found :examplesgithub:`here <E1BasicHAZUS/input.json>`.

#. **VIZ** The visualization panel in the following figure shows the location of the assets considered in this example.

   .. figure:: figures/r2dt-0001-VIZ.png
      :width: 600px
   :alt: Screenshot of a Geographic Information System (GIS) interface showing a detailed map overlaid with colorful grid-like analysis. Various layers such as 'Ground Motion' and 'Buildings' are activated, and there are toolbars and panels visible for data management and map controls. The map seems to represent a section of a city with marked streets and labeled areas like 'Civic Center' and 'Mission Bay'.
      :align: center


#. **GI** The unit system and asset type are prescribed in this panel, and we're interested in the **building engineering demand parameters**, **damage measures**, and the resulting **decision variables**.

   .. figure:: figures/r2dt-0001-GI.png
      :width: 600px
   :alt: Screenshot of an analysis settings interface with sections for General Information, Asset Layers, and Output Settings. Under General Information, there is an Analysis Name field "E1 - HAZUS" and units for Force (Kips), Length (Feet), and Time (Seconds). Asset Layers include Buildings selected, and options for Soil, Gas Network, Water Network, Waste Network, and Transportation Network. Output Settings include checked options for Engineering demand parameters (EDP), Damage measures (DM), and Decision variables (DV), with additional output settings below. On the left, there is a vertical navigation bar with acronyms like VIZ, HAZ, ASD, and others.
      :align: center


#. **HAZ** Next, the hazard panel is used to load the event grid ``.csv`` file (:examplesgithub:`view on Github <E1BasicHAZUS/input_data/San_Andreas_Mw72_filtered/EventGrid.csv>`) which lists out the ground motions which are used as the ground acceleration time history inputs in this example.

   .. figure:: figures/r2dt-0001-HAZ.png
      :width: 600px
   :alt: Screenshot of a software interface for hazard selection. The interface includes a file path to an event file listing motions related to the San Andreas fault earthquake simulation data. Additional options for input file units are visible, with 'PGA' and 'Gravitational constant (g)' as selectable options. On the left side, there is a vertical menu with acronyms VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES, possibly representing different modules or functions of the software. Two 'Browse' buttons are present for locating and selecting files.
      :align: center


#. **ASD** In the asset definition panel, the path to the :examplesgithub:`SanFranciscoBuildings.csv <E1BasicHAZUS/input_data/SanFrancisco_buildings.csv>` file is specified. Once this file is loaded, the user can select which particular assets will be included in the analysis by entering a valid range (e.g., 1-50) in the form and clicking **Select**. The ``SanFranciscoBuildings_full.csv`` file includes parameters for the damage and loss assessment (e.g., number of stories, year of built, occupancy class, structure type, and plan area) for more than 100,000 buildings in the community.

   .. figure:: figures/r2dt-0001-ASD.png
      :width: 600px
   :alt: Screenshot of a Regional Building Inventory spreadsheet with columns for id, Latitude, Longitude, PlanArea, NumberOfStories, YearBuilt, ReplacementCost, StructureType, and OccupancyClass. The data appears to be related to various buildings, including their geographical coordinates, size, construction year, estimated cost to replace, and other characteristics. There are visible headers with options like "CSV to AIM," "Browse," "Advanced Filter," and "Clear Selection." The table displays rows of data entries with numerical and alphabetic values.
      :align: center


#. **HTA** Next, a hazard mapping algorithm is specified using the **Nearest Neighbor** method and the **SimCenterEvent** application, which are configured as shown in the following figure with **100** samples in **4** neighbors, i.e., randomly sampling 100 ground motions from the nearest four stations (each station has a large number of ground motion records specified in the **HAZ**).

   .. figure:: figures/r2dt-0001-HTA.png
      :width: 600px
   :alt: Screenshot of a user interface for "Building Mapping" with options including "Nearest Neighbour" at the top. Fields available for input are "Number of samples" with 100 entered, "Number of neighbors" with 4 entered, and "Seed" with 687 entered. On the left side, there's a vertical navigation bar with menu items including VIZ, GI, HAZ, ASD, HTA (highlighted), MOD, ANA, DL, UQ, RV, and RES.
      :align: center


#. **MOD** panel is not used for this procedure. The **Building Modeling** dropdown should be left set to **None**.

   .. figure:: figures/r2dt-0001-MOD.png
      :width: 600px
   :alt: Screenshot of a user interface with a vertical navigation bar on the left side, showing various abbreviated options such as VIZ, GI, HAZ, ASD, HTA, MOD (highlighted in blue), ANA, DL, UQ, RV, and RES. On the right side is a header titled "Building Modeling" with a dropdown menu set to "None" and a search icon next to it. The rest of the right side is blank.
      :align: center

#. **ANA** In the analysis panel, **IMasEDP** is selected from the primary dropdown.

   .. figure:: figures/r2dt-0001-ANA.png
      :width: 600px
   :alt: A screenshot depicting a user interface with a dark vertical navigation bar on the left showing various abbreviated categories such as VIZ, GI, HAZ, and others, with the category ANA highlighted in light blue. On the right, there's a header titled "Building Analysis Method" above an empty, interactive section labeled "IMasEDP" with a search or navigation icon displayed at the top right corner.
      :align: center


#. **DL** The damage and loss panel is now used to configure the **Pelicun3** backend. The **HAZUS MH EQ IM** damage and loss method is selected and configured as shown in the following figure:

   .. figure:: figures/r2dt-0001-DL.png
      :width: 600px
   :alt: Screenshot of a software interface titled "Building Damage & Loss Application". The interface includes a section labeled "Pelicun Damage and Loss Prediction Methodology" with options for selecting the Damage and Loss Method, toggling Event Time, and setting the Number of realizations to 100. Options for output include checkboxes for 'Output detailed results', 'Log file' (checked), 'Coupled EDP' (checked), and 'Include ground failure'. On the left sidebar are various tabs abbreviated as VIZ, GI, HAZ, ASD, HTA, MOD, ANA, and the active tab DL, with subsequent tabs UQ, RV, and RES. The overall theme of the user interface is a clean, muted color palette with simple rectangular sections and buttons.
      :align: center


#. **UQ** For this example the **UQ** dropdown box should be set to **None**.

   .. figure:: figures/r2dt-0001-UQ.png
      :width: 600px
   :alt: Screenshot of a software interface with a dark sidebar on the left containing options such as VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ (highlighted in light blue), RV, and RES. The right side of the interface has a header reading "UQ Application" with a drop-down menu set to "None", and the rest of the area is blank.
      :align: center
	  
#. **RV**

   The random variable panel will be left empty for this example.


