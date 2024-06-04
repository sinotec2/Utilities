import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
from flask import Flask, request, jsonify
from threading import Thread

# 创建 Flask 应用
app = Flask(__name__)

# 变量来存储 bounds
bounds_data = None

@app.route('/handle_bounds', methods=['POST'])
def handle_bounds():
    global bounds_data
    bounds_data = request.json
    return jsonify(bounds_data)

def run_flask():
    app.run(port=5001)

# 创建 Streamlit 应用程序
def main():
    st.title("Streamlit 和 Leaflet Draw 控件示例")

    # 启动 Flask 服务器
    if 'flask_thread' not in st.session_state:
        flask_thread = Thread(target=run_flask)
        flask_thread.start()
        st.session_state['flask_thread'] = flask_thread

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
        fetch('http://localhost:5001/handle_bounds', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: boundsJSON
        }).then(response => response.json())
          .then(data => {
              // Fit the map to the new bounds
              map.fitBounds(layer.getBounds());
          }).catch(error => console.error('Error:', error));
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

    # 显示接收到的 bounds 数据
    global bounds_data
    if bounds_data:
        st.write("接收到的 bounds 数据:")
        st.write(bounds_data)
    else:
        st.write("没有接收到 bounds 数据")

if __name__ == "__main__":
    main()

