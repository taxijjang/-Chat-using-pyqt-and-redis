import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import time
import socket
import redis

# from .redis_connect import redis_connect as rc

form_class = uic.loadUiType("chat.ui")[0]


### redis에 저장되어 있는 채팅목록 가지고 오기 ###
class Worker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.user_r = redis.Redis(host='3.34.134.147', port=6379, db=0)
        self.user_pub_sub = self.user_r.pubsub()
        self.user_pub_sub.subscribe('chat_server')

    def run(self):

        while True:
            message = self.user_pub_sub.get_message()

            if message:
                msg = str(message['data'])[1:]
                self.finished.emit(msg)
                print(msg)

            time.sleep(0.01)


class MyChat(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.worker = Worker()
        self.worker.finished.connect(self.get_text_brower)
        self.worker.start()

        self.my_ip_addr = socket.gethostbyname(socket.getfqdn())
        self.my_ip.setText(self.my_ip_addr)

        self.input_text.returnPressed.connect(self.append_text)

        self.user_r = redis.Redis(host='3.34.134.147', port=6379, db=0)
        self.user_r.pubsub()

    def append_text(self):
        text = self.input_text.text()
        message = str(self.my_ip_addr + " : " + text)
        #self.text_browser.append(message)
        self.user_r.publish('chat_server', message)
        self.input_text.clear()

    def send_redis(self):
        pass

    @pyqtSlot(str)
    def get_text_brower(self, data):
        self.text_browser.append(data)


if __name__ == "__main__":
    print(socket.gethostbyname(socket.getfqdn()))
    app = QApplication(sys.argv)

    myChat = MyChat()
    myChat.show()
    app.exec_()
