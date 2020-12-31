from socket import *
from struct import *
from scapy.arch import get_if_addr
import time
import sys
import select
import tty
import termios

def disconnectClient(sock):
    print('Server disconnected, timeout reached - listening for offer requests...')
    sock.close()

def sendCharsToServer(sock):
    timeout = time.time() + 10
    originalAttributes = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        while time.time() < timeout :
            if (select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])) :
                sock.sendall(sys.stdin.read(1).encode())
        return True
    except:
        return False
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, originalAttributes)

def openSocket(socktype, proto, broadcast):
    sock = socket(AF_INET, socktype, proto)
    sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, broadcast) #enable broadcasting mode for udp packet
    return sock

# main loop for client
while True:
    print ('Client started, listening for offer requests')
    
    # start udp socket and begin listening
    clientBroadcast = openSocket(SOCK_DGRAM, IPPROTO_UDP, 1)
    clientBroadcast.bind(("", 13117))
    data, serverName = clientBroadcast.recvfrom(1024)
    clientBroadcast.close()
    
    # unpack received data
    try:
        unpackedData = unpack('!IBH', data)
    except:
        unpackedData = (0, 0, 0)
    if ((unpackedData[0] != 0xfeedbeef) | (unpackedData[1] != 0x02)) :
        # incorrect udp packet format, go back to listening
        continue
    else:
        serverPort = unpackedData[2]
        print("Received offer from %s, attempting to connect..."%serverName[0])
        
        # start tcp socket
        try:
            clientSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            clientSocket.connect((serverName[0], serverPort))
            clientSocket.settimeout(15.0)
            teamName = 'THE MOST POGGED TEAM'
            
            #send team name
            clientSocket.sendall(teamName.encode())
            
            # print starting message
            gameStartMsg = clientSocket.recv(2048).decode()
            print (gameStartMsg)
        except:
            disconnectClient(clientSocket)
            continue
        
        # begin sending characters
        clientSocket.settimeout(2.0)
        if (sendCharsToServer(clientSocket)):
            try:
                # print end message
                endMsg = clientSocket.recv(2048).decode()
                print ("%s"%endMsg)
                clientSocket.close()
                print('Server disconnected, listening for offer requests...')
            except:
                disconnectClient(clientSocket)
        else:
            disconnectClient(clientSocket)