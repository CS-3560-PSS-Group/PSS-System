from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHeaderView, QLabel, QComboBox, QHBoxLayout, QDialog, QCheckBox, QColorDialog, QPlainTextEdit, QErrorMessage
from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtCore import Qt

class QColorButton(QPushButton):
    def __init__(self, color=QColor("white")):
        super().__init__()
        self.color = color
        self.setStyleSheet("background-color: {}".format(self.color.name()))
        self.clicked.connect(self.choose_color)

    def choose_color(self):
        color = QColorDialog.getColor(initial=self.color)
        if color.isValid():
            self.color = color
            self.setStyleSheet("background-color: {}".format(self.color.name()))