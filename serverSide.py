from socket import *
from struct import *
from random import *
from scapy import *
import time
import threading

    #Black: \u001b[30m
    #Red: \u001b[31m
    #Green: \u001b[32m
    #Yellow: \u001b[33m
    #Bright Yellow: \u001b[33;1m
    #Blue: \u001b[34m
    #Bright Blue: \u001b[34;1m
    #Magenta: \u001b[35m
    #Cyan: \u001b[36m
    #White: \u001b[37m
    #Reset: \u001b[0m

def groupNames(lst, id) : # print group names
    names = ''
    i = 0
    while i < len(lst) :
        if (lst[i][2] == id) :
            names += lst[i][0]+'\n'
        i += 1
    return names

#gaming
def gaming (id, sock, scoreList, startMsg, endMsg) : # thread function
    lst = list() # list of every character sent by the player
    counter = 0
    try:
        # send starting message
        sock.sendall(startMsg.encode())
        timeout = time.time() + 10
        # receive characters
        while time.time() < timeout :
            try:
                sentChar = sock.recv(1024).decode()
                if(len(sentChar) == 1):
                    lst.append(sentChar)
            except:
                continue
        scoreList.append((len(lst), id)) # send the char count to the main thread
        try: # wait for the end message from the main thread
            while len(endMsg) == 0 :
                time.sleep(1)
            sock.sendall(endMsg[0].encode())
        except:
            sock.close()
    except:
        scoreList.append((len(lst), id))
    sock.close()
    return False

while True:
    # start server tcp reception socket
    serverPort = 2070
    serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.setblocking(False)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(20)
    print ("The server is ready to receive")
    # start server udp socket
    serverBroadcast = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    serverBroadcast.setblocking(False)

    # enable broadcasting mode
    serverBroadcast.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    serverBroadcast.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverBroadcast.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    print("Server started, listening on IP address %s" %gethostbyname(gethostname()))
    clientList = list()
    i = 0
    while i < 10 : # send out udp packets
        serverBroadcast.sendto(pack('!IBH', 0xfeedbeef, 0x02, 0x0816), ('<broadcast>', 13117))
        print("message sent!")
        i += 1
        time.sleep(1)
    serverBroadcast.close()
    temp = 0
    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
            connectionSocket.settimeout(0.2)
            try:
                clientName = connectionSocket.recv(2048) # get player name
                connectionSocket.setblocking(False)
            except:
                continue
            if(temp % 2 == 0):
                clientList.append((clientName.decode(), connectionSocket, 1))
            else:
                clientList.append((clientName.decode(), connectionSocket, 2))
        except:
            break
        temp += 1

    serverSocket.close()
    gameStartMsg = '\u001b[36;1mWelcome to Keyboard Spamming Battle Royale.\n\u001b[31;1mGroup 1:\n==\n' + groupNames(clientList, 1) + '\n\u001b[34;1mGroup 2:\n==\n' + groupNames(clientList, 2)+ '\n\u001b[32;1mStart pressing keys on your keyboard as fast as you can!!\u001b[0m\n'
    scoreList = list() # list of total chars collected per player
    endMsgList = list() # list that will contain the end message when its ready
    for tpl in clientList :
        threading.Thread(target = gaming, args = (tpl[2], tpl[1], scoreList, gameStartMsg, endMsgList)).start()
    while (len(scoreList) < len(clientList)):
        time.sleep(1)
    sum1 = 0 # team 1 score
    sum2 = 0 # team 2 score
    for result in scoreList :
        if(result[1] == 1):
            sum1 += result[0]
        else:
            sum2 += result[0]
    if(sum1 > sum2):
        winnerInfo = ('\u001b[31;1mGroup 1 wins!' , groupNames(clientList, 1))  
    elif(sum1 < sum2):
        winnerInfo = ('\u001b[34;1mGroup 2 wins!' , groupNames(clientList, 2))
    else:
        winnerInfo = ('\u001b[35mIt\'s a Tie!', 'Both groups won')
    endMsgList.append('Game over!\n\u001b[31;1mGroup 1 typed in ' + str(sum1) + ' characters. \u001b[34;1mGroup 2 typed in ' + str(sum2) + ' characters.\n' + winnerInfo[0] + '\n\n\u001b[33;1mCongratulations to the winners:\n==\n' + winnerInfo[1] +'\u001b[0m')
    print ('\u001b[0mGame over, sending out offer requests...')

