import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [23.76, 120.4],
    columns=["lat", "lon"],
)
st.map(df)
