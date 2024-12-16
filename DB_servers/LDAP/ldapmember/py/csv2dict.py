## 整合allname.csv及grp_svr.csv並打印在terminal
## linux執行時加 > json.txt 將輸出存為txt

##注意：python dist使用' 透過json.dumps轉為JSON使用之"

import csv
import json
import pandas as pd


def read_csv_to_dict(csv_file_path):
    data = []
    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def read_xlsx_to_dict(xlsx_file_path):
    # 讀取 Excel 檔案
    df = pd.read_excel(xlsx_file_path)
    return df.map(lambda x: None if pd.isna(x) else x).to_dict(orient='records')


# 讀取CSV檔案並轉換成字典形式
filepath1 = r"D:\Desktop\笙蜚交接資料\ldapmember\data\data_user.xlsx"
xlsx_data = read_xlsx_to_dict(filepath1)

filepath2 = r"D:\Desktop\笙蜚交接資料\ldapmember\data\grp_svr.csv"
group_data = read_csv_to_dict(filepath2)

output = "[" + "\n"

for i in range(len(xlsx_data)):
    # xlsx員編為數字 為比對轉為文字
    xlsx_data[i]['EmpNo'] = str(xlsx_data[i].get("EmpNo"))
    
    xlsx_data[i]['FirstName'] = xlsx_data[i].get("EmpName")[1:]
    xlsx_data[i]['LastName'] = xlsx_data[i].get("EmpName")[0]

    # UserName處理
    email = xlsx_data[i].get("Email")       
    ei = email.rfind('@')
    xlsx_data[i]['UserName'] = email[:ei]

    for group_dist in group_data:
        if xlsx_data[i]["EmpNo"] == group_dist["EmpNo"][:-2]:
            xlsx_data[i]["grp"] = group_dist["grp"]
            group_data.remove(group_dist)
        if not bool(xlsx_data[i].get("grp")):
            xlsx_data[i]["grp"] = None

    # 整理原本有小數點的str 新檔案無小數點
    # xlsx_data[i]["EmpNo"] = xlsx_data[i]["EmpNo"][0:-2]
    # xlsx_data[i]["CenterNo"] = xlsx_data[i]["CenterNo"][0:-2]
    # xlsx_data[i]["DeptNo"] = xlsx_data[i]["DeptNo"][0:-2]
    # xlsx_data[i]["Title"] = xlsx_data[i]["Title"][0:-2]
    # xlsx_data[i]["Duty"] = xlsx_data[i]["Duty"][0:-2]
    
    # 轉為JSON格式
    output += json.dumps(xlsx_data[i]) + "," + "\n"

output = output[:-2] + "\n" + "]"

print(output)
with open("123.txt", "w") as file:
    file.write(output)