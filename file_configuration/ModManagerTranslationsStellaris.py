
import os
import re
import qdarktheme

# --- Импорты из QtCore ---
# Все, что связано с базовыми типами данных, событиями, таймерами, потоками, настройками
from PyQt6.QtCore import (
    QThread, 
    QSettings,
    Qt,
    QSize,
    QPoint, 
    QThreadPool, 
    QTimer,  
    QByteArray
    )
# --- Импорты из QtGui ---
# Все, что связано с графикой, цветом, шрифтами, иконками, художниками (painter)
from PyQt6.QtGui import (
    QIcon, 
    QAction, 
    QFileSystemModel, 
    QFont 
    )
from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QPushButton,
    QVBoxLayout, 
    QHBoxLayout, 
    QLineEdit, 
    QFileDialog, 
    QToolBar, 
    QMessageBox, 
    QMenuBar, 
    QFontDialog,
    QDialog,
    QTabWidget, 
    QPlainTextEdit,
    QSplitter, 
    QGridLayout, 
    QApplication,  
    QLabel, 
    QTreeView, 
    QHeaderView,     
    QMenu    
)
import functools
from file_configuration.QTextEditWithLineNumber import QTextEditWithLineNumber
from file_configuration.CreateFolderName import CreateFolderName
from file_configuration.GetDialsThreadComparison import GetDialsThreadComparison
from file_configuration.ErrorMessageBox import ErrorMessageBox
from file_configuration.constants import ProcessingConstants
from file_configuration.word_counter import WordCounter, WordCountRunnable
from file_configuration.TextProcessingThread import TextProcessingThread
from file_configuration.LogSettingsDialog import LogSettingsDialog

from file_configuration.CreateFolderDialog1 import CreateFolderDialog1
from file_configuration.LocalisationManagerThread import LocalisationManagerThread
from file_configuration.CreateFolderDialog import CreateFolderDialog


from file_configuration.utils import log_debug, log_error, log_info, log_warning


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

class MyQFileSystemModel(QFileSystemModel):

    def headerData(self, section, _, role):
        if section == 0 and role == Qt.ItemDataRole.DisplayRole:
            return "Имя"
        elif section == 1 and role == Qt.ItemDataRole.DisplayRole:
            return "Размер"
        elif section == 2 and role == Qt.ItemDataRole.DisplayRole:
            return "Тип"
        elif section == 3 and role == Qt.ItemDataRole.DisplayRole:
            return "Дата изменения"

class ModManagerTranslationsStellaris(QMainWindow):
    def __init__(self, project_root, app_data_dir):
        super().__init__()      
        self.project_root = project_root         
        self.app_data_dir = app_data_dir
        self.tetr = None # Хранитель потока
        self.objekt = None # Хранитель объекта  
        self.potok = None   
        self.is_processing = False        
        self.werkil3 = False     
        self.text_edit = None 
        
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        self.status_bar = self.statusBar()        
        self.mode_label = QLabel("Файловый менеджер")
        self.info_label = QLabel("Готов")
        self.status_bar.addPermanentWidget(self.mode_label)
        self.status_bar.addPermanentWidget(self.info_label)        
        
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(1) # Достаточно одного потока для подсчета
        
        self.word_counter = WordCounter()
        # Подключаем сигнал от счетчика к нашему методу обновления интерфейса
        self.word_counter.count_complete.connect(self._update_word_count_ui)
        
        # 3. Таймеры
        self.count_timer = QTimer(self)
        self.count_timer.setSingleShot(True) # Таймер сработает только один раз
        self.count_timer.timeout.connect(self._start_counting_thread)
        
        # 4. Вспомогательные объекты
        self.word_counter = WordCounter()
        self.word_counter.count_complete.connect(self._update_word_count_ui)
        # =======================================================        
        
        self.setWindowTitle("Mod Manager Translations Stellaris")    
        main_icon_path = os.path.join(self.project_root, "file_configuration", "resources", "ModManagerTranslationsStellaris.ico") 

        if os.path.exists(main_icon_path):
            self.setWindowIcon(QIcon(main_icon_path))
        else:
            log_debug(f"Предупреждение: Главный значок приложения не найден по адресу {main_icon_path}")
        
        self.settings = QSettings("ModManagerTranslationsStellaris", "mySettings")   
        self._log_settings_dialog = LogSettingsDialog(self) 
        
        
        self._setup_settings()             
        
        self._central_widget() 
        
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        self._on_tab_changed(self.tab_widget.currentIndex()) # Инициализируем статус при старте
        
        self._potoc_Thread_pool()         
        self.set_language(self.selected_language) # * Устанавливаем галку     
        
        self._setup_seve_file_name()
        
        
        
    def _potoc_Thread_pool(self):        
        
        # 2. Потоки и пулы задач
        self.thread_pool = QThreadPool() # Для "легких" задач вроде подсчета слов
        self.tetr = None # Для "тяжелых" задач (LocalisationManagerThread)
        self.objekt = None
        self.text_processing_thread = TextProcessingThread(
            app_data_dir = self.app_data_dir,            
            text_widget=self.text_edit,
            parent_widget=self, 
            save_result_on_finish=False,
            command="" 
        )     
        
        # === НОВАЯ ИНИЦИАЛИЗАЦИЯ ПОДСЧЕТА СЛОВ ===
        
        self.worker_thread = QThread()
        self.worker_thread.start()                 
        self.text_processing_thread.signal_processed_text.connect(self.returnFunction_linesi)
        self.text_processing_thread.signal_error.connect(self.returnFunction_error)
        self.text_processing_thread.signal_filename.connect(self.returnFunction_filename)
        self.text_processing_thread.signal_processing_path.connect(self.returnFunction_signal_processing_path)
        self.text_processing_thread.signal_task_complete.connect(self.setInit)      
    
    def _central_widget(self):
        """
        Настраивает центральный виджет окна с вкладками.
        """
        # 1. Создаем центральный виджет и основной лайаут
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0) # Убираем отступы, чтобы вкладки "вплотную"
        main_layout.setSpacing(0) # Убираем отступы между элементами
        
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self._setup_file_manager_tab()
        self._setup_text_editor_tab()        
        
        self._create_menubar()
                
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
                
        self._on_tab_changed(self.tab_widget.currentIndex())
        
        
    
    def _setup_file_manager_tab(self):
        """Настраивает вкладку с менеджером файлов и его панелью инструментов."""
        # Создаем главный виджет для этой вкладки    
        
        # Создаем Splitter, который будет разделять наш интерфейс и дерево файлов
        tab_content_widget = QWidget()
        self.splitter = QSplitter(Qt.Orientation.Horizontal) # Горизонтальный разделитель

        # --- Левая часть интерфейса (все ваши кнопки и поля ввода) ---
        left_panel_widget = QWidget()
        left_layout = QGridLayout(left_panel_widget)
        
        # Контейнер 1
        container1 = QWidget()
        container1_layout = QHBoxLayout()
        container1.setLayout(container1_layout)        
        self.qLine1 = QLineEdit()        
        Button11 = QPushButton('Найти')
        Button11.clicked.connect(lambda: self.Button_dirs(1))                
        container1_layout.addWidget(self.qLine1)
        container1_layout.addWidget(Button11)        

        # Контейнер 2
        container2 = QWidget()
        container2_layout = QHBoxLayout()
        container2.setLayout(container2_layout)        
        self.qLine2 = QLineEdit()        
        Button21 = QPushButton('Найти')
        Button21.clicked.connect(lambda: self.Button_dirs(2))               
        container2_layout.addWidget(self.qLine2)
        container2_layout.addWidget(Button21)        
            
        Button22 = QPushButton('Обновить Ключи')
        Button22.clicked.connect(lambda: self.Button_poisk(1)) 

        # Контейнер 3
        container3 = QWidget()
        container3_layout = QHBoxLayout()
        container3.setLayout(container3_layout)        
        self.qLine3 = QLineEdit()
        Button31 = QPushButton('Найти')
        Button31.clicked.connect(lambda: self.Button_dirs(3))                
        container3_layout.addWidget(self.qLine3)
        container3_layout.addWidget(Button31)
        
        Button32 = QPushButton('Обновить Ключи и Текст')
        Button32.clicked.connect(lambda: self.Button_poisk(2))
        
        # Контейнер 4
        container4 = QWidget()
        container4_layout = QVBoxLayout()
        container4.setLayout(container4_layout)        
        Button41 = QPushButton(r'Папка каталога Сборок')
        Button41.clicked.connect(lambda: os.startfile(self.dir_assembling))       
        Button42 = QPushButton(r'Steam - content')
        Button42.clicked.connect(lambda: os.startfile(self.dir_content))       
        Button43 = QPushButton(r'Stellaris\mod')
        Button43.clicked.connect(lambda: os.startfile(self.dir_Stellaris_mod))      
        container4_layout.addWidget(Button41)       
        container4_layout.addWidget(Button42)        
        container4_layout.addWidget(Button43)        

        # Расстановка всех элементов в левой части
        left_layout.addWidget(QLabel(r'Файл.yml - russian файл что требуется обновить.'), 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignBottom)
        left_layout.addWidget(QLabel(r'Откройте файл для редактирования в TextConverter.'), 1, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        left_layout.addWidget(container1, 2, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)        
        left_layout.addWidget(QLabel(r'Файл.yml - localisation.'), 3, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignBottom)
        left_layout.addWidget(QLabel(r'Если добавить путь к файлу из стима алгоритм обновит ключи а устаревшие уберёт.'), 4, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        left_layout.addWidget(container2, 5, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop) 
        left_layout.addWidget(Button22, 6, 2, 1, 1)       
        left_layout.addWidget(QLabel(r'Файл.yml - localisation rezerv'), 7, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignBottom)
        left_layout.addWidget(QLabel(r'Если добавить путь rezerv то алгоритм обновит все изменённые строки с обновлением для перевода.'), 8, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
        left_layout.addWidget(container3, 9, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop) 
        left_layout.addWidget(Button32, 10, 2, 1, 1)
        left_layout.addWidget(container4, 11, 0, 3, 1)       
        left_layout.setColumnStretch(1, 1) # Позволяем колонке 1 растягиваться, чтобы кнопки не прижимались к краю

        # Инициализация модели и дерева, если еще не сделано
        if not hasattr(self, 'modell'):
            self.modell = MyQFileSystemModel()
            self.modell.setReadOnly(True)  
            self.modell.setNameFilters(["*.yml", "*.mod"])
            self.modell.setNameFilterDisables(True)       

        self.tree_view = QTreeView()
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)     
        self.tree_view.customContextMenuRequested.connect(self.contextMenuEvent)
        self.tree_view.setModel(self.modell)
        self.modell.fileRenamed.connect(self._on_file_renamed)
        
        self.tree_view.setColumnWidth(0, 250)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setAnimated(True)
        
        header = self.tree_view.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        self.splitter.addWidget(left_panel_widget)
        self.splitter.addWidget(self.tree_view)
        
        # Восстанавливаем состояние разделителя, если оно сохранено
        if hasattr(self, 'splitter_geometry') and isinstance(self.splitter_geometry, QByteArray):
            try:
                self.splitter.restoreState(self.splitter_geometry)
                log_debug("Состояние сплиттера успешно восстановлено.")
            except Exception as e:
                log_error(f"Ошибка при восстановлении состояния сплиттера: {e}.", exc_info=True)
        else:
            log_debug("Не удалось получить корректное состояние сплиттера. Используется состояние по умолчанию.")
        #if hasattr(self, 'splitter_geometry'):
        #    self.splitter.restoreState(self.splitter_geometry)
        
        # Устанавливаем корневой путь для дерева и настраиваем его отображение
        self.modell.setRootPath(self.dir_assembling)
        index_to_show = self.modell.index(self.dir_assembling)
        self.tree_view.setRootIndex(index_to_show)
        self.tree_view.expand(index_to_show)
        
        # --- Финал: возвращаем собранный интерфейс для добавления на вкладку ---
        self.tab_widget.addTab(self.splitter, "Менеджер модов")
        log_debug("Вкладка 'Менеджер модов'")
        
    def _setup_text_editor_tab(self):
        """
        Настраивает виджет с текстовым редактором для второй вкладки.
        Использует общую для окна строку состояния.
        """
        # * Создаем основной виджет, который будет лежать на вкладке
        editor_widget = QWidget()

        # * Создаем лайаут для этого виджета
        layout = QVBoxLayout(editor_widget)
        layout.setContentsMargins(5, 5, 5, 5)

        # 2. Создаем и добавляем панель инструментов
        self.editor_toolbar = self._create_text_editor_toolbar()
        layout.addWidget(self.editor_toolbar)
        
        # * Используем вашу существующую логику инициализации редактора
        self.text_edit = QTextEditWithLineNumber()
        self.text_edit.enableSyntaxHighlighting(True)        
        self.text_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.text_edit.textChanged.connect(self._on_text_changed) 
        self.text_edit.cursorPositionChanged.connect(self._update_selection_info)
        layout.addWidget(self.text_edit)        
        # * Добавляем готовый виджет на вторую вкладку
        self.tab_widget.addTab(editor_widget, "Текстовый редактор")    
        
        log_debug("Вкладка 'Текстовый редактор' настроена.")
        
    def _create_menubar(self):
        """Создает верхнее меню."""        
        self.menuBar = QMenuBar(self)        
        self.setMenuBar(self.menuBar)
        self.menu_file_bar = QMenu("&Файл", self)
        self.menuBar.addMenu(self.menu_file_bar)
        self.menu_tools_bar = QMenu("&Инструменты", self)
        self.menuBar.addMenu(self.menu_tools_bar)
        self.menu_analysis_bar = QMenu("&Анализ", self)
        self.menuBar.addMenu(self.menu_analysis_bar)
        self.menu_options_bar = QMenu("&Опции", self)
        self.menuBar.addMenu(self.menu_options_bar)
        
        neve1 = self.menu_file_bar.addAction("Новое")
        newTip1 = "Создание резервного файла для небольшого текста"
        self.set_tooltip_and_status_tip(neve1, newTip1)
        neve1.triggered.connect(lambda: self.getdials14()) 
                
        neve2 = self.menu_file_bar.addAction("Открыть")
        newTip2 = "Открытие файла *.yml"
        self.set_tooltip_and_status_tip(neve2, newTip2)
        neve2.triggered.connect(lambda: self.getdials13())
        
        self.menu_file_bar.addSeparator()
        
        neve3 = self.menu_file_bar.addAction("Сохранить")
        newTip3 = "Сохранить в ту же папку"
        self.set_tooltip_and_status_tip(neve3, newTip3)
        neve3.triggered.connect(lambda: self.getdials12())
        
        neve4 = self.menu_file_bar.addAction("Сохранить как")
        newTip4 = "Выбрать папку для сохранения"
        self.set_tooltip_and_status_tip(neve4, newTip4)
        neve4.triggered.connect(lambda: self.getdials11())
        
        self.menu_file_bar.addSeparator()
        
        neve51 = self.menu_file_bar.addAction("Открыть резерв")
        newTip51 = "Открыть паку куда сохранён файлы после конвертации для перевода в другом редакторе"
        self.set_tooltip_and_status_tip(neve51, newTip51)
        neve51.triggered.connect(lambda: self.getdials9())
        
        neve52 = self.menu_file_bar.addAction("Обновить из файла")
        newTip52 = "Обновления из резервного файла если вы переводите не в TextConverter"
        self.set_tooltip_and_status_tip(neve52, newTip52)
        neve52.triggered.connect(lambda: self.getdials8())
        
        neve53 = self.menu_file_bar.addAction("Закрыть файл")
        newTip53 = "Закрытие открытого файл без сохранение стирание текста"
        self.set_tooltip_and_status_tip(neve53, newTip53)
        neve53.triggered.connect(lambda: self.CloseTheFile()) 
        
        neve6 = self.menu_tools_bar.addAction("Упаковка ссылок")
        newTip6 = "Все ссылки в открытом в редакторе текста будут зашифрованы для дальнейшего перевода в переводчике"
        self.set_tooltip_and_status_tip(neve6, newTip6)
        neve6.triggered.connect(lambda: self.getdials6())
        
        neve7 = self.menu_tools_bar.addAction("Упаковка ключей")
        newTip7 = "Все ключи в открытом в редакторе текста будут зашифрованы для дальнейшего перевода в переводчике"
        self.set_tooltip_and_status_tip(neve7, newTip7)
        neve7.triggered.connect(lambda: self.getdials4()) 
        
        self.menu_tools_bar.addSeparator()
        
        neve8 = self.menu_tools_bar.addAction("Распаковка")
        newTip8 = "Всё зашифрованное в тесте будет расшифровано применяется когда вы завершили перевод"
        self.set_tooltip_and_status_tip(neve8, newTip8)
        neve8.triggered.connect(lambda: self.getdials3())   
        
        neve9 = self.menu_analysis_bar.addAction("Замена по словарю")
        newTip9 = "Заменяет по составленному списку выражения в тексте."
        self.set_tooltip_and_status_tip(neve9, newTip9)
        neve9.triggered.connect(lambda: self.getdials5())
        
        neve91 = self.menu_analysis_bar.addAction("Очистка #Новых строк")
        newTip91 = "Очищает текст от коментариев о новой строке"
        self.set_tooltip_and_status_tip(neve91, newTip91)
        neve91.triggered.connect(lambda: self.getdials51())
        
        neve10 = self.menu_options_bar.addAction("Очистить директорию резерва")
        newTip10 = "Всё зашифрованное в тесте будет расшифровано применяется когда вы завершили перевод"
        self.set_tooltip_and_status_tip(neve10, newTip10)
        neve10.triggered.connect(lambda: self.getdials1()) 
        
        self.menu_options_bar.addSeparator()
        
        neve15 = impAct2 = self.menu_options_bar.addMenu("Настройки")
        newTip15 = "Всё зашифрованное в тесте будет расшифровано применяется когда вы завершили перевод"
        self.set_tooltip_and_status_tip(neve15, newTip15)        
        
        neve16 = impAct2.addAction("Настройки шрифта")
        newTip16 = "Меню настрока шрифта"
        self.set_tooltip_and_status_tip(neve16, newTip16)
        neve16.triggered.connect(lambda: self.getdials10()) 
        
        neve20 = impAct2.addAction("Настройка темы")
        newTip20 = "Настройка темы"
        self.set_tooltip_and_status_tip(neve20, newTip20)
        neve20.triggered.connect(lambda: self.getdials01()) 
        
        neve11 = impAct1 = impAct2.addMenu("Настроить: Анализ-Замена")
        newTip11 = "Настройка словаря замены: слева то что заменяется тем что справо при редактирование придерживайтесь общей структуре."
        self.set_tooltip_and_status_tip(neve11, newTip11)        
        
        neve12 = impAct1.addAction("Открыть АЗ")
        newTip12 = "Открывает словарь в редакторе"
        self.set_tooltip_and_status_tip(neve12, newTip12)
        neve12.triggered.connect(lambda: self.gettext_r1())
        
        neve13 = impAct1.addAction("Закрыть АЗ")
        newTip13 = "Сохраняет и закрывает словарь"
        self.set_tooltip_and_status_tip(neve13, newTip13)
        neve13.triggered.connect(lambda: self.gettext_r2())
        
        self.language_menu = QMenu("Язык интерфейса", self)
        self.menu_options_bar.addMenu(self.language_menu)        
        self.language_actions = {}
        languages = ["Russian", "English", "French", "German", "Japanese", "Korean", "Polish", "Simp_chinese", "Spanish", "Braz_por"] # Список языков
        for lang in languages:
            action = QAction(lang, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, lang=lang: self.set_language(lang)) # Обработчик выбора
            self.language_menu.addAction(action)
            self.language_actions[lang] = action        
        
        neve21 = impAct2.addAction("Настрока Каталогов")
        newTip21 = "Настрока Каталогов"
        self.set_tooltip_and_status_tip(neve21, newTip21)
        neve21.triggered.connect(lambda: self.getdials_1()) 
        
        log_settings_action = self.menu_options_bar.addAction("Настройки логирования...")
        log_settings_action.triggered.connect(self._open_log_settings_dialog)
        
        log_debug("Верхнее меню создано.")
        
    def set_tooltip_and_status_tip(self, neve, text):
        self.neve = neve
        self.neve.setStatusTip(text)
        self.neve.setToolTip(text)  
        
    def _on_tab_changed(self, index):
        """
        Слот, который вызывается при переключении вкладок.
        Обновляет меню, строки состояния и активность пунктов меню.
        """
        log_debug(f"СЛОТ _on_tab_changed ВЫЗВАН с индексом: {index}")
        
        if not hasattr(self, 'tab_widget') or self.tab_widget is None:
            log_error("КРИТИЧЕСКАЯ ОШИБКА: self.tab_widget не существует в _on_tab_changed.")
            return

        tab_text = self.tab_widget.tabText(index)
        log_debug(f"Текст активной вкладки: '{tab_text}'")
        
        # Проверка существования меню перед их использованием
        if hasattr(self, 'menu_tools_bar'):
            log_debug("Меню 'Инструменты' найдено.")
            self.menu_tools_bar.setEnabled(True)
        else:
            log_warning("Меню 'Инструменты' (self.menu_tools_bar) не найдено! Вероятно, _create_menubar не был вызван.")

        # --- 1. Управление видимостью панелей инструментов (остается без изменений) ---
        if hasattr(self, 'editor_toolbar') and self.editor_toolbar is not None:
            self.editor_toolbar.setVisible(False)
        if hasattr(self, 'manager_toolbar') and self.manager_toolbar is not None:
            self.manager_toolbar.setVisible(False)
        
        # --- 2. Управление АКТИВНОСТЬЮ МЕНЮ ---
        # Сначала выключаем все, кроме "Опции"
        # ! Используем сохраненные ссылки на меню
        self.menu_file_bar.setEnabled(False)
        self.menu_tools_bar.setEnabled(False)
        self.menu_analysis_bar.setEnabled(False)
        # Опции всегда включены
        self.menu_options_bar.setEnabled(True) 

        # Включаем нужные в зависимости от активной вкладки
        tab_text = self.tab_widget.tabText(index)        
                
        if tab_text == "Менеджер модов":
            # * Включаем меню, релевантные менеджеру модов
            self.menu_file_bar.setEnabled(False)
            self.menu_tools_bar.setEnabled(False)
            self.menu_analysis_bar.setEnabled(False) # Анализ модов тоже здесь может быть
            
            self.mode_label.setText(tab_text)
            
            log_error("Переключено на 'Менеджер модов'")

            # Показываем панель инструментов для менеджера файлов
            if hasattr(self, 'manager_toolbar') and self.manager_toolbar is not None:
                self.manager_toolbar.setVisible(True)

        elif tab_text == "Текстовый редактор":
            # * Включаем меню, релевантные редактору
            self.menu_file_bar.setEnabled(True)
            self.menu_tools_bar.setEnabled(True)
            self.menu_analysis_bar.setEnabled(True) # Анализ текста, поиск и т.д.            
            
            self.mode_label.setText(tab_text)
                        
            log_error("Переключено на 'Текстовый редактор'")

            # Показываем панель инструментов для редактора
            if hasattr(self, 'editor_toolbar') and self.editor_toolbar is not None:
                self.editor_toolbar.setVisible(True)
                
        else:
            self.statusBar().showMessage("Готово")
        
    def _start_counting_thread(self):
        """Запускает задачу подсчета в отдельном потоке."""
        try:
            if self.text_edit is None:
                log_error("КРИТИЧЕСКАЯ ОШИБКА: self.text_edit равен None! Счетчик работать не будет.")
                self._update_word_count_ui(0, 0)
                return
            
            text = self.text_edit.toPlainText() 
            if not text:
                self._update_word_count_ui(0, 0)
                return
                
            runnable = WordCountRunnable(text, self.word_counter)
            self.thread_pool.start(runnable)
        except Exception as e:
            log_error(f"in _start_counting_thread: {str(e)}")

    def _on_text_changed(self):        
        """Вызывается при любом изменении текста."""
        self.count_timer.start(500) # 500 миллисекунд паузы       

    def _update_word_count_ui(self, word_count: int, char_count: int):
        """Обновляет интерфейс с новыми подсчетами общего текста."""
        try:
            # Обновляем, только если в данный момент нет активного выделения
            if not hasattr(self, '_last_selection_count'):
                self.info_label.setText(f"Слов = {word_count}, Знаков = {char_count}")
        except Exception as e:
            log_error(f"in _update_word_count_ui: {str(e)}")
            
    def _update_selection_info(self):
        """Обновляет информацию о выделенном тексте."""
        
        try:
            if not self.text_edit:
                return
                
            cursor = self.text_edit.textCursor()
            
            if cursor.hasSelection():
                selected_text = cursor.selectedText()
                char_count = len(selected_text)
                
                # Проверим, что выделение действительно изменилось
                if not hasattr(self, '_last_selection_count') or self._last_selection_count != char_count:
                    self.info_label.setText(f"Выделено: {char_count} зн.")
                    self._last_selection_count = char_count
            else:
                # Если выделения нет
                if hasattr(self, '_last_selection_count'):
                    del self._last_selection_count
                    # После отмены выделения, сразу пересчитываем общее количество слов
                    self._start_counting_thread()
                    
        except Exception as e:
            log_error(f"in _update_selection_info: {e}")
                
    def _create_text_editor_toolbar(self):
        """
        Создает и настраивает панель инструментов для вкладки 'Текстовый редактор'.
        """
        # 1. Создаем новую панель инструментов для редактора
        toolbar = QToolBar("Инструменты редактора", self)
        toolbar.setObjectName("editor_toolbar")
        toolbar.setMovable(False) # Обычно панели инструментов закрепляют
        
        # 2. Настраиваем иконки и действия для этой панели
        icons_dir = os.path.join(self.project_root, "file_configuration", "resources", "icons")
        
        log_debug(icons_dir)

        # --- Action 1: Преобразовать и скопировать ---
        icon_path_conv_copy = os.path.join(icons_dir, "icons_2.png")
        icon_conv_copy = QIcon(icon_path_conv_copy) if os.path.exists(icon_path_conv_copy) else QIcon()
        action_conv_copy = QAction(icon_conv_copy, "Преобразовать, Копировать", self)
        
        # ! Используем современный подход: устанавливаем подсказки прямо при создании QAction
        action_conv_copy.setStatusTip("Вставьте короткий текст и нажмите, чтобы зашифровать ключи и ссылки и сразу скопировать в буфер обмена.")
        action_conv_copy.setToolTip("Преобразовать, Копировать")
        action_conv_copy.triggered.connect(lambda: self.getdials17())
        
        toolbar.addAction(action_conv_copy)

        toolbar.addSeparator() # Добавляем разделитель для красоты

        # --- Action 2: Вставить, преобразовать и скопировать ---
        icon_path_paste_conv = os.path.join(icons_dir, "icons_3.png")
        icon_paste_conv = QIcon(icon_path_paste_conv) if os.path.exists(icon_path_paste_conv) else QIcon()
        action_paste_conv = QAction(icon_paste_conv, "Вставить, Преобразовать, Копировать", self)
        
        action_paste_conv.setStatusTip("Переведя текст, нажмите, чтобы вставить текст из буфера обмена, расшифровать и затем получить обратно его в буфер обмена.")
        action_paste_conv.setToolTip("Вставить, Преобразовать, Копировать")
        action_paste_conv.triggered.connect(lambda: self.getdials18())

        toolbar.addAction(action_paste_conv)
        
        # 3. Применяем стили к этой конкретной панели
        toolbar.setStyleSheet("color: black")
        
        # 4. Возвращаем готовую панель, чтобы ее можно было добавить на вкладку
        return toolbar        
        
######################################################################################################
        
    def contextMenuEvent(self, event): #Контекстное меню
        
        contextMenu = QMenu(self)
        
        index = self.tree_view.currentIndex() 
        self.path_fail = self.modell.filePath(index)
        self.statusBar().showMessage(f"{self.path_fail}")
        
        # --- Логика для ПАПОК ---
        if os.path.isdir(self.path_fail):
            open_action = contextMenu.addAction("Открыть папку")
            open_action.triggered.connect(lambda: os.startfile(self.path_fail))
            
            open_name = contextMenu.addAction("Переименовать")
            open_name.triggered.connect(self.open_rename_dialog)
            
            open_steam_action = contextMenu.addAction("Открыть в Steam")
            open_steam_action.triggered.connect(self.open_steam_mod_folder_by_id)
        
        elif os.path.isfile(self.path_fail):
            open_action = contextMenu.addAction("Открыть файл")
            open_action.triggered.connect(lambda: os.startfile(self.path_fail))
                        
            open_con = contextMenu.addAction("Открыть в редакторе")
            open_con.triggered.connect(lambda checked, path=self.path_fail: self._handle_open_in_editor(path))            
        
            open_name = contextMenu.addAction("Переименовать")
            open_name.triggered.connect(self.open_rename_dialog)        
        
            setmod = contextMenu.addMenu("Добавить в поле редактирования")

            setmod2 = setmod.addAction("russian.yml без rezerv.yml")
            setmod2.triggered.connect(lambda: self.set_mod_name(2))
            setmod_name = setmod.addAction("russian.yml с rezerv.yml")
            setmod_name.triggered.connect(lambda: self.set_mod_name(1))                 
                
        contextMenu.addSeparator()
        
        if os.path.basename(self.path_fail) in self.get_subdirectories(self.dir_assembling):
            set_k = contextMenu.addAction("Создать каталог")       
            set_k.triggered.connect(self.getdials_2)
            
        set_k = contextMenu.addAction("Скопировать в mod")       
        set_k.triggered.connect(self.copy_mod_to_game_folder)  
        
        if self.path_fail.split("/")[-2] in self.get_subdirectories(self.dir_assembling):
            set_k = contextMenu.addAction("Обновить файлы мода")       
            set_k.triggered.connect(self.start_mod_update_from_steam)

            name_ob = contextMenu.addAction("Обновить имя мода")
            name_ob.triggered.connect(self.name_obo) 
        
        if "rezerv" in self.path_fail.split("/")[-1]:
            rezerv_k = contextMenu.addAction("Обновить rezerv")
            rezerv_k.triggered.connect(self.name_obo) 

        if os.path.basename(self.path_fail) in self.get_subdirectories(self.dir_assembling):
            addmod = contextMenu.addMenu("Добавить мод")
            
            languages = ProcessingConstants.LOCALISATION
            log_debug(f"DEBUG: contextMenuEvent - languages = {languages}")  
            
            for lang in languages:   
                addmode = addmod.addAction(f"Файлы - {lang}")
                addmode.triggered.connect(functools.partial(self.addmodf, lang))            
            
        contextMenu.addSeparator()
        
        delitAction = contextMenu.addAction("Удалить")
        delitAction.triggered.connect(self.open_menu1)        
        contextMenu.exec(self.mapToGlobal(event.pos()))
        
######################################################################################################
    def _handle_open_in_editor(self, file_path: str):
        """
        Открывает указанный yml-файл в редакторе на второй вкладке.
        Переключает фокус на вкладку редактора.
        """
        log_info(f"Обработка открытия файла в редакторе: {file_path}")

        # 1. Проверяем существование файла
        if not os.path.isfile(file_path):
            log_error(f"Попытка открыть несуществующий файл: {file_path}")
            self.statusBar().showMessage(f"Ошибка: файл не найден.", 5000) # Показать на 5 секунд
            return
        editor_tab_index = 1 
        self.tab_widget.setCurrentIndex(editor_tab_index)
        self.file_name = file_path
        log_info(f"Переключены на вкладку '{self.tab_widget.tabText(editor_tab_index)}'.")

        # 4. Загружаем содержимое файла в наш текстовый редактор
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.text_edit.setPlainText(content)
            
            # 5. Обновляем статус-бар
            file_name = os.path.basename(file_path)            
            log_info(f"Файл '{file_name}' успешно загружен.")

        except Exception as e:
            log_error(f"Не удалось прочитать файл {file_path}: {e}")
            
            
    def open_steam_mod_folder_by_id(self):
        """
        Открывает папку мода в директории Steam по его ID.
        """
        log_debug(f"Попытка открыть папку мода ID в Steam.")
        
        steam_mods_dir = self.dir_content 
        
        folder_name = os.path.basename(self.path_fail)
        match = re.search(r"\d{9,10}", folder_name)
        if match:
            mod_id = match.group(0)
            
        mod_folder_path = os.path.join(steam_mods_dir, mod_id)
            
        if os.path.isdir(mod_folder_path):
            log_debug(f"Открываю папку: {mod_folder_path}")            
            os.startfile(mod_folder_path)
        else:
            log_error(f"Папка мода ID {mod_id} не найдена по пути: {mod_folder_path}")
            ErrorMessageBox.show_error(f"Не удалось найти папку мода в Steam. Возможно, мод был удален.")
            
    def open_rename_dialog(self):
        """
        Открывает диалог CreateFolderName для переименования выбранной папки или .yml файла.
        """
        log_debug("Запрошено переименование элемента.")
        
        # 1. Проверяем, что что-то выбрано
        if not self.path_fail:
            log_error("Для переименования выберите элемент (папку или файл) в списке.")
            return
        # 2. Проверяем, что элемент существует
        if not os.path.exists(self.path_fail):
            log_error("Выбранный элемент не существует.")
            return
        # 3. Определяем, что это: папка или файл?
        is_directory = os.path.isdir(self.path_fail)
        current_name = os.path.basename(self.path_fail)        
        log_debug(f"Текущий элемент: {self.path_fail} (Папка: {is_directory}, Текущее имя: '{current_name}')")
        # 4. Создаем и настраиваем диалог
        dialog = CreateFolderName(self) # Передаем self как родителя для правильного отображения
        
        # ВАЖНО: Устанавливаем текст метки в зависимости от типа элемента
        if is_directory:
            dialog.findChild(QLabel).setText("Введите новое имя для папки:")
        else:
            dialog.findChild(QLabel).setText("Введите новое имя для файла (расширение .yml будет добавлено, если его нет):")

        # 5. Вставляем текущее имя в поле ввода
        dialog.folder_name_input.setText(current_name)        
        # Устанавливаем фокус в поле ввода, чтобы пользователь сразу мог печатать
        dialog.folder_name_input.setFocus()
        # Выделяем весь текст, чтобы легко было его стереть и написать новое
        dialog.folder_name_input.selectAll()
        # 6. Показываем диалог и ждем результата
        result = dialog.exec()
        # 7. Если пользователь нажал "OK"
        if result == QDialog.DialogCode.Accepted:
            new_name = dialog.folder_name_input.text().strip() # Получаем имя и убираем пробелы по краям
            if not new_name:
                QMessageBox.warning(self, "Предупреждение", "Имя не может быть пустым.")
                log_debug("Предупреждение мя не может быть пустым.")
                return
            if new_name == current_name:
                log_debug("Новое имя совпадает со старым, переименование отменено.")
                return
            # Обработка имени для файла
            if not is_directory:
                # Убираем старое расширение, если пользователь его ввел
                base_name, _ = os.path.splitext(new_name)
                # Добавляем наше стандартное расширение
                clean_new_name = base_name + ".yml"
            else:
                # Для папки просто очищаем от "опасных" символов
                clean_new_name = new_name.replace('/', '_').replace('\\', '_').replace(':', ' -')

            new_path = os.path.join(os.path.dirname(self.path_fail), clean_new_name)
            
            try:
                # 8. Переименовываем папку или файл
                os.rename(self.path_fail, new_path)
                log_debug(f"Элемент успешно переименован: {self.path_fail} -> {new_path}")
                parent_index = self.modell.index(self.dir_assembling)
                self.tree_view.setRootIndex(parent_index)
                self.tree_view.expand(parent_index)
                # 9. Обновляем интерфейс
                # Важно: обновляем сохраненный путь, чтобы он вёл к новому имени
                self.path_fail = new_path
                # Обновляем представление дерева
                self.tree_view.setRootIndex(self.modell.index(self.dir_assembling))
                # Раскрываем родительскую папку, чтобы изменения были видны
                self.tree_view.expand(self.modell.index(self.dir_assembling))
                
                log_info(f"Элемент переименован в '{clean_new_name}'.")

            except FileExistsError:
                QMessageBox.critical(self, "Ошибка", f"Не удалось переименовать.\nЭлемент с именем '{clean_new_name}' уже существует.")
                log_error(f"Ошибка при переименовании: элемент '{clean_new_name}' уже существует.")
            except PermissionError:
                QMessageBox.critical(self, "Ошибка", "Не удалось переименовать.\nНет прав на доступ к файлу/папке.")
                log_error(f"Ошибка при переименовании: PermissionError для {self.path_fail}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Произошла неизвестная ошибка:\n{e}")
                log_error(f"Неизвестная ошибка при переименовании: {e}")
        else:
            # Пользователь нажал "Отмена"
            log_debug("Переименование отменено пользователем.")   
            
        
    def Button_poisk(self, int):
        if self.is_processing: # Если уже что-то обрабатывается, не запускаем новый поток
            ErrorMessageBox.show_error("Обработка уже выполняется.")            
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
        elif int == 2:
            ErrorMessageBox.show_error("Алгоритм пока не готов.")    
            log_debug("Алгоритм пока не готов.")
            self.setEnabled(True) # Включаем кнопку, так как поток не запускался
            self.is_processing = False # Сбрасываем флаг

    def handle_finish_success(self):
        log_debug("Поток успешно завершил работу.")
        self.reset_state() # Общий метод для сброса состояния

    def on_thread_finished(self):
        log_debug("QThread объект завершил выполнение.")
        pass

    def reset_state(self):
        self.setEnabled(True) # Включаем элементы интерфейса
        log_debug("Интерфейс включён")
        self.is_processing = False # Сбрасываем флаг        
        if self.potok is not None:
            if self.potok.isRunning():                
                self.potok.quit()
                if not self.potok.wait(2000): # Ждем 2 секунды
                    log_debug("Предупреждение: Поток не завершился вовремя, что привело к принудительному завершению.")
            self.potok = None # Обнуляем ссылку
        if self.objekt is not None:
            self.objekt = None # Обнуляем ссылку closeEvent

    def returnFunction_error(self, error):
        self.reset_state()        
        if error != "":
            ErrorMessageBox.show_error(error)  
            log_error(f"{error}")     
        
        

    def Button_dirs(self, nomer):
        #self.filenamesrt1 = ""
        filenamesrt, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "All Files (*)")
        # Проверяем, был ли выбран файл
        if filenamesrt:
            if nomer == 1:           
                self.qLine1.setText(filenamesrt)
            elif nomer == 2:
                self.qLine2.setText(filenamesrt)
            elif nomer == 3:
                self.qLine3.setText(filenamesrt)
            
    def Button_l(selfk, pytj):
        os.startfile(pytj)            
    
    def set_mod_name(self, i):
        source_language = self._extract_source_language_from_rezerv(self.path_fail)                
        if re.findall(ProcessingConstants.REZERV_S, self.path_fail) in self.rezerv:
                ErrorMessageBox.show_error("Этот файл не подлежит копированию в эту строку.")              
                return
        if i == 1:
            if os.path.isfile(self.path_fail):
                self.qLine1.setText(self.path_fail)
                path_fail1 = self.path_fail.replace(f"vs - {self.localisation}", f"vs - {source_language} - rezerv")
                self.qLine3.setText(path_fail1)
        if i == 2:
            if os.path.isfile(self.path_fail):
                self.qLine1.setText(self.path_fail)  
        for i in range(1, 100):                           
            if self.path_fail.split("/")[-i] == f"vs - {self.localisation}":
                ie = i + 1                            
                nomer = re.findall(r"\d+\Z", self.path_fail.split("/")[-ie])
                try:
                    nomer = nomer[0]
                except IndexError:
                    ErrorMessageBox.show_error("Этот мод не имеет номер в своём название для поиска в стим нужного оригинала.")                    
                    return
                break
        i -= 1        
        fail = (self.path_fail.replace("/".join(self.path_fail.split("/")[:-i]), "")).replace(self.localisation, source_language)        
        self.qLine2.setText(f"{self.dir_content}/{nomer}/localisation{fail}")                    
        
    def name_obo(self):     
        if not self.dir_content or not os.path.isdir(self.dir_content):
            self.statusBar().showMessage("Ошибка: Путь к папке модов Steam не настроен.")
            QMessageBox.warning(self, "Ошибка конфигурации", "Путь к папке `steamapps/workshop/content` не найден.")
            return            

        self._start_task(
            task_name='update_mod_name',
            source_dir=None,
            source_language=None
        )
        
    def open_conec(self):      
        lovie = "try5"
        if os.path.isfile(self.path_fail):
            if re.findall(ProcessingConstants.REZERV_S, self.path_fail) in self.rezerv:
                ErrorMessageBox.show_error("Я не знаю зачем вам открывать этот файл для редактирования но я это сделаю.") 
            self.perehod()
            self.textconverter.open_TC(self.path_fail, lovie=lovie)                                   
        else:
            self.statusBar().showMessage(f"None")
                    
    def copy_mod_to_game_folder(self):
        """Копирует готовый перевод в папку mod игры."""
        log_debug("Запрос на КОПИРОВАНИЕ в папку mod.")
                
        source_dir = self.dir_assembling # Папка Сборки
        stellaris_dir = self.dir_Stellaris_mod # Папка с модами Stellaris
        
        # Язык берем из настроек или определяем из папки            
        
        self._start_task(
            task_name='copy_to_game_mod',
            source_dir=source_dir,
            stellaris_dir=stellaris_dir                
        )
        
    
    def start_mod_update_from_steam(self):
        """
        Запускает процесс ОБНОВЛЕНИЯ выбранной папки в Сборке из Steam.
        Язык для обновления определяется автоматически по папке 'rezerv'.
        """
        log_debug("Запрос на ОБНОВЛЕНИЕ файлов мода.")        

        # 2. Автоматически определяем язык-источник из папки 'rezerv'
        source_language = self._extract_source_language_from_rezerv(self.path_fail)
        
        if not source_language:
            self.statusBar().showMessage("Ошибка: Не удалось определить язык мода для обновления.")
            ErrorMessageBox.show_error("В папке мода не найдена подпапка 'vs - <язык> - rezerv' или язык некорректен.", "Ошибка языка")
            return

        # 3. Пользователь выбирает папку МОДА ИЗ STEAMA, который будет источником файлов
        steam_mods_dir = self.dir_content 
        
        folder_name = os.path.basename(self.path_fail)
        match = re.search(r"\d{9,10}", folder_name)
        if not match:
            ErrorMessageBox.show_error("Не удалось найти ID мода в имени папки.")
            return
        mod_id = match.group(0)
        
        selected_steam_mod_path = os.path.join(steam_mods_dir, mod_id)

        # 4. Запускаем задачу обновления с найденным языком
        self._start_task(
            task_name='update_files',
            source_dir=selected_steam_mod_path, # Папка в Steam
            source_language=source_language      # Язык, найденный автоматически
        )
        
    def addmodf(self, source_lang_code):
        """
        Запускает подготовку к переводу.
        :param source_lang_code: Код языка, ИЗ КОТОРОГО будем переводить (например, 'english').
        """
        log_debug(f"Запрос на ПОДГОТОВКУ перевода из языка '{source_lang_code}'.")
        
        if os.path.basename(self.path_fail) not in self.get_subdirectories(self.dir_assembling):
            self.statusBar().showMessage("Ошибка: Выберите папку мода внутри директории Сборки.")
            QMessageBox.warning(self, "Неверный выбор", "Пожалуйста, выберите папку мода внутри директории Сборки.")
            return

        steam_mods_dir = self.dir_content         
        source_dir = QFileDialog.getExistingDirectory(
            self,
            "Выберите исходный мод из каталога Steam",
            steam_mods_dir,
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )

        # Если пользователь закрыл окно, ничего не делаем
        if not source_dir:
            log_debug("Пользователь отменил выбор мода из Steam.")
            self.statusBar().showMessage("Действие отменено.")
            return

        # 3. Определяем все необходимые параметры для потока  

        log_debug(f"Целевая папка (куда): {self.path_fail}")
        log_debug(f"Исходная папка (откуда): {source_dir}")
        log_debug(f"Язык перевода: {self.localisation}, Язык источника: {source_lang_code}")

        # 4. Запускаем задачу с правильными параметрами
        self._start_task(
            task_name='prepare_translation',
            source_dir=source_dir,    # Steam (откуда)
            source_language=source_lang_code
        )
    
    def getItemll(self):
        self.filename_2_ = QFileDialog.getExistingDirectory(self, caption=("Открыть папку"), directory = self.dir_content)
        self.statusBar().showMessage(f"{self.filename_2_}")        
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
            ErrorMessageBox(f"Указанный путь: {path} - не является файлом или папкой").exec()  
            log_debug(f"Указанный путь: {path} - не является файлом или папкой")
            return False            
        if os.path.isdir(path):
            # Если путь - директория, удаляем ее и все содержимое
            log_debug(f"Удаление каталога и всех его файлов и подкаталогов: {path}")
            self.delete_file_or_folder(path)                 
        elif os.path.isfile(path):
            # Если путь - файл, удаляем файл            
            os.remove(path)
            log_debug(f"Файл {path} - удален")            
        elif os.path.exists(path):
            # Если путь существует, но не является ни файлом, ни директорией
            ErrorMessageBox.show_error(f"Неизвестный тип пути: {path}")  
            log_debug(f"Неизвестный тип пути: {path}")   
        else:
            # Если путь не существует
            ErrorMessageBox.show_error(f"Путь не существует: {path}")
            log_debug(f"Неизвестный тип пути: {path}")        
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
            ErrorMessageBox.show_error("Ошибка доступа перезагрузите приложение и повторите удаление")
            log_error("Ошибка доступа перезагрузите приложение и повторите удаление")
                
    
    def get_subdirectories(self, directory):
        subdirectories = []        
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                subdirectories.append(item)
        return subdirectories  
        
            
    def _setup_settings(self):
        """Загружает настройки из файла или устанавливает значения по умолчанию."""        
        self.slovar_time = self.settings.value("slovar_time", "dark")  
        self.toolbar_state = self.settings.value("toolbar_state")   
        
        # Загрузка положения и размера окна
        self.resize(self.settings.value("size_mmanager", QSize(1564, 772)))
        self.move(self.settings.value("pos_mmanager", QPoint(188, 150)))   
        self.splitter_geometry = self.settings.value("splitter/geometry", QByteArray()) 
        self.dir_content = self.settings.value("dir_content", "")        
        self.dir_assembling = self.settings.value("dir_assembling", os.path.join(self.project_root, "assembling"))
        
        self.dir_Stellaris_mod = self.settings.value("dir_Stellaris_mod", "") 
        
        self.rezerv = ProcessingConstants.REZERV
        self.selected_language = self.settings.value("language", "Russian")
        self.localisation = ProcessingConstants.get_language_localisation(self.selected_language)    
        qdarktheme.setup_theme(self.slovar_time)  
        font_family = self.settings.value("font/family", "Times New Roman")
        font_size = self.settings.value("font/size", 9)
        font_bold = self.settings.value("text/font_bold", True)        
        if font_bold == "true":
            font_bold = True 
        font = QFont(font_family, font_size)
        font.setBold(font_bold)
        self.setFont(font) 

        self.lovie_sev = self.settings.value("file/lovie_sev", "")
        self.file_name = self.settings.value("file/file_name", "")
        self.seve_file_name = self.settings.value("file/seve_file_name", "")

        self.listOfChangedKeys = []      
        self.signal_processing_path = None         
        self.ilo, self.ila = 0, 0        
        self.isifra = 0  
        self.pending_saves = os.path.join(self.app_data_dir, "pending_saves")
        log_debug(f"_setup_settings - self.pending_saves: {self.app_data_dir}")
        
        self.lovie = None        
        
        self.werkil1 = False 
        self.werkil2 = False        
        self.werkil3 = False        
        self.werkil4 = False              
        
        self.selected_language = self.settings.value("language", "Russian") # * Получаем выбранный язык       
        log_debug(f"{self.localisation}")
        log_debug("Настройки загружены.")
        
    def _setup_seve_file_name(self):
        # ... ваш код ...
        if self.lovie_sev == "try4":                      
            if self.seve_file_name and os.path.exists(self.seve_file_name):
                # 1. ПРОВЕРКА: Существует ли вообще окно текстового редактора?
                text_edit_window = self.findChild(QWidget, "text_edit_window_name") # или другой способ доступа
                if not text_edit_window or not text_edit_window.isVisible():
                    log_debug("Окно текстового редактора не найдено или скрыто. Пропускаю автозагрузку.")
                    self.openAfFile() # Открываем диалог выбора файла
                    return

                # 2. ПРОВЕРКА: Является ли оно активным таб'ом?
                # Предполагается, что у вас есть QTabWidget с именем self.tab_widget
                current_tab_text = self.tab_widget.tabText(self.tab_widget.currentIndex())
                if current_tab_text != "Текстовый редактор":
                    log_debug("Активный tab не 'Текстовый редактор'. Пропускаю автозагрузку.")
                    # self.openAfFile() # Решите, нужно ли тут открывать диалог
                    return

                # Если все проверки пройдены, тогда загружаем
                log_debug("Все проверки пройдены. Запускаю автозагрузку файла.")
                self.setStart_1(puti=self.seve_file_name, lovie=self.lovie_sev)
                self.start_task("load_specific_file", lovie="try4")
            else:
                self.openAfFile()
        else:   
            self.openAfFile()
        
    def save_settings_pyti(self, dir_content, dir_assembling, dir_Stellaris_mod):
        self.settings.setValue("dir_content", dir_content)         
        self.settings.setValue("dir_assembling", dir_assembling)         
        self.settings.setValue("dir_Stellaris_mod", dir_Stellaris_mod)         
        self.save_settings()
        log_debug("Пути сохраненны.")

    def save_settings(self):
        # Сохранение положения и размера окна
        self.settings.setValue("pos_mmanager", self.pos())
        self.settings.setValue("size_mmanager", self.size())
        self.settings.setValue("splitter/geometry", self.splitter.saveState())        
        self.settings.setValue("toolbar_state", self.saveState()) 
        if os.path.isfile(self.seve_file_name):
            text_edit = self.text_edit.toPlainText()
            with open(self.seve_file_name, 'w', encoding="utf-8-sig") as file_l:
                file_l.write(text_edit)            
        
        self.settings.setValue("language", self.selected_language)
        self.settings.setValue("file/file_name", self.file_name)
        self.settings.setValue("file/lovie_sev", self.lovie_sev)
        self.settings.setValue("file/seve_file_name", self.seve_file_name)        
        # Сохранение положения и размера окна

        font = self.font()
        self.settings.setValue("font/family", font.family())
        self.settings.setValue("font/size", font.pointSize())
        self.settings.setValue("text/font_bold", True)
        
        self.settings.setValue("toolbar_state", self.saveState())   
        log_debug("Настройки сохраненны.")    
        
######################################################################################################   
    def _extract_source_language_from_rezerv(self, input_path):
        """
        Ищет в иерархии путей выше input_path папку, соответствующую шаблону 'vs - <language>...',
        и извлекает оттуда код языка.

        :param input_path: Путь к файлу (например, .yml) ИЛИ путь к папке.
        :return: Код языка (например, 'russian') или None.
        """
        
        available_languages = ProcessingConstants.LOCALISATION
        
        try:
            current_path = input_path
            
            # 1. Если входной путь - это файл, начинаем искать из его родительской папки
            if not os.path.isdir(current_path):
                current_path = os.path.dirname(current_path)
                log_debug(f"Входной путь был файлом. Начинаем поиск с директории: {current_path}")

            # 2. Цикл подъема по дереву директорий (для поиска корня мода)
            # Мы будем подниматься вверх до тех пор, пока не найдем папку,
            # содержащую нужный нам шаблон 'vs - ...'
            
            # Максимальное количество шагов подъема, чтобы избежать бесконечного цикла
            max_depth = 10 
            
            for _ in range(max_depth):
                if not os.path.isdir(current_path):
                    log_debug(f"Текущий путь '{current_path}' больше не является директорией. Прерывание поиска.")
                    break
                    
                # 3. Ищем в ТЕКУЩЕЙ директории папки, соответствующие шаблону
                for item in os.listdir(current_path):
                    item_path = os.path.join(current_path, item)
                    
                    if os.path.isdir(item_path) and item.startswith("vs - ") and item.endswith("rezerv"):
                        parts = item.split(' - ')
                        
                        if len(parts) >= 2:
                            language_code = parts[1].strip().lower()
                            
                            if language_code in available_languages:
                                log_debug(f"Язык-источник '{language_code}' успешно извлечен из папки '{item}' в пути: {current_path}")
                                return language_code
                            # Если мы нашли папку 'vs - ...', но язык неизвестен, то лучше сразу выйти
                            else:
                                log_debug(f"Найденная папка '{item}' содержит неизвестный язык '{language_code}'.")
                                return None

                # 4. Если ничего не найдено в текущей директории, поднимаемся на уровень выше
                parent_dir = os.path.dirname(current_path)
                
                # Если мы достигли корня файловой системы, останавливаемся
                if parent_dir == current_path:
                    break
                    
                current_path = parent_dir
                
            log_debug(f"Подпапка с языком не найдена в иерархии, начиная от {input_path}")
            return None

        except Exception as e:
            log_error(f"Критическая ошибка при поиске языка в иерархии {input_path}: {e}")
            return None
    
    def _on_file_renamed(self, path: str, old_name: str, new_name: str):
        """
        СЛОТ-обработчик сигнала fileRenamed от модели.
        Обновляет дерево, чтобы изменения были видны.
        """
        log_debug(f"Модель сообщает о переименовании: {path}/{old_name} -> {path}/{new_name}")
        
        # Получаем индекс родительской папки, где произошло переименование
        parent_index = self.modell.index(path)
        
        # Обновляем представление, чтобы оно перечитало данные из этой папки
        self.tree_view.setRootIndex(parent_index)
        # Возвращаемся на наш основной корень
        self.tree_view.setRootIndex(self.modell.index(self.dir_assembling))
        # И снова раскрываем его, чтобы дерево обновилось
        self.tree_view.expand(self.modell.index(self.dir_assembling))

        # Также нужно обновить сохраненный путь, если он относится к переименованному элементу
        if self.path_fail == os.path.join(path, old_name):
            self.path_fail = os.path.join(path, new_name)
            self.statusBar().showMessage(f"Элемент переименован в '{new_name}'.")
    
    def _start_task(self, task_name, **kwargs):
        """
        Универсальный метод для запуска задач в LocalisationManagerThread.
        
        :param task_name: Имя задачи ('prepare_translation', 'update_files', 'copy_to_game')
        :param kwargs: Параметры, необходимые для задачи.
        """
        # 1. Очищаем предыдущую задачу, если она есть
        if self.tetr and self.tetr.isRunning():
            log_debug("Предыдущая задача еще выполняется. Запуск новой невозможен.")            
            return

        self.setEnabled(False) # Блокируем интерфейс на время выполнения
        log_debug(f"Запуск задачи: {task_name} с параметрами {kwargs}")

        # 2. Создаем и настраиваем объект потока
        self.tetr = QThread()
        self.objekt = LocalisationManagerThread(
            target_language=self.localisation,
            base_dir=self.path_fail,
            stellaris_dir=self.dir_Stellaris_mod,
            source_dir=kwargs['source_dir'],            
            source_language=kwargs.get('source_language')
        )
        self.objekt.moveToThread(self.tetr)
        
        # 3. В зависимости от задачи, настраиваем и запускаем нужный метод
        if task_name == 'prepare_translation':
            # Параметры уже переданы в конструктор, остался только запуск нужного метода
            self.tetr.started.connect(lambda: self.objekt.sync_with_steam_mod(prepare_mode=True))

        elif task_name == 'update_files':
            self.tetr.started.connect(lambda: self.objekt.sync_with_steam_mod(prepare_mode=False))

        elif task_name == 'copy_to_game_mod':
            self.tetr.started.connect(self.objekt.copy_to_game_mod)
        
        elif task_name == 'update_mod_name':            
            self.tetr.started.connect(lambda: self.objekt.update_mod_name)
            
        else:
            log_error(f"Неизвестная задача: {task_name}")
            self.setEnabled(True)
            return

        # 4. Подключаем сигналы для всех задач (они у всех одни)
        self.objekt.finishSignal_1.connect(self._on_task_finished)
        self.objekt.finishSignal_2.connect(self._on_task_status_update) 
        self.objekt.finishSignal_1.connect(self.tetr.quit)
        self.objekt.finishSignal_3.connect(self._rename_update_path)
        
        self.tetr.start()
    
    def _rename_update_path(self, new_folder_name, new_dir_path):
        reply = QMessageBox.question(
            self, 'Обновить существующий мод?', 
            f'Папка "{new_folder_name}" уже существует. Обновить её?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.path_fail = new_dir_path
            self.start_mod_update_from_steam
    
    def _on_task_finished(self, message):
        """Слот для обработки сигнала о завершении задачи."""
        log_debug(f"Задача завершена. Сообщение: {message}")        
        self.setEnabled(True) # Разблокируем интерфейс
        

    def _on_task_status_update(self, message):
        """Слот для обновления статус-бара во время выполнения (если нужно)."""
        self.statusBar().showMessage(message)
    
    def _open_log_settings_dialog(self):
        """Открывает диалог настроек логирования."""
        # Создаем диалог, если его еще нет
        if not hasattr(self, '_log_settings_dialog'):            
            
            # Подключаем сигналы диалога к нашему методу-обработчику
            self._log_settings_dialog.debug_changed.connect(self._update_log_levels)
            self._log_settings_dialog.info_changed.connect(self._update_log_levels)
            self._log_settings_dialog.warning_changed.connect(self._update_log_levels)
            self._log_settings_dialog.error_changed.connect(self._update_log_levels)
        
        # Открываем диалог
        self._log_settings_dialog.exec()
    
    def _update_log_levels(self):
        """Обновляет уровни логирования в loguru на основе состояний чекбоксов."""
        # Получаем экземпляр логгера
        logger_instance = self._log_settings_dialog.get_logger()
        
        # Получаем состояния из диалога
        levels = self._log_settings_dialog.get_levels()
        
        # Устанавливаем уровни для loguru.
        # Уровень DEBUG включает в себя все остальные.
        # Уровень INFO включает WARNING и ERROR.
        # и т.д.
        if levels["debug"]:
            logger_instance.logger.remove() # Удаляем старые обработчики, если они были
            logger_instance.logger.add(sink=lambda m: print(m, end=""), level="DEBUG", format="{time:HH:mm:ss} | {level} | {message}")
            log_debug("Логирование установлено на уровень: DEBUG")
        elif levels["info"]:
            logger_instance.logger.remove()
            logger_instance.logger.add(sink=lambda m: print(m, end=""), level="INFO", format="{time:HH:mm:ss} | {level} | {message}")
            log_debug("Логирование установлено на уровень: INFO")
        elif levels["warning"]:
            logger_instance.logger.remove()
            logger_instance.logger.add(sink=lambda m: print(m, end=""), level="WARNING", format="{time:HH:mm:ss} | {level} | {message}")
            log_debug("Логирование установлено на уровень: WARNING")
        else:
            # Минимальный уровень - ERROR
            logger_instance.logger.remove()
            logger_instance.logger.add(sink=lambda m: print(m, end=""), level="ERROR", format="{time:HH:mm:ss} | {level} | {message}")
            log_debug("Логирование установлено на уровень: ERROR")
    
    def return_function_updates(self, path_fail, stre=None, listOfChangedKeys=None):
        self.setEnabled(True)
        if stre == "None":            
            return
                
    def return_function_1(self, text):
        os.chdir(self.project_root)                
        self.setEnabled(True)
        if text != "False":
            ErrorMessageBox.show_error(text)  
        
        
    def update_status_bar(self, message: str):
        """СЛОТ для простого вывода сообщений в статусную строку."""
        self.statusBar().showMessage(str(message))
            
################################################################################################### 
    
    def getItem(self):
        self.filename_1_ = QFileDialog.getOpenFileName(self, caption=("Открыть файл"), filter=("Файлы локализации (*.yml)"))[0]
        
    def getdials_1(self):        
        try:
            from file_configuration.ModFolderConfigurator import ModFolderConfigurator
            
            # Теперь создаем экземпляр, передавая self
            dialog = ModFolderConfigurator(main_window=self)
            result = dialog.exec()
            log_debug("ModFolderConfigurator успешно создан. {result}")
            
        except ImportError as e:
            log_error(f"Не удалось импортировать ModFolderConfigurator: {e}")
            # Можно показать пользователю ошибку
            QMessageBox.critical(self, "Ошибка импорта", f"Не удалось загрузить модуль ModFolderConfigurator: {e}")
            return # Прерываем выполнение, если модуль не загрузился      
    
    def getdials_2(self):
        dialog = CreateFolderDialog()
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            folder_name = dialog.folder_name_input.text()            
            log_debug(f"Создание папки с именем: {folder_name}")            
            os.chdir(self.dir_assembling)
            os.mkdir(folder_name)
            log_debug(f"Текущая директория изменилась на folder: {os.getcwd()}")
            os.chdir(self.project_root)
            log_debug(f"Текущая директория изменилась на folder: {os.getcwd()}")            
        else:
            log_debug("Создание папки отменено")            

######################## ? TextConverter функции ########################

    def set_language(self, lang):
        """Устанавливает выбранный язык."""
        self.selected_language = lang        
        for action in self.language_actions.values():
            action.setChecked(False)        
        self.language_actions[lang].setChecked(True)
        log_debug(f"Выбранный язык: {lang}") # * Отладочный вывод
    
    def CloseTheFile(self):
        self.file_name = ""
        self.text_edit.setPlainText("")
        self.lovie_sev = "" 
        self.seve_file_name = ""       
            
    def getdials17(self): 
        """Преобразовать, Копировать"""
        log_debug("getdials17 - started")
        self.lovie = "try1"
        self.getdials6() 
            
    def getdials17_1(self):
        log_debug("getdials17_1 - started")
        lex = self.text_edit.toPlainText()
        clipboard = QApplication.clipboard() 
        clipboard.setText(lex)
        
    def getdials18(self): 
        """Вставить, Преобразовать, Копировать"""
        clipboard = QApplication.clipboard()
        lex = clipboard.text()
        self.text_edit.setPlainText(lex)
        self.lovie = "try3"
        self.getdials3()
        lex = self.text_edit.toPlainText()
        clipboard.setText(lex)
        
    def getdials51(self): 
        """Очистка #Новых строк"""
        self.setStart_1()   
        self.start_task("remove_newline_tag") 
        
    def getdials1(self):      
        """Очистка каталога временных файлов"""                  
        d = f"{self.pending_saves}\\"        
        filesToRemove = [os.path.join(d, f) for f in os.listdir(d)]        
        for f in filesToRemove:
            os.remove(f)   
            log_info(f"Удалён файл: {f}")
            
    def getdials3(self): 
        """Распаковка"""  
        log_debug("getdials3 - started")      
        if self.ilo or self.ila == 0:    
            self.setStart_1() 
            self.start_task("apply_customizations") 
            self.ilo, self.ila = 0, 0
        else:
            log_debug(f"Распаковка отменена")     
            
    def getdials4(self): 
        """Упаковка ключей""" 
        log_debug("getdials4 - started")               
        if self.ilo == 0:  
            self.setStart_1()
            self.start_task("prepare_view_map")
            self.ilo = 1
        else:
            log_debug(f"Упаковка ключей отменена")
        # ...       
                
    def getdials6(self): 
        """Упаковка ссылок""" 
        log_debug("getdials6 - started")
        if self.ila == 0:     
            self.setStart_1()
            self.start_task("prepare_session_map")
            log_debug("start_task вернулся!")  
            self.ila = 1
        else:
            log_debug(f"Упаковка ссылок отменена")
        # ...

    def getdials5(self): 
        """Анализ-Замена"""  
        log_debug("getdials5 - started")   
        self.setStart_1()   
        self.start_task("apply_style_map")        
####################################################################################################################################################### 

    def setStart_1(self, file_name=None, lovie=None):
        log_debug("setStart_1 - started")        
        if file_name is not None:
            self.file_name = file_name
        if lovie is not None:
            self.lovie = lovie

        self.text_processing_thread.file_name = self.file_name
        self.text_processing_thread.processing_path = self.seve_file_name 
        self.text_processing_thread.command = self.lovie 

        self.setEnabled(False)

    def start_task(self, task_type: str, **kwargs):
        """Запускает задачу в потоке обработки текста.""" 
        self.text_processing_thread.signal_task_complete.connect(self.setInit)       
        self.text_processing_thread.run_task(task_type, **kwargs)    
        
    def setInit(self, command: str = None):                 
        self.setEnabled(True)
        if command == "try1":
            log_debug(f"setInit - try1: {self.lovie}")
            self.lovie = "try2"
            self.getdials4()
        elif command == "try2":
            log_debug(f"setInit - try2: {self.lovie}")
            self.getdials17_1()
        elif command == "try3":
            log_debug(f"setInit - try3: {self.lovie}")
            lex = self.text_edit.toPlainText()
            clipboard = QApplication.clipboard()
            clipboard.setText(lex)
        elif command == "try4":
            log_debug(f"setInit - try4: {self.lovie}")
            self.lovie_sev = command
            self.seve_file_name = self.text_processing_thread.processing_path  # Используем атрибут потока
                            
    def returnFunction_linesi(self, linesi):
        """Обрабатывает полученный текст из потока"""
        if linesi:
            log_debug(f"returnFunction_linesi: received text, length: {len(linesi)}")
            self.set_text(linesi)
            self.setEnabled(True) 
        else:
            log_debug("returnFunction_linesi: empty text received")
            self.set_text("")
            self.setEnabled(True)
            
            
    def returnFunction_signal_processing_path(self, signal_processing_path):
        if signal_processing_path != "":    
            self.signal_processing_path = signal_processing_path
    
    def returnFunction_filename(self, file_name):
        if file_name != "":    
            self.file_name = file_name
    
    def update_character_count_2(self, color_dict):
        self.text_edit.theResultoftheScantoUpdatetheColor(color_dict)
        self.secondaryPotok2.quit()
        self.secondaryPotok2.wait()  
        
    def set_text(self, text):
        """Устанавливает текст в редактор"""
        try:
            if text and isinstance(text, str):
                self.text_edit.setPlainText(text)
            elif text is None:
                self.text_edit.setPlainText("")  # Очищаем виджет
            else:
                log_debug(f"set_text - unexpected type of text: {type(text)}")
                self.text_edit.setPlainText("")  # В случае ошибки очищаем виджет
                
        except Exception as e:
            log_error(f"in set_text: {str(e)}")
            ErrorMessageBox.show_error(f"Ошибка установки текста: {str(e)}")
        
        
    def safe_operation(self, operation_function, *args, **kwargs):
        """Безопасное выполнение функции с обработкой ошибок"""
        try:
            return operation_function(*args, **kwargs)
        except Exception as e:
            log_error(f"in safe_operation: {str(e)}")
            return None
        
    def getdials7(self):          
        """Сохранить в резерв"""
        with open(self.signal_processing_path, 'w', encoding="utf8") as f:
            textv = self.text_edit.toPlainText()
            f.write(textv)        
            
    def getdials8(self):         
        """Обновить из файла"""
        with open(self.signal_processing_path, encoding="utf8") as file_l: 
            data = file_l.read()
            self.text_edit.setPlainText(data)                   
        
        
    def getdials9(self): 
        """Открыть резерв"""
        log_debug(f"start {self.pending_saves}")
        path = self.pending_saves
        path = os.path.realpath(path)
        os.startfile(path)
    
    def getdials10(self):  
        """Настройки шрифта"""        
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_edit.setFont(font)             
            
    def getdials11(self):   
        """Сохранить как"""        
        filename_l = QFileDialog.getSaveFileName(self)[0]
        if filename_l:
            try:
                with open(filename_l, 'w', encoding="utf-8-sig") as f:
                    textv = self.text_edit.toPlainText()
                    f.write(textv)            
            except FileNotFoundError as e:
                log_error(f"{str(e)}")
                ErrorMessageBox.show_error(f"{str(e)}") 
        else:
            return
            
    def getdials12(self): 
        """сохранить"""               
        try:
            with open(self.file_name, 'w', encoding="utf-8-sig") as f:
                textv = self.text_edit.toPlainText()
                f.write(textv)              
        except FileNotFoundError as e:
            log_error(f"{str(e)}")
            ErrorMessageBox.show_error(f"{str(e)}")   
            
    def getdials13(self): 
        """Открыть"""                       
        self.file_name = QFileDialog.getOpenFileName(self, caption=("Открыть файл"), filter = ("Файлы локализации (*.yml)"))[0]        
        self.openAfFile()  
    
    def openAfFile(self):  
        if self.file_name != "":            
            log_info(f"Файл загружен: {self.file_name}")            
            self.start_task("load_file_to_widget", path=self.file_name)            
        else:                
            log_info(f"Файл не выбран. Откройте новый.")
            
    def getdials14(self):     
        """Новое"""  
        self.CloseTheFile()        
        tehc = f"{self.pending_saves}{ProcessingConstants.AIL_L}"
        log_debug(f"Yes - {tehc}") 
        self.statusBar().showMessage(f"Yes - {tehc}")   
        with open(tehc, 'w', encoding="utf8") as f:
            textv = self.text_edit.toPlainText()
            f.write(textv)        
        self.signal_processing_path = tehc
        self.nova_fail = True     
        
    def gettext_r1(self): 
        """Открыть АЗ"""  
        editor_tab_index = 1 
        self.tab_widget.setCurrentIndex(editor_tab_index)        
        log_debug(f"Переключены на вкладку '{self.tab_widget.tabText(editor_tab_index)}'.")
        self.setStart_1()
        self.start_task("save_style_map_to_widget")      
    
    def gettext_r2(self):  
        editor_tab_index = 1 
        self.tab_widget.setCurrentIndex(editor_tab_index)        
        log_debug(f"Переключены на вкладку '{self.tab_widget.tabText(editor_tab_index)}'.")
        self.setStart_1()
        self.start_task("save_widget_to_style_map")     
            
    def closeEvent(self, event):  
        if self.is_processing and self.potok and self.potok.isRunning():            
            reply = QMessageBox.question(self, 'Подтверждение выхода', "Обработка данных еще не завершена. Вы уверены, что хотите выйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:               
                self.potok.quit()
                if not self.potok.wait(5000):  # Ждем до 5 секунд
                    log_debug("Предупреждение: Поток не завершился вовремя, что привело к принудительному завершению.")
                self.save_settings()                
                if self.werkil3 == True:
                    self.ModFolderConfigurator.close()
                    self.werkil3 = False                
                event.accept()
            else:               
                event.ignore()
                return 
        else:
            self.save_settings()            
            if self.werkil3 == True:
                self.ModFolderConfigurator.close()
                self.werkil3 = False
        
            event.accept()      
        self.seve_file_name = ""
        log_debug("Состояние текстового редактора очищено после закрытия.")
        super().closeEvent(event)
