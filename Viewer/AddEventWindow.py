from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QLabel, QComboBox, QHBoxLayout,
    QDialog, QCheckBox, QColorDialog, QPlainTextEdit, QErrorMessage, QDateEdit,
    QMessageBox, QCalendarWidget, QRadioButton, QButtonGroup
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

        self.create_widgets()
        self.setup_layout()

        self.daily_checkbox.stateChanged.connect(self.ensure_exclusive_selection)
        self.weekly_checkbox.stateChanged.connect(self.ensure_exclusive_selection)

        self.hide_type_options()
        self.recurring_checkbox.stateChanged.connect(self.toggle_type_options_visibility)

        self.transient_checkbox.stateChanged.connect(self.toggle_days_visibility)
        self.antitask_checkbox.stateChanged.connect(self.toggle_antitask_type_visibility)

        for checkbox in self.days_checkboxes:
            checkbox.toggled.connect(self.ensure_single_selection)

        self.update_visibility_on_uncheck()

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

        for radio_button in self.type_radio_buttons.buttons():
            radio_button.toggled.connect(self.handle_type_selection)


    def create_widgets(self):
        # Replace description_edit with type_radio_buttons
        self.event_name_edit = QLineEdit()
        self.start_time_edit = QLineEdit()
        self.end_time_edit = QLineEdit()
        self.type_radio_buttons = QButtonGroup(self)  # Group for radio buttons
        self.color_button = QColorButton()
        self.recurring_checkbox = QCheckBox("Recurring")
        self.daily_checkbox = QCheckBox("Daily")  
        self.weekly_checkbox = QCheckBox("Weekly")  
        self.transient_checkbox = QCheckBox("Transient")  
        self.antitask_checkbox = QCheckBox("Antitask")  
        self.transient_checkbox.stateChanged.connect(self.toggle_days_visibility)
        self.daily_checkbox.hide()  
        self.weekly_checkbox.hide()  
        self.days_layout = QHBoxLayout()
        self.days_checkboxes = [
            QCheckBox(day) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ]
        self.days_label = QLabel("Select a Day:")
        self.days_label.hide()  
        for checkbox in self.days_checkboxes:
            checkbox.hide()  

        self.start_am_pm = QComboBox()
        self.start_am_pm.addItems(["AM", "PM"])
        self.end_am_pm = QComboBox()
        self.end_am_pm.addItems(["AM", "PM"])
        self.beginning_date_edit = QDateEdit()
        self.ending_date_edit = QDateEdit()
        self.add_button = QPushButton("Add")
        self.cancel_button = QPushButton("Cancel")

        self.recurring_checkbox.stateChanged.connect(self.toggle_recurring_options)
        self.weekly_checkbox.stateChanged.connect(self.toggle_days_selection)
        self.add_button.clicked.connect(self.add_or_save_event)
        self.cancel_button.clicked.connect(self.reject)

        # Add radio buttons for type selection
        self.radio_button_daily = QRadioButton("Daily")
        self.radio_button_weekly = QRadioButton("Weekly")
        self.radio_button_transient = QRadioButton("Transient")
        self.radio_button_antitask = QRadioButton("Antitask")
        self.type_radio_buttons.addButton(self.radio_button_daily)  
        self.type_radio_buttons.addButton(self.radio_button_weekly)  
        self.type_radio_buttons.addButton(self.radio_button_transient)  
        self.type_radio_buttons.addButton(self.radio_button_antitask) 

        self.radio_button_class = QRadioButton("Class")
        self.radio_button_study = QRadioButton("Study")
        self.radio_button_sleep = QRadioButton("Sleep")
        self.radio_button_exercise = QRadioButton("Exercise")
        self.radio_button_work = QRadioButton("Work")
        self.radio_button_meal = QRadioButton("Meal")

        # Add transient type radio buttons
        self.radio_button_visit = QRadioButton("Visit")
        self.radio_button_shopping = QRadioButton("Shopping")
        self.radio_button_appointment = QRadioButton("Appointment")

        # Initialize button group for transient types
        self.type_radio_transient_buttons = QButtonGroup(self)

        # Add transient type radio buttons to button group
        self.type_radio_transient_buttons.addButton(self.radio_button_visit)
        self.type_radio_transient_buttons.addButton(self.radio_button_shopping)
        self.type_radio_transient_buttons.addButton(self.radio_button_appointment)

        # Hide transient type radio buttons initially
        self.radio_button_visit.hide()
        self.radio_button_shopping.hide()
        self.radio_button_appointment.hide()

        # Add antitask type radio buttons
        self.radio_button_cancellation = QRadioButton("Cancellation")
        self.type_radio_antitask_buttons = QButtonGroup(self)
        self.type_radio_antitask_buttons.addButton(self.radio_button_cancellation)
        self.radio_button_cancellation.hide()

        self.recurring_checkbox.stateChanged.connect(self.unselect_types)
        self.transient_checkbox.stateChanged.connect(self.unselect_types)
        self.antitask_checkbox.stateChanged.connect(self.unselect_types)

        


    def update_visibility_on_uncheck(self):
        # Connect the toggled signal of each checkbox to the corresponding method
        self.recurring_checkbox.toggled.connect(self.clear_if_unchecked)
        self.transient_checkbox.toggled.connect(self.clear_if_unchecked)
        self.antitask_checkbox.toggled.connect(self.clear_if_unchecked)
        self.daily_checkbox.toggled.connect(self.clear_if_unchecked)
        self.weekly_checkbox.toggled.connect(self.clear_if_unchecked)


    def clear_if_unchecked(self, checked):
        # If the sender is not checked anymore, clear the corresponding widgets
        if not checked:
            sender = self.sender()
            if sender == self.recurring_checkbox:
                self.hide_type_options()
            elif sender == self.transient_checkbox:
                self.toggle_days_visibility(Qt.Unchecked)
            elif sender == self.antitask_checkbox:
                pass  # Placeholder for any other actions you want to perform
            elif sender == self.daily_checkbox or sender == self.weekly_checkbox:
                self.days_label.hide()
                for checkbox in self.days_checkboxes:
                    checkbox.hide()
                    checkbox.setChecked(False)  # Uncheck the checkboxes

                
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
        
        # Add the checkboxes layout above the description
        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.addWidget(self.recurring_checkbox)
        checkboxes_layout.addWidget(self.transient_checkbox)  
        checkboxes_layout.addWidget(self.antitask_checkbox)  
        layout.addLayout(checkboxes_layout)

        # Add the daily and weekly checkboxes in a row below recurring checkbox
        recurring_options_layout = QHBoxLayout()
        recurring_options_layout.addWidget(self.daily_checkbox)
        recurring_options_layout.addWidget(self.weekly_checkbox)
        layout.addLayout(recurring_options_layout)
        
        # Add the days label and checkboxes below the transient, antitask checkboxes
        days_layout = QHBoxLayout()
        days_layout.addWidget(self.days_label)
        for checkbox in self.days_checkboxes:
            days_layout.addWidget(checkbox)
        layout.addLayout(days_layout)
        
        # Add the "Type:" label
        layout.addWidget(QLabel("Type:"))

        # Add a layout for type selection
        type_selection_layout = QVBoxLayout()

        # Add the radio buttons for transient types
        type_selection_layout.addWidget(self.radio_button_class)
        type_selection_layout.addWidget(self.radio_button_study)
        type_selection_layout.addWidget(self.radio_button_sleep)
        type_selection_layout.addWidget(self.radio_button_exercise)
        type_selection_layout.addWidget(self.radio_button_work)
        type_selection_layout.addWidget(self.radio_button_meal)

        # Add the radio buttons for cancellation type
        type_selection_layout.addWidget(self.radio_button_cancellation)

        # Add the radio buttons for transient types
        type_selection_layout.addWidget(self.radio_button_visit)
        type_selection_layout.addWidget(self.radio_button_shopping)
        type_selection_layout.addWidget(self.radio_button_appointment)

        layout.addLayout(type_selection_layout)

        layout.addWidget(QLabel("Color:"))
        layout.addWidget(self.color_button)

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

    def toggle_days_visibility(self, state):
        if state == Qt.Checked:  # If transient checkbox is checked
            self.days_label.hide()
            for checkbox in self.days_checkboxes:
                checkbox.hide()
            self.show_transient_types()
        else:  # If transient checkbox is unchecked
            if self.weekly_checkbox.isChecked():  # Only show if weekly checkbox is checked
                self.days_label.show()
                for checkbox in self.days_checkboxes:
                    checkbox.show()
            else:
                self.days_label.hide()
                for checkbox in self.days_checkboxes:
                    checkbox.hide()
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
        # Uncheck all other checkboxes if one is checked
        if checked:
            for checkbox in self.days_checkboxes:
                if checkbox != self.sender():
                    checkbox.setChecked(False)

    def ensure_exclusive_selection(self, state):
        # If daily checkbox is checked, uncheck weekly checkbox
        if self.daily_checkbox.isChecked() and self.weekly_checkbox.isChecked():
            self.weekly_checkbox.setChecked(False)
        
        # If weekly checkbox is checked, uncheck daily checkbox
        if self.weekly_checkbox.isChecked() and self.daily_checkbox.isChecked():
            self.daily_checkbox.setChecked(False)

    def update_type_options(self):
        # Clear existing radio buttons in the button group
        self.type_radio_buttons.buttons()

        # Check if Recurring checkbox is checked
        if self.recurring_checkbox.isChecked():
            # Add Type options for recurring events
            self.type_radio_buttons.addButton(self.radio_button_class)
            self.type_radio_buttons.addButton(self.radio_button_study)
            self.type_radio_buttons.addButton(self.radio_button_sleep)
            self.type_radio_buttons.addButton(self.radio_button_exercise)
            self.type_radio_buttons.addButton(self.radio_button_work)
            self.type_radio_buttons.addButton(self.radio_button_meal)
        else:
            # Add default Type option for non-recurring events
            self.type_radio_buttons.addButton(self.radio_button_meal)

        # Set the first radio button as default checked
        self.type_radio_buttons.buttons()[0].setChecked(True)
    
    def toggle_type_options_visibility(self, state):
        # Show or hide the radio buttons for Type options based on the state of the recurring_checkbox
        if state == Qt.Checked:
            self.show_type_options()
        else:
            self.hide_type_options()
    
    def hide_type_options(self):
        # Hide the radio buttons for Type options
        self.radio_button_class.hide()
        self.radio_button_study.hide()
        self.radio_button_sleep.hide()
        self.radio_button_exercise.hide()
        self.radio_button_work.hide()
        self.radio_button_meal.hide()

    def show_type_options(self):
        # Show the radio buttons for Type options
        self.radio_button_class.show()
        self.radio_button_study.show()
        self.radio_button_sleep.show()
        self.radio_button_exercise.show()
        self.radio_button_work.show()
        self.radio_button_meal.show()

    def toggle_recurring_options(self, state):
        # If recurring checkbox is checked, show daily and weekly checkboxes
        if state == Qt.Checked:
            self.daily_checkbox.show()
            self.weekly_checkbox.show()
        else:
            # If recurring checkbox is unchecked, hide daily and weekly checkboxes
            self.daily_checkbox.hide()
            self.weekly_checkbox.hide()
            # Also hide the days label and checkboxes
            self.days_label.hide()
            for checkbox in self.days_checkboxes:
                checkbox.hide()
    
    def toggle_transient_types_visibility(self, state):
        # If transient checkbox is checked, show transient type radio buttons
        if state == Qt.Checked:
            self.radio_button_visit.show()
            self.radio_button_shopping.show()
            self.radio_button_appointment.show()
        else:
            # If transient checkbox is unchecked, hide transient type radio buttons
            self.radio_button_visit.hide()
            self.radio_button_shopping.hide()
            self.radio_button_appointment.hide()

    def toggle_days_selection(self, state):
        # If weekly checkbox is checked, show the days label and checkboxes
        if state == Qt.Checked:
            self.days_label.show()
            for checkbox in self.days_checkboxes:
                checkbox.show()
        else:
            # If weekly checkbox is unchecked, hide the days label and checkboxes
            self.days_label.hide()
            for checkbox in self.days_checkboxes:
                checkbox.hide()

    def toggle_antitask_type_visibility(self, state):
        # If antitask checkbox is checked, show antitask type radio buttons
        if state == Qt.Checked:
            self.show_antitask_type_options()
        else:
            # If antitask checkbox is unchecked, hide antitask type radio buttons
            self.hide_antitask_type_options()

    def show_antitask_type_options(self):
        self.radio_button_cancellation.show()

    def hide_antitask_type_options(self):
        self.radio_button_cancellation.hide()

    def clear_hidden_selections(self):
        # If all checkboxes are unchecked
        if not self.recurring_checkbox.isChecked() and not self.transient_checkbox.isChecked() and not self.antitask_checkbox.isChecked():
            # Clear the selection of invisible radio buttons
            for radio_button in [self.radio_button_cancellation, self.radio_button_visit, self.radio_button_shopping, self.radio_button_appointment]:
                if not radio_button.isVisible():
                    radio_button.setChecked(False)

            # Clear the selection of invisible checkboxes
            for checkbox in self.days_checkboxes:
                if not checkbox.isVisible():
                    checkbox.setChecked(False)


    def unselect_types(self):
        if not self.recurring_checkbox.isChecked() or not self.transient_checkbox.isChecked() or not self.antitask_checkbox.isChecked():
            # Unselect all types
            self.type_radio_buttons.setExclusive(False)
            for button in self.type_radio_buttons.buttons():
                button.setChecked(False)
            self.type_radio_buttons.setExclusive(True)

    def handle_type_selection(self, checked):
        # Uncheck all other radio buttons if one is checked
        if checked:
            for radio_button in self.type_radio_buttons.buttons():
                if radio_button != self.sender():
                    radio_button.setChecked(False)