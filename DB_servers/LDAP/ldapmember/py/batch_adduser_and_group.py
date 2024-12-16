## 依照JSON內之員工list[dict]資料
## 批次新增使用者並根據技術組加入對應Group
## Group需先執行create_group.py

from python_freeipa import ClientMeta,exceptions
from m.group_ref import getdict
from m.importjson import from_json_to_list

## 載入整理好的JSON
user_list = from_json_to_list(r"D:\Desktop\笙蜚交接資料\ldapmember\123.txt")

## 載入組名 group對應dict
groupname_dict = getdict()

## 連線FreeIPA
client = ClientMeta("node03.sinotech-eng.com", verify_ssl=False)
client.login("admin", "sino2024")


for user in user_list:
    client.user_add(
        a_uid=user.get("UserName"),
        o_userpassword=user.get("EmpNo") * 2,
        o_mail=user.get("Email"),
        # 名
        o_givenname=user.get("FirstName"),
        # 姓
        o_sn=user.get("LastName"),
        # 全名
        o_cn=user.get("EmpName"),
        # 登錄shell 預設不能登錄
        o_loginshell="/sbin/nologin",
        # 組織單位
        o_ou=user.get("DeptName"),
        # 部門編號
        o_departmentnumber=user.get("DeptNo"),
        # 員工編號
        o_employeenumber=user.get("EmpNo"),
        # 職稱
        o_title=user.get("DutyName"),
        # 員工類型(職等)先不新增 o_employeetype=user.get("TitleName"),
        # 家目錄先不新增 o_homedirectory=user.get("Home"),
    )
    try:
        client.group_add_member(
            a_cn=groupname_dict.get(user.get("grp")), o_user=user.get("UserName")
        )
    except exceptions.BadRequest:
        print(f"{user.get('EmpNo')} {user.get('EmpName')}")
        pass

