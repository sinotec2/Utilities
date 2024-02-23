---
layout: default
title: CPU使用率之個人加總
parent: Operation System
grand_parent: Operation Systems
last_modified_date: 2023-07-26 09:52:44
tags: os bash
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

## 背景

- 因為工作站平行運作後，使用者的執行序增加成數百個、CPU使用量便是一長串結果，需要加總才能知道確切的資源分配情形。用簡單的top(htop), ps似乎不能達成。詢問chatGPT結果如下：

>**Q** 前述各個方法，如何得知哪個使用者總共用了多少CPU?

> **A** 要得知哪個使用者總共用了多少CPU，您可以使用以下方法：
> 使用ps與awk命令：運行下面的命令，它會計算每個使用者的總CPU使用率並列出結果。

```bash
ps -eo user,%cpu --sort=-%cpu | awk '{arr[$1]+=$2;} END {for (i in arr) {print i,arr[i]}}'
```
> 這個命令將會列出每個使用者的名稱以及他們所使用的總CPU百分比。
> 使用top與awk命令：運行下面的命令，它會顯示每個使用者的總CPU使用率。

```bash
top -b -n 1 | awk 'NR>7 {arr[$2]+=$9;} END {for (i in arr) {print i,arr[i]}}'
```

> 這個命令與之前提到的相同，使用top命令獲取每個進程的CPU使用率，並使用awk計算每個使用者的總CPU使用率。
> 無論使用哪種方法，它們都可以顯示每個使用者的總CPU使用率，這有助於您了解不同使用者在系統中的資源消耗情況。請注意，某些命令可能需要使用root權限或sudo來查看所有使用者的資訊。

## 腳本及應用

### 腳本

- 將時間列在前述結果的前面。
  - 為讓格式統一，選用資料庫形式，每時間、每使用者一行。
  - 這需要先將前述結果分開成2個array
- 因array長度不一定，用累計迴圈型態來列印結果

```bash
c=(); u=()
for j in $(ps -eo user,%cpu --sort=-%cpu | awk '{arr[$1]+=$2;} END {for (i in arr) {print i,arr[i]}}'|grep -v ' 0'|awk '{print $2}');do 
  c=( ${c[@]} $j);done
for j in $(ps -eo user,%cpu --sort=-%cpu | awk '{arr[$1]+=$2;} END {for (i in arr) {print i,arr[i]}}'|grep -v ' 0'|awk '{print $1}');do 
  u=( ${u[@]} $j);done
for ((i=0;i<${#u[@]};i+=1));do 
  echo $(date) ${u[$i]} ${c[$i]};done
```

### 結果

```bash
kuang@dev2 /home/GFS
$ ./list_cpu.cs
Wed Jul 26 09:29:32 CST 2023 kuang 4.1
Wed Jul 26 09:29:32 CST 2023 mssql 1.5
Wed Jul 26 09:29:32 CST 2023 root 5.1
```

### crontab應用

- 在程式執行的同時，另行監控CPU的使用率，了解是否有其他使用者與其使用情形，以檢討資源利用的有效性。
- 使用crontab控制每5分鐘詢問一次，並將每次統計結果附掛在檔案之後備查。

```bash
#WRF forecasting from gfs and CWBWRF results
30 17 * * * /home/GFS/fcst_devp.cs >& /home/GFS/fcst_devp.out
*/5 17-23 * * * rm /home/GFS/list_cpu.out;/home/GFS/list_cpu.cs >> /home/GFS/list_cpu.out
```

## 腳本說明

這個 Bash 腳本的目的是列出正在運行的進程中 CPU 使用率最高的用戶以及對應的 CPU 使用率百分比。以下是腳本的主要步驟：

1. **創建空陣列：**
   - 使用 `c=()` 和 `u=()` 分別創建空陣列 `c`（存儲 CPU 使用率百分比）和 `u`（存儲用戶名）。

2. **提取 CPU 使用率資訊：**
   - 使用 `ps` 命令列出所有進程的用戶名和 CPU 使用率，按 CPU 使用率降序排序。
   - 使用 `awk` 對用戶名和對應的 CPU 使用率進行統計，並過濾掉 CPU 使用率為零的項目。

3. **填充陣列：**
   - 將提取到的 CPU 使用率和用戶名分別填充到陣列 `c` 和 `u` 中。

4. **遍歷陣列並打印：**
   - 使用 `for` 迴圈遍歷 `u` 和 `c` 陣列，並在每次迴圈中使用 `echo` 命令打印時間、用戶名和對應的 CPU 使用率。

總的來說，這個腳本用於監視系統中 CPU 使用率最高的用戶，並在每次運行時打印出時間、用戶名和對應的 CPU 使用率。