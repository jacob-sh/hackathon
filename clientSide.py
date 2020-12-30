from socket import *
from struct import *
from scapy.arch import get_if_addr
import time
import sys
import select
import tty
import termios

def dataAvailable(): # checks if there is input in stdin
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

while True:
    print ('Client started, listening for offer requests')
    serverPort = 0
    
    # start udp socket and begin listening
    clientBroadcast = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    clientBroadcast.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    clientBroadcast.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientBroadcast.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    clientBroadcast.bind(("", 13117))
    data, serverName = clientBroadcast.recvfrom(1024)
    clientBroadcast.close()
    
    # unpack received data
    try:
        unpackedData = unpack('!IBH', data)
    except:
        unpackedData = (0, 0, 0)
    if ((unpackedData[0] != 0xfeedbeef) | (unpackedData[1] != 0x02)) :
        # not expected udp packet, go back to listening
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
            print('Server disconnected, timeout reached - listening for offer requests...')
            clientSocket.close()
            continue
        
        # begin sending characters
        clientSocket.settimeout(1.0)
        timeout = time.time() + 10
        originalAttributes = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            while time.time() < timeout :
                if dataAvailable():
                    clientSocket.sendall(sys.stdin.read(1).encode())
        except:
            print('Server disconnected, timeout reached - listening for offer requests...')
            clientSocket.close()
            continue
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, originalAttributes)
        
        # print end message
        try:
            clientSocket.settimeout(2.0)
            endMsg = clientSocket.recv(2048).decode()
            print ("%s"%endMsg)
            clientSocket.close()
            print('Server disconnected, listening for offer requests...')
        except:
            print('Server disconnected, timeout reached - listening for offer requests...')
            clientSocket.close()
