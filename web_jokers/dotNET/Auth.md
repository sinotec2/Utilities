---
layout: default
title:  Auth
parent: dotNET connections
grand_parent: Web Jokers
last_modified_date: 2024-01-19 13:47:15
tags: API_Server 
---

# .NET讀取AD帳號
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


## 程式碼

在 .NET 中，你可以使用 `System.DirectoryServices.AccountManagement` 命名空間提供的 `PrincipalContext` 類別來讀取使用者的 Active Directory 帳戶訊息。以下是一個簡單的範例：

```csharp
using System;
using System.DirectoryServices.AccountManagement;

class Program
{
    static void Main()
    {
        // 設定 Active Directory 上下文
        using (PrincipalContext context = new PrincipalContext(ContextType.Domain))
        {
            // 使用者名稱
            string username = "your_username";

            // 使用 PrincipalContext 進行使用者查詢
            UserPrincipal user = UserPrincipal.FindByIdentity(context, IdentityType.SamAccountName, username);

            if (user != null)
            {
                // 讀取使用者屬性
                Console.WriteLine("Display Name: " + user.DisplayName);
                Console.WriteLine("User Principal Name: " + user.UserPrincipalName);
                Console.WriteLine("Email: " + user.EmailAddress);
                Console.WriteLine("Description: " + user.Description);
                
                // 其他屬性根據需求添加
            }
            else
            {
                Console.WriteLine("User not found.");
            }
        }
    }
}
```

這個範例使用 `PrincipalContext` 來建立一個 Active Directory 上下文，然後使用 `UserPrincipal.FindByIdentity` 方法根據使用者名稱進行查詢。你可以根據需要擴展或修改這個範例以滿足特定的需求，例如讀取更多使用者屬性。

