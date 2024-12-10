#kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A/112roads
#$ cat kml_gdf3.py
import geopandas as gpd
from shapely.wkt import loads
import xml.etree.ElementTree as ET
import os
import pandas as pd
from shapely.geometry import LineString


def read_kml_to_gdf(kml_file):
    tree = ET.parse(kml_file)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    features = []
    for placemark in root.findall('.//kml:Placemark', ns):
        name = placemark.find('kml:name', ns).text
        geom_type = placemark.find('kml:LineString', ns) is not None
        if geom_type:
            coordinates = placemark.find('kml:LineString/kml:coordinates', ns).text.strip()
            coords = [tuple(map(float, coord.split(','))) for coord in coordinates.split()]
            geometry = LineString(coords)

            # Extract the extended data
            extended_data = placemark.find('kml:ExtendedData', ns)
            if extended_data is not None:
                schema_data = extended_data.find('kml:SchemaData', ns)
                if schema_data is not None:
                    attributes = {
                        elem.attrib['name']: elem.text
                        for elem in schema_data.findall('kml:SimpleData', ns)
                    }
            else:
                attributes = {}

            feature = {
                'name': name,
                'geometry': geometry,
                **attributes
            }
            features.append(feature)
        else:
            # Handle other geometry types if needed
            continue

    gdf = gpd.GeoDataFrame(features, geometry='geometry')
    return gdf


# Example usage
kml_dir ='.'
gdf_list = []

# Loop through all the KML files in the directory
for filename in os.listdir(kml_dir):
    if filename.endswith('.kml') and 'LINE' in filename:
      gdf = read_kml_to_gdf(filename)
      if len(gdf)==0:continue
      root=filename.replace('kml','')
      gdf.to_csv(root+'csv',index=False)
      for c in gdf.columns:
        if c!='geometry':del gdf[c]
      gdf_list.append(gdf)
if len(gdf_list)==0:sys.exit('fail')
all_gdf = pd.concat(gdf_list, ignore_index=True)
all_gdf.to_csv('line3D.csv', index=False)
