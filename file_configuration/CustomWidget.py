from file_configuration.import_libraries.libraries import *

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout()
        self.line_edit1 = QLineEdit()
        self.line_edit1.minimumSizeHint()
        layout.addWidget(self.line_edit1)
        
        self.Button1 = QPushButton('Поиск')
        self.Button1.minimumSizeHint()
        layout.addWidget(self.Button1)
        
        self.line_edit2 = QLineEdit()
        self.line_edit2.minimumSizeHint()        
        layout.addWidget(self.line_edit2)
        
        self.Button2 = QPushButton('Замена')
        self.Button2.minimumSizeHint()
        layout.addWidget(self.Button2)  
        
        self.setLayout(layout)