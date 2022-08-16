import datetime
import socket
import threading
import pickle

AllSockets = []


def sendingTwoWay(sockets):
    while True:
        message = input("Enter your message: ")
        for c in sockets:
            c.sendall(message.encode())


def recievingTwoWay(sockets):
    while True:
        for c in sockets:
            message = c.recv(1024).decode()
            print(message)


def recieve(c, addr, listOfAdresses):
    port = c.recv(1024).decode()
    if port not in listOfAdresses:
        listOfAdresses.append(port)
    print("List of addresses: ", listOfAdresses)
    AllSockets.append(c)
    send2 = threading.Thread(target=sendingTwoWay, args=(AllSockets,))
    send2.start()
    while True:
        message = c.recv(1024).decode()
        if message != "":
            print(message)
        else:
            print("Connection closed with: ", addr)
            c.close()
            break


def send(connectingPort, myPort):
    print("creating new socket")
    connectionSocket = socket.socket()
    print("Connecting socket created")
    connectionSocket.connect(("", connectingPort))
    connectionSocket.sendall((str(myPort)).encode())

    if connectionSocket not in AllSockets:
        AllSockets.append(connectionSocket)

    recieving2 = threading.Thread(target=recievingTwoWay, args=(AllSockets,))
    recieving2.start()
    while True:
        print("Allo ", str(len(AllSockets)))
        message = input("Enter your message: ")
        for s in AllSockets:
            s.sendall(message.encode())


messages = []

s = socket.socket()
print("Socket succesfully created")

port = int(input("Enter the port you want: "))

s.bind(("", port))
print(f"socket binded to port{port}")
s.listen(5)
print("Socket is listening")
listOfThreads = [None] * 5
i = 0
listOfAddresses = []
listOfAddresses.append(str(port))


connectingPort = input("Enter the port you want to connect With: ")
if connectingPort:
    listOfAddresses.append(str(connectingPort))
    print(listOfAddresses)
    connectionThread = threading.Thread(
        target=send, args=(int(connectingPort), int(port))
    )
    connectionThread.start()


while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    listOfThreads[i] = threading.Thread(target=recieve, args=(c, addr, listOfAddresses))
    listOfThreads[i].start()
    i += 1
