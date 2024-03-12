---
layout: default
title:  LDAP hierarchy
parent: LDAP
grand_parent: Security And Authentication
last_modified_date: 2024-02-15 14:52:16
tags: LDAP gitea
---

#  LDAP hierarchy
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

- OU：organization unit，用在組織的正式名稱
- CN：common name，用在一般性、功能性的名稱
- ou
  - departments(部門), centers, units, tech_units
  - titles(職級):
    - general
    - projects
  - duties(職務): 
    - engineers, 
    - planners, 
    - specilists,
- cn
  - editors: chief_ed, member_ed
  - login: accounts, users