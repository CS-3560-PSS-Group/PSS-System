from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QLabel, QComboBox, QHBoxLayout,
    QDialog, QMessageBox, QDateEdit, QRadioButton, QButtonGroup, QSpinBox
)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime
from Model.Model import TransientTask, RecurringTask, AntiTask  # Make sure to import the necessary task classes

class AddEventWindow(QDialog):
    def __init__(self, viewer, model, event_details=None):
        super().__init__()
        self.viewer = viewer
        self.model = model
        self.event_details = event_details

        self.setWindowTitle("Add Event")
        self.setGeometry(200, 200, 400, 350)

        self.create_widgets()
        self.setup_layout()
        self.connect_signals()
        self.hide_type_options()

    def add_event(self):
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
        event_type = [radio.text() for radio in self.type_radio_buttons.buttons() if radio.isChecked()]
        start_date = self.beginning_date_edit.date().toString("yyyyMMdd")
        start_time_str = self.start_time_edit.text()
        am_pm = self.start_am_pm.currentText()
        start_time = convert_to_decimal_time(start_time_str, am_pm)
        duration = float(self.duration_edit.text())

        if self.weekly_radio.isChecked():
            frequency = 7
        elif self.daily_radio.isChecked():
            frequency = 1

        task_type = None
        if self.recurring_radio.isChecked():
            task_type = "Recurring"
        elif self.transient_radio.isChecked():
            task_type = "Transient"
        elif self.antitask_radio.isChecked():
            task_type = "Antitask"

        task = None
        if task_type == "Recurring":
            task = RecurringTask(
                name=event_name,
                task_type=event_type[0] if event_type else None,
                start_date=self.beginning_date_edit.date().toString("yyyyMMdd"),
                start_time=start_time,
                duration=duration,
                end_date=self.ending_date_edit.date().toString("yyyyMMdd"),
                frequency=frequency
            )
        elif task_type == "Transient":
            task = TransientTask(
                event_name, event_type[0] if event_type else None, start_date, start_time, duration
            )
        elif task_type == "Antitask":
            task = AntiTask(
                event_name, start_date, start_time, duration
            )

        if task:
            try:
                self.model.add_task(task)
                self.viewer.refresh_views()
                self.accept()
            except ValueError as e:
                self.show_error(str(e))

    def create_widgets(self):
        self.event_name_edit = QLineEdit()
        self.start_time_edit = QLineEdit()
        self.duration_edit = QLineEdit()  # Duration input field
        self.recurring_radio = QRadioButton("Recurring")
        self.daily_radio = QRadioButton("Daily")
        self.weekly_radio = QRadioButton("Weekly")
        self.transient_radio = QRadioButton("Transient")
        self.antitask_radio = QRadioButton("Antitask")

        self.recurring_group = QButtonGroup(self)
        self.recurring_group.addButton(self.daily_radio)
        self.recurring_group.addButton(self.weekly_radio)

        self.daily_radio.hide()
        self.weekly_radio.hide()

        self.start_am_pm = QComboBox()
        self.start_am_pm.addItems(["AM", "PM"])
        self.beginning_date_edit = QDateEdit()
        self.ending_date_edit = QDateEdit()

        self.add_button = QPushButton("Add")
        self.cancel_button = QPushButton("Cancel")

        self.radio_button_class = QRadioButton("Class")
        self.radio_button_study = QRadioButton("Study")
        self.radio_button_sleep = QRadioButton("Sleep")
        self.radio_button_exercise = QRadioButton("Exercise")
        self.radio_button_work = QRadioButton("Work")
        self.radio_button_meal = QRadioButton("Meal")

        self.radio_button_visit = QRadioButton("Visit")
        self.radio_button_shopping = QRadioButton("Shopping")
        self.radio_button_appointment = QRadioButton("Appointment")
        self.radio_button_cancellation = QRadioButton("Cancellation")

        self.type_radio_buttons = QButtonGroup(self)
        self.type_radio_buttons.addButton(self.radio_button_class)
        self.type_radio_buttons.addButton(self.radio_button_study)
        self.type_radio_buttons.addButton(self.radio_button_sleep)
        self.type_radio_buttons.addButton(self.radio_button_exercise)
        self.type_radio_buttons.addButton(self.radio_button_work)
        self.type_radio_buttons.addButton(self.radio_button_meal)
        self.type_radio_buttons.addButton(self.radio_button_visit)
        self.type_radio_buttons.addButton(self.radio_button_shopping)
        self.type_radio_buttons.addButton(self.radio_button_appointment)
        self.type_radio_buttons.addButton(self.radio_button_cancellation)

        self.radio_button_visit.hide()
        self.radio_button_shopping.hide()
        self.radio_button_appointment.hide()
        self.radio_button_cancellation.hide()

    def connect_signals(self):
        self.recurring_radio.toggled.connect(self.toggle_recurring_options)
        self.daily_radio.toggled.connect(self.ensure_exclusive_daily_weekly)
        self.weekly_radio.toggled.connect(self.ensure_exclusive_daily_weekly)
        self.transient_radio.toggled.connect(self.toggle_transient_type_visibility)
        self.antitask_radio.toggled.connect(self.toggle_antitask_type_visibility)

        self.add_button.clicked.connect(self.add_or_save_event)
        self.cancel_button.clicked.connect(self.reject)

        self.recurring_radio.toggled.connect(self.unselect_types)
        self.transient_radio.toggled.connect(self.unselect_types)
        self.antitask_radio.toggled.connect(self.unselect_types)

        for radio_button in self.type_radio_buttons.buttons():
            radio_button.toggled.connect(self.handle_type_selection)

    def update_visibility_on_uncheck(self):
        self.recurring_radio.toggled.connect(self.clear_if_unchecked)
        self.transient_radio.toggled.connect(self.clear_if_unchecked)
        self.antitask_radio.toggled.connect(self.clear_if_unchecked)
        self.daily_radio.toggled.connect(self.clear_if_unchecked)
        self.weekly_radio.toggled.connect(self.clear_if_unchecked)

    def clear_if_unchecked(self, checked):
        if not checked:
            sender = self.sender()
            if sender == self.recurring_radio:
                self.hide_type_options()
                self.daily_radio.hide()
                self.weekly_radio.hide()
                self.daily_radio.setChecked(False)
                self.weekly_radio.setChecked(False)
            elif sender == self.antitask_radio:
                pass
            elif sender == self.daily_radio or sender == self.weekly_radio:
                if not self.daily_radio.isChecked() and not self.weekly_radio.isChecked():
                    self.recurring_radio.setChecked(False)

    def ensure_exclusive_daily_weekly(self, checked):
        sender = self.sender()
        if sender == self.daily_radio and checked:
            self.weekly_radio.setChecked(False)
        elif sender == self.weekly_radio and checked:
            self.daily_radio.setChecked(False)

        if self.daily_radio.isChecked() or self.weekly_radio.isChecked():
            self.recurring_radio.setChecked(True)

    def toggle_recurring_options(self, checked):
        if checked:
            self.daily_radio.show()
            self.weekly_radio.show()
            self.show_type_options()
        else:
            if not self.daily_radio.isChecked() and not self.weekly_radio.isChecked():
                self.daily_radio.hide()
                self.weekly_radio.hide()
                self.daily_radio.setChecked(False)
                self.weekly_radio.setChecked(False)
            self.hide_type_options()

    def show_transient_types(self):
        self.radio_button_visit.show()
        self.radio_button_shopping.show()
        self.radio_button_appointment.show()

    def hide_transient_types(self):
        self.radio_button_visit.hide()
        self.radio_button_shopping.hide()
        self.radio_button_appointment.hide()

    def toggle_transient_type_visibility(self, checked):
        if checked:
            self.show_transient_types()
        else:
            self.hide_transient_types()

    def setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Event Name:"))
        layout.addWidget(self.event_name_edit)
        layout.addWidget(QLabel("Start Time (H:MM):"))
        layout.addWidget(self.start_time_edit)
        layout.addWidget(self.start_am_pm)
        layout.addWidget(QLabel("Duration (hours):"))  # Duration input label
        layout.addWidget(self.duration_edit)  # Duration input field

        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.addWidget(self.recurring_radio)
        checkboxes_layout.addWidget(self.transient_radio)
        checkboxes_layout.addWidget(self.antitask_radio)
        layout.addLayout(checkboxes_layout)

        recurring_options_layout = QHBoxLayout()
        recurring_options_layout.addWidget(self.daily_radio)
        recurring_options_layout.addWidget(self.weekly_radio)
        layout.addLayout(recurring_options_layout)

        layout.addWidget(QLabel("Type:"))

        type_selection_layout = QVBoxLayout()
        type_selection_layout.addWidget(self.radio_button_class)
        type_selection_layout.addWidget(self.radio_button_study)
        type_selection_layout.addWidget(self.radio_button_sleep)
        type_selection_layout.addWidget(self.radio_button_exercise)
        type_selection_layout.addWidget(self.radio_button_work)
        type_selection_layout.addWidget(self.radio_button_meal)
        type_selection_layout.addWidget(self.radio_button_cancellation)
        type_selection_layout.addWidget(self.radio_button_visit)
        type_selection_layout.addWidget(self.radio_button_shopping)
        type_selection_layout.addWidget(self.radio_button_appointment)

        layout.addLayout(type_selection_layout)

        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Beginning Date:"))
        date_layout.addWidget(self.beginning_date_edit)
        date_layout.addWidget(QLabel("Ending Date:"))
        date_layout.addWidget(self.ending_date_edit)
        layout.addLayout(date_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def add_or_save_event(self):
        if self.validate_inputs():
            if self.event_details:
                self.save_event()
            else:
                self.add_event()

    def validate_inputs(self):
        event_name = self.event_name_edit.text()
        start_time = self.start_time_edit.text() + " " + self.start_am_pm.currentText()
        duration = self.duration_edit.text()

        if not event_name:
            QMessageBox.warning(self, "Error", "Event Name is required.")
            return False
        if not self.is_valid_time(start_time):
            QMessageBox.warning(self, "Error", "Invalid time format. Please enter time in HH:MM AM/PM format.")
            return False
        if not self.is_valid_duration(duration):
            QMessageBox.warning(self, "Error", "Invalid duration format. Please enter a numeric value.")
            return False
        return True

    def is_valid_time(self, time_str):
        try:
            datetime.strptime(time_str, "%I:%M %p")
            return True
        except ValueError:
            return False

    def is_valid_duration(self, duration_str):
        try:
            float(duration_str)
            return True
        except ValueError:
            return False

    def find_day_column_index(self, day):
        header = self.viewer.tableWidget.horizontalHeader()
        for col in range(header.count()):
            if header.model().headerData(col, Qt.Horizontal) == day:
                return col
        return -1

    def find_row_index(self, time_str):
        time_format = "%I:%M %p"
        time = datetime.strptime(time_str, time_format)
        hour = time.hour
        minute = time.minute

        row_index = (hour * 4) + (minute // 15)
        return row_index

    def update_type_options(self):
        self.type_radio_buttons.buttons()

        if self.recurring_radio.isChecked():
            self.type_radio_buttons.addButton(self.radio_button_class)
            self.type_radio_buttons.addButton(self.radio_button_study)
            self.type_radio_buttons.addButton(self.radio_button_sleep)
            self.type_radio_buttons.addButton(self.radio_button_exercise)
            self.type_radio_buttons.addButton(self.radio_button_work)
            self.type_radio_buttons.addButton(self.radio_button_meal)
        else:
            self.type_radio_buttons.addButton(self.radio_button_meal)

        self.type_radio_buttons.buttons()[0].setChecked(True)

    def toggle_type_options_visibility(self, state):
        if state:
            self.show_type_options()
        else:
            self.hide_type_options()

    def hide_type_options(self):
        self.radio_button_class.hide()
        self.radio_button_study.hide()
        self.radio_button_sleep.hide()
        self.radio_button_exercise.hide()
        self.radio_button_work.hide()
        self.radio_button_meal.hide()

    def show_type_options(self):
        self.radio_button_class.show()
        self.radio_button_study.show()
        self.radio_button_sleep.show()
        self.radio_button_exercise.show()
        self.radio_button_work.show()
        self.radio_button_meal.show()

    def toggle_antitask_type_visibility(self, state):
        if state:
            self.show_antitask_type_options()
        else:
            self.hide_antitask_type_options()

    def show_antitask_type_options(self):
        self.radio_button_cancellation.show()

    def hide_antitask_type_options(self):
        self.radio_button_cancellation.hide()

    def clear_hidden_selections(self):
        if not self.recurring_radio.isChecked() and not self.transient_radio.isChecked() and not self.antitask_radio.isChecked():
            for radio_button in [self.radio_button_cancellation, self.radio_button_visit, self.radio_button_shopping, self.radio_button_appointment]:
                if not radio_button.isVisible():
                    radio_button.setChecked(False)

    def unselect_types(self):
        if not self.recurring_radio.isChecked() or not self.transient_radio.isChecked() or not self.antitask_radio.isChecked():
            self.type_radio_buttons.setExclusive(False)
            for button in self.type_radio_buttons.buttons():
                button.setChecked(False)
            self.type_radio_buttons.setExclusive(True)

    def handle_type_selection(self, checked):
        if checked:
            for radio_button in self.type_radio_buttons.buttons():
                if radio_button != self.sender():
                    radio_button.setChecked(False)
