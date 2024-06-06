from flask import Flask, request, jsonify, send_file,send_from_directory
import pandas as pd
from io import BytesIO
from mem2cntr import cntr, rd_mem
from mem2dxf  import dxf

app = Flask(__name__)

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/api/v1/get_dxf', methods=['POST'])
def get_dxf():
    try:
        data = request.json
        print("Received data:", data)  # 调试输出
        sw_lat = data.get('sw_lat')
        sw_lon = data.get('sw_lon')
        ne_lat = data.get('ne_lat')
        ne_lon = data.get('ne_lon')

        # 检查是否传入了所有必要的数据
        if not all([sw_lat, sw_lon, ne_lat, ne_lon]):
            return jsonify({"error": "缺少必要的经纬度参数"}), 400

        # 将 DataFrame 写入内存中的 CSV 文件
        fname, output = dxf((sw_lat, sw_lon),(ne_lat, ne_lon))
        if fname=='LL not right!':
            return jsonify({"error": "经纬度参数超過範圍"}), 400

        return send_file(output, mimetype='application/dxf', download_name=fname, as_attachment=True)

    except KeyError as e:
        return jsonify({"error": f"缺少必要的字段: {str(e)}"}), 400
    except Exception as e:
        print("Exception occurred:", str(e))  # 调试输出
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/get_cntr', methods=['POST'])
def get_cntr():
    try:
        data = request.json
        print("Received data:", data)  # 调试输出
        sw_lat = data.get('sw_lat')
        sw_lon = data.get('sw_lon')
        ne_lat = data.get('ne_lat')
        ne_lon = data.get('ne_lon')

        # 检查是否传入了所有必要的数据
        if not all([sw_lat, sw_lon, ne_lat, ne_lon]):
            return jsonify({"error": "缺少必要的经纬度参数"}), 400

        # 将 DataFrame 写入内存中的 CSV 文件
        fname, output = cntr((sw_lat, sw_lon),(ne_lat, ne_lon))
        if fname=='LL not right!':
            return jsonify({"error": "经纬度参数超過範圍"}), 400

        return send_file(output, mimetype='image/png', download_name=fname, as_attachment=True)

    except KeyError as e:
        return jsonify({"error": f"缺少必要的字段: {str(e)}"}), 400
    except Exception as e:
        print("Exception occurred:", str(e))  # 调试输出
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True,  host='devp.sinotech-eng.com', port=5000)
