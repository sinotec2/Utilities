---
layout: default
title:  Gitea觸發Jenkins自動執行VuePress之佈建
parent: VuePress
grand_parent: Static Site Generators
nav_order: 3
last_modified_date: 2023-06-12 08:56:43
tags: VuPress
---

# Gitea觸發Jenkins自動執行VuePress之佈建
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

-

### settings

要讓 Jenkins 自動部署 VuePress 網誌，您需要在 Gitea 上設置 Webhook，並使用 Jenkins 的 Gitea 插件來觸發自動部署流程¹²³。

以下是設置步驟：

1. 在 Gitea 上創建一個新的 Webhook，並將其設置為觸發 Jenkins 的自動部署流程。您可以在 Gitea 的 Webhook 設置頁面上找到相關的文檔和指南¹。
2. 在 Jenkins 中安裝 Gitea 插件，並配置 Gitea 服務器的詳細信息。您可以在 Jenkins 的官方文檔中找到有關如何安裝和配置 Gitea 插件的詳細信息¹²。
3. 在 Jenkins 中創建一個新的 Pipeline 項目，並將其配置為使用 VuePress 進行自動部署。您可以在 Jenkins 的官方文檔中找到有關如何創建和配置 Pipeline 項目的詳細信息¹²。

希望這些信息對您有所幫助！

來源: 與 Bing 的交談， 2024/1/21

(1) Gitea 与 Jenkins 的集成实践，打造你的专属 CI/CD 系统 - Gitea - [博客园](https://www.cnblogs.com/Gitea/p/jenkins.html).

(2) VuePress搭建博客教程（含部署到gitee） [临渊的博客](http://linyuanstudy.gitee.io/linyuanstudy/frontEnd/VuePress%E6%90%AD%E5%BB%BA%E5%8D%9A%E5%AE%A2%E6%95%99%E7%A8%8B.html).

(3) 前端自动化部署jenkins+gitee一个博客系统vuePress项目_vuepress gitee 自动化-[CSDN博客](https://blog.csdn.net/weixin_42424283/article/details/128738568).

(4) 【Linux】云服务器自动化部署VuePress博客（[Jenkins](https://blog.51cto.com/returntmp/7330501)).

(5) Jenkins实现Vuepress自动化部署(上)-安装配置Jenkins - [掘金](https://juejin.cn/post/6969542924182749198).

(6) [undefined](https://plugins.jenkins.io/gitea/).

(7) [undefined](https://gitea.com).
