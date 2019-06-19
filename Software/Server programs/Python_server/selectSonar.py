import pymysql
import datetime

db = pymysql.connect("localhost", "root", "", "testdb")
c = db.cursor()

table_name = "SonarData"

today = datetime.date.today()

time_start = input("What time do you want to start select?\n")
#time_start = today.strftime('%Y-') + time_start
time_start = "2018-03-20 " + time_start
print(time_start)

time_end = input("What time do you want to end update?\n")
#time_end = today.strftime('%Y-') + time_end
time_end = "2018-03-20 " + time_end
print(time_end)

try:
	c.execute("SELECT * from " + table_name + " WHERE ts BETWEEN '%s' and '%s'" %(time_start, time_end))
	print("21")
	results = c.fetchall()
	for row in results:
		print ("date = %s, IN = %d, OUT = %d, activity = %s" % (row[0], row[1], row[2], row[3]))
	print ("Operation done successfully")
except:
	print("Error: unable to fetch data")

db.close()
