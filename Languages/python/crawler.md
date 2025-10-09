網頁內容之讀取 (爬蟲程式crawler)

閱讀網站已經是現代人每天必做的事，是否有程式界面可以自己閱讀網站的內容，篩選使用者有興趣的內容，進而操作網頁的動作呢？答案是肯定的，一般稱之為crawler爬蟲程式。做為crawler程式，其基本語言可以是javascripts或其他語言，當然也可以是python。

Python模組中的爬蟲程式一般使用requests來抓取頁面內容，也進而使用BeautifulSoup[^93]
進行內容的剖析[^94]，再以讀取結果內容進行程式設計，可以說是非常完整。

直讀與行動(selenium)

此處除了前述BS的解析之外，進一步介紹更為直覺的selenium[^95]來讀取網頁內容。

建立驅動程式

首先一樣要先輸入模組，建立驅動程式，並且開啟網頁：

$ cat start.py

from selenium import webdriver

driver =
webdriver.Firefox(**executable_path="/usr/bin/geckodriver"**)

driver.get("http://www.python.org")

若無錯誤，程式會開啟python的官方網站的首頁。小括弧的內容若是已經可以由$PATH環境變數可以找得到，就不必特別寫，系統還是找得到執行檔，寫出來是提醒當工作站firefox不能啟動時，可能是geckodriver的版本不對、或不存在或路徑找不到，需要進一步查證[^96]。

除了linux上內設是firefox做為瀏覽器之外，selenium以可以接受chrome、safari與ie，以下為MS
windows上使用chrome的驅動方式。

driver = webdriver.Chrome \\

('C:/Users/4139/AppData/Local/Google/Chrome/Application/chromedriver_win32/chromedriver.exe')

執行檔並不是chrome.exe而是chromedriver.exe，可以在google網站[^97]下載適合的版本。即使是在PC上，程式所在位置可以接受正斜線"/"。Linux上selenium當然也可以執行chrome，但是chrome已經不支援CentOS6了，如果是CentOS6環境，只能使用firefox。

firefox對https格式的限制，然而在chrome是OK的。

字詞解析程式(parser)

如同前述butifulSoup，selenium也可以列出網頁所讀到的內容，其命名方式更為直覺，如下例[^98]：

for element in
driver.find_elements_by_css_selector("header.main-header"):

print(element.text)

(result=...)

Search This Site

GO

Socialize

...

Python is a programming language that lets you work quickly

and integrate systems more effectively. Learn More

如果使用firefox，按下右鍵選取"inspect
elements(Q)"便會出現如下圖的分割畫面，firefox會將內容按scc選擇器類別予以分類，其中的header類即為所輸出所示的內容文字。

![](media/image25.png){width="5.568362860892388in"
height="4.446229221347331in"}

由於python程式設計經常使用試誤法，需要掌握所有的內容，從中挑選後續要執行的對象，因此find_element...的過程便非常重要。

點擊、選單等動作

啟動瀏覽器驅動程式之後，python就可以透過驅動程式控制網頁，一般操作網頁最重要的動作包括點擊、下拉選單等，捲軸是因為畫面不夠，因此使用者要看到其他頁面時進行捲軸上下拉動，而我們針對頁面要直行的對象內容已經有所掌握了，因此不需要拉動捲軸即可直接執行動作。以下為點擊ID、xpath與下拉選單(點擊與選擇)的副程式範例。

from selenium import **webdriver**

from selenium.webdriver.support.ui import Select

def **clkid**(ID): #click the id

button_element = **driver**.find_element_by_id(ID)

button_element.click()

return

def **clkpath**(ID): #click the xpath (no use)

button_element = **driver**.find_element_by_xpath(ID)

button_element.click()

return

def **SelectByIDnValue**(ID,v): #click and select by value

select = **Select**(driver.find_element_by_id(ID))

select.select_by_value(v)

return

#enter the website

**driver** = **webdriver**.Chrome( \\

'C:/Users/4139/AppData/Local/Google/Chrome/Application/chromedriver_win32/chromedriver.exe')

driver.get('https://cris.hpa.gov.tw/pagepub/Home.aspx?itemNo=cr.q.30')

clkid('WR1_2_cmdEnter')

> 因此我們只要指定瀏覽器的驅動程式(driver=...)，指定要瀏覽的網頁(國民健康署癌症登記線上互動系統：一般(年齡別))，將每個頁面要點擊的項目、選單的內容定義清楚(如下段3.6.3說明)，利用序列及迴圈的技巧，不斷呼叫這些副程式即可達成目標(3.6.4)，只剩下最後輸出檔案要如何保存的問題(3.6.5另存新檔及命名方式)。

點擊的項目、選單內容定義

以下範例是國健署癌症登記線上互動系統：一般(年齡別)的6個網頁點選內容(第1頁點選癌症類別、第2頁點選年代、第3頁點選年齡、第4頁點選地區、第5頁點選報告的圖或表，第6頁是處理檔案)，val(vXXX)表示是點選的值，id表示點擊的對象，dXXX表示XXX的val與XXX_name對照dict，_n表示出現在第n頁的點選內容。

val_data=['1','2'] #occurence and motality

val_point=['A'] #,'B','C','D'] #statistical point

val_sex=['1','2'] #['0','1','2','3']

dCancer = **rdtxt**('cancer.txt')

id_cancer=[i for i in dCancer]#??7ç¨®ç???

ID2=["WR1_1_Q_YearBeginII","WR1_1_Q_YearEndII","WR1_1_btnNext"]

va2=['1979','2013']#?\~Lä?å¼µè¡¨é¡¯ç¤º

id_age=['WR1_1_Q_AgeGroupII_'+str(i) for i in xrange(1,18)]
#??7?\~Kå¹´é½¡å???

id_reg=['WR1_1_QP_AreaRegionII','WR1_1_Q_AreaCity','WR1_1_Q_AreaTown']

Area=['ROOT','REGION_N','REGION_C','REGION_S','REGION_E','REGION_X','REGION_F']

nam=['?¨å?','?\~Wå?','ä¸­å?','?\~Wå?','?±å?','?\~Qé¦¬','?\~Kå?']

dArea={}

for i in xrange(len(Area)): dArea.update({Area[i]:nam[i]})

dCity=**rdtxt**('city.txt')#?°å?å¸?\...?¶ä?

City=[i for i in dCity]

dTown=**rdtxt**('region.txt')

Town=[i for i in dTown]

dRegion={}

for i in dArea:dRegion.update({i:dArea[i]})

for i in dCity:dRegion.update({i:dCity[i]})

for i in dTown:dRegion.update({i:dTown[i]})

val_reg=[[0 for i in xrange(389)] for j in xrange(3)]

for i in xrange(len(Area)):val_reg[0][i]=Area[i]

for i in xrange(len(City)):val_reg[1][i]=City[i]

for i in xrange(len(Town)):val_reg[2][i]=Town[i]

ID5=['WR1_1_Q_ReportKindII_2',"WR1_1_cmdQuery"]

ID6=["WR1_1_ReportViewer1_ctl01_ctl05_ctl00",'WR1_1_ReportViewer1_ctl01_ctl05_ctl01']

va6=["Excel"]

delCols=['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3']

cols=['Data','Point','Sex','Cancer','Age','Region']
#constant cols

df=DataFrame()

path=7*[0]

path[0]='C:\\\\Users\\\\4139\\\\Downloads\\\\'

點選內容可以由rdtxt之程式讀取。該程式先將頁面原始碼剪下另存成txt檔，再運用文字讀取的程式技巧將癌症種類、地區鄉鎮縣市等內容讀取出來。

# coding=utf-8

"""

This Routine is used to read the dictionary of ID:NAME in cancer online
query website

The input string (may with path) is the file name which contain "for"
ID's and names

The output result is the dictionary, which may used in selenium calls

"""

def **rdtxt**(fname):

w=[] #container of words

with open(fname) as ftext: #open file

for line in ftext: #read each line

for i in line.split(): #using the space as separation character

if i[0:3]=='for': #only the words leaded by 'for' are saved

w.append(i)

redunt=['for=',"</label>",'</td>','"',"'"] #these
characters or strings must be cleaned

for k in redunt:

for i in xrange(len(w)): w[i]=w[i].replace(k,'') #replace with
''

for i in xrange(len(w)): w[i]=w[i].replace('>',",") # > must
change to ',' for further split

(WR,nam)=([],[]) #containers declarations

for i in xrange(len(w)): #working for each words

lst=[j for j in w[i].split(',')] #split the ID and name

if len(lst)>1: #the overall ID may have no following name

WR.append(lst[0]) #first is the keys

nam.append(lst[1]) #the latter is the vlues

# print w[:15]

d={} #store the dictionary

for i in xrange(len(WR)):

d.update({WR[i]:nam[i]})

return d

序列及迴圈技巧與副程式之呼叫

整體下載的資料庫共有7層迴圈，為簡省工作，資料以原始數據下載不作年齡標準化，另行計算。且因鄉鎮區太多，僅下載關切地區的區別數據，其餘則以縣市或大區為範圍下載。年代數據一次下載所有年代，會同時出現在excel資料表內。癌症選取避開性別與性器官癌症之不合理組合，亦可有效減少迴圈之浪費。

程式藍色字部份為檔案管理，詳後分述，其餘則為迴圈與點選動作之進行。

for vdata in val_data:#[0:1]:

**path[1]=path[0]+vdata+'\\\\'**

for vpoint in val_point:#[0:1]:

**path[2]=path[1]+vpoint+'\\\\'**

for vsex in val_sex:#[0:1]:

**path[3]=path[2]+vsex+'\\\\'**

for icancer in id_cancer:#[0:1]:

if vsex=='1' and icancer[:len(icancer)-2] ==
'WR1_1_ctl180':continue

if vsex=='2' and icancer[:len(icancer)-2] ==
'WR1_1_ctl183':continue

if vsex=='2' and icancer[:len(icancer)-2] ==
'WR1_1_ctl185':continue

**path[4]=path[3]+icancer+'\\\\'**

for iage in id_age:#[0:1]:

**path[5]=path[4]+iage+'\\\\'**

for iACT in xrange(3):

for jACT in xrange(389):

**NameNew=path[5]+str(iACT)+str(jACT)+'.xls'**

**if val_reg[iACT][jACT]>1 and not os.path.exists (NameNew):**

**if not os.path.exists(NameNew):copy2('c.txt', NameNew)**

**driver.get('https://cris.hpa.gov.tw/pagepub/ Home.aspx
?itemNo=cr.q.30')**

#page1/5 data, point, sex, kind of cancer

ID1=["WR1_1_Q_DataII","WR1_1_Q_PointII", \\
"WR1_1_Q_SexII",icancer,"WR1_1_btnNext"]

va1=[vdata,vpoint,vsex]

for i in xrange(3):SelectByIDnValue(ID1[i],va1[i])

for i in xrange(3,5):clkid(ID1[i])

#page2/5 year

for i in xrange(2):SelectByIDnValue(ID2[i],va2[i])

for i in xrange(2,3):clkid(ID2[i])

#page3/5 age

ID3=["WR1_1_Q_AgeKindZone",iage,"WR1_1_btnNext"]

for i in xrange(3):clkid(ID3[i])

#page4/5 region

ID4=[id_reg[iACT],val_reg[iACT][jACT], "WR1_1_btnNext"]

if iACT==0: #in case of all nation

SelectByIDnValue(ID4[0],ID4[1])

else:

for i in xrange(2):clkid(ID4[i])

clkid(ID4[2])

#page5/5 report type

for i in xrange(2):clkid(ID5[i])

#result(page 6)

SelectByIDnValue(ID6[0],va6[0])

clkid(ID6[1])

**fname=path[0]+*'*Cr*.xls' #**

**while not os.path.exists(fname):**

**time.sleep(1)**

**f=*glob.glob(fname)**

**w=[x for x in** **s*ubprocess.check_output( \**

**'dir/w '+fname, shell=True).split()]**

**if path[0]+w[7] in f: fname=path[0]+w[7]**

**[#]{.underline}** **[while not
os.path.exists(fname):time.sleep(1)]{.underline}**

**copy2(fname, NameNew)**

**os.remove(fname)**

**driver.close()**

點選另存檔案之後，**chromedriver**可以點選上一頁，此舉雖然可以減少跳出再進的時間，也不必再選擇身份，然而有很高的機率會出錯。因此還是以關掉驅動程式(**.close()**)、重新啟動(**.get(...)**)的方式，較為穩定不會出錯(紅字部分)。

檔案名稱與檔案管理

下載檔案管理面臨之問題與解決方式：

整理成一個大檔案或者儲存個別檔案？

由於下載過程曠日費時，檔案另外處理，具有不怕斷線、容易累積的好處，而連線閱讀組成一超大資料庫，每次斷線後要重新讀取，並不符合經濟效益。

網站產生檔案、chrome下載儲存檔案都需要時間，python無法等待，以致發生重複同一檔名，系統會增加(1)、(2)等字尾，予以辨識，增加未來檔案處理的困難度，。

停等直到檔案出現的迴圈，如前述紫色字部分程式碼。如果系統給定的是確定的檔名(fname)，可以用while
not
os.path.exists(fname)來判別(底線部分)。但由於不知道系統會給定什麼樣的檔案名稱，只知道字頭是Cr(Cancer
Record)，字尾是.xls，若運用wild card(*)，not
os.path.exists(fname)反而會得到True的結果，系統將會一直停等。

因此必須運用2個方式檢查檔案名稱是否出現，一者為適合萬用卡的glob.glob()指令，一者為subprocess.check_output('dir/w
')，前者會出現所有Cr*.xls，包括預設的CrXXX -
複製.xls檔案(glob若沒有檔案會發生錯誤)，後者則利用中文檔名在DOS的dir/w指令中不會接副檔名的特性，排除在前者glob的結果之外，系統持續停等。

當系統出現特定的CrReportN_A01_A.xls
(或CrReportN_A01_B.xls...)檔案時，DOS的dir/w指令結果第7項為檔名，此時將明確檔名換掉萬用卡檔名，可以讓
os.path.exists(fname)生效，系統停止休息。

如此只有在明確的檔案名稱出現，二者對照成功，方能停止等待，繼續執行程式。

搬移或複製

理論上，搬移(os.rename或os.renames)會比copy &
remove更直接，但當目錄內已經有既有檔案時，rename將會失敗，此時就必須copy2。雖然確認檔案是否存在的邏輯判斷是在迴圈的前段就執行，此處仍然以可以覆蓋作為程式設計的原則，避免修正時的麻煩。

檔案個數的問題

每次迴圈點選之後，不論是否有符合該點選條件的癌症發生率、致癌率，系統都會出一個查詢結果excel檔，因此如何將其由系統內定的檔名轉成特定檔名，且不會造成檔案個數太大無法正常運作檔案管理，必須有足夠多的目錄以及足以分辨的檔名系統。

解決方式以5層目錄分開儲存這些檔案，而以迴圈的後2因子做為檔案名稱。目錄以累加方式產生，此一方式也可以用在後續的檔案管理。

for vdata in val_data:#[0:1]:

path[1]=path[0]+vdata+'\\\\'

for vpoint in val_point:#[0:1]:

path[2]=path[1]+vpoint+'\\\\'

for vsex in val_sex:#[0:1]:

path[3]=path[2]+vsex+'\\\\'

for icancer in id_cancer:#[0:1]:

path[4]=path[3]+icancer+'\\\\'

for iage in id_age:#[0:1]:

path[5]=path[4]+iage+'\\\\'

for iACT in xrange(3):

for jACT in xrange(389):

vals=[vdata,vpoint,vsex,icancer,iage,str(iACT),str(jACT)]

lastname=path[5]+str(iACT)+str(jACT)

# NameNew=path[0]

# for i in xrange(7):NameNew=NameNew+vals[i]

# NameNew=NameNew+'.xls'

# if os.path.exists(NameNew): os.rename(NameNew,lastname)

if os.path.exists(lastname+'xls'):
os.rename(lastname+'xls',lastname+'.xls')

執行與記憶體管理

由前述條件，當網站名稱為https時，將無法使用firefox或是工作站進行讀取，必須使用window上的chrome。而window上執行chromedrive，程式佔用系統的記憶體會緩慢增加。而當記憶體滿了的時候，chromedrive會crash當機，程式就中斷了。

此時可以運用DOS的批次檔技巧予以解決，設計批次檔呼叫自己，就成了永不停止的批次檔，如下所示：

c:python select3.py

del C:\\Users\\4139\\Downloads\\CrReport*.xls

endless.bat

當chrimedrive失效時，會釋放出記憶體，讓批次檔呼叫python繼續新的工作。因為程式內設計若目錄下若已經有要下載的檔案，就會跳過不執行，因此迴圈會從上次當機的地方繼續下載。

NOAA天氣圖之範例

NOAA將再分析之天氣圖等等數據資料，以網頁選單方式，提供圖面予使用者。因此使用程式來進行下載過程，將會大大簡化長時間數據圖面的取得。

程式範例如下：

> #written by Penny Hsu
>
> # -*- coding: utf-8 -*-
>
> #輸出文字顏色設定
> \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> #example：print red + "Hello!" + color_end
>
> red = '\\033[31m'
>
> green = '\\033[32m'
>
> color_end = '\\033[0m'
>
> #導入模組區\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> #from \... import、import、import\...as → 導入模組的方式
>
> #package -> module -> class -> function
>
> from selenium import webdriver #驅動網頁瀏覽器
>
> from selenium.webdriver.support.ui import Select #選取網頁讀取元素
>
> from BeautifulSoup import BeautifulSoup as bs #抓取數據網頁
>
> from urllib2 import urlopen #檢視網頁原始碼
>
> from urllib import urlretrieve #將網頁數據、資料下載
>
> import os #建立與刪除目錄相關的模組
>
> import time #時間模組
>
> from datetime import **date**, **timedelta**
> #時間模組，可以對年、月、日做加減
>
> import argparse
>
> #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> # construct the argument parser and parse the arguments
>
> ap = argparse.ArgumentParser()
>
> ap.add_argument("-d", "\--date", required = True, help =
> "request date")
>
> args = vars(ap.parse_args())
>
> yy=args["date"][0:2]
>
> mm=args["date"][2:4]
>
> dd=args["date"][4:6]
>
> #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> #開啟網頁驅動程式以及網頁\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> try:
>
> driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver")
> #Linux
>
> # driver = webdriver.Chrome('C:/Program Files
> (x86)/Google/Chrome/Application/chromedriver.exe')
>
> driver.get("**[https://www.esrl.noaa.gov/psd/data/composites/hour/]{.underline}**")
>
> print green + "開啟網頁成功" + color_end
>
> except:
>
> print red + "開啟網頁失敗" + color_end
>
> #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> # 尋找網路元素與 Selenuim Webdriver的屬性和方法
>
> def clkid(name): #按單擊扭
>
> button_element = driver.find_element_by_name(name)
> #以名稱查詢符號
>
> button_element.click()
>
> return
>
> def SelectByNameValue(name,v): #(變數名稱,月份)
>
> #example：<select name="monr1"><option value="1">Jan
>
> v = str(int(v)) #將字串變回整數再轉成字串, 去掉字串00\~09前面的0
>
> select = Select(driver.find_element_by_name(name)) #以名稱查詢符號
>
> select.select_by_value(v) #選取select搭配的value
>
> return
>
> def SelectByNametxt(name,t):
>
> t = str(int(t))
>
> select = Select(driver.find_element_by_name(name))
>
> select.select_by_visible_text(t) #選取select搭配的text
>
> return
>
> def SelectByNametxt1(name,v):
>
> select = Select(driver.find_element_by_name(name))
>
> select.select_by_visible_text(v) #選取select搭配的text
>
> return
>
> #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> #時間設定區\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> wait_time = 120 # 設定載入圖片網頁等待秒數 120 = 120秒 = 2分鐘
>
> year = '20'+yy # 設定抓取圖片的年份
>
> start_date = date(int(year),int(mm) , int(dd)) #
> 設定抓取圖片起始日期
>
> end_date = date(int(year),int(mm), int(dd))
>
> hours = ['00', '06', '12', '18'] # 設定抓取圖片每日哪些小時
>
> #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> #進入網頁後，不會重複點選、填寫的部分\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> #variables
>
> SelectByNametxt1('var',"Sea Level Pressure")
>
> #年份
>
> driver.find_element_by_name('iyr[1]').send_keys(year)
> #sed_keys為以鍵盤輸入
>
> #Color
>
> SelectByNametxt1('labelc',"Black and White")
>
> #Shading
>
> SelectByNametxt1('labels',"Contours (Black and White Only)")
>
> #Scale Plot Size
>
> driver.find_element_by_name('scale').send_keys('100')
>
> #Plot contour labels
>
> yes =
> driver.find_element_by_xpath("//input[@name='label'][@type='radio']\\
>
> [@value='1']").click() #找尋完整的id屬性
>
> #Region of global
>
> SelectByNametxt1('proj',"Custom")
>
> #If Custom
>
> driver.find_element_by_name('xlat1').send_keys('15')
>
> driver.find_element_by_name('xlat2').send_keys('45')
>
> driver.find_element_by_name('xlon1').send_keys('95')
>
> driver.find_element_by_name('xlon2').send_keys('135')
>
> #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
>
> #進入網頁後，會重複點選的部分(時間)
>
> current_date = start_date
>
> #判斷句，假如現在的時間小於或等於結束時間，執行以下迴圈
>
> while current_date <= end_date:
>
> for hour in hours:
>
> #抓取執行時間的字串 #傳%m給strftime會取得時間的月份, 傳%d取到日
>
> month = current_date.strftime('%m')
>
> day = current_date.strftime('%d')
>
> #time select
>
> SelectByNameValue('monr1',month)
>
> SelectByNametxt('dayr1',day)
>
> SelectByNameValue('hour1',hour)
>
> SelectByNameValue('monr2',month)
>
> SelectByNametxt('dayr2',day)
>
> SelectByNameValue('hour2',hour)
>
> clkid('Submit')
>
> print "按下Submit, 等待{0}秒載入圖片網頁".format(wait_time)
>
> wait = True
>
> timeout = wait_time + time.time()
>
> while wait:
>
> if "cgi-bin" in driver.current_url:
> #current_url為取得目前所在網址
>
> wait = False
>
> if time.time() > timeout:
>
> break
>
> if wait == True: #假如等超過120秒 wait == True成立
>
> print red + "圖片網頁在{0}秒內, 載入失敗".format(timeout) +
> color_end
>
> #{}索引，利用format指定索引的數值
>
> driver.back()
>
> continue
>
> print "圖片網頁載入完成"
>
> #存取圖片
>
> try:
>
> url = driver.current_url #載入當前頁面網址 .current_url
>
> out_folder =
> "/home/backup/data/NOAA/psd.data.composites.hour/slp"+yy+mm
> #linux路徑
>
> filename = "17"+month+day+hour+".gif" #字串要雙引號
>
> soup = bs(urlopen(url))
>
> get_image = False
>
> for image in soup.findAll("img"):
> #找尋原始碼中有img的部分定義為image
>
> print image
>
> if image.get('alt','') == "Composite Plot":
>
> src = image["src"]
>
> print src
>
> outpath = os.path.join(out_folder, filename)
>
> #ex：C:/Users/6919/Desktop/2016/16010100.gif
>
> #存檔位置+存檔檔名皆要告知
>
> urlretrieve("https://www.esrl.noaa.gov"+src, outpath)
>
> get_image = True
>
> if get_image != True: # != 不等於
>
> raise Exception #強制異常
>
> except:
>
> get_image != True # != 不等於
>
> print red + "抓取 {0}/{1}/{2} {3}z 圖片失敗".format(year, month,\\
>
> day, hour) + color_end
>
> driver.back()
>
> continue
>
> print green + "抓取 {0}/{1}/{2} {3}z 圖片成功".format(year, month,\\
>
> day, hour) + color_end
>
> driver.back()
>
> current_date += **timedelta(days=1)**
>
> driver.close()

程式之呼叫及執行

理想上，一次登入網站之後，只需要更換日期選單，即可完成所有月份、年份批次的工作，然而實務上伺服器會因為連線太久而當機。經試誤結果發現，以1天登入一次最為恰當。因此需另外撰寫執行批次檔，如下所示：

i=$1

cd slp17$i

DM=\`days_of_month 17 $i\`

for j in {01..31};do

if [ $j -le $DM ]; then

if [ ! -f 17$i$j"00" ]; then

python ../get_NOAA_s_1.py **-d** **17$i$j**

fi

fi

done

cd ..

程式呼叫之前須先確認月份的最後一天，同時也真的沒有下載過。**days_of_month**是一個給定日數的小程式，有2個引數，分別是年代與月份。

截圖與解析

前述爬蟲程式應用在網頁本身有提供數據、檔案以供程式自動下載，對網頁只提供圖面時，就必須結合**print
screen**功能以及圖檔的解析兩項工具。以下以nullschool網站所提供的空氣品質預報濃度圖為例進行說明(**sc_fire.py**)：

截圖程式

以下為工作站版本，以firefox做print screen動作的程式：

kuang@master /home/backup/data/earth.nullschool.net

$ cat sc_fire.py

from selenium import webdriver

import time

import os

import argparse

# construct the argument parser and parse the arguments

ap = argparse.ArgumentParser()

ap.add_argument("-d", "\--date", required = True, help = "request
date")

args = vars(ap.parse_args())

yy=args["date"][0:2]

mm=args["date"][2:4]

dd=args["date"][4:6]

path='/home/backup/data/earth.nullschool.net/'+args["date"]

os.system('mkdir -p '+path)

browser = webdriver.**Firefox**()

for ih in xrange(24):

hh=str(ih)

if ih<10:hh='0'+str(ih)

url=**'https://earth.nullschool.net/#20'+yy+'/'+mm+'/'+dd+'/'+hh+'00Z/particulates/surface/level/anim=off/overlay=pm2.5/orthographic=-239.01,23.61,2400'**

browser.**get**(url)

time.sleep(10) #wait for downloading

fname=path+'/'+args["date"]+hh+'.png'

browser.**save_screenshot**(fname)

browser.**quit**()

網頁圖面的控制

範例中網頁位址如url所示。經試誤瞭解其網址內容已經隱含畫面的控制，除日期時間之外，cLON=120.99-360=-239.01(center
long.)，cLAT=23.61000(center
lat.)為中心經緯度的設定，2400為解析度引數，數字越大解析度越高，最大為3000。經試誤2400可得符合MM5之terr2.dat南北緯度範圍，同時也可以包括空品模擬的d2.in範圍。particulates等是疊圖內容，與其網站提供的內容相符，particulate下的overlay可以是pm1、pm2.5、pm10、suexttau、duexttau，chem下的overlay可以是cosc、so2smass等等。

瀏覽器之啟動及截圖

基本上除了啟動與關閉之外，就只有**get**網址與**save_screenshot**兩個動作。

檔名及檔案管理

此處以日期做目錄名稱，並利用os.system功能建置目錄，以日期小時為名儲存圖片檔案，以利後續進一步解讀。

濃度圖解讀

如前述tiff圖檔的解讀，可以利用scikit-learn:
Sklearn的kmeans程式來解讀。解讀分成4個階段，解讀濃度尺標(legend.png)、解讀螢幕圖檔、將此二者連結之後予以定量、最後按照所要求的座標系統將矩陣寫出成數據檔。

解讀濃度尺標

nullschool網站附有各項貼圖的濃度顏色尺標，這是僅有讓顏色具有數量或順序意義的資料來源，可以先將其截圖存成**legend.png**，並運用下列程式將其解讀：

kuang@master /home/backup/data/earth.nullschool.net

$ cat rdpng2.py

import numpy as np

from mostfreqword import *

import cv2

from sklearn.cluster import KMeans

def rms(a):

return np.sqrt(np.mean(np.square(a)))

image = cv2.imread('**legend.png**')

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

mn=image.shape

image = image.reshape((mn[0] * mn[1], 3))

clt = KMeans(algorithm='auto', copy_x=True, init='k-means++',
max_iter=300, \\

n_clusters=**484**, n_init=10, n_jobs=-1,
precompute_distances='auto', \\

random_state=None, tol=0.0001, verbose=0)

kmeans=clt.fit(image)

**x**=np.array(clt.cluster_centers_)

for i in xrange(484):

rgb=x[i,:]

if abs(np.mean(rgb)-rms(rgb)) < **1.5**:

for j in xrange(mn[0]*mn[1]):

if kmeans.labels_[j] == i: kmeans.labels_[j]=-1

category=np.reshape(kmeans.labels_,(-1,mn[1]))

**categoryx**=[mostfreqword(category[:,i]) for i in xrange(483)]

濃度色標是個長條的圖檔，它的尺寸是11x484個色塊，理論上最多可以鑑別出484種不同顏色，但事實上即使將n_clusters=484只可以得到441種不同的顏色。但這並不影響後續的解讀，因為顏色已經夠多。解讀得到的顏色存在x矩陣之內，不見得按照某個順序排列，category則是圖檔各個色塊對應到x的指標，配合此二者，可以畫出與原圖幾乎一樣的圖檔。

為了防止解讀時將黑、白、灰色列為一種顏色，這些可能是陸地界線、可能是網頁上的說明文字，這裏使用算數平均值與幾合平均值的特性，當序列的每個元素都是一致時，此二平均值是一樣的，因此界定此二平均值的差異超過一定水準，是具有特性的顏色，而非灰色系列，判定的準則經過試誤，定為1.5。

category是將顏色排序的重要線索，因為category是矩陣排列，同一列有可能在辨色過程中有不同的結果，這裏運用mostfreqword小程式(2.5節)，將該列出現最多的顏色列出成為categoryx，此一序列則是具有順序的顏色，且每一序號只有一個顏色。

解讀濃度圖檔

困難1：正式螢幕截圖之逐時圖檔顏塊有880x1280，如果逐一比對計算是否是前述484個色標之一，或最靠近色標中哪一個顏色，疊代次數太多，嚴重延宕計算時間。

解決方式：不逐一比對，乃以前述**KMeans**程式先處理圖檔的代表色，再處理代表色與色標的連結。

困難2：正式逐時的圖檔顏色，可能與前數濃度尺標不一。因為顏色的判定是與其所佔據的色塊大小有關，前述色標圖檔因為任一個顏色都具有相同的色塊大小，因此程式可以辨認出來400多種顏色。而實際圖檔不可能有此分布，因此即使**n_clusters=400**也讀不出那麼多顏色，程式會當掉!即使將色標貼在正式圖檔、增加其面積，也無法克服此一問題。

程式大致還可以分辨200個顏色。

色標與圖檔代表色的連結

基本上連結有2個動作，先計算2個顏色之間的距離(差異的定量化)是如何，然而選一個最小差異的結果。前者因為涉及到人類肉眼和3元色間的數量，可以上網找到制式做法。而後者只是應用python的min與index指令即可完成。

def **ColorDistance**(rgb1,rgb2):

'''d = {} distance between two colors(3)'''

rm = 0.5*(rgb1[0]+rgb2[0])/256

return sum((2+rm,4,max(0,3-rm))*(rgb1-rgb2)**2)**0.5

**ColorDistance**程式已被廣泛利用在計算2個顏色的差異，具有加強紅色、弱化藍色的傾向。定義了此一副程式，就可以進行連結。

mmapR=[]

for i in xrange(200):

ldel=[ColorDistance(**x**[j,:],**x2**[i,:]) for j in xrange(484)]

mmapR.append(ldel.**index**(**min**(ldel)))

mmapR即為實際圖檔的200顏色，對照到484個標準顏色的編號序列。由於黑、白、灰等顏色並不在x陣列之內，因此即使逐時圖檔內有該等顏色，對照結果將不會有此類顏色。對照結果應用在螢幕圖檔，由於色標的順序與濃度的大小具有某種程度的關係，可以調整此一關係式讓濃度更符合實際。以下為平方的關係，高濃度的變化差異較大。

conc=category2

for i in xrange(mn2[0]):

for j in xrange(mn2[1]):

m=mmapR[category2[i,j]] #index of x

if m in categoryx[:]:

conc[i,j]=(float(categoryx[:].index(m)))*2**/484*2

else:

conc[i,j]=0

網格座標系統的轉換與輸出

螢幕截圖檔案與空品模式邊界/初始檔案二者的座標系統，只有中心點是完全相同，前者涵蓋後者，此外在解析度、原點等等，都不盡相同，需要進行網格座標系統的轉換。網站畫面提供陸地邊界與經緯度，然而經緯度的變化並非線性，螢幕截圖是正交、等距離的座標系統，因此會在邊界造成嚴重的錯誤。

解決方案是以power
point的量尺為工具，量測D2在螢幕上的南北範圍(以陸地邊界線做參考)，得到png中d2範圍的尺寸，相對即可得知png所有範圍的座標。

Png範圍：

len2=877.50*2 #從d2.in指定

len1=len2/7.88*9.98 #measured on powerpoint , unit=cm

len1x=len2/7.88*14.52 #measured on powerpoint ,unit=cm

mnx=-len1x/2

mxx=+len1x/2

mny=-len1/2

mxy=+len1/2

d2範圍(len_x=len_y=len2)

mnx2=-len2/2

mxx2=+len2/2

mny2=-len2/2

mxy2=+len2/2

(nx2,ny2)=(65,65)

最後以距離平方為反比，進行濃度的內插：

c0=np.empty([nxd,nyd])

for i in xrange(nxd):

for j in xrange(nyd):

c0[i,j]=conc[nyd-j-1,i]

cn=np.empty([nx2,ny2])

for i in xrange(nx2):

for j in xrange(ny2):

sum1=0

sum2=0

ic=int((xx2[i]-mnx)/delx)

jc=int((yy2[j]-mny)/dely)

for ii in xrange(max(0,ic-3),min(ic+3,nxd)):

for jj in xrange(max(0,jc-3),min(jc+3,nyd)):

d2=(xx2[i]-xx[ii])**2+(yy2[j]-yy[jj])**2

if d2==0:

cn[i,j]=c0[ii,jj]

break

if c0[ii,jj]<=0:continue

sum1=sum1+1/d2

sum2=sum2+c0[ii,jj]/d2

if d2==0: break

if d2==0:

cn[i,j]=c0[ii,jj]

else:

if sum1*sum2 == 0:

cn[i,j]=0.

else:

cn[i,j]=sum2/sum1

save_surfer(fname_d,nx2,ny2,mnx2,mny2,mxx2,mxy2,np.matrix.transpose(cn).reshape(nx2*ny2))

![](media/image26.png){width="5.408888888888889in"
height="3.3594028871391077in"}

Windy網頁畫面之逐時拮取

基本上windy網站提供的是目前天氣及預報天氣，並沒有時間的標示(包括過去及未來)可供調整，因此逐時拮取以累積歷史數據可能是唯一的解決方式。其他windy網頁畫面類似前述nullschool，可以沿用先前的程式架構，特殊的地方在於分別以不同陸徑名稱來標示其內容。其網頁儲存路徑的基本命名邏輯為:

url='https://www.windy.com/?'+**model**+**level**+'23.61,120.99,'+**domain**+',i:pressure'

其中**model,level,domain**為變數，**model**為GFS或者是ECMWF美國或歐盟氣象署的模擬結果，**level**則是高度，地面沒有特別標註，950h、850h等高度皆可，其後的2個數字為緯度與經度。**do
main**則為數據範圍，5是東亞範圍，7則為台灣地區，解析度則視各模式而異。,i:pressure'表示貼上等壓線(天氣圖)。

因此只要定時開啟所要的網頁，將網頁存在指定的目錄，並將時間資訊寫在名字中即可：

kuang@master /home/backup/data/windy

$ cat windy.py

#!/cluster/miniconda/bin/python

from selenium import webdriver

import os

import subprocess

batcmd="date +%Y%m%d%H"

url='https://www.windy.com/?23.61,120.99,5,i:pressure'

ymdh_old = ''

while True:

**ymdh = subprocess.check_output(batcmd, shell=True)[2:-1]**

if ymdh!=ymdh_old:

driver = webdriver.Firefox()

driver.get(url)

os.system('sleep 1s')#guang_gao

for model in ['','gfs,']:

m=model.strip(',')

if len(m)==0:m='ecm'

for domain in ['5','7']:

for level in ['','950h,','850h,']:

l=level.strip(',')

if len(l)==0:l='surf'

url='https://www.windy.com/?'+model+level+'23.61,120.99,'+domain+',i:pressure'

driver.get(url)

fname=m+'/'+l+'/'+'d'+domain+'/'+ymdh+'.png'

os.system('sleep 1s')

screenshot = driver.save_screenshot(fname)

ymdh_old=ymdh

print 'time=',ymdh

driver.quit()

else:

os.system('sleep 10m')

continue

**ymdh = subprocess.check_output(batcmd,
shell=True)[2:-1]**此一指令與**os.system**最大的不同是將os指令的執行成果(std
output)，以字串型態寫在**ymdh**裏，由於字尾最後會出現特殊碼(\^J)，因此只能取到倒數最後第2位。

airvisual 網頁畫面之逐時拮取

airvisual必須逐時拮取的原因是網站並沒有歷史數據或畫面提供下載檢視，而其畫面拮取的困難點則在於圖面完全是網站的程式所控制，必須由滑鼠(或鍵盤)互動決定，而不是儲存不同路徑的畫面。

kuang@master /home/backup/data/airvisual

$ cat airvisual.py

#!/cluster/miniconda/bin/python

from selenium import webdriver

from selenium.common.exceptions import WebDriverException

from selenium.webdriver import ActionChains

import os

def wheel_element(element, deltaY = 120, offsetX = 0, offsetY = 0):

error = element._parent.execute_script("""

var element = arguments[0];

var deltaY = arguments[1];

var box = element.getBoundingClientRect();

var clientX = box.left + (arguments[2] \|\| box.width / 2);

var clientY = box.top + (arguments[3] \|\| box.height / 2);

var target = element.ownerDocument.elementFromPoint(clientX, clientY);

for (var e = target; e; e = e.parentElement) {

if (e === element) {

target.dispatchEvent(new MouseEvent('mouseover', {view: window,
bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));

target.dispatchEvent(new MouseEvent('mousemove', {view: window,
bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));

target.dispatchEvent(new WheelEvent('wheel', {view: window, bubbles:
true, cancelable: true, clientX: clientX, clientY: clientY, deltaY:
deltaY}));

return;

}

}

return "Element is not interactable";

""", element, deltaY, offsetX, offsetY)

if error:

raise WebDriverException(error)

driver = webdriver.Firefox()

driver.get("https://www.airvisual.com/earth")

# get element

elm =
driver.find_element_by_css_selector("svg#foreground.fill-screen")

**actions = ActionChains(driver)**

**actions.drag_and_drop_by_offset(elm, 640,650)**

actions.perform()

**wheel_element(elm, -800)**

os.system('sleep 10s')

screenshot = driver.save_screenshot('my_screenshot.png')

driver.quit()

方框內**wheel_element**函數是從網路上抓下來的小工具，引數有2，首先是要滾輪作用在哪一個網頁元素的元素名稱，其次是一個數字，必須由試誤法決定，而且不同作業系統可能會不同(linux,
mac)。元素名稱必須由網頁原始碼中尋找。

在轉動滾輪之先，畫面要先經滑鼠將台灣島拖曳到螢幕中央，可以經由**ActionChains(driver).drag_and_drop_by_offset(elm,
640,650)**此一指令來完成，3個引數的第2\~3分別是左右與上下拖曳的幅度，也是由試誤法決定，不同作業系統也會不同。

複製網頁內容並儲存成資料庫

有些網頁會將數據直接寫在程式碼內容之中，因此需要將程式碼讀出來(**page_source**)，並將其轉成所要的格式，網頁之外觀如以下範例(新北市交通流量即時監測資訊)所示。

{"success":true,"**result**":{"resource_id":"382000000A-000357-001","limit":2000,"total":702,"fields":[{"type":"text","id":"vdid"},{"type":"text","id":"datacollecttime"},{"type":"text","id":"status"},{"type":"text","id":"vsrid"},{"type":"text","id":"vsrdir"},{"type":"text","id":"speed"},{"type":"text","id":"laneoccupy"},{"type":"text","id":"carid"},{"type":"text","id":"volume"}],"**records**":[{"vdid":"65000V008130","datacollecttime":"2017/12/04
21:38:00","status":"3","vsrid":"0","vsrdir":"0","speed":"-99","laneoccupy":"-99","carid":"L","volume":"-99"},{"vdid":"65000V008130","datacollecttime":"2017/12/04
21:38:00","status":"3","vsrid":"0","vsrdir":"0",
"speed":"-99",
"laneoccupy":"-99","carid":"S","volume":"-99"},......

程式碼中切割出所要字串

這些資訊(json或dict格式)可以在程式碼中找到：

<html><head><link rel="alternate stylesheet" type="text/css"
href="resource://gr

e-resources/plaintext.css" title="Wrap Long
Lines"></head><body><pre**>**{**...**}**<**/pre></body></html>

由於網頁程式碼是以<...>來撰寫，因此須以'>'及'<'來分割(split)，以截取出所要的字串。

kuang@master /home/backup/data/ETC/NewtaipeiVD

$ cat getvd.py

from selenium import webdriver

import simplejson

from pandas import *

driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver")
#Linux

url='http://data.**ntpc**.gov.tw/api/v1/rest/datastore/382000000A-000357-001'

driver.get(url)

fname='latest.json'

fl=open(fname,'w')

fl.write(driver.**page_source**)

driver.quit()

fl.close()

with open(fname) as ftext:

s=[]

for line in ftext:

s.append(line.split('>'))

ss=[x for x in s[0][6].split('<')]

z=ss[0]

json_2_dict = **simplejson.loads**(z)

jj=json_2_dict[**'result'**]

df=DataFrame(jj[**'records'**])

cols=["vdid","datacollecttime","status","vsrid","vsrdir","speed","laneoccupy","carid","volume"]

df[cols].set_index(['vdid']).to_csv('latest')

字串轉成字典

可以使用simplejson.loads[^99]將字串轉成字典，由於檢視該字典結構發現，是具有層次的，真正的數據是在第三層(**result**,
**records**)之下，必須循序將其讀出來。由於字典可以轉成pandas資料庫，可以寫成csv輸出格式，方便後續整併處理。

定時批次執行

新北市VD數據是每5分鐘更新覆蓋在網頁上，因此必須每5分鐘讀取儲存。可以利用bash之date功能，讓系統判定是否5分鐘到了，若還沒就先暫停(sleep)，若到了，就執行前述python程式。

$ cat NewtpGetVD.cs

rm latest

A=\`date +%M\`;M=\`date +%M\|cut -c1\`

if [ $M = 0 ] ;then A=\`date +%M\|cut -c2\`; fi

oldM=$(( $A / 5 ))

newM=$(( $A / 5 ))

while true; do

while [[ $newM == $oldM ]]; do

A=\`date +%M\`;M=\`date +%M\|cut -c1\`

if [ $M = 0 ] ;then A=\`date +%M\|cut -c2\`; fi

newM=$(( $A / 5 ));sleep 60;done;

oldM=$newM

**ymd=\`date \--rfc-3339='date'\`**

python getvd.py

**cat** latest**>>**$ymd

rm latest

done

撰寫時須注意bash無法進行字串I2.2的計算(如 $(( 07 /
5))是無法執行的)，必須先判斷分鐘數是個位數還是10位數，10位數M=\`date
+%M\|cut -c1\`若是0，則是個位數，必須取其第2位來計算。

執行結果必須儲存在當日的檔案中，此處運用**date**來取年月日數，用**cat
... >> ...**來附加在檔案最後面。

XML檔案格式數據之讀取

XML是一種常用網頁程式碼的類型[^100]，由於其數據儲存相對較為緊密，常常用來儲存即時更新之數據(以下範例為台北市交通局車輛流量監測數據[^101])，因此其爬蟲程式不是重點，一般以wget即可完整下載(詳見app.doc中有關bash變數、字串去尾等相關說明。)，然而其解析過程卻貌似非常困難。

究其困難在於：並無統一格式可遵循、無組織(每一個監測點有不同資料項目數量)、也不是每一個欄位均有完整的欄位名稱及數值配對、(亦即有不少欄位是從來不會有內容的)、最後每一次網頁只有寫一次時間，必須另外加一時間之資料項目與內容到資料庫內。

循序讀取範例

理論上結構化之檔案可以批次直接讀取較為有效，不應循序讀取，然而如果分支太過嚴重只得如此。以下為網頁內容範例:

```html
\<?xml version="1.0"
encoding="UTF-8"?>\<VDInfoSet>\<ExchangeTime>**2017/12/05T17:17:25**
\</ExchangeTime>
\<VDInfo>\<VDData>\<VDDevice>\<DeviceID>V0111C0\</DeviceID>\<TimeInterval>5\</TimeInterval>\<TotalOfLane>1\</TotalOfLane>\<**LaneData**>\<LaneNO>0\</LaneNO>\<Volume>143\</Volume>\<AvgSpeed>41\</AvgSpeed>\<AvgOccupancy>17.0\</AvgOccupancy>\<Svolume>0.0\</Svolume>\<Mvolume>143\</Mvolume>\<Lvolume>0\</Lvolume>\</LaneData>\</VDDevice>\</VDData>\</VDInfo>\<VDInfo>\<VDData>\<VDDevice>\<DeviceID>V0112A0\</DeviceID>\<TimeInterval>5\</TimeInterval>\<TotalOfLane>1\</TotalOfLane>\<LaneData>\<LaneNO>0\</LaneNO>\<Volume>94\</Volume>\<AvgSpeed>22\</AvgSpeed>\<AvgOccupancy>22.0\</AvgOccupancy>\<Svolume>0.0\</Svolume>\<Mvolume>93\</Mvolume>\<Lvolume>1\</Lvolume>\</LaneData>\</VDDevice>\</VDData>\</VDInfo>\<VDInfo>\<VDData>\<VDDevice>\<DeviceID>V0120C0\</DeviceID>\<TimeInterval>5\</TimeInterval>\<TotalOfLane>2\</TotalOfLane>\<LaneData>\<LaneNO>0\</LaneNO>\<Volume>69\</Volume>\<AvgSpeed>64\</AvgSpeed>\<AvgOccupancy>5.0\</AvgOccupancy>\<Svolume>0.0\</Svolume>\<Mvolume>65\</Mvolume>\<Lvolume>4\</Lvolume>\</LaneData>\<LaneData>\<LaneNO>1\</LaneNO>\<Volume>111\</Volume>\<AvgSpeed>62\</AvgSpeed>\<AvgOccupancy>14.0\</AvgOccupancy>\<Svolume>0.0\</Svolume>\<Mvolume>107\</Mvolume>\<Lvolume>4\</L
```

此處應用xml.etree.cElementTree模組來進行解析，詳細內容可以參考網友[^102]之說明，以下直接介紹範例程式。

```python
kuang@master /home/backup/data/ETC/TaipeiVD
$ cat getVD.py
from pandas import *
import **xml.etree.cElementTree** as ET
fname='GetVDDATA'
tree=ET.ElementTree(file=fname)
ttxt=[elem.text for elem in tree.iter()]
**id=set([elem.text for elem in tree.iter(tag='DeviceID')])**
cols=**['DeviceID','TotalOfLane','LaneNO','Volume','AvgSpeed','AvgOccupancy','Svolume','Mvolume','Lvolume']**
v=[]
for i in xrange(len(cols)):
v.append([])
for i in id:
ist=ttxt.index(i)
ttl=int(ttxt[ist+2])
for j in xrange(ttl):
v[0].append(i)
v[1].append(ttl)
istt=ist+4+**j*8**
for k in xrange(2,len(cols)):
v[k].append(ttxt[istt+k-2])
**d={}**
for i in xrange(len(cols)):**
**d.update({cols[i]:v[i]})**
cols.append('ExchangeTime')
d.update({cols[-1]:[ttxt[1] for x in xrange(len(v[0]))]})
df=DataFrame(d)
df[cols].set_index('DeviceID').to_csv(**'latest'**)
```

cElementTree與ElementTree差別在實現過程是否使用C語言副程式，這會使程式的記憶體較小一些，效率好一些。檢查tree的內容可以使用tree.getroot()、elem.tag、elem.attrib、elem.text等指令來探索要解析的XML檔案，如範例程式中就是運用[elem.text
for elem in tree.iter()]指令將所有網頁內容(數據內容部分)存成序列ttxt。

經過摸索之後，發現監測資料乃是以監測設施**id**為中心，有的設施有多條線道、有的只有單線道，而其有用的資訊除了時間須外加以外，其餘皆以循序方式，接在**id**的後面，必須以循序的方式小心讀取。

cols的數目雖然在每個監測點會略有不同，但順序總是相同，數量總是8的倍數(*總車道數**TotalOfLane**)，正好是7個變數與1個無用的LaneData共8個變數位置。

順序做好了，剩下就是序列名稱與對應關係了。此處先宣告9個空白、相同名字的2維序列，依序納入id、總車道數、以及其後的7個變數內容，這樣在編列成字典時就不需要再繁瑣撰寫，只要逐一將字典update即可。

如前所述，網頁只會在表頭處(第2個項目，即ttxt[1])寫一次時間
'ExchangeTime'，而不是每個id都會重複，並不符合資料庫型態，並且為了避免在讀取過程中造成干擾，因此在讀完之後再加一個字典項目即可。最後以csv形式輸出以利檔案整併。

XML屬性資料的利用

使用ElementTree讀取XML資料時，元素除了標簽(鑰)與文字(值)之外，還有屬性欄位可以放置數據內容，作為下一層次資料的統一說明，如下(桃園市車輛偵測2018/11月底前的即時數據，高雄市格式亦相同)所示：

kuang@master /home/backup/data/ETC/TaoyuanVD

$ more a

\<XML_Head **version="1.1" listname="VD ä¸€åˆ†é˜å‹•æ...‹è³‡è¨Š"
updatetime="2017/12/06 09:55:10" interval="60**

**"
xsi:noNamespaceSchemaLocation="http://211.72.255.245/VDClient/xsd_v11/VD_Value.xsd"
xmlns:xs**

**i="http://www.w3.org/2001/XMLSchema-instance"**>

\<Infos>

\<Info vdid="68000V100110" status="0" datacollecttime="2017/12/06
09:55:10">

\<lane vsrdir="0" vsrid="0" speed="0" laneoccupy="0.0">

\<cars carid="L" volume="0"/>

\<cars carid="S" volume="0"/>

\<cars carid="M" volume="0"/>

\</lane>

\<lane vsrdir="0" vsrid="1" speed="0" laneoccupy="0.0">

\<cars carid="L" volume="0"/>

\<cars carid="S" volume="0"/>

\<cars carid="M" volume="0"/>

\</lane>

\</Info>

\<Info vdid="68000V100360" status="0" datacollecttime="2017/12/06
09:55:10">

\<lane vsrdir="0" vsrid="0" speed="0" laneoccupy="0.0">

\<cars carid="L" volume="0"/>

\<cars carid="S" volume="0"/>

\<cars carid="M" volume="0"/>

\</lane>

\<lane vsrdir="0" vsrid="1" speed="0" laneoccupy="0.0">

\<cars carid="L" volume="0"/>

\<cars carid="S" volume="0"/>

\<cars carid="M" volume="0"/>

\</lane>

\<lane vsrdir="1" vsrid="2" speed="0" laneoccupy="0.0">

\<cars carid="L" volume="0"/>

XML_head標簽空一格後，跟著的就是所謂的屬性資料(elem.attrib)段落，在下一層Info之後，第3層lane之後，與第4層cars之後，都是該標籤的屬性。

ElemetTree將XML屬性的資訊內容(key=value)轉以python/json字典的型態({key:value})予以儲存，因此呼叫時必須以各個字典的鑰來代出其值。

可以運用elem.tag和elem.attrib將標籤與屬性的內容先儲存成序列，在本案例中elem.text沒有作用。如：

tree=ET.ElementTree(file=fname)

ttag=[elem.tag for elem in tree.iter()]

tatt=[elem.attrib for elem in tree.iter()]

**tree.iter()**會將遇到所有的元素組合都存成沒有層次的序列，一次破壞所有的層次，而將層次的從屬關係，變更序列前後的相對關係，同樣也可以利用前述序列的做法，將資料存成一龐大完整的表格。

不同的是**vdid**在本範例中是在屬性的範疇，而不是一個獨立的標籤，各個標籤中具有獨立特性的只有**'Info'**一項，2個**'Info'**中是一個完整的監測器數據內容，可以看做是一個封包，只是每個封包的大小不大相同。

因此首先必須先知道到底有幾個封包在檔案裏，然後逐一找到每個Info在序列中的位置，此2任務可以利用list.count與list.index指令。比較複雜一點的是，list.index只會找出序列裏第一個出現項目的位置，而對重複出現的項目，則必須先將之前找到的部分「摘除」，接著再找，找到後再加上前面摘掉的長度，如此疊代，即可找出所有項目的所在位置，如下所示：

ist=[ttag.index('Info')]

for i in xrange(ttag.count('Info')-1):

ist.append(ttag[ist[i]+1:].index('Info')+ist[i]+1)

ist.append(len(ttag))

範例程式中ist即是每個Info出現的位置，而所謂的「摘除」就是在進行ttag.index動作時，不計ttag序列在ist之前的內容，只計算ttag在ist+1以後的序列。

最後為了後續計算2個Info之間個數，需要ttag最後項的位置，即為ttag的長度，需要另外再附加上去。接下來就可以循序讀取封包裏各層屬性的內容了，類似前述循序讀取的程式：

v=[]

for i in xrange(len(cols)):

v.append([])

for i in xrange(ttag.count('Info')):

**d2**=tatt[ist[i]]

**ttl=(ist[i+1]-ist[i]-1)/4**

for lane in xrange(ttl):

for j in xrange(3):

v[j].append(**d2**[cols[j]])

v[3].append(ttl)

**d3**=tatt[ist[i]+4*lane+1]

for j in xrange(4,8):

v[j].append(**d3**[cols[j]])

for k in xrange(ist[i]+4*lane+2,ist[i]+4*lane+5):

**d4**=tatt[k]

for l in xrange(len(cols)-3,len(cols)):

if **d4**['carid']==size[l]:v[l].append(**d4**['volume'])

在本例中並沒有一個數據是「總線道數」，必須要由封包大小計算，每個線道會佔用4個項目，因此只要將前後2個Info的出現位置相減，前後都不算，再減一，再除以4即可得到「總線道數」(**ttl**)

依序讀出封包內第2\~4層的屬性，成為字典**d2\~d4**，再依照cols的順序將其內容存在v序列中，如此
重複每一個線道，就可以順利排列成完整的大資料表，作法與前例相同。

值得注意的是桃園市將資料筆數寫得很工整，每一個線道一定都會有大、中、小車的標籤屬性，這才能使程式較容易撰寫，減少很多判斷式。然而也因此多了很多沒有必要的'0'值，必須將其刪除以減省儲存空間，這是與前述範例差異之處。

d={}

for i in xrange(len(cols)):

d.update({cols[i]:v[i]})

df4=DataFrame(d)

drp=[]

for i in xrange(len(df4)):

**ss**=int(df4.loc[i,'Svolume'])+int(df4.loc[i,'Mvolume'])+int(df4.loc[i,'Lvolume'])

if ss==0 and int(df4.loc[i,'speed'])==0:

drp.append(i)

df4.**drop**(df4.index[drp], inplace=True)

df4[cols].set_index('vdid').to_csv('latest')

範例程式中設定如果三種車型的總流量(**ss**)是0，而且速度也是0，表示並沒有量測值，就直接就地將其刪除，使用**drop**指令來刪除資料表的橫向列。為使刪除速度可以增進，此處將0值序號先記住，最後一併刪除，再儲存檔案。

htm檔案[^103]之讀取

交通局網頁內容讀取案例

如前所示，BeautifulSoup是絕佳的html解碼器，以下範例即為台北市交通局網頁之內容，其後為讀取與整理程式。

kuang@master /home/backup/data/ETC/TaipeiVD/htm

$ more sht3_10_NI001.htm

\<html xmlns:v="urn:schemas-microsoft-com:vml"

xmlns:o="urn:schemas-microsoft-com:office:office"

xmlns:x="urn:schemas-microsoft-com:office:excel"

xmlns="http://www.w3.org/TR/REC-html40">

...

\<tr height=30 style='mso-height-source:userset;height:23.1pt'>

\<td height=30 class=xl117 style='height:23.1pt'>D\</td>

\<td class=xl117>▒@\</td>

\<td class=xl117>▒@\</td>

\<td class=xl121 align=right x:num>0\</td>

\<td class=xl121 align=right x:num>227\</td>

\<td class=xl121 align=right x:num>42\</td>

\<td class=xl121 align=right x:num>362\</td>

\<td class=xl158 align=right x:num="0.39999999999999991">40%\</td>

\<td class=xl121>▒@\</td>

\<td class=xl121>▒@\</td>

\<td class=xl121 align=right x:num>3\</td>

\<td class=xl121 align=right x:num>251\</td>

\<td class=xl121 align=right x:num>6\</td>

\<td class=xl121 align=right x:num>257\</td>

\<td class=xl158 align=right x:num="0.29">29%\</td>

\<td class=xl121>▒@\</td>

\<td class=xl121 align=right x:num>2\</td>

\<td class=xl121 align=right x:num>209\</td>

\<td class=xl121 align=right x:num>8\</td>

\<td class=xl121 align=right x:num>279\</td>

\<td class=xl158 align=right x:num="0.31">31%\</td>

\<td class=xl121>▒@\</td>

\<td class=xl121 align=right x:num>5\</td>

\<td class=xl158 align=right x:num="0.01">1%\</td>

\<td class=xl121 align=right x:num>687\</td>

\<td class=xl158 align=right x:num="0.91999999999999993">92%\</td>

\<td class=xl121 align=right x:num>56\</td>

\<td class=xl158 align=right x:num="0.07">7%\</td>

\<td class=xl121 align=right x:num>898\</td>

\<td class=xl122 align=right x:num="0.88217374213836486">0.88\</td>

\</tr>

...

> kuang@master /home/backup/data/ETC/TaipeiVD/htm
>
> $ cat rd_sht3.py
>
> from bs4 import **BeautifulSoup**
>
> from pandas import *
>
> from pypinyin import pinyin, lazy_pinyin
>
> import itertools
>
> def FindLastABC(end):
>
> for last in xrange(end,-1,-1):
>
> if a[last] in ABC:break
>
> return last
>
> with open('sss.txt') as ftext:
>
> s=[line.split('\\n')[0] for line in ftext]
>
> ABC=['A','B','C','D','E','F']
>
> year,time,dirn,name,road=[],[],[],[],[]
>
> nam_v=['Lvolume','Lratio','Mvolume','Mratio','Svolume','Sratio','PCU','PHF']
>
> v=[]
>
> for iv in xrange(8):
>
> v.append([])
>
> **note=['zhanming','zhan','shixiangshu']**
>
> for fname in s:
>
> yr=int(fname.split('_')[1])+90+1911
>
> if fname.split('.')[1]=='htm':
>
> #section 1
>
> fn=open(fname,'r')
>
> soup = BeautifulSoup(fn,'**html.parser**')
>
> **td=soup.find_all('td')**

a=[str(td[i]).split('>')[1].split('\<')[0] for i in
xrange(len(td))]

...

由範例中吾人可以發現，**td**與**/td**之間的內容是表格中的數值或文字，可以用**td=soup.find_all('td')**將其讀成序列，再利用split做2次切割，切出所要的內容(str(td[i]).split('>')[1].split('\<')[0])。讀出a序列之後，接著進行道路名稱(站名)的解析：

**#section 2**

b=[]

for i in xrange(100):

cha=a[i]

if type(cha)==float:

b.append(cha)

continue

if len(cha)\<2:

b.append(cha)

continue

**ss=lazy_pinyin(cha.decode('utf8'))**

**#section 3**

sss=''

for j in ss:

if j.isalnum():sss=sss+j

b.append(sss)

**#section 4**

for nt in note:

try:

b_note=b.index(nt)

except:

road_s='not_found'

else:

road_s=b[b_note+1]

break

section 2是先將序列中的數字分開，文字的長度如果小於2是單一字元，也不會是中文，就先儲存。其餘則運用中文拼音模組，將其翻譯為漢語拼音之字串(`ss=lazy_pinyin(cha.decode('utf8'))`)。由於ss是漢語字的序列，不方便進行比較與搜尋，

section 3將其黏成一長字串sss，儲存在b序列。

Section 4的目標是找出站名，一般會出現在「站名」之後，也有的htm出現在「站」或「時相數」之後，因此依序將其找出來，存在road_s變數以便儲存。

```python
> **#section 5**
>
> last=FindLastABC(len(a)-1)
>
A_last=a[last]
>
lastend=len(a)
>
if fname =='sht3_7_SI061.htm':A_last='D'
>
ampm='pm'
>
for chr in xrange(12): #repeat for A\~F twice
>
if fname == 'sht3_9_SI029.htm' and a[last]=='B':
>
lastend=last
>
last=FindLastABC(last-1)
>
if a[last] == A_last and ampm=='am':break
>
if a[last] == A_last and ampm=='pm':ampm='am'
>
continue
>
**#section 6**
>
tab=[]
>
for j in xrange(last,lastend):
>
try:
>
tt=float(a[j])
>
except:
>
if len(a[j])>1 and a[j][-1]=='%':
>
tab.append(float(a[j][:-1])/100)
>
else:
>
tab.append(tt)
>
**#section 7**
>
year.append(yr)
>
time.append(ampm)
>
dirn.append(a[last])
>
name.append((fname.split('_')[2]).split('.')[0])
>
road.append(road_s)
>
**if len(tab) \<8:**
>
for iv in xrange(8-len(tab)):**
>
**tab.insert(0,0.0)**
>
**len_tab=len(tab)**
>
for gt1 in xrange(1,10):**
>
**tt=tab[len(tab)-gt1]**
>
**if 0\< tt and tt \< 1:**
>
**len_tab=len_tab-gt1+1**
>
**break**
>
> if tab[len_tab-1] > 1 or tab[len_tab-1]==0.: tab=[0.0 for x in
> tab]
>
> for iv in xrange(len_tab-8,len_tab):
>
> v[iv-(len_tab-8)].append(tab[iv])
>
> **#section 8**
>
> lastend=last
>
> last=FindLastABC(last-1)
>
> if a[last] == A_last and ampm=='am':break
>
> if a[last] == A_last and ampm=='pm':
>
> ampm='am'
>
> **#section 9**
>
> d={'year':year,'time':time,'dirn':dirn,'name':name,'road':road}
>
> for iv in xrange(8):
>
> d.update({nam_v[iv]:v[iv]})
>
> df=DataFrame(d)
>
> for i in xrange(len(df)):
>
> sm=0.
>
> for j in nam_v:
>
> try:
>
> tt=float(df.loc[i,j])
>
> except:
>
> continue
>
> else:
>
> if tt>0:sm=sm+tt
>
> if sm==0.: df=df.drop(i)
>
> cols=['year','time','dirn','name','road']+nam_v
>
> df[cols].set_index('year').to_csv('sht3_df.csv')
```
FindLastABC是一個在序列a中尋找字母的小副程式，只要從指標end以相反方向在序列中找到A\~F中任一英文字母，就會回報該指標位置。藉由這支副程式，可以標定各方向的交通量統計結果。

section
6的重點在將前述標定結果內容，讀成一序列tab。由於該序列並非全是數字，有可能有空格中文字，也有可能有%符號，必須以試誤方式來判斷。

section
7目的在將各項數據儲存在序列裏。其中tab比較麻煩一點，有時會有數據不足(限制某種車輛進入車道)、或者數據太多(匝道交通量會出現在PHF之後)，因此需要逐一處理，原則就是，合計交通量最後一個數字一定是PHF，而該數字會是小於1的小數。

section 8預備讀取下一個方向數據之前處理，同時也設停止點(break)。section
9就將讀取結果整理成資料庫形式，然後輸出。

Wiki讀取交流道座標

fnames=['01F.csv','01H.csv','02F.csv','03A.csv','03F.csv','04F.csv','05F.csv',

'06F.csv','08F.csv','10F.csv']

guodao,sheshi,lat,lon=[],[],[],[]

for fname in fnames:

a=read_csv(fname)

c=a.columns[0]

for nam in list(a[c]):

url='https://zh.wikipedia.org/wiki/'+nam

sheshi.append(nam)

guodao.append(fname.replace('.csv',''))

try:

response = urllib2.urlopen(url)

except:

lat.append(0)

lon.append(0)

else:

html = response.read()

soup = BeautifulSoup(html,'html.parser')

sp=soup.find_all('span')

for i in xrange(len(sp)):

if 'class' not in sp[i].attrs:continue

if sp[i].attrs['class']==['latitude']:

for j in sp[i]:

lat.append(int(j[:2])+int(j[3:5])/60.+int(j[6:8])/3600.)

if sp[i].attrs['class']==['longitude']:

for j in sp[i]:

lon.append(int(j[:3])+int(j[4:6])/60.+int(j[7:9])/3600.)

df_exitXY=DataFrame({'lat':lat,'lon':lon,'nam':nam,'guodao':guodao})

df_exitXY.set_index('guodao').to_csv('df_exitXY.csv')

.json檔案之讀取與解析

桃園市2018年12月以後的VD檔案格式變成json格式，因此讀取解析程式也需要調整。

Json基本上就是dict，因此適用dict的操作方式：

kuang@master /home/backup/data/ETC/TaoyuanVD

$ more latest

{

"data" : [ {

"vdid" : "68000V100110",

"status" : "0",

"datacollecttime" : "2019/01/25 13:40:00",

"lane" : [ {

"vsrdir" : "0",

"vsrid" : "0",

"speed" : "48",

"laneoccupy" : "4.0",

"cars" : [ {

"carid" : "L",

"volume" : "4"

}, {

"carid" : "S",

"volume" : "28"

}, {

"carid" : "M",

"volume" : "0"

} ]

}, {

"vsrdir" : "0",

"vsrid" : "1",

"speed" : "45",

"laneoccupy" : "4.0",

"cars" : [ {

"carid" : "L",

"volume" : "1"

}, {

"carid" : "S",

"volume" : "27"

}, {

"carid" : "M",

"volume" : "0"

} ]

} ]

}, {

"vdid" : "68000V100360",

"status" : "0",

"datacollecttime" : "2019/01/25 13:40:00",

圖示latest檔案資料只有一項，key是data，對應到所有的內容，而latest[data]進去之後，則是個dict所形成的序列。