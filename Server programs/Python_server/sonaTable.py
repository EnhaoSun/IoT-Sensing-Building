import pymysql

db = pymysql.connect("localhost", "root", "", "testdb")

c = db.cursor()

c.execute("drop table if exists SonarData")
	#ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

c.execute("""create table SonarData(
	ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	SONARIN INT NOT NULL,
	SONAROUT INT NOT NULL,
	ACTIVITY TEXT
	)""")
print ("Sona Table created successfully")
db.close()
