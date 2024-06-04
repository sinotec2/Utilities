import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
import json


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

    # 在前端添加 JS 脚本来处理 draw:created 事件
    draw_control_js = """
    <script>
    function handleDrawCreated(e) {
        var layer = e.layer;
        var bounds = layer.getBounds();
        var boundsJSON = JSON.stringify({
            northEast: bounds.getNorthEast(),
            southWest: bounds.getSouthWest()
        });
        fetch('/bounds', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: boundsJSON
        }).then(response => response.json())
          .then(data => {
              // Fit the map to the new bounds
              map.fitBounds(layer.getBounds());
          });
    }

    // Wait for the map to be ready
    document.addEventListener('DOMContentLoaded', function() {
        map.on('draw:created', handleDrawCreated);
    });
    </script>
    """
    st.components.v1.html(draw_control_js, height=0)

    # 显示地图
    st_data = st_folium(m, width=725, height=500)

    # 处理从前端发送的 POST 请求
    if st.query_params.get('bounds'):
        bounds_data = st.query_params['bounds'][0]
        bounds = eval(bounds_data)  # 注意：eval 可能有安全隐患，在实际应用中应避免使用
        st.write("接收到的 bounds 数据:")
        st.write(bounds)
def handle_bounds():
    if st.request.method == 'POST':
        bounds = st.request.json
        return bounds
st.experimental_set_query_params({"bounds": json.dumps(handle_bounds())})
if __name__ == "__main__":
    main()

