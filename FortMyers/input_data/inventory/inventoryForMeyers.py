import sys
sys.path.insert(0, "../../")
import numpy as np
from brails.utils import Importer

LOCATION_NAME = 'Fort Myers Beach, FL'
INVENTORY_OUTPUT = 'BuildingInventory.geojson'
NO_POSSIBLE_WORLDS = 1

importer = Importer()

region_data = {"type": "locationName", "data": LOCATION_NAME}
region_boundary_class = importer.get_class("RegionBoundary")
region_boundary_object = region_boundary_class(region_data)

nsi_class = importer.get_class('NSI_Parser')
nsi = nsi_class()
nsi_inventory = nsi.get_raw_data(region_boundary_object)

scraper_class = importer.get_class('MS_FootprintScraper')
scraper = scraper_class({'length': 'ft'})
scraper_inventory = scraper.get_footprints(region_boundary_object)



nsi_inventory = nsi.get_filtered_data_given_inventory(
    scraper_inventory, "ft", get_extended_features=True)

knn_imputer_class = importer.get_class("KnnImputer")

imputer = knn_imputer_class(
    nsi_inventory, n_possible_worlds=NO_POSSIBLE_WORLDS,
    exclude_features=['lat', 'lon', 'fd_id'])
large_imputed_inventory = imputer.impute()

imputed_inventory = large_imputed_inventory.get_random_sample(20, 40)

# Get aerial imagery using GoogleSatellite:
google_satellite_class = importer.get_class('GoogleSatellite')
google_satellite = google_satellite_class()
images_aerial = google_satellite.get_images(imputed_inventory,
                                            'tmp/satellite/')

roof_shape_classifier_class = importer.get_class('RoofShapeClassifier')
roof_shape_classifier = roof_shape_classifier_class()
predictions = roof_shape_classifier.predict(images_aerial)


for key, val in imputed_inventory.inventory.items():
    val.add_features({'DesignWindSpeed': 159,
                      'FloodZone': 'AE',
                      'DesignLevel':'E',
                      'BuildingType':3001,
                      'RoofShape': predictions[key]})

imputed_inventory.change_feature_names({'erabuilt': 'YearBuilt',
                                        'constype': 'BuildingMaterial',
                                        'numstories': 'NumberOfStories',
                                        'occupancy':'OccupancyClass',
                                        'splitlevel':'SplitLevel',
                                        'found_ht':'FirstFloorElevation',
                                        'fparea':'PlanArea',
                                        'basement':'Basement'})

# imputed_inventory.print_info()

#
# infer needed attributes
#

windInfererClass = importer.get_class("HazusInfererWind")
infererWind = windInfererClass(
    input_inventory=imputed_inventory, clean_features=False)


hazus_inferred_wind_inventory = infererWind.infer()


waterInfererClass = importer.get_class("HazusInfererFlood")
waterInferer = waterInfererClass(
    input_inventory=hazus_inferred_wind_inventory, clean_features=False)

hazus_inferred_combined_inventory = waterInferer.infer()


#waterImputer = knn_imputer_class(hazus_inferred_combined_inventory,
#                            n_possible_worlds=NO_POSSIBLE_WORLDS)

#hazus_inventory_final = waterImputer.impute()

_ = hazus_inferred_combined_inventory.write_to_geojson(
    output_file=INVENTORY_OUTPUT)

print('DONE')
