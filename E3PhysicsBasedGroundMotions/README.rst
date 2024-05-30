
E3 - Physics-based Ground Motions
=================================

+-----------------+--------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E3PhysicsBasedGroundMotions/>`    |
+-----------------+--------------------------------------------------------------+

This example features ground motion acceleration time histories simulated using the SW4 software and a detailed geophysical model of the San Francisco Bay Area by the Lawrence Livermore National Laboratory (https://doi.org/10.1785/0220180261). The ground motions are used to investigate the impact of a Mw7.0 earthquake on the Hayward fault in the city of Berkeley. Engineering Demand Parameters are simulated with an idealized MDOF building model; building performance is evaluated at the story level based on the HAZUS earthquake damage and loss assessment methodology.

.. figure:: r2dt-0003.png
   :width: 400px
   :alt: A detailed satellite map depicting an urban grid of streets and blocks with numerous buildings in Berkeley, California. Colors vary across the image, with shades of blue representing different types of buildings or areas, such as the dark blue of the University of California, Berkeley campus, and the lighter blue for other buildings and blocks. The map includes street names such as University Avenue and Center Street, along with landmarks like Berkeley High School and the Martin Luther King Jr. Civic Center Park.
   :align: center

.. note::
   This example uses simulated ground motion time histories from the Lawrence Livermore National Lab. Due to size constraints, only the time histories near Berkeley are bundled with R2D. The complete set of simulated ground motions is available at https://berkeley.box.com/s/65113pqclc2j29ve9alita5kr7q2jnwc . After downloading the zip file, extract its contents to the SW4 folder under input_data.


Modeling Procedure
------------------

We now embark on our journey through the input panels of R2D, making known to the workflow builder how our procedure should be built. An input file that will automatically configure these steps can be downloaded :examplesgithub:`here <E3PhysicsBasedGroundMotions/input.json>`.

#. **VIZ** The following snapshot of the visualization panel shows the assets which have been configured for this study, and their locations on a map of Berkeley, CA.

   .. figure:: figures/r2dt-0003-VIZ.png
      :width: 600px
   :alt: This image shows a screenshot of a Geographic Information System (GIS) software interface with a map on the right side displaying a section of an urban area overlaid with various colored shapes representing different data layers, such as buildings. On the left side of the image, a panel with various GIS tool options and layer controls is visible. The map is detailed with streets, labels, and buildings, and colored shapes are presumably correlated with specific geographic or analytical information. The interface elements suggest analysis or data management tasks are being performed.
      :align: center


#. **GI** The following figure shows how the general information panel is configured to handle the units of our analysis and provide output corresponding to demand parameters, damage measures, and decision variables.

   .. figure:: figures/r2dt-0003-GI.png
      :width: 600px
   :alt: A screenshot of a user interface for a physics-based ground motions analysis program. The "General Information" section includes an "Analysis Name" called E3 - Physics Based Ground Motions and specifies units for force in Newtons, length in meters, and time in seconds. Under "Asset Layers," the option for "Buildings" is checked. The "Output Settings" section has options selected for "Engineering demand parameters (EDP)," "Damage measures (DM)," and "Decision variables (DV)," along with two other output options related to sampling realization and asset information models. There are various tabs and menu options on the left, with acronyms such as VIZ, GI, HAZ, and others, indicating different sections of the software. The main focus of the interface is on configuring settings for an analysis of ground motions and their impact on buildings.
      :align: center


#. **HAZ** Next, in the hazard panel, the :examplesgithub:`EventGrid.csv </E3PhysicsBasedGroundMotions/input_data/SW4/EventGrid.csv>` file is loaded pointing to the suite of SW4 ground motions which are used for the procedure.

   .. figure:: figures/r2dt-0003-HAZ.png
      :width: 600px
   :alt: Screenshot of a software interface with a section labeled "Hazard Selection" at the top, including fields labeled "Event File Listing Motions" and "Folder Containing Motions," each showing file paths, with "Browse" buttons on the right. On the left sidebar, several abbreviated section names such as VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES are visible, highlighted in blue and gray tones. No personal or sensitive information is displayed.
      :align: center

#. **ASD** Now a few buildings of interest can be singled out from the building inventory as shown in the following figure where the **CSV to BIM** option is selected as our backend.

   .. figure:: figures/r2dt-0003-ASD.png
      :width: 600px
   :alt: Screenshot of a data table titled "Regional Building Inventory" showing a list of buildings with columns for ID, Latitude, Longitude, Replacement Cost, Plan Area, Year Built, Number of Stories, Occupancy Class, and Structure Class. The data appear to be related to a building assessment or inventory system with several rows visible containing numerical and text entries for various building attributes. The interface includes options for saving to CSV, browsing for an asset file, and applying filters.
      :align: center

#. **HTA** Next, a hazard mapping algorithm is specified using the **Nearest Neighbor** method and the **SimCenterEvent** application, which are configured as shown in the following figure with **4** samples in **3** neighbors.

   .. figure:: figures/r2dt-0003-HTA.png
      :width: 600px
   :alt: A screenshot of a user interface with a sidebar on the left featuring menu items like 'VIZ', 'GI', 'HAZ', 'ASD', with 'HTA' currently highlighted. On the right, there's a main content area titled 'Building Mapping' with subheading 'Nearest Neighbour'. Below this title, there are settings with fields labeled 'Number of samples' with a value of 4, 'Number of neighbors' with a value of 3, and 'Seed' with a value of 926. The interface has a clean and modern design with a muted color palette.
      :align: center

#. **MOD** Now the building modeling procedure is configured with the **MDOF-LU** backend where standard deviations of :math:`0.1` for stiffness and damping are defined.

   .. figure:: figures/r2dt-0003-MOD.png
      :width: 600px
   :alt: Screenshot of a software interface with a section titled "Building Modeling" featuring data input fields for Hazus data file, standard deviation of stiffness and damping, and default story height. The interface includes a reference section with two academic citations related to earthquake engineering and seismic simulations.
      :align: center


#. **ANA** In the analysis panel, **OpenSees** is selected from the primary dropdown.

   .. figure:: figures/r2dt-0003-ANA.png
      :width: 600px
   :alt: Screenshot of a software interface with a menu on the left side featuring options like "VIZ," "GI," "HAZ," and several others, with "ANA" highlighted. The main panel is titled "Building Analysis Method" and contains fields labeled Analysis, Integration, Algorithm, ConvergenceTest, Solver, Damping Model, Selected Tangent Stiffness with dropdowns, input fields, and informational icons, indicating settings for a simulation or analytical computation in a tool named OpenSees.
      :align: center


#. **DL**  The damage and loss panel is now used to configure the **Pelicun3** backend. The **HAZUS MH EQ Story** damage and loss method is selected and configured as shown in the following figure.

   .. figure:: figures/r2dt-0003-DL.png
      :width: 600px
   :alt: Screenshot of a user interface for a "Building Damage & Loss Application" named Pelicun3. The UI includes options for selecting a damage and loss prediction methodology, with "HAZUS MH EQ Story" chosen. Settings available include toggling event time, specifying the number of realizations as 1000, and options to output detailed results, log files, couple EDP, and include ground failure, with only the log file option checked. A sidebar on the left lists various menu options such as VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES, with "DL" highlighted.
      :align: center

#. **UQ** Now nearing the end of our journey, it is time to configure the venerable **Dakota** uncertainty quantification engine to carry out our Latin Hypercube Sampling (LHS) procedure **10** samples and an arbitrary seed for reproducibility.

   .. figure:: figures/r2dt-0003-UQ.png
      :width: 600px
   :alt: Screenshot of a user interface for an application named "UQ Application" with "Dakota" written next to it. The interface shows options for selecting a method, with "LHS" currently selected, entering the number of samples, where "3" has been entered, setting a seed number, which is "890", and a checked option to "Keep Samples". On the left side, there is a vertical navigation bar with various options highlighted including "UQ" in teal color indicating the current selection. The rest of the interface elements are greyed out, and the overall design is simple and utilitarian.
      :align: center

#. **RV** For the problem at hand we elect to decline the services of the random variable panel and proceed to our journey's end with a swift click of the **Run** button.


