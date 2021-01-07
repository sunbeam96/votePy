import sys
import zmq
import socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread

class NewHostHandler(QObject):
    finished = pyqtSignal()
    newHost = pyqtSignal(str)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:6968")

    def __init__(self):
        super(NewHostHandler, self).__init__()

    def stopReceiver(self):
        print("Stopping receiver on new hosts handler")
        self.running = False
        self.socket.close()

    def runServer(self):
        self.running = True

        print("Running receiver")
        while self.running:
            message = self.socket.recv_string()
            print("Received info about new host: ", message)
            self.newHost.emit(message)
            self.socket.send("Received registration message")
        self.finished.emit()
