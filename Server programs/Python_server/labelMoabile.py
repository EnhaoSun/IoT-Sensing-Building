import csv
import pymysql

conn = pymysql.connect("localhost", "root", "", "testdb")

c = conn.cursor()
print ("Opened database successfully")

table_name = "MobileAccelerometer"
c.execute("select date, max, may, maz, activity from " + table_name)

data = c.fetchall()

print(len(data))
row = data[0]
print(row[0])

"""
csvfile = open('mobile.csv', 'w')
writer = csv.writer(csvfile)

writer.writerow(['date', 'x', 'y', 'z', 'activity'])

writer.writerows(data)
csvfile.close()
"""

conn.close()
