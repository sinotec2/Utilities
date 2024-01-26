---
layout: default
title: jenv之使用
parent:   Java
grand_parent: Languages
last_modified_date: 2024-01-02 13:33:58
tags: jenv
---

# jenv之使用

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

`jenv` 是一個用於管理 Java 版本的工具，類似於 Node.js 的 `nvm` 或 Ruby 的 `rvm`。它可以幫助你在同一台機器上管理多個 Java 版本。

以下是一些 `jenv` 的基本使用方法：

1. **安裝 `jenv`：**

   使用 Homebrew 在 macOS 上安裝：

   ```bash
   brew install jenv
   ```

   或者，你也可以在其他環境中使用 git 進行手動安裝：

   ```bash
   git clone https://github.com/jenv/jenv.git ~/.jenv
   echo 'export PATH="$HOME/.jenv/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(jenv init -)"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **安裝 Java 版本：**

   使用 `jenv` 安裝你需要的 Java 版本。例如，安裝 OpenJDK 11：

   ```bash
   jenv add /path/to/your/jdk/11
   ```

   或者，使用 Homebrew 安裝 OpenJDK：

   ```bash
   brew install openjdk@11
   jenv add $(brew --prefix)/opt/openjdk@11
   ```

3. **設定全域或專案特定的 Java 版本：**

   設定全域的 Java 版本：

   ```bash
   jenv global 11.0
   ```

   或者，進入到你的專案目錄，設定專案特定的 Java 版本：

   ```bash
   cd /path/to/your/project
   jenv local 11.0
   ```

4. **使用特定的 Java 版本：**

   ```bash
   jenv shell 11.0
   ```

   或者，只是臨時使用某個版本而不進行永久設定：

   ```bash
   jenv exec java -version
   ```

5. **列出已安裝的 Java 版本：**

   ```bash
   jenv versions
   ```

這只是 `jenv` 的基本使用方法。使用 `jenv` 可以很方便地在不同的專案中切換 Java 版本，確保你的應用程序使用了正確的 Java 環境。