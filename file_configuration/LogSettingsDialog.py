# file_configuration/LogSettingsDialog

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QCheckBox,
    QDialogButtonBox,
    QLabel    
)
from PyQt6.QtCore import pyqtSignal, QSize, QSettings
from PyQt6.QtGui import QFont # Импортируем QFont

class LogSettingsDialog(QDialog):
    """Диалоговое окно для настройки уровней логирования."""
    
    # Сигналы для изменения состояния логов
    debug_changed = pyqtSignal(bool)
    info_changed = pyqtSignal(bool)
    warning_changed = pyqtSignal(bool)
    error_changed = pyqtSignal(bool)
    
    def sizeHint(self):
        """
        Предлагает предпочитаемый размер для диалога.
        """
        # Возвращаем QSize с шириной и высотой
        return QSize(350, 250) # Ширина 350px, Высота 250px

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки логирования")
        self.setModal(True)
        
        # --- НОВЫЕ СТРОКИ ДЛЯ ФИКСАЦИИ РАЗМЕРА ---
        self.setFixedSize(self.sizeHint()) # Фиксируем размер окна
        # self.setMinimumSize(300, 200) # Альтернатива: задать минимальный размер
        # self.setMaximumSize(400, 300) # Альтернатива: задать максимальный размер

        layout = QVBoxLayout(self)
        
        # Добавляем заголовок для красоты
        title_label = QLabel("Выберите уровни логирования для отображения:")
        title_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(title_label)
        layout.addSpacing(10) # Добавим отступ

        self.debug_checkbox = QCheckBox("Включить log_debug")
        self.info_checkbox = QCheckBox("Включить log_info")
        self.warning_checkbox = QCheckBox("Включить log_warning")
        self.error_checkbox = QCheckBox("Включить log_error (рекомендуется оставить включенным)")
        
        layout.addWidget(self.debug_checkbox)
        layout.addWidget(self.info_checkbox)
        layout.addWidget(self.warning_checkbox)
        layout.addWidget(self.error_checkbox)
        
        layout.addSpacing(15) # Отступ перед кнопками

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        # --- НОВЫЕ СТРОКИ ДЛЯ СОХРАНЕНИЯ СОСТОЯНИЯ (см. следующий пункт) ---
        self._load_settings()
        
        self.debug_checkbox.toggled.connect(self._on_checkbox_changed)
        self.info_checkbox.toggled.connect(self._on_checkbox_changed)
        self.warning_checkbox.toggled.connect(self._on_checkbox_changed)
        self.error_checkbox.toggled.connect(self._on_checkbox_changed)

    def _on_checkbox_changed(self):
        """Слот, который вызывается при любом изменении состояния чекбокса."""
        self._save_settings() # Просто вызываем сохранение

    def _save_settings(self):
        """Сохраняет текущее состояние чекбоксов в системные настройки (QSettings)."""        
        settings = QSettings("ModManagerTranslationsStellaris", "mySettings") # Укажите ваше имя компании и приложения

        settings.setValue("log/debug_enabled", self.debug_checkbox.isChecked())
        settings.setValue("log/info_enabled", self.info_checkbox.isChecked())
        settings.setValue("log/warning_enabled", self.warning_checkbox.isChecked())
        settings.setValue("log/error_checkbox", self.error_checkbox.isChecked())
        
        # Сохраняем состояние только если ОК нажали.
        # Лучше сохранять в методе accept(), но для простоты сделаем так.

    def _load_settings(self):
        """Загружает состояние чекбоксов из системных настроек."""
        
        settings = QSettings("ModManagerTranslationsStellaris", "mySettings")

        # Используем метод value() с умолчанием, чтобы избежать ошибок,
        # если настройка еще не сохранялась
        self.debug_checkbox.setChecked(settings.value("log/debug_enabled", defaultValue=False, type=bool))
        self.info_checkbox.setChecked(settings.value("log/info_enabled", defaultValue=False, type=bool))
        self.warning_checkbox.setChecked(settings.value("log/warning_enabled", defaultValue=False, type=bool))
        self.error_checkbox.setChecked(settings.value("log/error_checkbox", defaultValue=True, type=bool))

    def get_levels(self):
        return {
            "debug": self.debug_checkbox.isChecked(),
            "info": self.info_checkbox.isChecked(),
            "warning": self.warning_checkbox.isChecked(),
            "error": self.error_checkbox.isChecked()
        }
        
    def accept(self):
        """Переопределяем accept, чтобы сохранить настройки именно при нажатии ОК."""
        self._save_settings()
        super().accept() # Не забываем вызвать родительский метод