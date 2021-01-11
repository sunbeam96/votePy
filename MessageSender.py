import zmq
import sys
from Voting import Voting

class MessageSender:
    def __init__(self, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)

    def sendMessage(self, messageData):
        print("Sending message")
        self.socket.send_string("%s" % (messageData))

    def sendVotingMsg(self, voting):
        messageData = "votingUpdate;"
        messageData += voting.votingName
        messageData += ";"
        for option in voting.votes:
            messageData += option # adding key - voting option name
            messageData += "_;"
            messageData += str(voting.votes[option]) # adding value - number of votes for this option
            messageData += ";"
        self.sendMessage(messageData)

