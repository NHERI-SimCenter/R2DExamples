
E12 - Istanbul Regional Seismic Risk Analysis
===============================================

+-----------------+-------------------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E12IstanbulRegionalSeismicRiskAnalysis/>`    |
+-----------------+-------------------------------------------------------------------------+

This example features a systematic regional seismic damage and loss assessment for Istanbul, Turkey. 
The ground motion acceleration time histories were simulated using the hercules software and a detailed 
geophysical model of Istanbul region ([ZhangEtAl2021]_, [ZhangEtAl2023-1]_, [ZhangEtAl2023-2]_, [ZhangEtAl2023-3]_). The ground motions are used to investigate the 
impact of a Mw7.0 earthquake on the Central Marmara Basin fault. Engineering Demand Parameters are simulated 
with OpenSees models for individual reinforced concrete buildings in this example. Building damage and loss 
is evaluated the story-level based on the HAZUS earthquake damage and loss assessment methodology.

.. figure:: r2dt-0012.png
   :width: 400px
   :alt: Screenshot of a geographical information system (GIS) application with a map of an urban area surrounded by water. The interface shows a tool titled "R2D: Regional Resilience Determination Tool" with various menus and options for adding basemaps, such as "OpenStreetMap." There are categorized lists of visible items on the map like buildings and infrastructure, labeled with symbols denoting different types like "COM1," "IND2," or "RES1." The map displays a dense concentration of colored dots and shapes representing data overlaying a coastal city area. There's a set of toolbar icons at the top and a side panel with browser-like bookmarks for data sources like "GeoPackage" and "PostgreSQL." The bottom right corner indicates the image scale and projection system as "1:46,042" and "EPSG:3857" respectively, with options for running analysis and exporting data.
   :align: center

.. note::
   This example uses simulated ground motion time histories from the hercules software. Due to size constraints, 
   only an example set of time histories are bundled with R2D. The complete set of simulated ground motions are 
   available at `DesignSafe PRJ-3712 <https://doi.org/10.17603/ds2-e7nq-8d52>`_.


Modeling Procedure
------------------

We now embark on our journey through the input panels of R2D, making known to the workflow builder how our procedure should be built. An input file which will automatically configure these steps can be downloaded :examplesgithub:`here <E12IstanbulRegionalSeismicRiskAnalysis/input.json>`.

#. **VIZ** The following snapshot of the visualization panel shows the assets which have been configured for this study, and their locations on a map of Istanbul, Turkey.

   .. figure:: figures/r2dt-0012-VIZ.png
      :width: 600px
   :alt: Screenshot of the "R2D: Regional Resilience Determination Tool" with a focus on a map interface. The map, which appears to use OpenStreetMap as a base layer, shows an urban area with various colored dots representing different types of buildings or assets. A legend on the left categorizes these by building type, such as commercial, government, industrial, and residential. A toolbar with icons for different functionalities lies across the top, and a side panel on the right provides options for data sources and layers. The interface includes options to identify, select, and analyze assets on the map as well as buttons to add and clear assets from the analysis list.
      :align: center


#. **GI** The following figure shows how the general information panel is configured to handle the units of our analysis and provide output corresponding to demand parameters, damage measures, and decision variables.

   .. figure:: figures/r2dt-0012-GI.png
      :width: 600px
   :alt: Screenshot of the R2D: Regional Resilience Determination Tool interface. It includes a login button in the top right corner. The page is divided into sections labeled 'General Information', 'Units', 'Asset Layers', and 'Output Settings'. The 'General Information' section has an 'Analysis Name' field filled with 'E12 - Istanbul Regional Seismic Risk Analysis'. Units specified are force in kips, length in inches, and time in seconds. Under 'Asset Layers', 'Buildings' is checked, among other unchecked options including Soil, Gas Network, Water Network, Waste Network, and Transportation Network. Under 'Output Settings', checkboxes are marked for Engineering demand parameters (EDP), Damage measures (DM), Decision variables (DV), and Output EDP, DM, and DV every sampling realization, as well as 'Output Asset Information Model (AIM)' and 'Output site IM'.
      :align: center


#. **HAZ** Next, in the hazard panel, the :examplesgithub:`EventGrid.csv </E12IstanbulRegionalSeismicRiskAnalysis/input_data/GroundMotionData/Seismograms/EventGrid.csv>` 
   file is loaded pointing to the suite of simulated ground motions which are used for the procedure.

   .. figure:: figures/r2dt-0012-HAZ.png
      :width: 600px
   :alt: Screenshot of a software interface with a sidebar on the left listing categories like VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES. The main panel is titled "Hazard Selection" with a dropdown menu for "User Specified Ground Motions" and two fields displaying file paths for "Event File Listing Motions" and "Folder Containing Motions", both pointing to directories on a C: drive. Below is a section titled "Units of Event Input File" with fields labeled "TH_file," "Gravitational constant (g)," and "factor," the latter being described as "Unitless (scalar)." The interface has a minimalistic design with a color scheme primarily in shades of blue and gray.
      :align: center

#. **ASD** Now a few buildings of interest can be singled out from the building inventory as shown in the following figure where the **CSV to BIM** option is selected as our backend.

   .. figure:: figures/r2dt-0012-ASD.png
      :width: 600px
   :alt: Screenshot of a computer interface titled "Regional Building Inventory," displaying a table of building information. The table includes columns for Building_ID, Longitude, Latitude, PlanArea, NumberOfStories, YearBuilt, Quality, OccupancyClass, and StructureType. The data shown includes a list of buildings with varying plan area sizes, number of stories, years built, and other attributes. Several menu options and tabs such as VIZ, GI, HAZ, ASD, and others are visible, suggesting it's part of a larger application, possibly related to urban planning or seismic risk analysis.
      :align: center

#. **HTA** Next, a hazard mapping algorithm is specified using the **Nearest Neighbor** method and the **SimCenterEvent** application, which are configured as show in the following figure with **5** samples in **4** neighbors.

   .. figure:: figures/r2dt-0012-HTA.png
      :width: 600px
   :alt: Screenshot of a user interface for a "Hazard to Local Asset Event" application showing the "Regional Mapping" section. It includes a "Mapping Application" dropdown menu with "Nearest Neighbour" selected, input fields for "Number of samples" set to 5, "Number of neighbors" set to 4, and "Seed" set to 624. On the left-hand side, there is a vertical menu with various abbreviated options such as VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES, with HTA highlighted in blue.
      :align: center

#. **MOD** Now the building modeling procedure is configured with the **CustomPy** backend.

   .. figure:: figures/r2dt-0012-MOD.png
      :width: 600px
   :alt: A screenshot of a Building Modeling software interface with a sidebar menu on the left and a main panel on the right. The sidebar menu includes options like VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES. The main panel displays "Building Modeling" at the top with fields for "Input Script," indicating a file path on a computer, "Response Nodes," "Spatial Dimension," "Number of Degrees of Freedom at Nodes," and "Damping Ratio," with values entered for some fields.
      :align: center


#. **ANA** In the analysis panel, **CustomPy-Simulation** is selected from the primary dropdown.

   .. figure:: figures/r2dt-0012-ANA.png
      :width: 600px
   :alt: A screenshot of a software interface showing a sidebar with various abbreviated options like VIZ, GI, HAZ, ASD, HTA, MOD, ANA (highlighted in light blue), DL, UQ, RV, and RES. The main area of the interface has a heading 'Building Analysis Method' with a dropdown menu currently displaying 'CustomPy-Simulation'. The rest of the interface is predominantly empty with a grey and white color scheme.
      :align: center


#. **DL**  The damage and loss panel is now used to configure the **Pelicun3** backend. The **HAZUS MH EQ Story** damage and loss method is selected and configured as shown in the following figure.

   .. figure:: figures/r2dt-0012-DL.png
      :width: 600px
   :alt: A screenshot of a software interface titled "Building Damage & Loss Application" displaying options for the "Pelican Damage and Loss Prediction Methodology." The interface includes a selection menu with the option "HAZUS MH EQ Story" chosen for the Damage and Loss Method and settings including "Event time: off," "Number of realizations: 10," with additional options such as "Output detailed results," "Log file" (checked), "Coupled EDP," and "Include ground failure." The menu on the left highlights the section "DL" in teal, with other sections like "VIZ," "GI," "HAZ," and more listed above and below it.
      :align: center

#. **UQ** Now nearing the end of our journey, it is time to configure the venerable **Dakota** uncertainty quantification engine to carry out our latin hypercube sampling procedure **5** samples and an arbitrary seed for reproducibility.

   .. figure:: figures/r2dt-0012-UQ.png
      :width: 600px
   :alt: Screenshot of a software interface with a sidebar on the left side with various menu options such as VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ (highlighted), RV, and RES. On the right side, there is a titled section "UQ Application" with drop-down options and checkboxes for Dakota Method Category, Method, # Samples, and Seed. The Dakota Method Category is currently set to "Forward Propagation" with options for "Parallel Execution" and "Save Working dirs" available as checkboxes. The Method is set to "LHS," with "5" entered as the number of samples and "868" as the seed value. The rest of the interface is minimalistic, with a gray and white color scheme.
      :align: center

#. **RV** For the problem at hand we elect to decline the services of the random variable panel and proceed to our journey's end with a swift click of the **Run** button.


.. [ZhangEtAl2021] 
   Zhang, W., Restrepo, D., Crempien, J. G., Erkmen, B., Taborda, R., Kurtulus, A., & Taciroglu, E. (2021). A computational workflow for rupture‐to‐structural‐response simulation and its application to Istanbul. Earthquake Engineering & Structural Dynamics, 50(1), 177-196.
  
.. [ZhangEtAl2023-1] 
   Zhang, W., Crempien, J., Kurtulus, A., Chen, P., Arduino, P., Taciroglu, E. (2023), A suite of broadband physics-based ground motion simulations for the Istanbul region, Earthquake Engineering and Structural Dynamics
   
.. [ZhangEtAl2023-2] 
   Zhang, W., Chen, P., Crempien, J., Kurtulus, A., Arduino, P., Taciroglu, E. (2023), Regional-scale seismic fragility, loss, and resilience assessment using physics-based simulated ground motions: an application to Istanbul, Earthquake Engineering and Structural Dynamics

.. [ZhangEtAl2023-3] 
   Zhang, W., Crempien, J., Zhong, K., Chen, P., Arduino, P., Taciroglu, E. (2023) "A suite of 57 broadband physics-based ground motion simulations for the Istanbul region", in Regional-scale physics-based ground motion simulation for Istanbul, Turkey. DesignSafe-CI. https://doi.org/10.17603/ds2-e7nq-8d52 v1
