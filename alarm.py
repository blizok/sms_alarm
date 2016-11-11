import MOD
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
#gpio handlilng function
#def gpioRead():
#v0 = 0
v1 = 0
#myText = ""
#GPIO.setIOvalue(2,0)
#GPIO.setIOdir(2,1,0)
v1 = GPIO.getIOvalue(3)
myText = str(v1)
#was open
#if v0 == 0 and v1 == 1:
#	status = "the door was open"
#was closed
#elif v0 == 1 or v1 == 0:
#	status = "the door was closed"
#else :
#	status = "business as usual"
		



#sms details
myNumber = "+972544939984"
#myText = status 
#checking alarm status
#gpioRead()
#Sending SMS
sendSMS(myNumber,myText)
