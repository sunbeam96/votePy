from MessageReceiver import MessageReceiver
from PeerDetector import PeerDetector

print("Message Receiver tests running")
receiver = MessageReceiver("vote", 5.0)
receiver.connectToHost("127.0.0.1", "80")
receiver.stopReceiver()

peerDetector = PeerDetector()
peerDetector.getHostsInLocalNetwork()