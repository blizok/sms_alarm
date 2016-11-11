import MOD
import MDM

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


#sms details
myNumber = "+972544939984"
myText = "mnjam"
#Sending SMS
sendSMS(myNumber,myText)
#	b=1
#else:
#	c=1
