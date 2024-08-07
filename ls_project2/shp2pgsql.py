import subprocess
import osgeo.ogr as ogr

def import_shapefile_to_postgresql(shp_file, pg_connection, schema_name):
    """
    Imports a shapefile into a PostgreSQL database using ogr2ogr.

    Parameters:
    shp_file (str): The path to the shapefile.
    pg_connection (str): The PostgreSQL connection string.
    schema_name (str): Schema name in the PostgreSQL database.
    """
    
    # Open the shapefile to get the layer name
    shapefile = ogr.Open(shp_file)
    if not shapefile:
        print("Could not open shapefile.")
        return

    layer = shapefile.GetLayer()
    layer_name = layer.GetName()

    # Prepare the ogr2ogr command
    command = [
        "ogr2ogr", 
        "-f", "PostgreSQL", 
        pg_connection, 
        shp_file, 
        "-nlt", "MULTIPOLYGON",
        "-nln", f"{schema_name}.{layer_name}"
    ]

    try:
        # Execute the command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode()}")
        print("Command failed:", ' '.join(command))

# Example usage:
# shp_file = "path/to/your/shapefile.shp"
# pg_connection = "PG:host=localhost user=your_user dbname=your_db password=your_password"
# schema_name = "your_schema"
# import_shapefile_to_postgresql(shp_file, pg_connection, schema_name)