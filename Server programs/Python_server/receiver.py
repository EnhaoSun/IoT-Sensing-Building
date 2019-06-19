import serial
import pymysql
import time
import sys

ser = serial.Serial('/dev/ttyS0', 9600, timeout = 1)

conn = pymysql.connect("localhost", "root", "", "testdb")
cur = conn.cursor()

sleeptime = 0
notify = 1
dic = {'LUX': None, 'TEMPIN': None, 'TEMPWIN': None, 'SONARIN': None, 'SONAROUT':None, 'RCWL':None, 'PRESSURE': None, 'ADX': None, 'ADY': None, 'ADZ': None, 'AWX': None, 'AWY': None, 'AWZ': None}
s = ["l","i","o","s","r", "p","d", "w"];
index = 0

def insertData():
	print("ready to insert")
	insert_sql = "insert into SensorData(LUX, TEMPERATUREIN, TEMPERATUREWIN, SONARIN, SONAROUT, RCWL, PRESSURE, ADX, ADY, ADZ, AWX, AWY, AWZ) VALUES ('%d', '%f', '%f', '%d', '%d', '%d', '%f', '%f', '%f', '%f', '%f', '%f', '%f' )" %\
	(dic['LUX'], dic['TEMPIN'], dic['TEMPWIN'], dic['SONARIN'], dic['SONAROUT'], dic['RCWL'], dic['PRESSURE'], dic['ADX'], dic['ADY'], dic['ADZ'], dic['AWX'], dic['AWY'], dic['AWZ'])
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
	
			if index == 0:
				#insert LUX
				if data[1] == 'L':
					try:
						if endindex - 1 == 2:
							print("LUX is %d" % int(data[2]))
							dic['LUX'] = int(data[2])
						else:
							print("LUX is %d" % int(data[2:endindex]))
							dic['LUX'] = int(data[2:endindex])
						index = index + 1
						ser.write(s[index].encode("UTF-8"))
						continue
					except ValueError:
						print("LUX data invalid")
						ser.write(s[index].encode("UTF-8"))
						continue
				else:
					print("LUX data error")
					ser.write(s[index].encode("UTF-8"))
					continue
			elif index == 1:
				if data[1] == 'T':
					try:
						print("TEMPIN is %.2f" % float(data[2:endindex]))
						dic['TEMPIN'] = float(data[2:endindex])
						index = index + 1
						ser.write(s[index].encode("UTF-8"))
						continue
					except ValueError:
						print("TEMPIN data invalid")
						ser.write(s[index].encode("UTF-8"))
						continue
				else:
					print("TEMP data error")
					ser.write(s[index].encode("UTF-8"))
					continue
			elif index == 2:
				if data[1] == 'T':
					try:
						print("TEMPWIN is %.2f" % float(data[2:endindex]))
						dic['TEMPWIN'] = float(data[2:endindex])
						index = index + 1
						ser.write(s[index].encode("UTF-8"))
						continue
					except ValueError:
						print("TEMPWIN data invalid")
						ser.write(s[index].encode("UTF-8"))
						continue
				else:
					print("TEMP data error")
					ser.write(s[index].encode("UTF-8"))
					continue
			elif index == 3:
				if data[1] == 'S':
					try:
						index_so = data.find(',', 1)
						si = data[2 : index_so]
						so = data[index_so+1 : endindex]
						print("Sonar in:%d,out:%d" % (int(si),int(so)));
						dic['SONARIN'] = int(si)
						dic['SONAROUT'] = int(so)
						index = index + 1
						ser.write(s[index].encode("UTF-8"))
						continue
					except ValueError:
						print("SONAR data invalid")
						ser.write(s[index].encode("UTF-8"))
						continue
				else:
					print("Sonar data error")
					ser.write(s[index].encode("UTF-8"))
					continue
			elif index == 4:
				if data[1] == 'R':
					try:
						print("movement is %d" % int(data[2]));
						dic['RCWL'] = int(data[2])
						index = index + 1
						ser.write(s[index].encode("UTF-8"))
						continue
					except ValueError:
						print("RCWL data invalid")
						ser.write(s[index].encode("UTF-8"))
						continue
				else:
					print("RCWL data error")
					ser.write(s[index].encode("UTF-8"))
					continue
			elif index == 5:
				if data[1] == 'P':
					try:
						print("Pressure is %.2f" % float(data[2: endindex]))
						dic['PRESSURE'] = float(data[2:endindex])
						index = index + 1
						ser.write(s[index].encode("UTF-8"))
						continue
					except ValueError:
						print("PRESSURE data invalid")
						ser.write(s[index].encode("UTF-8"))
						continue
				else:
					print("PRESSURE data error")
					ser.write(s[index].encode("UTF-8"))
					continue
			elif index == 6:
				#door
				if data[1] == 'D':
					if accdataformate(data) == 1:
						try:
							i1 = data.find(',',1)
							x = float(data[2: i1])
							i2 = data.find(',',i1 + 1)
							y = float(data[i1 + 1: i2])
							z = float(data[i2 + 1:endindex])
							print("door is x: %.2f, y: %.2f, z: %.2f" % (x, y, z));
							dic['ADX'] = x
							dic['ADY'] = y
							dic['ADZ'] = z
							index = index + 1
							ser.write(s[index].encode("UTF-8"))
							continue
						except ValueError:
							print("DOOR data convert error")
							ser.write(s[index].encode("UTF-8"))
							continue
					else:
						print("DOOR ACC data lost")
						ser.write(s[index].encode("UTF-8"))
						continue
				else:
					print("DOOR ACC data error")
					ser.write(s[index].encode("UTF-8"))
					continue
			elif index == 7:
				#window
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
							print("--------")
							index = 0
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
			else:
				print("nothing")
				print(data)
				ser.write(s[index].encode("UTF-8"))
				#do nothing
		except KeyboardInterrupt:
			print("Paused")
			inp =input('continue? (y/n)')
			if inp == 'y':
				index = 0
				continue
			elif inp == 'n':
				sys.exit(0)
			else:
				raise Exception('Invalid input')

	cur.close()
	conn.close()
