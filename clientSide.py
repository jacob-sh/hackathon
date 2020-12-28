from socket import *
from struct import *
from pynput import keyboard
import time

def on_press(key, timeout):
    if (time.time() < timeout) :
        try:
            print('alphanumeric key {0} pressed'.format(key.char))       
        except AttributeError: 
            print('special key {0} pressed'.format(key))
    else :
        return False


def on_release(key, sock, timeout):
    if (time.time() < timeout) :
        try:
            sock.send(key.char.encode())
            print('alphanumeric key {0} pressed'.format(key.char))       
        except AttributeError: 
            print('special key {0} pressed'.format(key))
    else :
        return False

while True:
    print ('Client started, listening for offer requests')
    serverPort = 0
    clientBroadcast = socket(AF_INET, SOCK_DGRAM)
    clientBroadcast.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientBroadcast.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    clientBroadcast.bind(("", 13117))
    data, serverName = clientBroadcast.recvfrom(1024)
    unpackedData = unpack('qqq', data)
    print("%d" %unpackedData[2])

    if ((unpackedData[0] != 0xfeedbeef) | (unpackedData[1] != 0x2)) :
        #return to more broadcast
        break
    else :
        serverPort = unpackedData[2]
        print("%s" %serverName[0])
    print("Received offer from %s, attemting to connect..."%serverName[0])
    clientBroadcast.close()
    #try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName[0], serverPort))
    teamName = 'cool dudes'
    clientSocket.send(teamName.encode())
    gameStartMsg = clientSocket.recv(2048).decode()
    print (gameStartMsg)
    timeout = time.time() + 10
    listener = keyboard.Listener(on_press = lambda key: on_press(key, timeout = timeout), on_release = lambda key: on_release(key, sock = clientSocket, timeout = timeout))
    listener.start()
    time.sleep(10)
    listener.stop()

    endMsg = clientSocket.recv(2048).decode()
    print ("%s"%endMsg)
    clientSocket.close()
    print('Server disconnected, listening for offer requests...')
    #except:
        #print("An exception occurred")
    


