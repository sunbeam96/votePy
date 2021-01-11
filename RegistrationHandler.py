import sys
import zmq
import socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PeerDetector import PeerDetector

class RegistrationHandler(QObject):
    finished = pyqtSignal()
    updatedHosts = pyqtSignal(list)
    hostsToNotify = []
    context = zmq.Context()
    hostsToRemove = []
    socket = context.socket(zmq.REQ)
    socket.RCVTIMEO = 3000

    def __init__(self):
        super(RegistrationHandler, self).__init__()

    def updateHostsToNotify(self, availableHosts):
        self.hostsToNotify = availableHosts

    def resetSocket(self):
        self.socket.close()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.RCVTIMEO = 3000
 
    def runRegistration(self):
        print("Running registration")
        peerDetector = PeerDetector()
        localhostIpAddress = peerDetector.getLocalhostAddress()
        print("Running registration on %s hosts" % len(self.hostsToNotify))
        if len(self.hostsToNotify) != 0:
            for host in self.hostsToNotify:
                if (host == localhostIpAddress):
                    self.hostsToRemove.append(host)
                    continue
                self.socket.connect("tcp://%s:6968" % host)
                print("Sending registration message")
                self.socket.send_string(localhostIpAddress)
                try:
                    message = self.socket.recv_string()
                    print("Received registration response: ", message)
                except:
                    print("Registration for host %s not possible" % host)
                    self.hostsToRemove.append(host)
                self.resetSocket()
        self.socket.close()
        for host in self.hostsToRemove:
            try:
                self.hostsToNotify.remove(host)
            except:
                pass
        self.updatedHosts.emit(self.hostsToNotify)
        self.finished.emit()
