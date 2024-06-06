from flask import Flask, request, jsonify, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/api/v1/get_file', methods=['POST'])
def get_file():
    try:
        data = request.json
        sw_lat = data['sw_lat']
        sw_lon = data['sw_lon']
        ne_lat = data['ne_lat']
        ne_lon = data['ne_lon']

        # 检查是否传入了所有必要的数据
        if not all([sw_lat, sw_lon, ne_lat, ne_lon]):
            return jsonify({"error": "缺少必要的经纬度参数"}), 400

        # 生成一个示例 CSV 文件
        data = {
            'Latitude': [sw_lat, ne_lat],
            'Longitude': [sw_lon, ne_lon]
        }
        df = pd.DataFrame(data)

        # 将 DataFrame 写入内存中的 CSV 文件
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return send_file(output, mimetype='text/csv', attachment_filename='data.csv', as_attachment=True)

    except KeyError as e:
        return jsonify({"error": f"缺少必要的字段: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

