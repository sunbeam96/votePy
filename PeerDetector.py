import socket
import logging
import nmap

class PeerDetector:
    def getLocalhostAddress(self):
        hostname = socket.gethostname()
        ipAddr = socket.gethostbyname(hostname)
        logging.info("Got localhost %s address of %s" % (hostname, ipAddr))
        return ipAddr

    def getHostsInLocalNetwork(self):
        nmapInstance = nmap.PortScanner()
        nmapInstance.scan(hosts='%s/24' % (self.getLocalhostAddress()), arguments='-sS')
        return nmapInstance.all_hosts()