from pandas import *
fname='df0.csv'
df110=read_csv(fname)
c1=df110.columns
fname='df0_111.csv'
df111=read_csv(fname)
c2=df111.columns
set(c2)-set(c1)
set(c1)-set(c2)
c1
df110['申報日期'].head()
df111['申報日期'].head()
df110['申報日期2'].head()
df110['申報日期']=df110['申報日期2'][:]
df110['申報日期'].head()
del df110['申報日期2']
c1=df110.columns
c2=df111.columns
set(c1)-set(c2)
set(c2)-set(c1)
c1==c2
all.(c1==c2)
(c1==c2).all()
!grep df ~/bin/*.py|grep conca
df = concat([df110, df111], ignore_index=True)
df['timestamp'] = to_datetime(df['申報日期'])
is_increasing = (df['timestamp'].diff().dt.total_seconds() > 0).all()
is_increasing
is_increasing = (df['timestamp'].diff().dt.total_seconds() >= 0).all()
is_increasing
df2=df.sort_values('申報日期').reset_index(drop=True)
(df2['timestamp'].diff().dt.total_seconds() >= 0).all()
df2['timestamp'].head()
df2['申報日期'].head()
df2['timestamp'].tail()
df2['timestamp'].tail().diff().dt.total_seconds()
a=df2['timestamp'].diff().dt.total_seconds()
a.head()
(a[1:]>= 0).all()
is_increasing = (df['timestamp'].diff().dt.total_seconds()[1:] >= 0).all()
is_increasing
(df2['timestamp'].diff().dt.total_seconds()[1:] >= 0).all()
del df2['timestamp']
df2.head()
df2.tail()
df2.to_csv('df2.csv',ignore_index=True)
df2.to_csv('df2.csv',index=False)
c1
fname
[i for i in c2 if '名稱' in i]
for c in [i for i in c2 if '名稱' in i]:
    del df2[c]
df2.to_csv('df2.csv',index=False)
!st
!lst
!pewd
!pwd
history -f concat.py
