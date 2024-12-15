kuang@eng06 /nas2/kuang/MyPrograms/GoogleCalendarAPI
$ cat break_md2.py
import os, sys
import pandas as pd
from datetime import datetime
from anthropic import Anthropic
import shutil

# 局部替代檔案字串
def sub_str(md_file,tag,newstr):
    with open(md_file, 'r') as file:
        lines = [line.strip() for line in file]
    # 替換行
    n=len(tag)
    lines = [newstr if line[:n] == tag else line for line in lines]
    with open(md_file, 'w') as file:
        file.write('\n'.join(lines) + '\n')
    return 0

# 分析部門當前重要事務

def summ_evnt(i,summ):
    api_key=os.getenv('ANTHROPIC_API_KEY', None)
    if not api_key:sys.exit('must export ANTHROPIC_API_KEY')
    client = Anthropic(api_key=api_key)
    prompt = [
              f"我會給你最近四週所有部門會發生的事件摘要，請從公司高層管理者的角度來檢討，提出前五大事件做出提示，\
               語氣請用秘書口吻一次性地提醒，不必說尊敬的長官云云、也不必署名、不必詢問是否需要進一步的細節說明、不要說如有任何需要進一步討論的事項，隨時告知。\
               事件摘要清單如下: {summ}",
              f"請給出一句話之精簡重點摘要(不必再前提)以下是我的內容：{summ}",
             ]
    headers=['','content: ']
    return headers[i] + client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt[i]}]
    ).content[0].text


# 定義常數
PATH = '/nas2/VuePressSrc/Sup.calendars/zh'
DEP_PTH = {'ICT': 'support'}
CAT_NAM = {
    '其他事項': 'others',
    '同仁行程': 'itinerary',
    '會議與活動': 'meeting_events',
    '計畫成果提交進度': 'submission_progress'
}
FNAME = 'whole.csv'

# 讀取 CSV 檔案
df = pd.read_csv(FNAME, parse_dates=['datetime'])

# 獲取唯一部門和列
dpts = df['department'].unique()
cols = ['OutDT', 'event', 'group']

today = 'lastUpdated: '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cnts=[
'list:',
'content:',
]

# 遍歷每個部門和類別
for d in dpts:
    df_d = df[df['department'] == d]
    cats = df_d['category'].unique()

    for c in cats:
        dir_path = os.path.join(PATH, DEP_PTH[d], CAT_NAM[c])
        # 複製檔案
        tmp_file = f"{dir_path}.tmp"
        md_file = f"{dir_path}.md"
        if os.path.exists(tmp_file):
            shutil.copy(tmp_file, md_file)
        result=sub_str(md_file,'lastUpdated',today)
        df_c = df_d[df_d['category'] == c]
        periods = df_c['period'].unique()

        for p in periods:
            df_p = df_c[df_c['period'] == p].sort_values(by='datetime').reset_index(drop=True)
            if df_p.empty:
                continue

            # 創建內容
            content = '\n'.join(df_p[cols].astype(str).agg('\t'.join, axis=1))
            result=sub_str(md_file, f'add{p}',content)

        #如果還有沒有被替代的，則填上(無訊息)
        periods = df['period'].unique()
        content = '(無訊息)'
        for p in periods:
            result=sub_str(md_file, f'add{p}',content)

    dir_path = os.path.join(PATH, DEP_PTH[d], 'README')
    # 複製檔案
    tmp_file = f"{dir_path}.tmp"
    md_file = f"{dir_path}.md"
    if os.path.exists(tmp_file):
        shutil.copy(tmp_file, md_file)
    df_p=df_d.loc[df_d.period==31]
    content = '\n'.join(df_p[cols].astype(str).agg('\t'.join, axis=1))
    strs=[]
    strs.append(summ_evnt(0,content))
    strs.append(summ_evnt(1,strs[0]))
    for i in [0,1]:
        result=sub_str(md_file,cnts[i],strs[i])

# 上傳命令
os.chdir('/nas2/VuePressSrc/Sup.calendars')
#os.system('./upload.cs')
'''
$ cat /nas2/VuePressSrc/Sup.calendars/upload.cs

#!/usr/bin/bash
/usr/bin/git init
/usr/bin/git add .
dt=$(date +%Y%m%d)
/usr/bin/git commit -m "updated $dt"
/usr/bin/git push -f http://kuang:sinotec2@eng06.sinotech-eng.com:3000/Sup/calendars.git main
'''

