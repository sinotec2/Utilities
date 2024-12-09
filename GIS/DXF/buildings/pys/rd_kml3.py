kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A
$ cat rd_kml3.py
import pandas as pd
import xml.etree.ElementTree as ET
import os

def kml_to_csv(kml_file):
    tree = ET.parse(kml_file)
    root = tree.getroot()

    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    data = []
    for placemark in root.findall('.//kml:Placemark', ns):
        record = {}
        # 提取標題
        name = placemark.find('kml:name', ns)
        record['name'] = name.text if name is not None else None

        # 提取地理位置
        point = placemark.find('.//kml:Model', ns)
        if point is not None:
            coords = point.find('kml:Location', ns)
            if coords is not None:
                record['longitude'] = coords.find('kml:longitude', ns).text
                record['latitude'] = coords.find('kml:latitude', ns).text

        # 提取區域資料
        region = placemark.find('.//kml:Region', ns)
        if region is not None:
            lat_lon_box = region.find('kml:LatLonAltBox', ns)
            if lat_lon_box is not None:
                record['maxAltitude'] = lat_lon_box.find('kml:maxAltitude', ns).text
            extended_data = placemark.find('{http://www.opengis.net/kml/2.2}ExtendedData')
            if extended_data is not None:
                schema_data = extended_data.find('{http://www.opengis.net/kml/2.2}SchemaData')
                if schema_data is not None:
                    county = schema_data.find('{http://www.opengis.net/kml/2.2}SimpleData[@name="COUNTY"]')
                    if county is not None:
                        record['COUNTY'] = county.text
        data.append(record)

    return pd.DataFrame(data)

def main(kml_folder, output_csv):
    all_data = []
    for filename in os.listdir(kml_folder):
        if filename.endswith('.kml'):
            kml_file = os.path.join(kml_folder, filename)
            df = kml_to_csv(kml_file)
            all_data.append(df)

    # 合併所有資料並儲存
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv(output_csv, index=False)

# 使用範例
kml_folder = './kmls'  # KML 檔案所在資料夾
output_csv = 'output2.csv'  # 輸出 CSV 檔案名稱
main(kml_folder, output_csv)
