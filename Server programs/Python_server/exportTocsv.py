import csv
import pymysql

conn = pymysql.connect("localhost", "root", "", "testdb")

c = conn.cursor()
print ("Opened database successfully")

table_name = "SensorData"
c.execute("SELECT ts, LUX, TEMPERATUREIN, TEMPERATUREWIN, SONARIN, SONAROUT, RCWL, PRESSURE, ADX, ADY, ADZ, AWX, AWY, AWZ, ACTIVITY from " + table_name)

data = c.fetchall()

writer.writerow(['date', 'lux', 'tem_in', 'tem_win', 'sonar_in', 'sonar_out', 'move','p', 'adx', 'ady', 'adz', 'awx', 'awy', 'awz', 'activity'])

writer.writerows(data)
csvfile.close()

conn.close()
