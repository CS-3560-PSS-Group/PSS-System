from datetime import datetime
<<<<<<< HEAD
from PyQt5.QtWidgets import QMessageBox

=======
>>>>>>> f8a2d9b2c8eea207e073b0768a8e9d3a33bd859f
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QLabel, QComboBox, QHBoxLayout,
    QDialog, QCheckBox, QColorDialog, QPlainTextEdit, QErrorMessage, QDateEdit,
<<<<<<< HEAD
    QMessageBox, QCalendarWidget
=======
    QMessageBox, QCalendarWidget, QFileDialog
>>>>>>> f8a2d9b2c8eea207e073b0768a8e9d3a33bd859f
)
from PyQt5.QtCore import Qt, QDate
from Viewer.QColorButton import QColorButton


class AddEventWindow(QDialog):
    def __init__(self, viewer, event_details=None):
        super().__init__()
        self.viewer = viewer
        self.event_details = event_details
        self.description = ""

        self.setWindowTitle("Add Event")
        self.setGeometry(200, 200, 400, 350)

        self.file_name = self.get_file_name()

        self.create_widgets()
        self.setup_layout()
        self.populate_event_details(event_details)
    

    def get_file_name(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            return file_name
        else:
            return None
        
    def create_widgets(self):
        self.event_name_edit = QLineEdit()
        self.start_time_edit = QLineEdit()
        self.end_time_edit = QLineEdit()
        self.description_edit = QPlainTextEdit()
        self.color_button = QColorButton()
        self.recurring_checkbox = QCheckBox("Recurring")
        self.transient_checkbox = QCheckBox("Transient")  # New checkbox for transient
        self.transient_checkbox.stateChanged.connect(self.toggle_days_visibility)
        self.days_layout = QHBoxLayout()
        self.days_checkboxes = [
            QCheckBox(day) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ]
        self.days_label = QLabel("Select Days:")

<<<<<<< HEAD
=======
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")  # Button to trigger the search
        self.search_button.clicked.connect(self.search_task)  # Connect search_button click event to search_task method

>>>>>>> f8a2d9b2c8eea207e073b0768a8e9d3a33bd859f
        self.start_am_pm = QComboBox()
        self.start_am_pm.addItems(["AM", "PM"])
        self.end_am_pm = QComboBox()
        self.end_am_pm.addItems(["AM", "PM"])
        self.beginning_date_edit = QDateEdit()
        self.ending_date_edit = QDateEdit()
        self.add_button = QPushButton("Add")
        self.cancel_button = QPushButton("Cancel")
        self.delete_button = QPushButton("Delete")
        self.save_button = QPushButton("Save")
        self.anti_task_button = QPushButton("Anti-Task")  # New button

        self.recurring_checkbox.stateChanged.connect(self.toggle_weekly_box)
        self.add_button.clicked.connect(self.add_or_save_event)
        self.cancel_button.clicked.connect(self.reject)
        self.delete_button.clicked.connect(self.delete_event)
        self.save_button.clicked.connect(self.add_or_save_event)
        self.anti_task_button.clicked.connect(self.anti_task)

    def is_valid_time(self, time_str):
        try:
            # Attempt to parse the time string
            datetime.strptime(time_str, "%I:%M %p")
            return True
        except ValueError:
            return False
        
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
        layout.addWidget(self.recurring_checkbox)
        layout.addLayout(self.days_layout)
        layout.addWidget(self.transient_checkbox)

        self.days_layout.addWidget(self.days_label)
        for checkbox in self.days_checkboxes:
            self.days_layout.addWidget(checkbox)
            checkbox.hide()  # Initially hide all day checkboxes

<<<<<<< HEAD
=======
        layout.addWidget(QLabel("Search Task by Name:"))
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

>>>>>>> f8a2d9b2c8eea207e073b0768a8e9d3a33bd859f
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Beginning Date:"))
        date_layout.addWidget(self.beginning_date_edit)
        date_layout.addWidget(QLabel("Ending Date:"))
        date_layout.addWidget(self.ending_date_edit)
        layout.addLayout(date_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.anti_task_button)  # Add the Anti-Task button
        layout.addLayout(button_layout)


    def anti_task(self):
        # This method is called when the "Anti-Task" button is clicked
        print("Anti-Task button clicked")

    def toggle_weekly_box(self, state):
        if state == Qt.Checked:
            for checkbox in self.days_checkboxes:
                checkbox.show()
        else:
            for checkbox in self.days_checkboxes:
                checkbox.hide()

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
            QMessageBox.warning(self, "Error", "Missing required information.")

        self.close()

    def validate_inputs(self):
        event_name = self.event_name_edit.text()
        start_time = self.start_time_edit.text() + " " + self.start_am_pm.currentText()
        end_time = self.end_time_edit.text() + " " + self.end_am_pm.currentText()
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]

        if not event_name:
            QMessageBox.warning(self, "Error", "Event Name is required.")
            return False
        if not self.is_valid_time(start_time) or not self.is_valid_time(end_time):
            QMessageBox.warning(self, "Error", "Invalid time format. Please enter time in HH:MM AM/PM format.")
            return False
        if not selected_days:
            QMessageBox.warning(self, "Error", "Select at least one day for the event.")
            return False
        return True


    def add_event(self):
        event_name = self.event_name_edit.text()
        start_time = self.start_time_edit.text() + " " + self.start_am_pm.currentText()
        end_time = self.end_time_edit.text() + " " + self.end_am_pm.currentText()
        description = self.description_edit.toPlainText()
        color = self.color_button.color
        selected_days = [checkbox.text() for checkbox in self.days_checkboxes if checkbox.isChecked()]

        new_event = {
            "name": event_name,
            "start": start_time,
            "end": end_time,
            "description": description,
            "color": color,
            "selected_days": selected_days
        }

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
                start_item = self.viewer.tableWidget.verticalHeaderItem

        self.viewer.add_event_to_schedule(new_event)
        self.close()

    def toggle_days_visibility(self, state):
        if state == Qt.Checked:  # If transient checkbox is checked
            # Hide the days checkboxes
            for checkbox in self.days_checkboxes:
                checkbox.hide()
            self.days_label.hide()  # Optionally hide the days label as well
        else:
            # Show the days checkboxes
            for checkbox in self.days_checkboxes:
                checkbox.show()
<<<<<<< HEAD
            self.days_label.show()
=======
            self.days_label.show()

    def search_task(self):
        task_name = self.search_input.text()
        if not task_name:
            QMessageBox.warning(self, "Error", "Please enter a task name to search.")
            return
        # Implement the logic to search for the task by name and display its information if found
        # You can use the viewer to access the schedule data and search for the task by name
        # Display the information using QMessageBox or any other appropriate widget

# You can test this by creating an instance of AddEventWindow and running the application
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AddEventWindow(None)
    window.show()
    sys.exit(app.exec_())
>>>>>>> f8a2d9b2c8eea207e073b0768a8e9d3a33bd859f
