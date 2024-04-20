#!/usr/bin/env python

import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
from rasterio.enums import Resampling
import pandas as pd
from shapely.geometry import Point
from tqdm import tqdm
import os

# Function to get nearest pixel value
def get_nearest_pixel(lon, lat, src):
    row, col = src.index(lon, lat)
    value = src.read(1, window=((row, row + 1), (col, col + 1)))
    return value[0, 0]

# Read shapefile
shapefile_path = '' #put shapefile path and name
gdf = gpd.read_file(shapefile_path)

# Read TIFF files
tiff_files = ['C:\\Users\\Hp\\D\\first.tif', 'C:\\Users\\D\\second.tif']  # Put all your tiff files
tiff_datasets = [rasterio.open(tiff) for tiff in tiff_files]

# Create an empty DataFrame to store results
result_df = pd.DataFrame(columns=['Longitude', 'Latitude'] + [os.path.splitext(os.path.basename(tiff))[0] for tiff in tiff_files])

# Iterate over each point in the shapefile
for index, row in tqdm(gdf.iterrows(), total=len(gdf), desc='Processing'):
    if row['geometry'] is None:
        continue  # Skip if geometry is None
    point = Point(row['geometry'].x, row['geometry'].y)
    lon, lat = point.x, point.y

    # Add longitude and latitude to the result DataFrame
    result_row = {'Longitude': lon, 'Latitude': lat}

    # Iterate over each TIFF file and get the nearest pixel value
    for i, tiff_ds in enumerate(tiff_datasets):
        tiff_name = os.path.splitext(os.path.basename(tiff_files[i]))[0]
        nearest_pixel_value = get_nearest_pixel(lon, lat, tiff_ds)
        result_row[tiff_name] = nearest_pixel_value

    # Append the result row to the DataFrame
    result_df = result_df.append(result_row, ignore_index=True)

# Save the result DataFrame to a CSV file
result_df.to_csv('C:\\Users\\Hp\\D\\result.csv', index=False)

# Close TIFF datasets
for tiff_ds in tiff_datasets:
    tiff_ds.close()


# In[ ]:




