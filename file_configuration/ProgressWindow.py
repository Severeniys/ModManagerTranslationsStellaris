from file_configuration.import_libraries.libraries import *
from file_configuration.TextConverter import *

class ProgressWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Прогресс")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint) # Устанавливаем флаг, чтобы окно оставалось поверх других окон
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # Убираем верхнюю панель окна
        self.setStyleSheet("background-color: 4C739A;") # Устанавливаем белый фон окна
        
        self.TextConverter = TextConverter()
        
        layout = QVBoxLayout(self)
        
        # Создаем виджет QLabel для отображения анимированной картинки
        self.label_image = QLabel(self)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Создаем виджет QLabel для отображения текста
        self.label_text = QLabel(self)
        self.label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.label_image)
        layout.addWidget(self.label_text)       
                
        self.start_animation() # Запускаем анимацию
        
    def start_animation(self):
        # Загружаем анимированную картинку
        movie = QMovie("C:\\Users\\Creatoris\\Desktop\\TextConverter\\TextConverter - актуальная версия в разработке\\6W9BFMc.gif")
        
        # Устанавливаем анимированную картинку в QLabel
        self.label_image.setMovie(movie)
        movie.start()
    
    def update_text(self, line):
        # Обновляем текст с помощью индекса в списке текстов
        self.label_text.setText(line)