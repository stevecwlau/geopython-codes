from osgeo import gdal

def converter(gdb_path, csv_path, layer_name):
    """
    Convert a GeoDatabase layer to a CSV file using GDAL's ogr2ogr functionality.
    
    :param gdb_path: Path to the GeoDatabase file (GDB)
    :param csv_path: Path to the output CSV file
    :param layer_name: Name of the layer to convert
    """
    # Open source dataset (GeoDatabase)
    src_ds = gdal.OpenEx(gdb_path, gdal.OF_VECTOR)
    if src_ds is None:
        print("Could not open GeoDatabase file")
        return

    # Translate the GeoDatabase layer to CSV
    options = gdal.VectorTranslateOptions(
        format='CSV',
        layers=[layer_name],
        datasetCreationOptions=['ENCODING=UTF-8-SIG']
    )

    # Perform the translation
    gdal.VectorTranslate(
        destNameOrDestDS=csv_path,
        srcDS=src_ds,
        options=options
    )

    print("Conversion completed successfully")