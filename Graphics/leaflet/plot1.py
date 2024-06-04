import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 標題和描述
st.title('簡單的資料視覺化工具')
st.write('使用Streamlit快速建立資料視覺化應用程式')

# 產生隨機數據
data = pd.DataFrame({
 'A': np.random.randn(100),
 'B': np.random.randn(100),
 'C': np.random.randn(100)
})

# 選擇要顯示的列
columns = st.multiselect('選擇要顯示的欄位', data.columns)

# 顯示選定的列
if columns:
 st.dataframe(data[columns])

 # 繪製選定列的圖表
 fig, ax = plt.subplots()
 data[columns].plot(kind='line', ax=ax)
 st.pyplot(fig)
else:
 st.write('請選擇至少一列資料進行顯示')

