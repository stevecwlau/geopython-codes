from osgeo import gdal, ogr
import subprocess

def transfer_gdb_to_postgis(gdb_path, pg_connection, schema_name):
    """
    Transfer layers from a GeoDatabase to a PostgreSQL/PostGIS database.

    Parameters:
    - gdb_path (str): Path to the GeoDatabase.
    - pg_connection (str): PostgreSQL connection string.
    - schema_name (str): Schema name in the PostgreSQL database.
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
        "Point": "POINT",
        "Line String": "LINESTRING",
        "Polygon": "POLYGON",
        "Multi Point": "MULTIPOINT",
        "Multi Line String": "MULTILINESTRING",
        "Multi Polygon": "MULTIPOLYGON",
        "Geometry Collection": "GEOMETRYCOLLECTION",
        "Circular String": "CIRCULARSTRING",
        "Compound Curve": "COMPOUNDCURVE",
        "Curve Polygon": "CURVEPOLYGON",
        "Multi Curve": "MULTICURVE",
        "Multi Surface": "MULTISURFACE",
        "Curve": "CURVE",
        "Surface": "SURFACE",
        "3D Point": "POINT",
        "3D Line String": "LINESTRING",
        "3D Polygon": "POLYGON",
        "3D Multi Point": "MULTIPOINT",
        "3D Multi Line String": "MULTILINESTRING",
        "3D Multi Polygon": "MULTIPOLYGON",
        "3D Geometry Collection": "GEOMETRYCOLLECTION",
        "3D Circular String": "CIRCULARSTRING",
        "3D Compound Curve": "COMPOUNDCURVE",
        "3D Curve Polygon": "CURVEPOLYGON",
        "3D Multi Curve": "MULTICURVE",
        "3D Multi Surface": "MULTISURFACE",
        "3D Curve": "CURVE",
        "3D Surface": "SURFACE",
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
        
        # Debugging line to print geometry type and corresponding command
        print(f"Layer: {layer_name}, Geometry Type: {geom_type_name}, Command Geometry Type: {geom_type_cmd}")
        
        command = [
            "ogr2ogr",
            "-f", "PostgreSQL",
            pg_connection,
            gdb_path,
            layer_name,
            "-nlt",
            geom_type_cmd,
            "-nln",
            f"{schema_name}.{layer_name}"
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

# Example usage:
# transfer_gdb_to_postgis("path/to/geodatabase.gdb", "PG:host=localhost dbname=mydb user=myuser password=mypassword", "myschema")