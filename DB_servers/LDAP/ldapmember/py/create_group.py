## 根據技術組新增FreeIPA Group

from python_freeipa import ClientMeta
from m.group_ref import gerTuple

client = ClientMeta("node03.sinotech-eng.com", verify_ssl=False)
client.login("admin", "sino2024")

# 取得groupname Tuple
group_tuple = gerTuple()

for groupstr in group_tuple:
    groupName = groupstr
    description = groupstr + " Group"
    client.group_add(a_cn=groupName, o_description=description)