import sys
from PyQt5.QtWidgets import (QApplication)
from Menu import Menu

if __name__ == '__main__':
    guiApp = QApplication(sys.argv)
    gui = Menu()
    gui.show()
    print("Executing gui")
    sys.exit(guiApp.exec_()) 