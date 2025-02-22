from pandas import *
import numpy as np

fname='/Users/kuang/Downloads/2024_crawler.csv'
df=read_csv(fname,encoding='utf8')
df.head()
def s2names(s):
    names = []
    i = 0 
    while i < len(s):
        # 找到下一個 "'" 字符
        end = s.find("':", i)
        if end == -1: 
            break
        # 找到下一個 "'" 字符
        start = s.find("'", end -4) 
        # 提取名字
        name = s[start+1:end]
        names.append(name)
        # 移動到下一個位置
        i = end + 1 
    return [i for i in names if len(i)>0]
fnames=[f"/Users/kuang/Downloads/202{i}_crawler.csv" for i in '2345']

years=[]
names=[]
budgs=[]
depgr=[]
for fname in fnames[:-1]:
    yr=fname[23:23+4]
    df=read_csv(fname,encoding='utf8')
    for i in range(len(df)):
        s=df.loc[i,'評審委員']
        if type(s)!=str:continue
        name_list=s2names(s)
        budg=df.loc[i,'決標金額']/len(name_list)
        if not df.loc[i,'是否得標']:budg*=-1
        for name in name_list:
            names.append(name)
            budgs.append(budg)
            dep=df.loc[i,'主辦部'].split(':')[1].replace('祖','組').replace("\'","").replace('"','')
            depgr.append(dep)
            years.append(yr)
dff=DataFrame({'year':years,'name':names,'budg':budgs,'depgr':depgr})

sdep=list(set(dff.depgr))
ndep=len(sdep)
for d in sdep:
    dfd=dff.loc[dff.depgr==d]
    pv=pivot_table(dfd,index=['year','name'],values=['budg'],aggfunc=sum).reset_index()
    yr_sum = {i:dfd.loc[dfd.year.astype(int)==i,'budg'].sum() for i in range(2022, 2026)}
    pv.year=[int(i) for i in pv.year]
    pv['budg_rate']=[i/yr_sum[j] for i,j in zip(pv.budg,pv.year)]
    pvm=pivot_table(pv,index=['name'],values=['budg_rate'],aggfunc=np.mean).reset_index()
    pvms=pvm.sort_values(by='budg_rate', ascending=False).reset_index(drop=True)

    names=[]
    yrs=[[],[],[]]
    for name in set(pv.name):
        a=pv.loc[pv.name==name]
        if len(a)==0:continue
        names.append(name)
        for y in range(3):
            yr=y+2022
            br=list(a.loc[a.year==yr,'budg_rate'])
            if len(br)>0:
                yrs[y].append(br[0])
            else:
                yrs[y].append(0)
    df_name_yr=DataFrame({'name':names,'y2022':yrs[0],'y2023':yrs[1],'y2024':yrs[2],})
    idx=np.where(df_name_yr.y2022*df_name_yr.y2023*df_name_yr.y2024>0)
    names=[]
    percent=[]
    for i in idx[0]:
        avg=(df_name_yr.loc[i,'y2022']+df_name_yr.loc[i,'y2023'])/2.
        if df_name_yr.loc[i,'y2024']<avg:
            name=df_name_yr.loc[i,'name']
            names.append(name)
            percent.append(round(100*list(pvms.loc[pvms.name==name,'budg_rate'])[0],3))
    dfnp=DataFrame({'name':names,f'percent_{d}':percent})
    dfnps=dfnp.sort_values(by=f'percent_{d}',ascending=False).reset_index(drop=True)
    n=str(sdep.index(d))
    dfnps.to_csv(f'dfnps{n}.csv',index=False)
    names=[]
    percent=[]
    for i in idx[0]:
        avg=(df_name_yr.loc[i,'y2022']+df_name_yr.loc[i,'y2023'])/2.
        if df_name_yr.loc[i,'y2024']>=avg:
            name=df_name_yr.loc[i,'name']
            names.append(name)
            percent.append(round(100*list(pvms.loc[pvms.name==name,'budg_rate'])[0],3))
    dfnp=DataFrame({'name':names,f'percent_{d}':percent})
    dfnps=dfnp.sort_values(by=f'percent_{d}',ascending=False).reset_index(drop=True)
    dfnps.to_csv(f'dfnpsGTavg{n}.csv',index=False)

