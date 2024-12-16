## 計算沒有技術組人數並打印名單

from m.importjson import from_json_to_list

list = from_json_to_list("/home/felix/python/ldapmember/json.txt")
token = 0
for dict in list:
    if dict.get("grp") is None:
        print(f' {dict["DeptName"]}  {dict["EmpName"]} {dict["DutyName"]}')
        token += 1

# 沒有技術組人數
print(token)