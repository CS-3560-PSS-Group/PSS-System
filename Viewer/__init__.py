from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QSpacerItem,QSizePolicy, QGroupBox, QDateEdit, QPushButton, QHeaderView, 
    QFileDialog, QMessageBox, QLineEdit, QLabel, QDialog, QComboBox,QGridLayout,
    QStackedWidget, QRadioButton, QScrollArea, QDialogButtonBox, QFrame
)
from PyQt5.QtCore import Qt, QDateTime, QDate
from PyQt5.QtGui import QFont

from Viewer.AddEventWindow import AddEventWindow
import json
from datetime import datetime
from Controller import Controller
from Task import Task, AntiTask, RecurringTask, TransientTask

from .MonthView import MonthViewWidget

class Viewer(QWidget):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PSS Schedule Viewer')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.create_search_layout(layout)
        self.create_table_widget()

        self.month_view_widget = MonthViewWidget(self.controller)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.tableWidget)
        self.stacked_widget.addWidget(self.month_view_widget)

        layout.addWidget(self.stacked_widget)

        # radio buttons for choosing between Weekly view vs Monthly+Daily
        groupBox = QGroupBox("Select View")
        groupBox.setAlignment(Qt.AlignCenter)
        groupBoxLayout = QHBoxLayout()

        self.radioBtnWeekly = QRadioButton("Weekly View")
        self.radioBtnMonthly = QRadioButton("Monthly && Daily View")

        self.radioBtnWeekly.setChecked(True)

        self.radioBtnWeekly.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.radioBtnMonthly.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        groupBoxLayout.addWidget(self.radioBtnWeekly)
        groupBoxLayout.addWidget(self.radioBtnMonthly)

        # Set the group box layout
        groupBox.setLayout(groupBoxLayout)

        # Add the group box to the main layout and center it horizontally
        layout.addWidget(groupBox)
        layout.setAlignment(groupBox, Qt.AlignHCenter)

        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.open_add_event_window)
        layout.addWidget(self.add_event_button)

        self.export_button = QPushButton("Export Schedule")
        self.export_button.clicked.connect(self.export_schedule)
        layout.addWidget(self.export_button)

        self.load_button = QPushButton("Load Schedule")
        self.load_button.clicked.connect(self.load_schedule)
        layout.addWidget(self.load_button)

        self.write_button = QPushButton("Write Schedule")
        self.write_button.clicked.connect(self.write_schedule_dialog)
        layout.addWidget(self.write_button)

        self.view_schedule_button = QPushButton("View Schedule")
        self.view_schedule_button.clicked.connect(self.view_schedule_dialog)
        layout.addWidget(self.view_schedule_button)

        self.tableWidget.cellClicked.connect(self.edit_event_details)

    def create_search_layout(self, parent_layout):
        search_layout = QHBoxLayout()
        parent_layout.addLayout(search_layout)

        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self.search_task)
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_task)
        search_layout.addWidget(self.search_button)

    def create_table_widget(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['Time Slot', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.populate_time_slots()

        return self.tableWidget

    def populate_time_slots(self):
        hours = range(0, 24)
        minutes = ['00', '15', '30', '45']
        self.tableWidget.setRowCount(len(hours) * len(minutes))

        for i, hour in enumerate(hours):
            for j, minute in enumerate(minutes):
                hour_12h = (hour % 12) or 12
                am_pm = "AM" if hour < 12 else "PM"
                item = QTableWidgetItem('{}:{:02d} {}'.format(hour_12h, int(minute), am_pm))
                self.tableWidget.setItem(i * len(minutes) + j, 0, item)
                self.tableWidget.setVerticalHeaderItem(i * len(minutes) + j, QTableWidgetItem(''))

    def open_add_event_window(self):
        add_event_window = AddEventWindow(self)
        add_event_window.exec_()

    def search_task(self):
        task_name = self.search_input.text()
        if not task_name:
            QMessageBox.warning(self, "Error", "Please enter a task name to search.")
            return
        task = self.controller.find_task_by_name(task_name)
        if task == None:
            QMessageBox.warning(self, "Error", f'Task with name "{task_name}" does not exist.')

    def edit_event_details(self, row, column):
        item = self.tableWidget.item(row, column)

        if item is not None and item.text():
            event_name = item.text()
            start_time_row = row // 4
            start_time = '{}:{} {}'.format((start_time_row % 12) or 12, (row % 4) * 15, 'AM' if start_time_row < 12 else 'PM')
            end_time_row = (row + self.tableWidget.rowSpan(row, column) - 1) // 4
            end_time = '{}:{} {}'.format((end_time_row % 12) or 12, (row % 4) * 15, 'AM' if end_time_row < 12 else 'PM')
            color = item.background().color()
            selected_day = self.tableWidget.horizontalHeaderItem(column).text()
            description = item.toolTip()

            event_details = {
                "name": event_name,
                "start": start_time,
                "end": end_time,
                "description": description,
                "color": color,
                "selected_days": [selected_day]
            }

            add_event_window = AddEventWindow(self, event_details)
            add_event_window.exec_()

    def export_schedule(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Schedule", "", "Text Files (*.txt)")
        if file_name:
            try:
                self.controller.export_schedule_to_json_file(file_name)
            except:
                QMessageBox.warning(self, "Error", f"Failed to write to {file_name}.")

    def load_schedule(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Schedule", "", "JSON Files (*.json)")
        if file_name: 
            try:
                self.controller.import_schedule_from_json_file(file_name)
                self.refresh_views()
            except Exception as e:
                QMessageBox.warning(self, "Error", f'Failed to load schedule: {str(e)}')

    def write_schedule_dialog(self):
        dialog = WriteScheduleDialog(self, self.controller)
        dialog.exec_()

    def view_schedule_dialog(self):
        dialog = ViewScheduleDialog(self, self.controller)
        dialog.exec_()

    def refresh_views(self):
        self.month_view_widget.updateCells()


class MonthViewWidget(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Month and Year selection layout
        date_selection_layout = QHBoxLayout()

        self.month_combo = QComboBox()
        self.month_combo.addItems(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        self.month_combo.setCurrentIndex(QDate.currentDate().month() - 1)
        self.month_combo.currentIndexChanged.connect(self.update_month_view)
        
        self.year_combo = QComboBox()
        self.year_combo.addItems([str(year) for year in range(1900, 2101)])
        self.year_combo.setCurrentText(str(QDate.currentDate().year()))
        self.year_combo.currentIndexChanged.connect(self.update_month_view)

        date_selection_layout.addWidget(QLabel("Select Month:"))
        date_selection_layout.addWidget(self.month_combo)
        date_selection_layout.addWidget(QLabel("Select Year:"))
        date_selection_layout.addWidget(self.year_combo)

        layout.addLayout(date_selection_layout)

        self.calendar_layout = QGridLayout()
        layout.addLayout(self.calendar_layout)

        self.update_month_view()

    def update_month_view(self):
        # Clear the current calendar view
        for i in reversed(range(self.calendar_layout.count())): 
            widget = self.calendar_layout.itemAt(i).widget()
            if widget is not None: 
                widget.deleteLater()
        
        month = self.month_combo.currentIndex() + 1
        year = int(self.year_combo.currentText())
        first_day = QDate(year, month, 1)
        start_day_of_week = first_day.dayOfWeek()
        days_in_month = first_day.daysInMonth()

        # Fill the calendar grid with days
        day = 1
        for i in range(start_day_of_week - 1, start_day_of_week - 1 + days_in_month):
            date = QDate(year, month, day)
            day_button = QPushButton(str(day))
            day_button.clicked.connect(lambda checked, date=date: self.view_tasks_for_date(date))
            self.calendar_layout.addWidget(day_button, i // 7, i % 7)
            day += 1

    def view_tasks_for_date(self, date):
        date_int = date.year() * 10000 + date.month() * 100 + date.day()
        task_list = self.controller.get_events_within_timeframe(date_int, 1)
        if task_list:
            dialog = ScheduleDialog(self)
            dialog.set_schedule(task_list)
            dialog.exec_()
        else:
            QMessageBox.information(self, "Schedule", "No tasks found.")

class WriteScheduleDialog(QDialog):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Write Schedule")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("File Name:"))
        
        hbox = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        hbox.addWidget(self.file_path_edit)

        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.open_file_dialog)
        hbox.addWidget(browse_button)

        layout.addLayout(hbox)

        self.setLayout(layout)

        layout.addWidget(QLabel("Start Date:"))
        
        self.dateedit = QDateEdit(calendarPopup=True)
        layout.addWidget(self.dateedit)
        self.dateedit.setDateTime(QDateTime.currentDateTime())

        self.schedule_type_combo = QComboBox()
        self.schedule_type_combo.addItems(["Day", "Week", "Month"])
        layout.addWidget(QLabel("Select Schedule Type:"))
        layout.addWidget(self.schedule_type_combo)

        button_layout = QHBoxLayout()
        self.write_button = QPushButton("Write")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.write_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.write_button.clicked.connect(self.write_schedule)
        self.cancel_button.clicked.connect(self.reject)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.file_path_edit.setText(file_path)


    def write_schedule(self):
        file_name = self.file_path_edit.text()
        date = self.dateedit.date()
        date_int = date.year() * 10000 + date.month() * 100 + date.day()
        schedule_type = self.schedule_type_combo.currentText()

        self.controller.write_schedule(file_name, date_int, schedule_type)
        
        self.accept()

class ViewScheduleDialog(QDialog):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("View Schedule")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Start Date:"))

        self.dateedit = QDateEdit(calendarPopup=True)
        layout.addWidget(self.dateedit)
        self.dateedit.setDateTime(QDateTime.currentDateTime())

        self.schedule_type_combo = QComboBox()
        self.schedule_type_combo.addItems(["Day", "Week", "Month"])
        layout.addWidget(QLabel("Select Schedule Type:"))
        layout.addWidget(self.schedule_type_combo)

        button_layout = QHBoxLayout()
        self.view_schedule_button = QPushButton("View")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.view_schedule_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.view_schedule_button.clicked.connect(self.view_schedule)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)

    def view_schedule(self):
        schedule_type = self.schedule_type_combo.currentText()
        date = self.dateedit.date()
        date_int = date.year() * 10000 + date.month() * 100 + date.day()

        if schedule_type == "Day":
            timeframe = 1
        elif schedule_type == "Week":
            timeframe = 7
        elif schedule_type == "Month":
            timeframe = 30
        else:
            timeframe = 1  # Default to day if the schedule type is not recognized

        task_list = self.controller.get_events_within_timeframe(date_int, timeframe)
        if task_list:
            dialog = ScheduleDialog(self)
            dialog.set_schedule(task_list)
            dialog.exec_()
        else:
            QMessageBox.information(self, "Schedule", "No tasks found.")

class ScheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout(self)

        # Create a table widget
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # Set table properties
        self.table_widget.setColumnCount(5)  # Number of columns
        self.table_widget.setHorizontalHeaderLabels(["Name", "Type", "Date", "Start Time", "Duration"])

        # Set up the horizontal header
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setStyleSheet("QHeaderView::section { border-bottom: 1px solid black; }")

        # Create buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

    def set_schedule(self, task_list):
        self.table_widget.setRowCount(len(task_list))
        
        for row, event in enumerate(task_list):
            task = event.task
            date_str = QDate.fromString(str(event.start_date), "yyyyMMdd").toString("MM/dd/yyyy")  # Convert date to MM/DD/YYYY format
            self.table_widget.setItem(row, 0, QTableWidgetItem(task.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(task.task_type))
            self.table_widget.setItem(row, 2, QTableWidgetItem(date_str)) 
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(event.start_time)))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(event.duration)))

          # Set up the horizontal header
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Add style sheet to create a line under the header
        header.setStyleSheet("QHeaderView::section { border-bottom: 1px solid black; }")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    viewer = Viewer()
    viewer.show()
    sys.exit(app.exec_())
