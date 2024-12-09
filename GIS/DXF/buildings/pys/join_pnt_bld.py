import geopandas as gpd
import osmium
from shapely.geometry import Point, LineString, Polygon
import sys

class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.nodes = {}
        self.ways = {}
        self.relations = {}

    def node(self, n):
        if n.location.valid():
            tags = {tag.k: tag.v for tag in n.tags}
            self.nodes[n.id] = {
                'geometry': Point(n.location.lon, n.location.lat),
                **tags
            }

    def way(self, w):
        valid_coords = []
        tags = {tag.k: tag.v for tag in w.tags}
        if "building" not in tags: return
        for nd in w.nodes:
            if nd.ref in self.nodes:
                valid_coords.append(self.nodes[nd.ref]['geometry'])
        if len(valid_coords) > 1:
            way_geometry = Polygon(valid_coords)
#            for node_id, node_data in self.nodes.items():
#                node_geometry = node_data['geometry']
#                if node_geometry.within(way_geometry):
#                    # Add the node's tags to the way's tags
#                    for k, v in node_data.items():
#                        if k != 'geometry':
#                            tags.update({k: v})
#                    break

            self.ways[w.id] = {
                'geometry': way_geometry,
                **tags
            }

handler = OSMHandler()
fname=sys.argv[1]
handler.apply_file(fname)

# Create a GeoDataFrame from the nodes, ways, and relations
osm_data = gpd.GeoDataFrame(
    list(handler.nodes.values()) + list(handler.ways.values()) ,
    geometry='geometry',
    crs="EPSG:4326"
)
fname=fname.replace('.osm','bld.csv')
building = osm_data.loc[osm_data["building"].map(lambda x:type(x)==str)]
building = building.dropna(axis=1, how='all')
building.to_csv(fname, index=False)
