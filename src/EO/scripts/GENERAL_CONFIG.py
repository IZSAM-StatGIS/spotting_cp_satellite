import os

# GENERAL PARAMS
year = '2022'
region = 'Abruzzo'
script_path = os.path.dirname(__file__)
sample_points_dir = os.path.join(os.path.dirname(script_path), 'VECTOR_DATA')
# MODIS PATHS
modis_dir = os.path.join(os.path.dirname(script_path), 'MODIS_SAMPLES')
modis_cropped_dir = os.path.join(os.path.dirname(script_path), 'MODIS_20M_CROPPED', year)
# SENTINEL PATHS
download_dir = os.path.join(os.path.dirname(script_path), 'S2_DOWNLOAD', year, region)
extracted_dir = os.path.join(os.path.dirname(script_path), 'S2_20M_EXTRACTED', year, region)
cropped_dir = os.path.join(os.path.dirname(script_path), 'S2_20M_CROPPED', year)
