from PyQt5.QtWidgets import QApplication
from Viewer import Viewer
from Controller import Controller

if __name__ == '__main__':
    app = QApplication([])
    controller = Controller()
    viewer = Viewer(controller)
    viewer.show()
    app.exec_()
