from file_configuration.import_libraries.libraries import *

class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self.editor.lineNumberAreaWidth(), 1)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)