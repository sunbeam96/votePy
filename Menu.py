from PyQt5.QtWidgets import (QVBoxLayout, QListWidget,
    QPushButton, QGroupBox, QGridLayout, QMainWindow, QMessageBox,
    QAction, QLabel, QListView, QWidget)
from PyQt5.QtCore import QStringListModel, QObject, pyqtSignal, QThread
from PeerDetector import PeerDetector

class HostFinder(QObject):
    finished = pyqtSignal()
    availableHosts = []

    def run(self):
        detector = PeerDetector()
        self.availableHosts = detector.getHostsInLocalNetwork()
        self.finished.emit()

class Menu(QMainWindow):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)

        self.availableHosts = []
        
        self.showLoadingBox()
        self.setupMenu()
        hostFinder = self.createHostFinderThread()
        hostFinder.run()

    def updateAvailableHosts(self, availableHosts):
        self.availableHosts = availableHosts

    def createHostFinderThread(self):
        hostFinderObject = HostFinder()
        hostFinderThread = QThread()
        hostFinderObject.moveToThread(hostFinderThread)
        hostFinderThread.started.connect(hostFinderObject.run)
        hostFinderObject.finished.connect(lambda: self.updateAvailableHosts(hostFinderObject.availableHosts))
        hostFinderObject.finished.connect(hostFinderThread.quit)
        hostFinderObject.finished.connect(hostFinderObject.deleteLater)
        hostFinderThread.finished.connect(hostFinderThread.deleteLater)
        return hostFinderThread

    def setupMenu(self):
        self.createVotingList()
        self.createActionList()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.leftBox, 0, 0)
        mainLayout.addWidget(self.rightBox, 0, 1)
        self.centralWidget.setLayout(mainLayout)

        self.setWindowTitle("votePy")

    def showNoAvailableHostsBox(self):
        box = QMessageBox()
        box.setWindowTitle("Info")
        box.setText("No hosts are currently available or search is still pending.")
        box.exec_()

    def showAvailableHosts(self):
        if not self.availableHosts:
            self.showNoAvailableHostsBox()
            return
        self.hostsView = QListView()
        model = QStringListModel(self.availableHosts)
        self.hostsView.setModel(model)
        self.hostsView.show()

    def findAvailableHosts(self):
        detector = PeerDetector()
        self.availableHosts = detector.getHostsInLocalNetwork()

    def createVotingList(self):
        self.leftBox = QGroupBox("Ongoing votings")
        listWidget = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(listWidget)
        layout.addStretch(1)
        self.leftBox.setLayout(layout)

    def showLoadingBox(self):
        box = QMessageBox()
        box.setWindowTitle("Starting votePy")
        box.setText("Searching for available hosts may take a while.\nPlease wait.")
        box.exec_()


    def showAboutBox(self):
        box = QMessageBox()
        box.setWindowTitle("About votePy")
        box.setText("votePy by qba.lukaszczyk")
        box.exec_()

    def createActionList(self):
        self.rightBox = QGroupBox("Actions")

        newVoteButton = QPushButton("New voting")
        newVoteButton.setDefault(True)

        showParticipantsButton = QPushButton("Show participants")
        showParticipantsButton.clicked.connect(self.showAvailableHosts)

        aboutButton = QPushButton("About")
        aboutButton.clicked.connect(self.showAboutBox)

        detector = PeerDetector()
        ipLabel = QLabel("My host IP address: %s" % (detector.getLocalhostAddress()))
        layout = QVBoxLayout()
        layout.addWidget(newVoteButton)
        layout.addWidget(showParticipantsButton)
        layout.addWidget(aboutButton)
        layout.addWidget(ipLabel)
        layout.addStretch(1)
        self.rightBox.setLayout(layout)
