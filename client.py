# time_client.py
import socket

# 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("localhost", 5000)
sock.connect(address)
print("현재 시각: ", sock.recv(1024).decode())