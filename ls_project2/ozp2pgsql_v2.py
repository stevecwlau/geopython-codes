import os
import zipfile
import geopandas as gpd

# Define the directory containing the zip files
zip_dir = r"C:\Users\Steve_Lau\Downloads\ozp"
output_dir = os.path.join(zip_dir, "extracted_gmls")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List all zip files in the directory
zip_files = [f for f in os.listdir(zip_dir) if f.endswith('.zip')]

# Loop through each zip file
for zip_file in zip_files:
    zip_path = os.path.join(zip_dir, zip_file)
    
    # Open the zip file
    with zipfile.ZipFile(zip_path, 'r') as z:
        # Find the full path of 'ZONE.gml' within the zip file
        zone_gml_path = None
        for file_name in z.namelist():
            if file_name.endswith('ZONE.gml'):
                zone_gml_path = file_name
                break
        
        # If 'ZONE.gml' is found, extract and read it
        if zone_gml_path:
            # Extract 'ZONE.gml' to a temporary location
            z.extract(zone_gml_path, zip_dir)
            
            # Read the extracted GML file into a GeoDataFrame
            gml_path = os.path.join(zip_dir, zone_gml_path)
            gdf = gpd.read_file(gml_path)
            
            # Save the GeoDataFrame to a new file in the output directory
            output_gml_path = os.path.join(output_dir, f"extracted_{zip_file[:-4]}.gml")
            gdf.to_file(output_gml_path, driver='GML')
            
            # Remove the extracted GML file after processing
            os.remove(gml_path)

print(f"Successfully extracted ZONE.gml files from {len(zip_files)} zip archives.")