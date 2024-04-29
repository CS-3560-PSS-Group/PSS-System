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

        if item is not None and item.text():
            event_name = item.text()
            start_time_row = row // 4  # Each hour has 4 rows
            start_time = '{}:00'.format(start_time_row)  # Calculate start time based on row index
            end_time_row = (row + self.tableWidget.rowSpan(row, column) - 1) // 4  # Calculate end time based on row index + row span
            end_time = '{}:00'.format(end_time_row)  # Calculate end time based on row index
            color = item.background().color()
            selected_day = self.tableWidget.horizontalHeaderItem(column).text()
            description = item.toolTip()  # Fetch description from the item's tooltip

            event_details = {
                "name": event_name,
                "start": start_time,
                "end": end_time,
                "description": description,  # Pass the description to the AddEventWindow
                "color": color,
                "selected_days": [selected_day]
            }

            add_event_window = AddEventWindow(self, event_details)
            add_event_window.exec_()



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
            
            # Clear previous event cells
            for row in range(start_row_index, end_row_index + 1):
                for c in range(1, self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, c)
                    if item and item.text().startswith(event_name):
                        self.tableWidget.setItem(row, c, QTableWidgetItem())

            for row in range(start_row_index, end_row_index + 1):
                # Ensure that vertical header items are set for each row
                if not self.tableWidget.verticalHeaderItem(row):
                    self.tableWidget.setVerticalHeaderItem(row, QTableWidgetItem())

                item = QTableWidgetItem(event_name)  # Only set event name without start time and end time
                if description:
                    item.setToolTip(description)
                item.setBackground(color)
                item.setTextAlignment(Qt.AlignTop)
                self.tableWidget.setItem(row, column_index, item)
                
                if row == start_row_index:
                    self.tableWidget.setSpan(row, column_index, end_row_index - start_row_index + 1, 1)

                print("Set vertical header item:", self.tableWidget.verticalHeaderItem(row).text())

        # Update start time and end time if changed
        if start_time != event_name.split('(')[-1].split('-')[0].strip() or end_time != event_name.split('-')[-1].split(')')[0].strip():
            self.clear_previous_event_cells(event_name, start_row_index, end_row_index, selected_days)
            self.update_time(event_name, start_time, end_time, color, start_row_index, end_row_index, selected_days)

    def clear_previous_event_cells(self, event_name, start_row_index, end_row_index, selected_days):
        for day in selected_days:
            column_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day) + 1
            for row in range(start_row_index, end_row_index + 1):
                for c in range(1, self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, c)
                    if item and item.text().startswith(event_name):
                        self.tableWidget.setItem(row, c, QTableWidgetItem())

    def update_time(self, event_name, start_time, end_time, color, start_row_index, end_row_index, selected_days):
        # Clear existing spans for the updated event
        for day in selected_days:
            column_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day) + 1
            for row in range(start_row_index, end_row_index + 1):
                self.tableWidget.setSpan(row, column_index, 1, 1)  # Set span to (1, 1) to unmerge cells

        # Set new spans and update event details
        for day in selected_days:
            column_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day) + 1
            for row in range(start_row_index, end_row_index + 1):
                # Clear existing cell content
                self.tableWidget.setItem(row, column_index, None)  # Set item to None to clear the existing content
                
                # Ensure that vertical header items are set for each row
                if not self.tableWidget.verticalHeaderItem(row):
                    self.tableWidget.setVerticalHeaderItem(row, QTableWidgetItem())

                # Set the new event details
                item = QTableWidgetItem(event_name + " (" + start_time + " - " + end_time + ")")
                item.setBackground(color)
                item.setTextAlignment(Qt.AlignTop)
                self.tableWidget.setItem(row, column_index, item)
                
                if row == start_row_index:
                    # Set the new span for the start row
                    span_height = end_row_index - start_row_index + 1
                    self.tableWidget.setSpan(start_row_index, column_index, span_height, 1)





