import socket, sys, time, thread
from sql_connector import *
CONST_DELIM = '?'
CONST_PORT = 4001
CONST_SENDERPORT = 4002 #different for testing


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

#takes a string and creates a substring from index x1 to x2
def substring(str,x1,x2):
    sub = []
    for i in range(x1,x2):
        sub+=str[i]
    return ''.join(sub)

#Simple functions dealing with data extraction from the packets.
def getData1(data):
    for i in range (0, len(data)):
        if data[i] == CONST_DELIM:
            x = i
            break

    for y in range(x+1, len(data)):
        if data[y] == CONST_DELIM:
            q = y
            break
    s = substring(data, x+1, q)
    return s

def getData2(data):
    count  = 0
    for i in range (0, len(data)):
        if data[i] == CONST_DELIM:
            x = i
            count+=1
        if count == 2:
            break
    
    for y in range(x+1, len(data)):
        if data[y] == CONST_DELIM:
            q = y
            break
    s = substring(data, x+1, q)
    return s

def getData3(data):
    count  = 0
    for i in range (0, len(data)):
        if data[i] == CONST_DELIM:
            x = i
            count+=1
        if count == 3:
            break
    
    for y in range(x+1, len(data)):
        if data[y] == CONST_DELIM:
            q = y
            break
    s = substring(data, x+1, q)
    return s



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
            print("Return food item from database with hashcode")
            hashcode = getData1(data)
            server_address = (senderIP, CONST_SENDERPORT)
            
            #INDENT EVERYTHING IN THE IF/ELSE ONCE DATABASE FUNCTIONS ARE ADDED B/C PYTHON IS STUPID
            if(handler.get_item(hashcode) is not None):
                #get FoodItem name and lifetime from database, using dummy values for now...
		row = handler.get_item(hashcode)
                name = row[0]
                lifetime = row[1]

                #combine the data to send back to the controller.
            	newData = '1'
            	newData += CONST_DELIM
            	newData += name
            	newData += CONST_DELIM
            	newData += lifetime
            	newData += CONST_DELIM
            	sendData = bytearray(newData)
            
                #send the data back to the controller.

            	try:
                	s.sendto(sendData, server_address)
            	except socket.error:
                	print("Failed sending")
                        
            	print("Food item found and sent to controller")
        
            else:
            	sendResponse('2', senderIP, CONST_SENDERPORT)
            	print("Food item is not in the database, notifying controller")

        elif data[0] == '3':
            print("Update the database with the new item")
            name = getData1(data)
            lifetime = getData2(data)
            hashcode = getData3(data)
            handler.put_item(hashcode, name, lifetime)
        elif data[0] == '4':
            print("ping back to the sender")
            sendResponse('4', senderIP, CONST_SENDERPORT)
        else:
            print("Improper format")
    if not len(data):
        break
    print ("Received %s bytes from %s %s: " % (len(data), address, data ))

s.shutdown(1)
