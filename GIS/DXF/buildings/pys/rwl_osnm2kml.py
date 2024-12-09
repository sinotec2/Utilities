__author__ = 'Richard Lincoln, r.w.lincoln@gmail.com'

import sys

from optparse import OptionParser

from xml.etree.ElementTree import \
    parse, Element, SubElement, ElementTree, register_namespace


KML_NS = 'http://www.opengis.net/kml/2.2'


def osm2kml(osm_path, kml_path, nodes=True, ways=True, fmt=False):
    register_namespace('', KML_NS)

    osm_tree = parse(osm_path)
    osm_root = osm_tree.getroot()

    kml_root = Element('{%s}kml' % KML_NS)
    kml_doc = SubElement(kml_root, '{%s}Document' % KML_NS)

    node_map = {}

    for node in osm_root.findall('node'):
        lon_lat = (node.get('lon'), node.get('lat'))
        node_map[node.get('id')] = lon_lat

    if nodes:
        for node_id, lon_lat in node_map.items():
            mark = SubElement(kml_doc, '{%s}Placemark' % KML_NS)
            point = SubElement(mark, '{%s}Point' % KML_NS)
            SubElement(point, '{%s}name' % KML_NS).text = node_id
            coords = SubElement(point, '{%s}coordinates' % KML_NS)
            coords.text = '%s,%s,0' % lon_lat

    if ways:
        for way in osm_root.findall('way'):
            mark = SubElement(kml_doc, '{%s}Placemark' % KML_NS)
            way_id = way.get('id')
            SubElement(mark, '{%s}name' % KML_NS).text = way_id
            linestring = SubElement(mark, '{%s}LineString' % KML_NS)
            coords = SubElement(linestring, '{%s}coordinates' % KML_NS)
            coords_text = ''
            for nd in way.findall('nd'):
                ref = nd.get('ref')
                lon_lat = node_map.get(ref)
                if lon_lat is not None:
                    coords_text += ' %s,%s,0' % lon_lat
                else:
                    print ('Missing node: %s (%s)' % (ref, way_id) )
            coords.text = coords_text

    if fmt: indent(kml_root)
    kml_tree = ElementTree(kml_root)
    kml_tree.write(kml_path, encoding='utf-8', xml_declaration=True)


def indent(elem, level=0):
    i = '\n' + level*'  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def main(argv=sys.argv[1:]):
    parser = OptionParser(
        usage='usage: osm2kml osm_file [kml_file] [options]')

    parser.add_option('--skip-nodes', action='store_true', default=False,
        help='do not include nodes in conversion')

    parser.add_option('--skip-ways', action='store_true', default=False,
        help='do not include ways in conversion')

    parser.add_option('--format-output', action='store_true', default=False,
        dest='format', help='format and indent XML output (experimental)')

    opts, args = parser.parse_args(argv)

    nargs = len(args)
    if nargs == 0:
        parser.print_usage()
        sys.exit(1)
    elif nargs == 1:
        osm_path = args[0]
        if osm_path.lower().endswith('.osm'):
            kml_path = osm_path[:-4] + '.kml'
        else:
            kml_path = osm_path + '.kml'
    elif nargs == 2:
        osm_path = args[0]
        kml_path = args[1] if len(argv) > 1 else (osm_path[:-3] + 'kml')
    else:
        print ('Too many arguments')
        parser.print_usage()
        sys.exit(1)

    osm2kml(osm_path, kml_path, not opts.skip_nodes, not opts.skip_ways,
            opts.format)


if __name__ == '__main__':
    main()
