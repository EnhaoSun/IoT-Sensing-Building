import pymysql

db = pymysql.connect("localhost", "root", "", "testdb")

c = db.cursor()

c.execute("drop table if exists pressureData")

c.execute("""create table pressureData(
	ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRESSURE FLOAT NOT NULL,
	ACTIVITY TEXT
	)""")
print ("pressureData Table created successfully")
db.close()
