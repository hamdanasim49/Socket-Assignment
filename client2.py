import socket

s = socket.socket()
port = 12343
s.connect(("127.0.0.1", port))
print(s.recv(1024))

message = input("Enter your message: ")
s.sendall(message.encode())
s.close()
