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

class AddEventWindow(QDialog):
    def __init__(self, viewer, event_details=None):
        super().__init__()
        self.viewer = viewer
        self.setWindowTitle("Add Event")
        self.setGeometry(200, 200, 400, 350)  # Increased height

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.event_name_edit = QLineEdit()
        self.start_time_edit = QLineEdit()
        self.end_time_edit = QLineEdit()
        self.description_edit = QPlainTextEdit()  # Use QPlainTextEdit for description
        self.color_button = QColorButton()
        self.days_checkboxes = []

        layout.addWidget(QLabel("Event Name:"))
        layout.addWidget(self.event_name_edit)
        layout.addWidget(QLabel("Start Time (HH:MM):"))
        layout.addWidget(self.start_time_edit)
        layout.addWidget(QLabel("End Time (HH:MM):"))
        layout.addWidget(self.end_time_edit)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_edit)
        layout.addWidget(QLabel("Color:"))
        layout.addWidget(self.color_button)

        self.days_label = QLabel("Select Days:")
        self.days_layout = QHBoxLayout()
        self.add_days_checkboxes()

        layout.addWidget(self.days_label)
        layout.addLayout(self.days_layout)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")
        self.cancel_button = QPushButton("Cancel")
        self.add_button.clicked.connect(self.add_event)
        self.delete_button.clicked.connect(self.delete_event)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        if event_details:
            self.populate_event_details(event_details)

        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_event)
        layout.addWidget(self.save_button)

        self.viewer = viewer
        self.event_details = event_details
        

    def populate_event_details(self, event_details):
        self.event_name_edit.setText(event_details["name"])
        self.start_time_edit.setText(event_details["start"])
        self.end_time_edit.setText(event_details["end"])
        self.description_edit.setPlainText(event_details["description"])
        self.color_button.color = event_details["color"]
        self.color_button.setStyleSheet("background-color: {}".format(event_details["color"].name()))

        selected_days = event_details["selected_days"]
        for checkbox in self.days_checkboxes:
            checkbox.setChecked(checkbox.text() in selected_days)


    def add_days_checkboxes(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            checkbox = QCheckBox(day)
            self.days_layout.addWidget(checkbox)
            self.days_checkboxes.append(checkbox)

    def add_event(self):
        event_name = self.event_name_edit.text()
        start_time = self.start_time_edit.text()
        end_time = self.end_time_edit.text()
        description = self.description_edit.toPlainText()  # Get description text
        color = self.color_button.color
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]

        if not event_name:
            self.showError("Event Name is required.")
            return
        if not self.isValidTime(start_time) or not self.isValidTime(end_time):
            self.showError("Invalid time format. Please enter time in HH:MM format.")
            return

        start_item = self.viewer.tableWidget.findItems(start_time, Qt.MatchExactly)
        if not start_item:
            self.showError("Start time does not exist in the time slots.")
            return

        end_item = self.viewer.tableWidget.findItems(end_time, Qt.MatchExactly)
        if not end_item:
            self.showError("End time does not exist in the time slots.")
            return

        start_row_index = start_item[0].row()
        end_row_index = end_item[0].row()

        for day in selected_days:
            column_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day) + 1
            for row in range(start_row_index, end_row_index + 1):
                # Ensure that vertical header items are set for each row
                start_item = self.viewer.tableWidget.verticalHeaderItem(row)
                item = QTableWidgetItem(event_name + " (" + start_time + " - " + end_time + ")")
                if description:
                    item.setToolTip(description)
                item.setBackground(color)
                item.setTextAlignment(Qt.AlignTop)
                self.viewer.tableWidget.setItem(row, column_index, item)
                if row == start_row_index:
                    self.viewer.tableWidget.setSpan(row, column_index, end_row_index - start_row_index + 1, 1)

        self.accept()

    def delete_event(self):
        # Get the selected days for the event
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]

        # Retrieve the start and end time of the event
        start_time = self.start_time_edit.text()
        end_time = self.end_time_edit.text()

        # Find the item corresponding to the start time in the table
        start_item = self.viewer.tableWidget.findItems(start_time, Qt.MatchExactly)

        # Check if the start item exists
        if start_item:
            start_row_index = start_item[0].row()

            # Calculate the number of rows occupied by the event
            duration_rows = self.calculate_duration_rows(start_time, end_time)

            # Iterate over the selected days and remove the event from the schedule
            for day in selected_days:
                column_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day) + 1

                # Clear the cells corresponding to the event
                for row in range(start_row_index, start_row_index + duration_rows):
                    item = self.viewer.tableWidget.item(row, column_index)
                    if item is not None:
                        self.viewer.tableWidget.setItem(row, column_index, QTableWidgetItem())

                # Remove the span from the start row
                self.viewer.tableWidget.setSpan(start_row_index, column_index, 1, 1)

            # Close the dialog
            self.close()
        else:
            self.showError("Event not found in the schedule.")

    def calculate_duration_rows(self, start_time, end_time):
        start_hour, start_minute = map(int, start_time.split(':'))
        end_hour, end_minute = map(int, end_time.split(':'))

        start_row = start_hour * 4 + start_minute // 15
        end_row = end_hour * 4 + end_minute // 15

        return end_row - start_row + 1

    def showError(self, message):
        error_dialog = QErrorMessage()
        error_dialog.showMessage(message)

    def isValidTime(self, time_str):
        try:
            hours, minutes = map(int, time_str.split(':'))
            return 0 <= hours <= 23 and 0 <= minutes <= 59
        except ValueError:
            return False
        
    def save_event(self):
        
        # Retrieve updated event details from the UI
        event_name = self.event_name_edit.text()
        start_time = self.start_time_edit.text()
        end_time = self.end_time_edit.text()
        description = self.description_edit.toPlainText()
        color = self.color_button.color
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]

        event_details = {
            "name": event_name,
            "start": start_time,
            "end": end_time,
            "description": description,
            "color": color,
            "selected_days": selected_days
        }

        start_item = self.viewer.tableWidget.findItems(start_time, Qt.MatchExactly)
        if not start_item:
            self.showError("Start time does not exist in the time slots.")
            return

        end_item = self.viewer.tableWidget.findItems(end_time, Qt.MatchExactly)
        if not end_item:
            self.showError("End time does not exist in the time slots.")
            return
        
        
        
        self.viewer.update_event_cells(event_details, start_item, end_item)

        # Close the dialog
        self.close()

    

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

if __name__ == '__main__':
    app = QApplication([])
    viewer = Viewer()
    viewer.show()
    app.exec_()
