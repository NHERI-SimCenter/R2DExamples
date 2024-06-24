
E12 - Istanbul Regional Seismic Risk Analysis
===============================================

+-----------------+-------------------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E12IstanbulRegionalSeismicRiskAnalysis/>`    |
+-----------------+-------------------------------------------------------------------------+

This example features a systematic regional seismic damage and loss assessment for Istanbul, Turkey. 
The ground motion acceleration time histories were simulated using the Hercules software and a detailed 
geophysical model of Istanbul region ([ZhangEtAl2021]_, [ZhangEtAl2023-1]_, [ZhangEtAl2023-2]_, [ZhangEtAl2023-3]_). The ground motions are used to investigate the 
impact of a Mw7.0 earthquake on the Central Marmara Basin fault. Engineering Demand Parameters are simulated 
with OpenSees models for individual reinforced concrete buildings in this example. Building damage and loss 
is evaluated the story-level based on the HAZUS earthquake damage and loss assessment methodology.

.. figure:: r2dt-0012.png
   :width: 400px
   :align: center

.. note::
   This example uses simulated ground motion time histories from the Hercules software. Due to size constraints, 
   only an example set of time histories are bundled with R2D. The complete set of simulated ground motions are 
   available at `DesignSafe PRJ-3712 <https://doi.org/10.17603/ds2-e7nq-8d52>`_.


Modeling Procedure
------------------

We now embark on our journey through the input panels of R2D, making known to the workflow builder how our procedure should be built. An input file which will automatically configure these steps can be downloaded :examplesgithub:`here <E12IstanbulRegionalSeismicRiskAnalysis/input.json>`.

#. **VIZ** The following snapshot of the visualization panel shows the assets which have been configured for this study, and their locations on a map of Istanbul, Turkey.

   .. figure:: figures/r2dt-0012-VIZ.png
      :width: 600px
      :align: center


#. **GI** The following figure shows how the general information panel is configured to handle the units of our analysis and provide output corresponding to demand parameters, damage measures, and decision variables.

   .. figure:: figures/r2dt-0012-GI.png
      :width: 600px
      :align: center


#. **HAZ** Next, in the hazard panel, the :examplesgithub:`EventGrid.csv </E12IstanbulRegionalSeismicRiskAnalysis/input_data/GroundMotionData/Seismograms/EventGrid.csv>` 
   file is loaded pointing to the suite of simulated ground motions which are used for the procedure.

   .. figure:: figures/r2dt-0012-HAZ.png
      :width: 600px
      :align: center

#. **ASD** Now a few buildings of interest can be singled out from the building inventory as shown in the following figure where the **CSV to BIM** option is selected as our backend.

   .. figure:: figures/r2dt-0012-ASD.png
      :width: 600px
      :align: center

#. **HTA** Next, a hazard mapping algorithm is specified using the **Nearest Neighbor** method and the **SimCenterEvent** application, which are configured as show in the following figure with **5** samples in **4** neighbors.

   .. figure:: figures/r2dt-0012-HTA.png
      :width: 600px
      :align: center

#. **MOD** Now the building modeling procedure is configured with the **CustomPy** backend.

   .. figure:: figures/r2dt-0012-MOD.png
      :width: 600px
      :align: center


#. **ANA** In the analysis panel, **CustomPy-Simulation** is selected from the primary dropdown.

   .. figure:: figures/r2dt-0012-ANA.png
      :width: 600px
      :align: center


#. **DL**  The damage and loss panel is now used to configure the **Pelicun3** backend. The **HAZUS MH EQ Story** damage and loss method is selected and configured as shown in the following figure.

   .. figure:: figures/r2dt-0012-DL.png
      :width: 600px
      :align: center

#. **UQ** Now nearing the end of our journey, it is time to configure the venerable **Dakota** uncertainty quantification engine to carry out our Latin hypercube sampling procedure **5** samples and an arbitrary seed for reproducibility.

   .. figure:: figures/r2dt-0012-UQ.png
      :width: 600px
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
