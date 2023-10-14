import cv2
import socket
import threading
import tkinter as tk
from ui import VideoChatUI  # VideoChatUI는 사용자 정의 모듈로 UI를 관리하는 역할을 합니다.

class VideoChatServer:
    def __init__(self):
        # VideoChatUI 인스턴스 초기화
        self.ui = VideoChatUI(tk.Tk(), "Video chatting server")
        self.ui.on_send_message = self.send_message_to_clients
        self.clients = []

        # 웹캠 초기화
        self.cap = cv2.VideoCapture(0)

        # 소켓 초기화
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 8080))  # 서버는 8080 포트를 사용
        self.server_socket.listen(5)

        # 웹캠 영상 전송 스레드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

        # 클라이언트 연결을 처리하는 스레드 시작
        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # 서버 GUI 시작
        tk.mainloop()

    def show_frame(self, frame):
        self.ui.show_frame(frame)

    def send_message_to_clients(self, message):
        # 모든 클라이언트에게 메시지 전송
        for client in self.clients:
            client.send(message.encode())
        # 서버 UI에도 메시지 표시
        self.ui.receive_message(": " + message)

    def send_webcam(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            # BGR에서 RGB로 변환
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            encoded_frame = encoded_frame[1].tobytes()
            for client in self.clients:
                try:
                    client.send(encoded_frame)
                except:
                    self.clients.remove(client)
            self.show_frame(frame)

    def receive_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"New client connected: {client_address}")

            # 클라이언트로부터 메시지 수신 및 브로드캐스트
            while True:
                try:
                    message = client_socket.recv(8080).decode()
                    if not message:
                        break
                    print(f"Received message from {client_address}: {message}")
                    self.send_message_to_clients(message)
                except:
                    pass

if __name__ == "__main__":
    server = VideoChatServer()

