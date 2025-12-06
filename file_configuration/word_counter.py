# file_configuration/word_counter.py
import re

from PyQt6.QtWidgets import (    
    QWidget, 
    QPlainTextEdit, 
    QTextEdit,
        
)
from PyQt6.QtCore import (
    QObject, pyqtSignal, QRunnable, pyqtSlot
    )

from file_configuration.utils import log_debug, log_error, log_info, log_warning

class WordCounter(QObject):
    """
    Класс для подсчета слов и символов.
    Сигналы для асинхронной передачи результатов.
    """
    count_complete = pyqtSignal(int, int) # Сигнал, который будет отправлять результаты (слова, символы)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Кеш для предыдущих результатов, чтобы не считать без изменений
        self._last_text_hash = None
        self._last_word_count = 0
        self._last_char_count = 0

    def count(self, text: str):
        """
        Основной метод для подсчета.
        Сравнивает хеш текста, и если он изменился, запусчет подсчет.
        """
        try:
            # Если текст не изменился, отправляем старый результат
            current_hash = hash(text)
            if current_hash == self._last_text_hash:
                log_debug("DEBUG: WordCounter - Text unchanged, using cached result.")
                self.count_complete.emit(self._last_word_count, self._last_char_count)
                return

            log_debug("DEBUG: WordCounter - Text changed, starting count.")
            
            # Эффективный подсчет слов с использованием регулярных выражений
            words = re.findall(r'\b\w+\b', text)
            word_count = len(words)
            char_count = len(text)
            
            # Сохраняем результаты
            self._last_text_hash = current_hash
            self._last_word_count = word_count
            self._last_char_count = char_count
            
            # Отправляем результаты через сигнал
            self.count_complete.emit(word_count, char_count)
            
        except Exception as e:
            log_debug(f"ERROR in WordCounter.count: {str(e)}")
            self.count_complete.emit(0, 0)
            
            
class WordCountRunnable(QRunnable):
    """
    Задача для запуска WordCounter в отдельном потоке.
    """
    def __init__(self, text: str, word_counter: WordCounter):
        super().__init__()
        self.text = text
        self.word_counter = word_counter
        #self.setAutoDelete(True) # Задача удалится автоматически после выполнения

    
    def run(self):
        """
        Вызывает метод count у WordCounter.
        """
        log_debug("DEBUG: WordCountRunnable - Запуск задачи подсчета.")
        try:            
            self.word_counter.count(self.text)
        except Exception as e:
            log_error(f"КРИТИЧЕСКАЯ ОШИБКА в потоке WordCountRunnable: {str(e)}")
