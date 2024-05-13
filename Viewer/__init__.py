from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QFileDialog, QMessageBox, QLineEdit, QLabel, QDialog, QComboBox
)
from PyQt5.QtCore import Qt
from Viewer.AddEventWindow import AddEventWindow
import json
from datetime import datetime
from Controller import Controller
from Task import Task, AntiTask, RecurringTask, TransientTask

class Viewer(QWidget):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PSS Schedule Viewer')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.create_search_layout(layout)
        self.create_table_widget(layout)

        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.open_add_event_window)
        layout.addWidget(self.add_event_button)

        self.export_button = QPushButton("Export Schedule")
        self.export_button.clicked.connect(self.export_schedule)
        layout.addWidget(self.export_button)

        self.load_button = QPushButton("Load Schedule")
        self.load_button.clicked.connect(self.load_schedule)
        layout.addWidget(self.load_button)

        self.write_button = QPushButton("Write Schedule")
        self.write_button.clicked.connect(self.write_schedule_dialog)
        layout.addWidget(self.write_button)

        self.tableWidget.cellClicked.connect(self.edit_event_details)

    def create_search_layout(self, parent_layout):
        search_layout = QHBoxLayout()
        parent_layout.addLayout(search_layout)

        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self.search_task)
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_task)
        search_layout.addWidget(self.search_button)

    def create_table_widget(self, layout):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['Time Slot', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.tableWidget)

        self.populate_time_slots()

    def populate_time_slots(self):
        hours = range(0, 24)
        minutes = ['00', '15', '30', '45']
        self.tableWidget.setRowCount(len(hours) * len(minutes))

        for i, hour in enumerate(hours):
            for j, minute in enumerate(minutes):
                hour_12h = (hour % 12) or 12
                am_pm = "AM" if hour < 12 else "PM"
                item = QTableWidgetItem('{}:{:02d} {}'.format(hour_12h, int(minute), am_pm))
                self.tableWidget.setItem(i * len(minutes) + j, 0, item)
                self.tableWidget.setVerticalHeaderItem(i * len(minutes) + j, QTableWidgetItem(''))

    def open_add_event_window(self):
        add_event_window = AddEventWindow(self)
        add_event_window.exec_()

    def search_task(self):
        task_name = self.search_input.text()
        if not task_name:
            QMessageBox.warning(self, "Error", "Please enter a task name to search.")
            return
        task = self.controller.find_task_by_name(task_name)
        if task == None:
            QMessageBox.warning(self, "Error", f'Task with name "{task_name}" does not exist.')
        # Implement the logic to search for the task by name and display its information if found
        # You can use the viewer to access the schedule data and search for the task by name
        # Display the information using QMessageBox or any other appropriate widget

    def edit_event_details(self, row, column):
        item = self.tableWidget.item(row, column)

        if item is not None and item.text():
            event_name = item.text()
            start_time_row = row // 4
            start_time = '{}:{} {}'.format((start_time_row % 12) or 12, (row % 4) * 15, 'AM' if start_time_row < 12 else 'PM')
            end_time_row = (row + self.tableWidget.rowSpan(row, column) - 1) // 4
            end_time = '{}:{} {}'.format((end_time_row % 12) or 12, (row % 4) * 15, 'AM' if end_time_row < 12 else 'PM')
            color = item.background().color()
            selected_day = self.tableWidget.horizontalHeaderItem(column).text()
            description = item.toolTip()

            event_details = {
                "name": event_name,
                "start": start_time,
                "end": end_time,
                "description": description,
                "color": color,
                "selected_days": [selected_day]
            }

            add_event_window = AddEventWindow(self, event_details)
            add_event_window.exec_()

    def export_schedule(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Schedule", "", "Text Files (*.txt)")
        if file_name:
            # Write the schedule to the file
            with open(file_name, 'w') as file:
                # Write the schedule content here
                pass  # Placeholder for actual writing logic

    def load_schedule(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Schedule", "", "JSON Files (*.json)")
        if file_name:
            # Load the schedule from the JSON file
            with open(file_name, 'r') as file:
                schedule_data = json.load(file)
                # Process the loaded schedule data
                pass  # Placeholder for actual processing logic

    def write_schedule_dialog(self):
        dialog = WriteScheduleDialog(self)
        dialog.exec_()

class WriteScheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Write Schedule")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout(self)

        self.file_name_input = QLineEdit()
        layout.addWidget(QLabel("File Name:"))
        layout.addWidget(self.file_name_input)

        self.start_time_input = QLineEdit()
        layout.addWidget(QLabel("Start Time (H:MM):"))
        layout.addWidget(self.start_time_input)

        self.schedule_type_combo = QComboBox()
        self.schedule_type_combo.addItems(["Day", "Week", "Month"])
        layout.addWidget(QLabel("Select Schedule Type:"))
        layout.addWidget(self.schedule_type_combo)

        button_layout = QHBoxLayout()
        self.write_button = QPushButton("Write")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.write_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.write_button.clicked.connect(self.write_schedule)
        self.cancel_button.clicked.connect(self.reject)

    def write_schedule(self):
        file_name = self.file_name_input.text()
        start_time = self.start_time_input.text()
        schedule_type = self.schedule_type_combo.currentText()

        # Implement the logic to write the schedule based on the provided parameters
        # You can access the viewer to get schedule data and other relevant information

        self.accept()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    viewer = Viewer()
    viewer.show()
    sys.exit(app.exec_())
