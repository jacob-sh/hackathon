from socket import *
from struct import *
import time
import sys
import select
import tty
import termios

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

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
        print("Received offer from %s, attempting to connect..."%serverName[0])

        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName[0], serverPort))
        clientSocket.settimeout(20)
        teamName = 'THE MOST POGGED TEAM'
        clientSocket.send(teamName.encode())
        try:
            gameStartMsg = clientSocket.recv(2048).decode()
            print (gameStartMsg)
        except:
            print('Server disconnected, timeout reached - listening for offer requests...')
            clientSocket.close()
            clientBroadcast.close()
            continue

        timeout = time.time() + 10
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            while time.time() < timeout :
                if isData():
                    clientSocket.send(sys.stdin.read(1).encode())
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        try:
            endMsg = clientSocket.recv(2048).decode()
            print ("%s"%endMsg)
            clientSocket.close()
            clientBroadcast.close()
            print('Server disconnected, listening for offer requests...')
        except:
            print('Server disconnected, timeout reached - listening for offer requests...')
            clientSocket.close()
            clientBroadcast.close()
