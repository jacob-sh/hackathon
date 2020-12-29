from socket import *
from struct import *
import getch
import time

while True:
    print ('Client started, listening for offer requests')
    serverPort = 0
    clientBroadcast = socket(AF_INET, SOCK_DGRAM)
    clientBroadcast.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    clientBroadcast.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientBroadcast.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    clientBroadcast.bind(("", 13117))
    data, serverName = clientBroadcast.recvfrom(1024)
    unpackedData = unpack('!IBH', data)
    if ((unpackedData[0] != 0xfeedbeef) | (unpackedData[1] != 0x02)) :
        #return to more broadcast
        clientBroadcast.close()
    else :
        serverPort = unpackedData[2]
        print("Received offer from %s, attemting to connect..."%serverName[0])
        #try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName[0], serverPort))
        teamName = 'very original team name'
        clientSocket.send(teamName.encode())
        gameStartMsg = clientSocket.recv(2048).decode()
        print (gameStartMsg)
        timeout = time.time() + 10
        while time.time() < timeout :
            c = getch.getch()
            if time.time() < timeout :
                clientSocket.send(c.encode())

        endMsg = clientSocket.recv(2048).decode()
        print ("%s"%endMsg)
        clientSocket.close()
        clientBroadcast.close()
        print('Server disconnected, listening for offer requests...')
        #except:
            #print("An exception occurred")
        


