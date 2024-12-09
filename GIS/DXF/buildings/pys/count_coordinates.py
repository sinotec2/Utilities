(pyn_env)
kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A/OSM
$ cat count_coordinates.py
def count_coordinates(kml_file):
    import xml.etree.ElementTree as ET
    tree = ET.parse(kml_file)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    coordinates_count = 0
    for coordinates in root.findall('.//kml:coordinates', ns):
        coords = coordinates.text.strip().split()
        coordinates_count += len(coords)

    return coordinates_count
