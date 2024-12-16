## 開發時測試用程式

# import math
# import pandas as pd

# # 讀取 Excel 檔案
# df = pd.read_excel('/home/felix/python/ldapmember/data/allemp.xlsx')

# # 將 DataFrame 轉換為 List[dict]
# records = df.applymap(lambda x: None if pd.isna(x) else x).to_dict(orient='records')
# print(records[73].get("DutyName"))




# from python_freeipa import ClientMeta,exceptions
# from m.grp2group import gerTuple
# from py.m.importjson import from_json_to_list

# client = ClientMeta("node03.sinotech-eng.com", verify_ssl=False)
# client.login("admin", "sino2024")
# user = client.user_add(
#     "ming",
#     "大明",
#     "王",
#     "王大明",
#     o_loginshell="/sbin/nologin",
#     o_userpassword="85058505",
# )
# print(user)

# print(group)
# group = client.group_add(a_cn="itg", o_description="IT GROUP")
# print(group)
# adgroup = client.group_add_member("itg", o_user="ming")
# print(adgroup)

# group_tuple = gerTuple()

# for i in range(2):
#     groupName = group_tuple[i]
#     description = group_tuple[i] + " Group"
#     print(f"組別：{groupName}，描述：{description}")

# test create group water
# group_tuple = gerTuple()
# groupName = group_tuple[5] 
# description = groupName + " Group"
# print(f"組別：{groupName}，描述：{description}")
# client.group_add(a_cn=groupName, o_description=description)

# 載入整理好的JSON
# from m.importjson import from_json_to_list
# from m.group_ref import getdict



# print(f"{user_list[0].get('EmpNo')}{user_list[0].get('EmpName')}")
# groupname_dict = getdict()
# print(groupname_dict.get(user_list[0].get("grp")))

# 載入整理好的JSON
# from m.importjson import from_json_to_list
# user_list = from_json_to_list("/home/felix/python/ldapmember/json.txt")
# user = user_list[307]
# print(user)
# from python_freeipa import ClientMeta
# client = ClientMeta("node03.sinotech-eng.com", verify_ssl=False)
# client.login("admin", "sino2024")

# client.user_add(
#     a_uid=user.get("UserName"),
#     o_userpassword=user.get("EmpNo") * 2,
#     o_mail=user.get("Email"),
#     # 姓
#     o_givenname=user.get("FirstName"),
#     # 名
#     o_sn=user.get("LastName"),
#     # 全名
#     o_cn=user.get("EmpName"),
#     # 登錄shell 預設不能登錄
#     o_loginshell="/sbin/nologin",
#     # 組織單位
#     o_ou=user.get("DeptName"),
#     # 部門編號
#     o_departmentnumber=user.get("DeptNo"),
#     # 員工編號
#     o_employeenumber=user.get("EmpNo"),
#     # 職稱
#     o_title=user.get("DutyName"),
#     # 員工類型(職等)先不新增 o_employeetype=user.get("TitleName"),
#     # 家目錄先不新增 o_homedirectory=user.get("Home"),
# )

# try:
# client.group_add_member(
#     a_cn='WATER', o_user="felixlee"
# )
# except exceptions.BadRequest:
#     print("BadRequest")
#     pass


#測試修改dist
# for index,user in enumerate(user_list):
    # user['FirstName'] = user.get("EmpName")[1:]
    # user['LastName'] = user.get("EmpName")[0]

    # email = user.get("Email")       
    # ei = email.rfind('@')
    # user['UserName'] = email[:ei]
    # 帳號為全數字人數
    # if user.get("UserName").isdigit():
    #     print(index,user)
 

# test add group
# client.group_add_member(
#     a_cn=group_name_dict.get(user.get("grp")), 
#     o_user=user.get("EmailName")
# )
