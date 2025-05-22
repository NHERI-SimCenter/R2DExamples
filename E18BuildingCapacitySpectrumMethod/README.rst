E18 - Capacity Spectrum Method for Earthquake Assessment of Buildings
======================================================================

+-----------------+------------------------------------------------------------+
| Download files  | :examplesgithub:`Download <E18BuildingCapacitySpectrumMethod/>`       |
+-----------------+------------------------------------------------------------+


.. _Example 1: https://nheri-simcenter.github.io/R2D-Documentation/common/user_manual/examples/desktop/E1BasicHAZUS/README.html

.. _GitHub: https://github.com/NHERI-SimCenter/SimCenterBackendApplications/tree/f692b3e3f1bcea5a012870ece3e9331315763455/modules/performSIMULATION/capacitySpectrum

This earthquake example demonstrates utilizing the FEMA HAZUS Capacity Spectrum Method for building damage assessment.

This example builds upon material presented in `Example 1`_. The area of interest is downtown San Francisco. The input for the event is an IM (PSA 0.3 second and 1.0 second) field for a Mw7.05 event on the Hayward fault which was obtained using R2D's earthquake event generation tool. Damage to the houses is determined using the HAZUS capacity spectrum and damage and loss methodology.


The material presented for this example is focused on the inputs to capacity spectrum method. Inputs for the Hazard, Assets, etc. as is shown and discussed in the other examples discussed and as such the reader is directed to those examples for understanding of inputs required. In this example we will be outlining the inputs in the **ANA** panel to run capacity spectrum.

#. **ANA** The visualization panel in the following figure shows the inputs for capacity spectrum. The input include a demand model, a capacity model and a damping model. The demand model defines the shape of a 5% damping earthquake response spectrum. The R2D implementation of the capacity spectrum method uses the response spectrum shape defined in FEMA HAZUS where SA 0.3s and SA1.0s are used as the anchor points for the spectrum. The capacity model is a set of equations that define the "push-over" curve for the buildings. Based on building type (e.g., W1, S1, C1, etc.) and design level (e.g., Pre-Code, Low-Code, High-Code, etc.) defined in HAZUS, the yield point and ultimate point of the pushover curves are provided by HAZUS. The shape of the pushover curve is defined as a elliptic curve as suggested by Cao and Peterson [cao2006]_. The damping model is used to modify the response spectrum to account for the effects of damping. R2D selects damping values based on the building type as suggested in Cao and Peterson [cao2006]_. The source code of the models are in SimCenter's backend applications `GitHub`_ repository, if users are interested at reading and modifying the models and assumptions.

.. [cao2006]
	Cao, T., & Petersen, M. D. (2006). Uncertainty of earthquake losses due to model uncertainty of input ground motions in the Los Angeles area. Bulletin of the Seismological Society of America, 96(2), 365-376.

   .. figure:: figures/ANA.png
      :width: 800px
      :align: center
