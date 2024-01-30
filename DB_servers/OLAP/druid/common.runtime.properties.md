

### 指定伺服器IP及連接埠

- 參數
  - 伺服器主機：`druid.host`
  - 分布式協調伺服器(ZooKeeper)：`druid.zk.service.host`
  - 元數據儲存連接器：`druid.metadata.storage.connector`
  - 

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