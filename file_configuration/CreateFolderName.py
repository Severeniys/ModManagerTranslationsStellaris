from file_configuration.import_libraries.libraries import *

class CreateFolderName(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon("TextConverter.ico"))
        self.setWindowTitle("TextConverter")
        layout = QVBoxLayout(self)

        # Метка с указанием пути
        path_label = QLabel("Переименовать")
        layout.addWidget(path_label)

        # Поле ввода с именем папки
        self.folder_name_input = QLineEdit()
        layout.addWidget(self.folder_name_input)

        # Кнопки "Ок" и "Отмена"
        button_box = QDialogButtonBox()
        ok_button = button_box.addButton(QDialogButtonBox.StandardButton.Ok)
        cancel_button = button_box.addButton(QDialogButtonBox.StandardButton.Cancel)

        # Подключение обработчиков сигналов нажатий на кнопки
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        layout.addWidget(button_box)