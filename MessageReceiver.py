import sys
import zmq
import logging
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

    def connectToAvailableHosts(self, hostsList, port):
        print("Connecting to available hosts")
        print("Current number of hosts to try:%s" % (len(self.availableHosts)))
        for host in hostsList:
            self.connectToHost(host, port)
        print("Removing unavailable hosts from hosts list")
        print("Current number of hosts:%s" % (len(self.availableHosts)))
        self.updatedHosts.emit(self.availableHosts)

    def connectToHost(self, senderAddress, port):
        logging.debug("Connection attempt ongoing")
        try:
            self.socket.connect((senderAddress, port))
            logging.info("Connection to tcp://%s:%s established" % (senderAddress, port))
        except:
            logging.error("Error occured when connecting to tcp://%s:%s. Removing from available hosts." % (senderAddress, port))
            print("Error occured when connecting to tcp://%s:%s. Removing from available hosts." % (senderAddress, port))
            self.availableHosts.remove(senderAddress)

    def stopReceiver(self):
        logging.info("Stopping receiver and closing socket on topic %s" % (self.topic))
        self.running = False
        self.socket.close()

    def runReceiver(self):
        self.running = True

        self.connectToAvailableHosts(self.availableHosts, 6969)

        print("Running receiver")
        while self.running:
            message = self.socket.recv_string()
            # handleMessage(message)
            # logger.info("Received message for %s" % topic)
