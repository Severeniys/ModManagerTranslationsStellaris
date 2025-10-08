from file_configuration.QLineNumberArea import *
from file_configuration.QTextEditWithLineNumber import *
from file_configuration.CustomWidget import *
from file_configuration.GetDialsThread import *
from file_configuration.CountThread import *
from file_configuration.TextConverter_main import *
from file_configuration.ModManagerTranslationsStellaris import *


class TextConverter(QMainWindow):  
    signal_text_changed = pyqtSignal(str)  
    def __init__(self, treserto=None):
        super().__init__()
        self.treserto = treserto
        self.dirs = os.path.abspath(os.curdir)
        print(f"Текущее положение {self.dirs}")
        
        self.setWindowIcon(QIcon("TextConverter.ico"))

        self.setWindowTitle("TextConverter")
        
        self.settings = QSettings("TextConverter", "mySettings")                                
        
        self.text_widget()
        
        self.QVBoxLayout_()

        self.createMenuBar() 
        
        self.load_settings()   
    
    def load_settings(self):        
        toolbar_state = self.settings.value("toolbar_state")
        if toolbar_state is not None:
            self.restoreState(toolbar_state)
        # Загрузка положения и размера окна
        self.resize(self.settings.value("size", QSize(1564, 772)))
        self.move(self.settings.value("pos", QPoint(188, 150)))
        
        font_family = self.settings.value("font/family", "Times New Roman")
        font_size = self.settings.value("font/size", 9)
        font_bold = self.settings.value("text/font_bold", True)        
        if font_bold == "true":
           font_bold = True 
        font = QFont(font_family, font_size)
        font.setBold(font_bold)
        self.setFont(font) 
        self.num_lines = None        
        
        #остальные переменные    
        
        self.listOfChangedKeys = []
        self.putirol = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\281990"        
        self.pytj = None         
        self.ilo, self.ila = 0, 0         
        
        self.isifra = 0     
        
        self.direktoria1 = rf"{self.dirs}\katalog\init_l"      
        self.lovie = None        
        
        self.werkil1 = False 
        self.werkil2 = False        
        self.werkil3 = False        
        self.werkil4 = False 
        self.nova_fail = None
        self.secondaryPotok = None 
        self.streamObject1 = None   
            
        self.lovie_sev = self.settings.value("file/lovie_sev", "")
        self.filename = self.settings.value("file/filename", "")
        self.pytj_permomene = self.settings.value("file/pytj_permomene", "")
                 
        if self.treserto == None:    
            if self.lovie_sev == "try4":                      
                self.setStart_1(self.pytj_permomene, self.lovie_sev)
                self.secondaryPotok.started.connect(self.streamObject1.start11)
                self.setStart_2()
            else:   
                self.openAfFile() 
            
    def save_settings(self): 
        if os.path.isfile(self.pytj_permomene):
            text_edit = self.text_edit.toPlainText()
            with open(self.pytj_permomene, 'w', encoding="utf-8-sig") as file_l:
                file_l.write(text_edit)
            file_l.close()
        
        self.settings.setValue("file/filename", self.filename)
        self.settings.setValue("file/lovie_sev", self.lovie_sev)
        self.settings.setValue("file/pytj_permomene", self.pytj_permomene)
        
        # Сохранение положения и размера окна
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("size", self.size())

        # Сохранение настроек шрифта
        
        font = self.font()
        self.settings.setValue("font/family", font.family())
        self.settings.setValue("font/size", font.pointSize())
        self.settings.setValue("text/font_bold", True)
        
        self.settings.setValue("toolbar_state", self.saveState())
                   
    def text_widget(self):                
        self.text_edit = QTextEditWithLineNumber()
        self.setCentralWidget(self.text_edit)
        
        self.is_running = True     
        
        self.text_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
                      
        self.statusar = self.statusBar()
        self.statusBar().setStyleSheet("border :0.5px solid darkGray;")
        self.character_count = QLabel(f"Слов = 0, Знаков = 0")                        
        self.statusBar().addPermanentWidget(self.character_count)
        self.statusBar().showMessage(f"Файл не выбран: ")
                
        fonti = self.text_edit.font()          
        self.text_edit.setFont(fonti)
        
        self.text_edit.textChanged.connect(self.handle_text_changed)
        

    def QVBoxLayout_(self):        
                
        self.tb = QToolBar("Help", self)
        self.tb.setObjectName("toolbar")
        self.addToolBar(self.tb)               
        newTipt = "Панель дополнительных окон"
        self.gjlcrfprf(self.tb, newTipt)
               
        """
        newor2 = QAction(QIcon(f"{self.dirs}\katalog\impek\\256879.png"),"Строка преобразованис UTF-8", self)
        self.tb.addAction(newor2)
        newor3 = QAction(QIcon(f"{self.dirs}\katalog\impek\\251970.png"),"Сборка модов", self)
        self.tb.addAction(newor3)
        """ 
        newor4 = QAction(QIcon(rf"{self.dirs}\katalog\impek\\icons8-per.png"),"TextConverter - Менеджер", self)
        newTipt4 = "Открывает Менеджер модов"
        self.tb.addAction(newor4)
        self.gjlcrfprf(newor4, newTipt4)
        
        self.tb.addSeparator()
        
        newor5 = QAction(QIcon(rf"{self.dirs}\katalog\impek\\53878.png"),"Преобразовать, Копировать", self)
        newTipt5 = "Вставте короткий текст и нажмите чтобы зашифровать ключи и ссылки и сразу скопировать в буфер обмена."
        self.tb.addAction(newor5)
        self.gjlcrfprf(newor5, newTipt5)
        
        newor6 = QAction(QIcon(rf"{self.dirs}\katalog\impek\\53896.png"),"Вставить, Преобразовать, Копировать", self)
        newTipt6 = "Переведя текст нажмите чтобы вставить текст из буфера обмена и ражшифровать и затем получить обратно его в буфер обмена."
        self.tb.addAction(newor6)
        self.gjlcrfprf(newor6, newTipt6)
               
        self.tb.actionTriggered[QAction].connect(self.toolbtnpressed)
        self.tb.setStyleSheet("color: black") 
    
    #################################################################################################################    
        
    def createMenuBar(self):    
        self.menuBar = QMenuBar(self)        
        self.setMenuBar(self.menuBar)

        file = QMenu("&Файл", self)
        self.menuBar.addMenu(file)
        file1 = QMenu("&Инструменты", self)
        self.menuBar.addMenu(file1)
        file2 = QMenu("&Анализ", self)
        self.menuBar.addMenu(file2)
        file3 = QMenu("&Опции", self)
        self.menuBar.addMenu(file3)

        self.neve1 = file.addAction("Новое", self.action_clicked)
        newTip1 = "Создание резервного файла для небольшого текста"
        self.gjlcrfprf(self.neve1, newTip1)
                
        self.neve2 = file.addAction("Открыть", self.action_clicked)
        newTip2 = "Открытие файла *.yml"
        self.gjlcrfprf(self.neve2, newTip2)
        
        file.addSeparator()
        
        self.neve3 = file.addAction("Сохранить", self.action_clicked)
        newTip3 = "Сохранить в ту же папку"
        self.gjlcrfprf(self.neve3, newTip3)
        
        self.neve4 = file.addAction("Сохранить как", self.action_clicked)
        newTip4 = "Выбрать папку для сохранения"
        self.gjlcrfprf(self.neve4, newTip4)
        
        file.addSeparator()
        
        self.neve51 = file.addAction("Открыть резерв", self.action_clicked)
        newTip51 = "Открыть паку куда сохранён файлы после конвертации для перевода в другом редакторе"
        self.gjlcrfprf(self.neve51, newTip51)
        
        self.neve52 = file.addAction("Обновить из файла", self.action_clicked)
        newTip52 = "Обновления из резервного файла если вы переводите не в TextConverter"
        self.gjlcrfprf(self.neve52, newTip52)
        
        self.neve53 = file.addAction("Закрыть файл", self.action_clicked)
        newTip53 = "Закрытие открытого файл без сохранение стирание текста"
        self.gjlcrfprf(self.neve53, newTip53) 
              
        self.neve6 = file1.addAction("Упаковка ссылок", self.action_clicked)
        newTip6 = "Все ссылки в открытом в редакторе текста будут зашифрованы для дальнейшего перевода в переводчике"
        self.gjlcrfprf(self.neve6, newTip6)
        
        self.neve7 = file1.addAction("Упаковка ключей", self.action_clicked)
        newTip7 = "Все ключи в открытом в редакторе текста будут зашифрованы для дальнейшего перевода в переводчике"
        self.gjlcrfprf(self.neve7, newTip7)
        
        file1.addSeparator()
        
        self.neve8 = file1.addAction("Распаковка", self.action_clicked)
        newTip8 = "Всё зашифрованное в тесте будет расшифровано применяется когда вы завершили перевод"
        self.gjlcrfprf(self.neve8, newTip8)   
        
        self.neve9 = file2.addAction("Замена по словарю", self.action_clicked)
        newTip9 = "Заменяет по составленному списку выражения в тексте."
        self.gjlcrfprf(self.neve9, newTip9)

        self.neve91 = file2.addAction("Очистка #Новых строк", self.action_clicked)
        newTip91 = "Очищает текст от коментариев о новой строке"
        self.gjlcrfprf(self.neve91, newTip91)
        
        self.neve10 = file3.addAction("Очистить директорию резерва", self.action_clicked)
        newTip10 = "Всё зашифрованное в тесте будет расшифровано применяется когда вы завершили перевод"
        self.gjlcrfprf(self.neve10, newTip10) 
                
        self.neve14 = file3.addAction("Количество слов", self.action_clicked)
        newTip14 = "Подсчитает кол. слов и символов выводя результат в этом баре"
        self.gjlcrfprf(self.neve14, newTip14)
        
        file3.addSeparator()
        
        self.neve15 = impAct2 = file3.addMenu("Настройки")
        newTip15 = "Всё зашифрованное в тесте будет расшифровано применяется когда вы завершили перевод"
        self.gjlcrfprf(self.neve15, newTip15)
        
        self.neve16 = impAct2.addAction("Настройки шрифта", self.action_clicked)
        newTip16 = "Меню настрока шрифта"
        self.gjlcrfprf(self.neve16, newTip16)
        
        self.neve20 = impAct2.addAction("Настройка темы", self.action_clicked)
        newTip20 = "Настройка темы"
        self.gjlcrfprf(self.neve20, newTip20)
        
        """
        self.neveral1 = QAction("1 тема", self, checkable=True)
        print(self.neveral1)
        newTip17 = "Стандартная белая тема"
        self.gjlcrfprf(self.neveral1, newTip17)
        self.neveral1.setChecked(self.slovar_time["time1"])        
        self.neveral1.triggered.connect(self.temalaps1)
        
        self.neveral2 = QAction("2 тема", self, checkable=True)
        newTip18 = "Тёмная тема"
        self.gjlcrfprf(self.neveral2, newTip18)
        self.neveral2.setChecked(self.slovar_time["time2"])        
        self.neveral2.triggered.connect(self.temalaps2)
        
        self.neveral3 = QAction("3 тема", self, checkable=True)
        newTip21 = "Текущая тема Виндовс"
        self.gjlcrfprf(self.neveral3, newTip21)
        self.neveral3.setChecked(self.slovar_time["time3"])        
        self.neveral3.triggered.connect(self.temalaps3)        
        
        impAct3.addAction(self.neveral1)
        impAct3.addAction(self.neveral2)
        impAct3.addAction(self.neveral3)        
        """
                
        self.neve11 = impAct1 = impAct2.addMenu("Настроить: Анализ-Замена")
        newTip11 = "Настройка словаря замены: слева то что заменяется тем что справо при редактирование придерживайтесь общей структуре."
        self.gjlcrfprf(self.neve11, newTip11)
        
        self.neve12 = impAct1.addAction("Открыть АЗ", self.action_clicked)
        newTip12 = "Открывает словарь в редакторе"
        self.gjlcrfprf(self.neve12, newTip12)
        
        self.neve13 = impAct1.addAction("Закрыть АЗ", self.action_clicked)
        newTip13 = "Сохраняет и закрывает словарь"
        self.gjlcrfprf(self.neve13, newTip13)
        
        self.neve19 = impAct2.addAction("Настройки -", self.action_clicked)
        newTip19 = "Заглушка"
        self.gjlcrfprf(self.neve19, newTip19)
        
        self.custom_widget = CustomWidget()
        self.menuBar.setCornerWidget(self.custom_widget)  
        
        self.custom_widget.Button1.clicked.connect(lambda: self.Buttonfuns1())
        self.custom_widget.Button2.clicked.connect(lambda: self.Buttonfuns2())   
    
    def gjlcrfprf(self, neve, text):
        self.neve = neve
        self.neve.setStatusTip(text)
        self.neve.setToolTip(text)            
    
    def toolbtnpressed(self,a):
        action = a.text()                             
        if action == "TextConverter - Менеджер":
            #try:            
            self.getdials16()                
            #except BaseException as e: 
                #print(e)
                #self.statusBar().showMessage(f"None")  
        elif action == "Преобразовать, Копировать":
            try:            
                self.getdials17()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")  
        elif action == "Вставить, Преобразовать, Копировать":
            try:            
                self.getdials18()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")  
        
    @QtCore.pyqtSlot()
    def action_clicked(self):
        action = self.sender()        
        self.statusBar().showMessage(action.text())   
        if action.text() == "Новое":            
            try:            
                self.getdials14()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")    
        elif action.text() == "Открыть":
            try:            
                self.getdials13()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")                     
        elif action.text() == "Сохранить":
            try:            
                self.getdials12()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")    
        elif action.text() == "Сохранить как":
            try:            
                self.getdials11()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")              
        elif action.text() == "Настройки шрифта":
            try:            
                self.getdials10()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None") 
        elif action.text() == "Открыть резерв":            
            try:            
                self.getdials9()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None") 
        elif action.text() == "Обновить из файла":
            try:            
                self.getdials8()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None") 
        elif action.text() == "Сохранить в резерв":
            try:            
                self.getdials7()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")            
        elif action.text() == "Упаковка ссылок":
            try:            
                self.getdials6()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")                
        elif action.text() == "Замена по словарю":
            try:            
                self.getdials5()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")   
        elif action.text() == "Очистка #Новых строк":
            try:            
                self.getdials51()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")   
        elif action.text() == "Упаковка ключей":
            try:            
                self.getdials4()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")    
        elif action.text() == "Распаковка":       
            try:            
                self.getdials3()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")  
        elif action.text() == "Открыть АЗ":
            try:            
                self.gettext_r1()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")  
        elif action.text() == "Закрыть АЗ":
            try:            
                self.gettext_r2()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")
        elif action.text() == "Очистить директорию резерва":
            try:            
                self.getdials1()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")                           
        elif action.text() == "Настройка темы":
            try:            
                self.getdials01()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")
        elif action.text() == "Закрыть файл":
            try:            
                self.CloseTheFile()                
            except BaseException as e: 
                print(e)
                self.statusBar().showMessage(f"None")
 
############################################################################################################### 
    
    def CloseTheFile(self):
        self.filename = ""
        self.text_edit.setPlainText("")
        self.lovie_sev = "" 
        self.pytj_permomene = ""       
                          
    def Buttonfuns1(self):
        line = self.custom_widget.line_edit1.text()
        self.text_edit.theResultoftheScantoUpdatetheColor()
    
    def Buttonfuns2(self):
        line1 = self.custom_widget.line_edit1.text()
        line2 = self.custom_widget.line_edit2.text()
        line = self.text_edit.toPlainText()
        line = line.replace(line1, line2)
        self.text_edit.setPlainText(line)       
   
    def getdials17(self): #"Преобразовать, Копировать"
        self.lovie = "try1"
        self.getdials6() 
            
    def getdials17_1(self):
        lex = self.text_edit.toPlainText()
        clipboard = QApplication.clipboard() 
        clipboard.setText(lex)
        
    def getdials18(self): #"Вставить, Преобразовать, Копировать"
        clipboard = QApplication.clipboard()
        lex = clipboard.text()
        self.text_edit.setPlainText(lex)
        self.lovie = "try3"
        self.getdials3()
        lex = self.text_edit.toPlainText()
        clipboard.setText(lex)
                             
    def getdials5(self): #"Анализ-Замена"     
        self.setStart_1()   
        self.secondaryPotok.started.connect(self.streamObject1.start4)
        self.setStart_2()        

    def getdials51(self): #"Очистка #Новых строк"     
        self.setStart_1()   
        self.secondaryPotok.started.connect(self.streamObject1.start5)
        self.setStart_2()  
                                
    def getdials1(self):                        
        d = f"{self.direktoria1}\\"
        filesToRemove = [os.path.join(d, f) for f in os.listdir(d)]
        for f in filesToRemove:
            os.remove(f)   
       
    def getdials3(self): #"Распаковка"
        print(333)  
        if self.ilo or self.ila == 0:    
            self.setStart_1()
            self.secondaryPotok.started.connect(self.streamObject1.start3)
            self.setStart_2()
            self.ilo, self.ila = 0, 0
        else:
            self.statusBar().showMessage(f"None")
        # ... 

    def getdials4(self): #"Упаковка ключей"
                
        if self.ilo == 0:  
            self.setStart_1()
            self.secondaryPotok.started.connect(self.streamObject1.start2)            
            self.setStart_2()
            self.ilo = 1
        else:
            self.statusBar().showMessage(f"None")
        # ...       
                
    def getdials6(self): #"Упаковка ссылок"\  
        
        if self.ila == 0:     
            self.setStart_1()
            self.secondaryPotok.started.connect(self.streamObject1.start1)            
            self.setStart_2()
            self.ila = 1
        else:
            self.statusBar().showMessage(f"None")
        # ...

####################################################################################################################################################### 

    def setStart_1(self, puti=None, lovie=None):
        if self.streamObject1 and self.secondaryPotok:
            # Если рабочий объект и поток уже существуют, прерываем выполнение
            return
        filename = self.filename
        nova_fail = self.nova_fail        
        pytj = self.pytj 
        text_edit = self.text_edit        
        if puti != None:
            filename = puti
        if lovie == None:
            lovie = self.lovie
        self.setEnabled(False)
        self.secondaryPotok = QThread()                    
        self.streamObject1 = GetDialsThread(text_edit, nova_fail, pytj, filename, lovie)             
        self.streamObject1.moveToThread(self.secondaryPotok)
        
        
    def setStart_2(self):  
        self.streamObject1.finishSignal_1.connect(self.setInit)
        self.streamObject1.finishSignal_filename.connect(self.returnFunction_filename) 
        self.streamObject1.finishSignal_linesi.connect(self.returnFunction_linesi)        
        self.streamObject1.finishSignal_error.connect(self.returnFunction_error)   
        self.streamObject1.finishSignal_pytj.connect(self.returnFunction_pytj)        
        self.secondaryPotok.start()
        
    def setInit(self, lovie=None):        
        self.secondaryPotok.quit()
        self.secondaryPotok.wait()
        self.streamObject1 = None
        self.secondaryPotok = None
        self.setEnabled(True)            
        if lovie == "try1":
            self.lovie = "try2"
            self.getdials4()
        elif lovie == "try2":
            self.getdials17_1()
        elif lovie == "try3":    
            lex = self.text_edit.toPlainText()
            clipboard = QApplication.clipboard()
            clipboard.setText(lex)                
        elif lovie == "try4":
            self.lovie_sev = lovie            
            self.pytj_permomene = self.pytj  
                    
    def returnFunction_linesi(self, linesi):
        if linesi != "":              
            self.text_edit.setPlainText(linesi)
            self.setEnabled(True) 
            
    def returnFunction_error(self, error):
        if error != "":
            self.statusBar().showMessage(f"None")
            
    def returnFunction_pytj(self, pytj):
        if pytj != "":    
            self.pytj = pytj
    
    def returnFunction_filename(self, filename):
        if filename != "":    
            self.filename = filename
    
    def scan_text(self, word_list):
        print("Поток Запущен 2")        
        if word_list != []:            
            if self.ilo == 0:
                print("Начат запуск")
                self.secondaryPotok2 = QThread() 
                text1 = self.text_edit.toPlainText()
                self.streamObject2 = CountThread_2(text1, word_list)              
                self.streamObject2.moveToThread(self.secondaryPotok2)
                self.secondaryPotok2.started.connect(self.streamObject2.start1)                
                self.streamObject2.finishSignal_1l.connect(self.update_character_count_2)                
                self.secondaryPotok2.start()
        else:
            print("Список пуст")
    
    def update_character_count_2(self, color_dict):
        self.text_edit.theResultoftheScantoUpdatetheColor(color_dict)
        self.secondaryPotok2.quit()
        self.secondaryPotok2.wait()        
                
    def handle_text_changed(self):            
        if self.is_running:
            print("Поток Запущен 3")  
            self.secondaryPotok3 = QThread() 
            text = self.text_edit.toPlainText()
            self.streamObject3 = CountThread_1(text)           
            self.streamObject3.moveToThread(self.secondaryPotok3)
            self.secondaryPotok3.started.connect(self.streamObject3.start1)       
            self.streamObject3.finishSignal_1l.connect(self.secondaryPotok3.quit)
            self.streamObject3.finishSignal_1l.connect(self.update_character_count_1)
            self.secondaryPotok3.start()
            self.is_running = False    
        else:
            print("Поток занят")
        
        num_lines = self.text_edit.document().blockCount()
        self.signal_text_changed.emit(str(num_lines))        
        self.num_lines = num_lines        
        
    def update_character_count_1(self, word_count, char_count):
        self.character_count.setText(f"Слов = {word_count}, Знаков = {char_count}")
        self.is_running = True
        self.secondaryPotok3.quit()
        self.secondaryPotok3.wait()
                     
#########################################################################################################################################################
        
    def getdials7(self):          # Сохранить в резерв
        with open(self.pytj, 'w', encoding="utf8") as f:
            textv = self.text_edit.toPlainText()
            f.write(textv)
        f.close()
            
    def getdials8(self):         # Обновить из файла
        with open(self.pytj, encoding="utf8") as file_l: 
            data = file_l.read()
            self.text_edit.setPlainText(data)                     
        file_l.close() 
        
    def getdials9(self): #Открыть резерв
        print(f"start {self.direktoria1}")
        path = self.direktoria1
        path = os.path.realpath(path)
        os.startfile(path)
    
    def getdials10(self):  #Настройки шрифта        
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_edit.setFont(font)             
            
    def getdials11(self):    #Сохранить как        
        filename_l = QFileDialog.getSaveFileName(self)[0]
        try:
            with open(filename_l, 'w', encoding="utf-8-sig") as f:
                textv = self.text_edit.toPlainText()
                f.write(textv)
            f.close()
        except FileNotFoundError:
            self.statusBar().showMessage(f"None") 
            
    def getdials12(self): #сохранить               
        try:
            with open(self.filename, 'w', encoding="utf-8-sig") as f:
                textv = self.text_edit.toPlainText()
                f.write(textv)
            f.close()            
        except FileNotFoundError:
            self.statusBar().showMessage(f"None")     
                    
    def getdials13(self): #"Открыть"                        
        self.filename = QFileDialog.getOpenFileName(self, caption=("Открыть файл"), filter = ("Файлы локализации (*.yml)"))[0]        
        self.openAfFile()  
    
    def openAfFile(self):  
        if self.filename != "":
            self.statusBar().showMessage(f"Файл: {self.filename}")
            self.filename_q = self.filename
            print("Поток Запущен 11")
            self.setStart_1()            
            self.secondaryPotok.started.connect(self.streamObject1.start6)
            self.setStart_2()        
        else:                
            self.statusBar().showMessage(f"None")  
                         
    def getdials14(self):     #Новое          
        tehc = f"{self.direktoria1}\\fail_l.yml"
        print(f"Yes - {tehc}") 
        self.statusBar().showMessage(f"Yes - {tehc}")   
        with open(tehc, 'w', encoding="utf8") as f:
            textv = self.text_edit.toPlainText()
            f.write(textv)
        f.close()
        self.pytj = tehc
        self.nova_fail = True     
        
    def gettext_r1(self): #"Открыть АЗ"        
        print("Поток Запущен 12")
        self.setStart_1()
        self.secondaryPotok.started.connect(self.streamObject1.start7)
        self.setStart_2()      
    
    def gettext_r2(self):        
        print("Поток Запущен 123")
        self.setStart_1()
        self.secondaryPotok.started.connect(self.streamObject1.start8)
        self.setStart_2()       
        
    def open_TC(self, puti, lovie=None, listOfChangedKeys=None):        
        if listOfChangedKeys != None:
            self.listOfChangedKeys = listOfChangedKeys  # список Измененных Ключей    
        self.filename = puti        
        self.setStart_1(puti, lovie)        
        self.secondaryPotok.started.connect(self.streamObject1.start11)
        self.setStart_2() 
        self.show()                                     
                    
#######################################################################################################################################       
#Функцис выхода#
################

    def closeEvent(self, event): 
        if self.werkil2 == True:   
            self.TextConverter_main.close()  
        self.save_settings()        
        super().closeEvent(event)
        # Закрываем прогресс окно, если оно открыто, перед закрытием основного окна    
             
    def getdials01(self):
        self.TextConverter_main = TextConverter_main()                 
        self.TextConverter_main.show()
               
    def getdials16(self):        
        self.MMTS = ModManagerTranslationsStellaris()         
        self.MMTS.show()
        self.close()
   
########################################################################################################################################################## 

if __name__ == "__main__":
    pass