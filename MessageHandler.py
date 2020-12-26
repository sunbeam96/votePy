import logging

class MessageHandler:
    def __init__(self):
        self.topics = []

    # def getMessageType(self, messageData):

    # def addTopic(self, topic):
        
    def handleMessage(self, message):
        topic, messagedata = message.split()
