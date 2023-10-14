# time_client.py
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('', 5700)
s.bind(address)
s.listen(5)

client, addr = s.accept()

while True:
    print("Connection requested from", addr)
    if client:
        time.sleep(1)
        client.send(time.ctime(time.time()).encode())

        print("connnection requested from", addr)
        if client:
            time.sleep(1)
            client.send(time.ctime(time.time()).encode())


