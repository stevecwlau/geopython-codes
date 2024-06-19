import os
import requests
import zipfile
import shutil

def download_and_extract_gdb(url, storage_path):
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

    # Unzip the file and find the .gdb folder
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        # List all files in the zip
        all_files = zip_ref.namelist()

        # Find the .gdb folder
        gdb_folder = None
        for file in all_files:
            if file.endswith('.gdb/') or '.gdb/' in file:
                gdb_folder = file.split('/')[0]
                break

        if gdb_folder is None:
            print("No .gdb folder found in the zip file.")
            return

        # Remove the old version of the gdb folder if it exists
        gdb_path = os.path.join(storage_path, gdb_folder)
        if os.path.exists(gdb_path):
            shutil.rmtree(gdb_path)
            print(f"Removed old version of {gdb_folder}")

        # Extract only the .gdb folder
        for file in all_files:
            if file.startswith(gdb_folder):
                zip_ref.extract(file, storage_path)
        print(f"Extracted {gdb_folder} to {storage_path}")

    # Remove the original downloaded file
    os.remove(download_path)
    print(f"Removed the original downloaded file {download_path}")