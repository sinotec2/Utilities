---
layout: default
title: 地端jupyterhub伺服器
nav_order: 99
has_children: true
permalink: /web_jokers/JupyerHub
last_modified_date: 2024-09-21 13:31:12
tags: Jpyter
---

# 建立/應用地端jupyterhub伺服器


## Table of contents

{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Jupyter notebook 的必要性

> python的發展環境(Integrated Development Environment, IDE)有很多種類，何以推介Jupyter ？

- 快速上手python、快速傳遞經驗、廣泛應用的教學平台。
- 簡化作業與發展環境，為目前最簡化的python IDE(Integrated Development Environment)。
- 不需要學習複雜的作業環境指令、顯示設定、檔案與目錄系統。
- 可以同時滿足新手(習慣使用滑鼠)與老手(習慣使用鍵盤)的單一IDE。
- 跨平台(MS WIN/Linux/macOS/Mobile)分享python經驗

## 地端 Jupyter 的必要性

> 網際網路上已有許多免費的Jupyter平台資源，何必一定要在本機或地端上執行？

- 公司內部、新進人員教育訓練。
- 需要讀取/分享的檔案、程式具有機敏性，不適合流出到公眾領域。

## 地端 JupyterHub 伺服器

> 每個人電腦安裝自己的 Jupyter 就好了，為什麼一定要用伺服器？

- 減省每台個人電腦安裝、版本管理等等過程的繁雜程序。
- 使用遠端計算資源：包括CPU/GPU算力、記憶體、暫存空間等等。
- 小眾的共同作業區。發展中的計畫方案、暫時性的工作成果。隨作隨教、即時指導。
- 有效了解、紀錄同仁的發展與應用的需要與過程。
