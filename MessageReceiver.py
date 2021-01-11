import sys
import zmq
import socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from Voting import Voting
    
class MessageReceiver(QObject):
    finished = pyqtSignal()
    updatedHosts = pyqtSignal(list)
    votingUpdate = pyqtSignal(Voting)
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
            self.socket.connect("tcp://%s:%s" % (senderAddress, port))
            print("Connection to tcp://%s:%s established" % (senderAddress, port))
        except:
            self.unavailableHosts.append(senderAddress)
            print("Error occured when connecting to tcp://%s:%s. Removing from available hosts." % (senderAddress, port))

    def stopReceiver(self):
        print("Stopping receiver and closing socket of message receiver")
        self.running = False
        self.socket.close()

    def handleVotingMsg(self, messageData):
        splitMsg = messageData.split(";")
        votingName = ""
        voteOptions = {}
        for element in splitMsg:
            if not element:
                continue
            processedKey = ""
            if splitMsg.index(element) == 0:
                continue
            elif splitMsg.index(element) == 1:
                votingName = element
            elif "_" in element:
                key = element.replace("_", "")
                voteOptions[key] = "0"
                processedKey = key
            else:
                voteOptions[processedKey] = element
        voting = Voting()
        voting.votingName = votingName
        voting.votes = voteOptions
        self.votingUpdate.emit(voting)

    def runReceiver(self):
        self.running = True

        self.connectToAvailableHosts(6969)

        print("Running receiver")
        while self.running:
            message = self.socket.recv_string()
            self.handleVotingMsg(message)
            print("Received message with content: %s" % message)
