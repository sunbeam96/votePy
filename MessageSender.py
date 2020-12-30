import zmq
import sys
import logging


class MessageSender:
    def __init__(self, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % port)

    def sendMessage(self, messageData):
        logging.info("Sending message")
        self.socket.send("%d" % (messageData))