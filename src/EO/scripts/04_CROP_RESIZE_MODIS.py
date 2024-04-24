'''
Name: CROP_RESIZE_MODIS.py
Author: Alessio Di Lorenzo
Description:   
    Given a point shapefile and a raster image, the procedure:
        1) reprojects the vector data to the raster projection
        2) retrieves the footprint of the raster image
        3) creates buffers around the points and their envelope
        4) selects only envelopes that overlap with the raster image footprint
        5) clips the raster with the selected envelopes
        6) normalizes the clips by setting cell values between 0 and 1
        7) warping
'''

import rasterio
from osgeo import gdal
from shapely.geometry import box, shape
from rasterio.plot import show
from pyproj import CRS
import geopandas as gpd
import os, sys
import json
from datetime import date, datetime
from GENERAL_CONFIG import year, modis_dir, sample_points_dir, modis_cropped_dir

# Sample Points GeoDF
wgs84_points = gpd.read_file(os.path.join(sample_points_dir, 'sample_points.shp'))
buffer_radius = 2240

# MODIS ARCHIVE
LSTD_ARCHIVE = os.path.join(modis_dir, r'DEF_022') #UTM33
LSTN_ARCHIVE = os.path.join(modis_dir, r'DEF_023') #UTM33

# Create cropped_dir if not exists
if not os.path.exists(modis_cropped_dir):
	os.makedirs(modis_cropped_dir)

# List with images to crop
images = []
for archive_dir in [LSTD_ARCHIVE, LSTN_ARCHIVE]:
    for root, dirs, files in os.walk(archive_dir):
        for name in files:
            if year in name:
                images.append(os.path.join(root, name))

print("Starting crop at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Crop images
# pylint: disable=maybe-no-member
for image in images:
	raster = rasterio.open(image, driver='GTiff')
	# raster footprint
	l = raster.bounds[0]
	b = raster.bounds[1]
	r = raster.bounds[2]
	t = raster.bounds[3]
	# box(minx, miny, maxx, maxy, ccw=True)
	b = box(l,b,r,t)
	# Creation of the geodataframe from the raster footprint polygon
	footprint_gdf = gpd.GeoDataFrame(gpd.GeoSeries(b), columns=['geometry'])
	# Input points reprojection
	crs = CRS('EPSG:32633')
	punti_utm = wgs84_points.to_crs(crs)
	# Buffer operation
	buffer_gs = punti_utm.buffer(buffer_radius)
	buffer_gdf = gpd.GeoDataFrame({'buffer_geom':buffer_gs}, geometry='buffer_geom')
	# Create a GeoSeries by calculating the envelope of the buffer
	envelope_gs = gpd.GeoSeries(buffer_gdf['buffer_geom'].envelope)
	# Add a column with the geometry of the envelopes to the points geodataframe
	punti_utm['envelope_geometry'] = envelope_gs
	# Removal of the point geometry
	punti_utm.drop('geometry', axis=1, inplace=True)
	# Create a new geodataframe with the envelopes
	punti_utm_envelope = gpd.GeoDataFrame(punti_utm, geometry='envelope_geometry')
	punti_utm_envelope.crs = crs
	# Find the envelopes entirely contained within the footprint
	within = punti_utm_envelope[punti_utm_envelope.within(footprint_gdf.geometry[0])]
	# Crop
	print("Crop start for {0}".format(raster.name))
	geometries = json.loads(within.to_json())
	for i in geometries['features']:
		geom = i['geometry']
		cod_azi = i['properties']['COD_AZIEND']
		region = i['properties']['REGIONE']
		# Raster clipping using GDAL Translate and the bounding box of the envelope polygon
		geom_bbox = [b for b in shape(geom).bounds]
		minX = geom_bbox[0]
		minY = geom_bbox[1]
		maxX = geom_bbox[2]
		maxY = geom_bbox[3]
		# Output file name
		if "DEF_022" in raster.name:
			cropped_name = "LSTD_"+raster.name[71:84]+"_"+str(cod_azi).replace('.tif', '')
		elif "DEF_023" in raster.name:
			cropped_name = "LSTN_"+raster.name[71:84]+"_"+str(cod_azi).replace('.tif', '')
		# Create output path if not exists
		cropped_path = os.path.join(modis_cropped_dir, region)
		if not os.path.exists(cropped_path):
			os.makedirs(cropped_path)
		cropped_image = os.path.join(cropped_path, cropped_name+".tif") 
		# Warping
		gdal.Warp(cropped_image, raster.name, format="GTiff", outputBounds=[minX, minY, maxX, maxY], xRes=20, yRes=20)
		
print("Crop finished at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	
	