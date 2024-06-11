from osgeo import gdal, ogr

def list_layers_with_types(gdb_path):
    """
    Opens a GeoDatabase and lists all layers with their geometry types.

    Parameters:
    gdb_path (str): Path to the GeoDatabase.

    Returns:
    None
    """
    # Open source dataset (GeoDatabase)
    src_ds = gdal.OpenEx(gdb_path, gdal.OF_VECTOR)

    # Check if the dataset was opened successfully
    if src_ds is None:
        print(f"Failed to open GeoDatabase at {gdb_path}")
        return

    # Function to get the geometry type as a string
    def get_geom_type_name(geom_type):
        return ogr.GeometryTypeToName(geom_type)

    # List all layers in the GeoDatabase with their types
    print("Layers in the GeoDatabase:")
    for i in range(src_ds.GetLayerCount()):
        layer = src_ds.GetLayerByIndex(i)
        layer_name = layer.GetName()
        geom_type = layer.GetGeomType()
        geom_type_name = get_geom_type_name(geom_type)
        print(f"Layer: {layer_name}, Type: {geom_type_name}")