history -f his.py
vi his.py
!vi his.py
history -g -f his.py
!vi his.py
from pandas import *
df0=read_csv('df0.csv')
cols=list(df0.columns)
e=[i for i in cols if i[-4]=='▒~W▒▒~\~_']
e=[i for i in cols if i[-2:]=='▒~W▒▒~\~_']
d=[i for i in cols if '▒~P~M稱' in i]
e
d
e=[i for i in cols if i[-2:]=='名稱']
e
cols
d
e
e1=[i[:2] for i in e]
e1
[i for i in cols if i[:2] in e1 and i not in e]
[i for i in cols if i[:2] in e1 and i[-2:] not in ['管編','代碼']]
e==[i for i in cols if i[:2] in e1 and i[-2:] not in ['管編','代碼']]
set(e) - set([i for i in cols if i[:2] in e1 and i[-2:] not in ['管編','代碼']])
set([i for i in cols if i[:2] in e1 and i[-2:] not in ['管編','代碼']])-set(e)
[i for i in cols if i[:2] in e1 and i[-2:] in ['管編','代碼']]
f=[i for i in cols if i[:2] in e1 and i[-2:] in ['管編','代碼']]
len(e),len(f)
e
f
[i for i in cols if '物理' in i]
[i for i in cols if '收受' in i]
len(f)
f1=[i[:2] for i in f]
len(set(f1))
f.sort()
f1=[i[:2] for i in f]
e.sort()
e1=[i[:2] for i in e]
f1,e1
set(e)-set(f)
set(e1)-set(f1)
e2=[i for i in e if i[:2]!='收受']
e2
f
code_name={i:j fir i,j in zip(f,e2)}
code_name={i:j for i,j in zip(f,e2)}
code_name
import json
with open('code_name.json','w') as f:
    f.dump(code_name)
with open('code_name.json','w') as f:
    json.dump(f,code_name)
with open('code_name.json','w') as f:
    json.dump(code_name,f)
!cat code_name.json
f
f
e
fnames="ChineseNameMainIngredients BusinessOrganizationName RecyclingOrganizationName IndustrialAreaName WasteName NameOfRecipient FinalDisposalAgencyName ChineseNameHarmfulCharacteristics ChineseNameCleaningMethod ClearOrganizationName ChineseNamePhysicalProperties SpeciesChineseName ProcessingOrganizationName IndustryChineseName ProcessChineseName".split()
fnames
for c in code_name:
    df=df[c,code_name[c]]
for c in code_name:
    df=df0[c,code_name[c]]
for c in code_name:
    df=df0[[c,code_name[c]]]
df.head()
for c in code_name:
    df=df0[[c,code_name[c]]]
    df=df.sort_values(on=c).reset_index(drop=True)
    df=df.drop_duplicate()
for c in code_name:
    df=df0[[c,code_name[c]]]
    df=df.sort_values(c).reset_index(drop=True)
    df=df.drop_duplicate()
for c in code_name:
    df=df0[[c,code_name[c]]]
    df=df.sort_values(c).reset_index(drop=True)
    df=df.drop_duplicates().reset_index(drop=True)
df.head()
df.tail()
c
e.index(c)
e
f.index(c)
f2.index(c)
f=[i for i in cols if i[:2] in e1 and i[-2:] in ['管編','代碼']]
f.sort()
f
fnames
len(fnames)
fnames='MainIngredients,BusinessOrganization,RecyclingOrganization,IndustrialArea,WasteName,FinalDisposalAgency,HarmfulCharacteristics,CleaningMethod,ClearOrganization,PhysicalProperties,SpecieName,ProcessingOrganization,Industry,Process'.split(',')
len(fnames)
i=0
for c in code_name:
    df=df0[[c,code_name[c]]]
    df=df.sort_values(c).reset_index(drop=True)
    df=df.drop_duplicates().reset_index(drop=True)
    print(c,len(df))
    df.to_csv(fnames[i]+'.csv',index=False)
history -f code_name.py
i=0
for c in code_name:
    df=df0[[c,code_name[c]]]
    df=df.sort_values(c).reset_index(drop=True)
    df=df.drop_duplicates().reset_index(drop=True)
    print(c,len(df))
    df.to_csv(fnames[i]+'.csv',index=False)
    i+=1
history -f code_name.py
