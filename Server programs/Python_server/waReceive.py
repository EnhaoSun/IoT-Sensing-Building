import serial
import pymysql
import time
import sys

ser = serial.Serial('/dev/ttyS0', 9600, timeout = 1)

conn = pymysql.connect("localhost", "root", "", "testdb")
cur = conn.cursor()

sleeptime = 0
notify = 1
dic = {'AWX': None, 'AWY':None, 'AWZ':None}
s = ["l","i","o","s","r", "p","d", "w"];
index = 7

def insertData():
	print("ready to insert")
	insert_sql = "insert into windowAcc(AWX, AWY, AWZ) VALUES ('%f', '%f', '%f')" %\
	(dic['AWX'], dic['AWY'], dic['AWZ'])
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
				#door
			if data[1] == 'W':
				if accdataformate(data) == 1:
					try:
						i1 = data.find(',',1)
						x = float(data[2: i1])
						i2 = data.find(',',i1 + 1)
						y = float(data[i1 + 1: i2])
						z = float(data[i2 + 1:endindex])
						print("window is x: %.2f, y: %.2f, z: %.2f" % (x, y, z));
						dic['AWX'] = x
						dic['AWY'] = y
						dic['AWZ'] = z
						insertData()
						ser.write(s[index].encode("UTF-8"))
						continue
					except ValueError:
						print("WINDOW data convert error")
						ser.write(s[index].encode("UTF-8"))
						continue
				else:
					print("WINDOW ACC data lost")
					ser.write(s[index].encode("UTF-8"))
					continue
			else:
				print("WINDOW ACC data error")
				ser.write(s[index].encode("UTF-8"))
				continue
		except KeyboardInterrupt:
			print("Paused")
			inp =input('continue? (y/n)')
			if inp == 'y':
				index = 7
				continue
			elif inp == 'n':
				sys.exit(0)
			else:
				raise Exception('Invalid input')

	cur.close()
	conn.close()
