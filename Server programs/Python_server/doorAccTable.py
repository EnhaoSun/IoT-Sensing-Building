import pymysql

db = pymysql.connect("localhost", "root", "", "testdb")

c = db.cursor()

c.execute("drop table if exists doorAcc")
	#ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
c.execute("""create table doorAcc(
	ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	ADX FLOAT NOT NULL,
	ADY FLOAT NOT NULL,
	ADZ FLOAT NOT NULL,
	ACTIVITY TEXT
	)""")
print ("doorAcc Table created successfully")
db.close()
