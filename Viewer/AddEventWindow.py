from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QLabel, QComboBox, QHBoxLayout,
    QDialog, QCheckBox, QColorDialog, QPlainTextEdit, QErrorMessage
)
from PyQt5.QtCore import Qt
from Viewer.QColorButton import QColorButton


class AddEventWindow(QDialog):
    def __init__(self, viewer, event_details=None):
        super().__init__()
        self.viewer = viewer
        self.event_details = event_details
        self.description = ""

        self.setWindowTitle("Add Event")
        self.setGeometry(200, 200, 400, 350)

        self.create_widgets()
        self.setup_layout()
        self.populate_event_details(event_details)

    def create_widgets(self):
        self.event_name_edit = QLineEdit()
        self.start_time_edit = QLineEdit()
        self.end_time_edit = QLineEdit()
        self.description_edit = QPlainTextEdit()
        self.color_button = QColorButton()
        self.days_checkboxes = [QCheckBox(day) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
        self.start_am_pm = QComboBox()
        self.start_am_pm.addItems(["AM", "PM"])
        self.end_am_pm = QComboBox()
        self.end_am_pm.addItems(["AM", "PM"])
        self.add_button = QPushButton("Add")
        self.cancel_button = QPushButton("Cancel")
        self.delete_button = QPushButton("Delete")
        self.save_button = QPushButton("Save")

        self.add_button.clicked.connect(self.add_or_save_event)
        self.cancel_button.clicked.connect(self.reject)
        self.delete_button.clicked.connect(self.delete_event)
        self.save_button.clicked.connect(self.add_or_save_event)

    def setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Event Name:"))
        layout.addWidget(self.event_name_edit)
        layout.addWidget(QLabel("Start Time (H:MM):"))
        layout.addWidget(self.start_time_edit)
        layout.addWidget(self.start_am_pm)
        layout.addWidget(QLabel("End Time (H:MM):"))
        layout.addWidget(self.end_time_edit)
        layout.addWidget(self.end_am_pm)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_edit)
        layout.addWidget(QLabel("Color:"))
        layout.addWidget(self.color_button)

        days_layout = QHBoxLayout()
        days_label = QLabel("Select Days:")
        days_layout.addWidget(days_label)
        for checkbox in self.days_checkboxes:
            days_layout.addWidget(checkbox)
        layout.addLayout(days_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)

    def populate_event_details(self, event_details):
        if event_details:
            self.event_name_edit.setText(event_details["name"])
            self.start_time_edit.setText(event_details["start"].split(" ")[0])
            self.end_time_edit.setText(event_details["end"].split(" ")[0])
            self.description_edit.setPlainText(event_details["description"])
            self.color_button.color = event_details["color"]
            self.color_button.setStyleSheet("background-color: {}".format(event_details["color"].name()))

            selected_days = event_details["selected_days"]
            for checkbox in self.days_checkboxes:
                checkbox.setChecked(checkbox.text() in selected_days)

            # Ensuring times that end with "00" retains the trailing 0
            if event_details["start"].split(" ")[0].split(":")[1] == "0":
                self.start_time_edit.setText(event_details["start"].split(" ")[0].split(":")[0] + ":00")
            if event_details["end"].split(" ")[0].split(":")[1] == "0":
                self.end_time_edit.setText(event_details["end"].split(" ")[0].split(":")[0] + ":00")

    def add_or_save_event(self):
        if self.validate_inputs():
            if self.event_details:
                self.save_event()
            else:
                self.add_event()

    def delete_event(self):
        # Retrieve the selected days for the event
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]

        # Retrieve the start and end time of the event
        start_time = self.start_time_edit.text() + " " + self.start_am_pm.currentText()
        end_time = self.end_time_edit.text() + " " + self.end_am_pm.currentText()

        # Ensure that all required arguments are available
        if selected_days and start_time and end_time:
            # Call delete_previous_event with the required arguments
            self.delete_previous_event(selected_days, start_time, end_time)
        else:
            self.show_error("Missing required information.")
        
        self.close()

    def validate_inputs(self):
        event_name = self.event_name_edit.text()
        start_time = self.start_time_edit.text() + " " + self.start_am_pm.currentText()
        end_time = self.end_time_edit.text() + " " + self.end_am_pm.currentText()
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]

        if not event_name:
            self.show_error("Event Name is required.")
            return False
        if not self.is_valid_time(start_time) or not self.is_valid_time(end_time):
            self.show_error("Invalid time format. Please enter time in HH:MM AM/PM format.")
            return False
        if not selected_days:
            self.show_error("Select at least one day for the event.")
            return False
        return True

    def add_event(self):
        event_name = self.event_name_edit.text()
        start_time = self.start_time_edit.text() + " " + self.start_am_pm.currentText()
        end_time = self.end_time_edit.text() + " " + self.end_am_pm.currentText()
        description = self.description_edit.toPlainText()
        color = self.color_button.color
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]

        start_item = self.viewer.tableWidget.findItems(start_time, Qt.MatchExactly)
        if not start_item:
            self.show_error("Start time does not exist in the time slots.")
            return

        end_item = self.viewer.tableWidget.findItems(end_time, Qt.MatchExactly)
        if not end_item:
            self.show_error("End time does not exist in the time slots.")
            return

        start_row_index = start_item[0].row()
        end_row_index = end_item[0].row()

        for day in selected_days:
            column_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day) + 1
            for row in range(start_row_index, end_row_index + 1):
                start_item = self.viewer.tableWidget.verticalHeaderItem(row)
                if not start_item:
                    start_item = QTableWidgetItem(start_time)
                    self.viewer.tableWidget.setVerticalHeaderItem(row, start_item)
                end_item = self.viewer.tableWidget.verticalHeaderItem(row + (end_row_index - start_row_index))
                if not end_item:
                    end_item = QTableWidgetItem(end_time)
                    self.viewer.tableWidget.setVerticalHeaderItem(row + (end_row_index - start_row_index), end_item)

                item = QTableWidgetItem(event_name)
                item.setBackground(color)
                item.setTextAlignment(Qt.AlignTop)
                tooltip = description
                item.setToolTip(tooltip)
                self.viewer.tableWidget.setItem(row, column_index, item)
                if row == start_row_index:
                    self.viewer.tableWidget.setSpan(row, column_index, end_row_index - start_row_index + 1, 1)

        self.accept()

    def save_event(self):
        event_name = self.event_name_edit.text()
        start_time = self.start_time_edit.text() + " " + self.start_am_pm.currentText()
        end_time = self.end_time_edit.text() + " " + self.end_am_pm.currentText()
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]

        if not event_name or not start_time or not end_time:
            self.show_error("Event Name, Start Time, and End Time are required.")
            return

        if not selected_days:
            self.show_error("Select at least one day for the event.")
            return

        previous_event_details = self.event_details
        previous_selected_days = previous_event_details["selected_days"]
        previous_start_time = previous_event_details["start"]
        previous_end_time = previous_event_details["end"]
        print(previous_selected_days)
        print(selected_days)
        self.delete_previous_event(previous_selected_days, previous_start_time, previous_end_time)

        self.description = self.description_edit.toPlainText()

        # Update the event details instead of adding a new event
        self.update_event(event_name, start_time, end_time, selected_days, self.description)

        # Close the window after saving the event
        self.close()

    def update_event(self, event_name, start_time, end_time, selected_days, description):
        # Update the event details in the table
        color = self.color_button.color
        start_item = self.viewer.tableWidget.findItems(start_time, Qt.MatchExactly)
        end_item = self.viewer.tableWidget.findItems(end_time, Qt.MatchExactly)

        if start_item and end_item:
            start_row_index = start_item[0].row()
            end_row_index = end_item[0].row()

            for day in selected_days:
                column_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day) + 1
                for row in range(start_row_index, end_row_index + 1):
                    start_item = self.viewer.tableWidget.verticalHeaderItem(row)
                    if not start_item:
                        start_item = QTableWidgetItem(start_time)
                        self.viewer.tableWidget.setVerticalHeaderItem(row, start_item)
                    end_item = self.viewer.tableWidget.verticalHeaderItem(row + (end_row_index - start_row_index))
                    if not end_item:
                        end_item = QTableWidgetItem(end_time)
                        self.viewer.tableWidget.setVerticalHeaderItem(row + (end_row_index - start_row_index), end_item)

                    item = QTableWidgetItem(event_name)
                    item.setBackground(color)
                    item.setTextAlignment(Qt.AlignTop)
                    tooltip = description
                    item.setToolTip(tooltip)
                    self.viewer.tableWidget.setItem(row, column_index, item)
                    if row == start_row_index:
                        self.viewer.tableWidget.setSpan(row, column_index, end_row_index - start_row_index + 1, 1)
        else:
            self.show_error("Start or End time does not exist in the time slots.")

    def delete_previous_event(self, selected_days, start_time, end_time):
        if start_time.split(" ")[0].split(":")[1] == "0":
            start_item = self.viewer.tableWidget.findItems(start_time.split(" ")[0].split(":")[0] + ":00", Qt.MatchExactly)
        else:
            start_item = self.viewer.tableWidget.findItems(start_time, Qt.MatchExactly)     

        print(start_item)   

        if start_item:
            print("Start item found")
            start_row_index = start_item[0].row()
            duration_rows = self.calculate_duration_rows(start_time, end_time)
            for day in selected_days:
                column_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day) + 1

                for row in range(start_row_index, start_row_index + duration_rows):
                    item = self.viewer.tableWidget.item(row, column_index)
                    if item is not None:
                        self.viewer.tableWidget.setItem(row, column_index, QTableWidgetItem())  # Clear cell content

                self.viewer.tableWidget.setSpan(start_row_index, column_index, 1, 1)  # Remove span
        else:
            self.show_error("Previous event not found in the schedule.")

    def calculate_duration_rows(self, start_time, end_time):
        # Split start and end time into parts
        start_time_parts = start_time.split()
        end_time_parts = end_time.split()

        # Check if input times are properly formatted
        if len(start_time_parts) != 2 or len(end_time_parts) != 2:
            raise ValueError("Invalid time format. Expected 'HH:MM AM/PM'.")

        # Extract the time parts (hour and minute) and AM/PM specifier
        start_time_hour, start_time_minute = map(int, start_time_parts[0].split(':'))
        end_time_hour, end_time_minute = map(int, end_time_parts[0].split(':'))

        # Adjust hour based on AM/PM specifier
        if start_time_parts[1] == 'PM' and start_time_hour != 12:
            start_time_hour += 12
        if end_time_parts[1] == 'PM' and end_time_hour != 12:
            end_time_hour += 12

        if start_time_parts[1] == 'AM' and start_time_hour == 12:
            start_time_hour = 0

        # Calculate the start and end row indices
        start_row = start_time_hour * 4 + start_time_minute // 15
        end_row = end_time_hour * 4 + end_time_minute // 15

        # Calculate duration rows
        duration_rows = end_row - start_row + 1
        print(duration_rows)
        return duration_rows


    def is_valid_time(self, time_str):
        try:
            hours, minutes = map(int, time_str.split()[0].split(':'))
            if 1 <= hours <= 12 and 0 <= minutes <= 45:
                return True
        except ValueError:
            pass
        return False

    def show_error(self, message):
        error_dialog = QErrorMessage(self)
        error_dialog.showMessage(message)
