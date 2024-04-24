'''
Name: CROP_NORM_S2_GDAL.py
Author: Alessio Di Lorenzo
Description:   
    Given a point shapefile and a raster image, the procedure:
        1) reprojects the vector data to the raster projection
        2) retrieves the footprint of the raster image
        3) creates buffers around the points and their envelope
        4) selects only envelopes that overlap with the raster image footprint
        5) clips the raster with the selected envelopes
        6) normalizes the clips by setting cell values between 0 and 1
        7) organizes the crops into subfolders named after the region attribute 'REGIONE'.
'''

import rasterio
from osgeo import gdal, gdal_array
from shapely.geometry import box, shape
from rasterio.plot import show
from pyproj import CRS
import geopandas as gpd
import os
import json
from datetime import date, datetime
from GENERAL_CONFIG import extracted_dir, sample_points_dir, cropped_dir

# Sample Points GeoDF
wgs84_points = gpd.read_file(os.path.join(sample_points_dir, 'sample_points.shp'))
buffer_radius = 2240

# Create cropped_dir if not exists
if not os.path.exists(cropped_dir):
	os.makedirs(cropped_dir)

print("Starting crop at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

images = []
for root, dirs, files in os.walk(extracted_dir):
	for name in files:
		if name.endswith('.jp2'):
			images.append(os.path.join(root, name))

# Crop images
# pylint: disable=maybe-no-member
for image in images:
	print(image)
	raster = rasterio.open(image, driver='JP2OpenJPEG')
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
		cropped_name = raster.name[-34:-4]+"_"+str(cod_azi)
		cropped_name = cropped_name.replace("_20m","")
		# Create the output file path if it does not exist
		cropped_path = os.path.join(cropped_dir,region)
		if not os.path.exists(cropped_path):
			os.makedirs(cropped_path)
		cropped_image = os.path.join(cropped_path, cropped_name+".png") 
		# Translate
		gdal.Translate(cropped_image, raster.name, format="PNG", projWin = [minX, maxY, maxX, minY])
		# Normalize
		print('Normalize pixel values')
		ds = gdal.Open(cropped_image)
		band = ds.GetRasterBand(1)
		arr = band.ReadAsArray().astype('f4')
		data = arr/10000 	# divide by 10000
		data[data > 1] = 1	# set to 1 all the values greater than 1
		output_image = os.path.join(cropped_path, cropped_name+".tiff") 
		gdal_array.SaveArray(data.astype("float32"), output_image, "GTIFF", ds)
		ds = None
		print('Remove not normalized file')
		if os.path.exists(cropped_image):
			os.remove(cropped_image)
			os.remove(os.path.join(cropped_path, cropped_name+".png.aux.xml"))
print('Crop finished at: '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))