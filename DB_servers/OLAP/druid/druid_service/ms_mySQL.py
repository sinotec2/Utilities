import pymssql
from pandas import *

server = '200.200.32.31:1433'
user = 'SelectDB'
password = 'SelectDBPW'
database = 'SelectDB'

conn = pymssql.connect(server, user, password, database)
cursor = conn.cursor()
cursor.execute('SELECT * FROM dbo.Dlist ')
data = cursor.fetchall()
cursor.execute("EXEC sp_columns 'Dlist'")
cols = cursor.fetchall()
colnames = [cols[i][3] for i in range(len(cols))]
fname = 'df0_111.csv'
dd = {}
for i in range(len(cols)):
    dd.update({colnames[i]: [data[j][i] for j in range(len(data))]})
df = DataFrame(dd)
df.to_csv(fname,index=False)
