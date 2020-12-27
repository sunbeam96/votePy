from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QListWidget, QPushButton, QGroupBox, QGridLayout, QDialog, QMessageBox, QAction)


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

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

        firstButton = QPushButton("New voting")
        firstButton.setDefault(True)

        secondButton = QPushButton("About")
        secondButton.clicked.connect(self.showAboutBox)
        layout = QVBoxLayout()
        layout.addWidget(firstButton)
        layout.addWidget(secondButton)
        layout.addStretch(1)
        self.rightBox.setLayout(layout)


if __name__ == '__main__':

    import sys

    guiApp = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(guiApp.exec_()) 