import MOD
import MDM

#def checkNetwork():
#	MOD.sleep(20)
#	REC_TIME = 200
#	for _ in range(10):
#		MDM.send("AT+CREG?\r",0)
#		res = MDM.receive(REC_TIME)
#		if (res.find('0,1')!=-1): return 1
#		else: MOD.sleep(50)
#	return 0

def sendSMS( number, smstext):
	if number=="" or smstext=="" : return 0
	MDM.send('AT+CMGF=1\r',2)
	MDM.receive(20)
	a = MDM.send('AT+CMGS="' + number + '"\r', 2)
	res = MDM.receive(10)          
	a = MDM.send(smstext, 2)
	a = MDM.sendbyte(0x1A, 2)
	a=''
	while a=='':
		a = MDM.receive(20)
	return ( a.find('OK')!=-1 )

#print "Start"
#while not checkNetwork():
#	print "No network"
#	MOD.sleep(10)
#print "I find network"

myNumber = "+972544939984"
myText = "Hello world"
#print "Trying to send SMS"
if sendSMS(myNumber,myText):
	b=1
else:
	c=1
