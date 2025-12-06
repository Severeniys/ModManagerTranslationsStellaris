import os
import re
import sys
import json
import shutil

from PyQt6.QtCore import (
    QObject, pyqtSignal, QThread
    )

from PyQt6.QtWidgets import (
    QPlainTextEdit, 
)
from file_configuration.constants import ProcessingConstants
from file_configuration.utils import log_debug, log_error, log_info, log_warning
# --- Выносим "магические" строки в константы ---


class TextProcessingThread(QObject):
    # --- Сигналы (с переименованными именами) ---
    signal_processed_text = pyqtSignal(str) # finishSignal_linesi -> signal_processed_text
    signal_filename = pyqtSignal(str)       # finishSignal_filename -> signal_filename
    signal_error = pyqtSignal(str)          # finishSignal_error -> signal_error
    signal_processing_path = pyqtSignal(str) # finishSignal_pytj -> signal_processing_path
    signal_task_complete = pyqtSignal(str)  # finishSignal_1 -> signal_task_complete
    signal_command = pyqtSignal(str)        # finishSignal_1 (в vozvrat_signal) -> signal_command

    def __init__(self, app_data_dir, text_widget: QPlainTextEdit, save_result_on_finish: bool, 
                command: str = "", filename: str = "", processing_path: str = "",
                parent_widget: QObject = None):
        super().__init__()
        self.app_data_dir = app_data_dir         
        self.text_widget = text_widget
        self.save_result_on_finish = save_result_on_finish
        self.command = command
        self.filename = filename
        self.processing_path = processing_path
        self.parent_widget = parent_widget
        self._base_resources_path = None
        self._is_running = False

        self.moveToThread(QThread())

    def run_task(self, task_type: str, **kwargs):
        """Основной диспетчер для выполнения задач."""
        self._reset_state()
        try:
            log_debug(f"Стартовые условия: {task_type}, {kwargs}")  # Логируем начало задачи
            if task_type == "load_file_to_widget":
                self._load_file_to_widget(kwargs.get("path"))
            elif task_type == "prepare_session_map":
                self._prepare_session_map()
            elif task_type == "prepare_view_map":
                self._prepare_view_map()
            elif task_type == "apply_customizations":
                self._apply_customizations()
            elif task_type == "apply_style_map":
                self._apply_style_map()
            elif task_type == "remove_newline_tag":
                self._remove_newline_tag()
            elif task_type == "load_file_to_widget":
                self._load_file_to_widget(kwargs.get("path"))
            elif task_type == "save_style_map_to_widget":
                self._save_style_map_to_widget()
            elif task_type == "save_widget_to_style_map":
                self._save_widget_to_style_map()
            elif task_type == "reset_paths":
                self._reset_paths()
            elif task_type == "load_file_to_widget_simple":
                self._load_file_to_widget(kwargs.get("path"))
            elif task_type == "load_specific_file":
                self._load_specific_file(kwargs.get("path"), kwargs.get("lovie"))  # path
            else:
                self._status_message = f"Unknown task type: {task_type}"
                self.signal_error.emit(self._status_message)
        except Exception as e:
            log_error(f"in run_task: {e}")
            self.signal_error.emit(f"Error: {e}")
        finally:
            self.signal_task_complete.emit(self.command)
    
    def _get_selected_language_safely(self) -> str | None:
        """
        Безопасно получает выбранный язык из главного окна.
        """
        # ! НОВАЯ, ПРАВИЛЬНАЯ ПРОВЕРКА
        if not self.parent_widget:
            log_warning("Родительский виджет (главное окно) не передан в поток.")
            return None

        try:
            # Прямой доступ к атрибуту главного окна
            return self.parent_widget.selected_language
        except AttributeError:
            log_warning("Атрибут 'selected_language' не найден у родительского виджета.")
            return None
    
    def get_base_resources_path(self):
        """Устанавливает и возвращает базовый путь к ресурсам."""
        if self._base_resources_path is None:
            if getattr(sys, 'frozen', False):
                self._base_resources_path = sys._MEIPASS
            else:
                # Определяем путь к корневой директории проекта
                # 1. Получаем путь к текущему файлу
                current_file_dir = os.path.dirname(os.path.abspath(__file__))
                log_debug(f"Current file directory: {current_file_dir}")
                
                # 2. Ищем корневую директорию проекта (ModManagerTranslationsStellaris_Alpha)
                # Идем вверх по иерархии директорий
                project_root = current_file_dir
                while project_root != os.path.dirname(project_root):
                    if os.path.basename(project_root) == "ModManagerTranslationsStellaris_Alpha":
                        break
                    project_root = os.path.dirname(project_root)
                else:
                    # Если не нашли корневую директорию, используем текущий каталог
                    log_debug(f"Warning: Project root not found, using current directory")
                    project_root = os.getcwd()
                    
                self._base_resources_path = project_root
                log_debug(f"Base resources path set to: {self._base_resources_path}")
        return self._base_resources_path

    # --- Внутренние методы-помощники ---
    def _apply_final_replacements(self, lines, placeholder_map):
        """Применяет финальные замены."""
        selected_language = self._get_selected_language_safely()
        if not selected_language:
            self.signal_error.emit("Не удалось определить выбранный язык.")
            self.signal_task_complete.emit(self.command)
            return
        language_replacements = ProcessingConstants.get_language_replacements(selected_language)
        # 1. Объединяем все замены в один словарь
        all_replacements = {
            **language_replacements,
            **ProcessingConstants.FORMATTING_REPLACEMENTS,
            **ProcessingConstants.SPACE_REPLACEMENTS,
            **placeholder_map
        }

        # 2. Применяем замены
        processed_lines = self._process_lines(lines, all_replacements) # keys
        self._result_text = processed_lines # self._apply_line_replacements(processed_lines, all_replacements) # values

        self.signal_processed_text.emit(self._result_text)
        self.signal_task_complete.emit(self.command)
    
    def _read_text_from_widget(self) -> list[str]:
        """Читает текст из виджета и разделяет на строки."""
        log_debug(f"_read_text_from_widget - self.text_widget: {self.text_widget}")
        text = self.text_widget.toPlainText()       
        return text.split(ProcessingConstants.NEWLINE_CHAR)

    def _read_json_file(self, file_path: str) -> dict | None:
        """Безопасно читает файл JSON."""
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError as e:
            self._status_message = f"Error: Файл не найден - {file_path}: {e}"
            self.signal_error.emit(self._status_message)
            log_error(f"{self._status_message}") # Добавляем отладочный вывод
            return None
        except json.JSONDecodeError as e:
            self._status_message = f"Error: Недопустимый JSON в файле - {file_path}: {e}"
            self.signal_error.emit(self._status_message)
            log_error(f"{self._status_message}") # Добавляем отладочный вывод
            return None
            
    def _write_to_json_file(self, data: dict, file_path: str):
        """Безопасно записывает данные в JSON файл."""
        try:
            # Убедимся, что папка для файла существует
            dir_name = os.path.dirname(file_path)
            if not os.path.exists(dir_name):
                # Убедимся, что папка существует перед записью
                os.makedirs(dir_name, exist_ok=True)
                log_debug(f"Создана папка для файла: {dir_name}")
                
            # Основная попытка записи
            with open(file_path, 'w', encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False) # ensure_ascii=False для кириллицы
                
            # Если все успешно
            self._status_message = f"Файл успешно записан: {file_path}"
            log_debug(self._status_message) # Используем log_debug для сообщений об успехе
            return True

        except (IOError, OSError) as e:
            # Ошибка доступа к файлу или диска
            self._status_message = f"Ошибка записи в файл {file_path}: {e}"
            log_error(f"Ошибка записи в файл {file_path}: {e}")
            self.signal_error.emit(self._status_message)
            
        except Exception as e:
            # Любая другая неожиданная ошибка (например, не смог сериализовать в JSON)
            self._status_message = f"Неожиданная ошибка при записи в файл {file_path}: {e}"
            log_error(f"Неожиданная ошибка при записи в файл {file_path}: {e}")
            self.signal_error.emit(self._status_message)
            
        return False # Возвращаем False, если что-то пошло не так

    def _apply_line_replacements(self, line: str, replacements: dict) -> str:
        """Применяет набор замен к строке."""              
        try:
            log_debug("_apply_line_replacements - started")  # Отладка
            for x, y in replacements.items():            
                line = line.replace(x, y)                
            log_debug(f"_apply_line_replacements - line {line}") 
            log_debug(f"_apply_line_replacements - replacements: x = {x} - y  = {y}")
            if ProcessingConstants.SPECIAL_CHAR_REPLACE[0] in line:
                line = line.replace(*ProcessingConstants.SPECIAL_CHAR_REPLACE)
                log_debug(f"_apply_line_replacements - if line {line}")
            log_debug(f"_apply_line_replacements - line {line}") 
            log_debug("_apply_line_replacements - finished")  # Отладка            
            return line
        except Exception as e:
            log_error(f"_apply_final_replacements: {e}")

    def _find_all_patterns(self, text: str, patterns: list[str]) -> set:
        """Находит все вхождения шаблонов в тексте и возвращает уникальные."""
        found_patterns = set()
        for pattern in patterns:
            matches = re.findall(pattern, text)
            found_patterns.update(matches)
        return found_patterns

    def _create_placeholder_map(self, patterns: list[str]) -> dict:
        """Создает словарь для замены шаблонов на пронумерованные плейсхолдеры."""
        self._found_patterns = list(set(patterns)) # Убедимся, что все уникальны
        self._numbered_placeholders = [f"[{i:02d}]" for i in range(1, len(self._found_patterns) + 1)]
        return dict(zip(self._found_patterns, self._numbered_placeholders))
        
    def _process_lines(self, lines: list[str], replacements_map: dict) -> str:
        """Применяет замены из словаря к списку строк и собирает результат."""
        log_debug("_process_lines - started") # Отладка
        result = []
        for i, line in enumerate(lines):
            log_debug(f"_process_lines - line {i}: {line[:50]}...")             
            log_debug(f"_process_lines - replacements: {replacements_map}")
            line = self._apply_line_replacements(line, replacements_map)
            result.append(line)
        log_debug(f"_process_lines - result: {result}")     
        log_debug("_process_lines - finished") # Отладка
        return "\n".join(result)

    def _generate_json_string(self, data: dict) -> str:
        """Генерирует отформатированную строку из словаря для сохранения в файл."""
        json_lines = ["{"]
        for x, y in data.items():
            y = y.replace("\"", "\\\"")
            x = x.replace("\"", "\\\"")
            comma = "," if self._list_counter < len(data) - 1 else ""
            json_lines.append(f'\t"{x}": "{y}"{comma}')
            self._list_counter += 1
        json_lines.append("}\n")
        return "\n".join(json_lines)

    def _save_result_to_file(self):
        """Сохраняет финальный результат в файл processing_path."""
        if self.processing_path and self.save_result_on_finish:
            try:
                with open(self.processing_path, 'w', encoding="utf-8-sig") as f:
                    f.write(self._result_text)
            except IOError as e:
                self._status_message = f"Error saving result: {e}"
                self.signal_error.emit(self._status_message)
    
    def _reset_state(self):
        """Сбрасывает переменные состояния перед новой задачей."""
        self._processed_lines = []
        self._found_patterns = []
        self._numbered_placeholders = []
        self._result_text = ""
        self._status_message = ""
        self._list_counter = 0

    # --- Реализация конкретных задач (внутри run_task) ---
    
    def filter_lines(self, lines):
        processed_lines_for_search = []
        selected_language = self._get_selected_language_safely()
        if not selected_language:
            self.signal_error.emit("Не удалось определить выбранный язык.")
            self.signal_task_complete.emit(self.command)
            return
        
        language_replacements = ProcessingConstants.get_language_replacements(selected_language)
        # 1. Объединяем все замены в один словарь
        all_replacements = {
            **language_replacements,
            **ProcessingConstants.FORMATTING_REPLACEMENTS,
            **ProcessingConstants.SPACE_REPLACEMENTS,
            
        }
        log_debug(f"filter_lines - all_replacements: {all_replacements}")
        for line in lines:
            processed_line = self._apply_line_replacements(line, all_replacements)
            log_debug(f"filter_lines - processed_line: {processed_line}")
            processed_lines_for_search.append(processed_line)
        return processed_lines_for_search

    def _prepare_session_map(self):        
        lines = self._read_text_from_widget()
        processed_lines_for_search = self.filter_lines(lines)     

        all_patterns = set()
        for line in processed_lines_for_search:
            patterns = self._find_all_patterns(line, ProcessingConstants.REGEX_PATTERNS["KEYS"])
            all_patterns.update(patterns)
        
        placeholder_map = self._create_placeholder_map(list(all_patterns))
        log_debug(f"_prepare_session_map - placeholder_map: {placeholder_map}")
        self._write_to_json_file(placeholder_map, os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['placeholder_map']))        
        log_debug(f"Placeholder map file path: {os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['placeholder_map'])}")
        # -------------------------------------
        # Применяем замены для финального текста
        session_map_data = self._read_json_file(os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['placeholder_map']))
        log_debug(f"_prepare_session_map - session_map_data: {session_map_data}")
        if session_map_data:
            # --- Проверяем содержимое session_map_data ---
            log_debug(f"Данные карты сеанса успешно загружены.")  
            language_replacements = self._get_selected_language_safely()
            if not language_replacements:
                self.signal_error.emit("Не удалось определить выбранный язык.")
                self.signal_task_complete.emit(self.command)
                return          
            
            language_replacements = ProcessingConstants.get_language_replacements(language_replacements)
            all_replacements = {
                **language_replacements,
                **ProcessingConstants.FORMATTING_REPLACEMENTS,
                **ProcessingConstants.SPACE_REPLACEMENTS                
            }                
            _result_text = self._process_lines(lines, all_replacements)            
            self._result_text = self._process_lines(_result_text.split(ProcessingConstants.NEWLINE_CHAR), session_map_data)
            log_debug(f"_prepare_session_map - self._result_text: {self._result_text}")
            self.signal_processed_text.emit(self._result_text)
            self.signal_task_complete.emit(self.command)
        else:
            log_debug("Не удалось загрузить данные карты сеанса.")
            self.signal_error.emit("Не удалось загрузить данные карты сеанса.")
            self.signal_task_complete.emit(self.command)  # Важно!
    
    def _prepare_view_map(self):       
        log_debug("_prepare_view_map - started")
        lines = self._read_text_from_widget()
        log_debug(f"_prepare_view_map - lines (первые 50 символов в каждом): {[line[:50] + '...' for line in lines]}")

        lines_to_replace = []
        for line in lines:
            if not re.match(r"\s*l_russian:\s*", line):
                lines_to_replace.append(line)
        log_debug(f"_prepare_view_map - lines_to_replace (считать): {len(lines_to_replace)}")       
        key_definitions = []
        for line in lines_to_replace:
            for match in re.finditer(ProcessingConstants.REGEX_PATTERNS["KEY_DEFINITION"], line):
                key_definitions.append(match.group(0))  
        
        placeholder_map = {key: f"[{i:05d}]" for i, key in enumerate(key_definitions, start=1)}
        log_debug(f"_prepare_view_map - placeholder_map (считать): {len(placeholder_map)}")
        log_debug(f"_prepare_view_map - placeholder_map (первые 5 пунктов): {list(placeholder_map.items())[:5]}")

        self._write_to_json_file(placeholder_map, os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['view_map']))
        log_debug(f"_prepare_view_map - view_map file path: {os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['view_map'])}")

        view_map_data = self._read_json_file(os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['view_map']))
        if view_map_data:
            log_debug("_prepare_view_map - view_map_data успешно загружен")
            
            processed_lines = []
            for line in lines:
                for key, value in view_map_data.items():
                    line = re.sub(re.escape(key), value, line)  # Заменяем key на value
                processed_lines.append(line)
            self._result_text = "\n".join(processed_lines)

            log_debug(f"_prepare_view_map - self._result_text (first 500 chars): {self._result_text[:500]}")

            self.signal_processed_text.emit(self._result_text)
            self.signal_task_complete.emit(self.command)
        else:
            log_debug("_prepare_view_map - Failed to load view map data.")
            self.signal_error.emit("Failed to load view map data.")
            self.signal_task_complete.emit(self.command)

        log_debug("_prepare_view_map - finished")

    def _apply_customizations(self):
        log_debug("_apply_customizations - started")

        lines = self._read_text_from_widget()

        view_map_data = self._read_json_file(os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['view_map']))
        placeholder_map_data = self._read_json_file(os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['placeholder_map']))
        all_replacements = {            
            **ProcessingConstants.FORMATTING_REPLACEMENTS,
            **ProcessingConstants.SPACE_REPLACEMENTS,        
        }
        if view_map_data and placeholder_map_data:
            
            reversed_placeholder_map = {v: k for k, v in placeholder_map_data.items()}
            temp_text = self._process_lines(lines, reversed_placeholder_map)
            
            reversed_view_map = {v: k for k, v in view_map_data.items()}
            log_debug(f"_apply_customizations - reversed_view_map: {reversed_view_map}")
            temp_text_2 = self._process_lines([temp_text], reversed_view_map)
            reversed_all_replacements = {v: k for k, v in all_replacements.items()}
            self._result_text = self._process_lines([temp_text_2], reversed_all_replacements)
            
        self.signal_processed_text.emit(self._result_text)
        self.signal_task_complete.emit(self.command)
        log_debug("_apply_customizations - finished")


    def _apply_style_map(self):
        # ... логика, похожая на start4 ...
        lines = self._read_text_from_widget()
        style_map_data = self._read_json_file(os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['style_map']))
        
        if style_map_data:
            self._result_text = self._process_lines(lines, style_map_data)
            self.signal_processed_text.emit(self._result_text)
            self.signal_task_complete.emit(None) # В оригинале emit(None)

    def _remove_newline_tag(self):
        # ... логика, похожая на start5 ...
        lines = self._read_text_from_widget()
        processed_lines = [line.replace("#Новая строка", "") for line in lines]
        self._result_text = "\n".join(processed_lines) 
        self.signal_processed_text.emit(self._result_text)
        self.signal_task_complete.emit(None)

    def _load_file_to_widget(self, path: str):
        """Загружает файл по указанному пути."""
        log_debug(f"Загрузка файла: {path}")
        if not path:
            self._status_message = "Error: Не указан путь к файлу."
            self.signal_error.emit(self._status_message)
            return
        try:
            with open(path, 'r', encoding="utf8") as f:
                self._result_text = f.read()
            self.signal_processed_text.emit(self._result_text)            
            # Генерируем и сохраняем копию файла
            base_name = os.path.basename(path).split('.')[0]
            # Используем исправленную функцию для получения пути
            base_path = self.get_base_resources_path()
            pending_saves_dir = os.path.join(self.app_data_dir, "pending_saves")
            # Применяем замену языков к пути
            new_path = os.path.join(pending_saves_dir, f"{base_name}.yml")
            
            selected_language = self._get_selected_language_safely()
            if not selected_language:
                self.signal_error.emit("Не удалось определить выбранный язык.")
                self.signal_task_complete.emit(self.command)
                return
            language_map = ProcessingConstants.get_language_map(selected_language)
            
            for lang, rus in language_map.items():
                new_path = new_path.replace(lang, rus)               
            try:
                with open(new_path, 'w', encoding='utf-8-sig') as outfile: # Укажите 'w' и кодировку
                    outfile.write(self._result_text)  # Записываем результат
                log_debug(f"Успешно сохраненная копия в: {new_path}")
            except Exception as e: # Если запись не удалась, выводим сообщение
                self._status_message = f"Ошибка записи в файл: {e}"
                self.signal_error.emit(self._status_message)
            try:
                shutil.copy2(path, new_path)
                log_debug(f"Успешно скопированный исходный файл в: {new_path}")
            except Exception as e:
                self._status_message = f"Ошибка при копировании файла: {e}"
                self.signal_error.emit(self._status_message)
            
            self.signal_filename.emit(path)
            self.signal_processing_path.emit(new_path)
            self.signal_task_complete.emit(self.command)
        except FileNotFoundError:
            # --- ГАРАНТИРУЕМ ЗАВЕРШЕНИЕ И ЗДЕСЬ! ---
            self.signal_error.emit(ProcessingConstants.ERROR_FILE_NOT_FOUND)
            self.signal_task_complete.emit(self.command) # <---

    def _save_style_map_to_widget(self):
        # ... логика, похожая на start7 ...
        style_map_data = self._read_json_file(os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['style_map']))
        if style_map_data:
            self._result_text = self._generate_json_string(style_map_data)
            self.signal_processed_text.emit(self._result_text)
            self.signal_task_complete.emit(self.command)
            
    def _save_widget_to_style_map(self):
        # ... логика, похожая на start8 ...
        log_debug(f"_save_widget_to_style_map - self.text_widget: {self.text_widget}")
        widget_text = self.text_widget.toPlainText()
        
        try:
            json_object = json.loads(widget_text)
            self._write_to_json_file(json_object, os.path.join(self.app_data_dir, ProcessingConstants.FILE_PATHS['style_map']))
            self.signal_processed_text.emit("") # В оригинале emit("")
            self.signal_task_complete.emit(self.command)
        except json.JSONDecodeError:
            log_error("Содержимое виджета не является допустимым JSON.")
            self.signal_error.emit("Error: Содержимое виджета не является допустимым JSON.")
            
    def _reset_paths(self):
        # ... логика, похожая на start9 ...
        # Просто сигнализирует о завершении команды
        self.signal_task_complete.emit(self.command)

    def _load_file_to_widget_simple(self, path: str):
        # ... логика, похожая на start10 ...
        try:
            with open(path, 'r', encoding="utf-8-sig") as f:
                self._result_text = f.read()
            self.signal_processed_text.emit(self._result_text)
            self.signal_task_complete.emit(self.command)
        except FileNotFoundError:
            self.signal_error.emit(ProcessingConstants.ERROR_FILE_NOT_FOUND)

    def _load_specific_file(self, path: str, lovie: str):
        # ... логика, похожая на start11 ...
        log_debug(f"{path} {lovie}")
        try:
            
            filename_to_load = ""
            if lovie == "try4" or lovie == "try5":  # Проверяем lovie, а не path
                filename_to_load = path
            else:
                self.signal_error.emit(f"Unknown command in lovie: {lovie}")
                return

            try:
                with open(filename_to_load, 'r', encoding="utf-8-sig") as f:
                    self._result_text = f.read()
                
                # Отправляем результат в TextConverter
                self.signal_filename.emit(self.filename)
                self.signal_processed_text.emit(self._result_text)
                self.signal_processing_path.emit(self.processing_path)
                self.signal_task_complete.emit(self.command)
            except FileNotFoundError:
                self.signal_error.emit(ProcessingConstants.ERROR_FILE_NOT_FOUND)
        
        except Exception as e:
            self.signal_error.emit(f"Ошибка загрузки файла: {str(e)}")         

    def _finish_task(self):
        """Общая логика завершения задачи."""
        self._save_result_to_file()
        self.signal_task_complete.emit(self.command)
        
    
    
