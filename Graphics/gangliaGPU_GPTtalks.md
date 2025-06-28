---
layout: default
title: Ganglia 偵錯
parent: Graphics
last_modified_date: 2025-06-26 11:18
tags:
  - graphics
---

# Ganglia 偵錯
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

根據你提供的有關 Ganglia 系統的 GPT 對話內容，以下是整理和分類的知識點：

## 1. 系統負載檢查

- **命令與數據解析**:
    
    ```bash
    sudo cat /proc/loadavg
    ```
    
    - 輸出示例：`0.43 0.56 0.64 1/4585 45560`
    - **解釋**：
        - 系統負載量相對較低，特別是與 CPU 核心的數量相比。
        - 負載在 1.0 以下（每個核心）是正常的。

## 2. 記憶體使用情況

- **命令與數據解析**:
    
    ```bash
    sudo cat /proc/meminfo
    ```
    
    - **關鍵數據**：
        - `MemTotal`: 總記憶體容量
        - `MemFree`: 空閒的記憶體
        - `MemAvailable`: 可用的記憶體
    - **解釋**：
        - 系統有足夠的記憶體來處理當前的負載。

## 3. Ganglia gmond 配置

### 3.1 UDP 接收通道設定

- **設定示例**:
    
    ```plaintext
    udp_recv_channel {
        port = 8649
        bind = 0.0.0.0
    }
    ```
    
- **註解**：
    
    - 可根據需要修改 `port` 和 `bind` 設置。

### 3.2 關於註記

- 註記掉 `udp_recv_channel` 不會影響資料上載到其他 Ganglia 主機。

### 3.3 數據上載檢查

- **命令與輸出示例**:
    
    ```bash
    tcpdump -i eno1
    ```
    
    - 輸出示例：`UDP, length 44`
- **解釋**：
    
    - 表明數據已經成功上載到遠端的 Ganglia 主機。

## 4. gmond 傳送的數據

- gmond 會傳送：
    1. **RRD 檔案**：圓形輪廓格式，用於儲存時間序列數據。
    2. **XML 檔案**：描述叢集狀態的數據。
    3. **快照檔案**：即時狀態的記錄。
    4. **日誌檔案**：運行狀態和錯誤的記錄。

### 4.1 XML 檔案位置

- 通常位於 `/var/lib/ganglia/` 目錄下。

### 4.2 資料上傳到兩個 gmetad 主機

- 可使用多個 `udp_send_channel` 來配置。
    
- **範例配置**:
    
    ```plaintext
    udp_send_channel {
        host = gmetad_host1
        port = 8649
    }
    udp_send_channel {
        host = gmetad_host2
        port = 8649
    }
    ```
    

## 5. 錯誤處理

### 5.1 配置錯誤

- **錯誤信息**:
    
    ```plaintext
    Fatal error: Errors were detected in your configuration.
    ```
    
- **解決步驟**：
    
    1. 確保 RRDs 和 DWOO 目錄具有正確的讀寫權限。
    2. 更新配置文件中的 `@vargmetadir@` 和 `@vargwebstatedir@` 為實際路徑。
    3. 檢查目錄的存在與權限。

### 5.2 Python 模組錯誤

- **錯誤示例**:
    
    ```plaintext
    SyntaxError: multiple exception types must be parenthesized
    ```
    
- **解決方案**：
    
    - 在 Python 3 中，捕獲多個異常類型必須使用括號。
    
    ```python
    except (NVMLError, err):
    ```
    

### 5.3 .so 檔案說明

- `.so` 文件為共享物件檔案，通常用於 Linux 系統中，以提供共用的函數庫。

### 5.4 啟動 gmond 的 Python 功能

- 確保 `gmond.conf` 中正確配置了 Python 模組，並確定所需的腳本存在且可執行。

## 6. Python 版本兼容性注意事項

- 在 Python 3 中執行 Python 2 的程式碼需要注意語法差異。
- 使用工具如 `2to3` 進行自動轉換，或者手動修改語法。

### 6.1 使用模組導入

- 使用 `from __future__ import print_function` 來獲取 Python 3 的 print 功能等。

### 6.2 Makefile.am 使用指南

#### 6.2.1 Makefile.am 基本用法

- **文件建立**： 在專案根目錄中建立名為 `Makefile.am` 的文件。
    
- **撰寫基本規則**：
    
    ```makefile
    bin_PROGRAMS = myprogram
    myprogram_SOURCES = main.c utils.c
    ```
    
    這表示將生成名為 `myprogram` 的可執行檔，源文件為 `main.c` 和 `utils.c`。
    
- **執行 Automake 和 Autoconf**：
    
    ```bash
    aclocal
    autoconf
    automake --add-missing
    ```
    
- **配置和編譯**：
    
    ```bash
    ./configure
    make
    ```
    
- **安裝**：
    
    ```bash
    make install
    ```
    

#### 6.2.2 配置錯誤處理

- **錯誤信息**：
    
    ```
    configure: error: cannot find required auxiliary files: compile config.guess config.sub missing install-sh
    ```
    
- **解決步驟**：
    
    1. 確保已安裝 Automake 和 Autoconf：
        
        ```bash
        automake --version
        autoconf --version
        ```
        
    2. 生成缺失的文件：
        
        ```bash
        aclocal
        autoconf
        automake --add-missing
        ```
        
    3. 重新運行配置：
        
        ```bash
        ./configure
        ```
        
    4. 編譯和安裝：
        
        ```bash
        make
        make install
        ```
        

### 6.3 LIBTOOL

#### 6.3.1 定義 LIBTOOL

- 當將 `AC_PROG_LIBTOOL` 改成 `LT_INIT` 時，若出現錯誤：
    
    ```
    error: Libtool library used but ‘LIBTOOL’ is undefined
    ```
    
- **解決方法**：
    
    1. 在 `configure.ac` 中添加 `LT_INIT`：
        
        ```m4
        LT_INIT
        ```
        
    2. 重新生成配置文件：
        
        ```bash
        aclocal
        autoconf
        automake --add-missing
        ```
        
    3. 再次運行`./configure`。
        

#### 6.3.2 自動產生config.h

- **解釋**：
    
    ```
    AC_CONFIG_HEADERS([config.h:config.h.in])
    ```
    
    這段代碼表示會自動生成 `config.h` 文件。
    

### 6.4 錯誤排查

#### 6.4.1 Makefile.am 的基本用法

- **文件創建**：在專案根目錄中創建 `Makefile.am`。
    
- **撰寫示例**：
    
    ```makefile
    bin_PROGRAMS = myprogram
    myprogram_SOURCES = main.c utils.c
    ```
    
- **執行 Automake 和 Autoconf**：
    
    ```bash
    aclocal
    autoconf
    automake --add-missing
    ```
    

#### 6.4.2 make 缺失分隔符

- **錯誤信息**：
    
    ```
    Makefile:5: *** missing separator. Stop.
    ```
    
- **解決步驟**：
    
    1. 確保所有命令行都以制表符（tab）開始，而不是空格。

#### 6.4.3 if 條件語句

- **基本語法**：
    
    ```makefile
    ifeq (条件1, 条件2)
        # 条件为真时执行的命令
    else
        # 条件为假时执行的命令
    endif
    ```
    
- **示例**：
    
    ```makefile
    ifdef VARIABLE_NAME
        # 某些命令
    else
        # 另一些命令
    endif
    ```
    

#### 6.4.4 缺少庫文件

- **錯誤信息**：
    
    ```
    /usr/bin/ld: cannot find -lpython2.7: No such file or directory
    ```
    
- **解決步驟**：
    
    1. 在 `Makefile` 中添加庫路徑：
        
        ```makefile
        LDFLAGS += -L/opt/anaconda3/envs/py27/lib/python2.7/config
        ```
        
    2. 使用環境變數：
        
        ```bash
        export LIBRARY_PATH=/opt/anaconda3/envs/py27/lib/python2.7/config:$LIBRARY_PATH
        ```
        

### 6.5 Ganglia gmond 錯誤處理

#### 6.5.1 gmond 讀取錯誤

- **錯誤信息**：
    
    ```
    Cannot load /var/lib/ganglia/python_modules/modpython.so metric module: undefined symbol: sincos
    ```
    
- **解決方法**：
    
    1. 確保在編譯 `modpython.so` 時連結了數學庫 `libm`：
        
        ```bash
        gcc -shared -o modpython.so your_source.c -lm
        ```
        
    2. 使用 `ldd` 檢查依賴項：
        
        ```bash
        ldd /var/lib/ganglia/python_modules/modpython.so
        ```
        

#### 6.5.2 Module Initialization Failed

- **錯誤信息**：
    
    ```
    Module python_module failed to initialize.
    ```
    
- **解決步驟**：
    
    1. 檢查 `PYTHONPATH` 環境變數，確保包含 Python 模塊的目錄。
    2. 檢查 `gmond` 的配置文件中 Python 模塊的路徑是否正確。
    3. 確保運行 `gmond` 的用戶對 Python 模塊有讀取權限。
    4. 查看 `gmond` 日誌獲取更詳細的錯誤信息。

#### 6.5.3 網路與發送問題

- 驗證網路配置確保 gmond 能夠正常發送數據到指定的主機。

## 7. 錯誤訊息處理

### 7.1 libpcre.so.0 缺失

- **錯誤信息**：
    
    ```
    Cannot load /var/lib/ganglia/python_modules/modpython.so metric module: libpcre.so.0: cannot
    ```
    
- **解決步驟**：
    
    1. **安裝 PCRE 庫**：
        
        ```bash
        sudo apt-get install libpcre3
        ```
        
    2. **檢查正確版本**：
        
        ```bash
        ldconfig -p | grep libpcre
        ```
        
    3. **創建符號鏈接**（如果需要）：
        
        ```bash
        sudo ln -s /usr/lib/x86_64-linux-gnu/libpcre.so.1 /usr/lib/x86_64-linux-gnu/libpcre.so.0
        ```
        
    4. **檢查庫路徑**：
        
        ```bash
        export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
        ```
        
    5. **重新安裝 Ganglia**（如有需要）：
        
        ```bash
        sudo apt-get remove ganglia
        sudo apt-get install ganglia
        ```
        

### 7.2 無法找到輔助文件

- **錯誤信息**：
    
    ```
    configure: error: cannot find required auxiliary files: compile config.guess config.sub missing install-sh
    ```
    
- **解決步驟**：
    
    1. **確認已安裝 Automake 和 Autoconf**：
        
        ```bash
        automake --version
        autoconf --version
        ```
        
    2. **生成缺失的文件**：
        
        ```bash
        aclocal
        autoconf
        automake --add-missing
        ```
        

### 7.3 undefined symbol: sincos

- **錯誤信息**：
    
    ```
    Cannot load /var/lib/ganglia/python_modules/modpython.so metric module: undefined symbol: sincos
    ```
    
- **解決步驟**：
    
    1. **確保連結數學庫**（添加 `-lm`）：
        
        ```bash
        gcc -shared -o modpython.so your_source.c -lm
        ```
        

## 8. 依賴庫管理

### 8.1 安裝需要的依賴

- **APR**：
    
    ```bash
    sudo apt-get install libapr1-dev
    ```
    
- **libconfuse**：
    
    ```bash
    sudo apt-get install libconfuse-dev
    ```
    
- **PCRE**：
    
    ```bash
    sudo apt-get install libpcre3-dev
    ```
    
- **Sun RPC**：
    
    ```bash
    sudo apt-get install libtirpc-dev
    ```
    

9. Ganglia 配置解析

### 9.1 host_dmax

- **定義**：`host_dmax` 指定最大時間（秒），在沒有更新數據的情況下主機被視為活躍的最大時間。設置為 0 表示永久活躍。

### 9.2 時間敏感指標

- 重要指標：
    - `gpu0_util.rrd` - GPU 使用率
    - `gpu0_temp.rrd` - GPU 溫度
    - `gpu0_fan.rrd` - 風扇轉速
    - `gpu0_power_usage_report.rrd` - 功耗
    - `gpu0_shutdown_temp.rrd` - 關閉溫度

## 10. RRD 數據匯總與錯誤排查調試

### 10.1 rrdtool dump

- **解釋**：`rrdtool dump` 會匯總指定時間範圍內的數據，生成快照以便於分析。

### 10.2 fsockopen error

- **錯誤信息**：
    
    ```
    fsockopen error: Connection refused
    ```
    
- **解決步驟**：
    
    - 確認 `gmond` 是否運行。
    - 檢查配置文件。
    - 確認沒有防火牆問題。
    - 驗證端口衝突。

---

