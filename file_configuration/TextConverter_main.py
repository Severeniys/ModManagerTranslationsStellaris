from file_configuration.import_libraries.libraries import *


class TextConverter_main(QMainWindow):
    def __init__(self, parent = None):
        super(TextConverter_main, self).__init__(parent)                
        from file_configuration.TextConverter import TextConverter
        self.textconverter = TextConverter() 
        self.textconverter.werkil2 = True                      
          
        self.setWindowTitle("TextConverter")
        self.setGeometry(500, 200, 300, 100)        
        
        self.setWindowIcon(QIcon("TextConverter.ico"))
        
        self.combo_box = QComboBox()
        self.combo_box.addItems(qdarktheme.get_themes())
        self.combo_box.currentTextChanged.connect(qdarktheme.setup_theme)
        
        self.btnl = QPushButton("Сохранить")
        self.btnl.clicked.connect(self.getIteml)
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.combo_box)
        self.layout.addWidget(self.btnl)
        
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.close()          
        
    def getIteml(self):
        self.slovar_time = self.combo_box.currentText()        
        self.textconverter.settings.setValue("slovar_time", self.slovar_time)
        
    def closeEvent(self, event):
        self.textconverter.werkil2 = False
        super().closeEvent(event)