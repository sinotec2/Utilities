import pymssql
server = '200.200.32.31'
server = '200.200.32.31:1433'
user = 'SelectDB'
password = 'SelectDBPW'
conn = pymssql.connect(server, user, password, "SelectDB")
cursor.execute('SELECT * FROM dbo.tmp_month.statistics')
cursor = conn.cursor()
cursor.execute('SELECT * FROM dbo.tmp_month.statistics')
cursor.execute('SELECT * FROM dbo.tmp_month_statistics')
data = cursor.fetchall()
cursor.execute("EXEC sp_columns 'tmp_month_statistics'")
cols = cursor.fetchall()
colnames = [cols[i][3] for i in range(len(cols))]
colnames
from pandas import *
dd = {}
for i in range(len(cols)):
    dd.update({colnames[i]: [data[j][i] for j in range(len(data))]})
df = DataFrame(dd)
df.loc[0]
for c in ['縣市別','事業名稱','製程名稱','申報項目','申報種類']:
    df['tmp']=[i.encode('latin1').decode('big5') for i in df[c]]
    df[c]=df['tmp']
c
df[c].head()
for c in ['縣市別','事業名稱','製程名稱','申報項目','申報種類']:
    df['tmp']=[str(i).encode('latin1').decode('big5') for i in df[c]]
    df[c]=df['tmp']
for c in ['事業名稱','製程名稱','申報項目','申報種類']:
    df['tmp']=[str(i).encode('latin1').decode('big5') for i in df[c]]
    df[c]=df['tmp']
for c in ['製程名稱','申報項目','申報種類']:
    df['tmp']=[str(i).encode('latin1').decode('big5') for i in df[c]]
    df[c]=df['tmp']
df.loc[0]
df.tail()
df.loc[0]
c='事業名稱'
df['tmp']=[i.encode('latin1').decode('big5') for i in df[c]]
df[c]
a=[type(i) for i in df[c]]
set(a)
df['tmp']=[i.encode('latin1').decode('big5', errors='ignore') for i in df[c]]
c
len(set(df.tmp))
list(set(df.tmp))[:5]
for c in ['事業名稱','製程名稱','申報項目','申報種類']:
    df['tmp']=[str(i).encode('latin1').decode('big5', errors='ignore') for i in df[c]]
    df[c]=df['tmp']
df.loc[0]
df.loc[-1]
df.loc[30500]
c='工業區名稱'
df['tmp']=[i.encode('latin1').decode('big5', errors='ignore') for i in df[c]]
df['tmp']=[str(i).encode('latin1').decode('big5', errors='ignore') for i in df[c]]
df[c]=df.tmp
!lst
df.to_csv('df0_tmp_month.statistics_112.csv',index=False)
colnames
df[colnames].to_csv('df0_tmp_month.statistics_112.csv',index=False)
len(df)
cursor.execute("EXEC sp_columns 'tmp_month_statistics_store'")
data = cursor.fetchall()
cursor.execute('SELECT * FROM dbo.tmp_month_statistics_store')
data = cursor.fetchall()
cursor.execute("EXEC sp_columns 'tmp_month_statistics_store'")
cols = cursor.fetchall()
colnames = [cols[i][3] for i in range(len(cols))]
dd = {}
for i in range(len(cols)):
    dd.update({colnames[i]: [data[j][i] for j in range(len(data))]})
df = DataFrame(dd)
df.loc[0]
for c in ['縣市別','工業區名稱','事業名稱','製程名稱','申報項目','申報種類']:
    df['tmp']=[str(i).encode('latin1').decode('big5', errors='ignore') for i in df[c]]
    df[c]=df['tmp']
    print(c)
df.loc[0]
len(df)
df.loc[30500]
df[colnames].to_csv('df0_tmp_month.statistics_store_112.csv',index=False)
!lst
!head df0_tmp_month.statistics_112.csv
history -f tmp_monHis.py
