from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QLabel, QComboBox, QHBoxLayout,
    QDialog, QMessageBox, QDateEdit, QRadioButton, QButtonGroup, QSpinBox
)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime
from Model.Model import TransientTask, RecurringTask, AntiTask  # Make sure to import the necessary task classes

class EditEventWindow(QDialog):
    def __init__(self, viewer, model, event_details):
        super().__init__()
        self.viewer = viewer
        self.model = model
        self.event_details = event_details

        self.setWindowTitle("Edit Event")
        self.setGeometry(200, 200, 400, 350)

        self.create_widgets()
        self.setup_layout()
        self.connect_signals()
        self.load_event_details()

    def load_event_details(self):
        self.event_name_edit.setText(self.event_details['name'])
        start_time_str, am_pm = self.event_details['start'].split()
        self.start_time_edit.setText(start_time_str)
        self.start_am_pm.setCurrentText(am_pm)
        start_date = QDate.fromString(self.event_details['selected_days'][0], "ddd MM/dd")
        self.beginning_date_edit.setDate(start_date)
        print(self.event_details['end'].split()[0])
        print(start_time_str)
        duration = float(self.event_details['end'].split()[0]) - float(start_time_str)
        self.duration_edit.setText(str(duration))
        
        # Set the type radio button
        event_type = self.event_details.get('description')
        if event_type:
            for button in self.type_radio_buttons.buttons():
                if button.text() == event_type:
                    button.setChecked(True)
                    break

        task_type = type(self.model.find_task_by_name(self.event_details['name']))
        if task_type == RecurringTask:
            self.recurring_radio.setChecked(True)
        elif task_type == TransientTask:
            self.transient_radio.setChecked(True)
        elif task_type == AntiTask:
            self.antitask_radio.setChecked(True)


    def update_event(self):
        def convert_to_decimal_time(time_str, am_pm):
            time_format = "%I:%M"
            time_obj = datetime.strptime(time_str, time_format)
            hours = time_obj.hour
            if am_pm == "PM" and hours != 12:
                hours += 12
            elif am_pm == "AM" and hours == 12:
                hours = 0
            return hours + time_obj.minute / 60.0

        event_name = self.event_name_edit.text()
        start_date = self.beginning_date_edit.date().toString("yyyyMMdd")
        start_time_str = self.start_time_edit.text()
        am_pm = self.start_am_pm.currentText()
        start_time = convert_to_decimal_time(start_time_str, am_pm)
        duration = float(self.duration_edit.text())

        task = self.model.find_task_by_name(self.event_details['name'])
        task_type = type(task)

        if task_type == RecurringTask:
            new_task = RecurringTask(
                name=event_name,
                task_type=task.task_type,
                start_date=start_date,
                start_time=start_time,
                duration=duration,
                end_date=task.end_date,
                frequency=task.frequency
            )
        elif task_type == TransientTask:
            new_task = TransientTask(
                name=event_name,
                task_type=task.task_type,
                start_date=start_date,
                start_time=start_time,
                duration=duration
            )
        elif task_type == AntiTask:
            new_task = AntiTask(
                name=event_name,
                start_date=start_date,
                start_time=start_time,
                duration=duration
            )

        try:
            self.model.edit_task(self.event_details['name'], new_task)
            self.viewer.refresh_views()
            self.accept()
        except ValueError as e:
            self.show_error(str(e))

    def delete_event(self):
        event_name = self.event_details['name']
        try:
            self.model.delete_task(event_name)
            self.viewer.refresh_views()
            self.accept()
        except ValueError as e:
            self.show_error(str(e))

    def create_widgets(self):
        self.event_name_edit = QLineEdit()
        self.start_time_edit = QLineEdit()
        self.duration_edit = QLineEdit()  # Duration input field

        self.start_am_pm = QComboBox()
        self.start_am_pm.addItems(["AM", "PM"])
        self.beginning_date_edit = QDateEdit()

        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Delete")
        self.cancel_button = QPushButton("Cancel")

    def connect_signals(self):
        self.update_button.clicked.connect(self.update_event)
        self.delete_button.clicked.connect(self.delete_event)
        self.cancel_button.clicked.connect(self.reject)

    def setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Event Name:"))
        layout.addWidget(self.event_name_edit)
        layout.addWidget(QLabel("Start Time (H:MM):"))
        layout.addWidget(self.start_time_edit)
        layout.addWidget(self.start_am_pm)
        layout.addWidget(QLabel("Duration (hours):"))  # Duration input label
        layout.addWidget(self.duration_edit)  # Duration input field

        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Date:"))
        date_layout.addWidget(self.beginning_date_edit)
        layout.addLayout(date_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
