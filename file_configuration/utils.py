# file_configuration/utils.py
import os
from loguru import logger as loguru_logger 
from PyQt6.QtCore import pyqtSignal, QObject

class LoggerWrapper(QObject):
    """
    Централизованный менеджер для логирования.
    Управляет выводом в консоль, GUI и файл.
    """
    simple_log_signal = pyqtSignal(str)
    rich_log_signal = pyqtSignal(str) 

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.logger - это наша ссылка на глобальный loguru_logger
        self.logger = loguru_logger 
        self._file_handler_id = None
        
        # Удаляем стандартный вывод в консоль, т.к. мы настроим свои
        self.logger.remove()
        self._setup_logger()

    def _setup_logger(self):
        """Настраивает базовые обработчики: консоль и GUI."""
                
        # 2. Вывод в статусную строку GUI через сигнал
        self._gui_handler_id = self.logger.add(
            sink=self.simple_log_signal.emit,
            level="DEBUG", # Базовый уровень
            format="{message}",
            colorize=False
        )
        # 2. Вывод в консоль для отладки
        self._console_handler_id = self.logger.add(
            sink=lambda msg: print(msg, end=""),
            level="DEBUG",
            format="{time:HH:mm:ss} | {level} | {message}",
            colorize=True
        )

    def set_log_level(self, level: str):
        """
        Изменяет уровень логирования для всех обработчиков.
        :param level: Уровень ("DEBUG", "INFO", "WARNING", "ERROR").
        """
        # loguru позволяет менять уровень для обработчика по его ID
        self.logger.level(level)# Это устанавливает глобальный уровень для логгера,
                                # и все обработчики, у которых уровень не указан явно, его используют.
        # Если нужно задать уровень для КАЖДОГО обработника отдельно:
        # self.logger.level(level, id=self._gui_handler_id)
        # self.logger.level(level, id=self._console_handler_id)
        # Но обычно достаточно и глобального уровня.
        
    def add_file_logger(self, log_file_path):
        """Добавляет или обновляет обработчик для записи логов в файл."""
        # 1. Если у нас уже есть файловый обработчик, его нужно УДАЛИТЬ
        if self._file_handler_id is not None:
            self.logger.remove(self._file_handler_id)
            self._file_handler_id = None
            # self.logger.info("Старый файловый обработчик логов удален.") # Не может вызвать сам себя
        
        # 2. Добавляем НОВЫЙ обработчик и сохраняем его ID
        self._file_handler_id = self.logger.add( # ИЗМЕНЕНИЕ 2: Используем self.logger
            sink=log_file_path,
            rotation="5 MB",
            retention="1 week",
            compression="zip",
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            encoding="utf-8",
            catch=False
        )
        
        # Сообщаем об успешной настройке через сигнал
        # Важно: это сообщение также попадет в консоль (наш другой обработчик)
        self.simple_log_signal.emit(f"Логирование в файл настроено: {log_file_path}")

# --- Глобальные функции-обертки для удобства ---
_log_wrapper_instance = None

def get_logger():
    """Возвращает единственный (singleton) экземпляр LoggerWrapper."""
    global _log_wrapper_instance
    if _log_wrapper_instance is None:
        _log_wrapper_instance = LoggerWrapper()
    return _log_wrapper_instance

def setup_logger(log_file_path):
    """
    Функция для вызова из main.py для настройки логирования в ФАЙЛ.
    """
    logger_instance = get_logger()
    logger_instance.add_file_logger(log_file_path)

# Ваши старые функции теперь просто перенаправляют вызов в экземпляр логгера
# ИЗМЕНЕНИЕ 3: Используем глобальный loguru_logger напрямую в функциях
def log_debug(message): loguru_logger.debug(message)
def log_info(message):  loguru_logger.info(message)
def log_error(message): loguru_logger.error(message)
def log_warning(message): loguru_logger.warning(message)

# Сигнал, который вы будете подключать к слоту в главном окне
# Он доступен сразу после импорта
log_signal = get_logger().simple_log_signal