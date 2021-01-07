import socket
import nmap

class PeerDetector:
    def getLocalhostAddress(self):
        hostname = socket.gethostname()
        ipAddr = socket.gethostbyname(hostname)
        print("Got localhost %s address of %s" % (hostname, ipAddr))
        return ipAddr

    def getHostsInLocalNetwork(self):
        nmapInstance = nmap.PortScanner()
        print("Running scan")
        nmapInstance.scan(hosts='%s/24' % (self.getLocalhostAddress()), arguments='-sn')
        print("Scanning hosts in local network done")
        return nmapInstance.all_hosts()