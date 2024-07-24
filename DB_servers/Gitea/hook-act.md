---
layout: default
title:  外部掛鉤vs工序執行器
parent: Gitea
grand_parent: DB_servers
last_modified_date: 2024-07-24 10:55:33
tags: gitea
---

#  Gitea的外部掛鉤vs工序執行器

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

- 雖然這二者的觀念非常接近，也都需要伺服器承接指令，不論是外部或內部。
- 但前者因為銜接外部資源，用在主動聯繫方面的功能會很方便。
- 後者的強項是繁瑣的編譯整合，雖然也有發布的功能，但僅限靜態網頁或app上架，靈活度還是有限。

## `hook` 和 `act_runner`

在持續整合/持續交付（CI/CD）環境中，`hook` 和 `act_runner` 是兩種不同的機制，分別用於觸發和執行 CI/CD 管線。它們在 Gitea 和 Jenkins 等工具中發揮不同的作用。以下是這兩者的詳細說明：

### Hook

**Hook** 是一種在特定事件發生時自動觸發預定義操作的機制。在版本控制系統（如 Git）中，常見的鉤子有 pre-commit、post-commit、pre-receive 和 post-receive 等。這些鉤子可以在本地或遠端倉庫中配置。

#### Gitea 中的 Hook

1. **Webhook**：Gitea 支援 Webhook，當特定事件（如程式碼推送、合併請求）發生時，Webhook 可以傳送 HTTP POST 請求到指定的 URL。這通常用於觸發外部的 CI/CD 工具，如 Jenkins 或 GitLab CI。

2. **Git Hook**：Gitea 也支援 Git 本身的鉤子腳本，這些腳本在特定的 Git 事件發生時運行，例如 pre-receive、post-receive 鉤子。這些鉤子可以用來執行自訂的伺服器端邏輯，例如拒絕不符合規範的提交。

### Act Runner

**Act Runner** 是一個用於執行 GitHub Actions 工作流程的本機執行器。它可以在本地環境中模擬 GitHub Actions 工作流程，非常適合在本地進行測試和偵錯。

#### Gitea 中的 Act Runner

Gitea 的 Act Runner 類似於 GitHub Actions，它允許你定義和執行工作流程，這些工作流程包含一個或多個步驟，可以執行各種 CI/CD 任務。

### 區別和用法

#### Hook

1. **觸發機制**：鉤子在特定事件發生時觸發，例如程式碼推送、合併請求。
2. **執行環境**：鉤子可以是本機 Git 倉庫中的腳本，也可以是遠端伺服器上設定的 Webhook。
3. **用途**：鉤子通常用於觸發外部系統的操作，例如通知 Jenkins 開始建置。

#### Act Runner

1. **觸發機制**：Act Runner 在收到特定事件的通知後執行預先定義的工作流程。
2. **執行環境**：Act Runner 可以在本地或指定的環境中運行，適用於模擬和調試 GitHub Actions 工作流程。
3. **用途**：Act Runner 主要用於執行複雜的 CI/CD 工作流程，包括程式碼建置、測試和部署等任務。

### 範例

#### 使用 Webhook 觸發 Jenkins 構建

1. 在 Gitea 中設定 Webhook：
 - 導航至倉庫設定頁面。
 - 點選 "Webhooks"。
 - 新增一個新的 Webhook，URL 指向 Jenkins 的建置觸發 URL。

2. 在 Jenkins 中設定對應的任務來處理 Gitea 的 Webhook 請求。

#### 使用 Act Runner 執行工作流程

1. 寫 `.github/workflows/main.yml` 檔案定義工作流程：
 ```yaml
 name: CI

 on: [push]

 jobs:
 build:
 runs-on: ubuntu-latest

 steps:
 - uses: actions/checkout@v2
 - name: Set up Node.js
 uses: actions/setup-node@v2
 with:
 node-version: '14'
 - name: Install dependencies
 run: npm install
 - name: Run tests
 run: npm test
 ```

2. 使用 Act Runner 在本地運行工作流程：
 ```sh
 act
 ```

透過理解 `hook` 和 `act_runner` 的差異和用途，可以更好地選擇適合你的 CI/CD 流程的工具和配置。在實際專案中，你可以根據需求組合使用這些工具，以實現高效的持續整合和持續交付。

## 功能特色及取代性


是的，部分的 Hook 功能確實可以透過 Act Runner 這樣的工具來實現。兩者在某些情況下可以互補使用，但各自有其適用的場景和優點。以下是對兩者的對比和適用場景的進一步說明：

### Hook

**Hook** 的主要功能是觸發預先定義的操作，通常用於以下場景：

1. **即時觸發外部服務**：如觸發 Jenkins 建置、通知聊天工具（如 Slack）、執行自訂腳本等。
2. **簡單、快速的操作**：如程式碼格式檢查、提交資訊驗證、簡單的測試腳本等。
3. **基於事件的直接回應**：如程式碼推送、合併請求、標籤建立等。

#### 優點

- **即時性**：在特定事件發生時立即執行。
- **靈活性**：可以執行任何自訂腳本或觸發任何外部服務。
- **輕量級**：適合快速的、本地化的操作。

### Act Runner

**Act Runner** 則是用來執行複雜的 CI/CD 工作流程，特別適合以下情境：

1. **複雜的建置與測試流程**：如多步驟建置、依賴安裝、執行測試、產生建置工件等。
2. **與版本控制系統整合**：例如根據不同的分支、標籤、Pull Request 執行不同的工作流程。
3. **可重複的工作流程**：定義一次工作流程，能在不同環境中一致地執行。

#### 優點

- **一致性**：工作流程定義和執行的一致性，不受環境變化影響。
- **複雜性**：適合處理複雜的 CI/CD 流程。
- **可擴充性**：支援外掛程式、擴充功能和整合各種服務和工具。

### 適用場景

#### 使用 Hook

- **簡單任務**：如程式碼格式檢查、通知、簡單測試。
- **即時回應**：需要立即對某個事件做出反應。
- **與外部系統互動**：觸發外部 CI/CD 系統或通知服務。

#### 使用 Act Runner

- **複雜工作流程**：如多步驟的建置、測試和部署。
- **一致性需求**：需要在不同環境中保持一致的工作流程執行。
- **高可擴充性**：需要整合多種工具和服務，支援複雜的 CI/CD 流程。

### 範例：結合使用 Hook 和 Act Runner

1. **使用 Hook 觸發 Act Runner**：
 - 在 Gitea 中設定一個 Webhook，觸發 URL 指向一個本機或遠端伺服器上的 Act Runner 端點。
 - 當程式碼推送時，Webhook 觸發 Act Runner 執行定義的工作流程。

2. **使用 Hook 處理簡單任務，Act Runner 執行複雜任務**：
 - 在 Gitea 中設定 Git Hook 進行程式碼格式檢查和簡單測試。
 - 在工作流程中使用 Act Runner 執行複雜的建置和部署任務。

### 範例配置

#### Gitea Webhook 配置

1. 登入 Gitea，導覽至倉庫設定頁面。
2. 點選 "Webhooks"。
3. 新增一個新的 Webhook，URL 指向 Act Runner 端點。

#### Act Runner 工作流程檔案（`.github/workflows/main.yml`）

```yaml
name: CI

on: [push]

jobs:
 build:
 runs-on: ubuntu-latest

 steps:
 - uses: actions/checkout@v2
 - name: Set up Node.js
 uses: actions/setup-node@v2
 with:
 node-version: '14'
 - name: Install dependencies
 run: npm install
 - name: Run tests
 run: npm test
 - name: Build project
 run: npm run build
```

透過這種組合使用方式，你可以利用 Hook 的即時性和 Act Runner 的複雜性處理不同的 CI/CD 需求，達到最佳效果。