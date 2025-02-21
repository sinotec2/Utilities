---
layout: default
title: plantUML之使用
parent:   UML
grand_parent: Languages
last_modified_date: 2024-01-02 13:33:58
tags: UML
---

# plantUML之使用

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

- [PlantUML 整合 VSCode 插件教學與常見 UML 圖例練習](https://medium.com/@NeroHin//plantuml-整合-vscode-插件教學與常見-uml-圖例練習-1fc2b689e183)
- github [plantuml-stdlib/C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML)

###  Sequence Diagram 序列圖

- request and response

![](/pngs/2025-01-22-11-26-04.png)

```plantuml
@startuml test_digram 

Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response

Alice -> Bob: Another authentication Request
Alice <-- Bob: Another authentication Response

@enduml
```

- user sequential work

![](pngs/2025-01-22-11-27-58.png)

```plantuml
@startuml

participant User

User -> A: DoWork
activate A
A -> B: << createRequest >>
activate B
B -> C: DoWork
activate C
C --> B: WorkDone
destroy C
B --> A: RequestCreated
deactivate B
A -> User: Done
deactivate A
@endum
```

### State Diagram 狀態圖

![](pngs/2025-01-22-11-29-57.png)

```plantuml
@startuml

scale 350 width
[*] --> NotShooting
state NotShooting {
  [*] --> Idle
  Idle --> Configuring : EvConfig
  Configuring --> Idle : EvConfig
}
state Configuring {
  [*] --> NewValueSelection
  NewValueSelection --> NewValuePreview : EvNewValue
  NewValuePreview --> NewValueSelection : EvNewValueRejected
  NewValuePreview --> NewValueSelection : EvNewValueSaved
  state NewValuePreview {
     State1 -> State2
  }
}

@enduml
```

### Class Diagram 類別圖

![](pngs/2025-01-22-11-31-06.png)

```plantuml
@startuml
class Car

Driver - Car : drives >
Car *- Wheel : have 4 >
Car -- Person : < owns

@enduml
```

### E-R（Entity Relationship）Diagram 實體關係圖

![](pngs/2025-01-22-11-32-47.png)

```plantuml
@startuml

' hide the spot
' hide circle
' avoid problems with angled crows feet
skinparam linetype ortho
entity "User" as e01 {
  *user_id : number <<generated>>
  --
  *name : text
  description : text
}
entity "Card" as e02 {
  *card_id : number <<generated>>
  sync_enabled: boolean
  version: number
  last_sync_version: number
  --
  *user_id : number <<FK>>
  other_details : text
}
entity "CardHistory" as e05 {
  *card_history_id : number <<generated>>
  version : number
  --
  *card_id : number <<FK>>
  other_details : text
}
entity "CardsAccounts" as e04 {
  *id : number <<generated>>
  --
  card_id : number <<FK>>
  account_id : number <<FK>>
  other_details : text
}

entity "Account" as e03 {
  *account_id : number <<generated>>
  --
  user_id : number <<FK>>
  other_details : text
}
entity "Stream" as e06 {
  *id : number <<generated>>
  version: number
  searchingText: string
  --
  owner_id : number <<FK>>
  follower_id : number <<FK>>
  card_id: number <<FK>>
  other_details : text
}

e01 }|..|| e02
e01 }|..|| e03
e02 }|..|| e05
e02 }|..|| e04
e03 }|..|| e04
e02 }|..|| e06
e03 }|..|| e06

@enduml
```

### User Case Diagram 用例圖

![](pngs/2025-01-22-11-35-01.png)

```plantuml
@startuml

left to right direction
actor Guest as g
package Professional {
  actor Chef as c
  actor "Food Critic" as fc
}
package Restaurant {
  usecase "Eat Food" as UC1
  usecase "Pay for Food" as UC2
  usecase "Drink" as UC3
  usecase "Review" as UC4
}
fc --> UC4
g --> UC1
g --> UC2
g --> UC3

@enduml
```

### JSON Diagram

![](pngs/2025-01-22-11-36-07.png)

```plantuml
@startjson JSON_DIAGRAM
{
    "personInfo": [
    {
        "firstName": "John",
        "lastName": "Smith",
        "isAlive": true,
        "age": 27,
        "address": {
        "streetAddress": "21\\n2nd\\nStreet",
            "city": "New York",
            "state": "NY",
            "postalCode": "10021-3100"
        }
        ,
        "phoneNumbers": [
        {
            "type": "home",
            "number": "212 555-1234"
        }
        ,
        {
            "type": "office",
            "number": "646 555-4567"
        }
        ],
        "children": [],
        "spouse": null
    }
    ,
    {
        "firstName": "Jack",
        "lastName": "Smith",
        "...": "..."
    }
]
}

@endjson
```

### 樣式

![](pngs/2025-01-22-11-37-07.png)

```plantuml
@startuml skinparam_demo

' 定義樣式
!define Driver << (D, orchid) >>
skinparam class {
    ' 背景色
    BackgroundColor Red
    ' 線條色
    ArrowColor Green
    ' 邊框色
    BorderColor Yellow
}
class Car
' 定義並使用 Driver 樣式
class DriverRole Driver
DriverRole - Car : drives
Car -- Wheel : have 4
Car -- Person : owns

@enduml
```

## C4 models

### System Context & System Landscape diagrams

### Container diagram

### Component diagram

### Dynamic diagram

### Deployment diagram

### C4 styled - Sequence diagram
