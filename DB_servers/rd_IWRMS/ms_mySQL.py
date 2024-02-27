import pymssql
server = '200.200.32.31'
server = '200.200.32.31:1433'
user = 'SelectDB'
password = 'SelectDBPW'
conn = pymssql.connect(server, user, password, "tempdb")
cursor = conn.cursor()
conn.execute('SELECT * FROM *')
conn = pymssql.connect(server, user, password, "SelectDB")
cursor = conn.cursor()
cursor.execute('SELECT * FROM dbo')
cursor.execute('SELECT * FROM *')
cursor.execute('SELECT * FROM SelectDB')
conn = pymssql.connect(server, user, password, "SelectDB")
cursor = conn.cursor()
cursor.execute('SELECT * FROM SelectDB')
conn = pymssql.connect(server, user, password, "dbo")
cursor = conn.cursor()
conn = pymssql.connect(server, user, password, "SelectDB")
cursor = conn.cursor()
cursor.execute('SELECT * FROM "SelectDB"')
cursor.execute('SELECT * FROM dbo.Dlist ')
data = cursor.fetchall()
cursor.execute("describe dbo.Dlist")
cursor.execute("EXEC sp_columns 'Dlist'")
cols = cursor.fetchall()
cols
len(cols)
cols = [cols[i][0] for i in range(len(cols))]
cols
cols = cursor.fetchall()
cols[0]
cursor.execute("EXEC sp_columns 'Dlist'")
cols = cursor.fetchall()
cols[0]
cols[0][4]
cols[0][3]
colnames = [cols[i][3] for i in range(len(cols))]
colnames
from pandas import *
fname = 'df0_111.csv'
dd = {}
for i in range(len(cols)):
    dd.update({colnames[i]: [data[j][i] for j in range(len(data))]})
df = DataFrame(dd)
df.loc[100]
raw_data = "¨ä¥L¥ú¹q§÷®Æ¤Î¤¸¥ó»s³y·~"
raw_data.encode('utf-16le').decode('utf-8')
raw_data = "¨ä¥L¥ú¹q§÷®Æ¤Î¤¸¥ó»s³y·~"
raw_data.encode('big5').decode('utf-8')
raw_data = df.loc[100,'清理方式中文名稱']
type(raw_data)
print(raw_data)
print(raw_data.encode('utf8'))
print(raw_data.encode('utf8').decode('utf-8'))
raw_data.encode('utf8').decode('utf-8')
cols[-1]
history -f ms_mySQL.py
