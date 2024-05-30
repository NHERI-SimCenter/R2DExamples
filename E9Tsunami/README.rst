
E9 - Tsunami
============

+-----------------+-----------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E9Tsunami/>`                   |
+-----------------+-----------------------------------------------------------------+

The Cascadia Subduction Zone (CSZ) separates the Juan de Fuca and North America plates, stretching approximately 1,000 km between California and British Columbia, Canada. A rupture of the CSZ may result in a megathrust earthquake and a subsequent tsunami. This example considers a tsunami event in the city of Seaside, located along the northern Oregon coast. A highlight of this example is that it shows how user-provided fragility functions are employed in the SimCenter workflow. The building inventory consists of 4744 buildings of different types and construction materials. For the tsunami hazard, the results of a Probabilistic Seismic-Tsunami Hazard Analysis (PSTHA; Park et. al. 2017), with a recurrence interval of 500 years, is employed. The building inventory, tsunami hazard raster, and building fragility functions are all from the Seaside testbed, made available by the Center of Excellence for Risk-Based Community Resilience Planning (CoE) as part of their Interdependent Networked Community Resilience Modeling Environment (IN-CORE) platform. They can be accessed online on the IN-CORE Web Tools website (https://incore.ncsa.illinois.edu/doc/incore/webtools.html).

.. figure:: r2dt-0009.png
   :width: 400px
   :alt: I'm sorry, but there is an issue with the image that prevents me from providing a description. The content is blurred and obscured, making it difficult to discern details for an accurate alt text. If you provide a clearer image, I'd be happy to help with the alt text description.
   :align: center

#. Set the **Units** in the **GI** panel as shown in :numref:`r2d_gi` and check interested output files.

   .. figure:: figures/r2dt-0009-GI.png
      :name: r2d_gi
   :alt: Screenshot of a software interface titled 'R2D: Regional Resilience Determination Tool' with menu options on the left and forms for analysis configuration centered on the screen. The form includes sections for 'General Information', 'Units', 'Asset Layers', and 'Output Settings' with various options such as 'E9 - Tsunami Inundation' under Analysis Name, units of measurement, selectable asset layers like 'Buildings' and 'Soil', and checkboxes for output settings including 'Engineering demand parameters (EDP)' and 'Output building BIM.' There are buttons at the bottom for running analysis and interfacing with DesignSafe. No personal information is displayed.
      :align: center
      :figclass: align-center
      :width: 500

      R2D GI setup.
#. Set the **Event Raster File** in the **HAZ** panel to the "E9Tsunami/input_data/IMs/500yr/Tsu_500yr_Hmax.tif" in the "IMs" folder.
   The app would automatically load the hazard (:numref:`r2d_haz`). And the **Units of Event Input File** should be 
   "meter". In addition, set the coordinate reference system of your hazard raster. 

   .. figure:: figures/r2dt-0009-HAZ.png
      :name: r2d_haz
   :alt: Screenshot of the "R2D: Regional Resilience Determination Tool" interface with a focus on the "Hazard Selection" tab. This tab is set to "Raster Defined Hazard" and contains fields for "Event Raster File" with a path filled in, "Event Type" selected as "Tsunami", setting for "Coordinate reference system (CRS)" as "EPSG:4326 - WGS 84", and "Units of Event Input File" chosen as "Meters". There are several other tabs labeled on the left side, such as VIZ, GI, ASD, HTA, MOD, and more, indicating a comprehensive tool with multiple functions. The interface also includes "RUN" buttons, and "Login" and "Exit" options in the top corner.
      :align: center
      :figclass: align-center
      :width: 500

      R2D HAZ setup.
#. Select **GIS File to BIM** in the **ASD** panel and set the **Import Path** to "E9Tsunami/input_data/GISBuildingInventory/Seaside_Buildings.gpkg" (:numref:`r2d_asd`). 
   Specify the building IDs that you would like to include in the simulation (e.g., 1-4744 for the entire inventory - note this may take very long time to run 
   on a local machine, so it is suggested to first test with a small sample like 1-100 locally and then submit the entire run to DesignSafe - see more details in :numref:`r2d_run_ds`).

   .. figure:: figures/r2dt-0009-ASD.png
      :name: r2d_asd
   :alt: Screenshot of a software interface titled "R2D: Regional Resilience Determination Tool" showing a data table in the "Regional Building Inventory" section. The table contains columns for fid (feature ID), Longitude, Latitude, AREA, PERIMETER, TAX_, TAX_ID, X_COORD, Y_COORD, GIS_ACRES, and AV, with multiple rows of numerical data. The interface includes tabs labeled VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES, along with buttons for "RUN," "RUN at DesignSafe," "GET from DesignSafe," and "Exit." There is also a panel for loading buildings from a GIS file and an option for the advanced filter.
      :align: center
      :figclass: align-center
      :width: 500

      R2D ASD setup.
#. Set the **Regional Mapping** and **SimCenterEvent** in the **HTA** panel (e.g., :numref:`r2d_hta`). In this case, because we are using a raster for a hazard, select "Site Specified." The raster will be sampled at each asset location. 

   .. figure:: figures/r2dt-0009-HTA.png
      :name: r2d_hta
   :alt: Screenshot of the "R2D: Regional Resilience Determination Tool" interface. The window has a sidebar on the left with various menu items such as VIZ, GI, HAZ, and others, highlighting a focus on hazard mapping and analysis. The main panel shows fields for "Hazard to Local Asset Event" with a subsection "Regional Mapping" containing a mapping application dropdown that is set to "Site Specified". Below, another field labeled "Local Mapping" shows a "Local Event Type" set to "SimCenterEvent". At the bottom are buttons for running analysis or interacting with DesignSafe, as well as a Login option in the top right of the window. The interface has a clean, organized layout with a light theme.
      :align: center
      :figclass: align-center
      :width: 500

      R2D HTA setup.
#. Set the "Building Modeling" in **MOD** panel to "None". 

   .. figure:: figures/r2dt-0009-MOD.png
      :name: r2d_mod
   :alt: Screenshot of a software interface labeled "R2D: Regional Resilience Determination Tool." The layout features a navigation menu on the left with options including VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES, highlighted on MOD. On the right, there's a main content area with a dropdown menu titled "Building Modeling" set to "None." At the bottom, there are buttons for "RUN," "RUN at DesignSafe," "GET from DesignSafe," and "Exit." There's also a "Login" option at the top right corner.
      :align: center
      :figclass: align-center
      :width: 500

      R2D MOD setup.
#. Set the "Building Analysis Engine" in **ANA** panel to "IMasEDP". 

   .. figure:: figures/r2dt-0009-ANA.png
      :name: r2d_ana
   :alt: "Screenshot of a computer interface titled 'R2D: Regional Resilience Determination Tool.' The interface has a dark sidebar on the left with various acronyms like VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES. The ANA option is highlighted. The main area of the interface is mostly empty with a header reading 'Building Analysis Engine' and a smaller subtitle 'IMasEDP.' There are buttons at the bottom including 'RUN', 'RUN at DesignSafe', 'GET from DesignSafe', and 'Exit.' A 'Login' button is visible at the top right corner."
      :align: center
      :figclass: align-center
      :width: 500

      R2D ANA setup.
#. Set the "Damage and Loss Method" in **DL** panel to "User-provided fragilitites". Note please place the ruleset scripts and fragility functions
   in their individual folders so that the application could copy and load them later. 

   .. figure:: figures/r2dt-0009-DL.png
      :name: r2d_dl
   :alt: Screenshot of the R2D: Regional Resilience Determination Tool interface on a computer screen. The section displayed is titled "Damage & Loss Application" with "Pelicun" as a sub-category. It includes various settings such as "Damage and Loss Method," "Event time," and "Number of realizations" with input fields and checkboxes for options like "Output detailed results", "Log file", and "Coupled EDP". Two file path inputs with corresponding 'Browse' buttons are provided for "Auto populate script" and "Folder containing user-defined fragility function". At the bottom are buttons labeled "RUN", "RUN at DesignSafe", "GET from DesignSafe", and "Exit".
      :align: center
      :figclass: align-center
      :width: 500

      R2D DL setup.
#. Set the "UQ Application" in **UQ** panel to "None". 

   .. figure:: figures/r2dt-0009-UQ.png
      :name: r2d_uq
   :alt: Screenshot of a software application named R2D: Regional Resilience Determination Tool. The interface has a clean, modern look with a navigation menu on the left side, featuring abbreviations such as GI, HAZ, ASD, and others. The main area of the interface is mostly empty, with a section titled "UQ Application" and a dropdown menu set to "None." There are buttons at the bottom, including "RUN," "RUN at DesignSafe," "GET from DesignSafe," and "Exit." A login button is visible in the top right corner.
      :align: center
      :figclass: align-center
      :width: 500

      R2D UQ setup.

After setting up the simulation, please click the **RUN** to execute the analysis. Once the simulation completed, 
the app would direct you to the **RES** panel (:numref:`r2d_res`) where you could examine and export the results.

.. figure:: figures/r2dt-0009-RES.png
   :name: r2d_res
   :alt: Screenshot of the R2D: Regional Resilience Determination Tool interface with a coastal area map showing various buildings color-coded according to damage assessment in red, yellow, and green. A chart on the right displays relative frequency losses with peaks at various points. Below the chart is a table listing assets with columns for repair cost, repair time, replacement probability, fatalities, and loss ratio. On the left is a sidebar with various menu options such as VIZ, GI, HAZ, and others. A disclaimer note on the top left indicates that simulation results are not representative of any individual building's response. There are options to run the analysis, export results, and navigation buttons at the bottom.
   :align: center
   :figclass: align-center
   :width: 500

   R2D RES panel.

For simulating the damage and loss for a large region of interest (please remember to reset the building IDs in **ASD**), it would be efficient to submit and run the job 
to `DesignSafe <https://www.designsafe-ci.org/>`_ on `Stampede2 <https://www.tacc.utexas.edu/systems/stampede2>`_. 
This can be done in R2D by clicking **RUN at DesignSafe** (one would need to have a valid 
`DesignSafe account <https://www.designsafe-ci.org/account/register/>`_ for login and access the computing resource). 
:numref:`r2d_run_ds` provides an example configuration to run the analysis (and please see `R2D User Guide <https://nheri-simcenter.github.io/R2D-Documentation/common/user_manual/usage/desktop/usage.html#figremjobpanel>`_ for detailed descriptions).
The individual building simulations are paralleled when being conducted on Stampede2 which accelerate the process. It is suggested for the entire building 
inventory in this testbed to use 15 minutes with 96 Skylake (SKX) cores (e.g., 2 nodes with 48 processors per node) to complete 
the simulation. One would receive a job failure message if the specified CPU hours are not sufficient to complete the run. 
Note that the product of node number, processor number per node, and buildings per task should be greater than the 
total number of buildings in the inventory to be analyzed.

.. figure:: figures/r2dt-0009-RUN.png
   :name: r2d_run_ds
   :alt: Screenshot of a computer interface for a job submission form titled "R2D". The form includes fields such as job Name filled with "lake_charles_full_inventory", Num Nodes set to "2", # Processes Per Node with "48", # Buildings Per Task showing "280", and the Max Run Time is "00:29:00". There is also a checkbox for Save Inter. Results, which is unchecked. At the bottom, there is a blue "Submit" button.
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

.. figure:: figures/r2dt-0009-GFD.png
   :name: r2d_get_ds
   :alt: Screenshot of a computer interface with a table listing various jobs or tasks with columns for Name, Status, ID, and Date Created. Most jobs are marked as FINISHED, with a couple of entries marked as FAILED. The table is part of an application with options to "RUN at DesignSafe," "Export to PDF," and "GET from DesignSafe" available at the bottom of the window. There is a note at the top indicating users can click on any job shown to update the status, download, or delete the job.
   :align: center
   :figclass: align-center
   :width: 400

   R2D GET from DesignSafe.

