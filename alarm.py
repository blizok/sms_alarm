import MDM
import GPIO

#sms sending function
def sendSMS( number, smstext):
	if number=="" or smstext=="" : return 0
	#text mode setup
	MDM.send('AT+CMGF=1\r',2)
	MDM.receive(20)
	#Send SMS intialization
	MDM.send('AT+CMGS="' + number + '"\r', 2)
	#"<" waiting
	res=0
	n=0
	while n<10:
		res = MDM.receive(10)
		if res.find(">")>-1:
			break
		else:
			n=n+1
	#sms text inserting and ctrl+z confirming
	MDM.send(smstext, 2)
	MDM.sendbyte(0x1A, 2)
	#"OK" confirmation waiting
	a=''
	while a=='':
		a = MDM.receive(20)
	return ( a.find('OK')!=-1 )

#initial door status check and sms
myText = "Alarm system is up and running"
myNumber = "+xxx"
sendSMS(myNumber,myText)

door2 = GPIO.getIOvalue(10)
if door2 == 0:
	myText = "Door status:closed"
elif door2 == 1:
	myText = "Door status:open"
else:
	myText = "Something went wrong on boot..."
myNumber = "+xxx"
sendSMS(myNumber,myText)
door1 = door2

#endless loop with door lookup
while (1):
	door2 = GPIO.getIOvalue(10)
	if door1 != door2:
		if door2 == 0:
			myText = "The door was closed"
		elif door2 == 1:
			myText = "The door was opened"
		else:
			myText = "Something went wrong..."
		door1 = door2
		myNumber = "+xxx"
		sendSMS(myNumber,myText)

