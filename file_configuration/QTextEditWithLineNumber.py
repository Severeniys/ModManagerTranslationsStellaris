
from PyQt6.QtCore import (
    Qt,
    pyqtSignal, 
    QSize, 
    QRect
    )

from PyQt6.QtGui import (
    QColor, 
    QFont, 
    QFontMetrics,
    QPainter,
    QTextFormat
)

from PyQt6.QtWidgets import (    
    QWidget, 
    QPlainTextEdit, 
    QTextEdit,
        
)

from file_configuration.utils import log_debug, log_error, log_info, log_warning

# Добавляем явный импорт QFrame
from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter
from PyQt6.QtCore import QRegularExpression

class TranslationHighlighter(QSyntaxHighlighter):
    """Подсветчик синтаксиса для файлов переводов Stellaris"""    
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []
        
        # Создаем словарь соответствия цветовых кодов и QColor
        self.color_map = {
            'B': Qt.GlobalColor.blue,          # Blue - синий
            'E': Qt.GlobalColor.cyan,          # Teal - бирюзовый
            'G': Qt.GlobalColor.green,         # Green - зеленый
            'H': Qt.GlobalColor.darkYellow,    # Orange - оранжевый
            'L': QColor("#8B4513"),            # Brown - коричневый
            'M': Qt.GlobalColor.magenta,       # Purple - пурпурный
            'P': Qt.GlobalColor.red,           # Light red - светло-красный
            'R': Qt.GlobalColor.darkRed,       # Red - красный
            'S': QColor("#FF8C00"),            # Dark orange - темно-оранжевый
            'T': QColor("#D3D3D3"),            # Light grey - светло-серый
            'W': Qt.GlobalColor.white,         # White - белый
            'Y': Qt.GlobalColor.yellow,        # Yellow - желтый
        }
        
        # Формат для ключей (до двоеточия)
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#C75E3E"))
        key_format.setFontWeight(QFont.Weight.Bold)
        
        # Регулярное выражение для ключа (может содержать точки и цифры)
        key_pattern = r'[\w\.]+(?=\s*:)'
        self.highlighting_rules.append((QRegularExpression(key_pattern), key_format))
        
        # Формат для значения в кавычках
        value_format = QTextCharFormat()
        value_format.setForeground(QColor("#80E4BA"))
        
        # Регулярное выражение для значений в кавычках
        value_pattern = r'"[^"]*"'
        self.highlighting_rules.append((QRegularExpression(value_pattern), value_format))
        
        # Формат для номеров строк после двоеточия
        number_format = QTextCharFormat()
        number_format.setForeground(Qt.GlobalColor.yellow)
        
        # Регулярное выражение для номеров строк
        number_pattern = r'(?::\s*)(\d+)'
        self.highlighting_rules.append((QRegularExpression(number_pattern), number_format))
        
        link_format = QTextCharFormat()
        link_format.setForeground(QColor("#C40D43"))
        
        # Регулярное выражение для номеров строк
        link_pattern = r'\[[^\[\]]+\]'
        self.highlighting_rules.append((QRegularExpression(link_pattern), link_format))
        
        smail_format = QTextCharFormat()
        smail_format.setForeground(QColor("#DF8D12"))
        
        # Регулярное выражение для номеров строк
        smail_pattern = r'£[^£]+£'
        self.highlighting_rules.append((QRegularExpression(smail_pattern), smail_format))
        
        link_format_2 = QTextCharFormat()
        link_format_2.setForeground(QColor("#D4C112"))
        
        # Регулярное выражение для номеров строк
        link_pattern_2 = r'\$[^\$]+\$'
        self.highlighting_rules.append((QRegularExpression(link_pattern_2), link_format_2))
        
        # Комплексный формат для цветовых секций §...§
        # Этот формат будет обрабатываться отдельно
        self.color_section_format = QTextCharFormat()
        self.color_section_format.setFontWeight(QFont.Weight.Bold)
        
        # Регулярное выражение для поиска цветовых секций
        # Ищем §, затем цветовой код (одну букву), затем текст до §!
        self.color_section_pattern = QRegularExpression(r'§([BEGHLMPRSTWY])([^§]+)§!')

    def highlightBlock(self, text):
        """Применяет правила подсветки к блоку текста"""
        # Применяем стандартные правила
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)
        
        # Обрабатываем цветовые секции отдельно
        match_iterator = self.color_section_pattern.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            
            # Получаем цветовой код и текст
            color_code = match.captured(1)
            colored_text = match.captured(2)
            
            # Находим соответствующий QColor
            color = self.color_map.get(color_code, Qt.GlobalColor.white)
            
            # Создаем формат для цветового текста        
            format = QTextCharFormat()  # Создаем пустой формат
            format.setForeground(color) # Устанавливаем цвет для формата
            format.setFontWeight(QFont.Weight.Bold) # Устанавливаем жирный шрифт            
            
            # Находим позицию цветового текста (без § и кода цвета)
            start = match.capturedStart(2)
            length = match.capturedLength(2)
            
            # Применяем формат
            self.setFormat(start, length, format)


class QLineNumberArea(QWidget):
    """Область с номерами строк для QTextEditWithLineNumber"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)

    def sizeHint(self) -> QSize:
        return QSize(self.editor.lineNumberAreaWidth(), 1)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

class QTextEditWithLineNumber(QPlainTextEdit):
    """Текстовый редактор с нумерацией строк и подсветкой синтаксиса"""
    
    # Сигналы для уведомления о событиях
    _cursorPositionChanged = pyqtSignal(int, int)  # line, column 
    
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Инициализация переменных
        self.lineNumberArea = QLineNumberArea(self)
        self.color_dict = {}
        self._current_line = -1
        self._current_column = -1
        self._highlighter = None
        
        # Настройка внешнего вида
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setCenterOnScroll(True)
        
        # Подключение сигналов
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self._cursorPositionChanged.connect(self.highlightCurrentLine)
        
        
        # Инициализация области с номерами строк
        self.updateLineNumberAreaWidth(0)
        
        # Установка цвета фона
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #333333;
                padding: 5px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }
        """)

    def lineNumberAreaWidth(self) -> int:
        """Вычисляет необходимую ширину области с номерами строк"""
        digits = 1
        max_lines = max(1, self.blockCount())
        
        while max_lines >= 10:
            max_lines //= 10
            digits += 1
            
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits + 5
        return space

    def updateLineNumberAreaWidth(self, _):
        """Обновляет ширину области с номерами строк"""
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        """Обновляет область с номерами строк при прокрутке или изменении текста"""
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event) -> None:
        """Обработка изменения размера виджета"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )

    def highlightCurrentLine(self):
        """Подсветка текущей строки с курсором"""
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            
            lineColor = QColor("#404040")
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            
            cursor = self.textCursor()
            selection.cursor = cursor
            selection.cursor.clearSelection()
            
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)
        
        # Эмитируем сигнал с изменением позиции курсора
        block = self.textCursor().block()
        line_number = block.blockNumber() + 1
        column = self.textCursor().position() - block.position()
        
        if line_number != self._current_line or column != self._current_column:
            self._current_line = line_number
            self._current_column = column
            self._cursorPositionChanged.emit(line_number, column)

    def lineNumberAreaPaintEvent(self, event):
        """Отрисовка области с номерами строк"""
        painter = QPainter(self.lineNumberArea)
        
        painter.fillRect(event.rect(), QColor("#1b1e1e"))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        
        font_metrics = QFontMetrics(self.font())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                line_number = block_number + 1
                
                color = self.color_dict.get(line_number, "darkCyan")
                if color == "red":
                    painter.setPen(Qt.GlobalColor.darkRed)
                elif color == "green":
                    painter.setPen(Qt.GlobalColor.darkGreen)
                else:
                    painter.setPen(Qt.GlobalColor.darkCyan)
                
                number_text = f"{line_number}"
                painter.drawText(
                    0, top, self.lineNumberArea.width(), font_metrics.height(),
                    Qt.AlignmentFlag.AlignRight, number_text
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def theResultoftheScantoUpdatetheColor(self, color_dict):
        """Обновляет цвета строк на основе переданного словаря"""
        self.color_dict = color_dict
        self.lineNumberArea.update()

    #def _on_text_changed(self):
        #"""Обработчик изменения текста"""
        #self.textChanged.emit()

    # --- Новые методы ---

    def enableSyntaxHighlighting(self, enable=True):
        """Включает или отключает подсветку синтаксиса"""
        if enable and not self._highlighter:
            self._highlighter = TranslationHighlighter(self.document())
        elif not enable and self._highlighter:
            self._highlighter = None

    def setLineColors(self, color_dict):
        """Устанавливает цвета для строк с более понятным названием"""
        self.theResultoftheScantoUpdatetheColor(color_dict)

    def getCursorPosition(self):
        """Возвращает текущую позицию курсора (номер строки и колонки)"""
        block = self.textCursor().block()
        line_number = block.blockNumber() + 1
        column = self.textCursor().position() - block.position()
        return line_number, column

    def gotoLine(self, line_number, column=0):
        """Перемещает курсор на указанную строку и колонку"""
        if 1 <= line_number <= self.blockCount():
            block = self.document().findBlockByLineNumber(line_number - 1)
            if block.isValid():
                cursor = self.textCursor()
                cursor.setPosition(block.position() + column)
                self.setTextCursor(cursor)
                self.centerCursor()
                return True
        return False

    def getVisibleLines(self):
        """Возвращает номера видимых строк"""
        visible_lines = []
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        
        while block.isValid() and block.isVisible():
            visible_lines.append(block_number + 1)
            block = block.next()
            block_number += 1
            
        return visible_lines

    def setLineNumberAreaWidth(self, width=None):
        """Устанавливает фиксированную ширину для области с номерами строк"""
        if width is None:
            self.updateLineNumberAreaWidth(0)
        else:
            self.setViewportMargins(width, 0, 0, 0)  
    
    
            
"""
# Создаем редактор
editor = QTextEditWithLineNumber()

# Устанавливаем цвета для строк
color_dict = {
    5: "red",    # 5-я строка будет красной
    10: "green", # 10-я строка будет зеленой
    15: "red"    # 15-я строка будет красной
}
editor.setLineColors(color_dict)

# Переходим к 10-й строке, 3-му символу
editor.gotoLine(10, 3)

# Получаем текущую позицию курсора
line, column = editor.getCursorPosition()
print(f"Текущая позиция: строка {line}, колонка {column}")

# Получаем все видимые строки
visible = editor.getVisibleLines()
print(f"Видимые строки: {visible}")

# Подключаемся к сигналу изменения позиции
editor.cursorPositionChanged.connect(lambda line, col: print(f"Курсор moved to {line}:{col}"))
"""