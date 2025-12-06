import sys
import os


from PyQt6.QtGui import (
    QIcon
)
from PyQt6.QtWidgets import (    
    QMessageBox,
    QPushButton    
)


from file_configuration.constants import ProcessingConstants
from file_configuration.utils import log_debug, log_error, log_info, log_warning

class ErrorMessageBox(QMessageBox):
    def __init__(self, message: str, title: str = "TextConverter", icon_path: str = None, icon: QMessageBox.Icon = QMessageBox.Icon.Critical):
        super().__init__()

        if getattr(sys, 'frozen', False):
            self.base_resources_path = sys._MEIPASS
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.base_resources_path = os.path.abspath(os.path.join(current_dir, '..')) 

        if icon_path is None: 
            icon_path = os.path.join(self.base_resources_path, "file_configuration", "resources", ProcessingConstants.APP_ICON_NAME)      
        
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            log_debug(f"Предупреждение: Главный значок приложения не найден по адресу {icon_path}")
        
        self.setWindowTitle(title)
        self.setIcon(icon)
        self.setText("Ошибка" if icon == QMessageBox.Icon.Critical else "Внимание" if icon == QMessageBox.Icon.Warning else "Информация") 
        self.setInformativeText(message)
        self.addButton(QPushButton("ОК"), QMessageBox.ButtonRole.AcceptRole)

    @staticmethod
    def show_error(message: str, title: str = "Ошибка", icon_path: str = None):
        """Показывает стандартное окно ошибки."""
        msg_box = ErrorMessageBox(message, title=title, icon_path=icon_path, icon=QMessageBox.Icon.Critical)
        msg_box.exec()

    @staticmethod
    def show_warning(message: str, title: str = "Внимание", icon_path: str = None):
        """Показывает стандартное окно предупреждения."""
        msg_box = ErrorMessageBox(message, title=title, icon_path=icon_path, icon=QMessageBox.Icon.Warning)
        msg_box.exec()

    @staticmethod
    def show_info(message: str, title: str = "Информация", icon_path: str = None):
        """Показывает стандартное информационное окно."""
        msg_box = ErrorMessageBox(message, title=title, icon_path=icon_path, icon=QMessageBox.Icon.Information)
        msg_box.exec()