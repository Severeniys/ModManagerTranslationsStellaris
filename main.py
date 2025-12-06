# main.py
import os
import sys
import shutil
import platform
import qdarktheme
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtCore import QLocale, QTranslator, QLibraryInfo

# ... (импорты вашего класса и логгера)
from file_configuration.ModManagerTranslationsStellaris import ModManagerTranslationsStellaris
from file_configuration.utils import setup_logger, log_debug, log_error, log_info, log_warning, log_signal

try:
    PROJECT_ROOT = sys._MEIPASS
except Exception:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# --- ЕДИНАЯ ФУНКЦИЯ ДЛЯ ИНИЦИАЛИЗАЦИИ ВСЕГО СВЯЗАННОГО С AppData ---
def initialize_app_environment():
    """
    Выполняет полную инициализацию окружения приложения:
    1. Определяет и создает главную папку в AppData.
    2. Копирует папку 'config' из .exe в AppData (если ее нет).
    3. Создает все остальные необходимые подпапки (logs, temp_files и т.д.).
    4. Возвращает словарь со всеми готовыми путями.
    """
    app_name = "ModManagerTranslationsStellaris"
    log_info("Начинаю инициализацию окружения приложения...")

    # 1. Определяем и создаем главную папку в AppData
    if platform.system() == "Windows":
        base_path = os.environ.get("APPDATA", "")
    elif platform.system() == "Darwin":
        base_path = os.path.expanduser("~/Library/Application Support")
    else:
        base_path = os.path.expanduser("~/.local/share")
        
    app_data_dir = os.path.join(base_path, app_name)
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)
        log_info(f"Создана главная папка приложения: {app_data_dir}")
    else:
        log_info(f"Главная папка приложения уже существует: {app_data_dir}")

    # 2. Копируем папку 'config', если ее нет
    app_config_dir = os.path.join(app_data_dir, "config")
    exe_config_source_dir = os.path.join(PROJECT_ROOT, "file_configuration", "config")

    if not os.path.exists(app_config_dir):
        log_info(f"Папка 'config' не найдена в AppData. Копирую из '{exe_config_source_dir}'...")
        try:
            shutil.copytree(exe_config_source_dir, app_config_dir)
            log_info(f"Папка 'config' успешно скопирована в '{app_config_dir}'.")
        except Exception as e:
            log_error(f"Не удалось скопировать папку 'config': {e}. Создаю пустую папку.")
            os.makedirs(app_config_dir, exist_ok=True) # Создаем пустую, чтобы приложение не упало
    else:
        log_info(f"Папка 'config' в AppData уже существует, пропускаю копирование.")

    # 3. Создаем все остальные необходимые подпапки
    folders_to_create = [
        "logs",
        "temp_files",
        "pending_saves",
        "user_settings"
    ]
    
    for folder in folders_to_create:
        folder_path = os.path.join(app_data_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        log_info(f"Гарантированно создана папка: {folder_path}")

    # 4. Собираем и возвращаем все готовые пути в одном словаре
    all_paths = {
        'app_root': app_data_dir,
        'config': app_config_dir,
        'logs': os.path.join(app_data_dir, "logs"),
        'temp_files': os.path.join(app_data_dir, "temp_files"),
        'pending_saves': os.path.join(app_data_dir, "pending_saves"),
        'user_settings': os.path.join(app_data_dir, "user_settings"),
    }
    
    log_info("Инициализация окружения завершена успешно.")
    return all_paths, app_data_dir


# --- ОСНОВНАЯ ФУНКЦИЯ ЗАПУСКА ---
def application():
    """Главная функция запуска приложения."""   
    qdarktheme.enable_hi_dpi()       
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create("Windows"))   
    app_paths, app_data_dir = initialize_app_environment()    
    log_file_path = os.path.join(app_paths['logs'], f"app_log_{datetime.now().strftime('%Y-%m-%d')}.log")
    setup_logger(log_file_path)
    log_info("Приложение запущено.")    
    MMTS = ModManagerTranslationsStellaris(PROJECT_ROOT, app_data_dir)    
    translator = QTranslator(app)
    locale = QLocale.system().name()
    path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    if translator.load(f'qt_{locale}', path):
        app.installTranslator(translator)
    else:
        log_debug(f"Предупреждение: Не удалось загрузить переводы Qt для локали: {locale}")
    log_signal.connect(MMTS.update_status_bar)
    MMTS.show()    
    sys.exit(app.exec())

if __name__ == "__main__":        
    application()