---
layout: default
title:  streamlit_folium
parent: leaflet
grand_parent: Graphics
date:  2024-06-04
last_modified_date: 2024-06-04 14:04:00
tags: CMAQ leaflet graphics streamlit_folium
---

# streamlit_folium
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## 背景


```python
from dataclasses import dataclass
from typing import Dict, List, Optional

import folium
import requests
import streamlit as st

from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# define layout
c1, c2 = st.columns(2)

with c1:
    """(_Click on a pin to bring up more information_)"""
    m = folium.Map(location=[23.5, 121.], zoom_start=8)
    map_data = st_folium(m, key="fig1", width=700, height=700)
```