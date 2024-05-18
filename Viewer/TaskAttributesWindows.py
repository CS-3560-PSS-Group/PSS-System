from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QSpacerItem,QSizePolicy, QGroupBox, QDateEdit, QPushButton, QHeaderView, 
    QFileDialog, QMessageBox, QLineEdit, QLabel, QDialog, QComboBox,QGridLayout,
    QStackedWidget, QRadioButton, QScrollArea, QDialogButtonBox, QFrame, QTextEdit
)

from PyQt5.QtCore import QDate


#def show_add_task():
from Task import Task, RecurringTask, TransientTask, AntiTask, Event
    
def show_task_attributes_dialog(task, controller, viewer):
    dialog = TaskAttributesDialog(task, controller, viewer)
    dialog.exec_()

class TaskAttributesDialog(QDialog):
    def __init__(self, task: Task, controller, viewer, parent=None):
        super().__init__(parent)
        self.setGeometry(200, 200, 600, 400)
        self.task = task
        self.controller = controller
        self.viewer = viewer
        self.build_layout()

        button_layout = QHBoxLayout()
        if task == None: # then this is for adding a task
            self.setWindowTitle("Add Task")
            add_button = QPushButton("Add")
            add_button.clicked.connect(self.on_add_clicked)
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(self.on_close_clicked)

            button_layout.addWidget(add_button)
            button_layout.addWidget(cancel_button)

        else:
            self.setWindowTitle("View Existing Task")
            self.populate_fields()

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(self.on_edit_clicked)
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(self.on_delete_clicked)
            close_button = QPushButton("Close")
            close_button.clicked.connect(self.on_close_clicked)

            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            button_layout.addWidget(close_button)

        self.layout.addLayout(button_layout)


        
    def build_layout(self):
        self.layout = layout = QVBoxLayout(self)

        self.name_label = QLabel("Task Name")
        layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # ====  User choose between recurring/transient/anti ====
        radio_layout = QHBoxLayout()
        self.recurring_radio = QRadioButton('Recurring')
        self.transient_radio = QRadioButton('Transient')
        self.anti_radio = QRadioButton('Anti-Task')
        self.recurring_radio.setChecked(True) # default selection
        self.recurring_radio.toggled.connect(self.radio_button_selected)
        self.transient_radio.toggled.connect(self.radio_button_selected)
        self.anti_radio.toggled.connect(self.radio_button_selected)

        radio_layout.addWidget(self.recurring_radio)
        radio_layout.addWidget(self.transient_radio)
        radio_layout.addWidget(self.anti_radio)

        

        layout.addLayout(radio_layout)

        
        self.task_type_label = QLabel("Task Type")
        layout.addWidget(self.task_type_label)

        self.task_type_dropdown = QComboBox()
        layout.addWidget(self.task_type_dropdown)
        self.setDropdownItems(0)


        time_row = QHBoxLayout()
        self.start_time_label = QLabel("Start Time (HH:MM)")
        time_row.addWidget(self.start_time_label)
        self.start_time_input = QLineEdit()
        time_row.addWidget(self.start_time_input)
        self.am_pm_combo = QComboBox()
        self.am_pm_combo.addItem("AM")
        self.am_pm_combo.addItem("PM")
        time_row.addWidget(self.am_pm_combo)
        layout.addLayout(time_row)


        duration_row = QHBoxLayout()
        self.duration_label = QLabel("Duration (HH:MM)")
        duration_row.addWidget(self.duration_label)
        self.duration_input = QLineEdit()
        duration_row.addWidget(self.duration_input)
        layout.addLayout(duration_row)



        self.start_date_row = QHBoxLayout()
        self.start_date_label = QLabel("Start Date")
        self.start_date_row.addWidget(self.start_date_label)
        self.start_date_picker = QDateEdit()
        self.start_date_picker.setCalendarPopup(True)  # Enable calendar popup
        self.start_date_row.addWidget(self.start_date_picker)
        layout.addLayout(self.start_date_row)

        self.recurring_extras_widget = QWidget()
        vert = QVBoxLayout()
        self.end_date_row = QHBoxLayout()
        self.end_date_label = QLabel("End Date")
        self.end_date_row.addWidget(self.end_date_label)
        self.end_date_picker = QDateEdit()
        self.end_date_picker.setCalendarPopup(True)  # Enable calendar popup
        self.end_date_row.addWidget(self.end_date_picker)
       
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItem("Daily")
        self.frequency_combo.addItem("Weekly")

        vert.addWidget(self.frequency_combo)
        vert.addLayout(self.end_date_row)
        
        self.recurring_extras_widget.setLayout(vert)
        #self.recurring_extras_widget.
        layout.addWidget(self.recurring_extras_widget)
        

    
    def setDropdownItems(self, task_type):
        items = []
        if task_type == 0:
            items = ["Class", "Study", "Sleep", "Exercise", "Work", "Meal"]
        elif task_type == 1:
            items = ["Visit", "Shopping", "Appointment"]
        elif task_type == 2:
            items = ["Cancellation"]

        self.task_type_dropdown.clear()
        self.task_type_dropdown.addItems(items)

    def radio_button_selected(self):
        sender = self.sender()
        if sender.isChecked():  # 
            if sender.text() == "Recurring":
                self.setDropdownItems(0)
                self.recurring_extras_widget.setVisible(True)
            elif sender.text() == "Transient":
                self.setDropdownItems(1)
                self.recurring_extras_widget.setVisible(False)
            else:
                self.setDropdownItems(2)
                self.recurring_extras_widget.setVisible(False)
            #print(f"{sender.text()} selected")

    def populate_fields(self):
        task = self.task
        self.name_input.setText(task.name) 
        if type(task) is RecurringTask:
            self.recurring_radio.setChecked(True) 
            self.frequency_combo.setCurrentText("Daily" if task.frequency == 1 else "Weekly")
            self.end_date_picker.setDate(getQDateFromInt(task.end_date))
        elif type(task) is TransientTask:
            self.transient_radio.setChecked(True) 
        elif type(task) is AntiTask:
            self.anti_radio.setChecked(True) 

        self.task_type_dropdown.setCurrentText(task.task_type)

        start_time, start_time_ampm = float_to_time_ampm(task.start_time)
        self.start_time_input.setText(start_time)
        self.am_pm_combo.setCurrentText(start_time_ampm)

        self.duration_input.setText(float_to_time_string(task.duration))

        self.start_date_picker.setDate(getQDateFromInt(task.start_date))



    # build a task from the data in the form
    def build_task(self) -> Task:
        name = self.name_input.text()
        task_type = self.task_type_dropdown.currentText()
        start_date = int(self.start_date_picker.date().toString("yyyyMMdd"))
        end_date = int(self.end_date_picker.date().toString("yyyyMMdd"))
        start_time = time_ampm_to_float(self.start_time_input.text(), self.am_pm_combo.currentText())
        frequency = 1 if self.frequency_combo.currentText() == "Daily" else 7
        duration = time_string_to_float(self.duration_input.text())

        if self.recurring_radio.isChecked():
            task = RecurringTask(name, task_type, start_date, start_time, duration, end_date, frequency)
        elif self.transient_radio.isChecked():
            task = TransientTask(name, task_type, start_date, start_time, duration)
        else:
            task = AntiTask(name, task_type, start_date, start_time, duration)
        return task

    def on_add_clicked(self):
        task = self.build_task()
        self.handle_error_before_close(lambda: self.controller.add_task(task))

    def on_close_clicked(self):
        self.accept()

    def on_edit_clicked(self):
        task = self.build_task()
        self.handle_error_before_close(lambda: self.controller.edit_task(self.task.name, task))

    def on_delete_clicked(self):
        #task = self.build_task()
        self.handle_error_before_close(lambda: self.controller.delete_task(self.task.name))

    def handle_error_before_close(self, func):
        try:
            func()
            self.viewer.refresh_views()
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


def getQDateFromInt(date_as_int):
    # Extract year, month, and day from the integer
    year = date_as_int // 10000
    month = (date_as_int // 100) % 100
    day = date_as_int % 100

    # Return QDate object
    return QDate(year, month, day)

def float_to_time_string(float_time):
    hours = int(float_time)
    minutes = int((float_time - hours) * 100)  # Multiply by 100 to get minutes

    return f"{hours}:{minutes:02d}"

def time_string_to_float(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours + (minutes / 100)

def float_to_time_ampm(float_time):
    hours = int(float_time)
    minutes = int((float_time - hours) * 100)  # Multiply by 100 to get minutes

    # Convert hours to 12-hour format and determine AM/PM
    am_pm = 'AM' if hours < 12 else 'PM'
    if hours == 0:
        hours = 12
    elif hours > 12:
        hours -= 12

    return f"{hours}:{minutes:02d}", am_pm

def time_ampm_to_float(time_str, am_pm):
    hours, minutes = map(int, time_str.split(":"))

    # Convert hours to 24-hour format if PM
    if am_pm == 'PM' and hours != 12:
        hours += 12

    return hours + (minutes / 100)


'''
class TaskAttributesUI():
    def __init__(self, task):
        #if task != None:
        self.layout = self.build_layout()
'''
         