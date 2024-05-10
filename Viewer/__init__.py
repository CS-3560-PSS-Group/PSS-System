from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView
)
from PyQt5.QtCore import Qt
from Viewer.AddEventWindow import AddEventWindow


class Viewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PSS Schedule Viewer')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.create_table_widget(layout)

        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.open_add_event_window)
        layout.addWidget(self.add_event_button)

        self.tableWidget.cellClicked.connect(self.edit_event_details)

    def create_table_widget(self, layout):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['Time Slot', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.tableWidget)

        self.populate_time_slots()

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

            # Include start and end dates
            start_date = add_event_window.beginning_date_edit.date().toString(Qt.ISODate)
            end_date = add_event_window.ending_date_edit.date().toString(Qt.ISODate)

            # Include recurring and transient checkbox states
            is_recurring = add_event_window.recurring_checkbox.isChecked()
            is_transient = add_event_window.transient_checkbox.isChecked()

            event_details = {
                "name": event_name,
                "start": start_time,
                "end": end_time,
                "description": description,
                "color": color,
                "selected_days": [selected_day],
                "start_date": start_date,
                "end_date": end_date,
                "is_recurring": is_recurring,
                "is_transient": is_transient
            }

            add_event_window = AddEventWindow(self, event_details)
            add_event_window.exec_()


