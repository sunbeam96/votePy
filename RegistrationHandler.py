import sys
import zmq
import socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PeerDetector import PeerDetector

class RegistrationHandler(QObject):
    finished = pyqtSignal()
    hostsToNotify = []
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    def __init__(self):
        super(RegistrationHandler, self).__init__()

    def updateHostsToNotify(self, availableHosts):
        self.hostsToNotify = availableHosts
 
    def runRegistration(self):
        print("Running registration")
        peerDetector = PeerDetector()
        localhostIpAddress = peerDetector.getLocalhostAddress()
        print("Running registration on %s hosts" % len(self.hostsToNotify))
        if len(self.hostsToNotify) != 0:
            for host in self.hostsToNotify:
                self.socket.connect("tcp://%s:6968" % host)
            print("Sending registration message")
            self.socket.send_string(localhostIpAddress)
            message = self.socket.recv_string()
            print("Received registration response: ", message)
        self.socket.close()
        self.finished.emit()
