---
layout: default
title: Python程式語言工作手冊
parent: python
grand_parent: Languages
last_modified_date: 2024-01-02 13:33:58
tags: UML
---

# Python **程式語言工作手冊**

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

## 背景說明

### Python的特性

#### 緣起與版本[^1]

Python的創始人為吉多·范羅蘇姆（Guido van Rossum）。1989年的聖誕節期間，吉多·范羅蘇姆為了在阿姆斯特丹打發時間，決心開發一個新的腳本解釋程式，作為ABC語言[^2]的一種繼承。之所以選中Python作為程式的名字，是因為他是BBC電視劇------蒙提·派森的飛行馬戲團（Monty
Python's Flying Circus）的愛好者。ABC是由吉多參加設計的一種教學語言。就吉多本人看來，ABC這種語言非常優美和強大，是專門為非專業程式設計師設計的。但是ABC語言並沒有成功，究其原因，吉多認為是非**開放**[^3]造成的。吉多決心在Python中避免這一錯誤，並取得了非常好的效果，完美結合了C和其他一些語言。

就這樣，Python在吉多手中誕生了。實際上，第一個實現是在Mac機上。可以說，Python是從ABC發展起來，主要受到了Modula-3（另一種相當優美且強大的語言，為小型團體所設計的）的影響。並且結合了Unix shell[^4]和C的習慣。

目前吉多仍然是Python的主要開發者，決定整個Python語言的發展方向。Python社群經常稱呼他是仁慈的獨裁者。

Python 2.0於2000年10月16日發布，增加了實現完整的**[垃圾回收]{.underline}**[^5]，並且支援Unicode[^6]。同時，整個開發過程更加透明，社群對開發進度的影響逐漸擴大。Python 3.0 於2008年12月3日發布，此版不完全相容之前的Python原始碼。不過，很多新特性後來也被移植到舊的Python 2.6/2.7版本。

Python的「禪」(理念)

凡是用過 Python的人，基本上都知道在互動式解譯器(ipython)中輸入 import this 就會顯示 Tim Peters 的 The Zen of Python，闡述Python程式編碼的原則(哲學)，中文翻譯修改自網友[^7]並列如下。

+----------------------------------+----------------------------------+
| The Zen of Python, by Tim Peters | Python之禪 by Tim Peters         |
+----------------------------------+----------------------------------+
| Beautiful is better than ugly.   | 優                               |
|                                  | 美勝於醜陋（Python以優美為目標） |
+----------------------------------+----------------------------------+
| Explicit is better than          | 明瞭                             |
| implicit.                        | 勝於晦澀（儘量以外顯方式來宣告） |
+----------------------------------+----------------------------------+
| Simple is better than complex.   | 簡潔                             |
|                                  | 勝於複雜（不要有複雜的內部實現） |
+----------------------------------+----------------------------------+
| Complex is better than           | 複雜勝於淩亂                     |
| complicated.                     | （如果複雜不可避免，那代碼間也不 |
|                                  | 能有難懂的關係，要保持介面簡潔） |
+----------------------------------+----------------------------------+
| Flat is better than nested.      | 扁平勝                           |
|                                  | 於套疊（不要有太多迴圈或副程式） |
+----------------------------------+----------------------------------+
| Sparse is better than dense.     | 鬆散更勝於緊湊（有適當的         |
|                                  | 間隔，不要奢望一行代碼解決問題） |
+----------------------------------+----------------------------------+
| Readability counts.              | 可讀                             |
|                                  | 才算數（優美的編碼必須是可讀的） |
+----------------------------------+----------------------------------+
| Special cases aren't special    | 即使實用性考量可能更勝於         |
| enough to break the rules.       | 單純性，特例也還不是很特殊，以致 |
|                                  | 必須違背規則（這些規則至高無上） |
| Although practicality beats      |                                  |
| purity.                          |                                  |
+----------------------------------+----------------------------------+
| Errors should never pass         | 不要讓錯誤無聲無息的發生，除     |
| silently.                        | 了精準捕獲異常並故意不顯示（不寫 |
|                                  | except:pass 風格的代碼）         |
| Unless explicitly silenced.      |                                  |
+----------------------------------+----------------------------------+
| In the face of ambiguity, refuse | 面對模棱兩可時，不要嘗試去猜測   |
| the temptation to guess.         |                                  |
|                                  | 而是儘                           |
| There should be one\-- and       | 量找一種，最好是唯一一種明顯的解 |
| preferably only one \--obvious   | 決方案（如果不確定，就用窮舉法） |
| way to do it.                    |                                  |
+----------------------------------+----------------------------------+
| Although that way may not be     | 雖然一                           |
| obvious at first unless you're  | 開始這道路並非顯然易懂，除非你是 |
| Dutch.                           | Python 之父（這裡的 Dutch 是指   |
|                                  | Guido ）                         |
+----------------------------------+----------------------------------+
| Now is better than never.        | 現在就嘗試處理，比永不處理更好。 |
|                                  |                                  |
| Although never is often better   | 雖然永不處理常常是               |
| than *right* now.              | 比馬上處理還好一些。(勿莽撞嘗試) |
+----------------------------------+----------------------------------+
| If the implementation is hard to | 如果不容                         |
| explain, it's a bad idea.       | 易向人描述你的實現方案，那肯定是 |
|                                  | 一個壞點子；如果方案很容易解釋， |
| If the implementation is easy to | 可能是一個好點子（方案測評標準） |
| explain, it may be a good idea.  |                                  |
+----------------------------------+----------------------------------+
| Namespaces are one honking great | 命名空間是一種絕妙的理念         |
| idea \-- let's do more of       | ，我們應當多加利用（宣導與號召） |
| those!                           |                                  |
+----------------------------------+----------------------------------+

## Python的應用

### 大數據分析

#### 資料科學概論[^8]

Data science, analytics, machine learning, big data... All familiar
terms in today's tech headlines, but they can seem daunting, opaque or
just simply impossible. Despite their schick gleam, they are *real*
fields and you can master them! We'll dive into what data science
consists of and how we can use Python to perform data analysis for us.

Data science is a large field covering everything from data collection,
cleaning, standardization, analysis, visualization and reporting.
Depending on your interests there are many different positions,
companies and fields which touch data science. You can use data science
to analyze language, recommend videos, or to determine new products from
customer or marketing data. Whether it's for a research field, your
business or the company you work for, there's many opportunities to use
data science and analysis to solve your problems.

When we talk about using big data in data science, we are talking about
large scale data science. What "big" is depends a bit on who you ask.
Most projects or questions you'd like to answer don't require big data,
since the dataset is small enough to be downloaded and parsed on your
computer. Most big data problems arise out of data that can't be held on
one computer. If you have large data requiring several (or more)
computers to store, you can benefit from big data parsing libraries and
analytics.

So what does Python have to do with it? Python has emerged over the past
few years as a leader in data science programming. While there are still
plenty of folks using R, SPSS, Julia or several other popular languages,
Python's growing popularity in the field is evident in the growth of its
data science libraries. Let's take a look at a few of them.

#### Pandas

One of the most popular data science libraries is
[[Pandas]{.underline}](http://pandas.pydata.org/). Developed by data
scientists familiar with R and Python, it has grown to support a large
community of scientists and analysts. It has many built-in features,
such as the ability to read data from many sources, create large
dataframes (or matrixes / tables) from these sources and compute
aggregate analytics based on what questions you'd like to answer. It has
some built-in visualizations which can be used to chart and graph your
results as well as several export functions to turn your completed
analysis into an Excel Spreadsheet.

#### Agate

A much younger and newer library which aims to solve data analysis
problems is
[[agate]{.underline}](https://source.opennews.org/en-US/articles/introducing-agate/).
Agate was developed with journalism in mind, and has many great features
for dataset analysis. Do you have a few spreadsheets you need to analyze
and compare? Do you have a database on which you'd like to run some
statistics? Agate has a much smaller learning curve and less
dependencies than Pandas, and has some really neat charting and viewing
features so you can see your results quickly.

#### Bokeh

If you're interested in creating visualizations of your finished
dataset, [[Bokeh]{.underline}](http://bokeh.pydata.org/en/latest/) is a
great tool. It can be used with agate, Pandas, other data analysis
libraries or pure Python. Bokeh helps you make striking visualizations
and charts of all types without much code.

There are many other libraries to explore, but these are a great place
to start if you're interested in data science with Python. Now let's
talk about "big data."

WORKING WITH BIG DATA: MAP-REDUCE

When working with large datasets, it's often useful to utilize
MapReduce. MapReduce is a method when working with big data which allows
you to first map the data using a particular attribute, filter or
grouping and then reduce those using a transformation or aggregation
mechanism. For example, if I had a collection of cats, I could first map
them by what color they are and then reduce by summing those groups. At
the end of the MapReduce process, I would have a list of all the cat
colors and the sum of the cats in each of those color groupings.

Almost every data science library has some MapReduce functionality built
in. There are also numerous larger libraries you can use to manage the
data and MapReduce over a series of computers (or a cluster / grouping
of computers). Python can speak to these services and software and
extract the results for further reporting, visualization or alerting.

#### Hadoop

If the most popular libraries for MapReduce with large datasets is
Apache's [[Hadoop]{.underline}](https://hadoop.apache.org/). Hadoop uses
cluster computing to allow for faster data processing of large datasets.
There are many Python libraries you can use to send your data or jobs to
Hadoop and which one you choose should be a mixture of what's easiest
and most simple to set up with your infastructure, and also what seems
like the most clear library for your use case.

#### Spark

If you have large data which might work better in streaming form
(real-time data, log data, API data), then Apache's
[[Spark]{.underline}](http://spark.apache.org/) is a great tool.
PySpark, the Python Spark API, allows you to quickly get up and running
and start mapping and reducing your dataset. It's also incredibly
popular with machine learning problems, as it has some built-in
algorithms.

#### 2016年壹讀網站[^9]-該使用哪種語言?

R[^10]、Python、Scala 和
Java，到底該使用哪一種大數據程式語言？恐怕這還得「視情況而定」。如果你對晦澀的統計運算進行繁重的數據分析工作，那麼你不青睞R才怪。如果你跨GPU[^11]進行NLP[^12]或密集的神經網絡處理，那麼Python是很好的選擇。如果想要一種加固的、面向生產環境的數據流解決方案，又擁有所有重要的操作工具，Java或Scala[^13]絕對是出色的選擇。

當然，不一定非此即彼。比如說，如果使用Spark[^14]，你可以藉助靜態數據，使用R或Python來訓練模型和機器學習管道(pipeline)，然後對該管道進行序列化處理，倒出到存儲系統，那裡它可以供你的生產Scala
Spark
Streaming應用程式使用。雖然你不應該過分迷戀某一種語言(不然你的團隊很快會產生語言疲勞)，使用一套發揮各自所長的異構語言也許會給大數據項目帶來成效。

批踢踢[^15]：請問Python在業界都用來寫什麼?

#### Python處理大數據的劣勢：

python線程有gil[^16]，通俗說就是多線程的時候只能在一個核上跑，浪費了多核服務器(已解決，如Cython或Numba[^17])。

python在處理大數據的時候，效率不高，[[pypy]{.underline}](https://pypy.org/)（一個jit[^18]的python解釋器，可以理解成腳本語言加速執行的東西）能夠提高很大的速度(可以快10倍)，但是pypy不支持很多python經典的包，例如numpy(已解決[^19])。

絕大部分的大公司，用java處理大數據不管是環境也好，積累也好，都會好很多。

Python處理數據的優勢（不是處理大數據）：

異常快捷的開發速度，代碼量巨少

豐富的數據處理包，不管正則[^20]也好，html解析啦，xml解析啦，用起來非常方便

內部類型使用成本巨低，不需要額外怎麼操作（java，c++用個map都很費勁）

公司中，很大量的數據處理工作工作是不需要面對非常大的數據的

巨大的數據不是語言所能解決的，需要處理數據的框架（hadoop[^21]，
mpi[^22]...）雖然小眾，但是python還是有處理大數據的框架的，或者一些框架也支持python

編碼問題處理起來太太太方便了

綜上所述：

python可以處理大數據

python處理大數據不一定是最優的選擇

python和其他語言（公司主推的方式）並行使用是非常不錯的選擇

> 因為開發速度，你如果經常處理數據，而且喜歡linux終端，而且經常處理不大的數據（100m以下），最好還是學一下python。

### Web程式

Python經常被用於Web開發。譬如，通過mod_wsgi[^23]模組，Apache可以運行用Python編寫的Web程式。使用Python語言編寫的Gunicorn作為Web伺服器，也能夠執行Python語言編寫的Web程式。Python定義了WSGI標準應用介面來協調Http伺服器與基於Python的Web程式之間的溝通。一些Web框架，如Django[^24]、Pyramid、TurboGears、Tornado、web2py、Zope、Flask等，可以讓程式設計師輕鬆地開發和管理複雜的Web程式。

Python對於各種網路協定的支援很完善，因此經常被用於編寫伺服器軟體、網路蠕蟲[^25]。第三方函式庫Twisted支援非同步線上編寫程式和多數標準的網路協定（包含用戶端和伺服器），並且提供了多種工具，被廣泛用於編寫高效能的伺服器軟體。另有gevent這個流行的第三方函式庫，同樣能夠支援高效能高並行的網路開發。

Python也被應用在自動讀取環保單位網站逐時發布的空氣品質數據，如法國的firapria[^26]。

GUI開發

Python本身包含的Tkinter庫能夠支援簡單的GUI開發。但是越來越多的Python程式設計師選擇wxPython或者PyQt等GUI套件來開發跨平台的桌面軟體。使用它們開發的桌面軟體執行速度快，與用戶的桌面環境相契合。通過PyInstaller還能將程式釋出為獨立的安裝程式包。

### 作業系統(Operation System)

在很多作業系統[^27]裡，Python是標準的系統元件。大多數Linux發行版和Mac OS
X都整合了Python，可以在終端機下直接執行Python。

有一些Linux發行版的安裝器使用Python語言編寫，比如Ubuntu的Ubiquity安裝器、Red
Hat
Linux和Fedora的Anaconda安裝器。在RPM系列Linux發行版中，有一些系統元件就是用Python編寫的。Gentoo
Linux使用Python來編寫它的Portage軟體包管理系統。Python標準庫包含了多個調用作業系統功能的函式庫。

通過pywin32這個第三方軟體包，Python能夠存取Windows的COM服務及其它Windows
API。使用IronPython，Python程式能夠直接調用.Net Framework。

OLPC[^28]的作業系統Sugar項目的大多數軟體都是使用Python編寫。

### 其他

NumPy、SciPy、Matplotlib可以讓Python程式設計師編寫科學計算程式。有些公司會使用SCons[^29]代替make構建C++程式。

很多遊戲使用C++編寫圖形顯示等高效能模組，而使用Python或者Lua編寫遊戲的邏輯、伺服器。相較於Python，Lua的功能更簡單、體積更小；而Python則支援更多的特性和資料類型。很多遊戲，如EVE
Online使用Python來處理遊戲中繁多的邏輯。

YouTube、Google、Yahoo!、NASA都在內部大量地使用Python。

### 語言選擇的思考

Java在網頁、電玩與行動APP方面有其強處，環境方面如常用的VERDI圖形顯示系統，就是出自java程式語言的應用，但在科學與工程方面需要大量數值計算與平行處理時，並沒有java發揮的空間。

以下就程式語言在環境方面的應用進行比較，說明各項語言的強處與弱點。除了python之外，比較對象為fortran[^30]。

#### Python 與fortran的差異比較

+----------------+----------------+----------------+----------------+
| 比較項目       | fortran        | python         | 說明           |
+----------------+----------------+----------------+----------------+
| 直譯/編譯      | >              | > 直譯、       | > 前者適合修改 |
|                | 編譯後才能執行 | 執行檔須另包裝 | 較少的大程式。 |
|                |                |                | >              |
|                |                |                | > 後者適合需   |
|                |                |                | 修改的小程式。 |
+----------------+----------------+----------------+----------------+
| 偵錯方式       | > debuggers    | > ipython      |                |
+----------------+----------------+----------------+----------------+
| 計算效率       | 強             | 中             | > 以數值       |
|                |                |                | 計算為主的模式 |
| 多工計算       |                |                | 主程式，仍以f  |
|                |                |                | ortran為主流。 |
| 分散計算       |                |                | 包括大氣、地質 |
|                |                |                | 、海洋、流力等 |
|                |                |                | >              |
|                |                |                | > Python則經常 |
|                |                |                | 應用在多工分散 |
|                |                |                | 處理之大數據分 |
|                |                |                | 析、資料庫分析 |
+----------------+----------------+----------------+----------------+
| 開放源         | 是             | 是             | > Fortran計    |
|                |                |                | 算能力強的編譯 |
|                |                |                | 軟體是須付費的 |
+----------------+----------------+----------------+----------------+
| 程式可讀性     | 強             | 中             | > Frotr        |
|                |                |                | an的格式化區塊 |
|                |                |                | 有利閱讀，GOTO |
|                |                |                | 仍是弱點。Pyth |
|                |                |                | on無GOTO功能。 |
+----------------+----------------+----------------+----------------+
| 大眾化與普及性 | 低             | 高             | > Python       |
|                |                |                | 已列入中學教材 |
|                |                |                | 。Fortran僅限  |
|                |                |                | 少數應數系課程 |
+----------------+----------------+----------------+----------------+
| 跨平台模組化   | 弱             | 強             | > Fortr        |
|                |                |                | an的函式庫大多 |
| 第三方函式庫   |                |                | 須付費，且無開 |
|                |                |                | 放源。資訊人員 |
|                |                |                | 支援度較低。Py |
|                |                |                | thon第三方平台 |
|                |                |                | 非常活躍，資訊 |
|                |                |                | 人員支援強大。 |
+----------------+----------------+----------------+----------------+
| 圖形處理       | 中             | 強             | > Fortran的    |
|                |                |                | 圖形套裝軟體經 |
|                |                |                | 常索費不貲。Py |
|                |                |                | thon可以銜接第 |
|                |                |                | 三方開放源程式 |
+----------------+----------------+----------------+----------------+
| 前             | 弱             | 強             | > Fortran模    |
| 後處理之整合性 |                |                | 式一般以「系統 |
|                |                |                | 」方式推出，py |
|                |                |                | thon則以模組化 |
|                |                |                | 積木方式提供。 |
+----------------+----------------+----------------+----------------+
| GIS 計算       | > 無           | > 有           | > 直           |
|                |                |                | 接在GIS環境進  |
|                |                |                | 行資料庫的計算 |
+----------------+----------------+----------------+----------------+
| 網路通訊、協定 | > 無           | > 有           | > 直接在網     |
|                |                |                | 站環境進行工作 |
+----------------+----------------+----------------+----------------+
| Excel/tiff     | > 無           | > 有           | > 直接存取常用 |
| 讀寫           |                |                | 資料庫與圖形檔 |
+----------------+----------------+----------------+----------------+
| netCDF讀寫     | > 有           | > 有           | > 地           |
|                |                |                | 球科學常用格式 |
+----------------+----------------+----------------+----------------+

1.  常用的網站

Python的特色之一就是「積木化」，因此何處可以找到適合的程式元件，其應用範例等，就非常重要，除了谷哥搜尋「python,
keyword」之外，也可以由下列網站開始，會更直接一些。

官方網站

Applications for Python[^31]

Python的官方介紹，將應用歸納成網頁與網際網路方面、科學與數學資料庫方面、教育方面、桌面GUI發展、軟體系統發展等等。

[[SciPy]{.underline}](https://www.scipy.org/):

做為一個高階的程式語言，同時要達到廣泛應用與深度簡潔，唯一的發展路徑就是走開源的道路，這是SciPy社群的基本理念，多年來在科學計算方面，SciPy社群已經完成了多項核心程式與程式庫，前者包括python及ipython，後者則包括NumPy(數值計算)、SciPy(訊號處理、最佳化、統計)、matplotlib(繪圖)、Pandas(資料庫軟體)、SymPy(符號數學與代數)等等。

這些基本的程式庫之上，社群的程式設計師持續不斷發展各項專案，以使python的應用有今天蓬勃的局面。

## 第三方程式庫

[[PyPI]{.underline}](https://pypi.python.org/pypi)(the Python Package
Index)[^32]

除了前述主要應用的介紹之外，
python官方也負責維護一個開放社群的網站，收集了各式各樣第三方提供的python程式庫及開源程式碼，數目將近10萬筆，供自由免費安裝或下載。可以在PyPI主頁上方鍵入關鍵字詞，再逐一檢討測試是否合乎需求，就可以找到優秀又合用的程式。

若想要成為PyPI的作者群之一，將自己寫的程式提供出來，需要登錄並按照指示撰寫程式說明或範例。

GitHub:

GitHub是目前全球最大的程式設計者社群網站，也是最活躍的專案發展平台。在其主頁上方Search
GitHub鍵入關鍵字詞，就可以找到很多意想不到的好物，包括各式各樣的程式語言，其中可以發現Python確實是受到歡迎的選項。

## 入門網站

中文入門網站可以參考「[[台灣使用者群組]{.underline}](http://wiki.python.org.tw/Pot)」，[[django
girl Python
入門]{.underline}](http://djangogirlstaipei.herokuapp.com/tutorials/python/?os=windows)，[[十分鐘上手]{.underline}](http://geniustom.noip.me/wordpress/?p=254)、以及[[codedata]{.underline}](http://www.codedata.com.tw/category/python/)公司網站。

### Python的安裝與基本作業方式

分為本地(個人電腦)及遠端(工作站)兩種工作方式分別說明如下：

本地工作方式

Windows系統安裝

在Windows系統安裝python可以參考[[網友]{.underline}](https://www.foolegg.com/how-to-build-a-python-programming-environment-on-windows/)[^33]的介紹。簡單來說，就是去到python的官方網站，選擇正確的版本、以及機器的規格(32/64位元電腦)，下載安裝檔後，即可照一般軟體安裝方式進行[^34]。假設將軟體安裝到$PATH_PYTHON2.7目錄。

安裝後，開啟對話窗，cd到$PATH_PYTHON2.7\\Scrpits下，用pip
安裝ipython、jupyter等等程式。如pip install *[jupyter]{.underline}*。

如果系統沒有C++，安裝程式會停下來，要求到ms
Window官方網站(http://aka.ms/vcpython27)下載python2.7編譯要用的C++，同樣的下載後照一般軟體安裝方式安裝即可。補足C++後即可繼續pip了。

Python對話窗>>>

下載安裝後由開始→在「搜尋程式及檔案」對話窗鍵入"python"→即會開始python的制式對話窗。在>>>之提示下鍵入help()指令即可詢問要執行的作業，import
os後執行os.chdir(path)可以換目錄到path。quit()即可跳出。

## ipython 對話窗 [*]

同上述啟動的方式，!CMD可以執行shell指令(CMD的內容視shell是DOS或者是unix而異)，run
test.py可執行test.py程式不必跳出ipython程式，history可以將過去的指令顯示出來，另外存成.py檔案。離開程式用exit或quit指令。

由於windows的**命令提示字元**選取、複製、貼上等功能要將滑鼠移到視窗頂端按右鍵下拉選單操作，應用上會很不方便。若要能複製ipython的指令，最好要有putty(詳下述)或其他shell程式才容易操作。

## jupyter-notebook

### notebook的啟動

由於jupyter必須使用到網路瀏覽器，要先開啟IE或firefox等本地電腦既設的網路瀏覽器。而且在jupyter-notebook環境無法變換到別的目錄，因此必須先開啟**命令提示字元**，cd到工作目錄(如/cygdrive/c/Users/4139/MyPrograms/python2.7/py_homework/ISCST)，設定路徑到path
$PATH_PYTHON2.7/Scripts;及$PATH_PYTHON2.7/python2.7/Lib目錄;再啟動jupyter-notebook程式。

NT系統架構下第一次使用IE，jupyter會要求輸入密碼(token)，在網站位置處鍵入[[http://localhost:8888]{.underline}](http://localhost:8888)後，回到jupyter的輸出畫面
(如[[http://localhost:8888/?token]{.underline}](http://localhost:8888/?token)=
**[ccd0d08978b55731dabd2b435a605e55fed245ce19d5aad)]{.underline}**在密碼處貼上token即可登入。

瀏覽器上的作業方式

其餘作業方式就與一般的網頁，以及前述的ipython沒有太大的差異(!可執行DOS指令)。

開始(新增)python工作：在右上方New處按下拉，選擇Python
2新增對話窗，除了執行方式以外，完全與ipython相同。

執行：在ipython內，Enter鍵就是直接執行，在jupyter環境，Enter鍵是程式編輯過程的換行。要執行可以直接按命令列Run
cell(play botton)。也可以由上方Cell下拉選擇Run Cells。

命名：預設是Untitle，點擊後可以在Rename Notebook框內給定(或修改)名字。

儲存：按命令列最左邊的磁碟片，工作會以附加檔名.ipynb存檔，無法更改目錄，只能儲存於目前所在的工作目錄。

關閉正在執行的工作：可以由Home的Running分頁，選擇工作，予以shutdown。

關閉home之後，回到cmd視窗後，必須要按Ctrl-C才能停止jupyter。

jupyter的強項

網路瀏覽器上可以方便選取、複製、貼上，對程式編寫較為方便。

可以直接用滾輪就能找到指令的歷史，完整留下執行過程。

網路瀏覽器亦能執行python顯示圖形或數據表格，直接在畫面顯示，可以對程式結果直接予以回饋。

一般網友也認為jupyter是最佳的作業環境。

Cygwin系統

Cygwin是windows系統上完整的unix系統(並不是模擬介面)，完整建置可能會需要20
G的磁碟機容量，是非常完整、持續精進、完全開源的unix作業環境，然而Python與cygwin的相容性尚不如window版本，ipython與jupyter不如前述版本。

下載與安裝可以參考[[cygwin]{.underline}](https://www.cygwin.com/)的官方網站，按照32與64位元不同，有個別的安裝程式，安裝時要記得點選python程式，再安裝pip程式。有了pip之後，任何python程式都很容易安裝了。

Cygwin的作業環境可以只利用其內設的cygwin-terminal，或者啟動/usr/sbin/sshd之後，以putty登入，作業方式與效果跟登入遠端主機是一樣的。

## 遠端工作站執行方式

工作站的優勢不單只是在硬體上，在軟體上亦比一般個人電腦更為強大，在早期個人電腦資源尚不充分的時代，工作站上分享軟硬體資源有其必要性。

今天雖然個人電腦已經很強大，但是因為python或其他大多數程式的應用機會，其實並不是非常頻繁，因此使用工作站也可以省去安裝程式的困擾。

由於不論是python直譯器或者是ipython都是「命令-控制」(command and
control)方式的傳統作業模式，主要都是在一個對話窗內進行，與目前常見的視窗系統(window)「看見-取得」(what
you see what you
get)方式，有很大的不同。因此在本地電腦與遠端電腦上執行，並沒有太大的差異。

此外工作站不但可以供使用者從內部網入，也可以提供從外部登入(telnet)的功能，這點開放使用者不必親赴工作站所在的電腦中心，只要透過網際網路，一樣可以在家上機、在任何地方利用手機、平板上網，即可遠端監控工作的進行。

遠端作業會需要2個介面，一個是命令列介面，一個是檔案交換的介面，此處介紹常見的putty與filezilla等2支程式。均是免費的程式。Cygwin-terminal的功能類似putty，也可以直接在終端機ssh
或sftp，但其實用性不如putty，並不推薦使用。

近年來有國人自行開發的MobaXterm程式，屬於付費升級之公開程式，同時亦有X
window，又延續putty的功能，雖然佔據記憶體較大，但也有其適用性。

Putty

簡介

Putty可以從[[官方網站]{.underline}](http://www.putty.org/)下載，解壓縮後即可使用，不需安裝，只要放在桌面、window開始畫面或者命令列，容易找到即可。Putty的介紹可以詳見[[wiki]{.underline}](https://zh.wikipedia.org/wiki/PuTTY)的說明，使用說明可以參考中研院教學網站[^35]。

使用putty進行遠端登錄先要確定遠端電腦已經開放可以ssh (secure
shell)登入，有正確的帳號、密碼、以及遠端電腦的ip，每個步驟與資訊缺一不可。

Putty登入遠端工作站之後，隨即開始unix-like
的shell作業系統，視窗類似ms-Windows之DOS視窗，然而其功能較更加靈活好用，其特色說明如下：

外表的設定

外表Appreance(字型、顏色、背景、游標等)的設定，在視窗頭按右鍵下拉選單內，不只提供使用者容易觀看的環境，最重要的功能，在於提供作為特定工作站的辨識，避免同時開啟多個工作站視窗，會造成混淆。

辨認工作站除了在命令列出現hostname之外，也可以由df指令，看到工作站的檔案系統。當然，如果介面的外觀顏色有顯著差異，是最容易辨識的。

經過測試結果，具有較高分辨率的色彩搭配，以黑底淺色字較高，包括白色(淺灰)、淺黃、亮綠、橙色等，都是較好的選擇。亮底(淺灰色)的搭配，除了黑色字之外，也可以考慮深藍色。

這些設定的改變，可以和連線訊息一起存在特定工作站設定中，不必每次再設定。

視窗文字之處理

putty視窗出現的文字內容，經由滑鼠滾輪或捲軸來翻閱。

也可以存在剪貼簿(在視窗頭按右鍵Copy All to
clipboard)，貼在其他軟體(如notepad或wordpad等簡易文字編輯軟體)，以便進一步偵錯或存檔。

Putty並不符合ms-window一般軟體選取複製貼上之按鍵規則，
ctrl-C是中止程式而不是選取、ctrl-V、ctrl-X也不會有作用。ctrl-Z也會中止程式(而不會恢復上一動)，ctrl-S暫時終端機作業(而不是存檔)，ctrl-Q則為繼續。這些ctrl-按鍵是符合unix作業系統的設定，要小心使用。

按左鍵反白(選取)後之文字，按右鍵之後，即會出現在命令列(貼上，亦可用Shift-Insert也會有相同的效果)，可以作為指令的部分內容。

鍵盤控制

方向鍵：ms-Windows之DOS視窗介面按向上鍵↑會出現前一次的指令，這個功能在大多數的終端機模擬程式都會有，也包括putty。

F8鍵：然而按F8出現前次指令，或按第一個字元再按F8會出現開頭是該字元的前次指令，這些在pytty是沒有的。

Tab鍵：在DOS或者unix作業系統，Tab鍵具有補滿檔名(或目錄名稱)的功能，甚至出現選項提示。這項功能可以減省打字錯誤的發生機會，可以多加利用。差異在於目錄名稱，前者不會出現分隔線"\"，後者會出現分隔線"/"。

filezilla

為類似檔案總管的互動式程式[^36]。已有非常多的中文介紹。

主機(H)：輸入IP位址，如Sino4: 59.124.9.104 (hinet IP, username:cybee,
passwd:cybee123)或localhost: 200.200.121.71
(LAN)或[ftp.sinotech.com.tw]{.underline}輸入SECLTD\\員工編號及登入密碼。

使用者名稱(U)及密碼(W) ：輸入user name與password

連接埠(P)：輸入22(sftp協定)或21(ftp協定)，視server開啟的服務項目而定(sino4開放sftp、[ftp.sinotech.com.tw]{.underline}則為ftp)。

輸入此4者後，以後下次登入可以按下「重新連線到先前的伺服器」即可。

系統預設右方視窗為遠方目錄樹，左方為本地檔案目錄。找到檔案按滑鼠右鍵即可選擇下載或上傳。

注意：

與ftp相同，要注意傳輸檔案的格式，可以在「傳輸(T)」→「傳輸型態(T)」中選取。

Filezilla不論在遠端與本地都有開新目錄、更名、刪除的功能，雖然沒有複製的功能，但是經過下載再上載到特定目錄去，也可以執行類似複製的動作。可以當成遠端的檔案總管來使用。

MobaXterm

MobaXterm雖然是商業軟體，但也提供個人使用的基本功能讓使用者測試並熟悉，以供商業使用採購的參考。一般而言，MobaXterm的X
Window算是蠻穩定的，也同時擁有putty、sftp(filezilla)等功能，只是耗費記憶體較putty多很多，如果沒有圖形顯示的需求，建議還是避免使用。有關MobaXterm的說明與下載安裝可以參考官網[^37]。

與putty一樣，在連線之前必須先定義session，如圖依序點選，輸入遠端的ip和username，記得要勾選X11的功能，這樣本機才可以當成遠端顯示輸出的設備。Session的名稱可以在bookmark
Setting頁面定義，如果沒有，內設是ip(username)，也可以在左欄出現後滑鼠右鍵rename
session更改名稱。

左欄session頁面出現bookmark之後就可以點選，如果曾經儲存過密碼，MobaXterm不會再問，出現畫面如圖所示，要檢視X11
forewarding和DISPLAY都已經打勾，或者在遠端以xclock&指令(&表示在背景執行命令)，測試會不會在本機出現如圖的小時鐘。

測試python的繪圖功能，可以進ipython之後，執行下列程式，就會出現另一圖形視窗，將輸出顯示在本機電腦螢幕上。


```python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000',
periods=1000))
ts = ts.cumsum()
ts.plot()
plt.show()
```
![](media/image1.png){width="4.72in" height="3.776000656167979in"}

![](media/image2.png){width="4.72in" height="3.776000656167979in"}

左欄除了ssh的session之外，也有類似檔案總管可以瀏覽的sftp，可以「用本機程式」開啟，類似網路磁碟機的功能，不必再另外以檔案總管連結網路磁碟機。

teamviewer

teamviewer[^38]是一個商業軟體，經常用在遠端偵錯服務、遠距或廣播教學、線上會議等用途，經由隨機且每次變更的密碼協定，可以安全又有效的進行遠端監控與檔案傳輸。teamviewer提供免費版給一般會員使用，如果要增加連線對象，必須成為付費會員。

類似ssh的服務方式，遠端必須先啟動teamviewer程式，將其機器編碼(9碼固定數字)與密碼(4碼隨機產生數字)提供給客戶端，客戶端再啟動程式，選擇該項機器設備編碼(可以預設)，按下「與夥伴連線」會出現密碼無效云云(不必理會)，在密碼對話框內輸入4碼數字之後，會在客戶本地電腦出現新的視窗，即為遠端電腦當時的畫面。

  ---------------------------------------------------------------------------------- --------------------------------------------------------------------------------
  ![](media/image3.png){width="2.8075153105861768in" height="2.080449475065617in"}   ![](media/image4.png){width="2.753284120734908in" height="1.49080271216098in"}
  輸入該項機器設備編碼(可以預設下拉)，按下「與夥伴連線」                             對話框內輸入4碼數字後按「登入」
  ---------------------------------------------------------------------------------- --------------------------------------------------------------------------------

注意事項：

登記成為會員可以不必輸入機器編碼與密碼而直接連線。

由於遠端電腦畫面縮小成為本地的一個視窗，因此其解析度會降低。因此本地電腦的解析度要更高，才能看清楚遠端電腦的畫面。

進入teamview遠端視窗，滑鼠動做會比較不敏感，動作必須要慢一些。

習慣用Alt-Tab來切換視窗的使用者要注意，teamviewer會不知道是要在本地還是在遠端切換視窗，teamviewer會需要確認使用者的意圖為何。

遠端與客戶端同時都可以控制遠端電腦設備。

如果任何人關閉遠端的teamviewer程式，所有的連線隨即中斷，必須由遠端重啟程式才能再次登入。

畫面上方工具列有「檔案與其他」下拉後有「開啟檔案傳輸」，就出現類似filezilla左右視窗的傳輸介面，用法也類似Filezilla但是滑鼠右鍵無效，要按畫面上\<\<或>>來傳送檔案。

習題

網友[^39]用python語言撰寫了大氣煙流模式，試由GitHub網站[^40]下載，用jupyter-notebook來執行。

程式語言與重要程式庫之應用

程式是數據處理的核心，要處理真實世界的專案，還是必須有檔案的輸入與輸出，這在第3章中會進一步說明，這一章集中在python程式語言與程式庫的應用。

程式基本的格式與標記

由於python是一個高度模組化的程式語言，因此必須在層次架構上十分清處，就層次架構，利用工具來尋找需要的元件「積木」，自然很快就可以很簡潔的完成工作，否則以一己之力要完成大小模組與工具，恐怕會事倍工半。

容器、迴圈與判斷

程式基本學習可以參考第1章介紹的中文網站，或者直接上英文官方網站[^41]，可以避免翻譯造成的誤解，以下是重要名詞的中英文對照與意義。

+------------------------+------------------+------------------------+
| 英文                   | 中文             | 意義                   |
+------------------------+------------------+------------------------+
| Python                 |                  |                        |
| 支援的容               |                  |                        |
| 器（Container）型態有  |                  |                        |
| list、set、dict、tuple |                  |                        |
| 等                     |                  |                        |
+------------------------+------------------+------------------------+
| string                 | 字串、字符串     | String                 |
|                        |                  | 的本意是細的繩         |
|                        |                  | 索，何以會成為文字，可 |
|                        |                  | 能與它排序的性質有關。 |
|                        |                  |                        |
|                        |                  | 字串是python           |
|                        |                  | 的預設形態，一個變數若 |
|                        |                  | 沒有特別宣告，它會是一 |
|                        |                  | 個字串，如果輸入的數字 |
|                        |                  | ，需要以**int()**或**f |
|                        |                  | loat()**改變它的屬性。 |
+------------------------+------------------+------------------------+
| list                   | 陣列、序列、串列 | 觀念有                 |
|                        |                  | 點像傳統具有維度的陣列 |
| [1,2,3,'a']          |                  | ，但是在陣列大小、維度 |
|                        |                  | 尺度、順序、乃至於內容 |
|                        |                  | 屬性等的靈活度要更高。 |
|                        |                  |                        |
|                        |                  | 陣列和字串的操作有     |
|                        |                  | 很多是沿用相同的方式。 |
+------------------------+------------------+------------------------+
| [...]                | 中括弧           | 將其內的物件定義為list |
|                        |                  |                        |
|                        |                  | 指定list               |
|                        |                  | 或string某個順序的內容 |
+------------------------+------------------+------------------------+
| array                  | 陣列、矩陣       | 除了具有前述list的特性 |
|                        |                  | 之外，array是numpy的一 |
| array(1,2,3)           |                  | 個函數，是數字的組合， |
|                        |                  | 不能是其他性質的物件。 |
|                        |                  | Matrix特別指2維的array |
|                        |                  |                        |
|                        |                  | 數字list和             |
|                        |                  | array的差異詳下述說明  |
+------------------------+------------------+------------------------+
| tuple                  | 元組             | 這個字是源自於音樂術   |
|                        |                  | 語tuplet，意思是很快的 |
| (1,2,3,'a')            |                  | 連音，強調它的不可分割 |
|                        |                  | 特性，所以中文很難翻譯 |
|                        |                  | ，特別給它一個「組」字 |
|                        |                  | 。Tuple的靈活度很低。  |
+------------------------+------------------+------------------------+
| (...)                  | 括弧             | (                      |
|                        |                  | )在python中可          |
|                        |                  | 以是函數的呼叫介面，也 |
|                        |                  | 可以是tuple的範圍定義  |
+------------------------+------------------+------------------------+
| set                    | 集合             | 傳統語                 |
|                        |                  | 言沒有集合的運作方式， |
| {1,2,3,'a'}            |                  | 集合可以做聯集、交集、 |
|                        |                  | 補集、空集等邏輯運作。 |
|                        |                  | 非常靈活，較傳統的陣列 |
|                        |                  | 而言有非常強大的功能。 |
|                        |                  |                        |
|                        |                  | 集合內                 |
|                        |                  | 的元素是**沒有**順序的 |
|                        |                  | ，因此也**不能重複**。 |
+------------------------+------------------+------------------------+
| dict                   | 字典             | **                     |
|                        |                  | key**與**value**對照組 |
| passwords =            |                  | 的集合，用**:**隔開。  |
| {'Justin' : 123456,  |                  |                        |
| \                      |                  |                        |
| 'caterpillar':933933} |                  |                        |
+------------------------+------------------+------------------------+
| DataFrame              | 數據結構、數據集 | Pandas程式庫           |
|                        |                  | 定義的資料表，各欄之間 |
|                        |                  | 沒有順序，列則有順序。 |
+------------------------+------------------+------------------------+
| for ... in ...:**    | 迴圈             | 迴圈執行條件與執行內容 |
|                        |                  | 之間，必須有一個冒號(  |
| **while...:**          |                  | :)隔開。Python的迴圈用 |
|                        |                  | indent(Tab或2/4個空格) |
| **with ...:**          |                  | 控制範圍與層次，因此不 |
|                        |                  | 需要enddo或continue。  |
|                        |                  |                        |
|                        |                  | Python沒有goto指令     |
|                        |                  | 。有**break**與**cont  |
|                        |                  | inue**跳出或繼續執行。 |
|                        |                  |                        |
|                        |                  | for...in..           |
|                        |                  | **.→執行該範圍內的指標 |
|                        |                  |                        |
|                        |                  | **while**              |
|                        |                  | (條                    |
|                        |                  | 件)→條件狀況下重複執行 |
|                        |                  |                        |
|                        |                  | **with**               |
|                        |                  | (動作)→該動作          |
|                        |                  | 成功狀況下重複執行內容 |
+------------------------+------------------+------------------------+
| **if ... :**           | 判斷             | 同樣以冒               |
|                        |                  | 號(:)隔開條件與內容。  |
| **try:\...except:\..   |                  |                        |
| .else:...finally:...** |                  | 相等(**==**)、         |
|                        |                  | 不等(**!=**)、大於(**\ |
|                        |                  | >**)、小於(**\<**)、且 |
|                        |                  | (**and**)、或(**or**)  |
+------------------------+------------------+------------------------+
| **def ... :**          | 副程式           | 用**()**當             |
|                        |                  | 做呼叫的介面，**return |
| **return ...**         |                  | **之後的結果將會被傳回 |
+------------------------+------------------+------------------------+
| **_**singl            | -   前底線       | 內部使用的副程式，     |
| e_leading_underscore |                  | 不能被**import**或呼叫 |
|                        | -   後底線       |                        |
| single_trai           |                  | -   與python           |
| ling_underscore**_** | -   前雙底線     | 命名有重複之虞時辨識用 |
|                        |                  |                        |
| **__**doubl          | -   前後雙底線   | -                      |
| e_leading_underscore |                  |   在類別內命名使用，該 |
|                        |                  | 名稱會跟在類別名稱之後 |
| **__**double         |                  |                        |
| _leading_and_traili |                  | -   在使用者控         |
| ng_underscore**__** |                  | 制之命名空間出現的名稱 |
+------------------------+------------------+------------------------+

數字序列(numerical list)和陣列(numpy array)的異同

加法：

2個(以上)序列相加是串聯、依序延長，join或者是concatenate，因此沒有必要內容或長度。因此序列不能相減，要去掉某個元素，必須用**remove**，或者是**del**指令(array
不適用)。序列適用append指令，array則否。


```python
In [148]: [1,2,3]+[4,5,6]
Out[148]: [1, 2, 3, 4, 5, 6]

In [149]: [1,2,3]+[4,5,6,7]
Out[149]: [1, 2, 3, 4, 5, 6, 7]

In [151]: a=[1,2,3]

In [152]: del a[2]

In [153]: a
Out[153]: [1, 2]

In [154]: a.remove(2)

In [155]: a
Out[155]: [1]
```

而陣列基本上是數學領域所定義向量，向量可以加減，但維度必須要完全一致，四則運算都是逐項進行的(itemwise)。

In [164]: a=np.array([1,2,3])

In [165]: b=np.array([4,5,6])

In [166]: c=a+b

In [167]: print c

[5 7 9]

乘法

因為序列是一個容器，可以乘上整數做重複。如範例做3重複：

In [168]: a=[1,2,3]

In [169]: b=3*a

In [170]: b

Out[170]: [1, 2, 3, 1, 2, 3, 1, 2, 3]

顯然序列沒有除法或其他的操作元，也不能將2序列相乘除。

陣列是向量，因此適用所有的計算元，如：

In [174]: a=np.array([1,2,3])

In [175]: b=np.array([4,5,6])

IIn [178]: print a*b

[ 4 10 18]

In [182]: print a**b

[ 1 32 729]

產生、修改、與其他操作

list的產生方式可以直接以**[...]**指定內容、相加、**append**、或者將其他容器轉成序列(**list(...)**指令)，如果是整數，可以用**range**指令，如

In [191]: b=range(5)

In [192]: b

Out[192]: [0, 1, 2, 3, 4]

陣列的**range**也類似，但指令是**np.arange(...)**。陣列雖然不能**append**或**concatenate**，必須一次定義其長度。如果要變更就必須轉成序列，使用序列的指令處理後，再將序列轉回成陣列(**np.array()**)：

In [195]: b=np.arange(5)

In [196]: b

Out[196]: array([0, 1, 2, 3, 4])

In [197]: b=np.zeros(shape=(10))

In [198]: b

Out[198]: array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])

In [199]: for i in xrange(len(b)):

\...: b[i]=i

\...: print b

[0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]

多維度序列的降階(flatten)，可以用**sum( list_of_lists,[])**指令：

In [204]: b

Out[204]: [[4, 10, 18], [4, 10, 18]]

In [205]: sum(b,[])

Out[205]: [4, 10, 18, 4, 10, 18]

Or...


```python
import itertools
flattened_list = list(itertools.chain(*list_of_lists))
```

判斷式

序列和陣列都可以適用判斷式，但是效果有所差異，

單一命令列迴圈之順序

基本邏輯

固然用分行與對齊(line and indent)方式，來撰寫樹枝狀的迴圈，比較容易解讀，然而會佔據太多的程式碼空間而顯得的累贅，此時，可以考慮以單行方式來撰寫迴圈，只要注意迴圈的順序。

下例將會寫出i,j的tuple，可以發現當寫成單行迴圈時，最後段落(右側)的迴圈將優先執行，為分行對齊方式之最內迴圈，可以看成原本寫成2行的迴圈，連成(join)一行來撰寫。

```python
In [289]: [(i,j) for i in xrange(5) for j in xrange(5)]
Out[289]:

[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
(1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
(2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
(3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]

In [290]: for i in xrange(5):
\...: for j in xrange(5):

\...: print (i,j)

\...:

(0, 0)
(0, 1)
(0, 2)
(0, 3)
(0, 4)
...

(4, 4)
```
此一習慣與fortran相反，fortran在讀寫時允許將迴圈寫在同一行，然是靠左側的迴圈優先執行。此外，python可在for之後可以加入if來做篩選，只執行特定條件的迴圈項目。

範例一：最近距離之臨海鄉鎮代碼(無方括號迴圈)

將此一邏輯作法推廣到實際案例中，如以下案例：

```python
kuang@master /home/camxruns/2018/emis/8760wt/area
$ vim SeaSuamiv2.py
for j in xrange(nrow*dx):
	for i in xrange(ncol*dx):
		if a[j,i]!=5300.:continue
		ss=[s for s in sea_side** if int(s/100) in [cnty[ic] for ic in
nearest3(i,j,ijM_cnty)]**]

ijSS={ij:**s for s in ss if len(ij_cnty2[sea_side.index(s)])>0 \\

for ij in ij_cnty2[sea_side.index(s)]}
b[j,i]=list(ijSS.values())[nearest3(i,j,ijSS)[0]]
```
上例由海邊鄉鎮代碼中找到距離海面(i,j)之最近距離者，記錄在b[j,i]陣列中，由於海邊鄉鎮有100個，每個鄉鎮又有約10數點是臨海的，如此迴圈將會太多，因此要先由其中挑選最近的3個縣市，只針對此3個縣市的海邊鄉鎮進行試誤，會大大降低迴圈次數。

其中紅字部分是最外圈迴路，要先定義**s**，否則後面的判斷式以及最內迴圈中的**sea_side.index(s)**都使用到**s**，卻不知道**s**是什麼？

本例中亦使用了字典來做(i,j)與鄉鎮代碼的連結，雖然也可以使用DataFrame來完成，然而因為迴圈太多次了，如果呼叫pandas程式會太慢，定義太多的序列又嫌繁瑣，最好就是用dict對照，可以快速更換內容，閱讀上也較為容易。

範例二：夜間平均排放量(方括號迴圈)

方括號容器內如果裝的是數字或符號，那就是一個序列的符號，如果裝的是可以執行的動作，那python就會重複執行指定的動作。前者會進一步說明，後者如：

[text_file.write(str(i)+'\\n') for i in SomeThingIterable]

這樣就可以只用單行指令就將SomeThingIterable依序一行一行的寫進text_file內。

在同個方括號的巢狀迴圈的簡單範例如下，python會先執行**最後**index的迴圈：

In [2]: [i+j for i in xrange(3) for j in xrange(0,31,10)]

Out[2]: [0, 10, 20, 30, 1, 11, 21, 31, 2, 12, 22, 32]

序列i,j各執行3次，共有9項，這9項的排列順序(i,j)是[(1,1), (1,2), (1,3),
(2,1), (2,2), (2,3), (3,1), (3,2),
(3,3)]。這是同一方括號不同指標的順序。如果多個方括號，當然就從最內圈的方括號來執行。

以下的範例也是用重複單行命令列，來形成一個字串和陣列的字典，在陣列的定義上，應用了條件及多個方括號巢狀的迴圈架構。

kuang@master /home/camxruns/2017/emis

$ vim modNVOsea_daily.py

...

night=[i for i in xrange(nt[D]) if (i+20)%24\<=5 or (i+20)%24>=18]

par_night={D:np.array([[np.mean([cas_fil[D].variables['PAR']**[it,0,j,i]
for it in night])

for i in xrange(ncol[D])] for j in xrange(nrow[D])]) for D in
domains}

範例中的主要變數是uamiv格式之5階陣列，此一格式的內容將會在後續PseudoNetCDF模組中進一步介紹，此處特別著眼在其5階的結構與順序。首先是化學成分，是一個字串'PAR'，直接指定它的值。其次是時間it，範例中給定一個範圍，並且用方括號[
]定義成序列，將重複的結果進行平均，即為夜間平均值。此平均之操作單元在最內圈，將會最先執行。

第3個維度是高度，因為是地面排放量，設為定值0。

第4\~5個維度是南北(j)、與東西方向(i)，此2個方向的迴圈也由方括號定義了，python將依照括號的順序分別先重複i再做j，所得的結果是：

In [308]: par_night['5'].shape

Out[308]: (164, 83)

如果按照fortran的作法，先異動靠左側第4個維度，再動右側第5個維度，得到的結果會是相反的，如b所示：

In [310]:
a=np.array([[np.mean([cas_fil[D].variables['PAR'][it,0,j,i]
for it in night]) for i** in xrange(ncol[D])] for j in
xrange(nrow[D])])

In [311]:
b=np.array([[np.mean([cas_fil[D].variables['PAR'][it,0,j,i]
for it in night]) for j** in xrange(nrow[D])] for i in
xrange(ncol[D])])

In [313]: a.shape

Out[313]: (164, 83)

In [314]: b.shape

Out[314]: (83, 164)

In [315]: cas_fil[D].variables['PAR'].shape

Out[315]: (720, 1, 164, 83)

整合此2範例，雖然有方括號的定義，可以對迴圈的執行順序更加明確，然而也要記住python單行命令列的迴圈順序，是右側先執行，即使是寫成巢狀方括號的形式，最內圈的結果也是形成最右側的維度，依序向左。而且在多維度的定義及轉換過程，也要注意原始變數的形狀(shape)，才不至於發生變形錯誤。

練習題：

試解讀下列程式，並利用jupyter自行測試。具有excel中的功能。

```python
import numpy as np
def avg_positive_speed(speed):
	s = np.array(speed)
	positives = s > 0
	if positives.any():
		return s[positives].mean()
	else:
		return 0.
	speed = [1., 2., 0., 3.]
	print avg_positive_speed(speed)
	# prints 2.0
	print avg_positive_speed([0., 0.])
	# prints 0.0
```

第4行`positives = s > 0`是將陣列s是否大於0的結果，指定為另一個陣列positives，是否也可以寫成`positives = [s > 0]`，或`positives = (s > 0)`?

-   np.array的用意與必要性為何？

### 字串的處理

字串可以相加('+')、替代.replace('old','new')、去尾.strip('\\n')、也可以靈活運用在資料的比對，在此基礎發展許多程式應用。

Pyton
在文字處理方面有其強大的優勢，許多讀、寫並運算文字的人工智慧程式庫可供應用。如下表所示；

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------- --------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -----------------
  **研究生:**                                                                                                                                                                **論文名稱:**                                **指導教授:**   **校院名稱:**                                                                                                                                                                                                                                                                                    **系所名稱:**                                                                                                                                                                                                                                                                                    **論文出版年:**
  [[張佑銘]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=auc=%2522%25E5%25BC%25B5%25E4%25BD%2591%25E9%258A%2598%2522.&searchmode=basic)   中文自動作文修辭評分系統設計                 李嘉晃          [[國立交通大學]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=sc=%2522%25E5%259C%258B%25E7%25AB%258B%25E4%25BA%25A4%25E9%2580%259A%25E5%25A4%25A7%25E5%25AD%25B8%2522.&searchmode=basic)                                                                       [[資訊科學系所]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=dp=%2522%25E8%25B3%2587%25E8%25A8%258A%25E7%25A7%2591%25E5%25AD%25B8%25E7%25B3%25BB%25E6%2589%2580%2522.&searchmode=basic)                                                                       2005
  [[蔡沛言]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=auc=%2522%25E8%2594%25A1%25E6%25B2%259B%25E8%25A8%2580%2522.&searchmode=basic)   自動建構中文作文評分系統：產生、篩選與評估   李嘉晃          [[國立交通大學]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=sc=%2522%25E5%259C%258B%25E7%25AB%258B%25E4%25BA%25A4%25E9%2580%259A%25E5%25A4%25A7%25E5%25AD%25B8%2522.&searchmode=basic)                                                                       [[資訊科學系所]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=dp=%2522%25E8%25B3%2587%25E8%25A8%258A%25E7%25A7%2591%25E5%25AD%25B8%25E7%25B3%25BB%25E6%2589%2580%2522.&searchmode=basic)                                                                       2005
  [[張佑銘]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=Rrno09/search?q=auc=%2522%25E5%25BC%25B5%25E4%25BD%2591%25E9%258A%2598%2522.&searchmode=basic)   中文自動作文修辭評分系統設計                 李嘉晃          [[國立交通大學]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=Rrno09/search?q=sc=%2522%25E5%259C%258B%25E7%25AB%258B%25E4%25BA%25A4%25E9%2580%259A%25E5%25A4%25A7%25E5%25AD%25B8%2522.&searchmode=basic)                                                                       [[資訊科學系所]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=Rrno09/search?q=dp=%2522%25E8%25B3%2587%25E8%25A8%258A%25E7%25A7%2591%25E5%25AD%25B8%25E7%25B3%25BB%25E6%2589%2580%2522.&searchmode=basic)                                                                       2005
  [[林信宏]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=auc=%2522%25E6%259E%2597%25E4%25BF%25A1%25E5%25AE%258F%2522.&searchmode=basic)   基於貝氏機器學習法之中文自動作文評分系統     李嘉晃          [[國立交通大學]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=sc=%2522%25E5%259C%258B%25E7%25AB%258B%25E4%25BA%25A4%25E9%2580%259A%25E5%25A4%25A7%25E5%25AD%25B8%2522.&searchmode=basic)                                                                       [[資訊科學與工程研究所]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=dp=%2522%25E8%25B3%2587%25E8%25A8%258A%25E7%25A7%2591%25E5%25AD%25B8%25E8%2588%2587%25E5%25B7%25A5%25E7%25A8%258B%25E7%25A0%2594%25E7%25A9%25B6%25E6%2589%2580%2522.&searchmode=basic)   2006
  [[粘志鵬]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=auc=%2522%25E7%25B2%2598%25E5%25BF%2597%25E9%25B5%25AC%2522.&searchmode=basic)   基於支援向量機之中文自動作文評分系統         李嘉晃          [[國立交通大學]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=sc=%2522%25E5%259C%258B%25E7%25AB%258B%25E4%25BA%25A4%25E9%2580%259A%25E5%25A4%25A7%25E5%25AD%25B8%2522.&searchmode=basic)                                                                       [[資訊科學與工程研究所]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=dp=%2522%25E8%25B3%2587%25E8%25A8%258A%25E7%25A7%2591%25E5%25AD%25B8%25E8%2588%2587%25E5%25B7%25A5%25E7%25A8%258B%25E7%25A0%2594%25E7%25A9%25B6%25E6%2589%2580%2522.&searchmode=basic)   2006
  [[陳彥宇]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=auc=%2522%25E9%2599%25B3%25E5%25BD%25A5%25E5%25AE%2587%2522.&searchmode=basic)   非監督式中文寫作自動評閱系統                 李嘉晃          [[國立交通大學]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=sc=%2522%25E5%259C%258B%25E7%25AB%258B%25E4%25BA%25A4%25E9%2580%259A%25E5%25A4%25A7%25E5%25AD%25B8%2522.&searchmode=basic)                                                                       [[網路工程研究所]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=dp=%2522%25E7%25B6%25B2%25E8%25B7%25AF%25E5%25B7%25A5%25E7%25A8%258B%25E7%25A0%2594%25E7%25A9%25B6%25E6%2589%2580%2522.&searchmode=basic)                                                      2007
  [[張道行]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=Rrno09/search?q=auc=%2522%25E5%25BC%25B5%25E9%2581%2593%25E8%25A1%258C%2522.&searchmode=basic)   中文寫作自動評閱之概念化方法                 李嘉晃          [[國立交通大學]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=Rrno09/search?q=sc=%2522%25E5%259C%258B%25E7%25AB%258B%25E4%25BA%25A4%25E9%2580%259A%25E5%25A4%25A7%25E5%25AD%25B8%2522.&searchmode=basic)                                                                       [[資訊科學與工程研究所]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=Rrno09/search?q=dp=%2522%25E8%25B3%2587%25E8%25A8%258A%25E7%25A7%2591%25E5%25AD%25B8%25E8%2588%2587%25E5%25B7%25A5%25E7%25A8%258B%25E7%25A0%2594%25E7%25A9%25B6%25E6%2589%2580%2522.&searchmode=basic)   2007
  [[葉啟祥]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=auc=%2522%25E8%2591%2589%25E5%2595%259F%25E7%25A5%25A5%2522.&searchmode=basic)   中文寫作多面向評分系統                       李嘉晃          [[國立交通大學]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=sc=%2522%25E5%259C%258B%25E7%25AB%258B%25E4%25BA%25A4%25E9%2580%259A%25E5%25A4%25A7%25E5%25AD%25B8%2522.&searchmode=basic)                                                                       [[資訊科學與工程研究所]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=5hSExj/search?q=dp=%2522%25E8%25B3%2587%25E8%25A8%258A%25E7%25A7%2591%25E5%25AD%25B8%25E8%2588%2587%25E5%25B7%25A5%25E7%25A8%258B%25E7%25A0%2594%25E7%25A9%25B6%25E6%2589%2580%2522.&searchmode=basic)   2008
  [[李垚暾]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=afvV0q/search?q=auc=%2522%25E6%259D%258E%25E5%259E%259A%25E6%259A%25BE%2522.&searchmode=basic)   使用模糊理論於中文寫作自動評分之新方法       張道行          [[國立高雄應用科技大學]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=afvV0q/search?q=sc=%2522%25E5%259C%258B%25E7%25AB%258B%25E9%25AB%2598%25E9%259B%2584%25E6%2587%2589%25E7%2594%25A8%25E7%25A7%2591%25E6%258A%2580%25E5%25A4%25A7%25E5%25AD%25B8%2522.&searchmode=basic)   [[資訊工程系]{.underline}](http://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=afvV0q/search?q=dp=%2522%25E8%25B3%2587%25E8%25A8%258A%25E5%25B7%25A5%25E7%25A8%258B%25E7%25B3%25BB%2522.&searchmode=basic)                                                                                        2011
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------- --------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -----------------

兩岸在中文程式方面有長足的進步，例如結巴(jieba)模組，至少在字彙與斷字方面已經有可用的成果，有需要可以參考網站上的資源[^42]。

### 集合的應用

集合的內容可以是任何型態的物件，但是不存在有集合的集合，因為那就是聯集的概念。集合是去除重複資料最有利的小工具，也是資料表之間比較的利器，以下介紹利用str將數字轉成字串，連結之後，以集合將其濃縮，找出資料表中的代表性項目。

範例中讀取TEDS面源資料庫(表'areagrid.csv')，找出每一座標位置的縣市(代碼及名稱)，過程必須先修正其中海上無縣市從屬、還有外島座標與本島座標不同系統的問題(詳見TWD97相關敘述)。

```pytnon
from pandas import *
import numpy as np
from pypinyin import pinyin, lazy_pinyin
fname='areagrid.csv'
df = read_csv(fname)
df.loc[df['DICT'].map(lambda x:np.isnan(x)==True),'DICT']=5300.
df['CNTY']=[str(int(s/100)) for s in list(df['DICT'])]
subX=['44','50','51']
df.loc[df['CNTY'].map(lambda x: x in subX),'UTME']= \\
> [x-**201500** for x in df.loc[df['CNTY'].map(lambda x: x in
> subX),'UTME']]
>
> ...
```
由於各類排放源的空間位置不同，但總體聯集應為台灣地區所有的土地範圍，因為有部份類別的排放是按照鄉鎮區分配到每一網格上，因此確保其範圍是充分且足夠。

為利工作，此處將座標值簡化成公里(取整數)、集中成為單一變數YX，再將座標與縣市代碼合併成一個變數YXCO，**使用集合可以很快去除重複資料，成為單純的數列**輸出成DataFrame。

由於YXCO含有3個變數，只需要按照字串長度將其拆開即可。

...

df['**YX'**]=[int(y)+int(x/1000) for x,y in
zip(df['UTME'],df['UTMN'])]

df['YXCO']=[str(x)+str(y) for x,y in
zip(df['YX'],df['CNTY'])]

s_xy=list(set(df['YXCO']))

co=[int(x[7:]) for x in s_xy]

yx=[int(x[:7]) for x in s_xy]

x=[i%1000*1000 for i in yx]

y=[int(i/1000)*1000 for i in yx]

df_xyc=DataFrame({'x':x,'xx':x,'y':y,'cnty':co})

...

此處用YX的理由是因為X值可能為負，為記住正負號將會浪費一碼，且會造成字串長度不一致，拆解困難。但如果將序列單純做成DataFrame之後，再利用DataFrame的篩選與**df.loc**功能可以很有效率一併解決。此處因台灣地區範圍最東方的座標約380Km(TWD97系統)，因此如果x值在400,000以上，應為負值的x，要把差值計算出來，加回到y值之上。由於計算過程會動到x值，會失去指標的意義，將其先存成xx。

df.loc[df['xx']>400000,'x']=df.loc[df['xx']>400000,'x']-1000*1000

df.loc[df['xx']>400000,'y']=df.loc[df['xx']>400000,'y']-df.loc[df['xx']>400000,'x']

del df['xx']

...

df_cnty=read_csv('cnty.csv')

for i in xrange(len(df_cnty)):

cha=df_cnty.loc[i,'cnty']

ll=lazy_pinyin(cha.decode('big5'))

s=''

for l in ll:

s=s+l

df_cnty.loc[i,'cnty']=s

df_cnty.loc[24,'no']=51

df_cnty.loc[24,'cnty']='lianjiangxian'

d_cnty={x:str(int(y)) for x,y in
zip(df_cnty['cnty'],df_cnty['no'])}

d_cnty.update({'xinbeishi':'41','taoyuanshi':'32'})

d_cnty.update({'sea':'53'})

d2_cnty={x:y for x,y in zip(d_cnty.values(), d_cnty.keys())}

df_xyc['name']=[d2_cnty[str(i)] for i in df_xyc['cnty']]

df_xyc.set_index('cnty').to_csv('cnty_xy.csv')

有關中文編碼

網址用之中文編碼(URL encoding)

這類編碼以%起始，當網址中有中文時，必須用此類來表示。因此如果要程式能上中文網址，或網頁內含此類編碼而不知其含意，就必須進行轉譯。

百分號編碼（英語：Percent-encoding，又稱：URL編碼（英語：URL
encoding）），是特定上下文的統一資源定位符 (URL)的編碼機制.
實際上也適用於統一資源標誌符（URI）的編碼。也用於為application/x-www-form-urlencodedMIME準備數據，因為它用於通過HTTP的請求操作（request）提交HTML表單數據[^43]。

轉譯須藉由urllib.quote或unquote，其轉換只限python2。如以下範例：

In [56]: pwd

Out[56]: u'/home/backup/data/cwb/e-service/read_web'

from pandas import *

import urllib

import os

df=read_csv('stats_tab.csv')

df['url_nam']=[urllib.quote(i.decode('utf8').encode('utf8'))
for i in df.stat_name]

df['url_nam25']=[i.replace('%','%25') for i in
df.url_nam]

h0='https://e-service.cwb.gov.tw/HistoryDataQuery/'

h1='DayDataController.do\\?command=viewMain\\&station\\='

h1='https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do\\?command=viewMain\\&station\\='

h2='\\&stname\\=';h3='\\&datepicker\\='

date='2019-05-30'

for i in xrange(len(df)):

orig=h1+df.loc[i,'stno']+h2+df.loc[i,'url_nam25']+h3+date

os.system('wget '+h0+orig+';mv Day*
'+df.loc[i,'stno']+'_'+date+'.html')

由於python2並未內設所有字元都是unicode，因此必須先將str轉成unicode，python3沒有此一問題，但是python3的urllib不再提供quote及dequote功能。

**%25**是保留字元%，因此url_nam25將會用在該網站內部程式的轉譯。程式中使用wget來下載網站上的網頁內容(測站日報表)，重新命名後再進行解讀。

### 中文轉成漢語拼音

中文方塊字在計算與處理時，確實不如拉丁語系的字母系統，因此如何將中文轉成拼音便是中文程式化的第一步。拼音方式有很多種，主要差異在母音及四聲的標注，此處選擇漢語拼音，是因為不需要26個英文字母以外的特殊字型，較為簡潔。

上網搜尋亦以結巴體系的pypinyin模組[^44]最受推荐，以pip下載裝置後便可呼叫使用，以下範例為SMOKE本土化過程中，需要將各縣市鄉鎮代碼與名稱排列成COSTCY檔案格式，如下。

IA **Dallas Co** 19 49 161040 CST -94.0560 41.6830 591.06890099 -94.2919
-93.7958 41.5008 41.8601 39486

IA **Johnson Co** 19103 162120 CST -91.6010 41.6440 610.69247815
-91.8347 -91.3679 41.4241 41.8568 104754

KS **Anderson Co** 20 3 17 60 CST -95.2910 38.2110 585.61316017 -95.5125
-95.0612 38.0306 38.3877 8168

```python
$/home/SMOKE4.5/data/ge_dat% cat town.py
# coding='utf-8'
from pypinyin import pinyin, **lazy_pinyin**
from pandas import *
#df=read_csv('town.txt',dtype={'code':str},sep='\\t') Note1
df=read_csv('town.csv',dtype={'code':str})
col=df.columns **#Note 2**
df['Name']=[0 for x in xrange(len(df))]
for i in xrange(len(df)):
cha=df.loc[i,col[3]]
if type(cha)==float:continue **#Note 3**
s=**lazy_pinyin**(cha.decode('big5')) **#Note 4**
ss=''
for j in s:
ss=ss+j **#Note 5**
df.loc[i,'Name']=ss
df.loc[i,'code1']=df.loc[i,'code'][0:2]
df.loc[i,'code2']=df.loc[i,'code'][2:4]
a=['code','code1','code2','Name',col[3]]
df[a].set_index('code').to_csv('town2.csv')
```
$ tail town2.csv

5001,50,01,jinchengzhen,金城鎮

5002,50,02,jinhuzhen,金湖鎮

5003,50,03,jinshazhen,金沙鎮

5004,50,04,jinningxiang,金寧鄉

5005,50,05,lieyuxiang,烈嶼鄉

5006,50,06,wuqiuxiang,烏坵鄉

5101,51,01,nanganxiang,南竿鄉

5102,51,02,beiganxiang,北竿鄉

5103,51,03,juguangxiang,莒光鄉

5104,51,04,dongyinxiang,東引鄉

程式編寫重點說明如下：

中文字形檔案在複製到工作站的時候，會將該列文字的順序予以變亂，即使是tab間格的txt檔也無法避免，因此建議還是在window環境中作業為宜。

中文字的欄位名稱做為字串在運作上還不是很順暢，建議還是以變數方式以避免錯誤。

當csv太長，有可能會讀到無資料，標記為NaN，是個實數而不是字串。

將中文方塊字轉成漢字拼音的文字序列，其長度為2\~4字都可能。

將英文之字串序列連在一起，成為像是一個英文字的感覺。

Python 3的中文問題

Python3不再有unicode()指令，同時也多了byte的格式(type)，其間的差異在：u及b2個新的type：

原本py2認為\\n是字元，py3認為是byte，因此text.split('\\n')是不能執行的，必須加b：text.split(b'\\n')
，原encode也要改成decode[^45]。此外原本中文字是字元。在py3也要加u''。

pdf文字的讀取

有不少網友提供python讀取pdf的程式庫模組，可以詳見網友的回顧及評論(如[^46])，然而並非所有模組都有跟著python進版，使用者還是必須逐一測試。

由於測試結果直接讀寫pdf並未成功，以下2個範例均先行轉換成一般文字檔案，再以python程式讀取。前者以**vi**進行讀取轉換格式，後者以linux指令**pdf2txt**進行轉換。

先經vi轉成文字檔案

以下以一讀取pdf檔案(數據表格)的程式，介紹python的寫作技巧，也可以應用在機器閱讀相關的情況之中：

下圖為目標要讀取的表格，程式的目的就是將此pdf書面表格讀成csv格式的表格，以利計算。

![](media/image5.png){width="5.802638888888889in"
height="2.928059930008749in"}

基本上此表可以分為化學物質名稱(name)、中間的碳鍵比例(mid)、分子量(MW)、以及碳數(nc、#carbon)等4個部分。最後的2欄最容易，名稱還算可以找到規則，最難的是中間部分。

一般書面檔案要先數位化(scan與文字辨識)，慶幸的是此pdf檔並未鎖住，可以全選、複製、到文字處理軟體貼上。

此處建議使用linux上的vi，可以接受龐大文字的處理，整理出表格內容(cbm_cb5.txt)的內容(taking
sample, not in sequence)如下：

name NASN PAR OLE TOL XYL FORM ALD2 ETH ISOP MEOH ETOH NR CH4 ETHA IOLE
ALDX TERP MW #carbons

methane 00000000000010000 16.04 1

ethane 00000000000001000 30.07 2

n-butane 04000000000000000 58.12 4

methyldecanes 0 9.5 0 0 0 0 0 0 0 0 0 1.5 0 0 0 0 0 156.31 9.5

c5 substituted cyclohexane 0 10.25 000000000 0.75 00000 154.3 10.25

dimethylnonanes 0 10.4 0 0 0 0 0 0 0 0 0 0.6 0 0 0 0 0 156.31 10.4

isomers of dodecane (c12 paraffins) 0 10.67 000000000 1.33 00000 170.34
10.67

isomers of tetradecane (c14 paraffins) 0 10.75 000000000 3.25 00000
198.39 10.75

isomers of octadecane (c18 paraffins) 0 16.5 0 0 0 0 0 0 0 0 0 1.5 0 0 0
0 0 254.5 16.5

dl-limonene {dipentene} 00000000000000001 136.24 10

terpene 00000000000000001 136.24 10

methyldecenes 0 8 0.5 00000000000010 154.3 11

c11 olefins 0 8 0.5 00000000000010 154.3 11

整理出name部分並不是單一個字，還可能包括數字與大/小括號、迫折號，mid部份共有17欄，若是個位數，大多相連一起，但也有分欄的，有小數點或十位數則為獨立一字串。MW雖然大多數是有小數點的實數，但也出現沒有小數點的整數。nc則相反，大多數是整數，少數是實數。


```python
[kuang@master teds9.0]$ cat rd_cbm.py
from pandas import *
"""
This routine is used to read the text table of cb5.
The original text is from:
Yarwood. G., S. Rao, M. Yocke, and G.Z. Whitten. 2005b. Updates to the
Carbon Bond chemical
mechanism: CB05. Final Report prepared for US EPA. Available at
http://www.camx.com/publ/pdfs/CB05_Final_Report_120805.pdf.
The vi editor is helping to paste the characters copied from pdf.
After deleting the other text, only appendix table-like is stored to
cbm_cb5.txt and the task begins.
The algorithm used is quite simple: locate, cut and store.
The resultant matrix is save as cbm_cb5.csv.
"""
def sp_str(line):
""" change the string into a series of unique characters.

Use it to transform '01000' to ['0','1','0','0','0']

Although this small routine is used just once,

due to its simplicity, still remained here."""

**return** [x for** x **in** line]

**#section 1**

fname='cbm_cb5.txt'

nsp=17

bac=[')','}','(','-'] #the right most end of name characters

**with** **open**(fname) **as** ftext: #open the file

lns=[line for** line **in** ftext] #read the line text

**#*section 2**

(name,mid,mw,nc)=([],[],[],[]) #divide into 4 parts

for** line **in** lns:

w=[j for** j **in** line.split()] #split the words

len_w=len(w) #number of words

llne=len(line) #n of total characters

**#section 2-1**

**if** len_w > 2 **and** llne > 3 **and** '.' **in** line:#skip
1st/end line

mw.append(w[len_w-2]) #record the last 2 word

nci=w[len_w-1]

nc.append(nci) #record the #carbons

**#section 2-2**

for** j **in** **xrange**(llne-3,0,-1): #read from right to left

**if** line[j].isalpha() or line[j] **in** bac:

**break**#first abc and bac's to locate end of name

namei=line[0:j+1] #save the name

name.append(namei) #store to the list

name_tmp='' #collect the name's word

**#section 2-3**

for** j **in** **xrange**(len_w): #test for every word

name_tmp=name_tmp+' '+str(w[j])#concate the words

**if** namei == name_tmp[1:]: #check for name=words

**break** #found the words to form the name

**#section 2-4**

seqm=[]

for** k **in** w[j+1:len_w-2]: #the other words are mid

boo1=('.' in k) #word with '.' must be isolated

boo2=(k==nci) #nc=word, may be 10\~15, strickly

boo3=(len(k)==2 and int(k)\<20 and int(k)>9)#broadly

**if** boo1 **or** boo2 **or** boo3: #the rules must be tried

seqm.append(k) #the words did not take splitted

**else**: #other long words are splitting

seqm=seqm+[o for** o **in** sp_str(k)]#add to the list

**if** **len**(seqm)!=nsp: #in case of failue

**print** line #may be the bac shortage

**print** namei #do not trust human eye

**print** seqm #try and error is golden rule

mid.append(seqm)#the 2d mid must be further proccessed

**else**: #error line printed after debugs !!!

print lns.**index**(line),line

**#section 3**

lens=**len**(mid) #the resultant numb. of rows

cols=[n for** n **in** lns[0].split()] #first line is col name

sp_nm=cols[1:nsp+1] #split the species name

d={} #empty set of dictionary

for** n **in** **xrange**(nsp): #loop for sp, 2d mid to column

d.update({sp_nm[n]:Series([mid[o][n] for** o **in**
**xrange**(lens)])})

d.update({'name':Series(name)}) #store the columns

d.update({'MW':Series(mw)})

d.update({'#carbons':Series(nc)})

df_ln=DataFrame(d) #change to df format

#sort the columns order in the cols sequence

df_ln[cols].set_index('name').to_csv('cbm_cb5.csv') #output
```
讀取程式大致區隔成3個段落，

1.  section 1為開啟檔案與輸入每一行文字，將其儲存在序列lns裏。

nsp是中間(mid)陣列的欄數，須予以給定，做為確認之用。bac是化學物質名稱(name)最右字元出現的特輸符號，可以由試誤法逐一找到。

2.  section 2是主要解讀的部份。

首先以序列的方法split()將一行文字按照區隔字元(可以是\\,或者是\\tab，若無特別指定，則為空格)將一行拆解成字串的序列(w[])，字數至少要包括MW與nc等2項，以避免讀到空白行，同時也必須有小數點，以避免處理第一行。以下則針對讀取到的字串進行辨識及處理。

最後2個字分別是分子量與碳數，這2個字並沒有與其他字相連的情況，因此值接儲存成該欄的序列(**section
2-1**)。**section
2-2**從行尾開始向左辨識，若是讀到英文字母(line[j].isalpha())，或者是前述指定的name右邊界特殊字元bac[]，則停止辨識，開始切割，將該行文字左端到停止處，儲存到name[]的序列裏，停止處到最後2個字之前，則為mid[]的內容。然而為達成此一目標，還需要將該行文字停止處與字串w[]編號做一連結。

連結的方式可以使用in指令，看看w[]字串是否在name裏，如果name裏有數字，這個方式就會誤判。或者將name拆解，將拆解後的字串個數從w[]前面的個數中扣除，此法邏輯上有其合理性，但無法得到保證。**section
2-3**此處選用最嚴謹的方式來判別字串w[]與行文字段落所得到的name[]的異同，從最左邊開始，將字串逐一累加，加至正好等於name[]的內容，其後部分則為mid[]，如此才不會出現誤判的情形。字串間以一空白隔開，經測試原檔案的name沒有2個以上的空白，否則也會造成失敗，所以說是較嚴格的邏輯。

3.  section 2-4是整個讀取處理最核心的部分

按照前述的觀察與策略，有小數點的實數(boo1=('.' in
k))會是個別的字串，其餘相連的整數，則可以用字串變序列的方式(副程式sp_str)，將其變成字串的序列，再將此二類的字串循序加在同一個序列中，如此則大功告成，組成mid[]2維的陣列。

在試誤的過程中發現，除了實數之外，2碼的十位數也會自成字串，此點較難證實(boo3=(len(k)==2
and int(k)\<20 and
int(k)>9))，還好此十位數大多恰好是nc，可以查證，較為確定(boo2=(k==nci))。因此再加另2個判別式，事實上boo2是包含在boo3的情況中。

在離開此段之前，程式設計了嚴謹的檢驗，就是mid[]的欄數，必須正好與碳鍵代表成分(PAR、OLE、...)之個數相等，以避免在排列時發生跳欄的錯誤。

第3大段落(section 3)是整理表格與輸出。

首先整理欄位名稱(cols)不但包括了碳鍵代表成分的名稱(sp_nm)，也包括了MW與碳數，前者也用在將2維的mid[]轉成各個成分的欄位序列，同時cols也是整體dataframe的橫向順序。

pandas的
dataframe可以由個別欄所組成的，其格式是欄位名稱與相同長度的序列，是以字典型態所組成的集合。因此各欄之間是沒有順序的，必須另外指定，在輸出的表上才不會造成錯誤。此外，若無特別指定，dataframe會有一欄index，並無特別意義的序號，這在excel中是多餘的，因此可以用.set_index('name')指令，給定了最左邊欄位即可去除。

以下為讀取結果。

![](media/image6.png){width="5.800001093613298in" height="4.64in"}

Linux指令直接讀取pdf檔案

以下乃是台北市交通局歷年路口調查結果pdf檔案的讀取範例，如圖所示[^47]。我們要讀取的是表格下方的加總「合計」結果，包括路口站名(翻譯成漢語拼音以利資料庫處理，詳前述2.2.1)、方向、上/下午、大/小型車/機車的流量及比例、PCU、以及PHF。目標是寫成資料庫以csv檔案格式輸出。由於路口很多、以pdf格式儲存計有2年463個檔案，必須以程式為之。

由於表格循序解讀的方式，與XML格式相同(詳3.8.4)，以下介紹到讀成一階序列的過程。後續利用相同的程式，將交通量最後轉換成資料庫格式的架構。

![](media/image7.png){width="5.800001093613298in" height="4.64in"}

首先在linux平台以**pdftotxt**指令[^48]進行轉換。首先運用bash迴圈技巧將所有的pdf都讀成txt檔。

for i in $(ls *pdf);do root=\`echo $i\|cut -d'.'
-f1\`;**pdftotext** -f 1 -l 1 $root'.pdf' $root'.txt';done

kuang@master /home/backup/data/ETC/TaipeiVD/htm

$ more sht3_13_NI003.txt

89.0 6031 %84 597 %74 587 %5 48 %21 161 29 49 0 5 %76 378 307 394 0 74
66 %12 272 0 891 0 23 D

97.0 1562 %66 5562 %13 3421 %3 431 %31 733 991 231 0 93 %78 4132 6542
1111 08 51 57

C

49.0 3941 %34 977 %05 409 %7 811 %51 422 39 931 0 01 %26 329 686 725 0
06 282 %32 643 0 832 74 1 B

19.0 2792 %17 5533 %52 1611 %4 581 %01 403 51 921 0 85 %98 4262 0433
2301 08 52 271 %1 44 0 0 22 0 00:91-00:81 A

97.0 3801 %05 207 %54 936 %5 76 %8 38 63 05 0 4 %46 396 666 253 0 43 64
%82 703 0 732 0 92 D

09.0 0153 %77 7174 %12 9521 %2 721 %8 392 532 301 0 82 %29 7123 2844
6511 98 01 631

C

18.0 8821 %54 517 %94 577 %6 89 %41 581 08 911 0 6 %86 968 536 694 0 95
49 %81 432 0 061 33 0 B

49.0 7902 %26 2281 %23 269 %6 971 %11 522 12 511 0 33 %68 0181 1081 748
801 7 191 %3 26 0 0 13 0 00:90-00:80 A

2248 %26 4857 %43 3904 %4 125 %21 6201 993 494 0 211 %08 4376 5817 3613
061 741 595 %8 266 0 634 96 33 00:91-00:81

9287 %06 8566 %63 1793 %4 384 %21 479 423 984 0 801 %18 2726 4336 1213
661 701 384 %7 385 0 163 95 34 00:81-00:71

8797 %66 6597 %03 5363 %4 174 %01 687 273 783 0 17 %28 9856 4857 1582
791 011 764 %8 306 0 793 46 92 00:90-00:80

4675 %86 0785 %72 4332 %5 654 %01 895 052 432 0 48 %18 0564 0265 9971
461 801 162 %9 615 0 103 55 54 00:80-00:70 計合

由結果發現格式轉換的結果，不論行數、每行的內容、甚至連字串的順序都完全顛倒了。因此程式撰寫的重點就在如何將順序翻轉。

kuang@master /home/backup/data/ETC/TaipeiVD/htm

$ cat rd_sht3.py

from bs4 import BeautifulSoup

from pandas import *

from pypinyin import pinyin, lazy_pinyin

import itertools

def FindLastABC(end):

for last in xrange(end,-1,-1):

if a[last] in ABC:break

return last

with open('sss.txt') as ftext:

s=[line.split('\\n')[0] for line in ftext]

ABC=['A','B','C','D','E','F']

year,time,dirn,name,road=[],[],[],[],[]

nam_v=['Lvolume','Lratio','Mvolume','Mratio','Svolume','Sratio','PCU','PHF']

v=[]

for iv in xrange(8):

v.append([])

for fname in s:

yr=int(fname.split('_')[1])+90+1911

if fname.split('.')[1]=='htm':

#section 1

fn=open(fname,'r')

soup = BeautifulSoup(fn,'html.parser')

td=soup.find_all('td')

a=[str(td[i]).split('>')[1].split('\<')[0] for i in
xrange(len(td))]

else:

with open(fname) as ftext:

**ln**=[line.split() for line in ftext]

#section 2

if fname=='sht3_12_SI114.txt':ln.remove(ln[0])

if fname!='sht3_13_NI028.txt':

#section3

#reverse the lines

lnn=[ln[-1-i] for i in xrange(len(ln))]

lna=[]

for i in xrange(len(lnn)):

#reverse the words

lna.append([lnn[i][-1-j] for j in xrange(len(lnn[i]))])

ln=[]

#reverse the string

for i in xrange(len(lna)):

ln1=[]

for j in xrange(len(lna[i])):

string=lna[i][j]

sa=''

ibeg=len(string)-3

if ibeg >=0:

while True:

try:

string[ibeg:ibeg+3].decode('utf-8')

except UnicodeError:

#不是utf8，每次轉一個字元。

sa=sa+string[ibeg+2]

ibeg=ibeg-1

if ibeg\<0:break

else:

if len(string[ibeg:ibeg+3].decode('utf-8'))==1:

#中文字，一批三個字元，順序不翻轉

k=ibeg

sa=sa+string[k]+string[k+1]+string[k+2]

else:

#非中文字，一批也是三個字元，順序要翻轉

for k in xrange(ibeg+2,ibeg-1,-1):

sa=sa+string[k]

#不足3字元的尾部

if 0\<ibeg\<3:

for k in xrange(ibeg-1,min(-1,ibeg-2),-1):

sa=sa+string[k]

ibeg=ibeg-3

#判斷是否做完了?!

if ibeg\<0:break

else:

for k in xrange(len(string)-1,-1,-1):

sa=sa+string[k]

ln1.append(sa)

ln.append(ln1)

a=list(itertools.chain(*ln))

4.  Section 1使用beutifulsoup解析

此段內容會在BS相關段落中交代，讀取、解析的結果是一個序列a。

5.  Section 2例外狀況

sht3_12_SI114.txt檔案有一個頁碼出現。sht3_13_NI028.txt檔案順序是正確的，沒有相反。

6.  Section 3翻轉順序

翻轉行、字的順序沒有太大的問題，在翻轉字元順序時，遇到了中文字是每三個utf8字串成一組，必須先判斷是否是中文字，判斷的方式是此組字串經過decode之後，若是中文字，其長度會是1
(len(string[ibeg:ibeg+3].decode('utf-8'))==1)，若不是，就還會是3。

pdfminer

[^49]

pdf breaker

[^50]

pdf OCR

10MB以下免費[^51]

tessaract[^52]

字典(dict)的應用範例

對fortran使用者而言，字典是一個新奇的容器，沒有順序、類似集合，一個元件有2個內容(key
and
value)，又有對照及轉換關係，可以直接呼叫，不再重複搜尋索引。然而字典在其他許多語言中已經有傑出的表現，在進行資料對照關係時，有其方便之處。

讀取程式的呼叫及回傳

以下為一SMOKE本土化過程中的運用範例。scc_PM2_5.py讀入過去所有的gsref的檔案(檔名由locate
gsref*指令產生，存入**all_GSREF.nam**檔案內)，搜尋是否有所要的SCC與P_NUMBER對照關係組合，rd_gs便是一通用的讀取程式，可以包括讀取SMOKE系統中的GSREF、GSCNV或GSPRO等3種特性之GS檔案，其引數及回傳內容，即設計以字典形式傳遞，以保有GS特性及其內容(對照到檔名fname?或回傳資料表return_df)，不再需要重複寫3個功能內容很相似、可以平行運作的讀取副程式。

> kuang@master /home/SMOKE4.5/subsys/smoke/scripts/run
>
> $ cat scc_PM2_5.py
>
> from pandas import *
>
> def
> rd_gs(args)**:#args={'gsref':fnameR,'gspro':fnameP,'gscnv':fnameC}**
>
> from pandas import DataFrame,Series
>
> skip=['#','/','!']
>
> return_df={}
>
> for iarg in args:
>
> fname=args[iarg]
>
> if type(fname)!=str:cotinue
>
> if iarg=='gspro':
>
> cols=['P_NUMBER','POLL_ID','SPEC_ID','SPLIT_FAC','DIVISOR','MASS_FRAC']
>
> if iarg=='gsref':cols=['SCC','P_NUMBER','SPEC_ID']
>
> if iarg=='gscnv':cols=['ID_FROM','ID_TO','CONV_FAC']
>
> lns=[]
>
> with open(fname) as ftext:
>
> for line in ftext:
>
> if line[0] not in skip and line.count(';')>=len(cols) :
>
> lns.append(line.strip('\\n').replace('"','').split(';'))
>
> d={}
>
> for i in cols:
>
> j=cols.index(i)
>
> d.update({i:Series([x[j] for x in lns])})
>
> df=DataFrame(d)
>
> note=[x+'!' for x in df[cols[-1]]]
>
> df[cols[-1]]=[x.split('!')[0] for x in note]
>
> df['NOTE']=[x.split('!')[1] for x in note]
>
> return_df.update({iarg:df})
>
> return return_df
>
> df_VB=read_csv('/home/camxruns/2013/ptse/TEDS9.0/TedsToSmoke/vbird_gsref.cmaq.cb4p25.csv')
>
> df_VB_PM=df_VB[df_VB['spec']=='PM2_5']
>
> df=df_VB_PM.reset_index()
>
> with open('/home/SMOKE4.5/subsys/smoke/scripts/run/err_PM2_5.scc')
> as ftext:
>
> pbm_scc=[line.strip('\\n') for line in ftext]
>
> pbm_scc=list(set(pbm_scc))
>
> pbm_scc.sort()
>
> with
> open('/home/SMOKE4.5/subsys/smoke/scripts/run/**all_GSREF.nam**')
> as ftext:
>
> gsref_nam=[line.strip('\\n') for line in ftext]
>
> for i in xrange(len(df)):
>
> s_SCCnPRO.add((df.loc[i,'SCC'],df.loc[i,'prof']))
>
> **#reading gsref files**
>
> for fname in gsref_nam:
>
> **a=rd_gs({'gsref':fname})**
>
> df=**a['gsref']**
>
> if 'PM2_5' not in set(df['SPEC_ID']):continue
>
> print fname
>
> df=df[df['SPEC_ID']=='PM2_5'].reset_index()
>
> for i in xrange(len(df)):
>
> s_SCCnPRO.add((df.loc[i,'SCC'],df.loc[i,'P_NUMBER']))
>
> a=list(s_SCCnPRO)
>
> a_scc=[x[0] for x in a]
>
> a_pro=[x[1] for x in a]
>
> df=DataFrame({'SCC':a_scc,'P_NUMBER':a_pro})
>
> df_1=df[df['SCC'].map(lambda x:x in pbm_scc)]
>
> df_1.set_index('SCC').to_csv('**found.csv**')

在**#reading gsref files**段落中，程式會重複開啟系統中各個GSREF檔案，
呼叫rd_gs副程式進行讀取成資料表的動作，其引數為一字典的形式**{'gsref':fname}**，以保持資料特性與檔名關係的連結。回傳的結果a亦為一字典，因此其對應之內容**a['gsref']**便是副程式所讀到的資料表了。

在本範例中，運用字典可以提高副程式rd_gs的應用彈性，減省副程式的個數，同時也不會造成引用的錯誤，有其強大之處。

模擬物質名稱及其分子量之對照表

在SPECIATE或光化反應機制更新版本的過程中，需要大量應用對照關係，其中每個模擬物質(CB_spec)與其分子量('Molwt')的關係，在計算莫耳數時使用非常頻繁，且為一對一固定的關係，最適合以dict形式來計算。

> kuang@master /home/camxruns/2013/ptse/TEDS9.0/TedsToSmoke
>
> $ cat gspro.py
>
> #importing modules
>
> from pandas import *
>
> import csv
>
> #loading dataframes
>
> df_pbm=read_csv('d_pbm.csv',dtype=str)
>
> df_cb5=read_csv('/home/camxruns/2013/ptse/TEDS9.0/CB05/cbm_cb5_2.csv',dtype={'SAROAD':str,'CAS1':int})
>
> df_cb4=read_csv('df_cb4.csv',dtype={'SAROAD':str})
>
> df_prm=read_csv('../CB05/camx.prm.cb05_cf.csv')
>
> df_spec=read_csv('df_spec.csv',dtype={'P_NUMBER':str,'SAROAD':str})
>
> df_specV=read_csv('../../df_specV.csv',dtype={'P_NUMBER':str,'SAROAD':str})
>
> **#preparing the dicts**
>
> s5=set(list(df_prm['Gas_Spec'])) & set(df_cb5.columns)
>
> d_s5={}
>
> for i in s5:
>
> d_s5.update({i:list(df_prm.loc[df_prm['Gas_Spec']==i,'Molwt'])[0]})
>
> d_s5.update({'NR':16.})
>
> s4=set(list(df_prm['Gas_Spec'])) & set(df_cb4.columns)
>
> d_s4={}
>
> for i in s4:
>
> d_s4.update({i:list(df_prm.loc[df_prm['Gas_Spec']==i,'Molwt'])[0]})
>
> d_s4.update({'NR':16.})
>
> **#looping for each profile and speciate**
>
> srd5=list(df_cb5['SAROAD'])
>
> cas5=list(df_cb5['CAS1'])
>
> srd4=list(df_cb4['SAROAD'])
>
> cas4=list(df_cb4['CAS'])
>
> df_pbm_pro=DataFrame({})
>
> p_num=list(set(df_pbm['Profile_NO']))
>
> col=['P_NUMBER','Poll_ID','CB_spec','Split_factor','Divisor','Mass_frac']
>
> p_numS=set(df_spec['P_NUMBER'])
>
> p_numSV=set(df_specV['P_NUMBER'])
>
> for p in p_num:
>
> if p in p_numS:
>
> df_p=df_spec[df_spec['P_NUMBER']==p]
>
> elif p in p_numSV:
>
> df_p=df_specV[df_specV['P_NUMBER']==p]
>
> else:
>
> continue
>
> mwt=list(df_p['SPEC_MW'])
>
> mole=[i/j for i,j in zip(list(df_p['WEIGHT_PER']),mwt)]
>
> s_p=list(df_p['SAROAD'])
>
> c_p=list(df_p['CAS'])
>
> l=len(df_p)
>
> wtj=[]
>
> nmj=[]
>
> div=[]
>
> spl=[]
>
> for i in xrange(l):
>
> (j5,j4)=(0,0)
>
> if s_p[i] in srd5: j5=srd5.index(s_p[i])
>
> elif c_p[i] in cas5: j5=cas5.index(c_p[i])
>
> elif s_p[i] in srd4: j4=srd4.index(s_p[i])
>
> elif c_p[i] in cas4: j4=cas4.index(c_p[i])
>
> else:
>
> print 'not found',s_p[i],c_p[i]
>
> if j5!=0:
>
> for j in d_s5:
>
> m_cbm=df_cb5.loc[j5,j]
>
> if np.isnan(m_cbm) or m_cbm==0:continue
>
> molei=round(mole[i]*d_s5[j],4)
>
> if molei>0.0001:
>
> wtj.append(molei)
>
> div.append(mwt[i])
>
> spl.append(d_s5[j])
>
> nmj.append(j)
>
> if j4!=0:
>
> for j in d_s4:
>
> m_cbm=df_cb4.loc[j4,j]
>
> if np.isnan(m_cbm) or m_cbm==0:continue
>
> molei=round(mole[i]*d_s4[j],4)
>
> if molei>0.0001:
>
> wtj.append(molei)
>
> div.append(mwt[i])
>
> spl.append(d_s4[j])
>
> nmj.append(j)
>
> a=round(sum(wtj),4)
>
> if 'NR' not in nmj and a \< 100:
>
> wtj.append(round(100-a,4))
>
> nmj.append('NR')
>
> div.append(d_s5['NR'])#np.mean(mwt))
>
> spl.append(1.0)
>
> else:
>
> wtj=[round(x*100/a+5.E-6,4) for x in wtj]
>
> df_s=DataFrame({'Mass_frac':Series([round(x/100.,6) for x in
> wtj]), \\
> 'CB_spec':Series(nmj),'Split_factor':Series(spl),'Divisor':Series(div)})
>
> **#doing pivot**
>
> df1=pivot_table(df_s,index=['CB_spec'], \\
> values=['Split_factor','Mass_frac'],aggfunc=np.sum).reset_index()
>
> df2=pivot_table(df_s,index=['CB_spec'],values=['Divisor'],aggfunc=np.mean).reset_index()
>
> df=concat((df1,df2['Divisor']),axis=1)
>
> l=len(df)
>
> df['P_NUMBER']=[p for x in xrange(l)]
>
> df['Poll_ID']=['VOC'for x in xrange(l)]
>
> df3=DataFrame({'Poll_ID':[s for s in list(df['CB_spec'])],
> \\
>
> 'Mass_frac':[1. for x in xrange(l)],'CB_spec':[s for s in
> list(df['CB_spec'])], \\
>
> 'Split_factor':[1. for x in xrange(l)],'Divisor':[d_s5[s]
> for s in list(df['CB_spec'])], \\
>
> 'P_NUMBER':[p for x in xrange(l)]})
>
> df=df.append(df3[col]).reset_index()
>
> del df['index']
>
> if p_num.index(p) == 0:
>
> df_pbm_pro=df[col].reset_index()
>
> del df_pbm_pro['index']
>
> else:
>
> df_pbm_pro=df_pbm_pro.append(df[col]).reset_index()
>
> del df_pbm_pro['index']
>
> df_pbm_pro['Split_factor']=df_pbm_pro['Mass_frac'].round(6)
>
> df_pbm_pro['Divisor']=df_pbm_pro["Divisor"].round(1)
>
> df_pbm_pro['Mass_frac']=df_pbm_pro['Mass_frac'].round(6)
>
> df_pbm_pro[col].set_index('P_NUMBER').to_csv('gspro.csv',sep=';',
> quoting=csv.QUOTE_NONNUMERIC)

numpy程式庫

numpy可能說是python數據處理的基礎，雖然很多程式也在python的內設程式範圍(如max,min等)，但是numpy下的程式更適合在向量矩陣的處理。以下範例即為模擬範圍內矩陣的處理(排放量按照點、線、面三者的比例，正比分配之後寫到新的檔案)，包括矩陣的相加(自我增值)、相除、nan判別、以及部分指定，說明如下：

#!/cluster/miniconda/bin/python

from PseudoNetCDF.camxfiles.Memmaps import uamiv

**import numpy as np**

import os,sys

pal=['P','A','L']

domains=[str(i) for i in xrange(2,6)]

nt0=720

for D in domains:

path0={i:'fortBE.'+D+'13.teds90.base04NPetc'+i for i in pal}

ems_file0={i:uamiv(path0[i],'r') for i in pal}

pathO3='fortBE.'+D+'13.teds90.1704baseO3'

path1={i:pathO3+i for i in pal}

for i in pal:

os.system('cp '+pathO3+' '+path1[i])

ems_file1={i:uamiv(path1[i],'r+') for i in pal}

v4=filter(lambda x:ems_file0[pal[0]].variables[x].ndim==4,

> [i for i in ems_file0[pal[0]].variables])

nt,nlay,nrow,ncol=ems_file0[pal[0]].variables[v4[0]].shape

for v in v4:

t=np.zeros(shape=(nt0,nlay,nrow,ncol))

for i in pal:

t+=np.array(ems_file0[i].variables[v][:nt0,:,:,:])

for i in pal:

rat=np.array(ems_file0[i].variables[v][:nt0,:,:,:])/t

where_are_NaNs = np.isnan(rat)

rat[where_are_NaNs] = 0

o3v=np.array(ems_file1[i].variables[v][:nt0,:,:,:])

ems_file1[i].variables[v][:nt0,:,:,:]=rat*o3v

for i in pal:

ems_file1[i].close

橙色網底是**numpy**宣告的方式，一般語言會有宣告段，採事先宣告的方式，在程式計算之前一次宣告完畢，但python可以在使用前再宣告即可。可以宣告陣列元素的型態、大小(dimensions)以及數值(**ones,zeros**)。如果沒有現成的模版可以照抄，則必須用宣告的方式產生，因為**numpy.array**似乎沒有**append**、**update**、**add**的功能，雖然可以**reshape**。

青色部分是**numpy.array**自我增值的寫法，等式右邊也必須是個np.array，且大小必須完全一樣。由於變數**v**在時間上的長度可能較**nt0**更長，因此要調整成一樣，就必須指定成**0:nt0，**或簡寫成**:nt0**。由於某一個維度指定了，**uamiv**必須知道其他方向的維度是如何設定，因此也必須出現:，否則**uamiv**不知道是哪一個維度被指定了。**uamiv**是uam格式的程式庫，未來會進一步說明。

特別要介紹**numpy.array**的功用，是將陣列形式的物件，轉變成為**numpy.array**形式。如範例中括弧內的物件，是uamiv檔案的某一個變數內容，雖然也是4維的陣列，但因為還掛有uamiv的許多屬性或功能，並不能進行特定的numpy計算，因此必須先轉成**numpy.array**形式。

紫色部分是陣列相除的作法。特別介紹相除是因為除式陣列中，很可能有0，會發生**NaN**(not
a
number)的結果，一般如果是依序逐一相除，可能會造成程式失敗，必須寫很多條件來避免，但是**numpy.array**可以容忍**NaN**的發生或存在，程式先行計算完成，後續再一併處理就可以了。

**np.isnan(...)**會判斷括弧內的內容是否是**NaN**，如果是**NaN**就會回傳**True**，以便可以進一步處理。由於括弧內的內容是一個龐大的數字陣列，因此回傳結果也是一個龐大的判斷(boolean)陣列，大小尺寸是一樣的。

綠色部分將判斷陣列放在**numpy.array**的引數位置，會產生遮罩(mask)的效果，只有**True**的引數或位置才會發生作用，因此將前面挑出來的**NaN**設為特定的數字(0)，就不再需要逐一檢視判斷了。

紅色的部分是陣列相乘，相乘結果放入uamiv的容器中，最後將其檔案關閉、儲存。

資料處理(Pandas)

在MSOFFICE作業系統上，使用者習慣以excel處理資料表，從原始數據import開始、進行篩選、排序、減貼整理等等作業，最後再進行統計分析或繪圖，功能可以說十分夠用。然而excel及access等軟體最大的困難在於**沒有留下處理的過程**，即使有計算公式，也是隱藏在儲存格內，無法讓其他的使用者可以追溯，在重製時經常發生困難，即使有巨集VBA程式，也常常因為格式有稍微差異而發生錯誤。

使用Python及Pandas可以完全解決此一困境。不但處理過程可以追溯，而且每一個步驟在jupyter上也可以查核確認，在套用到類似情況時，經由稍加修改亦可以得到滿意的結果，使得程式可以廣泛使用，對處理技術的傳播而言，實在是不可多得的解決方案。

安裝

Pandas的安裝可以直接用pip install
pandas指令即可，並無任何困難。執行pandas必須要有numpy，因此要先安裝numpy才能執行程式。

10分鐘教學

Pandas官網有10分鐘教學[^53]，內容包括大多數pandas的操作指令，項目包括：

+----------------------+----------------------+----------------------+
| Directories          | > 意義               | > Summaries of       |
|                      |                      | > directories        |
+----------------------+----------------------+----------------------+
| 1.  Basics           |                      | import               |
|                      |                      | matplotlib.pyplot as |
|                      |                      | plt;import pandas as |
|                      |                      | pd;import numpy as   |
|                      |                      | np                   |
+----------------------+----------------------+----------------------+
| a.  [Object          | >                    | > pd.Series();       |
|     C                | 產生檢視序列及資料表 | > pd.date_range();  |
| reation](http://pand |                      | > pd.DataFrame()     |
| as.pydata.org/pandas |                      |                      |
| -docs/stable/10min.h |                      |                      |
| tml#object-creation) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Viewing         |                      | > pd.dtypes;         |
|     Data](http://p   |                      | > df2.\<TAB>;       |
| andas.pydata.org/pan |                      | >                    |
| das-docs/stable/10mi |                      | df.head();df.tail(3) |
| n.html#viewing-data) |                      | >                    |
|                      |                      | > df.index;          |
|                      |                      | > df.columns;        |
|                      |                      | > df.values;         |
|                      |                      | > df.describe()      |
|                      |                      | >                    |
|                      |                      | > df.T;              |
|                      |                      | > df.sort_index     |
|                      |                      | ();df.sort_values() |
+----------------------+----------------------+----------------------+
| 1                    |                      |                      |
| .  [Selection](http: |                      |                      |
| //pandas.pydata.org/ |                      |                      |
| pandas-docs/stable/1 |                      |                      |
| 0min.html#selection) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Getting](htt    | > 取資料             | > df['A']=       |
| p://pandas.pydata.or |                      | > df.A;df[0:3];    |
| g/pandas-docs/stable |                      | > df['20130        |
| /10min.html#getting) |                      | 102':'20130104'] |
+----------------------+----------------------+----------------------+
| a.  [Selection by    | > 按指標             | > d                  |
|     L                |                      | f.loc[dates[0]]; |
| abel](http://pandas. |                      | > df.loc[           |
| pydata.org/pandas-do |                      | :,['A','B']]; |
| cs/stable/10min.html |                      | > df.loc\            |
| #selection-by-label) |                      | [dates[0],'A']= |
|                      |                      | > df.loc             |
|                      |                      | [dates[0],'A'] |
+----------------------+----------------------+----------------------+
| a.  [Selection by    | > 按位置             | > df.iloc[3];      |
|     Positio          |                      | >                    |
| n](http://pandas.pyd |                      |  df.iloc[3:5,0:2]; |
| ata.org/pandas-docs/ |                      | > df.iloc[1,1]=    |
| stable/10min.html#se |                      | > df.iat[1,1]      |
| lection-by-position) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Boolean         | > 按邏輯             | > df\                |
|     In               |                      | [df.A>0];df2[df2\ |
| dexing](http://panda |                      | ['E'].isin(['t' |
| s.pydata.org/pandas- |                      | ,'f'])];df[df[ |
| docs/stable/10min.ht |                      | 'nst'].map(lambda |
| ml#boolean-indexing) |                      | > x:47\<=x\<=61)]   |
+----------------------+----------------------+----------------------+
| a.  [Setting](htt    | > 給值               | > df['F'] =      |
| p://pandas.pydata.or |                      | > pd.Series([...], |
| g/pandas-docs/stable |                      | > index=pd.date\     |
| /10min.html#setting) |                      | _range('20130102', |
|                      |                      | > periods=6))        |
|                      |                      | >                    |
|                      |                      | > df2[df2 > 0] =  |
|                      |                      | > -df2               |
+----------------------+----------------------+----------------------+
| a.  [Missing         | > NaN                | > df1.               |
|     Data](http://p   |                      | dropna(how='any'); |
| andas.pydata.org/pan |                      | >                    |
| das-docs/stable/10mi |                      | df1.fillna(value=5); |
| n.html#missing-data) |                      | > pd.isna(df1)       |
+----------------------+----------------------+----------------------+
| 1.                   |                      |                      |
|  [Operations](http:/ |                      |                      |
| /pandas.pydata.org/p |                      |                      |
| andas-docs/stable/10 |                      |                      |
| min.html#operations) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Stats](h        | > 統計               | > d                  |
| ttp://pandas.pydata. |                      | f.mean();df.mean(1); |
| org/pandas-docs/stab |                      | > df.sub(s,          |
| le/10min.html#stats) |                      | > axis='index')    |
+----------------------+----------------------+----------------------+
| a.  [Apply](h        | > 函數               | > df.appl            |
| ttp://pandas.pydata. |                      | y(np.cumsum)=df.cums |
| org/pandas-docs/stab |                      | um();df.apply(lambda |
| le/10min.html#apply) |                      | > x: x.max() -       |
|                      |                      | > x.min())           |
+----------------------+----------------------+----------------------+
| a.  [[Histogramming] | > 分布               | > Series.va          |
| {.underline}](http:/ |                      | lue_counts();factor |
| /pandas.pydata.org/p |                      | > = pd.cut(arr, 4)   |
| andas-docs/stable/ba |                      |                      |
| sics.html#discretiza |                      |                      |
| tion-and-quantiling) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [[String         | > 字串               | > s.str.lower()      |
|     Methods]{.underl |                      |                      |
| ine}](http://pandas. |                      |                      |
| pydata.org/pandas-do |                      |                      |
| cs/stable/text.html) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [[Time           | > 時序               | > rng=pd.date_      |
|     Series]{.und     |                      | range('1/1/2012',p |
| erline}](http://pand |                      | eriods=100,freq='S\ |
| as.pydata.org/pandas |                      | ');ts=pd.Series(..., |
| -docs/stable/timeser |                      | > index =rng);       |
| ies.html#timeseries) |                      | > ts.resa            |
|                      |                      | mple('5Min').sum() |
+----------------------+----------------------+----------------------+
| 1.  [Merge](h        |                      |                      |
| ttp://pandas.pydata. |                      |                      |
| org/pandas-docs/stab |                      |                      |
| le/10min.html#merge) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Concat](ht      | > 接龍               | > pd.concat([df1,   |
| tp://pandas.pydata.o |                      | > df2, df3])        |
| rg/pandas-docs/stabl |                      |                      |
| e/10min.html#concat) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Join](http://   | > 左右合併           | > pd.merge(left,     |
| pandas.pydata.org/pa |                      | > right, on='key') |
| ndas-docs/stable/10m |                      |                      |
| in.html#join)(merge) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Append](ht      | > 附加               | > df.append(s,       |
| tp://pandas.pydata.o |                      | >                    |
| rg/pandas-docs/stabl |                      |  ignore_index=True) |
| e/10min.html#append) |                      |                      |
+----------------------+----------------------+----------------------+
| 5.  Grouping and     |                      |                      |
|                      |                      |                      |
|    [Reshaping](http: |                      |                      |
| //pandas.pydata.org/ |                      |                      |
| pandas-docs/stable/g |                      |                      |
| roupby.html#groupby) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [[Grouping       | > 小計               | > df.groupby('A')  |
| ]{.underline}](http: |                      | .sum();df.groupby([ |
| //pandas.pydata.org/ |                      | 'A','B']).sum() |
| pandas-docs/stable/g |                      |                      |
| roupby.html#groupby) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Stack](h        | > 堆疊降階           | > stacked =          |
| ttp://pandas.pydata. |                      | > df2.stack          |
| org/pandas-docs/stab |                      | ();stacked.unstack() |
| le/10min.html#stack) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Pivot           | > 樞紐分析           | >                    |
|     Tables](http://p |                      |  pd.pivot_table(df, |
| andas.pydata.org/pan |                      | > values='D',      |
| das-docs/stable/10mi |                      | > index=['A',     |
| n.html#pivot-tables) |                      | > 'B'],           |
|                      |                      | > columns=['C']) |
+----------------------+----------------------+----------------------+
| a.  [[               | > 類別分析           | > df["grade"] =  |
| Categoricals]{.under |                      | > d                  |
| line}](http://pandas |                      | f["raw_grade"]. |
| .pydata.org/pandas-d |                      | astype("category") |
| ocs/stable/categoric |                      | >                    |
| al.html#categorical) |                      | > df["grad         |
|                      |                      | e"].cat.categories |
|                      |                      | > = ["very good", |
|                      |                      | > "good", "very   |
|                      |                      | > bad"]            |
|                      |                      | >                    |
|                      |                      | > df.sort_values(by |
|                      |                      | ="grade");df.group |
|                      |                      | by("grade").size() |
+----------------------+----------------------+----------------------+
| 6.  Showing/[Getting |                      |                      |
|     Data             |                      |                      |
|     In/              |                      |                      |
| Out](http://pandas.p |                      |                      |
| ydata.org/pandas-doc |                      |                      |
| s/stable/10min.html# |                      |                      |
| getting-data-in-out) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Plotting](http  | matplotlib           | ts =                 |
| ://pandas.pydata.org |                      | pd.Series(np         |
| /pandas-docs/stable/ |                      | .random.randn(1000), |
| 10min.html#plotting) |                      | index=pd.date\       |
|                      |                      | _range('1/1/2000', |
|                      |                      | periods=1000));ts =  |
|                      |                      | ts.cumsum();         |
|                      |                      | ts.plot();plt.show() |
+----------------------+----------------------+----------------------+
| a.  [CSV]            | > 檔案IO             | > pd.read_          |
| (http://pandas.pydat |                      | csv('foo.csv');df. |
| a.org/pandas-docs/st |                      | to_csv('foo.csv') |
| able/10min.html#csv) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [HDF5](          |                      | > df.to_hd          |
| http://pandas.pydata |                      | f('foo.h5','df') |
| .org/pandas-docs/sta |                      |                      |
| ble/10min.html#hdf5) |                      |                      |
+----------------------+----------------------+----------------------+
| a.  [Excel](h        |                      | > pd.read\           |
| ttp://pandas.pydata. |                      | _excel('foo.xlsx', |
| org/pandas-docs/stab |                      | > 'Sheet1',        |
| le/10min.html#excel) |                      | > index_col=None,   |
|                      |                      | > na                 |
|                      |                      | _values=['NA']) |
|                      |                      | >                    |
|                      |                      | > df.to\             |
|                      |                      | _excel('foo.xlsx', |
|                      |                      | > she                |
|                      |                      | et_name='Sheet1') |
+----------------------+----------------------+----------------------+
| 1.  [[Gotchas        |                      |                      |
| ]{.underline}](http: |                      |                      |
| //pandas.pydata.org/ |                      |                      |
| pandas-docs/stable/g |                      |                      |
| otchas.html#gotchas) |                      |                      |
+----------------------+----------------------+----------------------+

組成一個資料結構(DataFrame, df)

如果原始資料是一個整理好的資料表，當然直接以df型態讀入記憶體即可(如pandas.read_csv指令，詳第3章資料讀取相關章節)，或者使用list指令將df的內容讀取成序列，如下範例：

```python
# read in meteorology data
wind_df = read_csv('wind.txt', index_col=0, sep='\\t')
```

```python
# record bin labels for velocity ranges and direction
orient = list(wind_df.columns)
intense = list(wind_df.index)
```
然而經常狀況是資料過於龐大，使用者只需要讀取其中的一些序列或矩陣，或者是由不同方式產生的序列要組合成為一個df，此時就需要使用pandas.DataFrame指令。

範例一：空的df容器與附加

List、set及dict均可增減，Pandas
dataframe基本上是欄位名稱及一個序列的特定組合，每一欄是以字典方式(dict)來定義，因此也可以就容器的概念予以增減。字典在python是以大括號{}來表示，因此一個空的資料結構容器就如此表示：

df=DataFrame({})

df_app=DataFrame({column_name:Series(values.list)})

df=df.append(df_app).reset_index()

del df['index']

因為df與df_app會有各自的索引(index)，合併之後都會留存一份，以備發生錯誤時可以還原成原來的2個資料表，如果沒有錯誤，就可以將其刪除。

附加df時也要注意2個df必須有相同的欄位名稱(可以不必有相同的逐欄順序)。

範例二：處理2維聯合頻率函數

Python
numpy在計算多維度聯合頻率的程式(np.histogramdd)可以說強大到不行，當然使用者也可以在python之外計算出結果，整理好一次讀成df，但如果使用numpy處理，就必需將計算結果整併成df。

下面的例子是由聯合機率計算結果，併同序列名稱成為dict，再組合成為一個資料結構(DataFrame,
df)，最後是利用已經建好的風玫瑰(wind
rose)繪圖模組(plotly.Area)，將此df的內容繪製成風玫瑰圖。

...

#forming the output dataframe

import numpy as np

import pandas as pd

x=np.linspace(0,max(ws),num=numBinWS)

its=[]

for i in xrange(numBinWS):its.append(str(int(x[i]*10.)/10.)+'-')

for i in xrange(numBinWS-1):its[i]=its[i]+its[i+1]

wts=['NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S',

'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW','N']

d1={'intensity':pd.Series(its)}

for i in
xrange(numBinWD):d1.update({wts[i]:pd.Series(jointProbs[:,i])})

df=pd.DataFrame(d1)

...

DataFrame將輸入的dict集合(d1)，轉變成pandas看得懂的df格式。其單元要先整理成一樣長度的序列，如範例中的資料表矩陣jointProbs[風速等級,風向]，和its[風速等級]有一樣的長度，即可順利整併，若不一樣長度，需要做merge，詳見下述。

因為是dict的型態，所以每個序列要有自己的名字(key)，如its的名字是'intensity'(風力強度)，每個加上去的陣列，則為各個風向的結果，名字就是wts=['NNE','NE'...'N']。pd.Series()是將序列轉化的程式，其輸入內容即為序列，甚為直觀。

將dict元素加入到一個集合是用update指令，不能用add，因為還包括名字(key)與內容(item)的組合，需要對照是否有舊的key要更新其內容，不是單純加入元件而已。

由於是集合的形態，無法控制各個元素(序列)在column-wise的排列順序(本範例即為風向)，還需要進一步加工。

範例三：處理多筆序列的條件平均值

在套用繪圖軟體時，經常會使用df，除了前述的風玫瑰圖之外，以下為matplotlib的折線圖作為範例。

...

(data_1,data_2,data_3,data_4)=(np.array(dd1),np.array(dd2),np.array(dd3),np.array(dd4))

(w1,N1,A1,s1)=([],[],[],[])

for ss in stn:

s=float(ss)

aa=np.ma.masked_where(data_4!=s, data_1)

bb=np.ma.masked_where(data_4!=s, data_2)

for i in xrange(1,17):

s1.append(s)

w1.append(i)

N1.append(np.mean(np.ma.masked_where(data_3!=float(i), aa)))

A1.append(np.mean(np.ma.masked_where(data_3!=float(i), bb)))

d1={'station':Series(s1),'WD':Series(w1),'NO2':Series(N1),'NH3':Series(A1)}

data=DataFrame(d1)

同樣的，程式也應用了np.ma.masked_where的條件(平均)功能，計算測站上(stn)各個風向(w1)的平均NO2(N1)及NH3(A1)，使用excel上的avergeif或avergeifs公式，也可以達到相同功能，但就必須到儲存格位置，點擊儲存格，方能看到使用者設定的公式。

範例中同樣使用DataFrame與Series等2個副程式，將各項計算成果整理成df形式，方便後續繪圖或分析。

新增、刪除特定行與列

DataFrame一行的新增與刪除的方式甚為直觀，直接以指令df['NameOfNewColumn']=Series([...])即新增一欄。至於新增欄位的排序方式、是否與現有資料庫相容等問題，使用者須自行確認。刪除特定一欄或數欄，可以用del指令，如：

del df_pv['XY'],df_pv['subX']

然而對索引而言，並不是真的有一行名叫'index'的欄位，因此不能使用del指令，要去掉索引欄，必須要reset_index(drop=True)，如：

#eg of /home/python_eg/atmos_diff/McNab.py:

wind_bins_df = wind_bins_df.reset_index(drop=True)

刪除列必須使用drop指令，範例與使用方式會進一步說明。

#eg of /home/camxruns/2013/ptse/TEDS9.0/ rd_cbm.py

df_ln.drop_duplicates(inplace=True)

#eg of /home/python_eg/GHG/wp4.py

df_s.drop(df_s[df_s['plant']==i].index, inplace=True)

新增列可以有幾個方式，一者是應用下述的.loc，整排替換的作法，不過這個方法要先有一個固定長度、空白的DataFrame容器，不適用在未知長度或持續增加長度的狀況。

如果是持續增加長度的情況，可以用df.append()指令，作用方式與序列的append非常類似，只是應用在df之間的附加。附加時要注意，df都要有一樣的欄位，

for i in d_orl:#copy the ID,NAMEs,and STKs

c=d_orl[i] #i is new, c is teds col name

d2.update({i:Series(a3.loc[0,c])})

d2.update({'CAS':Series(sp_ef[js])})

d2.update({'ANN_EMIS':Series(ann)})

d2.update({'AVD_EMIS':Series(avd)})

d2.update({'CEFF':Series(eff)})

d2.update({'ERPTYPE':Series(erptype)})

d2.update({'SRN':Series(srn)})

if srn==0:

df_orl=DataFrame(d2).set_index('SRN')

else:

dforl=DataFrame(d2).set_index('SRN')

df_orl=df_orl.append(dforl)

srn=srn+1

DataFrame的儲存格處理(.loc、.ix)

除了整個資料表、整個欄位序列的處理之外，在excel中經常也必須進入到特定行列位置，進行計算、替換等動作，此時必須藉由.loc、.ix等指令。範例如下：

#eg1

df_ln.loc[df_ln['name'].map(lambda x:
x=='propenylcyclohexane'),'CAS']='5364-83-0'

#eg2 /home/camxruns/2013/ptse/TEDS9.0/check_HEI_em.py

from pandas import *

import numpy as np

from del_dup import check_nan

"""

This routine is used to calculate the sum of emission rates for
different stack heights.

Input file is the TEDS9.0 csv file

Output file is the samary table with stack heights columnwise and
species row-wise.

"""

df=read_csv('point.csv') #read the teds 9.0 point source csv file

df=check_nan(df) #delete the NaN records, only the missing coordinates

cols=df.columns #store all the column names

col_em=filter((lambda x: 'EMI' in x),cols) #filter the emission
rates column names

lb=[-1,0,35,70,150,200] #the lowerbound of stack heights(meter)

ub=[0,35,70,150,200,250] #the upperbound of stack heights(meter)

boo=[] #boolean container

col_h=['SP','T/y'] #output column names

s_dum=list([0]*len(col_em)) #dummy column for \...

d1={col_h[0]:Series(s_dum)} #species names container

d1.update({col_h[1]:Series(s_dum)}) #total amount container

for i in xrange(len(lb)): #do loop for each stack heights

col_h.append(str(lb[i])+'\<H\<='+str(ub[i])) #expanding the
column names

boo.append((df['HEI']>lb[i])&(df['HEI']\<=ub[i]))#forming
the boolean for each stack height class

d1.update({col_h[i+2]:Series(s_dum)})#filling with dumy list

a=DataFrame(d1)[np.array(col_h)] #construct the output data frame

for i in xrange(len(col_em)): #do loop in row-wise of output table

sp=col_em[i] #names of pollutants

b=sum(df[sp]) #sum of all stacks

l=[sum(df[boo[rnk]][sp])/b for rnk in xrange(len(lb))]#ratio of
each stack categories

l.insert(0,sum(df[sp])) #insert the sum of emission rate

l.insert(0,sp[:sp.index('_')] #only spnam (before and without
"_EMI")

print l

a.loc[i]=l #substitute the whole row as a batch

DataFrame(a).set_index('SP').to_csv('tpy_HEI.csv') #save the
file

上述2個範例前者是簡單地指定特定儲存格的內容，後者更為單純，是將某一列(row)的內容指向另一序列。基本上，df.loc()的引數有2個，第1是列數、第2是行數，如第1個範例所示，第1個引數是符合特定條件的某些列，以判別式(boolean)的型態撰寫(df_ln['name'].map(lambda
x:
x=='propenylcyclohexane'))，直言之，就是指name那一行中內容正好等於'propenylcyclohexane'的那一列，有關map()的使用會進一步說明，基本上是個序列經過特定函數的轉換與對照，此處的函數就是個判別式。至於第2個引數，範例中指向'CAS'該欄位。所以範例1的應用，就是找到'name'是'propenylcyclohexane'的那一列，再將'CAS'欄位的內容，改為字串'5364-83-0'。

第2個範例是一個統計不同煙囪高度排放量的小程式，輸入TEDS9.0的點源csv檔案，輸出為個別污染物的排放總量，以及各個煙囪高度排放量佔比的表格。

程式先以橫方向(column-wise)形成一個空白的表格，以及各個煙囪高度的判別式，再以縱方向(row-wise)按照各個污染物分別計算總量，以及符合前述判別式的總量比例。df.loc[i]在此的應用只有一個引數，因為搭配輸入的是一個與行數(索引)正好相等的序列，系統會自動替換掉該列(row)全部的內容。

綜合上述，由篩選條件所得到的結果，除了df.loc[i]之外，其餘都可能有好幾行或列的結果，其型態還是資料表，必須要特別用list或者set指定其型式，以方便取用其內容。

至於loc、iloc、ix、iat、at等指令的差異與應用，可以見stackoverflow網站的問題與答覆[^54]。

各欄位之間的排序範例、索引與轉置

一般在excel內作業時，倘若要讓資料表照所期待的方式排列，在垂直向(row-wised)可以用資料篩選功能，然而在橫方向(column-wised)則必須以手動的方式剪貼了。如以前述範例而言，要按照風向的順序來整理資料表，用手動剪貼方式處理16個風向的表格，不是一件容易的作業，即使運用轉置再排序的方式可以因應，但畢竟風向並不是照一定文字或數字方式排序，幾乎是不可能處理。以下為使用pandas的作業範例。只需要1行指令即完成排序。

...

wts_output=[wts[numBinWD-1]]+wts[:numBinWD-1] #output sequence,
0 for N

df=pd.DataFrame(d1)

cols=['intensity']+wts_output #due to no sequence in set, the
index must be made

df=[df[cols]]{.underline}.s*et_index('intensity').T

...

範例中因d1是一個序列dict的集合，而集合並不能指定順序，因此組成df資料表之後，在橫向(column-wise)也不會自動按照一定方式排好順序。

此時要先準備好序列cols，為一字串(dict的key)的序列，按照N、NEN、NE...NWW之順序，做為df橫向排序的目標。然後執行[df[cols]]{.underline}這一行指令即可排好順序。

此處要注意，plotly風玫瑰圖的設定是由北方開始畫圖，因此順序必須使用wts_output而不是原有的風向序列(wts)。在聯合頻率計算過程，風向是起始於NNE，風向度數16等分的第1份。方向起始於N，這是plotly風玫瑰圖的設定。

.set_index('intensity')指令的用意是取消原有的索引(index)[^55]，改用'intensity'(key)的內容做索引(items=its，見前述案例中的風速等級字串)做為index，以便轉置(transpose,
.T)之後直接就會變成新的key，而原來的風向(**cols**序列)則變成資料表最左邊新的索引(index)，可以用來繪製風玫瑰圖。

整理前、後的資料表如下所示，由原本17X9的矩陣變成了9X17，原本df自動會跟著索引，轉置後會變成新的key，必須要先拿掉，以intensity的內容為索引與新的key。

![](media/image8.png){width="3.1733333333333333in"
height="2.5386668853893264in"}![](media/image9.png){width="3.2in"
height="2.5280008748906386in"}

資料表的合併(merge)

整併2個資料表看來似乎是很簡單的動作，但在傳統程式設計中卻需要逐筆比較2個資料表的索引，確認之後將2個資料表的內容存成第3個資料表，對於只有第1或第2個資料內容的項目，另外還要建立處理的邏輯，例如填入空白值、或者指定的字元。如果要整併超過2個以上資料表，比對工作會增加很多。

相同筆數與順序

相對而言，pandas使用merge指令卻非常容易，如以下範例所示：

...

d1={'ymdhs':Series(ymdhsN),'NO2':Series(N)}

dataN=**DataFrame**(d1)

d2={'ymdhs':Series(ymdhsA),'NH3':Series(A)}

dataA=**DataFrame**(d2)

d3={'ymdhs':Series(ymdhsW),'WD':Series(WD)}

dataW=**DataFrame**(d3)

result=**merge**(dataA,dataN,**on=**['ymdhs']) #panda.merge

result2=**merge**(result,dataW,**on=**['ymdhs']) #panda.merge

...

第1\~2個引數分別是要整併的資料表，可以是不同長度，但是一定要有同樣的索引名稱，如範例中的'ymdhs'。如果要合併更多的資料表，只需要重複merge的動作，並把前次merge的結果加入成為merge的一個資料表即可。merge之後的橫向順序理論上是按照引數的順序，不論結果為何，如果要排列特定的順序，只要按照前述排序方式即可重組。各資料表與整併情形如下圖所示。

![](media/image10.png){width="1.3200010936132984in"
height="2.3146675415573053in"} ![](media/image11.png){width="1.24in"
height="2.2933333333333334in"}
![](media/image12.png){width="1.2266666666666666in"
height="2.2933333333333334in"}
![](media/image13.png){width="1.3466666666666667in"
height="2.2826673228346457in"} ![](media/image14.png){width="1.6in"
height="2.2933333333333334in"}

測試2個資料庫的長度與順序是否完全一致

如果2個要整併的資料庫df_s與df2pv，是按照各資料表中的'plant'欄位來進行整併，必須要確認

1.個別資料庫的索引已經先行整併過(例如利用pivot_table指令)，沒有重複的索引，若有，在2個資料庫整併時將不知要併到哪一個索引。經整併後的索引，其序列的長度與集合的長度是一致的。

print len(df_s['plant'])-len(set(df_s['plant']))

print len(df_2pv['plant'])-len(set(df_2pv['plant']))

(ans=)0 0

2.要保證2個索引的內容必須完全一致，此時可以利用python的集合功能，如果2個序列的集合相減為一空集合，則表示2個索引的內容完全相對

set(df_s['plant'])-set(df_2pv['plant'])

(ans=){}

3.排順序，可以使用DataFrame.sort_values的方法，括號內即為排序的樞紐軸，作法如下：

df_all=DataFrame(a).**sort_values**('plant_all')

修剪較多的資料(drop)

使用drop指令如下，首先用集合差找到2個資料庫索引差異的項目，再找出多出來的項目，從資料庫中將其刪除：

a=set(plant_s)-set(df_2pv['plant']) #drop the plant without COD
data

for i in a:

df_s.**drop**(df_s[df_s['plant']==i].index, inplace=True)

範例中的資料表df_s較df_2pv為大，多出來的項目即為a集合的內容。因此從資料表中找到該筆資料，令其為index，將其drop掉，同時設定為inplace即時進行改變，df_s將會被改變。

索引與選取(indexing)

Pandas的選取與修改方式有許做法，使用者可以參考網站[^56]上的說明自行測試。此處介紹boolean
indexing。

篩選若以資料的大小、數值或文字完全相等這類的邏輯，可以適用在以資料表、整欄為對象，可以用批次進行篩選。相對而言，有些邏輯條件是有針對性的，例如資料內容中的第幾個文字，這樣的條件就不能適用在序列、陣列或資料表，而是單一個別字串，就必須用迴圈方式逐一判別。

全面性適用與複合式邏輯

這類的邏輯條件直接下在dataframe的屬性之內，將內容直接呼叫出來。最常見的就是給定欄位名稱，將資料表的欄位呼叫出來，如：df_cat[u'業別']即是將資料表df_cat中欄位名稱符合u'業別'的欄位，給篩選出來。

#secondly, do the section

cat_nam=list(df_cat[u'業別'])

reg_nam=list(df_cat[u'工業區'])

(categ_s,plant_s)=([],[])

for c in cat_nam:

for r in reg_nam[0:2]: #other are blank (NaN)

#boolean for matching categories and regions

#categories with number must be skipped(already cut by previous step)

**boo=(*d*f_all['cat_all']==
c)&(*d*f_all['reg_all']==r) #multipled criteria**

l=list(df_all[**boo**]['cat_all'])

if len(l)>=1: #maybe no item at all

for p in set(list(df_all[boo]['plant_all'])):

boo=df_all['plant_all']==p

#store the first record is enough and only

categ_s.append(list(df_all[boo]['cat_all'])[0])

plant_s.append(p)

a={'plant':Series(plant_s),'category_selected':Series(categ_s)}

df_s=DataFrame(a).sort_values('plant') #sources with certain
categori

這個方法適用在條件較為複雜、資料量龐大的狀況。如範例中，要篩出的資料條件包括符合2個序列(序列df_all['cat_all']==
c**及**序列df_all['reg_all']==r)的所有資料，再將其中的2欄(plant_all及cat_all)組合成新的資料表。

複合條件中的連接方式，並不是用一般邏輯表述所使用的and,
or或not等關鍵字，而是用**&**
、**\|**、及\~之符號，而且必須用括號**(...)**將其分組。

式中df_all[boo]為符合boo條件的資料表，而再加上欄位名稱之呼叫['plant_all']，即為'plant_all'該欄位中所有符合篩選條件boo的序列。序列若還是有重複值，後續計算會造成重複加總，必須要去掉。此時只要取其集合即可消除重複值，因此篩出的工廠就變成：set(list(df_all[boo]['plant_all']))了。

而對應該工廠的類別(其序列為df_all[boo]['cat_all'])，只需要(也只能)記錄其第一筆(df_all[boo]['cat_all']**[0]**)，而略去其他重複值。

個別元素之迴圈判別

Python程式設計很簡潔，將字串也向量化處理，適用所有序列的處理規則，但在資料庫進行字串的篩選邏輯時，就會遭遇到困難，python無法分辨邏輯是針對整個序列的元素還是個別元素的文字序列。此時dataframe要借助迴圈處理之內設序列函數map[^57]。

boo=(df2[u'管制編號'].**map**(lambda x: x in plant_s )) #eg1

df2_s=df2[boo]

boo=(df2_s[u'申報區間(起)'].**map**(lambda x: '104' in x)) #eg2

df2_yr=df2_s[boo]

boo=df1[u'行業別'].**map**(lambda x: x[6:]==cat_nam) #eg3

傳統上map有2個引數，分別是回傳對照的數值函數，以及輸入輪迴的序列。但此處經由lambda的作用，資料庫將整個序列依序傳入map，map傳回的則是一個個邏輯判別的結果(固定的函數)，如eg1中x是否是集合plant_s的一員、eg2中'104'是否在字串x之中、eg3則是傳來的字串第6碼之後的字元與cat_nam完全相同，而不是序列中第6個之後的元素與cat_nam相同。

由於map已經是迴圈處理的函數了，因此不再需要(也不能)對序列再做迴圈。雖然eg1與eg2是2個同時存在的邏輯(and或&)，但是python不接受複合式的map操作，必須循序處理。

樞紐分析(pivot table)

Excel經常被用來做資料表的樞紐分析，按照某一指定欄位的內容，來整併其他欄位的數據，產出一濃縮的次級資料表格，可以是指定欄位的分項下，其他欄位的資料筆數、資料平均值、小計加總等等。這些作業往往因為資料表過於複雜，原始數據與中間成果交雜在同一資料表內，因而不容易處理。

對此一問題，python/pandas則顯示出其簡潔與強大之處。

print 'the water pollution sources in taiwan:'

print
**pivot_table**(df_all,index=["cat_all"],values=["reg_all"],aggfunc=**'count'**)

col_id=["C_NO","NO_S","SCC"]

col_na=["NO_P","COMP_NAM","COMP_KIND1","DICT_NO","EQ_1","EQ_2"]

df_pv4=pivot_table(df,index=col_id,values=col_na,aggfunc=mostfreqword)

此處前1個範例，是計算事業廢水污染源的家數與行業別的關係，後者是固定污染源管制編號("C_NO"代表某一家工廠)、污染排放口("NO_S"可能有許多不同製程的廢氣導入)、以及各污染製程的分類碼("SCC")的分組樞紐分析。各輸入參數說明如下：

母體資料結構(資料表)

如前述2個範例中的df_all或者是df都是完整的資料表，有數據欄位，有指標欄位，可能由別的欄位或序號做為指標(index)都無關緊要。所謂的樞紐分析就是以特定的某一欄位(或某些欄位)為分組的依據，進行分組的計算。在進行pivot_table時將暫時改以該(等)欄位作為指標，如下所示。

指標欄位

以index=["欄位名稱"...)]序列方式指定，因為是序列，若指標欄位數大於1時，其順序就有其意義，依續是大類、中類、與細類的分類依據。因此在第2個範例中，系統將會按照工廠別、污染源、以及SCC等大、中、小類進行分組，若是相反或有其他順序，則有不同的意義。

資料欄位

以values=["欄位名稱"...)]序列方式指定，因為個別資料欄只與指標欄的分組方式有關，與其他資料欄位並沒有關係，因此其順序在DataFrame的結構中是不具有意義的。

資料可以是任何型式，數據或文字皆可，只要能符合後續要處理的函數型態即可。

合併的函數

以aggfunc='...'型式指定同一組類別內所要進行整合的方式，可以是'count'進行筆數計算，或者是numpy.mean、numpy.sum等進行平均或加總，第2個範例另外寫一個副程式[^58]，進行同一組內最頻字之計算，以選擇具代表性的文字。此副程式內容如下，在pivot_table呼叫時直接指定函數名稱即可，不必指定引數(即為values之各欄位資料)，也不必加上空括號()：

def **compareItems**((w1,c1), (w2,c2)):

if c1 > c2:

return - 1

elif c1 == c2:

return cmp(w1, w2)

else:

return 1

def **mostfreqword**(list_of_w):

counts = {}

for w in list_of_w:

counts[w] = counts.get(w,0) + 1

it=counts.items()

it.sort(**compareItems**)

return it[0][0]

習題

統計分析

相關係數

此處介紹模式性能評估之相關係數計算過程，並與性能目標值進行比較。應用包括pandas,
numpy與argparse等模組。

第一段(藍底部分)為模組之宣告與檔名定義。

from pandas import *

import numpy

import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-f", "\--csv_filename", required = True,
type=str,help = "aok csv")

args = vars(ap.parse_args())

fname=args['csv_filename']

fnameO='CCR'+fname[3:]

第二段(綠底部分)讀進表格，並定義欄位名稱。由於模擬結果可能沒有表頭(不同年代結果)，還是需要給定欄位名稱比較方便處理。一般預設是逐時的模擬比較表，然而程式也會判斷是否是逐日的日均值

df0=read_csv(fname) #with head

if df0.columns[0] !='ID':

df0.columns=['ID','NAME','JuliHr','CalDat','TMP','SO2','CMO','OZN','PMT',
\\

'NOX','P25','NO2','THC','NMH','WSP','WDR','TMP','SO2','CMO','OZN','PMT',
\\

'NOX','P25','NO2','NMH','THC','WSP','WDR']

nm=[i[0:4] for i in set(list(df0['NAME']))]

nm.append('all')

nm_ful=[i for i in set(list(df0['NAME']))]

pp=[5,7,8,10,11,13]

ps=[0.35,0.45,0.35,0.35,0.35,0.35] #hrly standard,PM/PM2.5 not used

if 'ovd' in fname:

ps=[0.45,0.45,0.55,0.55,0.45,0.45]#daily standard, O3 not used

pn=[df0.columns[isp] for isp in pp]

d={'NAME':nm}

第一段(藍底部分)為模組之宣告與檔名定義。

for isp in pp:

sp=df0.columns[isp]

rr_st=[]

for st in nm_ful:

boo=(df0['NAME']==st) & (df0[sp]>0)

df=df0[boo]

ccr=0

if len(set(list(df[sp])))>1:

try:

ccr=numpy.corrcoef(list(df[sp]),list(df[sp+'.1']))[0,1]

except:

ccr=0.

rr_st.append(ccr)

if len(set(list(df0[sp])))>1:

try:

ccr=numpy.corrcoef(list(df0[sp]),list(df0[sp+'.1']))[0,1]

except:

ccr=0.

rr_st.append(ccr)

d.update({sp:rr_st})

df_r=DataFrame(d)

for isp in xrange(len(pp)):

df_r[pn[isp]+'_ex']=map(lambda x: 1 if x>=ps[isp] else 0,
list(df_r[pn[isp]]))

df_r['NAME']=nm

pn2=['NAME']

for i in pn:

pn2.append(i)

pn2.append(i+'_ex')

df_r[pn2].to_csv(fnameO)

print fname

print 'SPE:attainment rate(%)'

for i in pn:

print i,sum(list(df_r[i+'_ex']))*100./len(df_r)

時間

Python的時間模組非常強大，以往fortran複雜的計算邏輯，在python的datetime模組都可輕鬆處理。

calendar

以往的星期與月份名稱必須打成一個對照表，這在calendar中為內設程式，如'day_name',
'day_abbr', 'month_abbr', 'month_name'等：

for i in xrange(1,13):

print calendar.month_name[i], calendar.month_name[i][:3]

潤年測試、計數也比較簡潔：

calendar.isleap(2019)

Out[56]: False

calendar.isleap(2020)

Out[57]: True

In[60]: calendar.leapdays(2000,2020)

Out[60]: 5

還有星期幾的判定：

calendar.weekday(2019,8,12)

Out[66]: 0

calendar.day_name[calendar.weekday(2019,8,12)]

Out[67]: 'Monday'

其指令都較為簡單。calendar還可以寫成html格式以供掛網[^59]。

datetime

Julian date

這裡的juldate是指以當年度1月1日起算的日數，因為遇到潤年日數會加1，跨年的日數要重算等等問題。jjj
也可以直接從日期差值取.days而得。（jjj =
(ldate-jan01).days，.days之結果為整數，不必再取int()。

ldate = datetime.datetime(int(yr), int(mm), int(dd))

jan01= datetime.datetime(int(yr), 1, 1)

if ldate==jan01:

jjj=1

else:

jjj=int(str(ldate-jan01).split('day')[0])+1

第三種作法是利用.strftime('%Y%j')的格式轉換技巧，將日期轉成Julian
date的文字格式，再轉成整數即可加減計算。

datetime.datetime(2019,12,25).strftime('%Y%j')

結果='2019359'

3.  Gregoria date

Gregoria date也有人稱為Julian
date，其定義是自公元1年1月1日開始起算的日數，可以順利解決跨年、閏年的問題，Mozart
模式輸出檔的time即為Gregoria date，可以按照定義計算如下：

gdate = (datetime.datetime(int(yr), int(mm),
int(dd))-datetime.datetime(int(yr), 1, 1)).days + 1

[(datetime.datetime(2015,m,1)+datetime.timedelta(days=d)).toordinal()
for d in range(31)]})

toordinal()也有取Gregoria date的效果。

1.  使用bash的date指令

Bash
的date指令不但能用來轉換日期時間的格式，也可以做簡單的加減，計算昨天、明天的日期：

set START_DATE = "2010-05-02" #> beginning date (May 1, 2010)

set END_DATE = "2010-05-02" #> ending date (June 30, 2010)

set TODAYJ = \`date -ud "${START_DATE}" +%Y%j\` #> Convert
YYYY-MM-DD to YYYYJJJ

set STOP_DAY = \`date -ud "${END_DATE}" +%Y%j\` #> Convert
YYYY-MM-DD to YYYYJJJ

while ($TODAYJ \<= $STOP_DAY ) #>Compare dates in terms of YYYYJJJ

set YYYYMMDD = \`date -ud "${TODAYG}" +%Y%m%d\` #> Convert
YYYY-MM-DD to YYYYMMDD

set YYYYMM = \`date -ud "${TODAYG}" +%Y%m\` #> Convert YYYY-MM-DD
to YYYYMM

set YYMMDD = \`date -ud "${TODAYG}" +%y%m%d\` #> Convert YYYY-MM-DD
to YYMMDD

set YESTERDAY = \`date -ud "${TODAYG}**-1days**" +%Y%m%d\` #>
Convert YYYY-MM-DD to YYYYJJJ

set TODAYG = \`date -ud "${TODAYG}**+1days**" +%Y-%m-%d\` #> Add a
day for tomorrow

set TODAYJ = \`date -ud "${TODAYG}" +%Y%j\` #> Convert YYYY-MM-DD
to YYYYJJJ

set day = \`date -ud "${day}+1days" +%Y-%m-%d\`

OSX的date作法略有不同：

set STD_YMD = \`date -j -f "%Y-%m-%d" "${START_DATE}" +%Y%m%d\`
#> Convert YYYY-MM-DD to YYYYMMDD

setenv EXECUTION_ID "CMAQ_CCTM${VRSN}_\`id -u -n\`_\`date -u
+%Y%m%d_%H%M%S_%N\`" #> Inform IO/API of the Execution ID

set TODAYJ = \`date -j -f "%Y-%m-%d" "${START_DATE}" "+%Y%j"\`
#> Convert YYYY-MM-DD to YYYYJJJ

set STOP_DAY = \`date -j -f "%Y-%m-%d" "${END_DATE}" "+%Y%j"\`
#> Convert YYYY-MM-DD to YYYYJJJ

while ($TODAYJ \<= $STOP_DAY ) #>Compare dates in terms of YYYYJJJ

set YYYYMMDD = \`date -j -f "%Y-%m-%d" "${TODAYG}" +%Y%m%d\` #>
Convert YYYY-MM-DD to YYYYMMDD

set YYYYMM = \`date -j -f "%Y-%m-%d" "${TODAYG}" +%Y%m\` #>
Convert YYYY-MM-DD to YYYYMM

set YYMMDD = \`date -j -f "%Y-%m-%d" "${TODAYG}" +%y%m%d\` #>
Convert YYYY-MM-DD to YYMMDD

set YESTERDAY = \`date -v**-1d** -j -f "%Y-%m-%d" "${TODAYG}"
+%Y%m%d\` #> Convert YYYY-MM-DD to YYYYJJJ

set TODAYG = \`date -v**+1d** -j -f "%Y-%m-%d" "${TODAYG}"
"+%Y-%m-%d"\` #> Add a day for tomorrow

set TODAYJ = \`date -j -f "%Y-%m-%d" "${TODAYG}" "+%Y%j"\` #>
Convert YYYY-MM-DD to YYYYJJJ

set day = \`date -v+1d -j -f "%Y-%m-%d" "${day}" +%Y-%m-%d\`

重要共用格式與軟體之建置

除了前述以對話窗執行得到結果的方式之外，使用者也會需要從檔案讀進真實世界的數據資料，或將程式結果寫成檔案，以利與別的軟體程式進行串接。

一般檔案

文字檔案

Python有許多內建讀取程式，可以輕鬆讀取複雜的資料格式，包括以空白、逗號、tab鍵等分格的資料檔案。

ISCST直角座標網格輸出檔為fortran產生的格式，以空白格開各欄數據，以下為讀取的Python程式作為說明範例：

ISCST3的網格設定

模擬範圍為25 x
60格，間距500M的網格系統，年平均地面濃度輸出檔名為SAL.yr，以下為部分輸入檔之設定值：

RE GRIDCART CG1 STA

XYINC 172000. **25** 500. 2615000. **60** **500**.

RE GRIDCART CG1 END

...

OU PLOTFILE PERIOD ALL SAL.yr

模擬結果檔案範例如下：

* ISCST3 (96113): YUNLIN INDUSTRIAL PARK AIR QUALITY ASSESSMENT - SO2

* MODELING OPTIONS USED:

* CONC URBAN FLAT DFAULT

* PLOT FILE OF PERIOD VALUES FOR SOURCE GROUP: ALL

* FOR A TOTAL OF 1500 RECEPTORS.

* FORMAT: (3(1X,F13.5),1X,F8.2,2X,A6,2X,A8,2X,I8,2X,A8)

* X Y AVERAGE CONC ZELEV AVE GRP NUM HRS NET ID

* ___________ ___________ ___________
______ ______ ________ ________
________

172000.00000 2615000.00000 [1.04605]{.underline} 0.00 PERIOD ALL
8760 CG1

172500.00000 2615000.00000 [0.94170]{.underline} 0.00 PERIOD ALL
8760 CG1

...

183500.00000 2644500.00000 0.37734 0.00 PERIOD ALL 8760 CG1

184000.00000 2644500.00000 [0.39325]{.underline} 0.00 PERIOD ALL
8760 CG1

此檔案讀取重點在第9行以後，前3欄數據，其餘在製圖時並不需要。

Python讀取程式範例

傳統fortran須按照格式(FORMAT:
(3(1X,F13.5),1X,F8.2,2X,A6,2X,A8,2X,I8,2X,A8))輸入，且須指定輸入筆數(1500)，python則較為靈活(pp5.py)：

import numpy

**(nx,ny,** delx**)=(25,60,0.500) #用tuple方式可以一次設定所有的參數**

(datz,datx,daty)=([],[],[]) #空白的list準備裝資料

fname='SAL.yr' 要讀取的檔案名稱

with open(fname) as ftext: 開啟檔案，直到讀完為止。

for i in xrange(**8**): ISCST3會寫**8**行表頭，因此須先跳過**0\~7**共8行

id = ftext.**[readline]{.underline}**()

for line in ftext: 剩下所有的行數

k=1 用k控制欄位，避免讀到文字無法轉換

for s in line.**[split]{.underline}**(): 內設是空白做間隔，予以切分資料

if k == 1: datx.append(float(s)) x值→裝進list

if k == 2: daty.append(float(s)) y值→裝進list

if k == 3: datz.append(float(s)) z值→裝進list

k=k+1

datx=numpy.array(datx) #list轉成array，numpy才可以作用

daty=numpy.array(daty)

datz=numpy.array(datz)

datz=datz.reshape(ny,nx)

#存成SURFER GRD檔，套疊GIS地圖，詳見後續說明。

from save_surfer import save_surfer

fname='pp5.grd' #必須先有一空白檔案

mnx=numpy.min(datx) #必須是公尺

mny=numpy.min(daty)

save_surfer(fname,nx,ny,mnx,mny,delx*1000.,datz.reshape(nx*ny))

注意事項：

在此應用了2個內設函數readline()及split()。

ISCST3輸出檔的2維排序與一般(如plotly
contour)排序不同，與SURFER一致，須特別注意。

numpy array在矩陣維度轉換(reshape)時，有較強大的功能。

有網友提出，python程式最好不要出現read這麼直接的用法。因此程式還可以這樣改：

fname='SAL.yr' 要讀取的檔案名稱

iskip=0

**with open(fname) as ftext:**

for line in ftext:**

if iskip >= 8:

k=1

for s in line.split():

if k == 1: datx.append(float(s))

if k == 2: daty.append(float(s))

if k == 3: datz.append(float(s))

k=k+1

iskip=iskip+1

datx=numpy.array(datx)

...

more pp5.grd結果如下

DSAA

25 60

172000 184000

2615000 2644500

1.785599999999999965e-01 1.357217999999999947e+01

[1.046049999999999924e+00]{.underline}
[9.416999999999999815e-01]{.underline} 8.540699999999999958e-01
8.13760000000000038

9e-01 8.032200000000000450e-01 7.877600000000000158e-01
7.970000000000000417e-01 8.31010000000

...

00000377e-01 4.445799999999999752e-01 3.773400000000000087e-01
[3.932499999999999885e-01]{.underline}

以Tab 分隔檔案之讀取(pandas.read_csv)

基本上tab是許多種分隔方式之一，可以使用line.split('\\t')指令讀取，也可以直接用pandas的指令read_csv直接讀成資料表(dataframe資料框架)，可以運用pandas指令來篩選。

以下範例wind.txt為風速(命名為intense)、風向(命名為orient)聯合頻率檔案，讀入後進行篩選與累加(運用numpy.cumsum)，累加最後結果就是100%。

from numpy import *

from pandas import *

wind_df = **[read_csv]{.underline}**('wind.txt', index_col=0,
sep='\\t') **#讀取檔案**

orient = list(wind_df.columns)

intense = list(wind_df.index)

wind_bins_df = wind_df.stack()

wind_bins_df = wind_bins_df.reset_index()

wind_bins_df.columns = ['intensity', 'direction', 'freq']

(m,n)=(len(intense),len(orient))

cum=array(m*[n*[0.0]]) **#必須要是array否則順序很容易亂掉**

freq=cum

for i in xrange(m):

ff=wind_bins_df[wind_bins_df['intensity']==intense[i]]
**#篩選、降階**

freq**[i,:]**=list(ff['freq']*100) **#篩選、轉成list**

for j in xrange(n):

cum[:,j]=cumsum(freq**[:,j]**) **#2維陣列的設定方式**

x=cumsum(cum[m-1,:]) **#numpy累加函數**

print x[n-1] **#ANS= 99.8033329**

讀取固定格式之數據檔案成為矩陣

傳統電腦數據檔案為節省空間，設計成「固定格式」，而表頭、變數名稱與順序等，則以程式控制。以下以ISCST3氣象檔案為例說明：

99999 92 99999 92

92 1 1 1 181.2000 1.0000 290.2 5 100.0 100.0

92 1 1 2 182.2000 1.1000 290.2 5 100.0 100.0

92 1 1 3 186.3000 3.1500 290.2 5 110.0 110.0

...

92 1 1 9 298.5000 4.2500 291.8 4 300.0 300.0

92 1 110 225.0000 2.5000 291.8 3 300.0 300.0

...

92 93024 201.8000 4.9000 297.2 5 100.0 100.0

9210 1 1 209.5000 4.3000 297.2 5 100.0 100.0

...

92123123 196.8000 6.5000 290.9 5 100.0 100.0

92123124 199.0000 5.6000 290.9 5 100.0 100.0

表頭為測站編碼與年代，地面及高空測站重複2次。其後為逐時的數據，一般是每小時，依序為年、月、日、時、氣溫(0.1C)、風速(m/s)、風向(去向deg)、穩定度及混合層高度(m)。用fortran的格式定義方式為(4I2,2F9.4,F6.1,I2,2F7.1)。

困難在於前面時間有些有空格未補0，字是連在一起的，其他變數還可以用空白格開。解釋方式：前者必須用「字元」觀念來讀入，補上空白，再轉成時間(整數)。後者則可以line.split()指令來隔開。

在python中字元、list的順序定義與標記方式是一致的，可以用[
]指定特定序位的字元。

fname='METR.DAT'

(cdate_time,temp,ws,wd,mixh)=([],[],[],[],[])
**#由空的序列開始**

with open(fname) as ftext:

id = ftext.readline() **#跳開第一行表頭**

for line in ftext:

tm=0 **#開始累加計算時間**

for i in xrange(0,8,2): **#年月日時共執行4次**

tm=tm*100+int(line[i:i+2]) **#前次結果X100 填上'0'了**

cdate_time.append(tm)

dat=[]

for s in line[**8:**].**split()**:dat.append(float(s))
**#剩下部份用空白格開**

temp.append(dat[0])

ws.append(dat[1])

wd.append(dat[2])

mixh.append(dat[4])

for i in xrange(3):

print cdate_time[i],temp[i],ws[i],wd[i],mixh[i]

from numpy import *

matrx=**row_stack**((cdate_time,temp,ws,wd,mixh))
**#沿著row方向堆疊，增加直排數**

print matrx.shape **#印出dimension**

答案是：

92010101 181.2 1.0 290.2 100.0

92010102 182.2 1.1 290.2 100.0

92010103 186.3 3.15 290.2 110.0

(5L, 8760L)

很顯然python在解讀「固定格式」的報表檔案十分吃力，還不如傳統fortran簡潔。然而由於「固定格式」的作法純粹是配合早期印表機字形大小完全一致的結果，除了減省列印的空間之外，特定變數也會出現在報表的特定位置，利於當時工程師閱讀報表。現代印表機的字形不見得有一樣的寬度(如0與1)，因此「固定格式」完全沒有必要了。

將向量堆疊成矩陣，在python就只有一行指令numpy.row_stack()。

二進位(binary)檔案

暫存檔.npy

二進位檔可以大幅減少檔案的體積，但是讀寫都必須小心規範其格式(順序及內容)一般用在暫存檔使用，Python.numpy有.npy與.npz兩種格式，以下為npy的範例。

>>> from tempfile import TemporaryFile

>>> outfile = TemporaryFile()

>>> x = np.arange(10)

>>> np.save(outfile, x)

>>> outfile.seek(0) *# Only needed here to simulate closing &
reopening file*

>>> np.load(outfile)

array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

npz雖然壓縮程度不如npy但是可儲存多個陣列，並存記變數名稱，有其較強大功能之處。

>>> from tempfile import TemporaryFile

>>> outfile = TemporaryFile()

>>> x = np.arange(10)

>>> y = np.sin(x)

Using savez with *args, the arrays are saved with default names.

>>>

>>> np.savez(outfile, x, y)

>>> outfile.seek(0) # Only needed here to simulate closing &
reopening file

>>> npzfile = np.load(outfile)

>>> npzfile.files

['arr_1', 'arr_0']

>>> npzfile['arr_0']

array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

Using savez with **kwds, the arrays are saved with the keyword names.

>>>

>>> outfile = TemporaryFile()

>>> np.savez(outfile, x=x, y=y)

>>> outfile.seek(0)

>>> npzfile = np.load(outfile)

>>> npzfile.files

['y', 'x']

>>> npzfile['x']

array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

Numpy.fromfile

寫入檔案可以用write與byearray函式，也可以用numpy的tofile指令更簡潔：

fn=open('pal.sa.receptor.bin','wb')

fn.write(bytearray(conc))

fn.close()

filename='pal.sa.receptor.bin2'

conc.tofile(filename)

os.system('diff pal.sa.receptor.bin pal.sa.receptor.bin2')

讀取時，因為不知道要讀取的檔案內容形態與陣列大小，因此必須在程式內予以指定，此時用numpy的fromfile比較順暢。

filename='pal.sa.receptor.bin2'

cnc=np.array(np.fromfile(filename,
dtype=dt).reshape(240,70,10,83),dtype=float)

(conc==cnc).all()

Excel格式

Excel雖然有其強大之處，然而其處理過程是以儲存格方式記錄公式(formula)，沒有完整的過程紀錄，即使有visual
basic語言可以記下處理聚集的細節，但畢竟並不容易閱讀，也不容易在不同軟體中做交流(剪貼)並做必要的修改。

因此最好還是將其資料讀出來後，以python進行處理，若有必要再存回excel進一步處理、甚至也可以應用excel的繪圖功能，以批次方式產生excel圖表。

python-excel平台

目前已經有使用者平台[^60]，專注在以python處理excel檔案的相關問題，介紹常用的第三方套件與付費軟體。前者如：

openpyxl[^61]：讀寫Excel 2010
.xlsx檔，可以運用python的numpy及pandas(官方資料處理程式庫)進行資料處理，為目前最廣為使用的excel程式庫。

xlsxwriter[^62]：位階類似Excel的VBA功能，以python製做excel圖檔，儲存成xlsx檔再利用Excel輸出。也可以運用python的pandas以及Excel
VBA聚集功能，因此非常適合龐大且具繪圖品質要求的專案。

xlrd/xlwt：舊版本Excel檔案(ie: .xls)

xlutils：綜合xlrd/ xlwt與其他功能的python工具，皆包括在openpyxl內。

經評估，乃以建置openpyxl較為實用。

矩陣儲存至excel檔

上接3.1.3讀取固定格式之氣象數據檔案成為矩陣，以下試將寫成excel
檔案，可以呼叫excel內設功能或繪圖：

from openpyxl import Workbook

wb = Workbook()

ws1 = wb.active

s=['datetime','temp','ws','wd','mixh']

ws1.append(s)

print ws1['d1'].value,cdate_time[0]

for i in xrange(matrx.shape[1]):

s=list(matrx[:,i])

ws1.append(s)

a=ws1['b3'].value

print a

wb.save("metr.xlsx")

![](media/image15.png){width="5.796000656167979in"
height="4.34700021872266in"}

繪圖範例：利用excel繪製bar chart

>>> from openpyxl import Workbook

>>> wb = Workbook()

>>> ws = wb.active

>>> for i in range(10):

\... ws.append([i])

>>>

>>> from openpyxl.chart import BarChart, Reference, Series

>>> values = Reference(ws, min_col=1, min_row=1, max_col=1,
max_row=10)

>>> chart = BarChart()

>>> chart.add_data(values)

>>> ws.add_chart(chart, "E15")

>>> wb.save("SampleChart.xlsx")

與統計程式庫結合使用

範例一xls檔案讀成DataFrame

對於已經整理好的excel表格，讀成DataFrame只需要一行指令：

df=read_excel(fname)

然而若是第一行不正好就是欄位名稱，或者需要別的調整，就不是那麼方便了，以下整理過程也許可以作為參考：

![](media/image16.png){width="5.800001093613298in" height="4.64in"}

fname='SCC_Codes.xlsx'

from openpyxl import Workbook, load_workbook

from itertools import islice

wb= load_workbook(fname,data_only='true')

ws=wb['SCC Codes']

data = ws.values

cols = next(data)[1:]

data = list(data)

idx = [r[0] for r in data]

data = (islice(r, 1, None) for r in data)

df_scc = DataFrame(data, index=idx, columns=cols)

範例二

健康風險評估程序中，須求取所謂的信賴區間，並對模擬的變數用適當的分布型態予以擬合，以檢討結果的合理性。以下範例將excel檔案中的B欄讀出，用log
normal分布擬合，再繪出擬合後分布的圖形。

import numpy as np

import matplotlib.pyplot as plt

from openpyxl import Workbook, load_workbook

wb2= load_workbook('IWWM.xlsx')

ws=wb2['2006']

B=[0]*2

for i in xrange(2,27):

B.append(ws.cell(row=i, column=2).value)

br=np.array(B[2:27]) #min() and max() only applied to array, not list

bins=np.linspace(min(br),max(br),20) #define the x-axis for histogram
plot

plt.hist(br, bins, alpha=0.2) #plot the histogram

plt.title("B Histogram")

plt.xlabel("B")

plt.ylabel("Frequency")

fig = plt.gcf() #get the current figure

from scipy import stats

shape, loc, scale = stats.lognorm.fit(B[2:26], floc=0) #以lognormal
擬合

sigma = shape

mu = math.log(scale) #mean

ran_p=np.random.random(10000) #rv from 0 to 1, as the probabilities

#generate the value of designated prob.

B_q = stats.lognorm.ppf(ran_p, [sigma], scale=scale)

br=np.array(B_q)

bins=np.linspace(min(br),max(br),100)

plt.hist(B_q, bins, alpha=0.2)

plt.title("B Histogram")

plt.xlabel("B")

plt.ylabel("Frequency")

fig = plt.gcf()

plt.show()

plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram') #plot
on the website

TIFF(Tagged Image File Format)格式

TIFF為靈活的點陣圖格式，主要用來儲存包括相片和藝術圖在內的圖像[^63]。環境與地球科學方面亦有不少處理照片的機會，例如土地使用在空氣污染與氣象的模擬過程中是非常重要的參數，如何從航空攝影或其他結果照片，讀取結果、進而辨識其土地利用型態而予以正確分類，為一必要之程序。

LU_nowadays, reading from CTCI_LU, others LU's

Surfer .grd (GIS raster)格式

一般模式輸出檔案已經是網格化之數據資料，即可應用軟體進行繪圖，不需要內、外插(或整併)成網格化的資料格式，僅須按照軟體要求的格式進行資料檔案轉換。

Surfer是Golden
Software的產品，經常用在網格資料繪製等值線圖(contour)或者是色塊圖(shaded
contour or raster
plot)，是地球科學與環境方面常用的軟體，其輸入檔的附加名稱約定為.grd。因此其檔案格式也經常是程式撰寫的重點。

fortran 版本

grd (GIS raster)格式範例

基本上，ASCII版本的.grd檔，前五行為表頭，其後為網格資料如：

```bash
DSAA(SURFER researved command)
83 137(nx, ny)
133916.9 379916.9(xmin, xmax, 不含最後一格的間距)
2407522\. 2815522.(ymin,ymax不含最後一格的間距)
0.0000000E+00 1.000000(cmin, cmax)
1.0000 1.0000 1.0000 1.0000 1.0000 1.0000 1.0000 1.0000 1.0000 1.0000
1.0000 1.0000 1.0000 1.0000 1.0000 1.0000 1.0000 1.0000 1.0000 1.0000
...
```

### fortran程式碼

資料排列方式為自圖面左下(西南)角開始，每行10個值，做第一個維度的迴圈，空一行之後再做第2維度的迴圈。如下：

```fortran
DO 221 J=1,nj
	DO 221 I=1,ni
		SCR(JJ)=a(i,j)
		CMIN=AMIN1(CMIN,SCR(JJ))
		CMAX=AMAX1(CMAX,SCR(JJ))
		JJ=JJ+1
221 CONTINUE

WRITE(n,'(a4)')'DSAA'
WRITE(n,*)NI,NJ
WRITE(n,*)XORG,XUTM !dot in grid
WRITE(n,*)YORG,YUTM
WRITE(n,*)CMIN,CMAX

I1=NI/10+1
I2=MOD(NI,10)
IF(I2.EQ.0)I1=I1-1
DO 2 J=1,NJ
	DO 3 KK=1,I1
		K2=K1+9
		IF(KK.EQ.I1.AND.I2.NE.0) K2=K1+I2-1
		WRITE(N,101)(SCR(I),I=K1,K2)
	4 K1=K2+1
	3 CONTINUE
	WRITE(N,*)
2 CONTINUE
101 FORMAT(1x,10(1PG13.5E3))
```

python版本

python程式碼

以副程式型式撰寫，以便於其他主程式可以import。整體而言，python程式較為簡潔：

```python
import numpy #應用numpy的 min/max/savetxt
def save_surfer(fname,nx,ny,x0,y0,delx,grd): #由主程式供應這些條件
	xn=(nx-1)*delx+x0 #x方向的極大值(不含最末格間距)
	yn=(ny-1)*delx+y0 #y方向的極大值(不含最末格間距)
	cmin=numpy.min(grd)
	cmax=numpy.**max(grd)
[output=('DSAA\\n',(nx,ny),(x0,xn),(y0,yn),(cmin,cmax),grd)
#tuple方便coding]{.underline}
fo=open(fname,'rw+') #開啟檔案
fo.write(output[0]) #寫檔頭
for i in range(1,4): #寫整數
numpy.savetxt(fo,numpy.array(output[i]).reshape(1,-1),fmt='%i')
for i in range(4,6): #寫cmin,cmax及資料(實數)
numpy.savetxt(fo,numpy.array(output[i]).reshape(1,-1))
fo.close()
return
```
結果範例

Python程式寫出結果如下，由於savetxt沒有(不需)指定格式，可讀性較低。注意：若要套GIS地圖，x0及y0的單位必須是公尺。一般選擇TWD
97 TM2 zone 121。

DSAA

83 137

133916 379916

2407522 2815522

1.000000000000000000e+00 6.000000000000000000e+00

6.000000000000000000e+00 6.000000000000000000e+00
6.000000000000000000e+00 6.000000000000000000e+00
6.000000000000000000e+00 6.000000000000000000e+00
6.000000000000000000e+00 6.000000000000000000e+00
6.000000000000000000e+00 6.00000...

python讀取程式

讀取程式必須按照來源檔案的格式進行研判，選擇適用的方式讀取，因此較為複雜，可以參考網友公開的程式[^64]，或使用Steno3d的程式[^65]與服務，可以讀取surfer
7的binary 檔[^66]。

讀取程式詳下：
```python
kuang@master /home/sespub/flare/GX_epb
$ cat \~/bin/load_surfer.py
import numpy
def load_surfer(fname, fmt='ascii'):
"""
Read a Surfer grid file and return three 1d numpy arrays and the grid
shape
Surfer is a contouring, gridding and surface mapping software
from GoldenSoftware. The names and logos for Surfer and Golden
Software are registered trademarks of Golden Software, Inc.
http://www.goldensoftware.com/products/surfer
According to Surfer structure, x and y are horizontal and vertical
screen-based coordinates respectively. If the grid is in geographic
coordinates, x will be longitude and y latitude. If the coordinates
are cartesian, x will be the easting and y the norting coordinates.
WARNING: This is opposite to the convention used for Fatiando.
See io_surfer.py in cookbook.
Parameters:
* fname : str
Name of the Surfer grid file
* fmt : str
File type, can be 'ascii' or 'binary'
Returns:
* x : 1d-array
Value of the horizontal coordinate of each grid point.
* y : 1d-array
Value of the vertical coordinate of each grid point.
* grd : 1d-array
Values of the field in each grid point. Field can be for example
topography, gravity anomaly etc
* shape : tuple = (ny, nx)
The number of points in the vertical and horizontal grid dimensions,
respectively
"""
assert fmt in ['ascii', 'binary'], "Invalid grid format '%s'.
Should be \\
'ascii' or 'binary'." % (fmt)
if fmt == 'ascii':
# Surfer ASCII grid structure

# DSAA Surfer ASCII GRD ID

# nCols nRows number of columns and rows

# xMin xMax X min max

# yMin yMax Y min max

# zMin zMax Z min max

# z11 z21 z31 \... List of Z values

with open(fname) as ftext:

# DSAA is a Surfer ASCII GRD ID

id = ftext.readline()

# Read the number of columns (nx) and rows (ny)

nx, ny = [int(s) for s in ftext.readline().split()]

# Read the min/max value of x (columns/longitue)

xmin, xmax = [float(s) for s in ftext.readline().split()]

# Read the min/max value of y(rows/latitude)

ymin, ymax = [float(s) for s in ftext.readline().split()]

# Read the min/max value of grd

zmin, zmax = [float(s) for s in ftext.readline().split()]

data = numpy.fromiter((float(i) for line in ftext for i in

line.split()), dtype='f')

grd = numpy.ma.masked_greater_equal(data, 1.70141e+38)

# Create x and y numpy arrays

x = numpy.linspace(xmin, xmax, nx)

y = numpy.linspace(ymin, ymax, ny)

x, y = [tmp.ravel() for tmp in numpy.meshgrid(x, y)]

if len(grd) > nx*ny:

print 'grd length not match, len(grd)=',len(grd),'(nx,ny)=',nx,ny

tmp,xtmp,ytmp=[],[],[]

for i in xrange(nx*ny):

tmp.append(grd[i])

xtmp.append(x[i])

ytmp.append(y[i])

x=numpy.array(xtmp)

y=numpy.array(ytmp)

grd=numpy.array(tmp)

# x=x.reshape(ny,-1)

# y=y.reshape(ny,-1)

# grd=grd.reshape(ny,-1)

if fmt == 'binary':

raise NotImplementedError(

"Binary file support is not implemented yet.")

return x, y, grd, (ny,nx)
```

### python在KML格式檔案之應用

### KML格式與用途

KML(Keyhole Markup Language)及其zip後的檔案格式KMZ，是google map/google
earth平台上特有的檔案格式，詳細介紹可以參考官網[^67]及網友[^68]的說明。

大致上KML語法和html相同，除了一般性的格式之外，在地圖上標示的元件以\<Placemark>...\</Placemark>做為起迄標示。而在本作業中乃是以Polygon(shaded色塊)為繪圖形式，此外KML也有Line、Path、Point等形態。

Google Map貼座標點

Point的圖像(icon)可以由網路上找到典型範例，如下紅色尖尾標，其他也有白色範例[^69]，


```python
kuang@master /home/sespub/flare/GX_epb
$ cat csv2kml.py
from pandas import *
import twd97,json
with open('/home/cpuff/2013/ptem/cno_name.json','r') as f:
	cno2name=json.load(f)
def nstnam():
	import json
	fn=open('/home/backup/data/epa/pys/sta_list.json')
	d_nstnam=json.load(fn)
	d_namnst = {v: k for k, v in d_nstnam.iteritems()}
	return (d_nstnam,d_namnst)
(d_nstnam,d_namnst)=nstnam()
a=read_csv('cno_XY.csv')
head0='\<?xml version="1.0" encoding="UTF-8"?>\<kml
xmlns="http://www.opengis.net/kml/2.2">\<Document>'+ \\
'\<name>Flares and AQ stations</name><description>GaoXiong Flares
and AQ stations</description>'
line=[head0]
stylH='<Style id="highlightPlacemark"><IconStyle><Icon>
<href>http://maps.google.com/mapfiles/kml/paddle/red-stars.png</href>
</Icon> </IconStyle></Style>'
stylN='<Style id="normalPlacemark"><IconStyle><Icon>
<href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href>
</Icon> </IconStyle></Style>'
line.append(stylH)
line.append(stylN)
for i in xrange(len(a)):
cno=a.loc[i,'C_NO']
nam=cno+'_'+cno2name[cno]
line.append('<Placemark><name>'+nam+'</name>
<styleUrl>#highlightPlacemark</styleUrl><Point><coordinates>')
x,y=a.loc[i,'UTM_E'],a.loc[i,'UTM_N']
lat,lon=twd97.towgs84(x,y)
line.append(str(lon)+','+str(lat)+',0</coordinates></Point></Placemark>')
with open('sta_list.txt','r') as f:
t=[ln.strip('\\n') for ln in f]
t=[i.split() for i in t[1:]]
Xcent,Ycent= 248417-333.33*5, 2613022-3000.
GP=[47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 58, 59, 60, 61]
a=DataFrame({'name':[d_nstnam[i[0]] for i in
t],'UTM_E':[float(i[2])+Xcent for i in t],
'UTM_N':[float(i[3])+Ycent for i in t],'ID':[int(i[0]) for i
in t]})
a=a.loc[a.ID.map(lambda x:x in GP)].reset_index(drop=True)
for i in xrange(len(a)):
nam=a.loc[i,'name']
line.append('<Placemark><name>'+nam+'</name>
<styleUrl>#normalPlacemark</styleUrl><Point><coordinates>')
x,y=a.loc[i,'UTM_E'],a.loc[i,'UTM_N']
lat,lon=twd97.towgs84(x,y)
line.append(str(lon)+','+str(lat)+',0</coordinates></Point></Placemark>')
line.append('</Document></kml>')

with open('cno_xy.kml','w') as f:
[f.write(l) for l in line]
```
![](media/image17.png){width="5.800001093613298in" height="4.64in"}

Google Map上貼等值圖

數據之讀取

由ISC或其他模式產生X，Y，C，三個等長度的數據向量，可以是網格數據、也可以是離散點數據。由於以下X與Y有分開處理的需求，因此雖然是3維數據，還是以1維的3個向量處理較為方便。

with open('NAL.yr','r') as f:

g=[line for line in f]

desc=g[:3]

g=g[8:]

x,y,c=([float(i.split()[j]) for i in g] for j in xrange(3))

lg=len(g)

ISCST/AERMOD輸出之plot
file前8行是有關模擬設定的敘述，前3行是模式設定，將用做KML檔案之說明；4\~8行是plot
file的格式設定，這是因為早先fortran程式設計時，為使資料檔最小化，會考量資料的緊密度，對資料格式有較精確的要求，而使用python或較新的語言，**split()**即可解決大多數的資料切割的問題。

元組(...)tuple雖然不能更改內容順序，但亦是可以接受迴圈重複(iterate)，使用tuple方式來給定一組變數，是蠻方便的方式。

圖面網格的產生

使用np現有模組(**meshgrid**)，先產生圖面格點座標系統，再內插到新的格點。由於模式計算、以及此處的內插程式，都必須在直角座標系統下運作，而google則需要經緯度來對照位置。此處的策略是分進合擊，座標同時有TWD97與GSW84兩組，直角座標系統進行格點內插計算，而經緯度則為等值線計算與最後輸出之座標。

```python
nx,ny=max(int(np.sqrt(lg)),len(set(x)))*2,max(int(np.sqrt(lg)),len(set(y)))*2
x_mesh=np.linspace(np.min(x),np.max(x),nx)
y_mesh=np.linspace(np.min(y),np.max(y),ny)

#2-d mesh coordinates, both in TWD97 and WGS84
x_g,y_g=np.meshgrid(x_mesh,y_mesh)
ll=np.array([[twd97.towgs84(i,j) for i,j in zip(x_g[k],y_g[k])]
for k in xrange(ny)])
	lat,lon=(ll[:,:,i] for i in [0,1])
```

此處nx/ny除了由x,y的集合元素個數讀取之外，還增加了一個選項就是所有點的開根號值(二者選較大值，較為保守)，這個設計是為離散點或非等間距網格資料來源，這樣程式還是可以估計大致上的解析度需求，不會產出太粗或太密的圖面網格系統。

網格產生程式**meshgrid**需要輸入等間距的X與Y序列(此處長度為nx/ny)，結果產生ny×nx的網格點座標值x_g及y_g，座標值的shape是(ny,nx)的2維陣列，其順序與ISC
plot file一致。

### 直角座標與經緯度座標的轉換

`TWD97 based on lon=121`

如前所述，內插時乃使用直角座標系統（TWD97），繪製等值圖與輸出時才須轉成經緯度系統。

Twd97與gsw84轉換程式雖然有大氣模式中的fortran副程式**UTM2LL**，但一方面UTM與TWD97還有50公里差異，一方面fortran程式與python還是格格不入，在速度要求時將造成屏障。

python方面許多網友及網站也都有提出解決方案，但還是使用pypi的套件**twd97**最為方便[^70]，用法為**twd97.togws84(X,Y)**，X,Y為TWD97座標值，單位為公尺。其結果先是緯度、後是經度，單位是度。此一程式須另行**pip**裝置並**import**。程式應用時要注意網格點的順：

ll=np.array([[twd97.towgs84(i,j) for i,j in zip(x_g[k],y_g[k])]
for k in xrange(ny)])

lat,lon=(ll[:,:,i] for i in [0,1])

由於twd97函數不能以陣列輸入/輸出方式整筆一次作用，必須要一個個的進行座標轉換，在**ll**的設計上有其暫存與順序的必要性，因為同時必須保持**g_x/g_y**網格點的2維的維度與順序，也要能容納每點的2個結果(共3維)。

經緯度與**ll**的轉換再次用到元組迴圈的手法，3維變數降階成為2個2維變數。

`tm2 based on 119 vs 121`

TEDS資料庫中外島(開頭以WXY者)直角座標同樣採二度分帶系統tm2，只是中心線是在119，而非本島之121，因此如果將其畫在同樣一張圖上，會以為落在海上(金門縣落在新竹西方、澎湖縣落在花蓮東方)的錯誤結果。如果精度要求不高，x值直接扣一個定值(201500
m)大略可以得到滿意的結果，如果需要套圖，就必須正視此一問題。

目前直角座標與經緯度轉換工具仍然聚焦使用twd97模組，策略目標仍然是向左平移，但移動的是2度，而非一個定值，這樣在不同緯度上會有較高的精度。

首先求得外島tm2座標在121度系統的lat/lon值是多少，緯度應為不變，然而經度則需扣2度，向左平移2度的意思，才會是正確的位置。最後，即使是tm2-119系統，但經緯度是正確的，而這些經緯度值同樣在tm2-121度系統，會代出多少TWD97
xy值?一樣由twd97模組計算：

```python
ll=[twd97.towgs84(i,j) for i,j in zip(x,y)]
ll2=[(i,j-2) for i,j in ll]
xy=[twd97.fromwgs84(i,j) for i,j in ll2]
```

x,y是TEDS原來外島tm2-119的座標值，最後(xy)則是本島tm-121系統的座標值，如果檢討其間的差值，約為119,590\~204,676，與前述定值(201,500
m)差異還不小。

這樣整理完，外島的座標值才會和本島同一個系統，都是121系統，可以應用相同的程式進行計算，而且點位不會掉到海裏。

![](media/image18.png){width="2.72in" height="2.176000656167979in"}

### 內插數據到圖面網格

主要使用scipy的程式(from scipy.interpolate import
griddata)[^71]進行，輸入x/y2個向量、濃度向量**c**以及要內插的圖面網格系統座標矩陣**rid_x,
grid_y**，即為前述np.meshgrid的結果。

```python
points=np.array(zip(x,y))
grid_z2 = griddata(points, c, (grid_x, grid_y), method='cubic')
```

內插的方法有nearest、linear、cubic(1-D、2-D cubic
spline)等，為考慮模擬結果的平滑性，此處選用cubic。

### 等值線座標解析

由conto圖中解析等值線(輪廓線)方式有很多，但大多是圖像處理(如opencv)，此類程式乃針對一個高解析度的圖形檔進行處理，並不一定需要是連續場，相對而言，物理世界的連續場較圖形檔案單純許多。

而就連續場的等值線方面的應用一般也會應用到`matplotlib.contour.collection.get_path`。此處則是用matplotlib既有的模組cntr.trace進行[^72]。首先須設定等值線的值，將等值線圖先準備好：

```python
import matplotlib._cntr as cntr
N=10
levels=np.linspace(0,np.max(grid_z2),N)
M=int(np.log10(levels[1]))-1
levels=[round(lev,-M) for lev in levels]
c = cntr.Cntr(lon, lat, grid_z2)
```
此處將最小值到最大值之間線性等分為10份進行解析，如果濃度太過集中，也可以改成對數值再等分。M值為有效位數，取第一層的log10值再減1。

等值範圍無法形成封閉多邊形之問題

當模擬範圍不足時，等值範圍線會以資料範圍為界，等值線頭、尾的位置相隔太遠(此處定義為起點與端點的距離大過多邊形的最大邊的20倍)，頭、尾相連後會發生切割別的多邊形狀況。

解決策略方案可以(一)增加模式模擬的範圍直到包括所有煙流形狀的多邊形、也可以(二)在模擬範圍周界增加一圈極低值，這樣就會自然形成一個內插的邊界線，此處考量最簡直接且不造錯誤的方案，選擇(三)在頭、尾端點中間增加地圖的角落點，讓該部分等值線與邊界重疊。

作法上研判端點的位置最靠近哪一個邊，選擇兩個邊所夾的直角，加入該直角頂端的座標做為頭、尾點的中間點，連成多邊形。

tol=1.E-4

e,w,s,n=np.max(lon),np.min(lon),np.min(lat),np.max(lat)

...

for level in levels:

...

for seg in segs:

line.append('<Placemark><name>level:'+str(level)+'</name>'+head2)

leng=-9999

for j in xrange(len(seg[:,0])):

line.append(str(seg[j,0])+','+str(seg[j,1])+',0 ')

if j>0:

leng=max(leng,np.sqrt((seg[j,0]-seg[j-1,0])2+(seg[j,1]-seg[j-1,1])2))

leng0=np.sqrt((seg[j,0]-seg[0,0])2+(seg[j,1]-seg[0,1])2)

ewsn=np.zeros(shape=(4,2))

j=-1

if leng0>leng and leng0/leng>20:

if abs(seg[j,0]-e)<tol:ewsn[0,1]=1

if abs(seg[0,0]-e)<tol:ewsn[0,0]=1

if abs(seg[j,0]-w)<tol:ewsn[1,1]=1

if abs(seg[0,0]-w)<tol:ewsn[1,0]=1

if abs(seg[j,1]-s)<tol:ewsn[2,1]=1

if abs(seg[0,1]-s)<tol:ewsn[2,0]=1

if abs(seg[j,1]-n)<tol:ewsn[3,1]=1

if abs(seg[0,1]-n)<tol:ewsn[3,0]=1

if
sum(ewsn[1,:]+ewsn[2,:])==2:line.append(str(np.min(lon))+','+str(np.min(lat))+',0
')

if
sum(ewsn[1,:]+ewsn[3,:])==2:line.append(str(np.min(lon))+','+str(np.max(lat))+',0
')

if
sum(ewsn[0,:]+ewsn[3,:])==2:line.append(str(np.max(lon))+','+str(np.max(lat))+',0
')

if
sum(ewsn[0,:]+ewsn[2,:])==2:line.append(str(np.max(lon))+','+str(np.min(lat))+',0
')

首先定義4個範圍邊界的座標(東西南北ewsn)，以及差值的容忍度tol，作為研判是否足夠靠邊的依據。由多邊形每個線段中找到最大值，如果頭、尾端點閉合時的距離，大於最大值的20倍，則啟動研判機制，否則直接閉合。

進行頭、尾端點與東、西、南、北4邊座標進行比較，看端點是靠近哪一邊，記錄在4×2陣列ewsn內。按照西南、西北、東北、東南的順序，看頭尾端點是哪一個狀況，以便加入直角頂端的角落座標。

此處因主要用在點源在中央的模擬狀況，並不會有等值線貫串範圍中央的情形，該類狀況有偏東、西、南、北共有4個可能情形，各須增加2個端點座標。

等值線(contour line)或是色塊圖(shaded area)

色塊圖雖然清楚，但可能在細部檢討時把底圖疊得霧濛濛，不容易檢討，還蠻干擾的。理論上後者比前者多一個動作就是將Polygon填滿顏色，因此如果只要等值線，只要把Polygon相關的設定拿掉即可。

> kuang@master \~/bin

$ diff grd2kml.py grd2kml_l.py

63,64c63,64

<
head2='</styleUrl><Polygon><outerBoundaryIs><LinearRing><tessellate>1</tessellate>

<coordinates>'

<
tail2='</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'

\-\--

>
head2='</styleUrl><LinearRing><tessellate>1</tessellate><coordinates>'

> > tail2='</coordinates></LinearRing></Placemark>'

linearRing會將線段圈起來，必須還保留，只要把紅字Polygon與outerBoundaryls刪除，就不會將等值線圈區域填滿顏色了。

輸入grd檔案

理論上grd格式的檔案已經整理非常適合畫等值圖了，使用副程式load_surfer.py(詳前述)即可解決輸入檔格式問題。然而還是有些困難。一是超大值的邊界空白值、一是解析度的問題。

前者肇因於SURFER內設一高值（1.70141e+38）會在圖面上保留空白，一般是在邊界線上。CALPOST也應用這個設定，將邊界上沒有模擬的地方保留空白，而顯然matplotlib的cntr沒有這個協定。

前述KML畫等高線的多邊形還有一件事沒有做，就是凹地、外側高值的情況，在此邊界高、內部低的情況，目前的作法會畫一個帳篷一樣的天花板，整個圖面都會是最高值範圍。

空白不是0，也不能填入任何定值，mask雖然不會讓它干擾計算，但值仍然還是存在，所以必須實質上將其裁剪掉，原來nx,ny的array就成了nx-2,ny-2的array：

```python
#read the iscst result plot file, must be in TWD97-m system.
x,y,c,(ny,nx)=load_surfer(fname)
if type(max(c))==np.ma.core.MaskedConstant:
	x=x.reshape(ny,nx)
	y=y.reshape(ny,nx)
	c=c.reshape(ny,nx)
xx=np.array([x[j,i] for j in xrange(1,ny-1) for i in xrange(1,nx-1)])
yy=np.array([y[j,i] for j in xrange(1,ny-1) for i in xrange(1,nx-1)])
cc=np.array([c[j,i] for j in xrange(1,ny-1) for i in xrange(1,nx-1)])
x,y,c,ny,nx=(xx,yy,cc,ny-2,nx-2)
```

為避免剪錯，先判別最大值是否是被mask過的常數，如果是，那就先將1維的x,y,c轉成2維，再將2維陣列內部值另存新的陣列，如此就將邊界裁剪掉了。

解析度指得是圖面上線段的解析度，如果使用資料原來的解析度，可能會有所不足，當放大圖來看時，就會發現等值線轉折生硬的情況。解決的方式是將資料檔的nx和ny與內插網格數的nx,ny區隔，讓後者是前者的一定倍數，即可解決此一問題，如範例中為3倍：

```python
$ cat \~/bin/grd2kml.py
#!/cluster/miniconda/bin/python
import numpy as np
import twd97
from scipy.interpolate import griddata
import matplotlib._cntr as cntr
from load_surfer import load_surfer

def getarg():
	""" read the setting of plot from argument(std input)"""
	import argparse
	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "\--fname", required = True, type=str,
	help = "isc_plotfile")
	args = vars(ap.parse_args())
	return args['fname']

fname=getarg()
#read the iscst result plot file, must be in TWD97-m system.
x,y,c,(ny,nx)=load_surfer(fname)
if type(max(c))==np.ma.core.MaskedConstant:
	x=x.reshape(ny,nx)
	y=y.reshape(ny,nx)
	c=c.reshape(ny,nx)
xx=np.array([x[j,i] for j in xrange(1,ny-1) for i in xrange(1,nx-1)])
yy=np.array([y[j,i] for j in xrange(1,ny-1) for i in xrange(1,nx-1)])
cc=np.array([c[j,i] for j in xrange(1,ny-1) for i in xrange(1,nx-1)])
x,y,c,ny,nx=(xx,yy,cc,ny-2,nx-2)

#1-d X/Y coordinates
nxg,nyg=nx*3,ny*3
x_mesh=np.linspace(np.min(x),np.max(x),nxg)
y_mesh=np.linspace(np.min(y),np.max(y),nyg)

#2-d mesh coordinates, both in TWD97 and WGS84
x_g,y_g=np.meshgrid(x_mesh,y_mesh)
ll=np.array([[twd97.towgs84(i,j) for i,j in zip(x_g[k],y_g[k])]
for k in xrange(nyg)])
	lat,lon=(ll[:,:,i] for i in [0,1])
e,w,s,n=np.max(lon),np.min(lon),np.min(lat),np.max(lat)

#interpolation vector c into meshes
points=np.array(zip(x,y))

#cubic spline may smooth too much,be careful.
grid_z2 = griddata(points, c, (x_g, y_g), method='cubic')
#levels size,>10 too thick, <5 too thin
N=10
levels=np.linspace(0,np.max(c),N)
col='#00FF0A #3FFF0A #7FFF0A #BFFF0A #FFFF0A #FECC0A #FD990A #FC660A #FB330A #FA000A'.replace('#','').split()
if len(col)!=N:
	print 'color scale not right, please redo from [[http://www.zonums.com/]{.underline}](http://www.zonums.com/)online/color_ramp/'
aa='28' #''28'\~ 40%, '4d' about 75%
rr,gg,bb=([i[j:j+2] for i in col] for j in [0,2,4])
col=[aa+b+g+r for b,g,r in zip(bb,gg,rr)]

#round the values of levels to 1 significant number at least, -2 at least 2 digits

M=int(np.log10(levels[1]))-1
levels=[round(lev,-M) for lev in levels]
c = cntr.Cntr(lon, lat, grid_z2)

#the tolerance to determine points are connected to the boundaries
tol=1E-3
col0='4d6ecdcf'
col_line0='cc2d3939'
head1= """
<?xml version="1.0" encoding="UTF-8"?><kml
xmlns="http://earth.google.com/kml/2.2">
<Document><name><![CDATA['+fname+']]></name>'
st_head=''
st_med='</color><width>1</width></LineStyle><PolyStyle><color>'
st_tail='</color></PolyStyle></Style>'
for i in xrange(N):
st_head+='<Style
id="level'+str(i)+'"><LineStyle><color>'+col[i]+st_med+col[i]+st_tail
head2='</styleUrl><Polygon><outerBoundaryIs><LinearRing><tessellate>1</tessellate><coordinates>'
tail2='</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
line=[head1+st_head]

#repeat for the level lines
for level in levels[:]:
nlist = c.trace(level, level, 0)
segs = nlist[:len(nlist)//2]

i=levels.index(level)
for seg in segs:
line.append('<Placemark><name>level:'+str(level)+'</name><styleUrl>#level'+str(i)+head2)

leng=-9999

for j in xrange(len(seg[:,0])):

line.append(str(seg[j,0])+','+str(seg[j,1])+',0 ')

if j>0:

leng=max(leng,np.sqrt((seg[j,0]-seg[j-1,0])2+(seg[j,1]-seg[j-1,1])2))

leng0=np.sqrt((seg[j,0]-seg[0,0])**2+(seg[j,1]-seg[0,1])**2)

ewsn=np.zeros(shape=(4,2))

j=-1

#end points not closed, add coner point(s) to close the polygons.

if leng0>leng and leng0/leng>5:

if abs(seg[j,0]-e)<tol:ewsn[0,1]=1

if abs(seg[0,0]-e)<tol:ewsn[0,0]=1

if abs(seg[j,0]-w)<tol:ewsn[1,1]=1

if abs(seg[0,0]-w)<tol:ewsn[1,0]=1

if abs(seg[j,1]-s)<tol:ewsn[2,1]=1

if abs(seg[0,1]-s)<tol:ewsn[2,0]=1

if abs(seg[j,1]-n)<tol:ewsn[3,1]=1

if abs(seg[0,1]-n)<tol:ewsn[3,0]=1

if
sum(ewsn[1,:]+ewsn[2,:])==2:line.append(str(np.min(lon))+','+str(np.min(lat))+',0
')

if
sum(ewsn[1,:]+ewsn[3,:])==2:line.append(str(np.min(lon))+','+str(np.max(lat))+',0
')

if
sum(ewsn[0,:]+ewsn[3,:])==2:line.append(str(np.max(lon))+','+str(np.max(lat))+',0
')

if
sum(ewsn[0,:]+ewsn[2,:])==2:line.append(str(np.max(lon))+','+str(np.min(lat))+',0
')

#TODO: when contour pass half of the domain,must add two edge points.

line.append(tail2)

line.append('</Document></kml>')

with open(fname+'.kml','w') as f:

[f.write(i) for i in line]
```
KML相關設定

此處方案一(單色)多邊形樣式的設定，乃是仿照網友提供範例[^73]，並無太大的修改：

方案一：
```python
head1=
"""
<?xml version="1.0" encoding="UTF-8"?> 
<kml xmlns="http://earth.google.com/kml/2.2"> 
<Document><name><![CDATA['+fname+']]></name> 
<Style id="www.leguideregional.fr">
<LineStyle><color>**cc2d3939</color><width>2</width></LineStyle>
<PolyStyle><color>4d6ecdcf</color></PolyStyle></Style>
"""
head2="""
<styleUrl>#www.leguideregional.fr</styleUrl>
<Polygon><outerBoundaryIs><LinearRing><tessellate>1</tessellate><coordinates>
"""
tail2='</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
"""
```

### 顏色

KML其中顏色的格式並非html 也不是16進位的顏色表，而是ABGR格式[^74](Alpha,
Blue,Green,Red共8碼)，可以由網友提供的轉換程式建立對照關係，先點選色表[^75]得到html編號，再輸入線上轉換程式[^76]，由網頁取得透明度代碼(aa)[^77]，即可得到ABGR編號。或者由色階表[^78]直接由RGB進行轉換：

```python
col='#00FF0A #3FFF0A #7FFF0A #BFFF0A #FFFF0A #FECC0A #FD990A
#FC660A #FB330A #FA000A'.replace('#','').split()

if len(col)!=N:
print 'color scale not right, please redo from http://www.zonums.com/online/color_ramp/'
aa='28' #''28'\~ 40%, '4d' about 75% opacity
rr,gg,bb=([i[j:j+2] for i in col] for j in [0,2,4])
col=[aa+b+g+r for b,g,r in zip(bb,gg,rr)]
```

col原始字串來自於網友提供色階表產生器(example 1紅綠色階，首末交換後，按照總階層數(10)，扣掉前中後3個顏色，鍵入中間的階層數(10-3=7，分別再分為3及4，高濃度需要較高的鑑別力，給較多階層)，將表列文字選取複製貼成文字檔後**cat  |awkk 2**即可得第2欄HEX值，去掉'#'後依序存成rr,gg,bb 三個序列。另讀取透明度值令為aa，即可再組合成ABGR值。

![](media/image19.png){width="3.5733333333333333in"
height="1.7386668853893263in"}

透明度

透明度在KML顏色的控制是最重要的，因此色碼第1碼即為Alpha值。如果色塊重疊的個數較多，高濃度的位置透明度將會較低，因此透明度的設定與濃度階層數有關。Alpha值可以由網友提供的界面讀取，亦可大略求得[^79]：00為完全透明，ff為完全不透明，50
percent opacity= 80，40%: 66, 4d about 30% opacity。

線寬

KML的線寬選項是以畫素為單位，如果太粗在等值線密集處將會造成重疊。一般選擇1\~3畫素為合理範圍。

樣式之定義與連結

KML元件使用到的樣式必須統一在檔頭一併宣告，其後個別元件再引用連結。例如：

方案二：


```python
st_head=''
st_med='</color><width>1</width></LineStyle><PolyStyle><color>'
st_tail='</color></PolyStyle></Style>'
for i in xrange(N):
	st_head+='<Style id="level'+str(i)+'"><LineStyle><color>'+col[i]+st_med+col[i]+st_tail
```

範例中的st_head內容為N個level的樣式，名稱分別為level0,
level1\~level9(設N=10)，其特徵在於各有自己的顏色設定(col[i])。

樣式的引用必須使用<styleUrl>#...</styleUrl>指令：

```python
head2='</styleUrl><Polygon><outerBoundaryIs><LinearRing><tessellate>1</tessellate><coordinates>'

for level in levels[:]:
	nlist = c.trace(level, level, 0)
	segs = nlist[:len(nlist)//2]
	i=levels.index(level)
	for seg in segs:
		line.append('<Placemark><name>level:'+str(level)+\
		'</name>styleUrl>level'+str(i)+head2)
```

引用的名稱即為上述level0, level1 \~level9等，如果沒有抓到指定的樣式，KML將無法解析。

### KML元件以及檔案之組合

基本上KML檔案為表頭、元件、以及表尾三者之組合，表頭包括前述所有樣式的宣告，如前所述。此處主要處理元件部分，本範例即為每個等值線所形成的多邊形。

```python
....
tol=1E-3
line=[head1+st_head]

#repeat for the level lines
for level in levels[:]:
	nlist = c.trace(level, level, 0)

segs = nlist[:len(nlist)//2]

i=levels.index(level)

for seg in segs:

line.append('<Placemark><name>level:'+str(level)+'</name><styleUrl>#level'+str(i)+head2)

leng=-9999

for j in xrange(len(seg[:,0])):

line.append(str(seg[j,0])+','+str(seg[j,1])+',0 ')

if j>0:

leng=max(leng,np.sqrt((seg[j,0]-seg[j-1,0])**2+(seg[j,1]-seg[j-1,1])**2))

leng0=np.sqrt((seg[j,0]-seg[0,0])**2+(seg[j,1]-seg[0,1])**2)

ewsn=np.zeros(shape=(4,2))

j=-1

#end points not closed, add coner point(s) to close the polygons.

if leng0>leng and leng0/leng>5:

if abs(seg[j,0]-e)<tol:ewsn[0,1]=1

if abs(seg[0,0]-e)<tol:ewsn[0,0]=1

if abs(seg[j,0]-w)<tol:ewsn[1,1]=1

if abs(seg[0,0]-w)<tol:ewsn[1,0]=1

if abs(seg[j,1]-s)<tol:ewsn[2,1]=1

if abs(seg[0,1]-s)<tol:ewsn[2,0]=1

if abs(seg[j,1]-n)<tol:ewsn[3,1]=1

if abs(seg[0,1]-n)<tol:ewsn[3,0]=1

if
sum(ewsn[1,:]+ewsn[2,:])==2:line.append(str(np.min(lon))+','+str(np.min(lat))+',0
')

if
sum(ewsn[1,:]+ewsn[3,:])==2:line.append(str(np.min(lon))+','+str(np.max(lat))+',0
')

if
sum(ewsn[0,:]+ewsn[3,:])==2:line.append(str(np.max(lon))+','+str(np.max(lat))+',0
')

if
sum(ewsn[0,:]+ewsn[2,:])==2:line.append(str(np.max(lon))+','+str(np.min(lat))+',0
')

#TODO: when contour pass half of the domain,must add two edge points.

line.append(tail2)

line.append('</Document></kml>')

with open(fname+'.kml','w') as f:

[f.write(i) for i in line]
```
元件的開始與結束亦有其表頭及表尾，以<Placemark>...
</Placemark>所夾為範圍，內容包括名稱(name此處做為濃度值之標示)、樣式呼叫(**StyleURL**，此處作為濃度值之顏色)以及座標值(lat,lon,altitude
即為前述**trace**結果)

TITLE、PLACE、與descriptions
緊接文件(`<Document>`)之後，頭一次的<name>...</name>內容會出現在「你的地圖」圖層名稱，可以類似GIS圖層勾選顯示，或暫時不勾選以進行比較，此處應插入**TITLE**以利辨識。

以下在「你的地圖」圖層個別樣式之下會出現各線條(**Line**)、圖像(**Icon**)之名稱，須個別給定，以利辨識。此名稱須在標記之後予以給定(<Placemark><name>...</name></Placemark>)，將PLACE的內容，如前述的等值線level數值、或標記點的地名、測站名稱、工廠名稱等予以插入，如以下範例的nam。

前述TITLE及PLACE會出現在「你的地圖」左側。如果還需要更多訊息，可以在每次的name之後使用**description**指令，會將在點選地標、線條之後出現補充說明，如範例中的**desc**：

```python
ems='NO2_KGpH PM_KGpH SO2_KGpH'.split()
for i in xrange(len(a)):
nam=a.loc[i,'CNO']
desc=a.loc[i,'name']+' '
for j in ems:
desc+=j[0:3].strip('_')+':'+str(round(a.loc[i,j],0))+'(T/Y),
'
desc.strip(', ')
line.append('<Placemark><name>'+nam+'</name><description>'+desc+'</description><styleUrl>#highlightPlacemark</styleUrl><Point><coordinates>')
x,y=a.loc[i,'UTM_E'],a.loc[i,'UTM_N']
lat,lon=twd97.towgs84(x,y)
line.append(str(lon)+','+str(lat)+',0</coordinates></Point></Placemark>')
```
範例中將資料表a中的CNO列為地標的名稱，會在左側圖例出現工廠的管制編號，然而並不是每個人對管制編號都很熟悉，這時候就需要說明，因此在name之後加上<description>'
+desc+
'</description>，其內容包括工廠名稱、N/P/S之全年排放量等。在點選左側圖例或者是地標時，就會出現這段文字。

![](media/image20.png){width="4.1333344269466314in"
height="3.306667760279965in"}

### Google map界面

工作地圖

進入google
map→選單(左側)→你的地點→地圖「建立地圖」→新增圖層「匯入」→選取裝置中的檔案→選擇檔案後→按確定即可。

Google
map的圖層界面在左側panel，可以勾選是否貼上圖層，當輸入不同模擬結果時，可以用勾選圖層來進行模擬結果的比較。

當滑鼠經過左側選單個別多邊形名稱(level:nn)的時候，圖面上的多邊形會反白，同樣在滑鼠經過圖面上多邊形的時候，左側名稱亦會出現灰底，如此可以檢試模擬結果的數字及位置。

成果地圖

工作地圖有左側圖例版，也有搜尋命令列，還蠻干擾的，可以在「你的地圖」名稱之下，點選「預覽」，在標題右側的選單選擇收合地圖圖例，就可以有乾淨的圖面，如果再按F11全螢幕檢視，按下ctrl-printscreen鍵就可以複製到記憶體了。

![](media/image21.png){width="3.24in"
height="2.5920002187226596in"}![](media/image22.png){width="3.24in"
height="2.581334208223972in"}


PseudoNetCDF系統

NetCDF是科技資訊界常用的資料格式，一般是給fortran給或者是C語言使用，亦有學者發展Python版本，謂之PseudoNetCDF，相關說明、安裝與使用說明如下。

PseudoNetCDF安裝

程式來源與發展者

Barron
Henderson原為佛州大學環境科學及工程學系助理教授，現任職於USEPA，程式碼與安裝使用說明可以由個人網站下載[^87]。

下載與安裝

git

可以用git指令下載[[https://github.com/barronh/pseudonetcdf.git]{.underline}](https://github.com/barronh/pseudonetcdf.git)內容，或由githup網頁的右上綠色按鈕「Clone
or download」下拉「download
zip」另存zip檔於所在地硬碟。在指定目錄解開後就可以使用。目錄應為\~/lib/python2.7/site-packages/PseudoNetCDF(\~為python程式所在地之根目錄)。

pip zip

亦可直接使用pip指令：

pip install
[[https://github.com/barronh/pseudonetcdf/archive/v2.0.1.zip]{.underline}](https://github.com/barronh/pseudonetcdf/archive/v2.0.1.zip)

for the most stable version or

pip install
[[http://github.com/barronh/pseudonetcdf/archive/master.zip]{.underline}](http://github.com/barronh/pseudonetcdf/archive/master.zip)

for the latest.

安裝完畢除在前述目錄下有python程式之外，在\~/bin下亦會有pncdump執行檔。前者可供python程式內呼叫(import)，後者則類似ncdump程式的功能，在命令列可以直接進行netCDF(或其他CAMx等)檔案之讀取、處理及存檔。

pip uninstall/install

PseudoNetCDF在更新版本的時候，必須先卸載之前的版本(pip uninstall
PseudoNetCDF)，在系統詢問時按y確定卸載之後，再安裝最新版本(pip install
PseudoNetCDF)，否則不同版本之間會有少數功能不能協調。

pncdump/pncgen

除了做為python程式import的module之外，PseudoNetCDF也有類似ncdump/ncgen一樣命令列的指令pncdump/pncgen，使用方式可以參考說明檔pncdump
\--help:

看表頭

**pncdump -H -f uamiv** *[1009_Hs.S.grd02]{.underline}*

斜體字為UAM格式檔案名稱。-H在ncdump是-head。

轉換檔案

**pncgen -f uamiv** *[1009_Hs.S.grd02]{.underline}* **-O**
*[1009_Hs.S.grd02.nc]{.underline}*

(ncgen是-o)

如果是點源檔案，不論輸入或輸出格式都必須給定。(-f
point_source或\--format =
point_source，輸出格式之設定\--out-format=point_source)，若無指定，pncgen輸出內設是netCDF格式。

限制

然而此結果nc檔案不能用在verdi/meteoInfo/
grads_sdfopen。可能原因：PseudonetCDF並不接受也不會產生lambert座標系統，而grads似乎必須是等間距且正交之經緯度系統。

Python程式內呼叫pseudonetcdf程式庫

基礎說明

一般運用pncgen或pncdump就可以完成大部分的檔案讀寫動作，但有時須配合其他的作業，或整合個別的檔案讀寫動作，因此以python直接呼叫pseudonetcdf程式庫會比較有效率一些。如此可以輕鬆開啟、讀取、並進行計算(詳參numpy的操作方式)。亦可藉由ipython對話介面處理uamiv(等)格式之大型檔案，在程式靈活度上是比fortran更具有優勢。

一般基本的功能

檔案讀寫

開啟檔案的種類與python相同，'r','w',及'r+',
'w+'唯讀、唯寫及同時可讀可寫等三種[^88]('w+'目前尚未開放)。與NetCDF4一樣，PseudoNetCDF並無特殊指令儲存檔案，NetCDF4只需執行.close()即可將最後變數的情況全部予以存檔，並關閉檔案，不能再更改了。然而PseudoNetCDF的close不能加()，此外即使關閉了也還能再改內容，此一功能類似.sync()。

維度與變數模版的應用

與NetCDF4一樣，因為所有變數的項目與維度順序都是tuple，是不能更動的，只能更動矩陣的內容數值，因此一般以「模版」方式來作業[^89]。

而在netcdf或pseudonetcdf的運作中，'='的作用是會回溯的，因此在更動前，最好以os.system(或shutil)複製一份來作業比較保險。如下範例：

kuang@master /nas1/camxruns/2017/ICBC/bndextr

$ cat addVOC.py

import os

from PseudoNetCDF.camxfiles.lateral_boundary.Memmap import *

dirs=['NORTH','SOUTH','EAST','WEST']

for mon in ['09','10','11','12']:

fname='base.grd02.17'+mon+'.bc'

fnameO='base.grd02.17'+mon+'.bcM'

os.system('cp '+fname+' '+fnameO)

a=**lateral_boundary**(fnameO,'r+')

for d in dirs:

varnam=d+'_PAR'

a.variables[varnam][:,:,0:4]=a.variables[varnam][:,:,0:4]*1.5
#////

維度與變數的增修

如果要形成新的檔案模版，可以類似nc.createDimension及nc.createVariable的做法，形成新模版的維度與變數，然後在python內直接呼叫pncgen輸出檔案。

from PseudoNetCDF import PseudoNetCDFFile

from PseudoNetCDF.pncgen import pncgen

newf = **PseudoNetCDFFile**()

newf.createDimension('TSTEP', 25)

newf.createDimension('LAY', ?)

newf.createDimension('ROW', ?)

newf.createDimension('COL', ?)

newf.createDimension('DATE-TIME', 2)

newf.createDimension('VAR', ?)

newf.NROWS = ?

newf.NCOLS = ?

\...

newf.XORIG = ?

\...

newf.createDimension('COL', ?)

var = newf.createVariable(\...)

var.units = '\...'

var[:] = '\...'

pncgen(newf, '/path/for/output.bin', format = 'uamiv')

**減少**特定維度的長度

一如netCDF其他的檔案處理軟體，一但讀入記憶體的pnc/nc檔案內容，是不能增加或減少其長度的，必須在讀入時即進行切片(slicing)動作，這樣才能篩選出所要的維度範圍，進行特定的計算或剪接。範例如下：

pt=pnc.pncopen(fname1,format='point_source').sliceDimensions(NSTK=1)

...

atobsf = camxf.sliceDimensions(TSTEP=t, LAY=k, ROW=j, COL=i)

...

aqf1 = pnc.pncopen(aqpath1, format='ioapi')\\

.subsetVariables(['O3'])\\

.sliceDimensions(TSTEP=slice(-5, None), LAY=0)

aqf2 = pnc.pncopen(aqpath2, format='ioapi')\\

.subsetVariables(['O3'])\\

.sliceDimensions(TSTEP=slice(None,19), LAY=0)

...

wrff = pnc.pncopen(wrfpath)\\

.subsetVariables(['T2'])\\

.sliceDimensions(

Time=slice(31, 55),

bottom_top=0,

west_east=slice(100, 287),

...

引數第一項即是維度的名稱，不能加引號，可以由**pncdump**找到。另**sliceDimensions**()是pnc檔案的物件，之間的連接是用"**.**"而非"**,**"。引數等號右邊的內容適用xrange()的作法方式(三個數字分別是起、迄與間隔)。

**增加**特定維度的長度

增加一個檔案在特定維度上的長度是不可能，除非檔案原來就宣告長度是未受限的(Unlimited)。然而將2個相同維度數的檔案，在該維度上前後相連、疊加、合併(concatenate)，卻是可能的，在PseudoNetCDF此一指令叫做堆疊pncfile1**.stack(**pncfile2,dimension**)**

pt1=pt.copy()

pt=pnc.pncopen(fname2,format='point_source')

pt2= pt.stack(pt1, 'NSTK')

範例中pt1為整理好單一煙囪的煙道條件與排放量所有數據，除了在煙道數這個維度上有長度的差異之外，其餘包括時間、物質種類等維度的長度及順序，都必須與原來的pt檔案相同。堆疊後pt1將會在pt之後，形成pt2檔案，準備輸出。此處.stack()第2引數維度名稱必須加引號，與前述sliceing有異。

矩陣內容的更動

可以用批次方式[:]來更動，更動之後檔案內容隨即改變。如上範例，(有時)甚至不必關閉檔案，離開即存。

特定格式的檔案處理，有時必須用**pncwrite**(pncfile,fname)或pncfile.save(fname)指令，後者無法指定格式，內設為nc格式。

屬性變數的更動

屬性變數存放了pnc檔案不隨時間變動的重要資訊，原本在uamiv或point_source格式的header前4筆，在pnc檔案則沒有順序。可以在ipython環境下用dir(fname)來檢查有哪些變數名稱，或fname.ncattrs()顯示。

更動的方式只要直接給定數字或字元即可。

屬性變數在轉檔(格式轉換)時之損失與補充

EDATE與ETIME在轉檔時會消失不見，原因是它們的類型是numpy.core.memmap.memmap而不只是數字。要注意適時補充。

值得注意的是NOTE這個屬性。如果是smoke或者是camx,
pncgen所產生的pnc檔案，會自動產生60個字元的note，然而自行以fortran產生的檔案如果沒有note(因為fortran會讀取或預設空白的字元，而python內則沒有預設字元長度的概念或做法，若無給定會以長度0的字串輸出)，在pncgen時將會發生困難。須檢核並產生新的note。

這些補充屬性變數的範例如下：

...

fname2='flare.14.nc'

ck_sav(pt,fname2)

pt1=pnc.pncopen(fname+'.nc') #,format='point_source')

pt=pnc.pncopen(fname2)#,format='point_source')

pt2= pt1.stack(pt, 'NSTK')

**pt2.EDATE=[edate]**

**pt2.ETIME=[etime]**

fname2=fname+'flare.nc'

#note filling

if len(pt2.NOTE)!=60:

s=fname+' add pt-flares.txt'

**pt2.NOTE=s[:max(len(s),60)]+max(0,60-len(s))*' '**

ck_sav(pt2,fname2)

...

範例中先將point_source檔存成nc格式再讀進程式中，在寫、讀過程中格式就出現了問題。EDATE及ETIME須填入單一數字的序列，而NOTE則填入正好長度60的字串。

-   PseudoNetCDF模組提供的功能

各類檔案模版可以由pncdump \--help的內容中讀取，以下為uamiv為例：

from PseudoNetCDF.camxfiles.Memmaps import **uamiv**

path = "/home/camxruns/2010/outputs/con12/1012_2linpmbase.avrg.grd01"

con_file = **uamiv**(path,'r+')

HNO3 = con_file.variables['HNO3']

print "HNO3 max",HNO3.units,HNO3[:].max() !求取最大值

...(其他功能如下

con_file.ncattrs() #所有檔案屬性之名稱

con_file.variables.keys() 所有變數的名稱

VAR.mean() 空間與時間的平均值

VAR.min() 空間與時間的最小值

VAR.dimensions 檢視變數的維度

VAR.shape 各維度的大小形狀

var3=var1+var2 可以直接做四則運算

其他功能由dir()可知：'all', 'any', 'argmax', 'argmin',
'argpartition', 'argsort', 'assignValue', 'astype', 'base',
'byteswap', 'choose', 'clip', compress', 'conj', 'conjugate',
'coordinates', 'copy', 'ctypes', 'cumprod', 'cumsum',
'data', 'diagonal', 'dimensions', 'dot', 'dtype', 'dump',
'dumps', 'fill', 'flags', 'flat', 'flatten', 'getValue',
'getfield', 'grid_mapping', 'imag', 'item', 'itemset',
'itemsize', 'long_name', 'max', 'mean', 'min', 'nbytes',
'ncattrs', **'ndim'**, 'newbyteorder', 'nonzero', 'partition',
'prod', 'ptp', 'put', 'ravel', 'real', 'repeat',
'reshape', 'resize', 'round', 'searchsorted', 'setfield',
'setflags', **'shape'**, 'size', 'sort', 'squeeze', 'std',
'strides', 'sum', 'swapaxes', 'take', 'tobytes', 'tofile',
'tolist', 'tostring', 'trace', 'transpose', 'typecode',
'units', 'var', 'var_desc', 'view']

點源讀取程式(point_source)修改與範例

由於CAMx點源格式與其他uamiv格式略有不同，在前、後處理與查核確認時，有其困難度。雖然也有一些fortran寫的小工具如pt2em.f,
rdpt.f等，然而仍然不是很方便。

pnc應用程式範例如下，將事先從模版複製出來的點源檔案開啟備用(藍底部分，以鄉鎮區代碼分類，包括原高雄市範圍201\~211、以及原高雄縣10個、與其他(212)共22個檔案)，再依序按照點源的位置研判是否位於特定範圍，如果是，則將排放量設為0(紅底部分)，以利進行模式敏感性測試：

from PseudoNetCDF.camxfiles.Memmaps import uamiv

from PseudoNetCDF.camxfiles.Memmaps import **point_source**

path='fortBE.14_212'

pts_file=**point_source**(path)

v2=filter(lambda x:pts_file.variables[x].ndim==2, [i for i in
pts_file.variables])

**nt,nstk=pts_file.variables[v2[0]].shape**

path='/home/camxruns/2018/emis/8760wt/area/seasd5.uamiv'

con_file=uamiv(path,'r')

v4=filter(lambda x:con_file.variables[x].ndim==4, [i for i in
con_file.variables])

ntd,nlay,nrow,ncol=con_file.variables[v4[0]].shape

dct42=set([4201, 4205, 4206, 4208, 4209, 4210, 4212, 4215, 4217,
4222])

alldct=set([i for i in xrange(201,212)])\|dct42

pts_file={}

for d in alldct\|set([212]):

path='fortBE.14_'+str(d)

pts_file.update({d:**point_source**(path)})

for k in xrange(nstk):

d=201

i=int((pts_file[d].variables['XSTK'][k]-con_file.XORIG)/con_file.XCELL)

j=int((pts_file[d].variables['YSTK'][k]-con_file.YORIG)/con_file.YCELL)

D=0

if i*(i-ncol)<0 and
j*(j-nrow)<0:D=int(con_file.variables[v4[0]][0,0,j,i])

if i<0 or i>ncol or j<0 or j>nrow or D not in alldct:

for v in
set(v2)**-set(['FLOW','IONE','ITWO','KCELL','NSTKS','PLMHT']**):

for d in alldct:

pts_file[d].variables[v][:,k]=0.

else:

for d in [i for i in alldct\|set([212]) if i!=D]:

for v in
set(v2)**-set(['FLOW','IONE','ITWO','KCELL','NSTKS','PLMHT']**):

pts_file[d].variables[v][:,k]=0.

for d in alldct\|set([212]):

pts_file[d].close

點源檔案沒有空間上的3維網格，只有留一個總數為nstk的順序，因此加上時間之後只有2維。此外，在時間變化維度方向上，仍有6項煙囪參數可以隨時間而不同，要將其避開不設為0，只讓污染排放為0，以避免程式運作困難。

新增點源程式範例

運用前述減少與新增維度長度的手法，來新增特定污染源在既有的點源檔案之後，範例如下：

**import PseudoNetCDF as pnc**

import numpy as np

import sys,os

with open('start.end','r') as text_file:

d=[line.strip('\\n') for line in text_file]

begJH,endJH=d[0][0:3],d[1][0:3]

fname1='BINs/fortBE.14_'+'0'*(3-len(begJH))+begJH+'-'+'0'*(3-len(endJH))+endJH

fname2='fortBE.14.test'

if not os.path.isfile(fname1):sys.exit('file not found')

os.system('cp '+fname1+' '+fname2)

pt=pnc.pncopen(fname1,format='point_source').sliceDimensions(NSTK=1)

#v3 are the time flag's

v3=filter(lambda x:pt.variables[x].ndim==3, [i for i in
pt.variables])

#v2 are the emission variables

v2=filter(lambda x:pt.variables[x].ndim==2, [i for i in
pt.variables])

#XYHDTVN

v1=filter(lambda x:pt.variables[x].ndim==1, [i for i in
pt.variables])

nhr,nvar,dt=pt.variables[v3[0]].shape

nt,nopts=pt.variables[v2[0]].shape

#fill the xinda stack variables

#v1 filling

v1_xinda=[168616.09,2527230.05,80.,-11.0,363.0,19.8*3600.,1]

Xcent,Ycent= 248417-333.33*5, 2613022-3000. #tuning the coordinates

v1_xinda[0:2]=[v1_xinda[0]-Xcent,v1_xinda[1]-Ycent]

for i in xrange(6):

pt.variables[v1[i]][0]=v1_xinda[i]

pt.variables[v1[6]][:]=[v1_xinda[6] for i in xrange(nt)]

#v2 filling

flow=(3.14*v1_xinda[3]**2/4.)*v1_xinda[5]*3600.

pt.variables['FLOW'][:,0]=[flow for i in xrange(nt)]

pt.variables['PLMHT'][:,0]=[v1_xinda[2] for i in xrange(nt)]

SPNAMs=['NO','NO2','FPRM','CPRM','SO2']

(NOx,SOx,PM)=(29.809,4.815,2.104)

fac=[3600./46.,3600./64.,3600.]

ems=[NOx*fac[0]*0.9,NOx*fac[0]*0.1,PM*fac[2]*1.0,PM*fac[2]*0.0,SOx*fac[1]]

sp_em={i:j for i,j in zip(SPNAMs,ems)}

for s in SPNAMs:

pt.variables[s][:,0]=[sp_em[s] for i in xrange(nt)]

for s in set(v2)-set(SPNAMs):

pt.variables[s][:,0]=[0. for i in xrange(nt)]

pt1=pt.copy()

pt=pnc.pncopen(fname2,format='point_source')

#sys.exit('fine')

pt2= pt.stack(pt1, 'NSTK')

pt2.save(fname2)

fname3=fname2+'_ok'

if os.path.isfile(fname3):os.system('rm '+fname3)

os.system('pncgen \--out-format=point_source '+fname2+' '+fname3)

#pnc.pncwrite(pt2,fname2,format='point_source')

-   pnc有比較多IO選項，使用point_source只允許一個引數。

-   讀入檔案、變數名稱、維度的長度，其中只有v1在後續程式中有引用，其餘並沒有用到。

-   填入興達電廠之條件數據：要注意給定條件要轉換成模式所需要的單位。座標系統的定義方式也必須和模式的設定方式一致，如預定排放的位置是UTM-M，則必須轉成模式使用的LCP系統。v1[6]
    NSTKS的長度有nt，跟其他變數不同。若要對該污染源啟動PiG次模式，必須將直徑設為負值。

-   填入時間變化的二維變數。順序為時間、煙道序。

    -   FLOW是CAMx模式用以計算每小時流速的依據，不能是負值，其數值(M3/hr)也不能低於有效高度(M)。

    -   PLMHT是用以計算煙流高度的依據，如果要CAMx用外部方式計算煙流高度，必須將PLMHT設為負值，此時FLOW不能是正值。如使用CAMx內設方式計算煙流高度，此二值設為正值即可，PLMHT沒有用到。

    -   由於模版隨機抓取，因此原有其他物質的排放量必須強制歸0。

-   存檔的方式

    -   由於記憶體中檔案的長度被改過了，所形成的新檔並不符合原來任何既存的模版檔案，不能再用point_source.close()或sync()指令，只能用pt2.save(ncfile)或pncwrite指令。

    -   pncwrite指令雖然可以直接指定輸出格式，但執行會當掉，只好使用pt2.save存成ncfile再以pncgen程式由外部進行轉檔。

    -   pncgen轉檔還有一個必要性，會重新檢查NSTKS的數目，自動修正增加此一v1陣列，不必特別再以程式另外給定。

        讀取特定污染源資料的方式

由於CAMx模式point_source格式檔案龐大，如果要讀取檢討特定的點源，肯定會非常複雜，利用PseudoNetCDF模組會比其他程式界面更新快速簡潔，程式(指令)如下：

cat /home/camxruns/2013_6.40/ptse/rd_tz150.py

import PseudoNetCDF as pnc

import numpy as np

fname1='/home/camxruns/2013/ptse/fortBE.14.g1112.h150.11Mp'

pt1=pnc.pncopen(fname1,format='point_source')

v3=filter(lambda x:pt1.variables[x].ndim==3, [i for i in
pt1.variables])

v2=filter(lambda x:pt1.variables[x].ndim==2, [i for i in
pt1.variables])

v1=filter(lambda x:pt1.variables[x].ndim==1, [i for i in
pt1.variables])

nhr,nvar,dt=pt.variables[v3[0]].shape

nt,nopts=pt.variables[v2[0]].shape

for i in xrange(nopts):

**if pt1.variables[v1[2]][i]==150:**

**print i, [pt1.variables[v1[j]][i] for j in xrange(6)]**

i1=61603;i2=61604

dd={}

for i in xrange(len(v2)):

a=pt1.variables[v2[i]][0,i2]

if a==0:continue

print v2[i], a

dd.update({v2[i]:a})

(dd['NO']+dd['NO2'])*46./3600.

(dd['SO2'])*64./3600.

s=0

for i in ['FPRM','CPRM','FCRS']:

s+=dd[i]/3600.

print s

由於這個點源的特徵是它的高度(150M)以及位置，因此最簡單直覺的方式就是列印出所有高度150M的數據，然後看看X/Y位置與該點源位置相近的結果，記錄其序號(i1/i2)，再輸出其他參數即可。

CALPUFF模式的後處理

CALPUFF模式產生的逐時網格檔案(calpuff.con)有其特殊自有的格式，除了使用CALPOST之外，其餘程式似無用武之地。首先可以利用con2avrg程式[^90]將其轉變成uamiv格式，再利用pncgen或python程式進行後處理。

由於con2avrg結果雖然可以適用所有的fortran或python程式，但尚不能直接進入verdi.sh(原因未明)，還必須進行轉換：

$ cat /home/kuang/bin/pnc_congrd02

NSTEP=\`pncdump \--head -f uamiv calpuff.con.S.grd02 \|grep NSTEPS\|grep
\\=\|awkk 3\|tail -n1\`

pncgen.py -f uamiv -a TSTEP,global,o,i,$NSTEP \--from-conv=ioapi
\--to-conv=cf -O calpuff.con.S.grd02 calpuff.con.S.grd02.nc

pncgen \--out-format=uamiv -O calpuff.con.S.grd02.nc calpuff.con.S.grd02

rm calpuff.con.S.grd02.nc

由於CALPUFF物種和傳統verdi.sh物種有差異，其對照如下：

  ------------- ---------------------
  CALPUFF.CON   暫時儲存名稱(grd02)
  SO4           CO
  NO3           NO2
  HNO3          O3
  PM2.5(原生)   PM25
  SO2           SO2
  ------------- ---------------------

因此需要一個程式將最後的PM2.5(包括原生及衍生全計算出來)

$ cat \~/bin/con2pm.py

#!/cluster/miniconda/bin/python

import numpy as np

from PseudoNetCDF.camxfiles.Memmaps import uamiv

path='calpuff.con.S.grd02'

con_file = uamiv(path,'r+')

so4=np.array(con_file.variables['CO'][:,:,:,:])

hno3=np.array(con_file.variables['O3'][:,:,:,:])

no3=np.array(con_file.variables['NO2'][:,:,:,:])

nh4=so4*(36./96.)+no3*(18./62.)+hno3*(18./63.)

p25=np.array(con_file.variables['PM25'][:,:,:,:])

total=so4+no3+hno3+nh4+p25

con_file.variables['PM25'][:,:,:,:]=total

con_file.close

由於程式將會覆蓋原來檔案內容，因此須由結果來判定是否經過處理，如下所示。一般原生性PM25較靠近點源排放口，且濃度較低。而總PM2.5濃度較高，分布位置則以煙囪口及遠方山區為主。

形態上，uamiv.variables若不指定範圍，讀出來的變數是PseudoNetCDF.core._variables.PseudoNetCDFVariable，並不是一個np陣列，**因此指定範圍[:,:,:,:]是必要的**，將陣列內容放回uamiv.variables容器時，如果沒有指定範圍，程式將不知道如何放置，存檔時可能也會發生不穩定的情形。

  ------------------------------------------------------------------------------------ ----------------------------------------------------------------------------------
  ![](media/image23.png){width="2.7959634733158354in" height="3.7790627734033246in"}   ![](media/image24.png){width="2.764750656167979in" height="3.779099956255468in"}
  ------------------------------------------------------------------------------------ ----------------------------------------------------------------------------------

將全月逐時排放量平均為24小時日變化

旨述作業為一降階(5階維度降為4階)，策略上在此選擇以陣列疊加後除以日數的方式進行，而不用**np.mean**函數來做，以保持陣列維度的整齊。

除陣列批次處理簡化程序之外，原本約720小時的檔案，如何能縮小成為24小時，(Pseudo)netCDF檔案一旦開啟後就不能修改任何維度，需要在程式外另外形成模版。模版的形成，在點源及面源採取不同的方式，前者以**sliceDimensions**單層取得1小時之模版，填入資料後再疊加24次後成為24小時成果，後者以**ncrcat**程式先取得24小時模版再一次更改內容。點源之讀寫與前述類似(slice維度由煙囪NSTK改為時間NSTEP)，不另多說明，黃底部分為疊加與平均歷程。

kuang@master /home/camxruns/2013/emis/tmp

$ cat ptse24.py

import numpy as np

import os

import PseudoNetCDF as pnc

import netCDF4 as nc

SDATE=2018288

STIME=0

fname='fortBE.14_304-334'

pt1=pnc.pncopen(fname,format='point_source').**sliceDimensions(TSTEP=1)**

pt=pnc.pncopen(fname,format='point_source')

v2=filter(lambda x:pt.variables[x].ndim==2, [i for i in
pt.variables])

v3=filter(lambda x:pt.variables[x].ndim==3, [i for i in
pt.variables])

nt,nopts=pt.variables[v2[0]].shape

nhr,nvar,dt=pt.variables[v3[0]].shape

nv=len(v2)

tt=[i for i in xrange(20,24)]+[i for i in xrange(20)]

var=np.zeros(shape=(nv,nt,nopts))

for v in xrange(nv):

var[v,:,:]=pt.variables[v2[v]][:,:]

mn=np.zeros(shape=(nv,24,nopts))

for t in xrange(24):

for d in xrange(nt/24):

mn[:,tt[t],:]+=var[:,t+d*24,:]

mn=mn/int(nt/24)

for t in xrange(24):

for v in xrange(nv):

pt1.variables[v2[v]][:,:]=mn[v,t,:]

if t==0:

pt=pt1

else:

pt=pt.stack(pt1,'TSTEP')

pt.variables['TFLAG'][:,:,0]=[[2018288 for i in xrange(nvar)]
for j in xrange(24)]

pt.variables['TFLAG'][:,:,1]=[[i*10000 for j in xrange(nvar)]
for i in xrange(24)]

pt.SDATE=[SDATE]

pt.STIME=[STIME]

pt.EDATE=[SDATE]

pt.ETIME=[23]

fname2=fname+'nc'

pt.save(fname2)

fname3=fname+'_ok'

os.system('pncgen \--out-format=point_source -O '+fname2+'
'+fname3)

藍底部分程式碼將逐1小時檔案堆疊成24小時檔。

kuang@master /home/camxruns/2013/emis/tmp

$ cat ../time24.py

import numpy as np

import os

from PseudoNetCDF.camxfiles.Memmaps import uamiv

import netCDF4 as nc

NOTE='b'*60

SDATE=2018288

STIME=0

for D in ['2','3','4']:

fname='fortBE.'+D+'13.teds90.base11Mk311a1n10p10'

con_file= uamiv(fname,'r')

nt,nlay,nrow,ncol=(con_file.variables['SO2'].shape[i] for i in
xrange(4))

v4=filter(lambda x:con_file.variables[x].ndim==4, [i for i in
con_file.variables])

nv=len(v4)

var=np.zeros(shape=(nv,nt,nlay,nrow,ncol))

for v in xrange(nv):

var[v,:,:,:,:]=con_file.variables[v4[v]][:,:,:,:]

con_file.close

os.system('pncgen -f uamiv -a NOTE,global,o,c,'+NOTE+' -a
TSTEP,global,o,i,24 '+

' -a SDATE,global,o,i,'+str(SDATE)+

' -a STIME,global,o,i,'+str(STIME)+

' \--from-conv=ioapi \--to-conv=cf -O '+fname+' tmp.nc')

os.system('ncrcat -O -F -d TSTEP,1,24 tmp.nc tmp24.nc')

ncfile = nc.Dataset('tmp24.nc','r+')

ncfile.variables['TFLAG'][:,:,0]=[[2018288 for i in xrange(38)]
for j in xrange(24)]

ncfile.variables['TFLAG'][:,:,1]=[[i*10000 for j in
xrange(38)] for i in xrange(24)]

ncfile.close()

os.system('pncgen \--out-format=uamiv -O tmp24.nc '+fname+'T')

con_filO= uamiv(fname+'T','r+')

nt2,nlay,nrow,ncol=(con_filO.variables['SO2'].shape[i] for i in
xrange(4))

tt=[i for i in xrange(10,nt2)]+[i for i in xrange(10)]

mn=np.zeros(shape=(nv,nt2,nlay,nrow,ncol))

for t in xrange(24):

for d in xrange(nt/24):

mn[:,tt[t],:,:,:]+=var[:,t+d*24,:,:,:]

mn=mn/int(nt/24)

for v in xrange(nv):

con_filO.variables[v4[v]][:,:,:,:]=mn[v,:,:,:,:]

con_filO.SDATE=SDATE

con_filO.STIME=STIME

con_filO.close

v4在py27及py37有不同的作法，py37不會自動認為filter結果是個序列，必須再加以轉換，否則就只是個operator。

v4=**list**(filter(lambda x:con_file.variables[x].ndim==4, [i for i
in con_file.variables]))

面源部分綠色部分先將uam檔案轉成nc(ioapi格式)檔，因nc等並沒有NOTE及TSTEP之全域變數(global)，因此特別需要另外加上。轉完後使用**ncrcat**來切出所要的模版大小(粉紅色底部分)。

由於**pncgen**會讀取檔案的TFLAG做為全域變數中SDATE,
STIME等之設定，因此須先在nc檔中即準備好，有一致的全域變數與實質變數(灰底部分)。

pyncf (Pure Python NetCDF Reader)

一般python專案讀寫netCDF檔案，只是許多功能中附帶的元件，因此在使用上會顯得較為龐雜，不符合python精簡的精神。Pyncf即是為改變此一情況而寫的程式庫。pyncf為2016年4月公開的開放源程式庫[^91]，可以自GitHub網站[^92]下載使用。





web展示與GUI

與前述爬蟲程式相反，此類GUI程式則是將資料展示在網頁上、或者由GUI介面獲得手動輸入的資料。由於此類模組眾多，畫面品質有很大的落差，也有很多網友進行評比[^104]，以下以較新、推薦較多的Pyforms進行說明。此外，matplolib也有其GUI的widget，經由互動式繪圖，找到最好的圖形輸出，可以減省很多時間與檔案。

Pyforms

Pyforms雖然發展的歷史相較其他的模組都還短，但是受重視的程度卻很高。

python 繪圖與GIS

python繪圖以matplotlib功能最為強大，在圖形視窗界面(如jupyter與firefox界面)上以互動方式更能發揮。

然而對遠端控制或圖形數據太過龐大狀況，互動方式反而造成困難，因此還必須發展其他方式之繪圖。

而一般環境方面的空間繪圖需要套用底圖，目前這些軟體尚無法貼上台灣地圖，因此還是回到GIS系統中較為方便。

matplotlib程式庫

matplotlib是一個開源程式庫，延續自MATLAB的概念與特色，主要應用在數學相關的圖形繪製，包括主要excel能夠繪製的2D圖形。雖然MATLAB是一個付費軟體，然而在美國學界已經非常普遍，因此對matplotlib有其基本的熟悉度。詳情可以參考其官網的介紹[^105]，華人網友也提供不少中文的範例與說明。

傳統MATLAB的控制介面是互動式的對話框，matplot亦延續這項傳統，此外亦可由ipython(鍵入%pylab指令)或jupyter對話介面來控制產生的圖形，而這些對話方式都必須有X
window系統的支援($DISPLAY環境設定)。倘若無法提供DISPLAY，事實上matplotlib也提供了無顯示畫面的批次方式來產生圖檔(如以jupyter-notebook)，對於遠端控制或大圖檔存取困難而言，是非常必要的方式。

matplotlib範例

以下以histogram的繪製加以說明：

import numpy as np

import matplotlib.pyplot as plt

a=...

bins = np.linspace(0,179, 90)

plt.hist(a, bins, alpha=0.5)

plt.title("Hue Histogram")

plt.xlabel("Hue")

plt.ylabel("Frequency")

plt.show()

savefig('alldone', dpi=300)

範例中的a是0\~179的變數序列，histogram即為其出現次數(頻度)的分布。利用matplotlib可以輕鬆產生報告水準的圖形。

非互動式(批次式)之繪圖方式

環境研究過程中，常常會繪製同一型式之圖形以便進行比較，如時間序列的數據資料、或者重複不同測站的同一圖形模版，會需要以批次方式套用不同組資料進行繪圖。在MS
OFFICE軟體是使用VBA程式與巨集來連續產生，在GrAds亦是使用其個別的gs(GrAds
scripts)語言及繪圖函數來製作，而面對此一處境，正是python展現其語言共通性、彈性與強大支援之處。

Matplotlib.pyplot.subplot

以下範例是將每一測站的NO2及NH3隨風向變化的折線圖，以批次方式產生。程式常常會搭配pandas的DataFrame架構功能，較容易以篩選及迴圈方式處理。

```python
import numpy as np
import matplotlib.pyplot as plt
from pandas import *
...
d1={'station':Series(s1),'WD':Series(w1),'NO2':Series(N1),'NH3':Series(A1)}
data=DataFrame(d1) #整併4個序列
for temp in stn:
fig, ax = plt.subplots() #開始新的圖

dat = data[data['station']==int(temp)]  #篩選測站
wd = dat['WD'] #符合條件之風向
dates_f = [ss for ss in wd]
ax.plot(dates_f, dat['NO2'], label = "NO2,station:{0}".format(temp))
ax.plot(dates_f, dat['NH3'], label = "NH3,station:{0}".format(temp))
plt.xlabel("Wind direction") #X軸名稱
plt.ylabel("NO2 or NH3(ppb)") #y軸名稱
start, end = ax.get_xlim() #don't automaticly set
ax.xaxis.set_ticks(np.arange(start, end, stepsize=45/nwd)) #every 45
deg.
# ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#標籤在右外側
ax.legend() #標籤在右內側
plt.show() #一次繪出
```
![](media/image27.png){width="2.7740627734033247in"
height="1.9399792213473315in"}![](media/image28.png){width="2.6933759842519684in"
height="1.9085629921259843in"}

不同解析度畫出同一站的結果，左圖解析度22.5度，右圖5度。

開關界面顯示

對於連續產生圖檔的批次作業中，每一次圖形要輸出到螢幕上，對於使用者構成很大的干擾，如果是在互動介面(如ipython或jupyter)，可以用ioff()來關閉圖形顯示，用draw()來強制繪圖，用ion()來開啟。若不知道是否已經開啟或關閉互動模式，可以用[isinteractive](http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.isinteractive)()來確認。

在批次作業過程，則必須先確定使用(use[^106])backend的選項，如此系統才會停止在顯示器輸出，將結果儲存成檔案即可，如：

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
...
plt.savefig("sine.png",dpi=500,format="png")
```
matplotlib.use()的引數可以是'Agg'[^107]或者是'pdf'，內設則是'TkAgg'，因此會連結DISPLAY來輸出繪圖過程。可以用matplotlib.get_backend()指令來確認當下的backend是哪個選項。

網站服務之應用

非互動式的圖形產生方式，亦是網站圖形應用伺服器(web application
server)的核心程式，例如以下要介紹的plotly。

本節習題

以ISCST3輸出地面濃度為變數，利用matplotlib程式庫繪出地面濃度的histogram。

利用matplotlib.pyplot.contour(*args,
**kwargs)程式來繪製ISCST3地面濃度等值線圖。

#X,Y,Z由前述讀取程式(3.1.2 pp5.py)而來，

import matplotlib

import matplotlib.cm as cm

import matplotlib.mlab as mlab

import matplotlib.pyplot as plt

# matplotlib會自動找到最合適的x/y比例(aspect
ratio)，可能與實際差很多，可由網路找到適合的修正副程式

def adjustFigAspect(fig,aspect=1):

'''

Adjust the subplot parameters so that the figure has the correct

aspect ratio.

'''

xsize,ysize = fig.get_size_inches()

minsize = min(xsize,ysize)

xlim = .4*minsize/xsize

ylim = .4*minsize/ysize

if aspect \< 1:

xlim *= aspect

else:

ylim /= aspect

fig.subplots_adjust(left=.5-xlim,

right=.5+xlim,

bottom=.5-ylim,

top=.5+ylim)

matplotlib.rcParams['xtick.direction'] = 'out'

matplotlib.rcParams['ytick.direction'] = 'out'

# Create a simple contour plot with labels using default colors. The

# inline argument to clabel will control whether the labels are draw

# over the line segments of the contour, removing the lines beneath

# the label

fig = plt.figure()

adjustFigAspect(fig,aspect=0.8)

CS = plt.contour(X, Y, Z,50)

plt.clabel(CS, inline=1, fontsize=10)

plt.title('Simplest default with labels')

plt.show()

![](media/image29.png){width="2.9895833333333335in"
height="4.020833333333333in"}

Plotly網站

一般套裝軟體所畫的圖形多為制式老套，不太合用，而要搜尋期刊文獻上好看又適用的圖形方式，又如大海撈針事倍功半，是否有一個社群網站，人們願意將圖片貢獻出來，同時也提供製作方式可以免費下載，其他使用者也可以找到適合的圖表，
plotly就是這樣的一個地方。

基本上，plotly是一個遠端製圖的網站伺服器，免費供使用者製圖、下載、儲存，若是使用者願意，也可以分享給其他人。如果要更進一步的製圖功能或儲存空間，使用者也可以付費升級成菁英會員，付費後可以畫更多種不同類型的圖，也可以保持資料的隱密性。

Plotly網站使用教學可以參考其tutorial網頁[^108]。

安裝與登錄

Plotly為開源系統，可以免費安裝。要使用前先確定系統已經安裝plotly模組，若無，則執行sudo
pip install plotly自動安裝。

雖然是免費使用，為管理方便plotly還是需要登錄會員，包括上網登錄username並取得api_key。

https://plot.ly/ 到右邊下拉選單sign up(產生新帳號)或sign in(舊帳號登入)

sign up可使用fb或G+登入

登入後，在使用者名稱下拉選單進入Settings，左側選API
KEYS，或在https://plot.ly/settings/api 網頁，可以取得api_key。

將其copy到.py檔案中，如範例中斜體字部分：

import plotly.tools as tls

tls.set_credentials_file(username=['sinotec2']{.underline},api_key=['yuxyoghypd']{.underline})

這樣python在執行之後，就會自動跳出plotly網頁。然而要注意網站有單日繪圖的上限，如果超過可能要等明天才能看到結果。

### plotly程式撰寫重點

與一般python程式不同之處，在於plotly必須將結果上傳到該網站上去，一般遠端控制是先將圖形結果儲存成圖檔，再以檔案傳送軟體(如filezilla等)傳送到本地或其中地址。Plotly則是將圖形設定上傳，而在該網站上儲存並顯示圖形，使用者可以檢視後修改程式再傳，或在遠端網站直接修改圖片另存，直到滿意再下載使用。

import plotly(與其他python程式無異)

指定credentials_file。見前述。或者使用**sign_in**指令：

py.sign_in('DemoAccount', 'lr1c37zw81')

執行資料處理與繪圖程式，將圖形命名(如data)

確認伺服器已經連上網路。執行上傳，在遠端會出現檔名為斜體字之圖形。

plot_url = py.plot(data,
filename='simple-colorscales-colorscale')

範例：類似前述2.1.1.2

[#1\~4行是離線網站繪圖用]{.underline}

import plotly.plotly as py

import plotly.graph_objs as go

import plotly.tools as tls

tls.set_credentials_file(username='sinotec2',api_key='yuxyoghypd')

[# 以下與前述2.1.1.2 相同]{.underline}

import numpy

(nx,ny, delx)=(25,60,0.500)

datz=[] 空白的list準備裝資料

datx=[]

daty=[]

fname='SAL.yr' 要讀取的檔案名稱

with open(fname) as ftext: 開啟檔案，直到讀完為止。

for i in xrange(8): ISCST3會寫8行表頭，因此須先跳過

id = ftext.[readline]{.underline}()

for line in ftext: 剩下所有的行數

k=1 用k控制欄位，避免讀到文字無法轉換

for s in line.[split]{.underline}(): 內設是空白做間隔，予以切分資料

if k == 1: datx.append(float(s)) x值→裝進list

if k == 2: daty.append(float(s)) y值→裝進list

if k == 3: datz.append(float(s)) z值→裝進list

k=k+1

datx=numpy.array(datx) list轉成array

daty=numpy.array(daty)

datz=numpy.array(datz)

x=datx.reshape(ny,nx) 1維的array轉成2維的array

y=daty.reshape(ny,nx)

datz=datz.reshape(ny,nx)

datx=[]

daty=[]

for i in xrange(nx):datx.append(x[0,i]/1000.) 純粹用在plotly繪圖

for i in xrange(ny):daty.append(y[i,0]/1000.)

data = [go.Contour(x=datx,y=daty,z=datz, colorscale='Jet',) ]

plot_url = py.plot(data, filename='simple-colorscales-colorscale')

plotly
繪圖網站並未提供地圖套疊，其座標系統也不是等方向性(南北向壓縮了)，因此座標數字放不完整，必須減少有效位數(以公里表示)，否則無法辨識。

Plotly網站應用

執行.py程式之後，結果將會上傳到網站，位置為系統指定，目錄包括使用者名稱(底線部分)與序號(斜體字部分)，如：https://plot.ly/\~[sinotec2]{.underline}/0/#plot

上plotly網站、登入(sign in)、

登入後，在使用者名稱下拉選單進入My Files，

可選擇長條排列或是格狀排列，右側可勾選是否公開、分享、刪除、最愛等狀態。

點入該圖之後，在上方可以點選公開、下載(export)、編輯等，

1\. image有png與jpeg兩種格式，

2.資料有csv/excel/ppt格式，

3\. code有python/matlab/R/plotly.js/node.js/Julia等格式，

4\. HTML也可以下載成zip封包

也可以直接在網站上輸入或上傳資料，繪製xy plot等統計、科學圖形。

結果：如下圖所示：

![](media/image30.png){width="5.796000656167979in"
height="4.34700021872266in"}

Plotly網站具有每日繪圖的上限次數，如果超過會發信息如下：

PlotlyError: Hey there! You've hit one of our API request limits.

To get unlimited API calls(10,000/day), please upgrade to a paid plan.

UPGRADE HERE: https://goo.gl/i7glmM

Plotly應用習題

試將前一習題matplotlib所產生的histogram圖形，在plotly網站呈現。

matplotlib亦有contour模組，試利用plotly網站將其繪製成圖。

試利用網友提供的風玫瑰程式[^109]，套入前述plume
model的風速風向頻率數據，繪製風玫瑰圖，重要提示：

需要用到Pandas與colorlover等2個程式庫

Pandas的資料結構(dataframe)必須經篩選及選取，前者指令如：ff=wind_bins_df[wind_bins_df['intensity']==i]後者指令如r=list(ff['freq'])。

Colorlover可能有些色階無法接受太多的階數，可以直接由colorlover.scales指令的結果來挑選適合的色階。

List不適合用在for
loop累加，如果要累加，建議還是要用numpy.array()指令來定義變數(見前述numpy.cumsum指令)。

import plotly.plotly as py

import plotly.graph_objs as go

trace=[] #每一圈(層)是trace序列的一個項目

for i in xrange(9,0,-1): # for each level of wind
speed(intensity)從外到內

item = go.Area(

r=list(cum[i,0:16]), #radius,需要16個方向的徑向長度

t=orient[0:16], #方向名稱(每層都一樣)

marker=dict(color=cl.scales['10']['div']['PRGn'][i]),
#要先測試

name=intense[i] + ' m/s' )

trace.append(item)

layout = go.Layout(

title='Wind Speed Distribution in Laurel, NE',

font=dict(size=16),

legend=dict(font=dict(size=16)),

radialaxis=dict(ticksuffix='%'),

orientation=270)

fig = go.Figure(data=trace, layout=layout)

py.iplot(fig, filename='polar-area-chart')

#plot_url = py.plot(data, filename='polar-area-chart')

![](media/image31.png){width="5.208333333333333in" height="4.6875in"}

Bokeh

Bokeh is a Python interactive visualization library that targets modern
web browsers for presentation. Its goal is to provide elegant, concise
construction of novel graphics in the style of D3.js, and to extend this
capability with high-performance interactivity over very large or
streaming datasets. Bokeh can help anyone who would like to quickly and
easily create interactive plots, dashboards, and data applications.

QGIS之應用

GIS是環境資訊應用過程中，經常使用到的軟體系統。由於python在資料處理與集合、矩陣計算等方面具有強大功能，因此全球各大GIS系統均提供了系統內執行python程式的界面，以擴充GIS使用的彈性。

考慮我國政府開放資訊平台推廣QGIS之使用，可以到QGIS的官網下載安裝[^110]，並連線到政府之WMTS[^111]，本文也以此為範例，做為python應用之說明。QGIS上使用python可以參考QGIS官網之說明文件[^112]。

經緯度與UTM之轉換

可以採用網友提供的套件，執行速度較完整的lib更快速，以下是以台灣中心做為LCP座標系統的中心點，。

from pypinyin import pinyin, lazy_pinyin

from pandas import *

import utm

def lpy_ss(cha):

try:

s=lazy_pinyin(cha.decode('utf8'))

except:

ss=cha

else:

ss=''

for j in s:

ss=ss+j

cha=''

for s in ss:

if len(s.encode('utf8'))==3 and len(s) == 1:s='-'

cha=cha+s

!wget
[[https://www.freeway.gov.tw/Upload/DownloadFiles/%e5%9c%8b%e9%81%93%e8%a8%88%e8%b2%bb%e9%96%80%e6%9e%b6%e5%ba%a7%e6%a8%99%e5%8f%8a%e9%87%8c%e7%a8%8b%e7%89%8c%e5%83%b9%e8%a1%a8.csv]{.underline}](https://www.freeway.gov.tw/Upload/DownloadFiles/%25e5%259c%258b%25e9%2581%2593%25e8%25a8%2588%25e8%25b2%25bb%25e9%2596%2580%25e6%259e%25b6%25e5%25ba%25a7%25e6%25a8%2599%25e5%258f%258a%25e9%2587%258c%25e7%25a8%258b%25e7%2589%258c%25e5%2583%25b9%25e8%25a1%25a8.csv)

!a=$(ls --rt *.csv\|tail --n1);mv $a coord.csv

df_xy=read_csv('coord.csv')

col_xy=[lpy_ss(i) for i in df_xy.columns]

col_xy[2]=col_xy[2].replace('qidianjiaoliudao','qidianjiaoliudao.2')

df_xy.columns=col_xy

for j in
['qidianjiaoliudao','qidianjiaoliudao.2','guodaobie','fangxiang']:

df_xy[j]=[lpy_ss(i) for i in df_xy[j]]

xcent,ycent,izone,s=utm.from_latlon(23.61, 120.99)

df_xy['x_lcp']=[utm.from_latlon(lat,lon)[0]-xcent

for lat,lon in
zip(list(df_xy['beiwei']),list(df_xy['dongjing'])])

df_xy['x_lcp']=[list(utm.from_latlon(lat,lon))[0]-xcent

for lat,lon in
zip(list(df_xy['beiwei']),list(df_xy['dongjing']))]

雖然UTM與台灣常用的twd97有差距，但只要對同一組經緯度進行轉換，即可得到相對的座標了。

Xcent97,Ycent97= 248417,2613022

df_xy['x97']=[int((i+Xcent97)/1000)*1000 for i in
df_xy['x_lcp']]

df_xy['y97']=[int((i+Ycent97)/1000)*1000 for i in
df_xy['y_lcp']]

圖檔之載入

Python對話窗由QGIS視窗頂「外掛程式(P)」下拉選單進入，為一傳統python的對話窗，並沒有ipython或jupyter的功能。

from PyQt4.QtCore import QFileInfo

fileName
="C:/Users/4139/MyPrograms/python2.7/py_homework/ISCST/pp5.grd"

fileInfo = QFileInfo(fileName)

baseName = fileInfo.baseName()

iface.addRasterLayer(fileName,baseName)

rlayer.width(), rlayer.height()

s=[]

for i in rlayer.extent().toString().split(':'):

for j in i.split(','):

s.append(float(j))

[xmin,ymin,xmax,ymax]=s

若同時要輸入好幾層圖形，python的輸入方式就很方便了。但要注意檔名的約定方式，目錄是用正斜線(/slash)，磁碟機是用冒號分開。

layer = iface.activeLayer()[^113]

layer.name()

P=0

for f in layer.getFeatures():

P=P+ f['P_CNT']

print P

Try more:

GeospatialPython.com
[[http://geospatialpython.com/]{.underline}](http://geospatialpython.com/)

Points, Polylines, Polygons, Pixels, Python!

Job notes

.Scan diagram as tiff or directively as tiff

->histogram and statistics of occurrence of colors

->plot.py and web-site

->RGB vs HSV

->RGB vs grayscale

.delete the black lines and characters

->QGIS raster display

.km_method and most_closed_color

->parallelization and importing

->MatLibPlot

.assign the corresponding LU to the color

->checking the legend colors

->one color, one tiff output

.reading the LU's from corrected color

->Color2LU.def

.modifying the LU with dict.grd or topo_m

->load and save texts and surfer .GRDs

->corresponding southern and northern most-points of the map

->transpose and reshape of a matrix

->post a huge grd in QGIS system

.Filling or interpolation of the blank or holes

->smoothing (not work)

->script.interpolate(small scale in dimensions)

->max and index

.wrap in the avrg format

[^1]: https://zh.wikipedia.org/wiki/Python#.E6.AD.B7.E5.8F.B2

[^2]: ABC，一種程式語言與編程環境，起源於荷蘭國家數學與計算機科學研究中心，最初的設計者為Leo
    Geurts、Lambert Meertens與Steven
    Pemberton。程式風格受到ALGOL-68的影響，最初用來取代AWK、BASIC、與Pascal，目標是在教導非專業的程式設計師學習如何開始寫程式。

[^3]: 葛冬梅(2005)
    自由軟體？開放源碼軟體？還是開放原始碼軟體？「這些用詞皆表示這樣一個軟體具有不收取授權金、原始碼開放給任何人取得等等的特色。」

    [[http://www.openfoundry.org/tw/legal-column-list/508-2010-07-15-10-50-34]{.underline}](http://www.openfoundry.org/tw/legal-column-list/508-2010-07-15-10-50-34)

[^4]: UNIX
    Shell本身是一個交談式的命令環境，也是一個功能強大的直譯式程式語言(Interpreter)，有迴圈、判斷、文字處理、數字計算、檔案處理等功能。

[^5]: []{.underline}
    一種自動的記憶體管理機制。當一個電腦上的動態記憶體不再需要時，就應該予以釋放，以讓出記憶體，這種記憶體資源管理，稱為垃圾回收（garbage
    collection）。

[^6]: Unicode（中文：萬國碼、國際碼、統一碼、單一碼）是電腦科學領域裡的一項業界標準。它對世界上大部分的文字系統進行了整理、編碼，使得電腦可以用更為簡單的方式來呈現和處理文字。https://zh.wikipedia.org/wiki/Unicode

[^7]: 戀花蝶的博客（http://blog.csdn.net/lanphaday

[^8]: KATHARINE JARMUL(2016) INTRODUCTION TO DATA SCIENCE: HOW TO "BIG
    DATA" WITH PYTHON, OCTOBER 18, 2016,
    http://dataconomy.com/2016/10/big-data-python/

[^9]: 中國大數據2016-04-25 00:00:00, https://read01.com/8d3y88.html

[^10]: R語言，一種自由軟體程式語言與操作環境，主要用於統計分析、繪圖、資料探勘。R本來是由來自紐西蘭奧克蘭大學的羅斯·伊哈卡和羅伯特·傑特曼(Ross
    Ihaka and Robert
    Gentleman)開發（也因此稱為R），現在由「R開發核心團隊」負責開發。R基於S語言的一個GNU計劃專案，所以也可以當作S語言的一種實現，通常用S語言編寫的代碼都可以不作修改的在R環境下執行。R的語法是來自Scheme。

[^11]: GPU圖形處理器（英語：graphics processing
    unit，縮寫：GPU），又稱顯示核心、視覺處理器、顯示晶片或繪圖晶片，是一種專門在個人電腦、工作站、遊戲機和一些行動裝置（如平板電腦、智慧型手機等）上執行繪圖運算工作的微處理器。

[^12]: NLP神經語言規劃（Neuro-Linguistic
    Programming）又譯作神經語言程序學、身心語言程序學，NLP就是對成功人士的語言及思考模式進行解碼，並有系統地將之歸納成一套可模仿，可學習的成功模式。

[^13]: Scala（發音為/ˈskɑːlə,
    ˈskeɪlə/）是一門多範式的程式語言，設計初衷是要整合物件導向編程和函數語言程式設計的各種特性。Scala
    是新一代的JVM 語言，作為最普及程式語言之一Java
    的替代選擇，正逐漸贏得用戶青睞。

[^14]: Apache Spark™ is a fast and general engine for large-scale data
    processing. http://spark.apache.org/

[^15]: 請問Python在業界都用來寫什麼居多? Sat Oct 11 06:24:01 2014,
    https://www.ptt.cc/bbs/Soft_Job/M.1412979844.A.A8D.html

[^16]: GIL，即全局解釋器鎖（Global Interpreter
    Lock），是電腦程式設計語言解釋器用於同步執行緒的工具，使得任何時刻僅有一個執行緒在執行。

[^17]: Nick Coghlan's Python Notes (2015) Efficiently Exploiting
    Multiple Cores with Python
    http://python-notes.curiousefficiency.org/en/latest/python3/multicore_python.html

[^18]: 即時編譯（英語：Just-in-time
    compilation），又譯及時編譯、實時編譯，動態編譯的一種形式，是一種提高程式執行效率的方法。通常，程式有兩種執行方式：靜態編譯與動態直譯。靜態編譯的程式在執行前全部被翻譯為機器碼，而直譯執行的則是一句一句邊執行邊翻譯。

[^19]: PyPy's fork of Numpy, NumPyPy, https://bitbucket.org/pypy/numpy

[^20]: 正則(正規)表示式Regular
    Expression，使用單個字串來描述、符合一系列符合某個句法規則的字串。在很多文字編輯器裡，正則運算式通常被用來檢索、取代那些符合某個模式的文字。

    許多程式設計語言都支援利用正則運算式進行字串操作。

[^21]: Apache Hadoop是一款支援資料密集型分布式應用程式並以Apache
    2.0許可協議發布的開源軟體框架。它支援在商品硬體構建的大型集群上運行的應用程式。Hadoop是根據Google公司發表的MapReduce和Google檔案系統的論文自行實作而成。

[^22]: 訊息傳遞介面/介面（英語：Message Passing
    Interface，縮寫MPI）是一個平行計算的應用程式介面（API），常在超級電腦、電腦叢集等非共享內存環境程式設計。

[^23]: Web伺服器閘道介面（**Python Web Server Gateway
    Interface**，縮寫為WSGI）是為[[Python]{.underline}](https://zh.wikipedia.org/wiki/Python)語言定義的[[Web伺服器]{.underline}](https://zh.wikipedia.org/wiki/%25E7%25B6%25B2%25E9%25A0%2581%25E4%25BC%25BA%25E6%259C%258D%25E5%2599%25A8)和[[Web應用程式]{.underline}](https://zh.wikipedia.org/wiki/%25E7%25BD%2591%25E7%25BB%259C%25E5%25BA%2594%25E7%2594%25A8%25E7%25A8%258B%25E5%25BA%258F)或[[框架]{.underline}](https://zh.wikipedia.org/wiki/Web%25E5%25BA%2594%25E7%2594%25A8%25E6%25A1%2586%25E6%259E%25B6)之間的一種簡單而通用的[[介面]{.underline}](https://zh.wikipedia.org/wiki/%25E4%25BB%258B%25E9%259D%25A2_(%25E7%25A8%258B%25E5%25BC%258F%25E8%25A8%25AD%25E8%25A8%2588))。自從WSGI被開發出來以後，許多其它語言中也出現了類似介面。https://zh.wikipedia.org/wiki/Web服务器网关接口

[^24]: Django (/ˈdʒæŋɡoʊ/ jang-goh) 是個用 Python
    寫成的，免費而且開放原始碼的 Web 應用程式框架。他是個 Web 框架 -
    就是一堆零件的組成，可以幫助你輕鬆快速的開發網站。https://carolhsu.gitbooks.io/django-girls-tutorial-traditional-chiness/content/django/README.html

[^25]: 蠕蟲病毒是一種常見的計算機病毒。它是利用網路進行複製和傳播，傳染途徑是通過網路和電子郵件。

[^26]: firapria is a lightweight library to extract pollution indices
    from Airparif website for IDF (法蘭西島大區).
    https://pypi.python.org/pypi/firapria

[^27]: OS是管理計算機硬體與軟體資源的電腦程式，同時也是計算機系統的核心與基石。
    作業系統需要處理如管理與配置內存、決定系統資源供需的優先次序、控制輸入與輸出裝置、操作網絡與管理文件系統等基本事務。
    作業系統也提供一個讓使用者與系統互動的操作界面。

[^28]: One Laptop Per Child，OLPC,
    由麻省理工學院多媒體實驗室發起並組織為一個非營利組織，藉由生產接近100美元的筆記型電腦給對這項計畫有興趣的開發中國家，由該國政府直接提供給兒童使用，降低知識鴻溝，故又稱百元電腦。

[^29]: SCons: A software construction tool - SCons
    是一個開放源代碼、以Python 語言編寫下一代的程序建造工具。

[^30]: Fortran (formula translation)
    1957年由IBM開發出，是世界上第一個被正式採用並流傳至今的高階程式語言。https://zh.wikipedia.org/wiki/Fortran

[^31]: Applications for Python, https://www.python.org/about/apps/

[^32]: the Python Package Index, https://pypi.python.org/pypi

[^33]: https://www.foolegg.com/how-to-build-a-python-programming-environment-on-windows/

[^34]: Python 2.7.0 Release,
    https://www.python.org/download/releases/2.7/

[^35]: [[http://www.ascc.sinica.edu.tw/putty]{.underline}](http://www.ascc.sinica.edu.tw/putty)

[^36]: [[https://filezilla-project.org/download.php]{.underline}](https://filezilla-project.org/download.php)

[^37]: [[https://mobaxterm.mobatek.net/]{.underline}](https://mobaxterm.mobatek.net/)

[^38]: https://www.teamviewer.com/zhTW/

[^39]: Walt McNab, NUMERICAL ENVIRONMENTAL, Coding examples for
    quantitative environmental data analysis and simulation,
    https://numericalenvironmental.wordpress.com/

[^40]: https://github.com/NumericalEnvironmental/Monte_Carlo_atmospheric_plume

[^41]: The Python Tutorial,
    https://docs.python.org/2.7/tutorial/index.html

[^42]: [[https://github.com/ldkrsi/jieba-zh_TW]{.underline}](https://github.com/ldkrsi/jieba-zh_TW)
    或
    [[https://github.com/fxsjy/jieba]{.underline}](https://github.com/fxsjy/jieba)

[^43]: https://zh.wikipedia.org/wiki/百分号编码

[^44]: http://fecbob.pixnet.net/blog/post/43573138-將漢字轉換成中文拼音的python庫

    http://pypinyin.mozillazg.com/zh_CN/master/index.html

[^45]: 'bytes' object has no attribute 'encode'
    https://www.jianshu.com/p/a4cf632d97f1

[^46]: Tim Arnold (2014)Manipulating PDFs with Python, Nov 6, 2014,
    https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167

[^47]: http://163.29.251.188/botedata/交通流量/103年度/路口/NI003.pdf

[^48]: pdftotext − Portable Document Format (PDF) to text converter
    (version 4.00) Copyright 2017 Glyph & Cog, LLC,
    https://www.xpdfreader.com/pdftotext-man.html

[^49]: 整體說明:
    [[https://www.zhihu.com/question/47480852]{.underline}](https://www.zhihu.com/question/47480852),
    [[https://zhuanlan.zhihu.com/p/29410051]{.underline}](https://zhuanlan.zhihu.com/p/29410051),
    python 3:
    [[https://pypi.org/project/pdfminer3k/]{.underline}](https://pypi.org/project/pdfminer3k/)

[^50]: [[https://www.ilovepdf.com/split_pdf#split,range]{.underline}](https://www.ilovepdf.com/split_pdf#split,range)

[^51]: [[https://zhtw.109876543210.com/]{.underline}](https://zhtw.109876543210.com/)

[^52]: Guo-Kai Chen,
    [[https://medium.com/@b98606021/實用心得-tesseract-ocr-eef4fcd425f0]{.underline}](https://medium.com/@b98606021/%25E5%25AF%25A6%25E7%2594%25A8%25E5%25BF%2583%25E5%25BE%2597-tesseract-ocr-eef4fcd425f0)

    字形包:[[https://github.com/tesseract-ocr/tessdata_best/blob/master/chi_sim.traineddata]{.underline}](https://github.com/tesseract-ocr/tessdata_best/blob/master/chi_sim.traineddata)

[^53]: http://pandas.pydata.org/pandas-docs/stable/10min.html#string-methods

[^54]: Loc vs. iloc vs. ix vs. at vs. iat?
    https://stackoverflow.com/questions/28757389/loc-vs-iloc-vs-ix-vs-at-vs-iat

[^55]: .set_index('...')以特定欄位作為索引，該欄位的內容不會消失，但是欄位名稱則不見了，因此將其還原成一般欄位時，則必須指定其欄位名稱(如下例中的'plant')，與其內容(即為index的內容)，如下列方法：

    df_2pv[**'plant'**]=df_2pv.**index** #reset the plant as a
    column

[^56]: Indexing and Selecting Data, pandas 0.20.1 documentation ,
    http://pandas.pydata.org/pandas-docs/stable/indexing.html

[^57]: map() Format: map(function, sequence)
    iterate所有的sequence的元素並將傳入的function作用於元素，最後以List作為回傳值。請參考下面例子:
    https://dotblogs.com.tw/law1009/2013/07/09/109217

    >>> a = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    >>> def fn(x):

    \... return x*2

    >>> c = map(fn, a)

    >>> c

    [2, 4, 6, 8, 10, 12, 14, 16, 18]

[^58]: http://mcsp.wartburg.edu/zelle/python/ppics1/code/chapter11/wordfreq.py

[^59]: Python CALENDAR Tutorial with Example,
    [[https://www.guru99.com/calendar-in-python.html]{.underline}](https://www.guru99.com/calendar-in-python.html)

[^60]: http://www.python-excel.org/

[^61]: A Python library to read/write Excel 2010 xlsx/xlsm files,
    https://openpyxl.readthedocs.io/en/default/

[^62]: Creating Excel files with Python and XlsxWriter,
    https://xlsxwriter.readthedocs.io/

[^63]: TIFF, https://zh.wikipedia.org/wiki/TIFF

[^64]: http://pydoc.net/Python/fatiando/0.3/fatiando.gridder/

[^65]: Engage Your 3D Data in the Conversation, Steno3D is data
    agnostic. We support visualization of points, point clouds, lines,
    surfaces and volumes, with more functionality on its way. Steno3D is
    also file agnostic. We don't support file types, we support you and
    your data. We enable data upload using an open-source Python client
    library. Support for more languages is coming soon!
    https://steno3d.com/

[^66]: [[https://github.com/3ptscience/steno3d-surfer/blob/master/steno3d_surfer/parser.py]{.underline}](https://github.com/3ptscience/steno3d-surfer/blob/master/steno3d_surfer/parser.py)

[^67]: KML Samples - Google Developers,
    [[https://developers.google.com/kml/documentation/KML_Samples.kml]{.underline}](https://developers.google.com/kml/documentation/KML_Samples.kml),

    KML Tutorial,
    https://developers.google.com/kml/documentation/kml_tut

[^68]: https://blog.xuite.net/lwkntu/blog/51204497-%28GM-5%29Google+Map讀取KML檔

[^69]: http://maps.google.com/mapfiles/kml/paddle/wht-blank.png

[^70]: Tom.chen, Python converter between TWD97 and WGS84,
    https://pypi.org/project/twd97/

[^71]: scipy.interpolate.griddata,
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html

[^72]: https://stackoverflow.com/questions/5666056/matplotlib-extracting-data-from-contour-lines

[^73]: https://github.com/pivaldi/pi-google-maps-api/blob/master/res/france/regions/54/contour.kml

[^74]: KML Reference
    [[https://developers.google.com/kml/documentation/kmlreference]{.underline}](https://developers.google.com/kml/documentation/kmlreference)

[^75]: [[http://www.zonums.com/gmaps/kml_color/]{.underline}](http://www.zonums.com/gmaps/kml_color/)

[^76]: [[http://www.netdelight.be/kml/index.php]{.underline}](http://www.netdelight.be/kml/index.php)

[^77]: [[http://www.zonums.com/gmaps/kml_color/]{.underline}](http://www.zonums.com/gmaps/kml_color/)

[^78]: Color Ramps Generator, Color Ramp: Create color-ramp lists for
    you data and maps
    [[http://www.zonums.com/online/color_ramp/]{.underline}](http://www.zonums.com/online/color_ramp/)

[^79]: Hexadecimal color code for transparency,
    https://gist.github.com/lopspower/03fb1cc0ac9f32ef38f4

[^80]: Russ Rew, 1999, Software for Manipulating or Displaying NetCDF
    Data, http://www.unidata.ucar.Edu/packages/netcdf/software.html.

[^81]: Chris Slocum(2012) Python - NetCDF reading and writing example
    with plotting , Colorado State University,
    [[http://www.unidata.ucar.edu/software/netcdf/]{.underline}](http://www.unidata.ucar.edu/software/netcdf/)

    netcdf4-python,
    [[https://code.google.com/archive/p/netcdf4-python/]{.underline}](https://code.google.com/archive/p/netcdf4-python/)

    [[http://unidata.github.io/netcdf4-python/]{.underline}](http://unidata.github.io/netcdf4-python/)

[^82]: http://schubert.atmos.colostate.edu/\~cslocum/netcdf_example.html

[^83]: Supported specifiers include: C{'S1' or 'c' (NC_CHAR),
    'i1' or 'b' or 'B'

    (NC_BYTE), 'u1' (NC_UBYTE), 'i2' or 'h' or 's'
    (NC_SHORT), 'u2'

    (NC_USHORT), 'i4' or 'i' or 'l' (NC_INT), 'u4' (NC_UINT),
    'i8' (NC_INT64),

    'u8' (NC_UINT64), 'f4' or 'f' (NC_FLOAT), 'f8' or 'd'
    (NC_DOUBLE)}.

    C{datatype} can also be a L{CompoundType} instance

    (for a structured, or compound array), a L{VLType} instance

    (for a variable-length array), or the python C{str} builtin

    (for a variable-length string array). Numpy string and unicode
    datatypes with

    length greater than one are aliases for C{str}.

    [[https://unidata.github.io/netcdf4-python/netCDF4/index.html#netCDF4.Dataset.createVariable]{.underline}](https://unidata.github.io/netcdf4-python/netCDF4/index.html#netCDF4.Dataset.createVariable)

[^84]: http://www.nies.go.jp/REAS/

[^85]: netCDF Operator, http://nco.sourceforge.net/

[^86]: The Generic Mapping Tools, http://gmt.soest.hawaii.edu/

[^87]: Github網站<https://github.com/barronh/pseudonetcdf>
    個人網站[[http://www.barronh.com/home]{.underline}](http://www.barronh.com/home)
    Pypi平台<https://pypi.python.org/pypi/PseudoNetCDF/2.0.1>

[^88]: r+：可读可写，若文件不存在，报错；w+:
    可读可写，若文件不存在，创建https://blog.csdn.net/ztf312/article/details/47259805

[^89]: 如https://github.com/barronh/pseudonetcdf/issues/22

[^90]: /cluster/CALPUFF6/CALPOST/CALPOST_v7.1.0_L141010/con2avrg.f

[^91]: http://geospatialpython.com/2016/04/pure-python-netcdf-reader.html

[^92]: Pure Python NetCDF file reader and writer,
    https://github.com/karimbahgat/pyncf

[^93]: Beautiful Soup Documentation,
    https://www.crummy.com/software/BeautifulSoup/bs4/doc/

[^94]: 開始使用Python撰寫網路爬蟲 ( Crawler )
    http://www.largitdata.com/course/5/

[^95]: 認識 Selenium,
    https://learngeb-ebook.readbook.tw/intro/selenium.html

[^96]: Unable to open Firefox browser using Selenium
    [[https://stackoverflow.com/questions/42732841/unable-to-open-firefox-browser-using-selenium]{.underline}](https://stackoverflow.com/questions/42732841/unable-to-open-firefox-browser-using-selenium)

    版本說明：selenium, geckodrive以及firefox的版本都必須匹配才行。例如
    firefox 52.0/geckodrive 0.16\~0.17/selenium 3.6,
    版本差異太大將導致程式不能運作。各版本的geckodrive可以自網路上下載，要注意32或64位元。
    https://github.com/mozilla/geckodriver/releases

[^97]: ChromeDriver - WebDriver for Chrome
    https://sites.google.com/a/chromium.org/chromedriver/downloads

[^98]: How to parse Selenium driver elements?
    https://stackoverflow.com/questions/30945212/how-to-parse-selenium-driver-elements

[^99]: [[https://gist.github.com/youngsterxyf/5088794]{.underline}](https://gist.github.com/youngsterxyf/5088794)

[^100]: 「可延伸標示語言」(Extensible Markup Language，
    XML)是一個讓文件能夠很容易地讓人去閱讀，同時又很容易讓電腦程式去辨識的語言格式和語法，它自SGML(Standard
    Generalized Markup Language)延伸而來。

[^101]: https://tcgbusfs.blob.core.windows.net/blobtisv/GetVDDATA.gz

    http://data.taipei/opendata/datalist/datasetMeta;jsessionid=0FA13B2E7710FB04C4CD236A509FC007?oid=e57afe7f-3c9e-4f31-9208-eed859a92600

[^102]: 用 ElementTree 在 Python 中解析 XML
    http://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/processing-xml-in-python-with-element-tree.html

[^103]: HyperText Markup Language

[^104]: 八款常用的 Python GUI 開發框架推薦
    https://stackoverflow.max-everyday.com/2018/05/python-gui-framework/

    2017年最棒的七個Python圖形應用GUI開發框架

    https://kknews.cc/other/meq388z.html

[^105]: matplotlib,
    [[http://matplotlib.org/]{.underline}](http://matplotlib.org/)
    或者是scpipy網站之介紹
    [[http://www.scipy-lectures.org/intro/matplotlib/matplotlib.html]{.underline}](http://www.scipy-lectures.org/intro/matplotlib/matplotlib.html)

[^106]: tkinter.TclError: couldn't connect to display "localhost:18.0"
    [[http://stackoverflow.com/questions/19518352/tkinter-tclerror-couldnt-connect-to-display-localhost18-0]{.underline}](http://stackoverflow.com/questions/19518352/tkinter-tclerror-couldnt-connect-to-display-localhost18-0)

    Matplotlib in a web application server,
    [[http://matplotlib.org/faq/howto_faq.html#matplotlib-in-a-web-application-server]{.underline}](http://matplotlib.org/faq/howto_faq.html%23matplotlib-in-a-web-application-server)

[^107]: Anti-Grain Geometry, Anti-Grain Geometry (AGG) is a high-quality
    2D rendering library written in C++.
    https://en.wikipedia.org/wiki/Anti-Grain_Geometry

[^108]: https://plot.ly/python/ipython-notebook-tutorial/

[^109]: [[https://plot.ly/python/wind-rose-charts/]{.underline}](https://plot.ly/python/wind-rose-charts/)或[[https://plot.ly/pandas/wind-rose-charts/]{.underline}](https://plot.ly/pandas/wind-rose-charts/)

[^110]: Download QGIS for your platform,
    http://www.qgis.org/en/site/forusers/download.html

[^111]: OpenGIS [W]{.underline}eb [M]{.underline}ap [T]{.underline}ile
    [S]{.underline}ervice:
    •台灣百年歷史地圖http://gis.sinica.edu.tw/tileserver/wmts

    •國土測繪圖資服務雲WMTS服務（Open
    Data）http://maps.nlsc.gov.tw/OpenData/wmts

    •國土利用調查(WMTS)
    http://maps.nlsc.gov.tw/S_Maps/wmts/LUIMAP/default/EPSG%3A3857/6/27/53

    •土壤管理組圖
    http://soilsurvey.tari.gov.tw/SOA_WMS/SimpleWMS.aspx?VERSION=1.1.1&LAYERS=土壤管理組圖&STYLES=&BgColor=0xFFFFFF&TRANSPARENT=TRUE&SRS=EPSG:4326&BBOX=117.20868394531248,20.440352622553142,124.71234605468748,26.875979270148132&WIDTH=1106&HEIGHT=595

[^112]: PyQGIS Developer Cookbook,
    http://docs.qgis.org/2.18/en/docs/pyqgis_developer_cookbook/index.html

[^113]: Getting Started With Python Programming,
    http://www.qgistutorials.com/en/docs/getting_started_with_pyqgis.html
