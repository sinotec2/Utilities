---
layout: default
title:  Apache Druid 之API
parent: Apache Druid Services
grand_parent: Apache Druid
last_modified_date: 2024-02-12 14:15:31
tags: DB_servers Druid
---

# Apache Druid 之API
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

- [Druid SQL API](https://www.bookstack.cn/read/druid-27.0-en/cf91c9e9d2d2bf3f.md#Result%20formats)
{"query":"SELECT deltaBucket, COUNT(*) AS Count FROM wikipedia GROUP BY 1 ORDER BY 2 DESC",
"resultFormat" : "array",
  "header" : true,
  "typesHeader" : true,
  "sqlTypesHeader" : true}
curl -XPOST -H'Content-Type: application/json' http://admin:password1@sinotec24.com:8888/druid/v2/sql/ -d @query.json

curl -u admin:password1 -XPOST https://sinotec24.com:8281/druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/myname

- [Security overview](https://druid.apache.org/docs/latest/operations/security-overview/)
- given names:`for i in {0..9};do curl -u admin:password1 -XPOST http://sinotec24.com:8081/druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/user$i ;done`
- credentials:`for i in {0..9};do curl -u admin:password1 -H'Content-Type: application/json' -XPOST http://sinotec24.com:8081/druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/user$i/credentials --data-raw '{"password": "passwd123"}';done`
- Authorizer definition:`for i in {0..9};do curl -u admin:password1 -XPOST http://sinotec24.com:8081/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/user$i ;done`
- create roles

```bash
for r in admin analyst;do curl -u admin:password1 -XPOST http://sinotec24.com:8081/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/roles/$r;done
```
for i in {0..9};do 
curl -u admin:password1 -XPOST http://sinotec24.com:8081/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/user$i/roles/analyst
done
- permission

```bash
for r in admin analyst;do
curl -u admin:password1 -H'Content-Type: application/json' -XPOST --data-binary @perms_$r.json http://sinotec24.com:8081/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/roles/$r/permissions
done
```

r=admin
for i in {0..9};do 
curl -u admin:password1 -XPOST  http://sinotec24.com:8081/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/user$i/roles/$r
done