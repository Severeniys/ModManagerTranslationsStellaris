from file_configuration.MyQFileSystemModel import *
from file_configuration.CreateFolderName import *
from file_configuration.GetDialsThreadComparison import *
from file_configuration.ErrorMessageBox import *

from file_configuration.CreateFolderDialog1 import *
from file_configuration.GetDialsThread2 import *
from file_configuration.CreateFolderDialog import *
from file_configuration.TextConverter_main3 import *


class ModManagerTranslationsStellaris(QMainWindow):
    def __init__(self, parent=None, dir_path=None):
        super().__init__(parent=parent)
        self.objekt = None  # Инициализируем, чтобы можно было проверить, существует ли он
        self.potok = None   # Инициализируем, чтобы можно было проверить, существует ли он
        self.is_processing = False # Флаг, показывающий, идет ли обработка
        self.dirs = os.path.abspath(os.curdir)
        self.werkil3 = False     
           
        self.setWindowTitle("TextConverter - Менеджер")       
        
        self.setWindowIcon(QIcon("TextConverter.ico"))
        
        self.settings1 = QSettings("TextConverter", "my1Settings")        
        
        self.text_wq()
        
        self._createToolBars()    
        
        widget = QWidget()     
        
        self.splitter = QSplitter(self)
        self.setCentralWidget(self.splitter)  
        
        layout = QGridLayout()

        container1 = QWidget()
        container1_layout = QHBoxLayout()
        container1.setLayout(container1_layout)        
        self.qLine1 = QLineEdit()        
        Button11 = QPushButton('Найти')
        Button11.clicked.connect(lambda: self.Button_l1())                
        container1_layout.addWidget(self.qLine1)
        container1_layout.addWidget(Button11)        

        container2 = QWidget()
        container2_layout = QHBoxLayout()
        container2.setLayout(container2_layout)        
        self.qLine2 = QLineEdit()        
        Button21 = QPushButton('Найти')
        Button21.clicked.connect(lambda: self.Button_l2())               
        container2_layout.addWidget(self.qLine2)
        container2_layout.addWidget(Button21)        
        
        Button22 = QPushButton('Обновить Ключи')
        Button22.clicked.connect(lambda: self.Button_poisk(1)) 

        container3 = QWidget()
        container3_layout = QHBoxLayout()
        container3.setLayout(container3_layout)        
        self.qLine3 = QLineEdit()
        Button31 = QPushButton('Найти')
        Button31.clicked.connect(lambda: self.Button_l3())                
        container3_layout.addWidget(self.qLine3)
        container3_layout.addWidget(Button31)
        
        Button32 = QPushButton('Обновить Ключи и Текст')
        Button32.clicked.connect(lambda: self.Button_poisk(2))
        
        container4 = QWidget()
        container4_layout = QVBoxLayout()
        container4.setLayout(container4_layout)        
        Button41 = QPushButton(r'Папка каталога Сборок')
        Button41.clicked.connect(lambda: self.Button_l(self.pyti_modl))        
        Button42 = QPushButton(r'Steam - content')
        Button42.clicked.connect(lambda: self.Button_l(self.pyti_mod))        
        Button43 = QPushButton(r'Stellaris\mod')
        Button43.clicked.connect(lambda: self.Button_l(self.pyti_modll))        
        container4_layout.addWidget(Button41)       
        container4_layout.addWidget(Button42)        
        container4_layout.addWidget(Button43)        

        layout.addWidget(QLabel(r'Файл.yml - russian файл что требуется обновить.'), 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(QLabel(r'Откройте файл для редактирования в TextConverter.'), 1, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(container1, 2, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)        
        layout.addWidget(QLabel(r'Файл.yml - localisation.'), 3, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(QLabel(r'Если добавить путь к файлу из стима алгоритм обновит ключи а устаревшие уберёт.'), 4, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(container2, 5, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop) 
        layout.addWidget(Button22, 6, 2, 1, 1)       
        layout.addWidget(QLabel(r'Файл.yml - localisation rezerv'), 7, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(QLabel(r'Если добавить путь rezerv то алгоритм обновит все изменённые строки с обновлением для перевода.'), 8, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(container3, 9, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop) 
        layout.addWidget(Button32, 10, 2, 1, 1)
        layout.addWidget(container4, 11, 0, 3, 1)       
                 
        widget.setLayout(layout)
       
        self.modell = MyQFileSystemModel()
        self.modell.setReadOnly(True)
        self.modell.setRootPath(dir_path)         
        self.modell.setNameFilters(["*.yml", "*.mod"])
        self.modell.setNameFilterDisables(True)       
        self.tree_view = QTreeView(self)
        
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)     
        self.tree_view.customContextMenuRequested.connect(self.contextMenuEvent)
            
        self.tree_view.setModel(self.modell)
        
        #self.modell.directoryLoaded.connect(lambda: self.handle_index_loaded(self.expanded_items))        
        
        self.tree_view.setColumnWidth(0, 250)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setAnimated(True)
        
        headerl = self.tree_view.header()
        
        headerl.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        headerl.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        headerl.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        headerl.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        self.tree_view.resizeColumnToContents(0)
        self.tree_view.resizeColumnToContents(1)
        self.tree_view.resizeColumnToContents(2)
        self.tree_view.resizeColumnToContents(3)
        
        self.splitter.addWidget(widget)
        self.splitter.addWidget(self.tree_view)   
        
        self.load_settings1() 

        qdarktheme.setup_theme(self.slovar_time)        
              
        self.close()
    
    def text_wq(self):        
        self.text_edit = QTextEdit(self)        
                
        self.setCentralWidget(self.text_edit)       
        
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
                       
        self.statusarr = self.statusBar()
        self.statusBar().setStyleSheet("border :0.5px solid darkGray;")                           
        
        self.statusBar().showMessage(f"Файл не выбран: ")
                
        fonti = self.text_edit.font()          
        self.text_edit.setFont(fonti)    
        
    def toolbtnpressed(self, a):
        action = a.text()
        if action == "Настрока Каталогов":            
            try:            
                self.getdials_1()                
            except BaseException as e: 
                self.statusarr.showMessage(f"None")
        elif action == "Создать каталог":            
            try:            
                self.getdials_2()                
            except BaseException as e: 
                self.statusarr.showMessage(f"None") 
        elif action == "Открыть TextConverter":            
            try:            
                self.perehod()                
            except BaseException as e: 
                self.statusarr.showMessage(f"None")
                
    def perehod(self, treserto = None): #Открыть TextConverter  
        from file_configuration.TextConverter import TextConverter    
        self.textconverter = TextConverter(treserto)              
        self.textconverter.show()                
        self.close()
            
    def _createToolBars(self):        
        self.helpToolBar = QToolBar("File", self)
        self.helpToolBar.setObjectName("toolbar")
        self.addToolBar(self.helpToolBar)    
        
        newor1 = QAction(QIcon(rf"{self.dirs}\katalog\impek\\icons8.png"), "Настрока Каталогов", self)   
        newTipt1 = "Открывает панель для ввода двух файлов локализации для их сравнения и обновления русской за счёт иноязычного файла"
        self.gjlcrfprf(newor1, newTipt1)
        
        newor1 = QAction(QIcon(rf"{self.dirs}\katalog\impek\\icons8-per.png"), "Открыть TextConverter", self)   
        newTipt1 = "Открывает TextConverter"
        self.gjlcrfprf(newor1, newTipt1)
        
        self.helpToolBar.addSeparator()
        
        newor2 = QAction(QIcon(rf"{self.dirs}\katalog\impek\\icons84.png"), "Создать каталог", self)   
        newTipt2 = "Создаёт каталог для заполнения модами"
        self.gjlcrfprf(newor2, newTipt2)
        
        self.helpToolBar.actionTriggered[QAction].connect(self.toolbtnpressed)
        self.helpToolBar.setStyleSheet("color: black")
    
    def gjlcrfprf(self, neve, text):
        self.neve = neve
        self.helpToolBar.addAction(neve)
        self.neve.setStatusTip(text)
        self.neve.setToolTip(text)

######################################################################################################
        
    def contextMenuEvent(self, event): #Контекстное меню
        contextMenu = QMenu(self)
        
        index = self.tree_view.currentIndex() 
        self.path_fail = self.modell.filePath(index)
        self.statusarr.showMessage(f"{self.path_fail}")
        
        open = contextMenu.addAction("Открыть")
        open.triggered.connect(self.open_menu)
        
        if self.path_fail.endswith(".yml"):            
            open_con = contextMenu.addAction("Открыть в TC")
            open_con.triggered.connect(self.open_conec)            
        
        open_name = contextMenu.addAction("Переименовать")
        open_name.triggered.connect(self.open_name)
        
        
        if self.path_fail.endswith(".yml"):
            setmod = contextMenu.addMenu("Добавить в поле редактирования")

            setmod2 = setmod.addAction("russian.yml без rezerv.yml")
            setmod2.triggered.connect(lambda: self.setmod1(2))
            setmod1 = setmod.addAction("russian.yml с rezerv.yml")
            setmod1.triggered.connect(lambda: self.setmod1(1))                 
                
        contextMenu.addSeparator()
        
        if os.path.basename(self.path_fail) in self.get_subdirectories(self.pyti_modl):
            set_k = contextMenu.addAction("Создать каталог")       
            set_k.triggered.connect(self.getdials_2)
            
        set_k = contextMenu.addAction("Скопировать в mod")       
        set_k.triggered.connect(self.getdials_3)  
        
        if self.path_fail.split("/")[-2] in self.get_subdirectories(self.pyti_modl):
            set_k = contextMenu.addAction("Обновить файлы мода")       
            set_k.triggered.connect(self.getdials_4)

            name_ob = contextMenu.addAction("Обновить имя мода")
            name_ob.triggered.connect(self.name_obo) 
        
        if "rezerv" in self.path_fail.split("/")[-1]:
            rezerv_k = contextMenu.addAction("Обновить rezerv")
            rezerv_k.triggered.connect(self.name_obo) 

        if os.path.basename(self.path_fail) in self.get_subdirectories(self.pyti_modl):
            addmod = contextMenu.addMenu("Добавить мод")           
            
            addmode1 = addmod.addAction("Файлы - english")
            addmode1.triggered.connect(lambda: self.addmodf("english"))        
            addmode2 = addmod.addAction("Файлы - russian")
            addmode2.triggered.connect(lambda: self.addmodf("russian"))
            addmode3 = addmod.addAction("Файлы - braz_por")
            addmode3.triggered.connect(lambda: self.addmodf("braz_por"))
            addmode4 = addmod.addAction("Файлы - french")
            addmode4.triggered.connect(lambda: self.addmodf("french"))
            addmode5 = addmod.addAction("Файлы - german")
            addmode5.triggered.connect(lambda: self.addmodf("german"))
            addmode6 = addmod.addAction("Файлы - polish")
            addmode6.triggered.connect(lambda: self.addmodf("polish"))
            addmode7 = addmod.addAction("Файлы - simp_chinese")
            addmode7.triggered.connect(lambda: self.addmodf("simp_chinese"))
            addmode8 = addmod.addAction("Файлы - spanish")
            addmode8.triggered.connect(lambda: self.addmodf("spanish"))             
            
        contextMenu.addSeparator()
        
        delitAction = contextMenu.addAction("Удалить")
        delitAction.triggered.connect(self.open_menu1)        

        contextMenu.exec(self.mapToGlobal(event.pos()))

######################################################################################################
    
    def open_name(self):        
        dialog = CreateFolderName()
        result = dialog.exec()
        if os.path.isfile(self.path_fail):
            py, fa = os.path.split(self.path_fail)
            dialog.folder_name_input.setText(fa)              
        elif os.path.isdir(self.path_fail):
            fa = self.path_fail.split("/")[-1]
            py = "/".join(self.path_fail.split("/")[:-1])
            dialog.folder_name_input.setText(fa)
        if result == QDialog.DialogCode.Accepted:
            folder_name = dialog.folder_name_input.text()                      
            os.chdir(self.pyti_modl)
            os.mkdir(folder_name)            
            os.chdir(self.dirs)                    
        else:
            self.statusarr.showMessage(f"None")
        
    def Button_poisk(self, int):
        if self.is_processing: # Если уже что-то обрабатывается, не запускаем новый поток
            dialog = ErrorMessageBox("Обработка уже выполняется.")
            dialog.exec()
            return
        
        self.setEnabled(False)
        self.is_processing = True # Устанавливаем флаг
         
        if int == 1:
            filename_1_ = self.qLine1.text()
            filename_2_ = self.qLine2.text()                             
            self.objekt = GetDialsThreadComparison(filename_1_, filename_2_)
            self.potok = QThread()
            self.objekt.moveToThread(self.potok)
            self.potok.started.connect(self.objekt.start1)
            self.objekt.finishSignal_1.connect(self.potok.quit)
            self.objekt.finishSignal_1.connect(self.return_function_updates)
            self.objekt.finishSignal_1.connect(self.handle_finish_success)
            self.objekt.finishSignal_error.connect(self.returnFunction_error) 
            self.potok.finished.connect(self.on_thread_finished)
            self.potok.start()
        if int == 2:
            dialog = ErrorMessageBox("Алгоритм пока не готов.")   
            dialog.exec()
            self.setEnabled(True) # Включаем кнопку, так как поток не запускался
            self.is_processing = False # Сбрасываем флаг

    def handle_finish_success(self):
        print("Поток успешно завершил работу.")
        self.reset_state() # Общий метод для сброса состояния

    def on_thread_finished(self):
        print("QThread объект завершил выполнение.")
        pass

    def reset_state(self):
        self.setEnabled(True) # Включаем элементы интерфейса
        self.is_processing = False # Сбрасываем флаг
        # Очищаем ссылки на объекты потока и рабочего, чтобы они могли быть собраны сборщиком мусора
        if self.potok is not None:
            if self.potok.isRunning():
                # Если поток по какой-то причине все еще работает (что не должно случиться при правильном quit/finished),
                # можно попытаться его остановить, но это крайняя мера
                self.potok.quit()
                if not self.potok.wait(2000): # Ждем 2 секунды
                    print("Предупреждение: Поток не завершился вовремя, что привело к принудительному завершению.")
            self.potok = None # Обнуляем ссылку
        if self.objekt is not None:
            self.objekt = None # Обнуляем ссылку closeEvent

    def returnFunction_error(self, error):        
        if error != "":
            dialog = ErrorMessageBox(error)   
            dialog.exec()
        self.reset_state()
        

    def Button_l1(self):
        self.filenamesrt1 = ""
        self.filenamesrt1, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "All Files (*)")
        # Проверяем, был ли выбран файл
        if self.filenamesrt1:
            # Вставляем путь к файлу в QLineEdit
            self.qLine1.setText(self.filenamesrt1)

    def Button_l2(self):
        self.filenamesrt2 = ""
        self.filenamesrt2, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "All Files (*)")
        # Проверяем, был ли выбран файл
        if self.filenamesrt2:
            # Вставляем путь к файлу в QLineEdit
            self.qLine2.setText(self.filenamesrt2)

    def Button_l3(self):
        self.filenamesrt3 = ""
        self.filenamesrt3, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "All Files (*)")
        # Проверяем, был ли выбран файл
        if self.filenamesrt3:
            # Вставляем путь к файлу в QLineEdit
            self.qLine3.setText(self.filenamesrt3)
        
    def Button_l(selfk, pytj):
        os.startfile(pytj)            
    
    def setmod1(self, i):        
        if re.findall(r"vs - \S+ - rezerv", self.path_fail) in self.rezerv:
                dialog = ErrorMessageBox("Этот файл не подлежит копированию в эту строку.")   
                dialog.exec()
                return
        if i == 1:
            if os.path.isfile(self.path_fail):
                self.qLine1.setText(self.path_fail)
                path_fail1 = self.path_fail.replace("vs - russian", "vs - english - rezerv")
                self.qLine3.setText(path_fail1)
        if i == 2:
            if os.path.isfile(self.path_fail):
                self.qLine1.setText(self.path_fail)  
        for i in range(1, 100):                           
            if self.path_fail.split("/")[-i] == "vs - russian":
                ie = i + 1                            
                nomer = re.findall(r"\d+\Z", self.path_fail.split("/")[-ie])
                try:
                    nomer = nomer[0]
                except IndexError:
                    dialog = ErrorMessageBox("Этот мод не имеет номер в своём название для поиска в стим нужного оригинала.")   
                    dialog.exec()
                    return
                break
        i -= 1        
        fail = (self.path_fail.replace("/".join(self.path_fail.split("/")[:-i]), "")).replace("russian", "english")        
        self.qLine2.setText(f"{self.pyti_mod}/{nomer}/localisation{fail}")                    
    
    logger.add(setmod1)

    def name_obo(self):     
        namel = (re.findall(r"\d\d\d\d\d\d\d\d\d+", self.path_fail))[0]        
        last_folderdes = f"{self.pyti_mod}/{namel}/descriptor.mod"        
        try:
            with open(last_folderdes, encoding="utf8") as f:
                self.name_linesi = f.read()                                
            f.close()
        except:
            dialog = ErrorMessageBox("Такого мода нет, скачайте его и повторите.")
            dialog.exec()
            return
        name = re.findall("name=\".+\"", self.name_linesi)[0]           
        for x, y in ("name=\"", ""), \
                    ("\"", ""), \
                    (":", " -"), \
                    ("/", "_"), \
                    ("*", "0"):                
            name = name.replace(x, y)        
        pathe, zero = os.path.split(self.path_fail)        
        pathe = f"{pathe}/{name} - {namel}"
        if os.path.exists(self.path_fail):
            try:
                os.rename(self.path_fail, pathe)
            except (FileNotFoundError, PermissionError, OSError) as e:
                dialog = ErrorMessageBox(f"PermissionError: {e}")   
                dialog.exec()                 
                # Обработка ошибки, если она все же возникает
        else:
            dialog = ErrorMessageBox(f"Файл или папка не найдены: {self.path_fail}")   
            dialog.exec()
                
    
    def open_conec(self):      
        lovie = "try5"
        if os.path.isfile(self.path_fail):
            if re.findall(r"vs - \S+ - rezerv", self.path_fail) in self.rezerv:
                dialog = ErrorMessageBox(r"Я не знаю зачем вам открывать этот файл для редактирования но я это сделаю.")   
                dialog.exec()            
            self.perehod(True)
            self.textconverter.open_TC(self.path_fail, lovie)                                   
        else:
            self.statusarr.showMessage(f"None") 
                    
    def getdials_3(self):      
        self.setStart_1(self.path_fail, self.pyti_modll, self.pyti_modl)
        self.tetr.started.connect(self.objekt.start2)
        self.setStart_2()  
    
    def getdials_4(self):        
        dirs = os.listdir(self.path_fail)        
        for element in dirs:
            if "rezerv" in element:
                words = element.split(' - ')
                for i in range(len(words)):
                    if words[i] == "rezerv":
                        before_word = words[i-1]   
        neme = self.path_fail.split("/")[-2]
        cfro = (re.findall(r"\d\d\d\d\d\d\d\d\d+", self.path_fail))[0]        
        try:
            self.setStart_1(self.path_fail, f"{self.pyti_mod}/{cfro}", self.pyti_modl, before_word, neme)
        except UnboundLocalError as ero:
            self.return_function_1(f"ошибка - {ero}")
        self.tetr.started.connect(self.objekt.start3)
        self.setStart_2()
    
    def addmodf(self, lokal):       
        if os.path.basename(self.path_fail) in self.get_subdirectories(self.pyti_modl):
            last = self.getItemll()                     
            if os.path.basename(self.path_fail) != "":                          
                if last in self.get_subdirectories(self.pyti_mod):
                    pass
                else:                                              
                    dialog = CreateFolderDialog1("Папка не из стим каталога", "Вы уверены что хотите выбрать эту папку?")
                    result = dialog.exec()
                    if result == QDialog.DialogCode.Accepted:  
                        pass
                    else:
                        self.statusarr.showMessage(f"None")
                        return                 
                self.setStart_1(self.path_fail, self.filename_2_, None, lokal)
                self.tetr.started.connect(self.objekt.start1)
                self.setStart_2()                
            else:
                self.statusarr.showMessage(f"None")
        else:
            self.statusarr.showMessage(f"None")            
    
    def getItemll(self):
        self.filename_2_ = QFileDialog.getExistingDirectory(self, caption=("Открыть папку"), directory = self.pyti_mod)
        self.statusarr.showMessage(f"{self.filename_2_}")        
        return os.path.basename(self.filename_2_)        
    
    def open_menu(self):        
        if self.path_fail != "":            
            os.startfile(self.path_fail)  
            self.path_fail = ""  
    
    def open_menu1(self):        
        if self.path_fail != "":            
            self.smart_delete(self.path_fail)
            self.path_fail = ""
 
    def smart_delete(self, path):
        if path.strip() == '':
            self.statusarr.showMessage(f"Указанный путь: {path} - не является файлом или папкой")
            return False            
        if os.path.isdir(path):
            # Если путь - директория, удаляем ее и все содержимое
            self.statusarr.showMessage(f"Удаление каталога и всех его файлов и подкаталогов: {path}")
            self.delete_file_or_folder(path)                 
        elif os.path.isfile(path):
            # Если путь - файл, удаляем файл            
            os.remove(path)
            self.statusarr.showMessage(f"Файл {path} - удален")            
        elif os.path.exists(path):
            # Если путь существует, но не является ни файлом, ни директорией
            self.statusarr.showMessage(f"Неизвестный тип пути: {path}")            
        else:
            # Если путь не существует
            self.statusarr.showMessage(f"Путь не существует: {path}")            
        return True    
            
    def delete_file_or_folder(self, path): 
        try:       
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(path)            
        except:
            dialog = ErrorMessageBox("Ошибка доступа перезагрузите приложение и повторите удаление")
            dialog.exec()       
    
    def get_subdirectories(self, directory):
        subdirectories = []        
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                subdirectories.append(item)
        return subdirectories        
            
    def load_settings1(self):
        self.slovar_time = self.settings1.value("slovar_time", "dark")     
        if self.settings1.value("toolbar_state") is not None:
            self.restoreState(self.settings1.value("toolbar_state"))
        # Загрузка положения и размера окна
        self.resize(self.settings1.value("size", QSize(1564, 772)))
        self.move(self.settings1.value("pos", QPoint(188, 150)))   
        try:     
            self.splitter.restoreState(self.settings1.value("splitter/geometry"))
        except:
            self.statusarr.showMessage(f"Ошибка расположения \"splitter\"")
        self.pyti_mod = self.settings1.value("pyti_mod", "")
        print(self.pyti_mod, 0)
        self.pyti_modl = self.settings1.value("pyti_modl", "")
        self.pyti_modll = self.settings1.value("pyti_modll", "") 
        self.tree_view.setRootIndex(self.modell.index(self.pyti_modl))  
        self.rezerv = ["vs - english - rezerv", 
                  "vs - russian - rezerv",
                  "vs - braz_por - rezerv",
                  "vs - french - rezerv",
                  "vs - german - rezerv",
                  "vs - polish - rezerv",
                  "vs - simp_chinese - rezerv",
                  "vs - spanish - rezerv"]                         
        """
        self.expanded_items = self.settings1.value("expanded_items", None)       
    
    def handle_index_loaded(self, expanded_items):
        print("Запуск каталога")        
        
        selected_indexes = self.tree_view.selectionModel().selectedIndexes()
        print(f"Selected Indexes: {selected_indexes}")
        for index in selected_indexes:
            print(f"Index: {index.row()}-{index.column()}")
                
        if expanded_items is None:            
            return    
        model = self.tree_view.model()
        for item in expanded_items:
            index = model.index(item) 
            widget = self.tree_view.indexWidget(index)           
            if isinstance(widget, QWidget):
                print("Индекс относится к QTreeView")
            else:
                print("Индекс не относится к QTreeView")
            self.tree_view.setExpanded(index, True) 
        """
    def save_settings_pyti(self, pyti_mod, pyti_modl, pyti_modll):
        self.settings1.setValue("pyti_mod", pyti_mod)         
        self.settings1.setValue("pyti_modl", pyti_modl)         
        self.settings1.setValue("pyti_modll", pyti_modll)         
        self.save_settings1()

    def save_settings1(self):
        # Сохранение положения и размера окна
        self.settings1.setValue("pos", self.pos())
        self.settings1.setValue("size", self.size())
        print(self.pyti_mod, 3)
        #if "" not in [self.pyti_mod, self.pyti_modl, self.pyti_modll]: 
            #self.settings1.setValue("pyti_mod", self.pyti_mod)         
            #self.settings1.setValue("pyti_modl", self.pyti_modl)         
            #self.settings1.setValue("pyti_modll", self.pyti_modll) 

        self.settings1.setValue("splitter/geometry", self.splitter.saveState())        
        self.settings1.setValue("toolbar_state", self.saveState())        
        """
        self.settings1.setValue("expanded_items", self.save_treel())
        
    def save_treel(self):
        model = self.tree_view.model()
        indexes = model.persistentIndexList()
        expanded_items = []
        for index in indexes:
            path = model.data(index)
            expanded_items.append(path)
        print(expanded_items)
        return expanded_items
        """
######################################################################################################    
    def setStart_1(self, path_1, path_2, path_3=None, lokal=None, name=None):        
        self.setEnabled(False)            
        self.objekt = GetDialsThread2(path_1, path_2, path_3, lokal, name)
        self.tetr = QThread()
        self.objekt.moveToThread(self.tetr)
        
    def setStart_2(self):
        self.objekt.finishSignal_1.connect(self.tetr.quit)
        self.objekt.finishSignal_1.connect(self.return_function_1)
        self.objekt.finishSignal_2.connect(self.return_function_2)
        self.tetr.start()
    
    def return_function_updates(self, path_fail, stre=None, listOfChangedKeys=None):
        self.setEnabled(True)
        if stre == "None":
            self.statusarr.showMessage("None")
            return
        #lovie = "try4"
        #path_fail = self.qLine1.text()
        #self.perehod(True)
        #self.textconverter.open_TC(path_fail, lovie, listOfChangedKeys) 
        
    def return_function_1(self, text):
        os.chdir(self.dirs)                
        self.setEnabled(True)
        if text != "False":
            dialog = ErrorMessageBox(text)   
            dialog.exec()   
    
    def return_function_2(self, text):    
        self.statusarr.showMessage(text)
        
            
################################################################################################### 
    
    def getItem(self):
        self.filename_1_ = QFileDialog.getOpenFileName(self, caption=("Открыть файл"), filter=("Файлы локализации (*.yml)"))[0]
                
    def getdials_1(self):        
        self.TextConverter_main3 = TextConverter_main3()         
        self.TextConverter_main3.show()        
    
    def getdials_2(self):
        dialog = CreateFolderDialog()
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            folder_name = dialog.folder_name_input.text()
            # Действия при нажатии кнопки "Ок"
            self.statusarr.showMessage(f"Создание папки с именем: {folder_name}")            
            os.chdir(self.pyti_modl)
            os.mkdir(folder_name)
            self.statusarr.showMessage("Текущая директория изменилась на folder:", os.getcwd())
            os.chdir(self.dirs)
            self.statusarr.showMessage("Текущая директория изменилась на folder:", os.getcwd())            
        else:
            # Действия при нажатии кнопки "Отмена"
            self.statusarr.showMessage("Создание папки отменено")            

    def closeEvent(self, event):
    # 1. Проверяем, выполняется ли обработка в потоке
        if self.is_processing and self.potok and self.potok.isRunning():
            # Обработка в потоке активна. Запрашиваем завершение и ждем.

            # 2. Открываем диалог подтверждения закрытия
            reply = QMessageBox.question(self, 'Подтверждение выхода', "Обработка данных еще не завершена. Вы уверены, что хотите выйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # Пользователь подтвердил выход.

                # 3. Запрашиваем завершение потока
                self.potok.quit()

                # 4. Даем потоку время на завершение (используем таймаут)
                if not self.potok.wait(5000):  # Ждем до 5 секунд
                    print("Предупреждение: Поток не завершился вовремя, что привело к принудительному завершению.")

                # 5.  Сохраняем настройки (делаем это *после* подтверждения)
                self.save_settings1()

                # 6. Закрываем дочернее окно, если оно открыто (делаем это *после* подтверждения)
                if self.werkil3 == True:
                    self.TextConverter_main3.close()
                    self.werkil3 = False

                # 7. Принимаем событие закрытия (разрешаем выход)
                event.accept()

            else:
                # Пользователь отменил выход.
                # Отменяем закрытие окна (и оставляем приложение работать).
                event.ignore()
                return # Выходим из функции, не вызывая super().closeEvent

        else:
            # Обработка в потоке не активна.  Просто выполняем стандартные действия.

            # 8. Сохраняем настройки
            self.save_settings1()

            # 9. Закрываем дочернее окно, если оно открыто
            if self.werkil3 == True:
                self.TextConverter_main3.close()
                self.werkil3 = False

            # 10. Принимаем событие закрытия
            event.accept()

        # 11. Вызываем базовый метод (в любом случае)
        super().closeEvent(event)

    '''
    def closeEvent(self, event):       
        self.save_settings1()
        event.accept()
        if self.werkil3 == True:   
            self.TextConverter_main3.close()            
            self.werkil3 = False      
        super().closeEvent(event)  '''