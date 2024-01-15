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

df=read_csv('paths.csv')
# creating a pdf file object
df=df.loc[df.Filename.map(lambda x:'pdf'==x[-3:])].reset_index(drop=True)
pdf_files = list(df.Filename)
if len(pdf_files)==0:sys.exit('must have PDF in Filename')
k=0
for fname in pdf_files:
    fnameO=list(df.loc[df['Filename']==fname,'Y06path'])[0]+fname.split('\\')[-1].replace('.pdf','.txt')
    if os.path.exists(fnameO): continue
    fname1=list(df.loc[df['Filename']==pdf_files[0],'Y06path'])[0]+fname.split('\\')[-1].replace('.pdf','.txt')
    if os.path.exists(fname1): 
        os.system('move /Y '+fname1+' '+fnameO)
        continue
    try:
        pdfFileObj = open(fname, 'rb')
    except:
        with open('not_write.txt','a') as f:
            f.write(fname+'\n')
        continue
# creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    a=''
    i=1
    for pageObj in pdfReader.pages:
        a+=pageObj.extract_text()#.replace(chap+'-'+str(i),'\n').replace(chap+' - '+str(i),'\n')
        i+=1
    lines=a.split('\n')
    outlines=[l.strip().split(':')[0].split('：')[0] for l in lines]
    outlines=[l for l in outlines if (dots(l) or CNnum(l) or ENnum(l))  and len(l)<60]# and FloatNotInLine(l)]
    outlines=[l for l in outlines if '-' not in l and '所示' not in l]
    if len(outlines)==0:continue
    with open(fnameO,'w', encoding='utf-8') as f:
        for i in lines:
            f.write(i+'\n')
    k+=1                
#    if k==10:break