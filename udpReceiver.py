import socket, sys, time, thread
from sql_connector import *
CONST_DELIM = '?'
CONST_PORT = 4001
CONST_SENDERPORT = 4002 #different for testing
CONST_HASHCODE_LENGTH = 10;


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Could not open socket")

server_address = ("", CONST_PORT)

try:
    s.bind(server_address)
except socket.error:
    print("Could not bind socket")

handler = db_hand();

#takes a string and returns the string equivalent of the hashcode.
def getHash(data, index):
    sub = []
    count = 0
    hashIndex = 0
    if(index == 1):
        for i in range(2,CONST_HASHCODE_LENGTH+2):
            sub+=data[i]
        return ''.join(sub)
    elif(index == 3):
        for z in range(0,len(data)):
            if(data[z] == '?'):
                count+=1
            if(count == 3):
                hashIndex = z
                break
        for i in range(z+1,CONST_HASHCODE_LENGTH+z+1):
            sub+=data[i]
        return ''.join(sub)

#takes a string and creates a substring from index x1 to x2
def substring(str,x1,x2):
    sub = []
    for i in range(x1,x2):
        sub+=str[i]
    return ''.join(sub)

#Simple functions dealing with data extraction from the packets.
def getData(data, index):
     x=data.split('?', 10)
     return x[index]


def sendResponse(errorCode, serverIP , port):
    #if errorCode == 0:

    data = [100]
    data[0] = errorCode
    sendData = ''.join(data)
    server_address = (serverIP, port)
    try:
        s.sendto(sendData, server_address)
    except socket.error:
        print("Failed sending")
    
    return;

#Main loop, print statements for testing.

while True:

    print ("Waiting to receive on port %d : press Ctrl-C or Ctrl-Break to stop " % CONST_PORT)
    #set to receive 100 bytes
	
    (data, address) = s.recvfrom(100)    
    
    senderIP, senderSocket = address

    if len(data) > 0:
        if data[0] == '0':
            hashcode = getHash(data, 1)
            server_address = (senderIP, senderSocket)
            row = handler.get_item(hashcode)
		
            #INDENT EVERYTHING IN THE IF/ELSE ONCE DATABASE FUNCTIONS ARE ADDED B/C PYTHON IS STUPID
            if(row is not None):
                #get FoodItem name and lifetime from database, using dummy values for now...
                name = row[0]
                lifetime = row[1]

                #combine the data to send back to the controller.
            	newData = '1'
            	newData += CONST_DELIM
            	newData += name
            	newData += CONST_DELIM
            	newData += str(lifetime)
            	newData += CONST_DELIM
            	sendData = bytearray(newData)
            
                #send the data back to the controller.

            	try:
                	s.sendto(sendData, server_address)
            	except socket.error:
                	print("Failed sending")
                        
            	print("Food item found and sent to controller")
        
            else:
            	sendResponse('2', senderIP, senderSocket)
            	print("Food item is not in the database, notifying controller")

        elif data[0] == '3':
            print("Update the database with the new item")
            name = getData(data,1)
            lifetime = getData(data,2)
            hashcode = getHash(data,3)
            handler.put_item(hashcode, name, lifetime)
        elif data[0] == '4':
            print("ping back to the sender")
            sendResponse('4', senderIP, senderSocket)
        else:
            print("Improper format")
    if not len(data):
        break
    print ("Received %s bytes from %s %s: " % (len(data), address, data ))

s.shutdown(1)
