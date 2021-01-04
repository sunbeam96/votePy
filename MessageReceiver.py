import sys
import zmq
import logging
import socket
from MessageHandler import MessageHandler

class MessageReceiver:
    def __init__(self, timeout):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.availableHosts = []

    def connectToHost(self, senderAddress, port):
        logging.debug("Connection attempt ongoing")
        try:
            self.socket.connect((senderAddress, port))
            logging.info("Connection to tcp://%s:%s established" % (senderAddress, port))
        except:
            logging.error("Error occured when connecting to tcp://%s:%s. Removing from available hosts." % (senderAddress, port))

    def stopReceiver(self):
        logging.info("Stopping receiver and closing socket on topic %s" % (self.topic))
        self.running = False
        self.socket.close()

    def runReceiver(self):
        self.running = True
        while self.running:
            message = self.socket.recv()
            # handleMessage(message)
            # logger.info("Received message for %s" % topic)
