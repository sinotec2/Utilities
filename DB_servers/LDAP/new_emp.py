# 20240726版 edit by python大神天霖
# api ref: https://python-freeipa.readthedocs.io/en/latest/
from python_freeipa import ClientMeta

## 連線FreeIPA
client = ClientMeta("node03.sinotech-eng.com", verify_ssl=False)
client.login("admin", "sino2024")

deptDict = {
    "監理": "01",
    "行政部": "03",
    "職安中心": "05",
    "研資部": "06",
    "環評部": "15",
    "循環部": "16",
    "水務部": "17",
    "能資部": "18",
    "永續部": "19",
    "環境工程部": "EV"
}

# 根據新進員工資訊修改此字典
user = {
    "EmpNo": "8847", #員工編號
    "DeptName": "能資部", #部門 需同上面字典key
    "DutyName": None, #職務 如總經理
    "LastName": "鍾", #姓
    "FirstName": "亞萱", #名
    "UserName": "chun8847" #Email名稱
    "UserGroup" "carbon" #分組名稱
}

#"UserGroup":
#Out[36]: dict_keys(['admin', 'air', 'carbon', 'construction', 'counseling', 'editors', 'eia', 'ict', 'operation', 'pipeline', 'soil', 'waste', 'water', 'wind'])


df=read_csv('ldapmember/group_id.csv')
gnam_id={i:j for i,j in zip(df.group_name,df.GID)}

# 重複資料處理
user["Email"] = user["UserName"] + "@mail.sinotech-eng.com" # Email
user["EmpName"] = user["LastName"] + user["FirstName"] # EmpName

client.user_add(
    a_uid=user.get("UserName"),
    o_userpassword=user.get("EmpNo") * 2, #密碼預設員編兩次
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
    # 部門編號 從字典自動取得
    o_departmentnumber=deptDict.get(user.get("DeptName")),
    # 員工編號
    o_employeenumber=user.get("EmpNo"),
    # 職稱
    o_title=user.get("DutyName"),
    # 員工類型(職等)先不新增 o_employeetype=user.get("TitleName"),
    # 家目錄先不新增 o_homedirectory=user.get("Home"),
    o_gidnumber = gnam_id.get(user.get("UserGroup")),
)

client.group_add_member(a_cn=user.get("UserGroup"),o_user=user.get("UserName"),)

client.logout()
