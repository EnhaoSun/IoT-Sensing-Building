import pymysql

db = pymysql.connect("localhost", "root", "", "testdb")

c = db.cursor()

c.execute("drop table if exists windowAcc")
	#ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
c.execute("""create table windowAcc(
	ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	AWX FLOAT NOT NULL,
	AWY FLOAT NOT NULL,
	AWZ FLOAT NOT NULL,
	ACTIVITY TEXT
	)""")
print ("windowAcc Table created successfully")
db.close()
