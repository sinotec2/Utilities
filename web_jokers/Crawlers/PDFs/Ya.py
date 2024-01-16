import os
import subprocess
from pandas import *

dirs=['離岸風電資料','空污資料庫']
Y1=[]
for dir in dirs:
    Y1+=subprocess.check_output('dir /b /s \\\\nas03.sinotech-eng.com\\Y10\\Y1\\PROJECT\\'+dir+'\\*',shell=True).decode('big5').split('\r\n')
d='環評資料庫'
for i in range(31):
    dir=d+'\\{:02d}-*'.format(i)
    Y1+=subprocess.check_output('dir /b /s \\\\nas03.sinotech-eng.com\\Y10\\Y1\\PROJECT\\'+dir,shell=True).decode('big5').split('\r\n')
Y3=subprocess.check_output('dir /b /s Y:\\Y3\\*',shell=True).decode('big5').split('\r\n')
Y4=subprocess.check_output('dir /b /s Y:\\Y4\\*',shell=True).decode('big5').split('\r\n')
Y={i:{} for i in [1,3,4]}
Yx={1:Y1,3:Y3,4:Y4}
for x in [1,3,4]:
    for ext in ['pdf','doc','ppt']:
        Y[x].update({ext:[i for i in Yx[x] if '?' not in i and ext in i[-5:].lower()]})

#新創目錄在Y06，以便儲存txt檔案
root='Y:\\Y06\\P3_AI專案\\txt_paths'
beg={1:28,3:2,4:2}
Ya=[]
paths=[]
for x in [1,3,4]:
    for ext in exts:
        Ya+=Y[x][ext]
        for a in Y[x][ext]:
            p=a.split('\\')
            path=root+a.replace(p[-1],'')[beg[x]:]
            path=path.replace(' ','\ ')#.replace(',','\\,')
            paths.append(path)
            if ' ' in path or ',' in path or '&' in path:
                os.system('mkdir "'+path+'" >nul 2>&1')
            else:
                os.system('mkdir '+path+' >nul 2>&1')
#            k+=1
#            if ' ' in path:break
#            if k>11:break
df=DataFrame({'Y06path':paths,'Filename':Ya})
df.set_index('Filename').to_csv('paths.csv')