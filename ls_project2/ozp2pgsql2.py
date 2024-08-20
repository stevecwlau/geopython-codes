from owslib.wfs import WebFeatureService
from requests import Request, get
from io import BytesIO
import geopandas as gpd
import os
import zipfile
import pandas as pd
from sqlalchemy import create_engine

def fetch_and_process_wfs_data(wfs_url, download_dir):
    # Initialize WFS service
    wfs = WebFeatureService(url=wfs_url, version='1.1.0')

    # Fetch the last available layer
    layer_name = list(wfs.contents)[-1]

    params = dict(service='WFS', version="2.0.0", request='GetFeature',
                  typeName=layer_name, outputFormat='geojson')

    # Parse the URL with parameters
    wfs_request_url = Request('GET', wfs_url, params=params).prepare().url

    # Read data from URL
    gdf_ozp_index = gpd.read_file(wfs_request_url)

    # Directory to store the downloaded zip files
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Open each link under the column "GML_LINK" and download the zip files
    for index, row in gdf_ozp_index.iterrows():
        link = row.get('GML_LINK')
        if link:
            response = get(link)
            if response.status_code == 200:
                zip_file_path = os.path.join(download_dir, f"{index}.zip")
                with open(zip_file_path, 'wb') as file:
                    file.write(response.content)

    # List all zip files in the directory
    zip_files = [f for f in os.listdir(download_dir) if f.endswith('.zip')]

    # Initialize an empty list to hold the GeoDataFrames
    gdf_ozp = []

    # Loop through each zip file
    for zip_file in zip_files:
        zip_path = os.path.join(download_dir, zip_file)
        
        # Open the zip file
        with zipfile.ZipFile(zip_path, 'r') as z:
            # Find the full path of 'ZONE.gml' within the zip file
            zone_gml_path = None
            for file_name in z.namelist():
                if file_name.endswith('BHC.gml'):
                    zone_gml_path = file_name
                    break
            
            # If 'ZONE.gml' is found, extract and read it
            if zone_gml_path:
                # Extract 'ZONE.gml' to a temporary location
                z.extract(zone_gml_path, download_dir)
                
                # Read the extracted GML file into a GeoDataFrame
                gml_path = os.path.join(download_dir, zone_gml_path)
                gdf = gpd.read_file(gml_path)
                
                # Append the GeoDataFrame to the list
                gdf_ozp.append(gdf)
