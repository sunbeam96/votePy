from PyQt5.QtWidgets import (QVBoxLayout, QListWidget, QPushButton, QGroupBox, QGridLayout, QDialog, QMessageBox, QAction)

class Menu(QDialog):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)

        self.createVotingList()
        self.createActionList()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.leftBox, 0, 0)
        mainLayout.addWidget(self.rightBox, 0, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("votePy")


    def createVotingList(self):
        self.leftBox = QGroupBox("Ongoing votings")
        listWidget = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(listWidget)
        layout.addStretch(1)
        self.leftBox.setLayout(layout)  

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

        aboutButton = QPushButton("About")
        aboutButton.clicked.connect(self.showAboutBox)
        layout = QVBoxLayout()
        layout.addWidget(newVoteButton)
        layout.addWidget(showParticipantsButton)
        layout.addWidget(aboutButton)
        layout.addStretch(1)
        self.rightBox.setLayout(layout)
