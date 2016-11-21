import MDM
import GPIO

allowedNumbers = ['+972544939984','+972543042360']
myNumber = "+972544939984"

#sms sending function
def sendSMS(number,smstext):
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


#send SMS on boot
myText = "Garazhik alarm system is up and running"
sendSMS(myNumber,myText)

#initial door status check and sms
door1 = 0
door2 = 0
door2 = GPIO.getIOvalue(10)
if door2 == 0:
	myText = "Door status:closed"
elif door2 == 1:
	myText = "Door status:open"
else:
	myText = "Something went wrong on boot..."
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
		sendSMS(myNumber,myText)

	#reset the module or get the current door status with an sms massage
	#valid number verification
	MDM.send('AT+CMGF=1\r',1)
	resp = MDM.receive(1)
	MDM.send('AT+CMGL="REC UNREAD"\r',1)
	resp = MDM.receive(1)
	respErr = resp.find('REC UNREAD')
	if respErr > -1:
		veriNumber = resp[respErr+13:respErr+26]
		while veriNumber in allowedNumbers:
			# look for a valid command
			doReset = resp.find('reset')
			doStatus = resp.find('status')
			if doReset > -1:
				myText="Performing the reset now upon sms request from " + veriNumber +"."
				sendSMS(myNumber,myText)
				MOD.sleep(5)
				MDM.send('AT#REBOOT\r',2)
			if doStatus > -1:
				door2 = GPIO.getIOvalue(10)
				if door2 == 0:
					doorStatus = "Door status:closed"
				elif door2 == 1:
					doorStatus = "Door status:open"
				else:
					doorStatus = "I don't know..."
				myText="Status requested by " + veriNumber + ". " + doorStatus + "" 
		while veriNumber not in allowedNumbers:
			myText="You are not authorized, fuck you."	
		sendSMS(myNumber,myText)
	MDM.send('AT+CMGD=1,4\r',1)

#MOD.sleep(10)
