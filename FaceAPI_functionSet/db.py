import pyodbc
import time
dsn = 'rpitestsqlserverdatasource'
user = 'makeNTU050@makentu'
password = 'GGininder123'
database = 'make'
connString = 'DSN={0};UID={1};PWD={2};DATABASE={3};'.format(dsn,user,password,database)
conn = pyodbc.connect(connString)
time.sleep(2)

cursor = conn.cursor()

#cursor.execute('CREATE TABLE makeNTU(name varchar(60), med varchar(60))')
#cursor.execute("INSERT INTO make1(name, med) VALUES (, '2') ON DUPLICATE KEY UPDATE med = '2'")
#cursor.execute("insert into makeNTU(name, med) values ('dick123', '0')")
#cursor.execute("insert into makeNTU(name, med) values ('hao123', '1')")
cursor.execute("insert into makeNTU(name, med) values ('fucker9487', '1')")
cursor.commit()
cursor.execute("SELECT * FROM makeNTU")
tables = cursor.fetchall()

print(tables)
