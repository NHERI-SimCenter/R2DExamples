
E1 - Basic HAZUS
===========================

+-----------------+---------------------------------------------+
| Download files  | :examplesgithub:`Download <E1BasicHAZUS/>`  |
+-----------------+---------------------------------------------+

This earthquake example demonstrates rapid analysis capabilities with the HAZUS earthquake damage and loss assessment methodology. Building-level Damage and Losses (D&L) are calculated directly from Intensity Measures (IM) for 25 assets. The IM field that represents peak ground acceleration in the city of San Francisco, CA, from a Mw7.2 event on the San Andreas fault, was obtained from Probabilistic Seismic Hazard Analysis (PSHA).

.. figure:: r2dt-0001.png
   :width: 400px
   :align: center

This study will be defined by sequentially traversing the input panels of the **R2D** interface. However, as outlined in the online user's manual, these procedures can be serialized to and loaded immediately from a JSON file, which for this example may be found :examplesgithub:`here <E1BasicHAZUS/input.json>`.

#. **VIZ** The visualization panel in the following figure shows the location of the assets considered in this example.

   .. figure:: figures/r2dt-0001-VIZ.png
      :width: 600px
      :align: center


#. **GI** The unit system and asset type are prescribed in this panel, and we're interested in the **building engineering demand parameters**, **damage measures**, and the resulting **decision variables**.

   .. figure:: figures/r2dt-0001-GI.png
      :width: 600px
      :align: center


#. **HAZ** Next, the hazard panel is used to load the event grid ``.csv`` file (:examplesgithub:`view on Github <E1BasicHAZUS/input_data/San_Andreas_Mw72_filtered/EventGrid.csv>`) which lists out the ground motions which are used as the ground acceleration time history inputs in this example.

   .. figure:: figures/r2dt-0001-HAZ.png
      :width: 600px
      :align: center


#. **ASD** In the asset definition panel, the path to the :examplesgithub:`SanFranciscoBuildings.csv <E1BasicHAZUS/input_data/SanFrancisco_buildings.csv>` file is specified. Once this file is loaded, the user can select which particular assets will be included in the analysis by entering a valid range (e.g., 1-50) in the form and clicking **Select**. The ``SanFranciscoBuildings_full.csv`` file includes parameters for the damage and loss assessment (e.g., number of stories, year of built, occupancy class, structure type, and plan area) for more than 100,000 buildings in the community.

   .. figure:: figures/r2dt-0001-ASD.png
      :width: 600px
      :align: center


#. **HTA** Next, a hazard mapping algorithm is specified using the **Nearest Neighbor** method and the **SimCenterEvent** application, which are configured as shown in the following figure with **100** samples in **4** neighbors, i.e., randomly sampling 100 ground motions from the nearest four stations (each station has a large number of ground motion records specified in the **HAZ**).

   .. figure:: figures/r2dt-0001-HTA.png
      :width: 600px
      :align: center


#. **MOD** panel is not used for this procedure. The **Building Modeling** dropdown should be left set to **None**.

   .. figure:: figures/r2dt-0001-MOD.png
      :width: 600px
      :align: center

#. **ANA** In the analysis panel, **IMasEDP** is selected from the primary dropdown.

   .. figure:: figures/r2dt-0001-ANA.png
      :width: 600px
      :align: center


#. **DL** The damage and loss panel is now used to configure the **Pelicun3** backend. The **HAZUS MH EQ IM** damage and loss method is selected and configured as shown in the following figure:

   .. figure:: figures/r2dt-0001-DL.png
      :width: 600px
      :align: center


#. **UQ** For this example the **UQ** dropdown box should be set to **None**.

   .. figure:: figures/r2dt-0001-UQ.png
      :width: 600px
      :align: center
	  
#. **RV**

   The random variable panel will be left empty for this example.


