from osgeo import gdal, ogr
import subprocess

def import_shapefile_to_postgresql(shp_file, pg_connection):
    """
    Imports a shapefile into a PostgreSQL database using ogr2ogr.

    Parameters:
    shp_file (str): The path to the shapefile.
    pg_connection (str): The PostgreSQL connection string.
    """
    # Prepare the ogr2ogr command
    command = [
        "ogr2ogr", 
        "-f", "PostgreSQL", 
        pg_connection, 
        shp_file, 
        "-nlt", "MULTIPOINT"
    ]

    try:
        # Execute the command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode()}")
        print("Command failed:", ' '.join(command))