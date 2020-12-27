import zmq
import sys
import logging


class MessageSender:
    def __init__(self, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)

    def sendMessage(self, topic, messageData):
        logging.info("Sending message of topic %s" % (topic))
        self.socket.send("%d %d" % (topic, messageData))