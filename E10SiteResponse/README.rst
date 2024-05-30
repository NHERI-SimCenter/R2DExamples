
E10 - Site Response Analysis
============================

+-----------------+-----------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E10SiteResponse/>`                   |
+-----------------+-----------------------------------------------------------------+

This example presents regional earthquake impact analysis including site response analysis and building damage and loss assessment. Overall 177 sites are included for soil response simulation under bedrock ground motion input with a building inventory including approximately 14,000 buildings in the city of Alameda, CA.

.. figure:: r2dt-0010.png
   :width: 400px
   :alt: A graphic depiction of a city's mapped area displayed in a pixelated, video game-like style. The perspective is overhead, showcasing an intricate layout of streets, buildings, and facilities in varied colors against a light blue background. Yellow dots that could represent points of interest are scattered across the map.
   :align: center

#. Set the **Units** in the **GI** panel as shown in :numref:`r2d_gi` and check interested output files.

   .. figure:: figures/r2dt-0010-GI.png
      :name: r2d_gi
   :alt: Screenshot of a software interface with a panel of analysis settings. On the left side, navigation tabs like VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, RES are listed. The main, larger panel on the right titled 'General Information' has fields under 'Analysis Name' with a field pre-filled with 'E10 - Site Response', and 'Units' with drop-down options for 'Force' (selected as Kips), 'Length' (Feet), and 'Time' (Seconds). 'Asset Layers' lists options like Buildings (checked), Soil, Gas Network and others. Below, 'Output Settings' has several checked options including 'Engineering demand parameters (EDP)', 'Damage measures (DM)', and others related to output specifications.
      :align: center
      :figclass: align-center
      :width: 500

      R2D GI setup.
#. Select the **Regional Site Response** method in the **HAZ** panel.
   In the ``Site`` input widget, the ``SiteModelData.csv`` should be automatically loaded, which includes the basic site information and modelng parameter.
   In the ``Soil Properties/Site Response Script`` widget, the modeling script should be automatically loaded which would create OpenSees tcl models for individual sites selected for analysis.
   In the ``Input Motions`` widget, the ``EventGrid.csv`` file as well as the input motion directory should be automatically loaded, which includes the ground acceleration time history data files.
   In the ``Units of Event Input File`` widget, the time history file ``TH_file`` has a unit of gravity acceleration and the scaling ``factor`` is unitless (these two fields are automatically created from the column headers in ``EventGrid.csv``).

   .. figure:: figures/r2dt-0010-HAZ.png
      :name: r2d_haz
   :alt: Screenshot of a software interface titled "R2D: Regional Resilience Determination Tool". The interface includes multiple sections for Hazard Selection, Soil Properties, and Input Motions. Key elements visible are data input fields, file paths, drop-down menus for model selections, and a table with columns such as id, Longitude, Latitude, Vs30, DepthToRock, and several soil parameters. The interface provides options to run operations, browse for files, and fetch site data.
      :align: center
      :figclass: align-center
      :width: 500

      R2D HAZ setup.
#. **ASD** In the asset definition panel, the path to the ``all_bldgs.csv`` file is specified. Once this file is loaded, the user can select which 
   particular assets will be included in the analysis by entering a valid range in the form and clicking **Select**. 

   .. figure:: figures/r2dt-0010-ASD.png
      :name: r2d_asd
   :alt: Screenshot of a computer application titled "R2D: Regional Resilience Determination Tool". The interface shows a regional building inventory with a table of data that includes building identifiers and various attributes such as latitude, longitude, number of stories, year built, occupancy class, structure type, plan area, replacement cost, population, and soil type. Some columns contain numerical data, while others contain text and code snippets in JSON format. The application offers options to load information from a CSV file, convert the CSV to BIM, and has buttons labeled "Run", "Advanced Filter", "Select", "Clear Selection". At the bottom, there are buttons for "RUN at DesignSafe", "GET from DesignSafe", "Save", and "Exit". The dataset shown lists buildings with IDs from 1 to 22.
      :align: center
      :figclass: align-center
      :width: 500

      R2D ASD setup.
#. **HTA** Next, a hazard mapping algorithm is specified using the **Nearest Neighbor** method, which is configured as shown in the following figure with **4** samples in **4** neighbors.

   .. figure:: figures/r2dt-0010-HTA.png
      :name: r2d_hta
   :alt: Screenshot of a user interface with a section titled "Building Mapping" selected on the screen. The section includes a dropdown menu labeled "Nearest Neighbour" and fields for "Number of samples" set to 4, "Number of neighbors" also set to 4, and "Seed" with a value of 468. A vertical menu on the left includes options such as VIZ, GI, HAZ, ASD, with HTA highlighted in blue, and other options including MOD, ANA, DL, UQ, RV, and RES. The interface has a simple, clean design with mostly grayscale colors.
      :align: center
      :figclass: align-center
      :width: 500

      R2D HTA setup.
#. **MOD** In the modeling panel, the **MDOF-LU** method is used to create Multi-Degree-Of-Freedom (MDOF) nonlinear shear building model from the input building file in **ASD**. 
   Following the HAZUS EQ Technical Manual Chapter 5, a hysteretic nonlinear material is defined for each story with a story shear and displacement relationship with the initial stiffness, 
   over-strength ratio, hardening ratio, and degradation factor. These parameters are stored in the ``HazusData.txt`` for different building design levels (e.g., high-, moderate-, or pre-code) 
   which is now primarily based on the built year of the structure.

   .. figure:: figures/r2dt-0010-MOD.png
      :name: r2d_mod
   :alt: Screenshot of a software interface named R2D: Regional Resilience Determination Tool. The screen shows a section titled "Building Modeling" with file path input fields and standard deviation settings. There are tabs on the left side labeled VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES, with the MOD tab currently highlighted. At the bottom of the interface, there are "RUN" and "GET from DesignSafe" buttons, and an "Exit" button on the lower right corner. The interface includes a note attributing a backend application to Prof. Xinzhehng Lu, Tsinghua University, and provides citation details for two scholarly articles associated with the software.
      :align: center
      :figclass: align-center
      :width: 500

      R2D MOD setup.
#. Set the "Building Analysis Engine" in **ANA** panel to "OpenSees". 

   .. figure:: figures/r2dt-0010-ANA.png
      :name: r2d_ana
   :alt: Screenshot of a software interface for building analysis labeled "Building Analysis Method". It includes settings and parameters such as Analysis method with command-line options, Integration method 'Newmark', Algorithm 'Newton', ConvergenceTest 'NormUnbalance', Solver 'Umfpack', and Damping Model 'Rayleigh Damping'. Options to select the tangent stiffness and input for two modes are also seen, along with a field to choose an optional Analysis Script. To the left side, there's a vertical navigation bar with various abbreviated menu items like 'VIZ', 'GI', 'HAZ', 'ASD', 'HTA', 'MOD', with 'ANA' highlighted, suggesting the current section.
      :align: center
      :figclass: align-center
      :width: 500

      R2D ANA setup.
#. **DL** The damage and loss panel is now used to configure the **Pelicun3** backend. The **HAZUS MH EQ Story** damage and loss method is selected and configured as shown in the following figure:

   .. figure:: figures/r2dt-0010-DL.png
      :name: r2d_dl
   :alt: Screenshot of a "Building Damage & Loss Application" interface with a section titled "Pelican Damage and Loss Prediction Methodology". This section presents options including a dropdown for "Damage and Loss Method" set to "HAZUS MH EQ Story", a toggle for "Event time" set to "off", a field for "Number of realizations" with a value of "1000", checkboxes for "Output detailed results" and "Include ground failure" which are unchecked, and a checkbox for "Log file" which is checked. The menu on the left side includes tabs labelled VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES, with DL highlighted.
      :align: center
      :figclass: align-center
      :width: 500

      R2D DL setup.
#. Set the "UQ Application" in **UQ** panel to "Dakota". 

   .. figure:: figures/r2dt-0010-UQ.png
      :name: r2d_uq
   :alt: Screenshot of a graphical user interface for uncertainty quantification settings, with a menu on the left side highlighting the option "UQ" among others including "VIZ", "GI", "HAZ", and more. On the right, the main panel is titled "UQ Method" with options for selecting an "UQ Engine", and checkboxes for "Parallel Execution" and "Save Working dirs". There is a method selection dropdown set to "LHS" with fields for "# Samples" set to "4" and "Seed" set to "471". The interface has a clean and minimalist design with a blue and gray color scheme.
      :align: center
      :figclass: align-center
      :width: 500

      R2D UQ setup.

After setting up the simulation, please click the **RUN** to execute the analysis. Once the simulation completed, 
the app would direct you to the **RES** panel (:numref:`r2d_res`) where you could examine and export the results.

.. figure:: figures/r2dt-0010-RES.png
   :name: r2d_res
   :alt: Screenshot of the "R2D: Regional Resilience Determination Tool" showing a regional map with various buildings marked, each associated with specific data such as repair cost and time, as well as a graph displaying relative frequency losses. The interface provides statistical information such as estimated regional totals for casualties, fatalities, economic and structural losses, and repair times. Options for exporting results and running analysis via DesignSafe are visible.
   :align: center
   :figclass: align-center
   :width: 500

   R2D RES panel.

For simulating the damage and loss for a large region of interest (please remember to reset the building IDs in **ASD**), it would be efficient to submit and run the job 
to `DesignSafe <https://www.designsafe-ci.org/>`_ on on `Frontera <https://tacc.utexas.edu/systems/frontera/>`_. 
This can be done in R2D by clicking **RUN at DesignSafe** (one would need to have a valid 
`DesignSafe account <https://www.designsafe-ci.org/account/register/>`_ for login and access the computing resource). 
:numref:`r2d_run_ds` provides an example configuration to run the analysis (and please see `R2D User Guide <https://nheri-simcenter.github.io/R2D-Documentation/common/user_manual/usage/desktop/usage.html#figremjobpanel>`_ for detailed descriptions).
The individual site response analysis and building damage and loss simulation are paralleled on Stampede2. It is suggested for this demoed example to use 60 minutes with 96 Skylake (SKX) cores (e.g., 2 nodes with 48 processors per node) to complete 
the simulation. One would receive a job failure message if the specified CPU hours are not sufficient to complete the run. 
Note that the product of node number, processor number per node, and buildings per task should be greater than the total number of sites/buildings in the inventory to be analyzed.

.. figure:: figures/r2dt-0010-RUN.png
   :name: r2d_run_ds
   :alt: An interface of a software application with various input fields and settings for a job named "regional_site_response." The fields include "Num Nodes" with a value of 2, "# Processes Per Node" with a value of 45, "# Buildings Per Task" with a value of 2, an unchecked checkbox for "Save Inter. Results," and "Max Run Time" with a value of 01:00:00. A blue "Submit" button is at the bottom of the interface.
   :align: center
   :figclass: align-center
   :width: 300

   R2D - Run at DesignSafe (configuration).

Users could monitor the job status and retrieve result data by **GET from DesignSafe** button (:numref:`r2d_get_ds`). The retrieved data include
four major result files, i.e., *IM.hdf*, *BIM.hdf*, *EDP.hdf*, *DM.hdf*, and *DV.hdf*. R2D also automatically converts the hdf files to csv files that are easier to work with.
While R2D provides basic visualization functionalities (:numref:`r2d_res`), users could access the data which are downloaded under the remote work directory, e.g., 
*/Documents/R2D/RemoteWorkDir* (this directory is machine specific and can be found in **File->Preferences->Remote Jobs Directory**).
Once having these result files, users could extract and process interested information - the next section will use 
the results from this testbed as an example to discuss more details.

