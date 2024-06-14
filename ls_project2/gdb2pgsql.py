from osgeo import gdal, ogr
import subprocess

def transfer_gdb_to_postgis(gdb_path, pg_connection):
    """
    Transfer layers from a GeoDatabase to a PostgreSQL/PostGIS database.

    Parameters:
    - gdb_path (str): Path to the GeoDatabase.
    - pg_connection (str): PostgreSQL connection string.
    """
    
    # Open source dataset (GeoDatabase)
    src_ds = gdal.OpenEx(gdb_path, gdal.OF_VECTOR)

    # Check if the dataset was opened successfully
    if src_ds is None:
        print(f"Failed to open GeoDatabase at {gdb_path}")
        return

    # Mapping from human-readable names to command line names
    geom_type_mapping = {
        "None": "NONE",
        "Multi Polygon": "MULTIPOLYGON",
        "3D Multi Polygon": "MULTIPOLYGON",
        "3D Multi Line String": "MULTILINESTRING",
        "3D Point": "MULTIPOINT",
        "3D Measured Multi Line String": "MULTILINESTRING",
        "3D Measured Point": "MULTIPOINT",
        "3D Measured Multi Polygon": "MULTIPOLYGON"
    }

    # Function to get the geometry type as a string
    def get_geom_type_name(geom_type):
        return ogr.GeometryTypeToName(geom_type)

    # Function to list all layers in the GeoDatabase with their types
    def list_layers(dataset):
        layers = []
        for i in range(dataset.GetLayerCount()):
            layer = dataset.GetLayerByIndex(i)
            layer_name = layer.GetName()
            geom_type = layer.GetGeomType()
            geom_type_name = get_geom_type_name(geom_type)
            layers.append((layer_name, geom_type_name))
            print(f"Layer: {layer_name}, Type: {geom_type_name}")
        return layers

    # Function to run ogr2ogr command
    def run_ogr2ogr(layer_name, geom_type_name):
        geom_type_cmd = geom_type_mapping.get(geom_type_name, "NONE")
        command = [
            "ogr2ogr",
            "-f", "PostgreSQL",
            pg_connection,
            gdb_path,
            layer_name,
            "-nlt", geom_type_cmd
        ]
        
        print("Running command:", " ".join(command))
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Command for layer {layer_name} executed successfully")
            print(result.stdout)
        else:
            print(f"Command for layer {layer_name} failed with error:")
            print(result.stderr)

    # List layers and run ogr2ogr for each
    layers = list_layers(src_ds)
    for layer_name, geom_type_name in layers:
        run_ogr2ogr(layer_name, geom_type_name)