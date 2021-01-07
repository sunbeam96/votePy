import zmq
import sys

class MessageSender:
    def __init__(self, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)

    def sendMessage(self, messageData):
        print("Sending message")
        self.socket.send("%d" % (messageData))