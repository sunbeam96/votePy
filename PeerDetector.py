import socket

class PeerDetector:
    def __init__(self):
        self.localhostIp = ""

    def getLocalhostAddress(self):
        hostname = socket.gethostname()
        ipAddr = socket.gethostbyname(hostname)
        return ipAddr