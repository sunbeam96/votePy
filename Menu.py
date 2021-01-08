from PyQt5.QtWidgets import (QVBoxLayout, QListWidget,
    QPushButton, QGroupBox, QGridLayout, QMainWindow, QMessageBox,
    QAction, QLabel, QListView, QWidget, QDialog)
from PyQt5.QtCore import QStringListModel, QObject, pyqtSignal, QThread
from PeerDetector import PeerDetector
from MessageReceiver import MessageReceiver
from HostFinder import HostFinder
from NewHostHandler import NewHostHandler
from RegistrationHandler import RegistrationHandler

class Menu(QMainWindow):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)

        self.availableHosts = []
        
        print("Show loading box")

        self.showLoadingBox()

        print("Setting up menu")
        self.setupMenu()

        print("Creating registration handler thread")
        self.registrationHandler = self.createRegistrationHandlerThread()

        print("Creating receiver service")
        self.receiverService = self.createReceiverService()

        print("Creating host finder thread")
        self.hostFinder = self.createHostFinderThread()

        print("Creating new host handler thread")
        self.newHostHandler = self.createNewHostHandlerThread()

        print("Running host finder")
        self.hostFinder.start()
        print("Running new host handler")
        self.newHostHandler.start()
        #print("Running receiver service")

    def updateHostsToNotify(self):
        self.registrationHandlerObject.updateHostsToNotify(self.availableHosts)

    def updateAvailableHosts(self, givenHosts):
        self.availableHosts = givenHosts
        try:
            self.availableHosts.remove(self.localhostAddress)
        except:
            pass
        self.messageReceiverObject.availableHosts = self.availableHosts

    def addAddressToAvailableHosts(self, address):
        self.availableHosts.append(address)

    def createRegistrationHandlerThread(self):
        self.registrationHandlerObject = RegistrationHandler()
        registrationHandlerThread = QThread()
        print("Moving registration handler to thread")
        self.registrationHandlerObject.moveToThread(registrationHandlerThread)

        print("Connecting signals for registration handler")
        registrationHandlerThread.started.connect(self.registrationHandlerObject.runRegistration)
        self.registrationHandlerObject.finished.connect(registrationHandlerThread.quit)
        self.registrationHandlerObject.finished.connect(self.registrationHandlerObject.deleteLater)
        registrationHandlerThread.finished.connect(registrationHandlerThread.deleteLater)
        return registrationHandlerThread

    def createReceiverService(self):
        self.messageReceiverObject = MessageReceiver()
        messageReceiverThread = QThread()
        print("Moving message receiver to thread")
        self.messageReceiverObject.moveToThread(messageReceiverThread)

        print("Connecting signals for message receiver")
        messageReceiverThread.started.connect(self.messageReceiverObject.runReceiver)
        self.messageReceiverObject.updatedHosts.connect(self.updateAvailableHosts)
        self.messageReceiverObject.updatedHosts.connect(self.updateHostsToNotify)
        self.messageReceiverObject.updatedHosts.connect(self.registrationHandler.start)
        self.messageReceiverObject.finished.connect(messageReceiverThread.quit)
        self.messageReceiverObject.finished.connect(self.messageReceiverObject.deleteLater)
        messageReceiverThread.finished.connect(messageReceiverThread.deleteLater)
        return messageReceiverThread

    def createNewHostHandlerThread(self):
        self.newHostHandlerObject = NewHostHandler()
        newHostHandlerThread = QThread()
        print("Moving to thread")
        self.newHostHandlerObject.moveToThread(newHostHandlerThread)

        print("Connecting signals")
        newHostHandlerThread.started.connect(self.newHostHandlerObject.runServer)
        self.newHostHandlerObject.newHost.connect(self.addAddressToAvailableHosts)
        self.newHostHandlerObject.finished.connect(newHostHandlerThread.quit)
        self.newHostHandlerObject.finished.connect(self.newHostHandlerObject.deleteLater)
        newHostHandlerThread.finished.connect(newHostHandlerThread.deleteLater)
        return newHostHandlerThread

    def createHostFinderThread(self):
        self.hostFinderObject = HostFinder()
        hostFinderThread = QThread()
        print("Moving to thread")
        self.hostFinderObject.moveToThread(hostFinderThread)

        print("Connecting signals")
        hostFinderThread.started.connect(self.hostFinderObject.run)
        self.hostFinderObject.foundHosts.connect(self.updateAvailableHosts)
        self.hostFinderObject.finished.connect(self.receiverService.start)
        self.hostFinderObject.finished.connect(hostFinderThread.quit)
        self.hostFinderObject.finished.connect(self.hostFinderObject.deleteLater)
        hostFinderThread.finished.connect(hostFinderThread.deleteLater)
        return hostFinderThread

    def setupMenu(self):
        print("Creating lists")
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

    def showNoHostsBox(self):
        box = QMessageBox()
        box.setWindowTitle("Action not available")
        box.setText("No hosts are available or search is pending.\nPlease wait.")
        box.exec_()

    def runNewVote(self):
        if len(self.availableHosts) == 0:
            self.showNoHostsBox()
            return
        self.newVoteDialog = QDialog()
        self.newVoteDialog.setWindowTitle("Create voting")

        createVotingButton = QPushButton("Create voting")
        #newVoteButton.clicked.connect(self.runNewVote)

        cancelNewVotingButton = QPushButton("Cancel")
        cancelNewVotingButton.setDefault(True)
        cancelNewVotingButton.clicked.connect(self.newVoteDialog.close)

        layout = QVBoxLayout()
        layout.addWidget(createVotingButton)
        layout.addWidget(cancelNewVotingButton)
        layout.setStretch(1, 1)
        self.newVoteDialog.setLayout(layout)

        self.newVoteDialog.exec_()

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
        newVoteButton.clicked.connect(self.runNewVote)

        showParticipantsButton = QPushButton("Show participants")
        showParticipantsButton.clicked.connect(self.showAvailableHosts)

        aboutButton = QPushButton("About")
        aboutButton.clicked.connect(self.showAboutBox)

        detector = PeerDetector()
        self.localhostAddress = detector.getLocalhostAddress()
        ipLabel = QLabel("My host IP address: %s" % (self.localhostAddress))
        layout = QVBoxLayout()
        layout.addWidget(newVoteButton)
        layout.addWidget(showParticipantsButton)
        layout.addWidget(aboutButton)
        layout.addWidget(ipLabel)
        layout.addStretch(1)
        self.rightBox.setLayout(layout)
