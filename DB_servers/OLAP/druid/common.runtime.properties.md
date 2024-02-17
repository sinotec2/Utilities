---
layout: default
title:  common.runtime.properties
parent: Apache Druid
grand_parent: OLAP
last_modified_date: 2024-01-31 19:49:51
tags: DB_servers Druid
---

# Apache Druid 主要設定檔
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

- 檔案位置
  - `./conf/druid/cluster/_common/common.runtime.properties`

## 內設與建議

### 外掛清單

- 在載入列表清單中指定將由Druid加載外掛項目名稱。
- 如果您指定清單為一空序列：`druid.extensions.loadList=[]`，Druid將不會從文件系統加載任何外掛。
- 如果您不指定`druid.extensions.loadList`，Druid將加載根擴展目錄下的所有擴展。
- 更多信息: [加載擴展](https://druid.apache.org/docs/latest/operations/including-extensions.html)
- 快速啟動內設加載項目

項目|內容|說明
-|-|-
`druid-hdfs-storage`|穩定的儲存方式|
`druid-kafka-indexing-service`||
`druid-datasketches`||
`druid-multi-stage-query`||

## 核心加載項目

### 與雲平台及深層儲存服務有關項目

項目|內容說明
-|-
`druid-avro-extensions`|支援 Apache Avro 資料格式的資料
`druid-azure-extensions`|微軟Azure深度儲存
`druid-ec2-extensions`|與 AWS EC2 連線以自動擴展中間管理者功能
`druid-google-extensions`|谷歌雲端儲存深層儲存
`druid-hdfs-storage`|HDFS深度儲存
`druid-s3-extensions`|與AWS S3中的資料交互，並使用S3作為深度儲存。

### 安全管理

項目|內容說明
-|-
`druid-basic-security`|支援基本 HTTP 驗證和基於角色的存取控制
`druid-ranger-security`|透過 Apache Ranger 進行存取控制
`druid-kerberos`|druid 程序的 Kerberos 驗證
`druid-aws-rds-extensions`|支援基於 AWS 令牌存取 AWS RDS 資料庫叢集
`druid-pac4j`|用於 druid 進程的 OpenID Connect 身份驗證。

### 大數據及統計工具

項目|內容說明
-|-
`druid-histogram`|已棄用，改用DataSketches 分位數聚合器
`druid-stats`|統計相關模組包括變異數和標準差
`druid-bloom-filter`|支援在 Druid 查詢中提供布隆過濾器
`druid-datasketches`|進行近似計數和集合操作

### 檢索(lookup)工具

項目|內容說明
-|-
`druid-kafka-extraction-namespace`|命名空間查找
`druid-lookups-cached-global`|一個用於查找的模組，為查找提供 jvm 全域熱切快取。它提供了用於獲取查找資料的 JDBC 和 URI 實作
`druid-lookups-cached-single`|每個查找快取模組支援需要將查找與全域查找池隔離的用例

### 索引(indexing)工具

項目|內容說明
-|-
`druid-kinesis-indexing-service`|監督索引服務的一次性 Kinesis 攝取
`druid-kafka-indexing-service`|監督索引服務的一次性 Apache Kafka 攝取

### 查詢(query)工具

項目|內容說明
-|-
`druid-multi-stage-query`|支援Apache Druid的多階段查詢架構和多階段查詢任務引擎

### 資料庫元數據之存儲

項目|內容說明
-|-
`mysql-metadata-storage`|MySQL 元資料儲存
`postgresql-metadata-storage`|PostgreSQL 元資料儲存
`druid-catalog`|[附加元資料目錄](https://github.com/apache/druid/issues/12546)，允許使用者在 Druid 中記錄資料形狀決策並重複使用。

### 叢集與通訊

項目|內容說明
-|-
`druid-kubernetes-extensions`|沒有 Zookeeper 的 Kubernetes 上的 Druid 叢集部署。
`simple-client-sslcontext`|透過 HTTPS 與其他 Druid 進程通訊時，Druid 的內部 HttpClient 使用簡單的 SSLContext 提供者模組。

### 特殊格式支援

項目|內容說明
-|-
`druid-orc-extensions`|支援 Apache ORC 資料格式的資料
`druid-parquet-extensions`|支援 Apache Parquet 資料格式的資料
`druid-protobuf-extensions`|支援 Protobuf 資料格式的資料

### 儲存方式

- 此處內設使用本地檔案系統作為深層存儲，
  - 但不建議在生產中使用。請改用S3、HDFS或NFS等較穩定的儲存方式。
- 資料庫元數據之存儲方式，內設使用本地之derby
  - 也不建議在生產中使用
  - 請改用MySQL或Postgres。



## 檔案全文

```bash
kuang@DEVP ~/MyPrograms/Apache_Druid/apache-druid-28.0.1
$ cat ./conf/druid/cluster/_common/common.runtime.properties
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

# Extensions specified in the load list will be loaded by Druid
# We are using local fs for deep storage - not recommended for production - use S3, HDFS, or NFS instead
# We are using local derby for the metadata store - not recommended for production - use MySQL or Postgres instead

# If you specify `druid.extensions.loadList=[]`, Druid won't load any extension from file system.
# If you don't specify `druid.extensions.loadList`, Druid will load all the extensions under root extension directory.
# More info: https://druid.apache.org/docs/latest/operations/including-extensions.html
druid.extensions.loadList=["druid-hdfs-storage", "druid-kafka-indexing-service", "druid-datasketches", "druid-multi-stage-query"]

# If you have a different version of Hadoop, place your Hadoop client jar files in your hadoop-dependencies directory
# and uncomment the line below to point to your directory.
#druid.extensions.hadoopDependenciesDir=/my/dir/hadoop-dependencies


#
# Hostname
#
druid.host=localhost

#
# Logging
#

# Log all runtime properties on startup. Disable to avoid logging properties on startup:
druid.startup.logging.logProperties=true

#
# Zookeeper
#

druid.zk.service.host=localhost
druid.zk.paths.base=/druid

#
# Metadata storage
#

# For Derby server on your Druid Coordinator (only viable in a cluster with a single Coordinator, no fail-over):
druid.metadata.storage.type=derby
druid.metadata.storage.connector.connectURI=jdbc:derby://localhost:1527/var/druid/metadata.db;create=true
druid.metadata.storage.connector.host=localhost
druid.metadata.storage.connector.port=1527

# For MySQL (make sure to include the MySQL JDBC driver on the classpath):
#druid.metadata.storage.type=mysql
#druid.metadata.storage.connector.connectURI=jdbc:mysql://db.example.com:3306/druid
#druid.metadata.storage.connector.user=...
#druid.metadata.storage.connector.password=...

# For PostgreSQL:
#druid.metadata.storage.type=postgresql
#druid.metadata.storage.connector.connectURI=jdbc:postgresql://db.example.com:5432/druid
#druid.metadata.storage.connector.user=...
#druid.metadata.storage.connector.password=...

#
# Deep storage
#

# For local disk (only viable in a cluster if this is a network mount):
druid.storage.type=local
druid.storage.storageDirectory=var/druid/segments

# For HDFS:
#druid.storage.type=hdfs
#druid.storage.storageDirectory=/druid/segments

# For S3:
#druid.storage.type=s3
#druid.storage.bucket=your-bucket
#druid.storage.baseKey=druid/segments
#druid.s3.accessKey=...
#druid.s3.secretKey=...

#
# Indexing service logs
#

# For local disk (only viable in a cluster if this is a network mount):
druid.indexer.logs.type=file
druid.indexer.logs.directory=var/druid/indexing-logs

# For HDFS:
#druid.indexer.logs.type=hdfs
#druid.indexer.logs.directory=/druid/indexing-logs

# For S3:
#druid.indexer.logs.type=s3
#druid.indexer.logs.s3Bucket=your-bucket
#druid.indexer.logs.s3Prefix=druid/indexing-logs

#
# Service discovery
#

druid.selectors.indexing.serviceName=druid/overlord
druid.selectors.coordinator.serviceName=druid/coordinator

#
# Monitoring
#

druid.monitoring.monitors=["org.apache.druid.java.util.metrics.JvmMonitor", "org.apache.druid.server.metrics.ServiceStatusMonitor"]
druid.emitter=noop
druid.emitter.logging.logLevel=info

# Storage type of double columns
# ommiting this will lead to index double as float at the storage layer

druid.indexing.doubleStorage=double

#
# Security
#
druid.server.hiddenProperties=["druid.s3.accessKey","druid.s3.secretKey","druid.metadata.storage.connector.password", "password", "key", "token", "pwd"]


#
# SQL
#
druid.sql.enable=true

# Planning SQL query when there is aggregate distinct in the statement
druid.sql.planner.useGroupingSetForExactDistinct=true

#
# Lookups
#
druid.lookup.enableLookupSyncOnStartup=false

#
# Expression processing config
#
druid.expressions.useStrictBooleans=true

#
# Http client
#
druid.global.http.eagerInitialization=false
```