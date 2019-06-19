import serial
import pymysql
import time
import sys

ser = serial.Serial('/dev/ttyS0', 9600, timeout = 1)

conn = pymysql.connect("localhost", "root", "", "testdb")
cur = conn.cursor()

sleeptime = 0
notify = 1
dic = {'SONARIN': None, 'SONAROUT':None}
s = ["l","i","o","s","r", "p","d", "w"];
index = 3

def insertData():
	print("ready to insert")
	insert_sql = "insert into SonarData(SONARIN, SONAROUT) VALUES ('%d', '%d')" %\
	(dic['SONARIN'], dic['SONAROUT'])
	try:
		cur.execute(insert_sql)
		conn.commit()
		print("insert success")
	except:
		conn.rollback()

def accdataformate(data):
	index1 = data.find(',', 1)
	if index1 != -1:
		index2 = data.find(',', index1 + 1)
		if index2 != -1:
			return 1
		else:
			return 0
	else:
		return 0

def datavalid(data, startindex, endindex):
	for char in data[startindex:endindex]:
		if char < "," or char > "9" or char == "/":
			return 0
	return 1

def checkdata(data):
	for datahex in data:
		if datahex > 0x7f:
			return 0
	return 1

if __name__ == "__main__":
	print("Start!")
	ser.write(s[index].encode("UTF-8"))
	while True:
		try:
			try:
				data = ser.readline()
			except serial.SerialTimeoutException:
				ser.write(s[index].encode("UTF-8"))

			#check whether data in hex is valid
			if checkdata(data) == 0:
				print("hex data invalid")
				ser.write(s[index].encode("UTF-8"))
				continue

			data = data.decode("ascii")
			if data.find('(') == -1 or data.find(')') == -1:
				print ("data losed, re-request data")
				ser.write(s[index].encode("UTF-8"))
				continue
	
			data = data.strip('\n')
			startindex = data.find('(')
			endindex = data.find(')')
	
			if index == 3:
				if data[1] == 'S':
					try:
						index_so = data.find(',', 1)
						si = data[2 : index_so]
						so = data[index_so+1 : endindex]
						print("Sona in:%d,out:%d" % (int(si),int(so)));
						dic['SONARIN'] = int(si)
						dic['SONAROUT'] = int(so)
						insertData()
						ser.write(s[index].encode("UTF-8"))
						continue
					except ValueError:
						print("SONA data invalid")
						ser.write(s[index].encode("UTF-8"))
						continue
				else:
					print("Sona data error")
					ser.write(s[index].encode("UTF-8"))
					continue
			else:
				print("nothing")
				print(data)
				ser.write(s[index].encode("UTF-8"))
				continue
		except KeyboardInterrupt:
			print("Paused")
			inp =input('continue? (y/n)')
			if inp == 'y':
				index = 3
				continue
			elif inp == 'n':
				sys.exit(0)
			else:
				raise Exception('Invalid input')

	cur.close()
	conn.close()
