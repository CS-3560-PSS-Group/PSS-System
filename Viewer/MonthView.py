from PyQt5.QtWidgets import QApplication, QCalendarWidget, QWidget, QVBoxLayout#, QTextCharFormat
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import random

class MonthViewWidget(QCalendarWidget):
    def __init__(self, controller, parent=None):
        super(MonthViewWidget, self).__init__(parent, gridVisible=False,
            #horizontalHeaderFormat=QtWidgets.QCalendarWidget.SingleLetterDayNames,
            verticalHeaderFormat=QtWidgets.QCalendarWidget.NoVerticalHeader,
            navigationBarVisible=True,
            dateEditEnabled=True)       
        self.controller = controller
        self.setEnabled(True)
        self.setGeometry(QtCore.QRect(0, 0, 320, 250))
        self.clicked.connect(print)

        self.table_view = self.findChild(QtWidgets.QTableView, "qt_calendar_calendarview")
        self.table_view.viewport().installEventFilter(self)
        self.setFirstDayOfWeek(QtCore.Qt.Monday)
        f = QTextCharFormat()
        f.setForeground(Qt.black)
        self.setWeekdayTextFormat(Qt.Saturday, f)
        self.setWeekdayTextFormat(Qt.Sunday, f)

    def referenceDate(self):
        refDay = 1
        while refDay <= 31:
            refDate = QtCore.QDate(self.yearShown(), self.monthShown(), refDay)
            if refDate.isValid(): return refDate
            refDay += 1
        return QtCore.QDate()

    def columnForDayOfWeek(self, day):
        m_firstColumn = 1 if self.verticalHeaderFormat() != QtWidgets.QCalendarWidget.NoVerticalHeader else 0
        if day < 1 or day > 7: return -1
        column = day - int(self.firstDayOfWeek())
        if column < 0:
            column += 7
        return column + m_firstColumn

    def columnForFirstOfMonth(self, date):
        return (self.columnForDayOfWeek(date.dayOfWeek()) - (date.day() % 7) + 8) % 7

    def dateForCell(self, row, column):
        m_firstRow = 1 if self.horizontalHeaderFormat() != QtWidgets.QCalendarWidget.NoHorizontalHeader else 0
        m_firstColumn = 1 if self.verticalHeaderFormat() != QtWidgets.QCalendarWidget.NoVerticalHeader else 0
        rowCount = 6
        columnCount = 7
        if row < m_firstRow or row > (m_firstRow + rowCount -1) or column < m_firstColumn or column > (m_firstColumn + columnCount -1):
            return QtCore.QDate()
        refDate = self.referenceDate()
        if not refDate.isValid():
            return QtCore.QDate()
        columnForFirstOfShownMonth = self.columnForFirstOfMonth(refDate)
        if (columnForFirstOfShownMonth - m_firstColumn) < 1:
            row -= 1
        requestedDay = 7*(row - m_firstRow) +  column  - columnForFirstOfShownMonth - refDate.day() + 1
        return refDate.addDays(requestedDay)

    def eventFilter(self, obj, event):
        if obj is self.table_view.viewport() and event.type() == QtCore.QEvent.MouseButtonPress:    
            ix = self.table_view.indexAt(event.pos())
            date = self.dateForCell(ix.row(), ix.column())
            d_start = QtCore.QDate(self.yearShown(), self.monthShown(), 1)
            d_end = QtCore.QDate(self.yearShown(), self.monthShown(), d_start.daysInMonth())
            if d_start > date or date > d_end:
                return True
        return super(MonthViewWidget, self).eventFilter(obj, event)

    def paintCell(self, painter, rect, date):
        d_start = QtCore.QDate(self.yearShown(), self.monthShown(), 1)
        d_end = QtCore.QDate(self.yearShown(), self.monthShown(), d_start.daysInMonth())
        if d_start <= date <= d_end:
            #super(MonthViewWidget, self).paintCell(painter, rect, date)
            date_int = date.year() * 10000 + date.month() * 100 + date.day()
            events = self.controller.get_events_within_timeframe(date_int, 1) # get all events on this day
            if len(events) > 0:
                painter.fillRect(rect, Qt.yellow)
            painter.drawText(rect, Qt.AlignCenter, str(date.day()))

            