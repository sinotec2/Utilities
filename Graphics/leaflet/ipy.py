import streamlit as st
import ipyleaflet

st.title("My Map App")

m = ipyleaflet.Map()

tile_layer = ipyleaflet.TileLayer(url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                                   attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
                                   subdomains=['a', 'b', 'c'])

m.add_layer(tile_layer)

st.leaflet(m)

