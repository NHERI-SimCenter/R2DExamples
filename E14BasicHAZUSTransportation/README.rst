
E14 - Basic HAZUS Transportation Infrastructure
===============================================

+-----------------+------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E14BasicHAZUSTransportation/>`  |
+-----------------+------------------------------------------------------------+

This earthquake example demonstrates rapid analysis capabilities with the HAZUS earthquake damage and loss assessment methodology for transportation infrastructure. Asset-level Damage and Losses (D&L) are calculated directly from Intensity Measures (IM) for buildings, highway bridges, highway tunnels, and roadways. The IM field that represents ground shaking intensity measures in Alameda Island, CA, from an Mw7.05 event on the Hayward fault was obtained from Probabilistic Seismic Hazard Analysis (PSHA). The liquefaction-induced ground failure intensity measures (Permanent Ground Deformation) are calculated following the method proposed by Wang, C., Wang, D., & Chen, Q. (2021). Regional Evaluation of Liquefaction-Induced Lateral Ground Deformation for City-Scale Transportation Resilience Analysis. Journal of Infrastructure Systems, 27(2), 04021008.

.. figure:: r2dt-0014.png
   :width: 400px
   :alt: A screenshot of a map-based software interface displaying a damage assessment tool for an urban area. The map is marked with various colors and lines, representing different levels of infrastructure damage such as bridges, buildings, roadways, and tunnels. On the left side of the image is a control panel with options to display different types of damage indicated by checkboxes and color codes. The background map shows geographical features like water bodies and streets, and the tool has a label at the top right corner saying "Regional Map."
   :align: center

This study will be defined by sequentially traversing the input panels of the **R2D** interface. However, as outlined in the online user's manual, these procedures can be serialized to and loaded immediately from a JSON file, which for this example may be found :examplesgithub:`here <E1BasicHAZUS/input.json>`.

#. **VIZ** The visualization panel in the following figure shows the location of the assets considered in this example.

   .. figure:: figures/r2dt-0014-VIZ.png
      :width: 600px
   :alt: Screenshot of the "R2D: Regional Resilience Determination Tool" interface, displaying a map with various geospatial layers overlaid on it. The area shown is around Jack London Square, with labeled locations such as "USS Hornet: Sea, Air & Space Museum" and "Robert W. Crown Memorial State Beach." The map includes colored lines and shapes representing different infrastructure elements. The left side of the screen contains a series of menu options for layer visibility, asset selection, and tool settings, as well as a program output log detailing recent actions taken within the software.
      :align: center


#. **GI** The unit system and asset type are prescribed in this panel. We select both Buildings and Transportation Network as asset types, and we are interested in the **building engineering demand parameters**, **damage measures**, and the resulting **decision variables**.

   .. figure:: figures/r2dt-0014-GI.png
      :width: 600px
   :alt: Screenshot of the user interface for the R2D: Regional Resilience Determination Tool. The interface is divided into multiple panels, with the left panel containing a vertical navigation menu including items like VIZ, GI, HAZ, ASD, and other abbreviations. The right panel displays sections for General Information with fields for 'Analysis Name' and 'Units,' Asset Layers with items like 'Buildings' and 'Transportation Network' checked, and Output Settings with various options related to output data. At the bottom, there are buttons for running the analysis and others for interaction with DesignSafe, as well as a log with timestamps detailing asset loading and selection activities. The overall color scheme is predominantly gray and white.
      :align: center


#. **HAZ** Next, the hazard panel is used to load the event grid ``.csv`` file (:examplesgithub:`view on Github <E14BasicHAZUSTransportation/input_data/IMs/EventGrid.csv>`), which lists out the ground motions, which are used as the seismic hazard inputs in this example.

   .. figure:: figures/r2dt-0014-HAZ.png
      :width: 600px
   :alt: Screenshot of the "R2D: Regional Resilience Determination Tool" interface on a computer screen, showing the Hazard Selection tab with options for specifying ground motions, input file units, and peak ground acceleration settings. The bottom of the screen displays a "Run" button along with a log of program outputs indicating the selection of assets such as a bridge and roadway for analysis.
      :align: center


#. **ASD** In the asset definition panel, the path to the :examplesgithub:`all_bldgs.csv <E14BasicHAZUSTransportation/input_data/all_bldgs.csv>` file is specified for buildings. 
For transportation infrastructure, the path to the :examplesgithub:`AI_hwy_inventory.geojson <E14BasicHAZUSTransportation/input_data/AI_hwy_inventory.geojson>` file is specified.
Once this file is loaded, the user can select which particular assets to include in the analysis by entering a valid range (e.g., 1-50) in the form and clicking **Select**. The ``all_bldgs.csv`` and ``AI_hwy_inventory.geojson``files include parameters for the damage and loss assessment (e.g., number of stories, year of built, occupancy class, structure type, and plan area) for the buildings and transportation infrastructure in the community.

   .. figure:: figures/r2dt-0014-ASD-building.png
      :width: 600px
   :alt: Screenshot of a computer application named "R2D: Regional Resilience Determination Tool" displaying a Regional Building Inventory table. The table includes columns for id, Latitude, Longitude, NumberOfStories, YearBuilt, Occupancy Class, StructureType, PlanArea, ReplacementCost, Population, SoilType, and type, with various entries listed. On the left, there are buttons labeled VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES, indicating different modules or sections of the application. There are options to run the program or retrieve data from DesignSafe, as well as a program output log at the bottom displaying recent activity.
      :align: center
   .. figure:: figures/r2dt-0014-ASD-transport.png
      :width: 600px
   :alt: Screenshot of the "R2D: Regional Resilience Determination Tool" interface showing a dataset in a table format under the 'Regional Transportation Network' tab. The displayed data includes columns for 'id,' 'BridgeClass,' 'DeckWidth,' 'Location,' 'MaxSpanLength,' 'NumOfSpans,' 'Skew,' 'SoilType,' 'StateCode,' 'StructureNumber,' 'YearBuilt,' 'assetSubtype,' and 'type' with several entries for bridges listed. There are additional options for filtering and analyzing the dataset, and at the bottom there's a program output log with recent activity timestamps.
      :align: center


#. **HTA** Next, a hazard mapping algorithm is specified using the **Nearest Neighbor** method, which is configured as shown in the following figure with **100** samples in **4** neighbors, i.e., randomly sampling 100 ground motions from the nearest Ground Motion Grid points(each grid point has 1000 intensity measure realizations as specified in the **HAZ**).

   .. figure:: figures/r2dt-0014-HTA.png
      :width: 600px
   :alt: Screenshot of a computer interface titled "R2D: Regional Resilience Determination Tool". The interface includes a navigation menu on the left with various options, such as VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES. In the main content area, there are tabs for "Buildings", "Transportation Components Mapping", and "Nearest Neighbour". Under the "Transportation Components Mapping" tab, there are fields labeled "Number of samples", "Number of neighbors", and "Seed" with inputs for numbers. At the bottom of the interface are buttons labeled "RUN", "RUN at DesignSafe", "GET from DesignSafe", and "Exit". The lower part of the screen displays a program output log with entries indicating analysis of a bridge, roadway, tunnel, and loading of a file. The overall color scheme includes shades of gray, white, and a light blue highlight.
      :align: center


#. **MOD** panel is not used for this procedure. The **Building Modeling** dropdown 
and **Transportation Components Modelling**should be left set to **None**.

   .. figure:: figures/r2dt-0014-MOD.png
      :width: 600px
   :alt: Screenshot of a software interface titled "R2D: Regional Resilience Determination Tool" displaying a sidebar with various menu options such as VIZ, GI, HAZ, ASD, and others. The main area has tabs for Buildings, Transportation Components Modeling, and None, with 'Transportation Network' selected under the Buildings tab. A message log at the bottom shows recent activity, including analysis tasks for a bridge, roadway, and tunnel, as well as a 'Done Loading File' message. Buttons for 'RUN,' 'RUN at DesignSafe,' 'GET from DesignSafe,' and 'Exit' are present at the bottom of the screen.
      :align: center

#. **ANA** In the analysis panel, **IMasEDP** is selected from the primary dropdown for both Buildings and Transportation Network.

   .. figure:: figures/r2dt-0014-ANA.png
      :width: 600px
   :alt: Screenshot of the R2D: Regional Resilience Determination Tool software with a graphical user interface featuring a navigation panel on the left side with various tabs such as VIZ, GI, HAZ, and selected ANA. The main area on the right includes tabs for Buildings, Transportation Components Modeling, and IMasEDP, however, the workspace appears mostly empty with no visual data present. There's a log at the bottom reporting actions such as selecting bridges and a tunnel for analysis and loading a file. The upper right corner features a 'Login' button indicating user authentication is possible.
      :align: center


#. **DL** The damage and loss panel is now used to configure the **Pelicun** backend. The **HAZUS MH EQ IM** damage and loss method is selected and configured as shown in the following figure
for both Buildings and Transportation Network. 

   .. figure:: figures/r2dt-0014-DL.png
      :width: 600px
   :alt: Screenshot of a user interface for the R2D: Regional Resilience Determination Tool. The interface features a menu on the left side with various options like VIZ, GI, HAZ, and others. The main panel is labeled "Transportation Network" and is part of the "Buildings" tab, showing settings for "Pelican Damage and Loss Prediction Methodology" with fields for damage and loss method, event time, number of realizations, and checkboxes for output options such as detailed results, log file, coupled EDP, and ground failure. At the bottom, there is a console with log messages about the analysis of a bridge, roadway, and tunnel selected for analysis, concluding with "Done Loading File." The bottom also features buttons for RUN, RUN at DesignSafe, GET from DesignSafe, and Exit.
      :align: center


#. **UQ** For this example the **UQ** dropdown box should be set to **None**.

   .. figure:: figures/r2dt-0014-UQ.png
      :width: 600px
   :alt: Alt Text: A screenshot of a computer interface for the "R2D: Regional Resilience Determination Tool," featuring a minimalist design with a navigation bar on the left with various abbreviated options like VIZ, GI, HAZ, and others. The main panel to the right is mostly empty except for a header with the words "Buildings" and "Transportation Network" under the label "UQ Application," and a small section at the bottom displaying a log of actions, including messages about a bridge, roadway, and tunnel selected for analysis and a file loading completion note. There are buttons labeled "Run," "Run at DesignSafe," "GET from DesignSafe," and "Exit" at the bottom of the window. The top right corner has a "Login" button, indicating user authentication functionality.
      :align: center
	  
#. **RV**

   The random variable panel will be left empty for this example.


