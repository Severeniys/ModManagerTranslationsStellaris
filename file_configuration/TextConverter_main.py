import os
import sys
import qdarktheme

from PyQt6.QtCore import (
    Qt,
    pyqtSignal, 
    QSize, 
    QRect
    )

from PyQt6.QtGui import (
    QIcon, 
    QFont, 
    QFontMetrics,
    QPainter,
    QTextFormat
)

from PyQt6.QtWidgets import (
    QComboBox, 
    QMainWindow,
    QPushButton,
    QWidget,
    QHBoxLayout
    
)

from file_configuration.utils import log_debug, log_error, log_info, log_warning

class TextConverter_main(QMainWindow):
    def __init__(self, parent = None):
        super(TextConverter_main, self).__init__(parent)                
        from file_configuration.ModManagerTranslationsStellaris import ModManagerTranslationsStellaris
        self.textconverter = ModManagerTranslationsStellaris() 
        self.textconverter.werkil2 = True                      
        
        self.setWindowTitle("ModManagerTranslationsStellaris")
        self.setGeometry(500, 200, 300, 100)        
        
        if getattr(sys, 'frozen', False): 
            self.base_resources_path = sys._MEIPASS
        else:            
            self.base_resources_path = os.path.dirname(os.path.abspath(__file__))
            self.base_resources_path = os.path.dirname(self.base_resources_path) # Поднимаемся на 1 уровень

        main_icon_path = os.path.join(self.base_resources_path, "file_configuration", "resources", "ModManagerTranslationsStellaris.ico") 

        if os.path.exists(main_icon_path):
            self.setWindowIcon(QIcon(main_icon_path))
        else:
            print(f"Warning: Application main icon not found at {main_icon_path}") 
        
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