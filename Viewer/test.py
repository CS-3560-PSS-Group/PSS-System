import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateEdit

class DateWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.dateEdit = QDateEdit()
        layout.addWidget(self.dateEdit)
        self.setLayout(layout)
        self.setWindowTitle('Date Picker')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DateWidget()
    window.show()
    sys.exit(app.exec_())
