"""
Script to generate a BRAILS building inventory using NSI data.

Steps performed:
1. Define the geographic boundary for the target region using a location name.
2. Scrape building footprint geometries within the specified region.
3. Retrieve and spatially filter NSI building attribute data based on scraped
   footprints.
4. Impute missing building attributes using K-Nearest Neighbors (KNN)
   imputation.
5. Add additional features, including computed elevation and roof shape
   (based on occupancy).
6. Rename features to match BRAILS inference model requirements.
7. Apply HAZUS-based rulesets to infer wind vulnerability characteristics.
8. Apply HAZUS-based rulesets to infer flood vulnerability characteristics.
9. Export the final enriched inventory to a GeoJSON file.

Input:
    - LOCATION_NAME (str): Human-readable location for building inventory.
    - INVENTORY_OUTPUT (str): Name of the building inventory output file.
    - NO_POSSIBLE_WORLDS (int): Number of requested inventory realizations.

Output:
    - GeoJSON file containing the building inventory for LOCATION_NAME.

Dependencies:
    - BRAILS
    - Random (for roof type assignment for residential buildings)
"""

from brails.utils import Importer
import random
random.seed(10)


def simple_roof_type_assignment(occupancy: str) -> str:
    """
    Predict the roof type based on occupancy class.

    Parameters:
        occupancy (str):
            The occupancy class (e.g., 'RES1', 'RES2', etc.)

    Returns:
        str:
            Predicted roof type ('Gable', 'Hip', or 'Flat')
    """
    gable_or_hip_classes = {'RES1', 'RES3A', 'RES3B', 'RES3C'}

    if occupancy in gable_or_hip_classes:
        return random.choice(['Gable', 'Hip'])
    elif occupancy == 'RES2':
        return 'Gable'
    else:
        return 'Flat'


LOCATION_NAME = 'Fort Myers Beach, FL'
INVENTORY_OUTPUT = 'FortMyers_BRAILS_NSI_BuildingInventory.geojson'
NO_POSSIBLE_WORLDS = 0

importer = Importer()

# Step 1: Define region boundary:
region_data = {"type": "locationName", "data": LOCATION_NAME}
region_boundary_class = importer.get_class("RegionBoundary")
region_boundary_object = region_boundary_class(region_data)

# Step 2: Scrape building footprints:
scraper_class = importer.get_class('MS_FootprintScraper')
scraper = scraper_class({'length': 'ft'})
scraper_inventory = scraper.get_footprints(region_boundary_object)

# Step 3: Retrieve and filter NSI data:
nsi_class = importer.get_class('NSI_Parser')
nsi = nsi_class()
nsi_inventory = nsi.get_raw_data(region_boundary_object)
nsi_inventory = nsi.get_filtered_data_given_inventory(
    scraper_inventory, "ft", get_extended_features=True)

# Step 4: Impute missing data:
knn_imputer_class = importer.get_class("KnnImputer")
imputer = knn_imputer_class(
    nsi_inventory, n_possible_worlds=NO_POSSIBLE_WORLDS,
    exclude_features=['lat', 'lon', 'fd_id'])
imputed_inventory = imputer.impute()

# Step 5: Add fixed or computed features:
for key, val in imputed_inventory.inventory.items():
    val.add_features({'DesignWindSpeed': 159,
                      'RoofShape': simple_roof_type_assignment(
                          val.features['occupancy']),
                      'BuildingType': 3001,
                      'FirstFloorElevation':
                          (val.features['ground_elv'] +
                           val.features['found_ht'])
                      })

# Step 6: Rename features to make them compatible with BRAILS Inferers:
imputed_inventory.change_feature_names({'erabuilt': 'YearBuilt',
                                        'constype': 'BuildingMaterial',
                                        'numstories': 'NumberOfStories',
                                        'occupancy': 'OccupancyClass',
                                        'splitlevel': 'SplitLevel',
                                        'fparea': 'PlanArea',
                                        'basement': 'Basement'})

# Step 7: Apply HAZUS rulesets for wind:
windInfererClass = importer.get_class("HazusInfererWind")
infererWind = windInfererClass(
    input_inventory=imputed_inventory, clean_features=False)
hazus_inferred_wind_inventory = infererWind.infer()

# Step 8: Apply HAZUS rulesets for flood:
waterInfererClass = importer.get_class("HazusInfererFlood")
waterInferer = waterInfererClass(
    input_inventory=hazus_inferred_wind_inventory, clean_features=False)
hazus_inferred_combined_inventory = waterInferer.infer()

# Step 9: Write output
_ = hazus_inferred_combined_inventory.write_to_geojson(
    output_file=INVENTORY_OUTPUT)

print('DONE')
