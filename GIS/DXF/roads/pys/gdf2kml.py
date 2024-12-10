import geopandas as gpd
from lxml import etree
from shapely.geometry import LineString

# Sample data
data = {
    'name': ['Line 1', 'Line 2', 'Line 3'],
    'geometry': [
        LineString([(120.3182376594, 22.9749026741, 38.257), (120.3182302196, 22.9748983039, 38.261), (120.3182227788, 22.9748939329, 38.266)]),
        LineString([(120.3182153389, 22.9748895627, 38.271), (120.3182078981, 22.9748851925, 38.280), (120.3182004573, 22.9748808215, 38.290)]),
        LineString([(120.3181930175, 22.9748764513, 38.300), (120.3181855777, 22.9748720802, 38.310), (120.3181781369, 22.9748677101, 38.320)])
    ]
}

# Create the GeoPandas DataFrame and set the CRS
gdf = gpd.GeoDataFrame(data, geometry='geometry', crs="EPSG:3857")

# Create the KML document
kml = etree.Element("kml", nsmap={'kml': 'http://www.opengis.net/kml/2.2'})
doc = etree.SubElement(kml, "Document")

# Add style to the KML document
style = etree.SubElement(doc, "Style", id="lineStyle")
line_style = etree.SubElement(style, "LineStyle")
etree.SubElement(line_style, "color").text = "ff0000ff"  # Red color
etree.SubElement(line_style, "width").text = "3"  # Line width

# Add features to the KML document
for _, row in gdf.iterrows():
    placemark = etree.SubElement(doc, "Placemark")
    etree.SubElement(placemark, "name").text = row['name']
    etree.SubElement(placemark, "styleUrl").text = "#lineStyle"
    linestring = etree.SubElement(placemark, "LineString")
    coords = etree.SubElement(linestring, "coordinates")
    coords.text = ",".join([f"{x},{y},{z}" for x, y, z in row.geometry.coords])

# Write the KML document to a file
tree = etree.ElementTree(kml)
tree.write("output.kml", encoding="utf-8", xml_declaration=True)