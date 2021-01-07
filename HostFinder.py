from PyQt5.QtCore import QStringListModel, QObject, pyqtSignal, QThread
from PeerDetector import PeerDetector

class HostFinder(QObject):
    finished = pyqtSignal()
    foundHosts = pyqtSignal(list)
    availableHosts = []
    print("Host Finder created")

    def run(self):
        print("Running run method and starting detector")
        self.detector = PeerDetector()
        self.availableHosts = self.detector.getHostsInLocalNetwork()
        self.foundHosts.emit(self.availableHosts)
        self.finished.emit()
