import os
import requests
import zipfile
import shutil

def download_and_extract_shp(url, storage_path):
    download_path = os.path.join(storage_path, "downloaded_file.zip")

    # Create the target directory if it doesn't exist
    os.makedirs(storage_path, exist_ok=True)

    # Download the file
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(download_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded file to {download_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        return

    # Unzip the file and find shapefiles
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        # List all files in the zip
        all_files = zip_ref.namelist()
        
        # Find files with extensions commonly associated with shapefiles
        shapefile_extensions = ('.shp', '.shx', '.dbf', '.prj')
        shapefile_files = [file for file in all_files if file.lower().endswith(shapefile_extensions)]

        if not shapefile_files:
            print("No shapefiles found in the zip file.")
            return

        # Extract only shapefiles to the storage path
        for file in shapefile_files:
            zip_ref.extract(file, storage_path)
        print(f"Extracted shapefiles to {storage_path}")

    # Remove the original downloaded file
    os.remove(download_path)
    print(f"Removed the original downloaded file {download_path}")