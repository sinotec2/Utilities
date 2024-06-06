---
layout: default
title:  API伺服器
parent: DTM and Relatives
grand_parent: GIS Relatives
last_modified_date: 2024-06-07 00:32:27
tags: dtm GIS
---

# API伺服器
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


這段程式碼建立了一個使用 Flask 框架的 API 服務，其中包含兩個端點 `/api/v1/get_dxf` 和 `/api/v1/get_cntr`。這兩個端點分別用於生成 DXF 文件和 PNG 圖像，並將其返回給客戶端。具體的工作流程如下：

1. **導入必要的庫**：
   - `Flask` 用於創建 web 應用。
   - `pandas` 用於數據處理。
   - `BytesIO` 用於處理內存中的文件。
   - `cntr` 和 `dxf` 分別從 `mem2cntr` 和 `mem2dxf` 模組中導入，用於生成 PNG 圖像和 DXF 文件。

2. **創建 Flask 應用**：
   - `app = Flask(__name__)` 初始化 Flask 應用。

3. **靜態文件的端點**：
   - `serve_html` 函數返回 `index.html` 文件。

4. **生成 DXF 文件的端點**：
   - `get_dxf` 函數接收 POST 請求中的 JSON 數據，提取西南和東北角的經緯度，並調用 `dxf` 函數生成 DXF 文件。生成的文件以附件形式返回。

5. **生成 PNG 圖像的端點**：
   - `get_cntr` 函數接收 POST 請求中的 JSON 數據，提取西南和東北角的經緯度，並調用 `cntr` 函數生成 PNG 圖像。生成的圖像以附件形式返回。

6. **主程序入口**：
   - 當程序以腳本形式運行時，啟動 Flask 服務。

以下是完整的代碼：

```python
from flask import Flask, request, jsonify, send_file, send_from_directory
import pandas as pd
from io import BytesIO
from mem2cntr import cntr, rd_mem
from mem2dxf import dxf

app = Flask(__name__)

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/api/v1/get_dxf', methods=['POST'])
def get_dxf():
    try:
        data = request.json
        print("Received data:", data)  # 調試輸出
        sw_lat = data.get('sw_lat')
        sw_lon = data.get('sw_lon')
        ne_lat = data.get('ne_lat')
        ne_lon = data.get('ne_lon')

        # 檢查是否傳入了所有必要的數據
        if not all([sw_lat, sw_lon, ne_lat, ne_lon]):
            return jsonify({"error": "缺少必要的經緯度參數"}), 400

        # 將 DataFrame 寫入內存中的 CSV 文件
        fname, output = dxf((sw_lat, sw_lon), (ne_lat, ne_lon))
        if fname == 'LL not right!':
            return jsonify({"error": "經緯度參數超過範圍"}), 400

        return send_file(output, mimetype='application/dxf', download_name=fname, as_attachment=True)

    except KeyError as e:
        return jsonify({"error": f"缺少必要的字段: {str(e)}"}), 400
    except Exception as e:
        print("Exception occurred:", str(e))  # 調試輸出
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/get_cntr', methods=['POST'])
def get_cntr():
    try:
        data = request.json
        print("Received data:", data)  # 調試輸出
        sw_lat = data.get('sw_lat')
        sw_lon = data.get('sw_lon')
        ne_lat = data.get('ne_lat')
        ne_lon = data.get('ne_lon')

        # 檢查是否傳入了所有必要的數據
        if not all([sw_lat, sw_lon, ne_lat, ne_lon]):
            return jsonify({"error": "缺少必要的經緯度參數"}), 400

        # 將 DataFrame 寫入內存中的 CSV 文件
        fname, output = cntr((sw_lat, sw_lon), (ne_lat, ne_lon))
        if fname == 'LL not right!':
            return jsonify({"error": "經緯度參數超過範圍"}), 400

        return send_file(output, mimetype='image/png', download_name=fname, as_attachment=True)

    except KeyError as e:
        return jsonify({"error": f"缺少必要的字段: {str(e)}"}), 400
    except Exception as e:
        print("Exception occurred:", str(e))  # 調試輸出
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, host='devp.sinotech-eng.com', port=5000)
```

此應用程序提供了一個簡單的網頁界面，並且可以通過 API 調用來生成並下載 DXF 文件和 PNG 圖像。確保 `mem2cntr` 和 `mem2dxf` 模組正確地被導入並且運行正常。