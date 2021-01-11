from PyQt5.QtWidgets import (QVBoxLayout, QListWidget,
    QPushButton, QGroupBox, QGridLayout, QMainWindow, QMessageBox,
    QAction, QLabel, QListView, QWidget, QDialog, QLineEdit)
from PyQt5.QtCore import QStringListModel, QObject, pyqtSignal, QThread
from PeerDetector import PeerDetector
from MessageReceiver import MessageReceiver
from MessageSender import MessageSender
from HostFinder import HostFinder
from NewHostHandler import NewHostHandler
from RegistrationHandler import RegistrationHandler
from Voting import Voting

class Menu(QMainWindow):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)

        self.availableHosts = []
        self.ongoingVotings = []
        self.showLoadingBox()

        print("Setting up menu")
        self.setupMenu()

        print("Creating services")
        self.registrationHandler = self.createRegistrationHandlerThread()
        self.receiverService = self.createReceiverService()
        self.hostFinder = self.createHostFinderThread()
        self.newHostHandler = self.createNewHostHandlerThread()

        self.messageSender = MessageSender(6969)

        print("Running services")
        self.hostFinder.start()
        self.newHostHandler.start()

    def updateHostsToNotify(self):
        self.registrationHandlerObject.updateHostsToNotify(self.availableHosts)

    def updateVotings(self, updatedVoting):
        isNew = True
        for voting in self.ongoingVotings:
            if voting.votingName == updatedVoting.votingName:
                voting.votes = updatedVoting.votes
                isNew = False
        if isNew:
            self.ongoingVotings.append(updatedVoting)

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
        self.registrationHandlerObject.moveToThread(registrationHandlerThread)

        registrationHandlerThread.started.connect(self.registrationHandlerObject.runRegistration)
        self.registrationHandlerObject.finished.connect(registrationHandlerThread.quit)
        self.registrationHandlerObject.finished.connect(self.registrationHandlerObject.deleteLater)
        registrationHandlerThread.finished.connect(registrationHandlerThread.deleteLater)
        return registrationHandlerThread

    def createReceiverService(self):
        self.messageReceiverObject = MessageReceiver()
        messageReceiverThread = QThread()
        self.messageReceiverObject.moveToThread(messageReceiverThread)

        messageReceiverThread.started.connect(self.messageReceiverObject.runReceiver)
        self.messageReceiverObject.updatedHosts.connect(self.updateAvailableHosts)
        self.messageReceiverObject.updatedHosts.connect(self.updateHostsToNotify)
        self.messageReceiverObject.updatedHosts.connect(self.registrationHandler.start)
        self.messageReceiverObject.votingUpdate.connect(self.updateVotings)
        self.messageReceiverObject.finished.connect(messageReceiverThread.quit)
        self.messageReceiverObject.finished.connect(self.messageReceiverObject.deleteLater)
        messageReceiverThread.finished.connect(messageReceiverThread.deleteLater)
        return messageReceiverThread

    def createNewHostHandlerThread(self):
        self.newHostHandlerObject = NewHostHandler()
        newHostHandlerThread = QThread()
        self.newHostHandlerObject.moveToThread(newHostHandlerThread)

        newHostHandlerThread.started.connect(self.newHostHandlerObject.runServer)
        self.newHostHandlerObject.newHost.connect(self.addAddressToAvailableHosts)
        self.newHostHandlerObject.finished.connect(newHostHandlerThread.quit)
        self.newHostHandlerObject.finished.connect(self.newHostHandlerObject.deleteLater)
        newHostHandlerThread.finished.connect(newHostHandlerThread.deleteLater)
        return newHostHandlerThread

    def createHostFinderThread(self):
        self.hostFinderObject = HostFinder()
        hostFinderThread = QThread()
        self.hostFinderObject.moveToThread(hostFinderThread)

        hostFinderThread.started.connect(self.hostFinderObject.run)
        self.hostFinderObject.foundHosts.connect(self.updateAvailableHosts)
        self.hostFinderObject.finished.connect(self.receiverService.start)
        self.hostFinderObject.finished.connect(hostFinderThread.quit)
        self.hostFinderObject.finished.connect(self.hostFinderObject.deleteLater)
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

    def votingOptionChoosedAction(self):
        updatedVoting = Voting()
        selectedVotingName = self.votingListWidget.currentItem().text()
        selectedVotingOption = self.optionsList.currentItem().text()
        for ongoingVoting in self.ongoingVotings:
            if selectedVotingName == ongoingVoting.votingName:
                updatedVoting = ongoingVoting
        for option in updatedVoting.votes:
            if option == selectedVotingOption:
                votesNumber = int(updatedVoting.votes[option])
                votesNumber += 1
                updatedVoting.votes[option] = votesNumber
                updatedVoting.myVote = option
        self.updateVotings(updatedVoting)
        self.messageSender.sendVotingMsg(updatedVoting)

    def runVotingWindow(self, votingName):
        self.votingWindow = QDialog()
        self.votingWindow.setWindowTitle("Voting")

        self.optionsList = QListWidget()

        for ongoingVoting in self.ongoingVotings:
            if votingName == ongoingVoting.votingName:
                for option in ongoingVoting.votes:
                    self.optionsList.addItem(option)

        self.optionsList.itemDoubleClicked.connect(self.votingOptionChoosedAction)
        self.optionsList.itemDoubleClicked.connect(self.votingWindow.close)

        layout = QGridLayout()
        layout.addWidget(self.optionsList, 0, 0)
        self.votingWindow.setLayout(layout)
        self.votingWindow.exec_()

    def showVotingResults(self, votingName):
        self.resultsWindow = QDialog()
        self.resultsList = QListWidget()

        for ongoingVoting in self.ongoingVotings:
            if ongoingVoting.votingName == votingName:
                for option in ongoingVoting.votes:
                    self.resultsList.addItem("%s: %s" % (option, ongoingVoting.votes[option]))

        layout = QGridLayout()
        layout.addWidget(self.resultsList, 0, 0)
        self.resultsWindow.setLayout(layout)
        self.resultsWindow.exec_()

    def handleExistingVoting(self):
        selectedVotingName = self.votingListWidget.currentItem().text()
        for ongoingVoting in self.ongoingVotings:
            if selectedVotingName == ongoingVoting.votingName:
                if not ongoingVoting.myVote:
                    self.runVotingWindow(selectedVotingName)
                else:
                    self.showVotingResults(selectedVotingName)

    def updateVotingListWidget(self):
        self.votingListWidget.clear()
        for element in self.ongoingVotings:
            self.votingListWidget.addItem(element.votingName)

    def findAvailableHosts(self):
        detector = PeerDetector()
        self.availableHosts = detector.getHostsInLocalNetwork()

    def createVotingList(self):
        self.leftBox = QGroupBox("Ongoing votings")
        self.votingListWidget = QListWidget()
        self.votingListWidget.itemDoubleClicked.connect(self.handleExistingVoting)

        layout = QVBoxLayout()
        layout.addWidget(self.votingListWidget)
        layout.addStretch(1)
        self.leftBox.setLayout(layout)

    def showNoHostsBox(self):
        box = QMessageBox()
        box.setWindowTitle("Action not available")
        box.setText("No hosts are available or search is pending.\nPlease wait.")
        box.exec_()

    def showInvalidParametersBox(self):
        box = QMessageBox()
        box.setWindowTitle("Invalid parameters")
        box.setText("Invalid parameters inserted. Cannot proceed.")
        box.exec_()

    def showVotingCreatedBox(self):
        box = QMessageBox()
        box.setWindowTitle("Voting created")
        box.setText("New voting created.")
        box.exec_()

    def removeVotingOption(self):
        self.rightVoteBoxLayout.removeWidget(self.voteOptions[-1])
        self.voteOptions.pop()

    def addVotingOption(self):
        voteOptionEdit = QLineEdit()
        self.voteOptions.append(voteOptionEdit)
        self.rightVoteBoxLayout.addWidget(self.voteOptions[-1])

    def createVotingButtonAction(self):
        options = []
        for option in self.voteOptions:
            if not option.text():
                self.showInvalidParametersBox()
                return
            options.append(option.text())
        
        if not self.votingNameEdit.text():
            self.showInvalidParametersBox()
            return
        voting = Voting()
        voting.createNewVoteOptionList(options)
        voting.votingName = self.votingNameEdit.text()

        self.ongoingVotings.append(voting)
        self.messageSender.sendVotingMsg(voting)
        self.voteOptions.clear()
        self.updateVotingListWidget()

    def runNewVote(self):
        # if len(self.availableHosts) == 0:
        #     self.showNoHostsBox()
        #     return

        self.newVoteDialog = QDialog()
        self.newVoteDialog.setWindowTitle("Create voting")
        self.voteOptions = []

        self.votingNameEdit = QLineEdit()
        votingNameLabel = QLabel("Enter voting name:")

        createVotingButton = QPushButton("Create voting")
        createVotingButton.clicked.connect(self.createVotingButtonAction)

        cancelNewVotingButton = QPushButton("Cancel")
        cancelNewVotingButton.setDefault(True)
        cancelNewVotingButton.clicked.connect(self.newVoteDialog.close)

        voteOptionsLabel = QLabel("Enter voting options:")

        addVoteOptionButton = QPushButton("Add vote option")
        addVoteOptionButton.clicked.connect(self.addVotingOption)

        removeVoteOptionButton = QPushButton("Remove vote option")
        removeVoteOptionButton.clicked.connect(self.removeVotingOption)

        self.rightVoteBox = QGroupBox("Voting creator")
        self.rightVoteBoxLayout = QVBoxLayout()
        self.rightVoteBoxLayout.addWidget(votingNameLabel)
        self.rightVoteBoxLayout.addWidget(self.votingNameEdit)
        self.rightVoteBoxLayout.addWidget(voteOptionsLabel)
        self.rightVoteBox.setLayout(self.rightVoteBoxLayout)

        self.leftVoteBox = QGroupBox("Actions")
        self.leftVoteBoxLayout = QVBoxLayout()
        self.leftVoteBoxLayout.addWidget(createVotingButton)
        self.leftVoteBoxLayout.addWidget(cancelNewVotingButton)
        self.leftVoteBoxLayout.addWidget(addVoteOptionButton)
        self.leftVoteBoxLayout.addWidget(removeVoteOptionButton)
        self.leftVoteBox.setLayout(self.leftVoteBoxLayout)

        layout = QGridLayout()
        layout.addWidget(self.leftVoteBox, 0, 0)
        layout.addWidget(self.rightVoteBox, 0, 1)
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
