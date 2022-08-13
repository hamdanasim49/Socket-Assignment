import socket
import json

s = socket.socket()
print("Socket succesfully created")
port = 12343
s.bind(("", port))
print(f"socket binded to port{port}")
s.listen(5)
print("Socket is listening")
while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    message = input("Enter your message: ")
    Message = {}
    Message["msg"] = message
    print(Message)
    json_object = json.dumps(Message)
    c.sendall(bytes(json_object, encoding="utf-8"))

    print(c.recv(1024))
    c.close()
