import os
import sys

from PyQt6.QtGui import (
    QIcon, 
)
from PyQt6.QtWidgets import (    
    QVBoxLayout, 
    QDialog, 
    QLabel,
    QDialogButtonBox,
    QLineEdit
)

from file_configuration.utils import log_debug, log_error, log_info, log_warning

class CreateFolderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        if getattr(sys, 'frozen', False): 
            self.base_resources_path = sys._MEIPASS
        else:            
            self.base_resources_path = os.path.dirname(os.path.abspath(__file__))
            self.base_resources_path = os.path.dirname(self.base_resources_path) # Поднимаемся на 1 уровень

        main_icon_path = os.path.join(self.base_resources_path, "file_configuration", "resources", "ModManagerTranslationsStellaris.ico") 

        if os.path.exists(main_icon_path):
            self.setWindowIcon(QIcon(main_icon_path))
        else:
            log_debug(f"Предупреждение: Главный значок приложения не найден по адресу {main_icon_path}")
        self.setWindowTitle("ModManagerTranslationsStellaris")
        layout = QVBoxLayout(self)

        # Метка с указанием пути
        path_label = QLabel("Имя сборки:")
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