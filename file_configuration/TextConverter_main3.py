from file_configuration.import_libraries.libraries import *


class TextConverter_main3(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)           
        from file_configuration.ModManagerTranslationsStellaris import TextConverterManager
        self.textconverter4 = TextConverterManager()
        self.textconverter4.werkil3 = True
           
        self.setWindowTitle("TextConverter")
        self.setGeometry(500, 200, 300, 100)        
        
        self.setWindowIcon(QIcon("TextConverter.ico"))

        self.settings1 = QSettings("TextConverter", "my1Settings") 
        
        self.layout = QFormLayout() 
        
        lbl1 = QLabel("Каталог Модов")        
        lbl1.setObjectName("first")
        self.layout.addRow(lbl1)            
    
        self.btn = QPushButton("Выберите файл")
        self.btn.clicked.connect(self.getItem)
        self.le = QLineEdit()
        self.layout.addRow(self.btn, self.le)
        
        lbl2 = QLabel("Каталог сборок")        
        lbl2.setObjectName("first")
        self.layout.addRow(lbl2) 
        
        self.btnl = QPushButton("Выберите файл")
        self.btnl.clicked.connect(self.getIteml)
        self.lel = QLineEdit()
        self.layout.addRow(self.btnl, self.lel)
        
        lbl3 = QLabel("Каталог \Stellaris\mod")        
        lbl3.setObjectName("first")
        self.layout.addRow(lbl3) 
        
        self.btnll = QPushButton("Выберите файл")
        self.btnll.clicked.connect(self.getItemll)
        self.lell = QLineEdit()
        self.layout.addRow(self.btnll, self.lell)        
        
        self.btnle = QPushButton("Сохранить")
        self.btnle.clicked.connect(self.getItemle)
        self.btnlx = QPushButton("Отмена")
        self.btnlx.clicked.connect(self.getItemlx)
        self.layout.addRow(self.btnle, self.btnlx)
        
        self.le.setText(self.textconverter4.pyti_mod)
        self.lel.setText(self.textconverter4.pyti_modl)
        self.lell.setText(self.textconverter4.pyti_modll)
        
        self.filename_1_ = ""
        self.filename_2_ = ""
        self.filename_3_ = ""                
        
        self.setLayout(self.layout)
        self.close()    

    def getItem(self):
        self.filename_1_ = QFileDialog.getExistingDirectory(self, caption=("Открыть папку"))
        self.le.setText(self.filename_1_)
        
    def getIteml(self):
        self.filename_2_ = QFileDialog.getExistingDirectory(self, caption=("Открыть папку"))
        self.lel.setText(self.filename_2_)
        
    def getItemll(self):
        self.filename_3_ = QFileDialog.getExistingDirectory(self, caption=("Открыть папку"))
        self.lell.setText(self.filename_3_)
        
    def getItemle(self): 
        le = self.le.text()   
        lel = self.lel.text()
        lell = self.lell.text()     
        """
        self.settings1.setValue("pyti_mod", self.le.text()) 
        self.settings1.setValue("pyti_modl", self.lel.text()) 
        self.settings1.setValue("pyti_modll", self.lell.text())
        """
        self.close()
        print(le, 1)
        self.textconverter4.save_settings_pyti(le, lel, lell)

    def getItemlx(self):
        self.close()
        
    def closeEvent(self, event):
        self.textconverter4.werkil3 = False
        super().closeEvent(event) 