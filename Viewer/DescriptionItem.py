from PyQt5.QtWidgets import QTableWidgetItem

class DescriptionItem(QTableWidgetItem):
    def __init__(self, description_widget):
        super().__init__()
        self.description_widget = description_widget

    def get_description(self):
        if self.description_widget:
            if hasattr(self.description_widget, "toPlainText"):
                return self.description_widget.toPlainText()
            elif hasattr(self.description_widget, "text"):
                return self.description_widget.text()
        return ""
