---
layout: default
title:  Druid Q&A
parent: Apache Druid
grand_parent: DB_servers
grand_parent: OLAP
last_modified_date: 2024-01-07 20:26:18
tags: DB_servers Druid
---

# Apache Druid General Q&A
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

- 控制檔：`common.runtime.properties`

### 指定伺服器IP及連接埠

- 參數
  - 伺服器主機：`druid.host`
  - 分布式協調伺服器(ZooKeeper)：`druid.zk.service.host`
  - 元數據儲存連接器：`druid.metadata.storage.connector`

```bash
kuang@DEVP /home/ApacheDruidSvrs/apache-druid-28.0.1_8887
$ d='conf/druid/auto/_common'
kuang@DEVP /home/ApacheDruidSvrs/apache-druid-28.0.1_8887
$ diff $d/common.runtime.properties ~/MyPrograms/Apache_Druid/apache-druid-28.0.1/$d/common.runtime.properties
36,37c36,37
< #
< druid.host=localhost

---
> # localhost
> druid.host=200.200.32.195
50c50,51
< druid.zk.service.host=localhost
---
> druid.zk.service.host=200.200.32.195
> #localhost
59,60c60,63
< druid.metadata.storage.connector.connectURI=jdbc:derby://localhost:1527/var/druid/metadata.db;create=true
< druid.metadata.storage.connector.host=localhost
---
> druid.metadata.storage.connector.connectURI=jdbc:derby://200.200.32.195:1527/var/druid/metadata.db;create=true
> #ocalhost:1527/var/druid/metadata.db;create=true
> druid.metadata.storage.connector.host=200.200.32.195
> #localhost
```

## verify-default-ports


```bash
./bin/verify-default-ports:  @ports = (1527, 2181, 8081, 8082, 8083, 8090, 8091, 8100, 8200, 8888);
```

### 腳本程式說明

這個 Perl 腳本用於檢查 Druid 是否能夠使用默認端口。該腳本確保 Druid 所需的一組端口沒有被其他應用程序占用。

腳本的主要步驟如下：

1. **引入模塊：** 使用 `use` 關鍵字引入 `strict` 和 `warnings` 模塊，啟用 Perl 的嚴格模式和警告。

2. **定義 `try_bind` 函數：** 該函數嘗試在給定端口上綁定 socket。如果綁定失敗，說明該端口已被使用，並退出腳本。

3. **獲取環境變數：** 檢查是否存在 `DRUID_SKIP_PORT_CHECK` 環境變數，如果存在並且不等於 "0"、"false" 或 "f"，則跳過端口檢查，直接退出腳本。

4. **設置默認端口列表：** 如果未提供命令行參數，使用一組默認端口，包括 1527、2181、8081、8082、8083、8090、8091、8100、8200 和 8888。

5. **循環檢查端口：** 對於每個端口，調用 `try_bind` 函數嘗試在該端口上進行綁定。首先在所有本地接口上嘗試，然後在 127.0.0.1 上嘗試。如果端口已被使用，輸出錯誤信息，退出腳本。

6. **輸出錯誤信息：** 如果發現任何端口被占用，輸出錯誤信息，指導用戶檢查端口並提供修改端口的方式。如果用戶確信這是錯誤的檢查，或者已經更改了端口，可以使用環境變數 `DRUID_SKIP_PORT_CHECK` 來跳過此檢查。

此腳本的目的是確保 Druid 可以使用指定的端口，如果發現端口被佔用，則提供相應的解決方案。

### perl script

```perl
kuang@DEVP /home/ApacheDruidSvrs/apache-druid-28.0.1_8887
$ cat ./bin/verify-default-ports
#!/usr/bin/env perl

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

use strict;
use warnings;
use Socket;

sub try_bind {
  my ($port, $addr) = @_;

  socket(my $sock, PF_INET, SOCK_STREAM, Socket::IPPROTO_TCP) or die "socket: $!";
  setsockopt($sock, SOL_SOCKET, SO_REUSEADDR, pack("l", 1)) or die "setsockopt: $!";
  if (!bind($sock, sockaddr_in($port, $addr))) {
    print STDERR <<"EOT";
Cannot start up because port $port is already in use.

If you need to change your ports away from the defaults, check out the
configuration documentation:

  https://druid.apache.org/docs/latest/configuration/index.html

If you believe this check is in error, or if you have changed your ports away
from the defaults, you can skip this check using an environment variable:

  export DRUID_SKIP_PORT_CHECK=1

EOT
    exit 1;
  }
  shutdown($sock, 2);
}

my $skip_var = $ENV{'DRUID_SKIP_PORT_CHECK'};
if ($skip_var && $skip_var ne "0" && $skip_var ne "false" && $skip_var ne "f") {
  exit 0;
}

my @ports = @ARGV;
if (!@ports) {
  @ports = (1527, 2181, 8081, 8082, 8083, 8090, 8091, 8100, 8200, 8888);
}

for my $port (@ports) {
  try_bind($port, INADDR_ANY);
  try_bind($port, inet_aton("127.0.0.1"));
}
```
