---
layout: default
title:  vscode powershell streamlit 系統的編碼
parent: streamlit
grand_parent: Web Jokers
nav_order: 99
last_modified_date: 2025-03-26 08:32:07
tags: web
---

#  vscode powershell streamlit 系統的編碼
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

- 官網說明：[瞭解 VS Code 和 PowerShell 中的檔案編碼](https://learn.microsoft.com/zh-tw/powershell/scripting/dev-cross-plat/vscode/understanding-file-encoding?view=powershell-7.5)

## 設定 VS Code

VS Code 的預設編碼方式為 UTF-8，不含 [BOM](#bom)。

若要設定 VS Code 的編碼，請移至 VS Code 設定（Ctrl+、），並設定 "files.encoding" 設定：

```jso
"files.encoding": "utf8bom"
```
一些可能的值為：

- utf8： [UTF-8] 不含 BOM
- utf8bom： [UTF-8] 搭配 BOM
- utf16le： 小端 [UTF-16]
- utf16be： 大端 [UTF-16]
- windows1252：[Windows-1252]

您應該會在 GUI 檢視中取得此專案的下拉式清單，或在 JSON 檢視中取得該清單的完成。

您也可以盡可能將下列內容新增至自動偵測編碼：

```json
"files.autoGuessEncoding": true
```

如果您不想要這些設定會影響所有文件類型，VS Code 也允許個別語言的組態。 將設定放在 `[[<language-name>]]` 字段中，以建立特定語言設定。 例如：

```json
"[powershell]": {
    "files.encoding": "utf8bom",
    "files.autoGuessEncoding": true
}
```

您也可以考慮安裝適用於 Visual Studio Code 的 [Gremlins]() 追蹤器。 此延伸模組會顯示某些容易損毀的 Unicode 字元，因為它們是看不見的，或看起來像其他一般字元。

## 設定 PowerShell

PowerShell 的預設編碼會因版本而異：

### PowerShell 6+

在 PowerShell 6+ 中，預設編碼方式是所有平台上沒有 BOM 的 UTF-8。

在 Windows PowerShell 中，預設編碼通常是 Windows-1252，這是 latin-1 的延伸模組（也稱為 ISO 8859-1）。

### PowerShell 5+

在 PowerShell 5+ 中，您可以使用下列方式找到預設編碼方式：

```PowerShell
[psobject].Assembly.GetTypes() | Where-Object { $_.Name -eq 'ClrFacade'} |
  ForEach-Object {
    $_.GetMethod('GetDefaultEncoding', [System.Reflection.BindingFlags]'nonpublic,static').Invoke($null, @())
  }
```

可能的結果如下：

```powershell
BodyName          : big5
EncodingName      : 繁體中文 (Big5)
HeaderName        : big5
WebName           : big5
WindowsCodePage   : 950
IsBrowserDisplay  : True
IsBrowserSave     : True
IsMailNewsDisplay : True
IsMailNewsSave    : True
IsSingleByte      : False
EncoderFallback   : System.Text.InternalEncoderBestFitFallback
DecoderFallback   : System.Text.InternalDecoderBestFitFallback
IsReadOnly        : True
CodePage          : 950
```

下列 腳本 可用來判斷沒有 BOM 之腳本的 PowerShell 會話推斷的編碼方式。

```PowerShell
$badBytes = [byte[]]@(0xC3, 0x80)
$utf8Str = [System.Text.Encoding]::UTF8.GetString($badBytes)
$bytes = [System.Text.Encoding]::ASCII.GetBytes('Write-Output "') + [byte[]]@(0xC3, 0x80) + [byte[]]@(0x22)
$path = Join-Path ([System.IO.Path]::GetTempPath()) 'encodingtest.ps1'

try
{
    [System.IO.File]::WriteAllBytes($path, $bytes)

    switch (& $path)
    {
        $utf8Str
        {
            return 'UTF-8'
            break
        }

        default
        {
            return 'Windows-1252'
            break
        }
    }
}
finally
{
    Remove-Item $path
}
```

您可以更普遍地使用設定檔設定，將 PowerShell 設定為使用指定的編碼方式。 請參閱下列文章：

- 在 Stack Overflow 上上有關 PowerShell 編碼的 答案。
- 關於在 PowerShell中處理無 BOM UTF-8 輸入的 部落格文章。
- 您無法強制 PowerShell 使用特定的輸入編碼。 PowerShell 5.1 和以下版本，在 Windows 上執行的地區設定設為 en-US，當沒有 BOM 時，預設為 Windows-1252 編碼。 
- 其他地區設定可能會使用不同的編碼方式。 為了確保互操作性，最好使用 BOM 以 Unicode 格式儲存腳本。

::: 重要

您擁有的任何其他觸控 PowerShell 腳本工具，都可能會受到編碼選擇的影響，或將腳本重新編碼為另一種編碼。


## Terminology

### BOM

[wiki:端序記號](https://zh.wikipedia.org/wiki/端序記號)