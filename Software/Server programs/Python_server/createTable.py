import pymysql

db = pymysql.connect("localhost", "root", "", "testdb")

c = db.cursor()

c.execute("drop table if exists SensorData")
	#ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
c.execute("""create table SensorData(
	ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	LUX INT NOT NULL,
	TEMPERATUREIN FLOAT NOT NULL,
	TEMPERATUREWIN FLOAT NOT NULL,
	SONARIN INT NOT NULL,
	SONAROUT INT NOT NULL,
	RCWL INT NOT NULL,
	PRESSURE FLOAT NOT NULL,
	ADX FLOAT NOT NULL,
	ADY FLOAT NOT NULL,
	ADZ FLOAT NOT NULL,
	AWX FLOAT NOT NULL,
	AWY FLOAT NOT NULL,
	AWZ FLOAT NOT NULL,
	ACTIVITY TEXT
	)""")
print ("Table created successfully")
db.close()
