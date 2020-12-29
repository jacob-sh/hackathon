from socket import *
from struct import *
#import getch   #LINUX
import msvcrt   #WINDOWS
import time

# color escape codes:
# Black: \u001b[30m
# Red: \u001b[31m
# Green: \u001b[32m
# Yellow: \u001b[33m
# Blue: \u001b[34m
# Magenta: \u001b[35m
# Cyan: \u001b[36m
# White: \u001b[37m
# Reset: \u001b[0m


while True:
    print ('Client started, listening for offer requests')
    serverPort = 0
    clientBroadcast = socket(AF_INET, SOCK_DGRAM)
    #clientBroadcast.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)    #LINUX
    clientBroadcast.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientBroadcast.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    clientBroadcast.bind(("", 13117))
    data, serverName = clientBroadcast.recvfrom(1024)
    try:
        unpackedData = unpack('!IBH', data)
    except:
        unpackedData = (0, 0, 0)
    if ((unpackedData[0] != 0xfeedbeef) | (unpackedData[1] != 0x02)) :
        #return to more broadcast
        clientBroadcast.close()
    else :
        serverPort = unpackedData[2]
        print("Received offer from %s, attemting to connect..."%serverName[0])
        #try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName[0], serverPort))
        teamName = 'the most pogged team'
        clientSocket.send(teamName.encode())
        gameStartMsg = clientSocket.recv(2048).decode()
        print (gameStartMsg)
        timeout = time.time() + 10
        while time.time() < timeout :
            c = msvcrt.getch()                  #WINDOWS
            # c = getch.getch()                 #LINUX
            if time.time() < timeout :
                clientSocket.send(c)            #WINDOWS
                # clientSocket.send(c.encode()) #LINUX

        endMsg = clientSocket.recv(2048).decode()
        print ("%s"%endMsg)
        clientSocket.close()
        clientBroadcast.close()
        print('Server disconnected, listening for offer requests...')
        #except:
            #print("An exception occurred")
        


