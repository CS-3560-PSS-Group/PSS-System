from PyQt5.QtWidgets import QApplication
from Viewer import Viewer

if __name__ == '__main__':
    app = QApplication([])
    viewer = Viewer()
    viewer.show()
    app.exec_()


