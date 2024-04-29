from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHeaderView, QLabel, QComboBox, QHBoxLayout, QDialog, QCheckBox, QColorDialog, QPlainTextEdit, QErrorMessage
from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtCore import Qt
from Viewer.QColorButton import QColorButton

class AddEventWindow(QDialog):
    def __init__(self, viewer, event_details=None):
        super().__init__()
        self.viewer = viewer
        self.event_details = event_details
        self.description = ""
        
        # Set window title and geometry
        self.setWindowTitle("Add Event")
        self.setGeometry(200, 200, 400, 350) 

        # Create a layout for the dialog
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create widgets for event details
        self.event_name_edit = QLineEdit()
        self.start_time_edit = QLineEdit()
        self.end_time_edit = QLineEdit()
        self.description_edit = QPlainTextEdit()
        self.color_button = QColorButton()
        self.days_checkboxes = []

        # Add widgets to the layout
        layout.addWidget(QLabel("Event Name:"))
        layout.addWidget(self.event_name_edit)
        layout.addWidget(QLabel("Start Time (H:MM):"))
        layout.addWidget(self.start_time_edit)
        layout.addWidget(QLabel("End Time (H:MM):"))
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
        self.cancel_button = QPushButton("Cancel")
        self.delete_button = QPushButton("Delete")
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
        description = self.description_edit.toPlainText()
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
        
        if not selected_days:
            self.showError("Select at least one day for the event.")
            return

        start_row_index = start_item[0].row()
        end_row_index = end_item[0].row()

        # Inside the loop for each day
        for day in selected_days:
            column_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day) + 1
            for row in range(start_row_index, end_row_index + 1):
                # Ensure that vertical header items are set for each row
                start_item = self.viewer.tableWidget.verticalHeaderItem(row)
                if not start_item:  # If vertical header item for start time doesn't exist, create one
                    start_item = QTableWidgetItem(start_time)
                    self.viewer.tableWidget.setVerticalHeaderItem(row, start_item)
                end_item = self.viewer.tableWidget.verticalHeaderItem(row + (end_row_index - start_row_index))
                if not end_item:  # If vertical header item for end time doesn't exist, create one
                    end_item = QTableWidgetItem(end_time)
                    self.viewer.tableWidget.setVerticalHeaderItem(row + (end_row_index - start_row_index), end_item)
                    
                # Puts event name on specific cells
                item = QTableWidgetItem(event_name)
                item.setBackground(color)
                item.setTextAlignment(Qt.AlignTop)

                tooltip = "Start Time: {}\nEnd Time: {}\nDescription: {}".format(start_time, end_time, description)
                item.setToolTip(tooltip)

                # Merges the cells on the grid based on the start and end time
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
        # Color was grabbed in a different way
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]

        # Ensure event name, start time, and end time are not empty
        if not event_name or not start_time or not end_time:
            self.showError("Event Name, Start Time, and End Time are required.")
            return

        # Check if start time and end time are in valid format
        if not self.isValidTime(start_time) or not self.isValidTime(end_time):
            self.showError("Invalid time format. Please enter time in HH:MM format.")
            return

        # Retrieve the selected days and check if any day is selected
        if not selected_days:
            self.showError("Select at least one day for the event.")
            return

        # Find items corresponding to the start and end time in the table
        start_item = self.viewer.tableWidget.findItems(start_time, Qt.MatchExactly)
        end_item = self.viewer.tableWidget.findItems(end_time, Qt.MatchExactly)

        # Ensure start and end time slots exist in the schedule
        if not start_item or not end_item:
            self.showError("Start or End time does not exist in the time slots.")
            return

        # Set the description variable
        self.description = self.description_edit.toPlainText()

        # Call the existing method to add the event to the schedule
        self.add_event()
        # Close the dialog
        self.close()

    def get_description(self):
        return self.description
