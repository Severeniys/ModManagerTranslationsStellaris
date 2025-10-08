from file_configuration.import_libraries.libraries import *

class ErrorMessageBox(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowIcon(QIcon("TextConverter.ico"))        
        self.setWindowTitle("TextConverter")
        self.setIcon(QMessageBox.Icon.Critical)
        self.setText("Ошибка")
        self.setInformativeText(message)
        self.addButton(QPushButton("ОК"), QMessageBox.ButtonRole.AcceptRole)