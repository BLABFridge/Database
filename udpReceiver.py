# Source: https://pymotw.com/2/socket/udp.html

import socket, sys, time, thread
CONST_DELIM = '_'
CONST_PORT = 4001
CONST_SENDERPORT = 4002 #different for testing


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', CONST_PORT)
s.bind(server_address)

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



def pingBack(errorCode, serverIP , port):
    send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = [100]
    data[0] = errorCode
    sendData = ''.join(data)
    server_address = (serverIP, port)
    send.sendto(sendData, server_address)
    
    return;

#TODO-----
def addToDataBase():
    return
def getFoodItem(hashcode):
    return
def isInDatabase(hashcode):
    return


#Main loop, print statements for testing.
#assumes that all datapackets are sent with no error
#TODO---- Add multithreading for sending so that the listener can remain open
#         Add appropriate waiting periods/timeouts
#         Integrate with database

while True:

    print ("Waiting to receive on port %d : press Ctrl-C or Ctrl-Break to stop " % CONST_PORT)

    data, address = s.recvfrom(100)

    if len(data) > 0:
        if data[0] == '0':
            print("Return food item from database with hashcode")
            print("%s" % getData1(data))
        elif data[0] == '1':
            print("Food item returned to the fridge")
            print("%s" % getData1(data))
            print("%s" % getData2(data))
        elif data[0] == '2':
            print("food item is not in the database")
            pingBack('2', 'localhost', CONST_SENDERPORT)
        elif data[0] == '3':
            print("Update the database with the new item")
            print("%s" % getData1(data))
            print("%s" % getData2(data))
            print("%s" % getData3(data))
        elif data[0] == '4':
            print("ping back to the sender")
            pingBack('4', 'localhost', CONST_SENDERPORT)
    if not len(data):
        break
    print ("Received %s bytes from %s %s: " % (len(data), address, data ))

s.shutdown(1)
