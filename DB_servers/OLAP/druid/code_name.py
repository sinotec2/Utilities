#!python3.9

from pandas import *
import json
import chardet

fname='df0_112.csv'
df0=read_csv(fname)
cols=list(df0.columns)
e=[i for i in cols if i[-2:]=='名稱']
e.sort()
f=[i for i in cols if i[-2:] in ['管編','代碼']]
f.sort()
code_name={i:j for i,j in zip(f,e)}
with open('code_name.json','w') as f:
    json.dump(code_name,f)
# 15組版本（2021）
fnames="ChineseNameMainIngredients BusinessOrganizationName RecyclingOrganizationName IndustrialAreaName WasteName NameOfRecipient FinalDisposalAgencyName ChineseNameHarmfulCharacteristics ChineseNameCleaningMethod ClearOrganizationName ChineseNamePhysicalProperties SpeciesChineseName ProcessingOrganizationName IndustryChineseName ProcessChineseName".split()

# 修正代碼成為字元
c='工業區代碼'
df0.loc[df0[c]==99,c]='99   '
c='行業別代碼'
idx=df0.loc[df0[c].map(lambda x:type(x)!=str and not (np.isnan(x)))].index
a=list(df0.loc[idx,c])
df0.loc[idx,c]=[str(int(i)) for i in a]

# 中文碼校正
for n in e+['縣市別','申報途徑','廢棄物種類(一般&有害)']:
    idx=df0.loc[df0[n].map(lambda x:type(x)==str)].index
    a=list(df0.loc[idx,n])
    if chardet.detect(a[0].encode())['encoding'] != 'latin1':continue
    df0.loc[idx,n]=[str(i).encode('latin1').decode('big5', errors='ignore') for i in a]
df0.to_csv(fname,index=False)

#10組版本(2022)
fnames="BusinessOrganizationName RecyclingOrganizationName IndustrialAreaName WasteName FinalDisposalAgencyName ChineseNameCleaningMethod ClearOrganizationName ProcessingOrganizationName IndustryChineseName ProcessChineseName".split()

# 寫出對照表以供Druid LOOKUP使用
kv=['key','value']
i=0
for c in f:
    n=code_name[c]
    df=df0[[c,n]]
    df=df.dropna()
    df=df.sort_values(c).reset_index(drop=True)
    df=df.drop_duplicates().reset_index(drop=True)
    df.columns=kv
    df.to_csv(fnames[i]+'.csv',index=False)
    print(c,n)
    i+=1
