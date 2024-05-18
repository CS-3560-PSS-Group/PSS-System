from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QButtonGroup, QComboBox,
    QDateEdit, QPushButton, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt
from datetime import datetime

class AddEventWindow(QDialog):
    def __init__(self, viewer, event_details=None):
        super().__init__()
        self.viewer = viewer
        self.event_details = event_details

        self.setWindowTitle("Add Event")
        self.setGeometry(200, 200, 400, 350)

        self.create_widgets()
        self.setup_layout()
        self.connect_signals()
        self.hide_type_options()

    def add_event(self):
        event_name = self.event_name_edit.text()
        start_time = self.start_time_edit.text() + " " + self.start_am_pm.currentText()
        end_time = self.end_time_edit.text() + " " + self.end_am_pm.currentText()
        event_type = [radio.text() for radio in self.type_radio_buttons.buttons() if radio.isChecked()]

        if self.recurring_radio.isChecked():
            selected_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        else:
            selected_days = [radio.text() for radio in self.days_radios if radio.isChecked()]

        if self.recurring_radio.isChecked():
            task_type = "Recurring"
        elif self.transient_radio.isChecked():
            task_type = "Transient"
            selected_days = [radio.text() for radio in self.days_radios if radio.isChecked()]
        elif self.antitask_radio.isChecked():
            task_type = "Antitask"

        new_event = {
            "name": event_name,
            "start": start_time,
            "end": end_time,
            "type": event_type[0] if event_type else None,
            "task_type": task_type,
            "selected_days": selected_days,
            "start_date": self.beginning_date_edit.date().toString(Qt.ISODate),
            "end_date": self.ending_date_edit.date().toString(Qt.ISODate)
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
                item = QTableWidgetItem(event_name)
                item.setTextAlignment(Qt.AlignTop)
                tooltip = f"{event_name}\n{start_time} - {end_time}\nType: {new_event['task_type']} - {new_event['type']}"
                item.setToolTip(tooltip)
                self.viewer.tableWidget.setItem(row, column_index, item)
                if row == start_row_index:
                    self.viewer.tableWidget.setSpan(row, column_index, end_row_index - start_row_index + 1, 1)

        self.accept()

    def create_widgets(self):
        self.event_name_edit = QLineEdit()
        self.start_time_edit = QLineEdit()
        self.end_time_edit = QLineEdit()
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

        self.days_label = QLabel("Select a Day:")
        self.days_radios = [QRadioButton(day) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
        self.days_group = QButtonGroup(self)
        for radio in self.days_radios:
            self.days_group.addButton(radio)
            radio.hide()
        self.days_label.hide()

        self.start_am_pm = QComboBox()
        self.start_am_pm.addItems(["AM", "PM"])
        self.end_am_pm = QComboBox()
        self.end_am_pm.addItems(["AM", "PM"])
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
        self.weekly_radio.toggled.connect(self.toggle_days_selection)

        for radio in self.days_radios:
            radio.toggled.connect(self.ensure_single_selection)

        self.transient_radio.toggled.connect(self.toggle_days_visibility)
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
                self.days_label.hide()
                for radio in self.days_radios:
                    radio.hide()
                    radio.setChecked(False)
            elif sender == self.transient_radio:
                self.days_label.show()
                for radio in self.days_radios:
                    radio.show()
            elif sender == self.antitask_radio:
                pass
            elif sender == self.daily_radio or sender == self.weekly_radio:
                if not self.daily_radio.isChecked() and not self.weekly_radio.isChecked():
                    self.recurring_radio.setChecked(False)
                self.days_label.hide()
                for radio in self.days_radios:
                    radio.hide()
                    radio.setChecked(False)

    def ensure_exclusive_daily_weekly(self, checked):
        sender = self.sender()
        if sender == self.daily_radio and checked:
            self.weekly_radio.setChecked(False)
        elif sender == self.weekly_radio and checked:
            self.daily_radio.setChecked(False)
            self.days_label.show()
            for radio in self.days_radios:
                radio.show()
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
                self.days_label.hide()
                for radio in self.days_radios:
                    radio.hide()
                    radio.setChecked(False)
            self.hide_type_options()

    def toggle_days_visibility(self, checked):
        if checked:
            self.days_label.show()
            for radio in self.days_radios:
                radio.show()
            self.show_transient_types()
        else:
            if self.weekly_radio.isChecked():
                self.days_label.show()
                for radio in self.days_radios:
                    radio.show()
            else:
                self.days_label.hide()
                for radio in self.days_radios:
                    radio.hide()
                self.hide_transient_types()

    def show_transient_types(self):
        self.radio_button_visit.show()
        self.radio_button_shopping.show()
        self.radio_button_appointment.show()

    def hide_transient_types(self):
        self.radio_button_visit.hide()
        self.radio_button_shopping.hide()
        self.radio_button_appointment.hide()

    def ensure_single_selection(self, checked):
        if checked:
            for radio in self.days_radios:
                if radio != self.sender():
                    radio.setChecked(False)

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
        
        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.addWidget(self.recurring_radio)
        checkboxes_layout.addWidget(self.transient_radio)
        checkboxes_layout.addWidget(self.antitask_radio)
        layout.addLayout(checkboxes_layout)

        recurring_options_layout = QHBoxLayout()
        recurring_options_layout.addWidget(self.daily_radio)
        recurring_options_layout.addWidget(self.weekly_radio)
        layout.addLayout(recurring_options_layout)
        
        days_layout = QHBoxLayout()
        days_layout.addWidget(self.days_label)
        for radio in self.days_radios:
            days_layout.addWidget(radio)
        layout.addLayout(days_layout)
        
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
        end_time = self.end_time_edit.text() + " " + self.end_am_pm.currentText()
        selected_days = [radio.text() for radio in self.days_radios if radio.isChecked()]

        if not event_name:
            QMessageBox.warning(self, "Error", "Event Name is required.")
            return False
        if not self.is_valid_time(start_time) or not self.is_valid_time(end_time):
            QMessageBox.warning(self, "Error", "Invalid time format. Please enter time in HH:MM AM/PM format.")
            return False
        if self.transient_radio.isChecked() and not selected_days:
            QMessageBox.warning(self, "Error", "Select a day for the transient task.")
            return False
        return True

    def is_valid_time(self, time_str):
        try:
            datetime.strptime(time_str, "%I:%M %p")
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

    def toggle_days_selection(self, state):
        if state:
            self.days_label.show()
            for radio in self.days_radios:
                radio.show()
        else:
            self.days_label.hide()
            for radio in self.days_radios:
                radio.hide()

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

            for radio in self.days_radios:
                if not radio.isVisible():
                    radio.setChecked(False)

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
