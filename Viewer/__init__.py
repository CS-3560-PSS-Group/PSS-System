from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHeaderView, QLabel, QComboBox, QHBoxLayout, QDialog, QCheckBox, QColorDialog, QPlainTextEdit, QErrorMessage
from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtCore import Qt
from Viewer.AddEventWindow import AddEventWindow

class Viewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PSS Schedule Viewer')
        self.setGeometry(100, 100, 800, 600)  # Increased window size

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QTableWidget with one column for time slots and seven columns for days of the week
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(8)  # One column for time slots and one for each day of the week
        self.tableWidget.setHorizontalHeaderLabels(['Time Slot', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

        # Set column widths and row heights
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Add rows for each hourly time slot from 12:00 AM to 11:45 PM
        hours = range(0, 24)
        minutes = ['00', '15', '30', '45']
        time_slots = ['{}:{:02d}'.format(hour, int(minute)) for hour in hours for minute in minutes]
        self.tableWidget.setRowCount(len(hours) * len(minutes))

        # Populate the first column with time slots (showing only hours)
        for i, hour in enumerate(hours):
            for j, minute in enumerate(minutes):
                item = QTableWidgetItem('{}:{}'.format(hour, minute))
                self.tableWidget.setItem(i * len(minutes) + j, 0, item)
                # Set vertical header item for each row
                self.tableWidget.setVerticalHeaderItem(i * len(minutes) + j, QTableWidgetItem(''))

        # Add a button to open the Add Event window
        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.open_add_event_window)

        layout.addWidget(self.tableWidget)
        layout.addWidget(self.add_event_button)

        self.tableWidget.cellClicked.connect(self.edit_event_details)

    def open_add_event_window(self):
        add_event_window = AddEventWindow(self)
        add_event_window.exec_()

    def edit_event_details(self, row, column):
        item = self.tableWidget.item(row, column)
        row_span = self.tableWidget.rowSpan(row, column)
        if item is not None and item.text():  # Check if the item exists and is not empty
            event_name = item.text()
            start_item = self.tableWidget.verticalHeaderItem(row)
            end_row = row + row_span - 1  # Calculate end row
            end_item = self.tableWidget.verticalHeaderItem(end_row)
            if start_item is not None and end_item is not None:
                start_time = start_item.text()
                end_time = end_item.text()
                description = item.toolTip()
                color = item.background().color()
                selected_days = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(1, 8) if self.tableWidget.horizontalHeaderItem(i) in self.tableWidget.selectedItems()]

                event_details = {
                    "name": event_name,
                    "start": start_time,
                    "end": end_time,
                    "description": description,
                    "color": color,
                    "selected_days": selected_days
                }
                add_event_window = AddEventWindow(self, event_details)
                add_event_window.exec_()
        else:
            # Handle case when cell is empty or modified
            print("Selected cell is empty or modified.")

    def update_event_cells(self, event_details, start_item, end_item):
        print("Update event cell called")
        event_name = event_details["name"]
        start_time = event_details["start"]
        end_time = event_details["end"]
        description = event_details["description"]
        color = event_details["color"]
        selected_days = event_details["selected_days"]

        start_row_index = start_item[0].row()
        end_row_index = end_item[0].row()

        for day in selected_days:
            column_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day) + 1
            for row in range(start_row_index, end_row_index + 1):
                # Ensure that vertical header items are set for each row
                start_item = self.tableWidget.verticalHeaderItem(row)
                item = QTableWidgetItem(event_name + " (" + start_time + " - " + end_time + ")")
                if description:
                    item.setToolTip(description)
                item.setBackground(color)
                item.setTextAlignment(Qt.AlignTop)
                self.tableWidget.setItem(row, column_index, item)
                if row == start_row_index:
                    self.tableWidget.setSpan(row, column_index, end_row_index - start_row_index + 1, 1)