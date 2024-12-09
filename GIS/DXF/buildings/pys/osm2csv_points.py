(pyn_env)
kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A/OSM
$ cat osm2csv_points.py
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
            if "addr:full" not in tags: return
            self.nodes[n.id] = {
                'geometry': Point(n.location.lon, n.location.lat),
                **tags
            }


handler = OSMHandler()
fname=sys.argv[1]
handler.apply_file(fname)
if len(handler.nodes.values())==0: sys.exit('no nodes found!')
# Create a GeoDataFrame from the nodes, ways, and relations
osm_data = gpd.GeoDataFrame(
    list(handler.nodes.values()) + list(handler.ways.values()) ,
    geometry='geometry',
    crs="EPSG:4326"
)
if 'addr:floor' in osm_data.columns:
    del osm_data['addr:floor']
idx=osm_data.loc[osm_data['addr:full'].map(lambda x:'號' in x)].index
osm_data.loc[idx,'addr:full']=[i[:i.index('號')+1] for i in osm_data.loc[idx,'addr:full']]
osm_data = osm_data.drop_duplicates().reset_index(drop=True)
fname=fname.replace('.osm','pnt.csv')
osm_data.to_csv(fname, index=False)
