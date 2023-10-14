import socket
import threading

# 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 2500))
sock.listen(1)
connections = [] # 서버와 연결된 클라이언트 목록

# 데이터를 수신하고 처리하는 함수

def handler(c, a):
    global connections  # 전역 변수. 서버와 연결된 클라이언트 목록 저장
    while True:
        data = c.recv(2014)
        for connection in connections:  # 모든 클라이언트에게 전송
            connection.send(bytes(data))
        if not data:  # 데이터가 없으면 목록에서 삭제
            connections.remove(c)
            c.close()
            break


# 서브 스레드의 생성과 실행
while True:
    c, a = sock.accept()
    cThread = threading.Thread(target=handler, args=(c,a))  # 서브 스레드 생성
    cThread.daemon = True
    cThread.start()  # 서브 스레드 실행
    connections.append(c)  # 새로운 클라이언트를 목록에 추가
    print(connections)