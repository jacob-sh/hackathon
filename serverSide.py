from socket import *
from struct import *
from random import *
import time
import threading
def groupNames(lst) :
    names = ''
    for tpl in lst :
        names += tpl[0]+'\n'
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
        while True:
            try:
                connectionSocket, addr = serverSocket.accept()
                clientName = connectionSocket.recv(2048)
                connectionSocket.setblocking(False)
                clientList.append((clientName.decode(), connectionSocket))
            except:
                break
        group1 = list()
        group2 = list()
        j = len(clientList)
        while j > 0 :
            if(j % 2 == 1) :
                group1.append(clientList.pop(randrange(j)))
            else :
                group2.append(clientList.pop(randrange(j)))
            j =- 1
        gameStartMsg = 'Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n' + groupNames(group1) + 'Group2:\n==\n' + groupNames(group2)+ '\nStart pressing keys on your keyboard as fast as you can!!\n'
        scoreList1 = list()
        scoreList2 = list()
        endMsgList = list()
        for tpl in group1 :
            threading.Thread(target = gaming, args = (tpl[0], tpl[1], scoreList1, gameStartMsg, endMsgList)).start()
        for tpl in group2 :
            threading.Thread(target = gaming, args = (tpl[0], tpl[1], scoreList2, gameStartMsg, endMsgList)).start()
        while (len(scoreList1) < len(group1)) | (len(scoreList2) < len(group2)):
            time.sleep(1)
        sum1 = 0
        sum2 = 0
        for result in scoreList1 :
            sum1 += result
        for result in scoreList2 :
            sum2 += result
        if(sum1 > sum2):
            winnerInfo = ('Group1' , groupNames(group1))
        else:
            winnerInfo = ('Group2' , groupNames(group2))
        endMsgList.append('Game over!\nGroup 1 typed in ' + str(sum1) + ' characters. Group 2 typed in ' + str(sum2) + ' characters.\n' + winnerInfo[0] + ' wins!\n\nCongratulations to the winners:\n==\n' + winnerInfo[1])
        print ('Game over, sending out offer requests...')

#gaming
def gaming (name, sock, scoreList, startMsg, endMsg) :
    sock.send(startMsg.encode())
    lst = list()
    timeout = time.time() + 10
    while time.time() < timeout :
        try:
            sentChar = sock.recv(1024)
            lst.append(sentChar.decode())
        except:
            continue
    scoreList.append(len(lst))
    while len(endMsg) == 0 :
        time.sleep(1)
    sock.send(endMsg[0].encode())
    sock.close()
        
sendingThread = threading.Thread(target = sendBroadcast, args = ())
sendingThread.start()
