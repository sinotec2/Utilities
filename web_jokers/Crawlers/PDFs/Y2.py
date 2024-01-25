import PyPDF2
import sys, glob, os
from pandas import *

def dots(l):
    tdic={'':'.','(':')','（':'）'}
    for p in ['','(','(']:
        for i in range(1,11):
            a=p+str(i)+tdic[p]
            n=len(a)
            if l[:n]==a:return True
    return False
def CNnum(l):
    num=['一','二','三','四','五','六','七','八','九','十',]
    tdic={'':'、','(':')','（':'）'}
    for p in ['','(','(']:
        for i in num:
            a=p+i+tdic[p]
            n=len(a)
            if l[:n]==a:return True
    return False
def ENnum(l):
    num='ABCDEFGHabcdefgh'
    tdic={'':['.','、'],'(':')','（':'）'}
    for p in ['','(']:
        for i in num:
            t=tdic[p]
            if type(t)==list:
                for tt in t:
                    a=p+i+tt
                    n=len(a)
                    if l[:n]==a:return True
            else:
                a=p+i+t
                n=len(a)
                if l[:n]==a:return True
    return False

def is_empty_file(file_path):
    return os.path.getsize(file_path) == 0

def rep_str(label,anchor,new_str):
    a=[i for i in list(df.Filename) if label in i][0]
    ibeg=a.index(anchor)
    bxg=a[ibeg:ibeg+4]
    df_bxg=df.loc[df.Filename.map(lambda x:bxg in x)].copy()
    df_bxg['Filename'] = df_bxg['Filename'].str.replace(bxg, new_str)
    df_bxg['Y06path'] = df_bxg['Y06path'].str.replace(bxg, new_str)
    df.loc[df_bxg.index]=df_bxg
    return df
def old_new(oddPath,old,new):
    oldF=oddPath+old
    newF=oddPath+new
    idx=df.loc[df.Filename==oldF].index[0]
    df.loc[idx,'Filename']=newF
    return df

for fnameH in ['not_write','written']:
    locals()[fnameH] = set()
    fname=fnameH+'.txt'
    if os.path.exists(fname):
        with open(fname,'r') as f:
            locals()[fnameH] = set([line.strip('\n') for line in f])
if os.path.exists('not_write.txt') and len(not_write)>0:
    with open('not_write.txt','w') as f:
        for fname in not_write:
            f.write(fname+'\n')
# creating a pdf file object
df=read_csv('paths2.csv')
df=df.loc[df.Filename.map(lambda x:'pdf'==x[-3:])].reset_index(drop=True)

#replace the odd str for stainless
df=rep_str('污水人孔設置不','不','不銹鋼')

# replace the str liuhengchang
df=rep_str('簡源水','劉','劉恒昌')

oPaths=[r'\\nas03.sinotech-eng.com\Y10\Y2\PROJECT\下水道資料庫17\09-4流量計及水位計及水質監測\廠商資料\2019桓達(導波雷達液位計及電磁流量計)',
r'\\nas03.sinotech-eng.com\Y10\Y2\PROJECT\下水道資料庫17\17自來水及地下水\自來水錶(智慧水網)'       ]
oldT=[r'\EPD _餌_撘�潷_�醂_new_1872403756.pdf',r'\弓銓��.pdf']
newT=[r'\EPD _餌_撘____new_1872403756.pdf',r'\弓銓.pdf']

for i in range(2):
    df=old_new(oPaths[i],oldT[i],newT[i])

pdf_files = list(df.Filename)
if len(pdf_files)==0:sys.exit('must have PDF in Filename')
a=r"\\nas03.sinotech-eng.com\Y10\Y1\PROJECT\空污資料庫\03-2研討會(環分環工氣膠)投稿\03-1環工學會空污研討會\2020環工學會空污研討會\3.論文集\第三十二屆環工年會論文集(全文)(密碼32).pdf"
passwds={a:'32'}   
k=0
skips=[1461,9121,14083,14100]
iskip=-1
sys.exit()
for fname in pdf_files:
#    print(fname)
    iskip+=1
    if iskip<=14100:continue
    if iskip in skips:continue #japanese content/平面圖
    fnameO=list(df.loc[df['Filename']==fname,'Y06path'])[0]+fname.split('\\')[-1].replace('.pdf','.txt')
#    if fnameO==r'Y:\Y06\P3_AI專案\txt_paths\Y2\PROJECT\廠站資料庫17\L-原O槽資料庫\台南水再生規劃服建書\參考資料\永康水質淨化場\施工規範及施工說明書\規範全.txt':
#        sys.exit(fnameO)
    if fnameO in written:
        print(iskip,fnameO)
        continue
    else:
        if os.path.exists(fnameO): 
            if '污水人孔設置不' in fname:
                fnameO=fnameO[:57]+'銹鋼'+fnameO[60:]
            with open('written.txt','a') as f:
                ipass=0
                for n in newT:
                    if n[1:-4] in fnameO:ipass=1
                if ipass==0:f.write(fnameO+'\n')
            written.add(fnameO)
            continue
#    fname1=list(df.loc[df['Filename']==pdf_files[0],'Y06path'])[0]+fname.split('\\')[-1].replace('.pdf','.txt')
#    if os.path.exists(fname1): 
#        os.system('move /Y '+fname1+' '+fnameO)
#        continue
    try:
        if is_empty_file(fname):
            with open('filesize0.txt','a') as f:
                f.write(fname+'\n')        
            continue
        pdfFileObj = open(fname, 'rb')
    except:
        with open('not_write.txt','a') as f:
            f.write(fname+'\n')
        continue
# creating a pdf reader object
    try:
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
    except:
        with open('not_write.txt','a') as f:
            f.write(fname+'\n')
        continue
        
    if pdfReader.is_encrypted :
        if fname in passwds:
            pdfReader.decrypt(passwds[fname])
        else:
            with open('passwd.txt','a') as f:
                f.write(fname+'\n')
            continue            
    a=''
    i=1
    try:
        for pageObj in pdfReader.pages:
            try:
                a+=pageObj.extract_text()#.replace(chap+'-'+str(i),'\n').replace(chap+' - '+str(i),'\n')
            except:
                break
            i+=1
        lines=a.split('\n')
    except:
        lines=''
    if len(lines)==0:
        with open('line0.txt','a') as f:
            f.write(fname+'\n')
        continue
    try:
        with open(fnameO,'w', encoding='utf-8') as f:
            for i in lines:
                f.write(i+'\n')                
        written.add(fnameO)
        with open('written.txt','a') as f:
            if newT[1][1:-4] in fnameO:
                f.write(fnameO.encode('utf-8')+'\n')       
            else:
                f.write(fnameO+'\n')
    except:
        with open('not_write.txt','a') as f:
            for i in range(2):
                if oldT[i][1:-4] in fname:
                    f.write(fname.encode('utf-8')+'\n')       
                else:
                    f.write(fname+'\n')
    k+=1                
#    if k==1:break