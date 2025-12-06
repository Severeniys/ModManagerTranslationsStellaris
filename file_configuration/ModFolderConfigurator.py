import os
import sys

from PyQt6.QtGui import QIcon 

from PyQt6.QtWidgets import (    
    QDialog, 
    QLabel,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QFileDialog
)
from PyQt6.QtCore import (
    QSettings
)

from file_configuration.utils import log_debug, log_error, log_info, log_warning
from file_configuration.ModManagerTranslationsStellaris import ModManagerTranslationsStellaris

class ModFolderConfigurator(QDialog):
    def __init__(self, main_window: ModManagerTranslationsStellaris):
        super().__init__()    
        log_debug("ModFolderConfigurator.__init__ - started")
        
        
        self.main_window = main_window
        self.main_window.werkil3 = True
        log_debug("ModFolderConfigurator инициализирован с доступом к главному окну.")
        
        self.setWindowTitle("Mod Manager Translations Stellaris")
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
            log_debug(f"Warning: Application main icon not found at {main_icon_path}")

        self.settings = QSettings("ModManagerTranslationsStellaris", "mySettings") 
        
        self.layout = QFormLayout() 
        
        lbl1 = QLabel("Каталог Модов (папка 281990)")        
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
        
        lbl3 = QLabel("Каталог /Stellaris/mod")        
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
        
        self.le.setText(self.main_window.dir_content)
        self.lel.setText(self.main_window.dir_assembling)
        self.lell.setText(self.main_window.dir_Stellaris_mod)
        
        self.filename_1_ = ""
        self.filename_2_ = ""
        self.filename_3_ = ""                
        
        self.setLayout(self.layout)
        log_debug("ModFolderConfigurator.__init__ - finished")

    def getItem(self):
        log_debug("ModFolderConfigurator.getItem - started")  # Логируем начало метода
        self.filename_1_ = QFileDialog.getExistingDirectory(self, caption=("Открыть папку"))
        self.le.setText(self.filename_1_)
        log_debug(f"ModFolderConfigurator.getItem - selected directory: {self.filename_1_}")  # Логируем выбранную директорию
        log_debug("ModFolderConfigurator.getItem - finished")  # Логируем завершение метода
        
    def getIteml(self):
        log_debug("ModFolderConfigurator.getIteml - started")  # Логируем начало метода
        self.filename_2_ = QFileDialog.getExistingDirectory(self, caption=("Открыть папку"))
        self.lel.setText(self.filename_2_)
        log_debug(f"ModFolderConfigurator.getIteml - selected directory: {self.filename_2_}")  # Логируем выбранную директорию
        log_debug("ModFolderConfigurator.getIteml - finished")  # Логируем завершение метода

    def getItemll(self):
        log_debug("ModFolderConfigurator.getItemll - started")  # Логируем начало метода
        self.filename_3_ = QFileDialog.getExistingDirectory(self, caption=("Открыть папку"))
        self.lell.setText(self.filename_3_)
        log_debug(f"ModFolderConfigurator.getItemll - selected directory: {self.filename_3_}")  # Логируем выбранную директорию
        log_debug("ModFolderConfigurator.getItemll - finished")  # Логируем завершение метода
        
    def getItemle(self):
        log_debug("ModFolderConfigurator.getItemle - started")  # Логируем начало метода
        le = self.le.text()
        lel = self.lel.text()
        lell = self.lell.text()
        self.close()  # Закрываем окно после сохранения
        log_debug(f"ModFolderConfigurator.getItemle - saving settings: dir_content={le}, dir_assembling={lel}, dir_Stellaris_mod={lell}")  # Логируем сохраняемые настройки
        self.main_window.save_settings_pyti(le, lel, lell)
        log_debug("ModFolderConfigurator.getItemle - finished")  # Логируем завершение метода

    def getItemlx(self):
        log_debug("ModFolderConfigurator.getItemlx - started")  # Логируем начало метода
        self.close()  # Закрываем окно при нажатии "Отмена"
        log_debug("ModFolderConfigurator.getItemlx - finished")  # Логируем завершение метода

    def closeEvent(self, event):
        log_debug("ModFolderConfigurator.closeEvent - started")  # Логируем начало метода
        self.main_window.werkil3 = False
        log_debug("ModFolderConfigurator.closeEvent - werkil3 set to False")  # Логируем изменение werkil3
        super().closeEvent(event)
        log_debug("ModFolderConfigurator.closeEvent - finished")  # Логируем завершение метода