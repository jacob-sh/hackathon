from socket import *
from struct import *
from scapy.arch import get_if_addr
import time
import threading

#this is why we are "THE MOST POGGED TEAM"
poggy = """
⠄⠄⠄⠄⠄⠄⣀⣀⣀⣤⣶⣿⣿⣶⣶⣶⣤⣄⣠⣴⣶⣿⣿⣿⣿⣶⣦⣄⠄⠄
⠄⠄⣠⣴⣾⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦
⢠⠾⣋⣭⣄⡀⠄⠄⠈⠙⠻⣿⣿⡿⠛⠋⠉⠉⠉⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿
⡎⣾⡟⢻⣿⣷⠄⠄⠄⠄⠄⡼⣡⣾⣿⣿⣦⠄⠄⠄⠄⠄⠈⠛⢿⣿⣿⣿⣿⣿
⡇⢿⣷⣾⣿⠟⠄⠄⠄⠄⢰⠁⣿⣇⣸⣿⣿⠄⠄⠄⠄⠄⠄⠄⣠⣼⣿⣿⣿⣿
⢸⣦⣭⣭⣄⣤⣤⣤⣴⣶⣿⣧⡘⠻⠛⠛⠁⠄⠄⠄⠄⣀⣴⣿⣿⣿⣿⣿⣿⣿
⠄⢉⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢰⡿⠛⠛⠛⠛⠻⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠸⡇⠄⠄⢀⣀⣀⠄⠄⠄⠄⠄⠉⠉⠛⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠈⣆⠄⠄⢿⣿⣿⣿⣷⣶⣶⣤⣤⣀⣀⡀⠄⠄⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠄⣿⡀⠄⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⠄⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠄⣿⡇⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠄⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠄⣿⡇⠄⠠⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠄⠄⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠄⣿⠁⠄⠐⠛⠛⠛⠛⠉⠉⠉⠉⠄⠄⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⠄⠄⠻⣦⣀⣀⣀⣀⣀⣀⣤⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠄\n""" 

# color escape codes
green = '\u001b[32m'
bright_green = '\u001b[32;1m'
bright_red = '\u001b[31;1m'
bright_yellow = '\u001b[33;1m'
bright_blue = '\u001b[34;1m'
magenta = '\u001b[35m'
bright_cyan = '\u001b[36;1m'
reset_color = '\u001b[0m'

# each player gets an id corresponding to their group
group1_id = 1
group2_id = 2

def groupNames(clientList, groupId) : # print group names
    names = ''
    for i in range(len(clientList)) :
        if (clientList[i][2] == groupId) :
            names += clientList[i][0]+'\n'
    return names

def generateStartMsg(clientList):
    return green + poggy + bright_cyan + 'Welcome to Keyboard Spamming Battle Royale.\n' + bright_red + 'Group 1:\n==\n' + groupNames(clientList, group1_id) + '\n' + bright_blue + 'Group 2:\n==\n' + groupNames(clientList, group2_id) + '\n' + bright_green + 'Start pressing keys on your keyboard as fast as you can!!' + reset_color + '\n'

def openSocket(socktype, proto, broadcast):
    sock = socket(AF_INET, socktype, proto)
    sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, broadcast) # enable/disable broadcasting mode for udp packet
    sock.setblocking(False)
    return sock

def generateEndGameMsg(clientList, scoreList):
    # calculate final tally
    sum1 = 0 # team 1 score
    sum2 = 0 # team 2 score
    for result in scoreList :
        if(result[1] == 1):
            sum1 += result[0]
        else:
            sum2 += result[0]

    # declare winner and generate the end game message
    if(sum1 > sum2):
        winnerInfo = (bright_red + 'Group 1 wins!' , groupNames(clientList, group1_id))  
    elif(sum1 < sum2):
        winnerInfo = (bright_blue + 'Group 2 wins!' , groupNames(clientList, group2_id))
    else:
        winnerInfo = (magenta + 'It\'s a Tie!', 'Both groups won\n' +  groupNames(clientList, group1_id) + groupNames(clientList, group2_id))
    return 'Game over!\n'+ bright_red +'Group 1 typed in ' + str(sum1) + ' characters. ' + bright_blue + 'Group 2 typed in ' + str(sum2) + ' characters.\n' + winnerInfo[0] + '\n\n'+ bright_yellow + 'Congratulations to the winners:\n==\n' + winnerInfo[1] + reset_color

def sendUdpPackets (sock) :
    for i in range(10) : 
        sock.sendto(pack('!IBH', 0xfeedbeef, 0x02, 0x0816), ('<broadcast>', 13117))
        print("message sent!")
        time.sleep(1)
    return False
    
#gaming
def gaming (groupId, sock, scoreList, startMsg, endMsg) : # thread function
    inputlist = list() # list of every character sent by the player
    try:
        # send starting message
        sock.sendall(startMsg.encode())
        timeout = time.time() + 10

        # receive characters
        while time.time() < timeout :
            try:
                receivedChar = sock.recv(1024).decode()
                if(len(receivedChar) == 1):
                    inputlist.append(receivedChar)
            except:
                continue
        scoreList.append((len(inputlist), groupId)) # send the char count to the main thread
        
        # wait for the end message from the main thread
        try: 
            while len(endMsg) == 0 :
                time.sleep(1)
            sock.sendall(endMsg[0].encode())
        except:
            sock.close()
    except:
        scoreList.append((len(inputlist), groupId))
    sock.close()
    return False

# main loop for server
while True:
    # start server tcp reception socket
    serverPort = 2070
    serverSocket = openSocket(SOCK_STREAM, IPPROTO_TCP, 0)
    serverSocket.bind(('', serverPort))

    # begin listening on tcp socket
    serverSocket.listen(20)
    print ("The server is ready to receive")

    # start server udp socket
    serverBroadcast = openSocket(SOCK_DGRAM, IPPROTO_UDP, 1)
    print("Server started, listening on IP address %s" %get_if_addr('eth1'))
    
    # begin sending udp packets
    udpThread = threading.Thread(target = sendUdpPackets, args = (serverBroadcast,))
    udpThread.start()

    # accept all waiting players
    clientList = list()
    groupDistributor = 0
    timeout = time.time() + 10
    while time.time() < timeout:
        try:
            connectionSocket, addr = serverSocket.accept()
            connectionSocket.settimeout(0.2)
            try:
                clientName = connectionSocket.recv(2048) # get player name
                connectionSocket.setblocking(False)
            except:
                continue
            if(groupDistributor % 2 == 0): # assign players to their groups
                clientList.append((clientName.decode(), connectionSocket, group1_id)) 
            else:
                clientList.append((clientName.decode(), connectionSocket, group2_id))
        except:
            continue
        groupDistributor += 1
    
    # end client solicitation state
    udpThread.join()
    serverBroadcast.close()
    serverSocket.close()

    # begin game
    gameStartMsg = generateStartMsg(clientList)
    scoreList = list() # list of total chars collected per player
    endMsgList = list() # list that will contain the end message when its ready
    
    # begin player threads
    for tpl in clientList :
        threading.Thread(target = gaming, args = (tpl[2], tpl[1], scoreList, gameStartMsg, endMsgList)).start()
    
    # wait for all players to finish typing
    while (len(scoreList) < len(clientList)):
        time.sleep(1)

    endMsgList.append(generateEndGameMsg(clientList, scoreList))
    print (reset_color + 'Game over, sending out offer requests...')