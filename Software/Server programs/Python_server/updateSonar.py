import pymysql
import datetime

db = pymysql.connect("localhost", "root", "", "testdb")
c = db.cursor()

table_name = "MobileAccelerometer"

today = datetime.date.today()

time_start = input("What time do you want to start update?\n")
time_start = today.strftime('%Y') + " " + time_start
print(time_start)

time_end = input("What time do you want to end update?\n")
time_end = today.strftime('%Y') + " " + time_end
print(time_end)

activity = input("What activity do you want update?\n")
print(activity)

try:
	c.execute("UPDATE " + table_name + " set activity = '" + activity + "'" + "where date BETWEEN '%s' and '%s'" %(time_start, time_end))
	db.commit()
	print ("Total number of rows updated : %d" % db.total_changes)
except:
	db.rollback()
	
try:
	c.execute("SELECT * from " + table_name + " WHERE date BETWEEN '%s' and '%s'" %(time_start, time_end))
	results = c.fetchall()
	for row in results:
		print ("date = %s, x = %.4f, y = %.4f, z = %.4f, activity = %s" % (row[0], row[1], row[2], row[3], row[4]))
	print ("Operation done successfully")
except:
	print("Error: unable to fetch data")

db.close()
