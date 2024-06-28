import geopandas as gpd
from sqlalchemy import create_engine

def remap_values_and_save(data, table_name):
    """
    Remap values in a GeoDataFrame and save the results to a PostGIS database.

    Parameters:
    data (GeoDataFrame): The input GeoDataFrame.
    remap_dict (dict): The dictionary for remapping values.
    db_url (str): The database connection URL.
    table_name (str): The name of the table to save the data in the database.

    Returns:
    GeoDataFrame: The GeoDataFrame with remapped values.
    """
    # Convert data to GeoDataFrame
    gdf = gpd.GeoDataFrame(data)
    
    # Apply the remapping and keep unmapped values unchanged
    gdf['DESC_ENG'] = gdf['DESC_ENG'].map(remap_dict).fillna(gdf['DESC_ENG'])
    
    # Save to PostGIS
    username = "postgres"
    password = "12345"
    host = "localhost"
    dbname = "Buildings"
    port = "5432"

    engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{dbname}")
    gdf.to_postgis(table_name, engine, if_exists='replace')

    return gdf

# Define the remapping dictionary
remap_dict = {
    'Agriculture(1)': 'Agriculture', 
    'Commercial / Residential(1)': 'Commercial / Residential', 
    'Commercial / Residential(2)': 'Commercial / Residential', 
    'Commercial / Residential(3)': 'Commercial / Residential', 
    'Commercial / Residential(4)': 'Commercial / Residential', 
    'Commercial(1)': 'Commercial', 
    'Commercial(2)': 'Commercial', 
    'Commercial(3)': 'Commercial', 
    'Commercial(4)': 'Commercial', 
    'Commercial(5)': 'Commercial', 
    'Commercial(6)': 'Commercial', 
    'Commercial(7)': 'Commercial', 
    'Commercial(8)': 'Commercial', 
    'Commercial(9)': 'Commercial',
    'Commercial (3)': 'Commercial',
    'Commercial (4)': 'Commercial',
    'Commercial (1)': 'Commercial',
    'Commercial (2)': 'Commercial',
    'Commercial(11)': 'Commercial',
    'Commercial(10)': 'Commercial',
    'Comprehensive Development Area(1)': 'Comprehensive Development Area', 
    'Comprehensive Development Area(2)': 'Comprehensive Development Area', 
    'Comprehensive Development Area(3)': 'Comprehensive Development Area', 
    'Comprehensive Development Area(4)': 'Comprehensive Development Area', 
    'Comprehensive Development Area(5)': 'Comprehensive Development Area', 
    'Comprehensive Development Area(6)': 'Comprehensive Development Area', 
    'Conservation Area(1)': 'Conservation Area', 
    'Government, Institution or Community(1)': 'Government, Institution or Community', 
    'Government, Institution or Community(10)': 'Government, Institution or Community', 
    'Government, Institution or Community(2)': 'Government, Institution or Community', 
    'Government, Institution or Community(3)': 'Government, Institution or Community', 
    'Government, Institution or Community(4)': 'Government, Institution or Community', 
    'Government, Institution or Community(5)': 'Government, Institution or Community', 
    'Government, Institution or Community(6)': 'Government, Institution or Community', 
    'Government, Institution or Community(7)': 'Government, Institution or Community', 
    'Government, Institution or Community(8)': 'Government, Institution or Community', 
    'Government, Institution or Community(9)': 'Government, Institution or Community',
    'Government, Institution or Community (1)': 'Government, Institution or Community',
    'Government, Institution or Community(13)': 'Government, Institution or Community',
    'Government, Institution or Community(12)': 'Government, Institution or Community',
    'Government, Institution or Community(11)': 'Government, Institution or Community',
    'Green Belt(1)': 'Green Belt', 
    'Green Belt(2)': 'Green Belt', 
    'Industrial(1)': 'Industrial', 
    'Industrial(2)': 'Industrial', 
    'Industrial(3)': 'Industrial', 
    'Open Space(1)': 'Open Space', 
    'Open Space(2)': 'Open Space', 
    'Open Space(3)': 'Open Space', 
    'Other Specified Uses(1)': 'Other Specified Uses', 
    'Other Specified Uses(2)': 'Other Specified Uses', 
    'Other Specified Uses(3)': 'Other Specified Uses', 
    'Other Specified Uses(4)': 'Other Specified Uses', 
    'Other Specified Uses(5)': 'Other Specified Uses', 
    'Other Specified Uses(6)': 'Other Specified Uses', 
    'Residential (Group A)1': 'Residential (Group A)', 
    'Residential (Group A)10': 'Residential (Group A)', 
    'Residential (Group A)11': 'Residential (Group A)', 
    'Residential (Group A)12': 'Residential (Group A)', 
    'Residential (Group A)13': 'Residential (Group A)', 
    'Residential (Group A)14': 'Residential (Group A)', 
    'Residential (Group A)15': 'Residential (Group A)', 
    'Residential (Group A)16': 'Residential (Group A)', 
    'Residential (Group A)17': 'Residential (Group A)', 
    'Residential (Group A)18': 'Residential (Group A)', 
    'Residential (Group A)19': 'Residential (Group A)', 
    'Residential (Group A)2': 'Residential (Group A)', 
    'Residential (Group A)20': 'Residential (Group A)', 
    'Residential (Group A)21': 'Residential (Group A)', 
    'Residential (Group A)22': 'Residential (Group A)', 
    'Residential (Group A)23': 'Residential (Group A)', 
    'Residential (Group A)24': 'Residential (Group A)', 
    'Residential (Group A)25': 'Residential (Group A)', 
    'Residential (Group A)26': 'Residential (Group A)', 
    'Residential (Group A)3': 'Residential (Group A)', 
    'Residential (Group A)4': 'Residential (Group A)', 
    'Residential (Group A)5': 'Residential (Group A)', 
    'Residential (Group A)6': 'Residential (Group A)', 
    'Residential (Group A)7': 'Residential (Group A)', 
    'Residential (Group A)8': 'Residential (Group A)', 
    'Residential (Group A)9': 'Residential (Group A)', 
    'Residential (Group B)1': 'Residential (Group B)', 
    'Residential (Group B)10': 'Residential (Group B)', 
    'Residential (Group B)11': 'Residential (Group B)', 
    'Residential (Group B)12': 'Residential (Group B)', 
    'Residential (Group B)14': 'Residential (Group B)', 
    'Residential (Group B)16': 'Residential (Group B)', 
    'Residential (Group B)17': 'Residential (Group B)', 
    'Residential (Group B)19': 'Residential (Group B)', 
    'Residential (Group B)2': 'Residential (Group B)', 
    'Residential (Group B)3': 'Residential (Group B)', 
    'Residential (Group B)4': 'Residential (Group B)', 
    'Residential (Group B)5)': 'Residential (Group B)', 
    'Residential (Group B)6)': 'Residential (Group B)', 
    'Residential (Group B)7)': 'Residential (Group B)', 
    'Residential (Group B)8)': 'Residential (Group B)', 
    'Residential (Group B)20)': 'Residential (Group B)',
    'Residential (Group B)15)': 'Residential (Group B)',
    'Residential (Group A)27)': 'Residential (Group B)',
    'Residential (Group A)28)': 'Residential (Group B)',
    'Residential (Group B)13)': 'Residential (Group B)',
    'Residential (Group B)9)': 'Residential (Group B)',
    'Residential (Group B)18)': 'Residential (Group B)',
    'Residential (Group C)1)': 'Residential (Group C)', 
    'Residential (Group C)10)': 'Residential (Group C)', 
    'Residential (Group C)11)': 'Residential (Group C)', 
    'Residential (Group C)12)': 'Residential (Group C)', 
    'Residential (Group C)13)': 'Residential (Group C)', 
    'Residential (Group C)14)': 'Residential (Group C)', 
    'Residential (Group C)15)': 'Residential (Group C)', 
    'Residential (Group C)2)': 'Residential (Group C)', 
    'Residential (Group C)3)': 'Residential (Group C)', 
    'Residential (Group C)4)': 'Residential (Group C)', 
    'Residential (Group C)5)': 'Residential (Group C)', 
    'Residential (Group C)6)': 'Residential (Group C)', 
    'Residential (Group C)7)': 'Residential (Group C)', 
    'Residential (Group C)8)': 'Residential (Group C)', 
    'Residential (Group C)9)': 'Residential (Group C)', 
    'Residential (Group D)1)': 'Residential (Group D)', 
    'Residential (Group E)1)': 'Residential (Group E)', 
    'Residential (Group E)2)': 'Residential (Group E)', 
    'Village Type Development(1)': 'Village Type Development',
    'Recreation(1)': 'Recreation',
    'Site of Special Scientific Interest(1)': 'Site of Special Scientific Interest',
    'Comprehensive Development Area (2)': 'Comprehensive Development Area',
    'Coastal Protection Area(1)': 'Coastal Protection Area'
}
