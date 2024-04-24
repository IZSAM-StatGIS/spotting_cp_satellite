'''
Name: DOWNLOAD_S2.py
Author: Alessio Di Lorenzo
Description: Download S2 images from scihub (deprecated)
'''

from collections import OrderedDict
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime
from calendar import monthrange
import os
from TILES_SCHEMA import selectImages
from GENERAL_CONFIG import region, year, download_dir

# Connection variables
HUB_URL = "https://apihub.copernicus.eu/apihub"
USERNAME = "your_hub_username"
PASSWORD = "your_hub_password"

# Search variables
platform = 'Sentinel-2'
product = 'S2MSI2A'
tiles = selectImages(region)

# API Connection
api = SentinelAPI(USERNAME, PASSWORD, HUB_URL)

# Create download_dir if not exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Query arguments
query_kwargs = {
    'platformname': platform,
    'producttype': product,
    'date': ('20220701', '20220710') # date range tuple 
}

# Search s2 images for each tile of the choosen region
products = OrderedDict()
for tile in tiles:
	kw = query_kwargs.copy()
	kw['filename'] = '*_{}_*'.format(tile)
	pp = api.query(**kw)
	products.update(pp)

# Download
if len(products) > 0:
	size = api.get_products_size(products)
	print("Images found: {0}".format(len(products)))
	print("Total size of the download: {0} GB".format(size))
	uuids = [uuid for uuid, prod in products.items()]
	print("\n"+"Download started at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	api.download_all(products, download_dir, max_attempts=5)
	print ("Check download errors and retry: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	for uuid in uuids:
		api.download(uuid, download_dir, checksum=True)
	print ("Download finished at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
else:
	print("No images to download")