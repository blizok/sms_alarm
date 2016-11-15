import MOD
import MDM
import GPIO

import time

TIMEOUT_CMD = 20

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





def getIOvalue(GPIOnumber):
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT#GPIO=',0)
    MDM.mdmser.send(str(GPIOnumber),0)
    MDM.mdmser.send(',2\r',0)
    timer = time.time() + TIMEOUT_CMD
    resp = MDM.mdmser.read()
    while((resp.find('OK') == -1) and (resp.find('ERROR') == -1) and (time.time() < timer)):
      #time.sleep(0.1)
      resp = resp + MDM.mdmser.read()

    if resp.find('ERROR') != -1:
      result = -1
    else:
      commapos = resp.find(',')
      stat = resp[commapos+1]
      result = int(stat)
  else:
    print 'dummy getIOvalue(', GPIOnumber, ')'
    result = -1
  return result

v1 = getIOvalue(3)



#gpio handlilng function
#def gpioRead():
#v0 = 0
#myText = ""
#GPIO.setIOvalue(2,0)
#GPIO.setIOdir(2,1,0)
#v1 = GPIO.getIOvalue(3)
#myText = str(v1)
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
myText = str(v1)
#myText = status 
#checking alarm status
#gpioRead()
#Sending SMS
#sendSMS(myNumber,myText)

#while (1):
#	if(GPIO.getIOvalue(3)==0):
sendSMS(myNumber,myText)
