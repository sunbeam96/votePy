import sys
import zmq
import logging
import socket
from MessageHandler import MessageHandler
from PyQt5.QtCore import QObject, pyqtSignal, QThread

class MessageReceiver(QObject):
    def __init__(self, timeout):
        self.finished = pyqtSignal()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.availableHosts = []

    def connectToAvailableHosts(self, hostsList, port):
        for host in hostsList:
            self.connectToHost(host, port)

    def connectToHost(self, senderAddress, port):
        logging.debug("Connection attempt ongoing")
        try:
            self.socket.connect((senderAddress, port))
            logging.info("Connection to tcp://%s:%s established" % (senderAddress, port))
        except:
            logging.error("Error occured when connecting to tcp://%s:%s. Removing from available hosts." % (senderAddress, port))
            self.availableHosts.remove(senderAddress)

    def stopReceiver(self):
        logging.info("Stopping receiver and closing socket on topic %s" % (self.topic))
        self.running = False
        self.socket.close()

    def runReceiver(self):
        self.running = True

        self.connectToAvailableHosts(self.availableHosts, 6969)
        while self.running:
            message = self.socket.recv()
            # handleMessage(message)
            # logger.info("Received message for %s" % topic)
