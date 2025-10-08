from file_configuration.import_libraries.libraries import *
from file_configuration.QLineNumberArea import *

class QTextEditWithLineNumber(QPlainTextEdit):
    def __init__(self):
        super().__init__()        
        self.lineNumberArea = QLineNumberArea(self)
        self.setViewportMargins(self.lineNumberArea.width(), 0, 0, 0) #установите поля видового экрана
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth) #Изменено количество блоков
        self.updateRequest.connect(self.updateLineNumberArea) #запрос на обновление
        self.cursorPositionChanged.connect(self.highlightCurrentLine) #Изменено положение курсора        
        self.updateLineNumberAreaWidth(0)
        self.color_dict = None

    def lineNumberAreaWidth(self) -> int: #номер строки Ширина области
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('12') * digits
        return space

    def updateLineNumberAreaWidth(self, _): #обновить номер строки, ширину области
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy): #обновить область номера строки
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self): #выделите текущую строку
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor("#333").lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event): #событие рисования области с номером строки
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#1b1e1e")) #заполнить прямоугольник

        block = self.firstVisibleBlock() #первый видимый блок
        blockNumber = block.blockNumber() #номер блока
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top()) #геометрия, ограничивающая блок
        bottom = top + int(self.blockBoundingRect(block).height()) ##прямоугольник, ограничивающий блок

        font_metrics = QFontMetrics(self.font()) #Q Показатели шрифта

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                block = self.document().findBlockByLineNumber(blockNumber)
                numbere =  blockNumber + 1
                if block.isValid():                 
                    if self.color_dict:                                            
                        if self.color_dict.get(numbere) == "red":
                            painter.setPen(Qt.GlobalColor.darkRed)
                        elif self.color_dict.get(numbere) == "green":
                            painter.setPen(Qt.GlobalColor.cyan)
                        else:
                            painter.setPen(Qt.GlobalColor.darkCyan)
                    else:
                        painter.setPen(Qt.GlobalColor.darkCyan)
                else:
                    print(f"Некорректный номер строки: {blockNumber}")          
                number = f"{str(blockNumber + 1)} "
                painter.setPen(Qt.GlobalColor.darkCyan)
                painter.drawText(0, top, self.lineNumberArea.width(), font_metrics.height(), Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def theResultoftheScantoUpdatetheColor(self, color_dict): #результат сканирования для обновления цвета
        self.color_dict = color_dict
        print(self.color_dict)
        
        