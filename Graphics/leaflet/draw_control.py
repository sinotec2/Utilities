import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw

# 创建 Streamlit 应用程序
def main():
    st.title("Streamlit 和 Leaflet Draw 控件示例")

    # 创建 Folium 地图
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

    # 添加 Draw 控件
    draw = Draw(
        draw_options={
            'polyline': False,
            'rectangle': True,
            'circle': True,
            'marker': True,
            'polygon': True,
            'circlemarker': False
        },
        edit_options={'edit': True}
    )
    draw.add_to(m)

    # 显示地图
    st_data = st_folium(m, width=725, height=500)

    # 获取用户绘制的形状
    if st_data.get('last_draw'):
        st.write("用户绘制的最后一个形状:")
        st.write(st_data['last_draw'])

    if st_data.get('all_drawings'):
        st.write("所有绘制的形状:")
        st.write(st_data['all_drawings'])

    m.fit_bounds([[y1, x2], [y2, x1]])
if __name__ == "__main__":
    main()

