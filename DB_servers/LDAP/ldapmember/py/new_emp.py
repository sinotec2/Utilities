from python_freeipa import ClientMeta

## 連線FreeIPA
client = ClientMeta("node03.sinotech-eng.com", verify_ssl=False)
client.login("admin", "sino2024")

user = {
    "EmpNo": "7762",
    "EmpName": "林容君",
    "DeptNo": "17",
    "DeptName": "水務部",
    "DutyName": None,
    "Email": "leolin@mail.sinotech-eng.com",
    "FirstName": "容君",
    "LastName": "林",
    "UserName": "leolin"
}

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
