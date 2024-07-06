---
layout: default
title: Markdown to PDF
nav_order: 99
has_children: true
parent: Marking Languages
permalink: /MarkLang/
last_modified_date: 2024-07-06 11:24:36
tags: md
---

# Markdown to PDF

## Table of contents

{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 背景

### 英文

```bash
sudo apt install   pandoc   texlive-latex-base   texlive-fonts-recommended   texlive-extra-utils   texlive-latex-extra   texlive-xetex
pandoc README.md -o README.pdf --pdf-engine=xelatex
```

### 中文

- 參考[這一篇](https://sam.webspace.tw/2020/01/13/使用%20Pandoc%20將%20Markdown%20轉為%20PDF%20文件/)
- 中文會需要[MikText](https://miktex.org/download)
- 如何引用字形參考[jgm/pandoc](https://github.com/jgm/pandoc/wiki/Pandoc-with-Chinese)，從`fc-list :lang=zh`來選擇。

```bash
JP: Japanese
HK: Hong Kong (Traditional Chinese)
KR: Korean
SC: Simplified Chinese
TC: Traditional Chinese
```

```bash
curl -fsSL https://miktex.org/download/key | sudo tee /usr/share/keyrings/miktex-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/miktex-keyring.asc] https://miktex.org/download/ubuntu jammy universe" | sudo tee /etc/apt/sources.list.d/miktex.list
sudo apt-get update
sudo apt-get install miktex
sudo miktexsetup --shared=yes finish
sudo initexmf --admin --set-config-value [MPM]AutoInstall=1
```