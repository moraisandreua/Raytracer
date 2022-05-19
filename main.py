from PyQt6.QtWidgets import QApplication
from MainWindow import MainWindow
import sys

def openGUI():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    openGUI()