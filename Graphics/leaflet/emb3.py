import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
import json

def main():
    st.title("Streamlit 和 Leaflet Draw 控件示例")

    # 創建 Folium 地圖
    st.markdown(
    """
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
    integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
    crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
    integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
    crossorigin=""></script>
    """,
    unsafe_allow_html=True
    )
    if 'geojson_data' not in st.session_state:
        st.session_state['geojson_data'] = None


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

    # 在前端添加 JS 腳本來處理 draw:created 事件
    draw_control_js = """
    <script>
    // 將 map 對象定義為全局變量
    var map;

    // 等待文檔準備好後初始化地圖
    document.addEventListener('DOMContentLoaded', function() {
        map = new L.map('map').setView([45.5236, -122.6750], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(map);

        // 初始化 Draw 控件並添加到地圖
        var drawControl = new L.Control.Draw({
            draw: {
                polyline: false,
                rectangle: true,
                circle: true,
                marker: true,
                polygon: true,
                circlemarker: false
            },
            edit: {
                featureGroup: new L.FeatureGroup().addTo(map)
            }
        }).addTo(map);

        // 處理 draw:created 事件
        map.on('draw:created', function(e) {
            var layer = e.layer;
            //var bounds = layer.getBounds();
            //map.fitBounds(bounds);
            var geoJsonData = layer.toGeoJSON();
            console.log("GeoJSON data:", geoJsonData);
        // 將 GeoJSON 資料寫入 st.session_state
            Streamlit.setComponentValue({ 'geojson_data': JSON.stringify(geoJsonData) });
        });
    });
    </script>
    """
    st.components.v1.html(draw_control_js, height=0)

    # 顯示地圖
    st_data = st_folium(m, width=725, height=500)

    # 在 Streamlit 中顯示接收到的 bounds 資料
    if 'geojson_data' in st.session_state:
        st.write("接收到的 bounds 資料:")
        st.write(st.session_state['geojson_data'])
    else:
        st.write("沒有接收到 bounds 資料")
#        st.experimental_rerun()


if __name__ == "__main__":
    main()

