
E8 - Hurricane Wind
===================

+-----------------+-----------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E8HurricaneWind/>`                   |
+-----------------+-----------------------------------------------------------------+

Hurricane Laura made landfall as a strong Category 4 storm near Cameron, LA in the early hours of 27 August 2020, tying the Last Island Hurricane of 1856 as the strongest land-falling hurricane in Louisiana history.
This example presents a wind-induced damage assessment for Lake Charles, LA. Peak wind speed data of Hurricane Laura from Applied Research Associates, Inc. is used as intensity measure, inventory data of about 26,000 wood residential buildings
is used along with the rulesets developed to map the inventory to HAZUS-type damage assessment. Final results include the damage and loss estimations along with the building information models based on the rulesets.

.. figure:: r2dt-0008.png
   :width: 400px
   :alt: A detailed map showing a segment of a city with roads, water bodies, and various zoned areas. Major roads and highways are marked with numbers such as I-210 and LA 385. The map includes color-coded areas, possibly indicating different land uses or zoning types, and clusters of black dots that could represent buildings or population density. The names of some locations, like Lake Charles, Westlake, and Chennault International Airport, are visible on the map.
   :align: center

#. Set the **Units** in the **GI** panel as shown in :numref:`r2d_gi` and check interested output files.

   .. figure:: figures/r2dt-0008-GI.png
      :name: r2d_gi
   :alt: Screenshot of a software interface with various elements labeled "VIZ," "GI," "HAZ," "ASD," "HTA," "MOD," "ANA," "DL," "UQ," "RV," and "RES" on the left side, indicating different modules or sections. The main part of the screen shows a section titled "General Information" with an analysis name "E8 - Hurricane Wind," and units listed for force in kips, length in feet, and time in seconds. Below, the "Asset Layers" section includes a checked box next to "Buildings" and several unchecked options like Soil, Gas Network, and others. The "Output Settings" section has several checked boxes, including "Engineering demand parameters (EDP)" and "Damage measures (DM)."
      :align: center
      :figclass: align-center
      :width: 500

      R2D GI setup.
#. The **Raster Defined Hazard** option is used to define the peak gust wind speed field in the region.

   .. figure:: figures/r2dt-0008-HAZ.png
      :name: r2d_haz
   :alt: A screenshot of a software interface with a section titled "Hazard Selection" that includes options for defining a raster-defined hazard. A file path is shown under "Event Raster File" indicating the location of data for a hurricane. An "Event Type" dropdown menu is set to "Hurricane," and there is a setting to "Set the coordinate reference system (CRS)" with "Coordinate Reference System: EPSG:4326 - WGS 84" selected. Below is another section labeled "Intensity Measures of Raster" with a dropdown menu for "Layer 0" set to "Peak Gust Wind Speed - PWS" and a second dropdown for units set to "Miles per hour." The left panel shows additional menu options, including VIZ, GI, HAZ (highlighted), ASD, HTA, MOD, ANA, DL, UQ, RV, and RES.
      :align: center
      :figclass: align-center
      :width: 500

      R2D HAZ setup.
#. Download the `BIM_LakeCharles_Full.csv <https://www.designsafe-ci.org/data/browser/public/designsafe.storage.published//PRJ-3207v4/01.%20Input:%20BIM%20-%20Building%20Inventory%20Data>`_ (under **01. Input: BIM - Building Inventory Data** folder). 
   Select **CSV to BIM** in the **ASD** panel and set the **Import Path** to "BIM_LakeCharles_Full.csv" (:numref:`r2d_asd`). 
   Specify the building IDs that you would like to include in the simulation (e.g., 1-26516 for the entire inventory - note this may take very long time to run 
   on a local machine, so it is suggested to first test with a small sample like 1-100 locally and then submit the entire run to DesignSafe - see more details in :numref:`r2d_run_ds`).

   .. figure:: figures/r2dt-0008-ASD.png
      :name: r2d_asd
   :alt: Screenshot of a computer interface titled "Regional Building Inventory," displaying a spreadsheet with columns titled fid, RoofShape, PlanArea, Longitude, Latitude, LULC, DWSII, BuildingType, Occupancy Class, and AvgJanTemp. The spreadsheet lists entries for various buildings with details such as roof shape (Hip or Gable), plan area in square feet, geographic coordinates, and other attributes. The interface includes options to browse files, apply advanced filters, and clear selections.
      :align: center
      :figclass: align-center
      :width: 500

      R2D ASD setup.
#. Select the **Site Specified** option in the **HTA** panel (e.g., :numref:`r2d_hta`).

   .. figure:: figures/r2dt-0008-HTA.png
      :name: r2d_hta
   :alt: Screenshot of a user interface with a navigation menu on the left side showing abbreviated category titles like VIZ, GI, HAZ, ASD, and others in a vertical list. The selected category is HTA, highlighted in blue. The main content area on the right is titled "Building Mapping" with a subtitle "Site Specified" and contains a brief description saying "Hazard values are provided, or calculated, at each asset site." The rest of the main content area is empty, indicating a placeholder or additional content to be loaded or added.
      :align: center
      :figclass: align-center
      :width: 500

      R2D HTA setup.
#. Set the "Building Modeling" in **MOD** panel to "None". 

   .. figure:: figures/r2dt-0008-MOD.png
      :name: r2d_mod
   :alt: Screenshot of a user interface with a sidebar on the left showing vertically listed menu options labeled VIZ, GI, HAZ, ASD, and HTA, with MOD highlighted in blue at the bottom. On the right, there is a larger pane with the title "Building Modeling" at the top and a dropdown menu set to "None." The overall color scheme is grayscale with a touch of blue.
      :align: center
      :figclass: align-center
      :width: 500

      R2D MOD setup.
#. Set the "Building Analysis Engine" in **ANA** panel to "IMasEDP". 

   .. figure:: figures/r2dt-0008-ANA.png
      :name: r2d_ana
   :alt: Screenshot of a user interface for the R2D: Regional Resilience Determination Tool. The interface includes a sidebar with categories like VIZ, GI, HAZ, ASD, HTA, MOD, and ANA highlighted. The main screen shows a section titled "Building Analysis Engine" with a dropdown menu currently displaying "IMasEDP". The overall color scheme features shades of gray and blue, indicating a professional software environment.
      :align: center
      :figclass: align-center
      :width: 500

      R2D ANA setup.
#. Set the "Damage and Loss Method" in **DL** panel to "HAZUS MH HU". Download the ruleset scripts from 
   `DesignSafe PRJ-3207 <https://www.designsafe-ci.org/data/browser/public/designsafe.storage.published//PRJ-3207v4/03.%20Input:%20DL%20-%20Rulesets%20for%20Asset%20Representation/scripts>`_ 
   (under **03. Input: DL - Rulesets for Asset Representation/scripts** folder) and 
   set the **Auto populate script** to "auto_HU_LA.py" (:numref:`r2d_dl`). Note please place the ruleset scripts 
   in an individual folder so that the application could copy and load them later. 

   .. figure:: figures/r2dt-0008-DL.png
      :name: r2d_dl
   :alt: Screenshot of a user interface for a Building Damage & Loss Application named "Pelican3." It displays the "Pelican Damage and Loss Prediction Methodology" section with settings for "Damage and Loss Method" set to "HAZUS MH HU," "Event time" off, "Number of realizations" at 5000, an option for "Output detailed results" unchecked, "Log file" checked, and "Coupled EDP" checked. Below, there's a field for "Auto-populate script" showing a file path on a user's desktop, with a "Browse" button next to it. On the left side, a vertical navigation bar shows tabs such as VIZ, GI, HAZ, ASD, and others with the DL tab highlighted in blue.
      :align: center
      :figclass: align-center
      :width: 500

      R2D DL setup.
#. Set the "UQ Application" in **UQ** panel to "None". 

   .. figure:: figures/r2dt-0008-UQ.png
      :name: r2d_uq
   :alt: Screenshot of a software interface titled "R2D: Regional Resilience Determination Tool" featuring a vertical menu bar with options labeled VIZ, GI, HAZ, ASD, HTA, MOD, ANA, and DL, and a main pane with a dropdown menu titled "UQ Application" currently set to "None". The interface has a clean and simple design with a color scheme of grays and a teal accent for the UQ section.
      :align: center
      :figclass: align-center
      :width: 500

      R2D UQ setup.

After setting up the simulation, please click the **RUN** to execute the analysis. Once the simulation is completed, 
the app would direct you to the **RES** panel (:numref:`r2d_res`) where you could examine and export the results.

.. figure:: figures/r2dt-0008-RES.png
   :name: r2d_res
   :alt: A screenshot of a geographic information system (GIS) interface displaying a map of a urban area with buildings and waterways. On the left side, a panel titled "Regional Results Summary" shows data classes indicating "Most Likely Critical Damage" with a color code, an "Earthquake Raster Hazard" histogram, and options for viewing buildings and an Open Street Map. There's a disclaimer at the top cautioning that this simulation results are not representative of individual building responses and should be consulted with a professional structural engineer. The map itself shows a grid layout of streets, with water bodies like the Calcasieu River and Lake Charles labeled, and several highways visible, such as US 171, US 90, and Interstate 10 crossing through the area.
   :align: center
   :figclass: align-center
   :width: 500

   R2D RES panel.

For simulating the damage and loss for a large region of interest (please remember to reset the building IDs in **ASD**), it would be efficient to submit and run the job 
to `DesignSafe <https://www.designsafe-ci.org/>`_ on `Frontera <https://tacc.utexas.edu/systems/frontera/>`_. 
This can be done in R2D by clicking **RUN at DesignSafe** (one would need to have a valid 
`DesignSafe account <https://www.designsafe-ci.org/account/register/>`_ for login and access the computing resource). 
:numref:`r2d_run_ds` provides an example configuration to run the analysis (and please see `R2D User Guide <https://nheri-simcenter.github.io/R2D-Documentation/common/user_manual/usage/desktop/usage.html#figremjobpanel>`_ for detailed descriptions).
The individual building simulations are paralleled when being conducted on Stampede2 which accelerate the process. It is suggested for the entire building 
inventory in this testbed to use 15 minutes with 96 Skylake (SKX) cores (e.g., 2 nodes with 48 processors per node) to complete 
the simulation. One would receive a job failure message if the specified CPU hours are not sufficient to complete the run. 
Note that the product of node number, processor number per node, and buildings per task should be greater than the 
total number of buildings in the inventory to be analyzed.

.. figure:: figures/r2dt-0008-RUN.png
   :name: r2d_run_ds
   :alt: Screenshot of a software interface with a job submission form titled "R2D". Fields displayed include "job Name" filled with "lake_charles_full_inventory", "Num Nodes" with a value of 2, "# Processes Per Node" with a value of 48, "# Buildings Per Task" with a value of 280, a checkbox for "Save Inter. Results" that is unchecked, and "Max Run Time" set to "00:29:00". A blue "Submit" button is at the bottom.
   :align: center
   :figclass: align-center
   :width: 300

   R2D - Run at DesignSafe (configuration).

Users could monitor the job status and retrieve result data by **GET from DesignSafe** button (:numref:`r2d_get_ds`). The retrieved data include
four major result files, i.e., *BIM.hdf*, *EDP.hdf*, *DM.hdf*, and *DV.hdf*. R2D also automatically converts the hdf files to csv files that are easier to work with.
While R2D provides basic visualization functionalities (:numref:`r2d_res`), users could access the data which are downloaded under the remote work directory, e.g., 
*/Documents/R2D/RemoteWorkDir* (this directory is machine specific and can be found in **File->Preferences->Remote Jobs Directory**).
Once having these result files, users could extract and process interested information - the next section will use 
the results from this testbed as an example to discuss more details.

.. figure:: figures/r2dt-0008-GFD.png
   :name: r2d_get_ds
   :alt: Screenshot of a computer interface showing a list of jobs with columns for Name, Status, ID, and Date Created. The status column indicates that most jobs are finished, but a few are marked as failed. The interface has interactive buttons at the bottom for "RUN at DesignSafe," "Export to PDF," and "GET from DesignSafe."
   :align: center
   :figclass: align-center
   :width: 400

   R2D GET from DesignSafe.

