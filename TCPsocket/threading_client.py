import socket, threading

LOCALHOST = "127.0.0.1"
PORT = 2500

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #주소 재사용
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")


class ClientThread(threading.Thread): #자식 클래스
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self) #부모 클래스 초기화 함수 실행
        self.csocket = clientsocket #인스턴스 변수 정의
        print ("New connection added: ", clientAddress)

    def run(self): #객체가 생성되면 자동실행 함수. 데이터를 수신하여 출력
        print ("Connection from : ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg=='quit': #'quit'가 수신되면 종료
              break
            print ("from client", msg)
            self.csocket.send(bytes(msg,'UTF-8'))
        print ("Client at ", clientAddress , " disconnected...")

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock) #서브 스레드를 생성하고 시작(run() 호출)
    newthread.start()


