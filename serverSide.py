from socket import *
from struct import *
from random import *
import copy
import time
import threading
def groupNames(lst, id) :
    names = ''
    i = 0
    while i < len(lst) :
        if (lst[i][2] == id) :
            names += lst[i][0]+'\n'
        i += 1
    return names

def sendBroadcast() :
    while True:
        serverPort = 12000
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.setblocking(False)
        serverSocket.bind(('', serverPort))
        serverSocket.listen(20)
        print ("The server is ready to receive")

        serverBroadcast = socket(AF_INET, SOCK_DGRAM)

        # Enable broadcasting mode
        serverBroadcast.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverBroadcast.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # Set a timeout so the socket does not block
        # indefinitely when trying to receive data.
        serverBroadcast.settimeout(0.2)
        print("Server started, listening on IP address 127.0.0.1")
        clientList = list()
        i = 0
        while i < 10 :
            serverBroadcast.sendto(pack('qqq', 0xfeedbeef, 0x2, 0x2ee0), ('<broadcast>', 13117))
            print("message sent!")
            i += 1
            time.sleep(1)
        temp = 0
        while True:
            try:
                connectionSocket, addr = serverSocket.accept()
                clientName = connectionSocket.recv(2048)
                connectionSocket.setblocking(False)
                if(temp % 2 == 0):
                    clientList.append((clientName.decode(), connectionSocket, 1))
                else:
                    clientList.append((clientName.decode(), connectionSocket, 2))
            except:
                break
            temp += 1
        gameStartMsg = 'Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n' + groupNames(clientList, 1) + 'Group 2:\n==\n' + groupNames(clientList, 2)+ '\nStart pressing keys on your keyboard as fast as you can!!\n'
        scoreList = list()
        endMsgList = list()
        for tpl in clientList :
            threading.Thread(target = gaming, args = (tpl[2], tpl[1], scoreList, gameStartMsg, endMsgList)).start()
        while (len(scoreList) < len(clientList)):
            time.sleep(1)
        sum1 = 0
        sum2 = 0
        for result in scoreList :
            if(result[1] == 1):
                sum1 += result[0]
            else:
                sum2 += result[0]
        if(sum1 > sum2):
            winnerInfo = ('Group 1' , groupNames(clientList, 1))
        else:
            winnerInfo = ('Group 2' , groupNames(clientList, 2))
        endMsgList.append('Game over!\nGroup 1 typed in ' + str(sum1) + ' characters. Group 2 typed in ' + str(sum2) + ' characters.\n' + winnerInfo[0] + ' wins!\n\nCongratulations to the winners:\n==\n' + winnerInfo[1])
        print ('Game over, sending out offer requests...')
        serverSocket.close()
        serverBroadcast.close()

#gaming
def gaming (id, sock, scoreList, startMsg, endMsg) :
    sock.send(startMsg.encode())
    lst = list()
    timeout = time.time() + 10
    while time.time() < timeout :
        try:
            sentChar = sock.recv(1024)
            lst.append(sentChar.decode())
        except:
            continue
    scoreList.append((len(lst), id))
    while len(endMsg) == 0 :
        time.sleep(1)
    sock.send(endMsg[0].encode())
    sock.close()
        
sendingThread = threading.Thread(target = sendBroadcast, args = ())
sendingThread.start()
