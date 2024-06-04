from dataclasses import dataclass
from typing import Dict, List, Optional

import folium
import requests
import streamlit as st
import leaflet
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# define layout
c1, c2 = st.columns(2)
y0,x0,z0=23.5, 121.,8
L = leaflet.L
with c1:
    """(_Click on a pin to bring up more information_)"""
    m = folium.Map(location=[y0, x0], zoom_start=z0)
    with st.sidebar:
        x1 = st.slider('Top-left X', x0-2, x0+2,x0-1)
        y1 = st.slider('Top-left Y', y0-2, y0-1,y0+1)
        x2 = st.slider('Bottom-right X', x0-2, x0+2,x0+1)
        y2 = st.slider('Bottom-right Y', y0-2, y0-1,y0-1)

# Add a rectangle to the map based on the selected coordinates
        folium.Rectangle([[y1, x1], [y2, x2]], color='blue', opacity=0.5).add_to(m)
    m.fit_bounds([[y1, x2], [y2, x1]])
    # Get the Leaflet.js map instance

    # Use Leaflet.js to add a drawing tool to the map
    leaflet_map.addControl(L.Control.Draw());

    map_data = st_folium(m, key="fig1", width=700, height=800)
