
E7 - Hurricane Wind + Water
=============================

+-----------------+-----------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E7HurricaneWindWater/>`              |
+-----------------+-----------------------------------------------------------------+

This example presents a coupled damage assessment for hurricane wind and water inundation hazards. Approximately 6600 buildings are considered in the city of Atlantic City, NJ.

.. figure:: r2dt-0007.png
   :width: 400px
   :alt: A detailed map view of a coastal urban area featuring numerous blue-shaded buildings, indicating a focus on the built environment, possibly for planning or analysis purposes. The area is labeled with street names and notable locations, such as Chelsea Heights and Boardwalk Hall. There are annotations and markings that suggest geographic data points or infrastructure elements, scattered across the land adjacent to the coastline. The map is centered around Atlantic City, as indicated by the labels and landmarks.
   :align: center

#. **VIZ** This example shows the simulation for a pseudo hurricane scenario in Atlantic City, NJ. The damage and loss of a sample of buildings in Atlantic City due to wind and water inundation are estimated.  The results presented herein are only for demonstrating the use of R2DTool and do not serve as an accurate representation of the real losses.

   .. figure:: figures/r2dt-0007-VIZ.png
      :width: 600px
   :alt: Screenshot of a Geographic Information System (GIS) software interface displaying a map with a grid overlay, presumably representing hurricane data. Various layers, including a Hurricane Grid and Buildings, are visible in the layer panel on the left side, along with a variety of controls and tools for map analysis. The map shows a coastal area with inland water bodies and a delineation of areas perhaps affected by a hurricane event, marked with a color-coded grid. The interface also includes various GIS data source options such as OpenStreetMap, GeoPackage, PostgreSQL, and others listed in a sidebar.
      :align: center


#. **GI** Next, the general information panel is used to broadly characterize the problem at hand. In this example, the imperial force and length units are used, and we're interested in the engineering demand parameters, damage measures, and the resulting decision variable (e.g., expected replacement cost).

   .. figure:: figures/r2dt-0007-GI.png
      :width: 600px
   :alt: Screenshot of a software interface with a section titled "General Information" showing an analysis setup. The analysis name is "E7 - Hurricane Wind + Water," with units set to "Kips" for force, "Feet" for length, and "Seconds" for time. Below, under "Asset Layers," the "Buildings" checkbox is ticked, and other options like "Soil," "Gas Network," and "Water Network" are available but not selected. In the "Output Settings," checkboxes for "Engineering demand parameters (EDP)," "Damage measures (DM)," "Decision variables (DV)," and options to output various data every sampling realization and "Asset Information Model (AIM)" are selected. The software contains additional menu options on the left side like "VIZ," "GI," "HAZ," and others, indicating a complex analysis tool possibly used for risk assessment or disaster management planning.
      :align: center


#. **HAZ** Now, in the hazard panel, the **User Specified Hurricane** option is selected, which allows for the use of pre-generated hurricane wind field scenarios. The following figure shows the relevant example files, which are now entered in this pane. The peak wind speed is used as the intensity measure to quantify the potential hurricane effects.

   .. figure:: figures/r2dt-0007-HAZ.png
      :width: 600px
   :alt: A screenshot of a software interface involving 'Hazard Selection'. There are two input fields with pre-filled file paths: one for 'Event File Listing Wind Field' and another for 'Folder Containing Wind Field Stations'. To the right of each path, there are 'Browse' buttons. On the left part of the screen, there is a vertical navigation bar with various options such as VIZ, GI, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES, with HAZ highlighted as the current selection. The overall interface is simple, with a color scheme of blues, whites, and grays.
      :align: center


#. **ASD** In the asset definition panel, the path to the ``AtlanticBuildingInventory.csv`` file is specified. Once this file is loaded, the user can select which particular assets will be included in the analysis by entering a valid range in the form and clicking **Select**. For this example, the range **1-20** is used to include all buildings. The ``AtlanticBuildingInventory.csv`` includes parameters for the damage and loss assessment (i.e., number of stories, year of built, occupancy class, structure type, plan area, replacement cost, and population).

   .. figure:: figures/r2dt-0007-ASD.png
      :width: 600px
   :alt: Screenshot of a Regional Building Inventory spreadsheet with columns for id, latitude, longitude, building ID, address, city, state, occupancy class, and building class. Rows are populated with example data, including numerical IDs, coordinate values, and addresses all located in Absecon, NJ. The document has functionality buttons like "CSV to AIM," "Browse," "Advanced Filter," and "Clear Selection." The screenshot displays assets with IDs 1 to 15.
      :align: center

#. **HTA** Next, a hazard mapping algorithm is specified using the **Nearest Neighbor** method and the **SimCenterEvent** application, configured as shown in the following figure with **10** samples in **4** neighbours.

   .. figure:: figures/r2dt-0007-HTA.png
      :width: 600px
   :alt: Screenshot of a user interface with a sidebar menu on the left and a form titled "Building Mapping" on the right. The sidebar menu contains options such as VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES, with HTA being highlighted. The form includes fields for "Number of samples" set to 10, "Number of neighbors" set to 4, and "Seed" set to 75. There is a dropdown titled "Nearest Neighbour" at the top of the form, indicating a selection or setting related to the mapping function.
      :align: center

#. **MOD** In the building modeling panel, simply leave the first dropdown box set to **None**.

   .. figure:: figures/r2dt-0007-MOD.png
      :width: 600px
   :alt: Screenshot of a user interface with a sidebar on the left containing acronyms such as VIZ, GI, HAZ, ASD, HTA, highlighted "MOD", ANA, DL, UQ, RV, and RES. The main area of the interface is titled "Building Modeling" with a dropdown menu set to "None". There's also an information icon on the top right corner of the main area. The interface has a minimalistic design with a color scheme of grey and a blue highlight for the selected option "MOD".
      :align: center

#. **ANA** In the analysis panel, **IMasEDP** is selected from the primary dropdown.

   .. figure:: figures/r2dt-0007-ANA.png
      :width: 600px
   :alt: Screenshot of a software interface with a dark sidebar on the left, listing categories such as VIZ, GI, HAZ, ASD, HTA, MOD, ANA highlighted in blue, DL, UQ, RV, and RES. On the top right, there is a header that says "Building Analysis Engine," with a progress bar and an option to minimize or close the window. The main area of the interface is blank.
      :align: center

#. **DL** The damage and loss panel is now used to configure the **Pelicun3** backend. The **HAZUS MH EQ HU** damage and loss method is selected and configured as shown in the following figure:

   .. figure:: figures/r2dt-0007-DL.png
      :width: 600px
   :alt: A screenshot of a software interface titled "Building Damage & Loss Application" with a selection of parameters under the heading "Pelican Damage and Loss Prediction Methodology." Options include "Damage and Loss Method: HAZUS MH HU," "Event time: off," "Number of realizations: 5000," with checkboxes for "Output detailed results," "Log file," and "Coupled EDP" selected. An 'Auto-populate script' field contains a file path, and there is a "Browse" button to the right of this field. The interface includes a navigation menu on the left with options like "VIZ," "GI," "HAZ," and others, with "DL" highlighted in blue.
      :align: center

#. **UQ** For this example the **UQ** dropdown box should be set to **None**.

   .. figure:: figures/r2dt-0007-UQ.png
      :width: 600px
   :alt: Screenshot of a user interface with a menu on the left side showing various abbreviated options such as VIZ, GI, HAZ, ASD, HTA, MOD, ANA, DL, UQ, RV, and RES. The option labeled UQ is highlighted in blue, indicating selection. On the top right, there's a header that reads "UQ Application" with a dropdown menu indicating "None" and an icon suggesting additional settings or actions. The rest of the interface is predominantly gray with no text or images visible in the main content area.
      :align: center

#. **RV**

   The random variable panel will be left empty for this example.

