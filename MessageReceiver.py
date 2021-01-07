import sys
import zmq
import socket
from MessageHandler import MessageHandler
from PyQt5.QtCore import QObject, pyqtSignal, QThread

class MessageReceiver(QObject):
    finished = pyqtSignal()
    updatedHosts = pyqtSignal(list)
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.subscribe("")

    def __init__(self):
        super(MessageReceiver, self).__init__()
        self.availableHosts = []
        self.unavailableHosts = []

    def connectToAvailableHosts(self, port):
        print("Connecting to available hosts")
        print("Current number of hosts to try:%s" % (len(self.availableHosts)))
        for host in self.availableHosts:
            self.connectToHost(host, port)
        print("Removing unavailable hosts from hosts list")
        for host in self.unavailableHosts:
            self.availableHosts.remove(host)
        print("Current number of hosts:%s" % (len(self.availableHosts)))
        self.updatedHosts.emit(self.availableHosts)

    def connectToHost(self, senderAddress, port):
        print("Connection attempt ongoing")
        try:
            self.socket.connect((senderAddress, port))
            print("Connection to tcp://%s:%s established" % (senderAddress, port))
        except:
            self.unavailableHosts.append(senderAddress)
            print("Error occured when connecting to tcp://%s:%s. Removing from available hosts." % (senderAddress, port))

    def stopReceiver(self):
        print("Stopping receiver and closing socket of message receiver")
        self.running = False
        self.socket.close()

    def runReceiver(self):
        self.running = True

        self.connectToAvailableHosts(6969)

        print("Running receiver")
        while self.running:
            message = self.socket.recv_string()
            # handleMessage(message)
            # logger.info("Received message for %s" % topic)
