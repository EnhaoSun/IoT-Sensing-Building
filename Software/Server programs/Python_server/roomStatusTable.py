import pymysql

db = pymysql.connect("localhost", "root", "", "testdb")

c = db.cursor()

c.execute("drop table if exists RoomStatus")

c.execute("""create table RoomStatus(
	ts TIMESTAMP NOT NULL,
	WINDOW TINYINT NOT NULL,
	DOOR TINYINT NOT NULL,
	CHAIR TINYINT NOT NULL,
	LIGHT TINYINT NOT NULL,
	)""")
print ("Table created successfully")
db.close()
