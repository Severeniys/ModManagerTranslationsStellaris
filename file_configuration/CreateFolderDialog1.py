from file_configuration.import_libraries.libraries import *

class CreateFolderDialog1(QDialog):
    def __init__(self, Ogla, text):
        super().__init__()
        self.setWindowIcon(QIcon("TextConverter.ico"))
        self.setWindowTitle(Ogla)
        layout = QVBoxLayout(self)

        # Метка с указанием пути
        path_label = QLabel(text)
        layout.addWidget(path_label)

        # Кнопки "Ок" и "Отмена"
        button_box = QDialogButtonBox()
        ok_button = button_box.addButton(QDialogButtonBox.StandardButton.Ok)
        cancel_button = button_box.addButton(QDialogButtonBox.StandardButton.Cancel)

        # Подключение обработчиков сигналов нажатий на кнопки
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        layout.addWidget(button_box)