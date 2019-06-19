import csv
import pymysql

conn = pymysql.connect("localhost", "root", "", "testdb")

c = conn.cursor()
print ("Opened database successfully")

table_name = "windowAcc"
c.execute("SELECT ts, AWX, AWY, AWZ, ACTIVITY from " + table_name)
data = c.fetchall()

csvfile = open('windowAcc.csv', 'w')
writer = csv.writer(csvfile)

writer.writerow(['date','x', 'y', 'z', 'activity'])
writer.writerows(data)
csvfile.close()

conn.close()
