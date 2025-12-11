import os
import re
import shutil

from PyQt6.QtCore import (
    QObject, pyqtSignal
    )

from file_configuration.constants import ProcessingConstants
from file_configuration.utils import log_debug, log_error, log_info, log_warning

class LocalisationManagerThread(QObject):
    """
    Управляет процессом копирования, подготовки и применения локализации модов.
    """
    finishSignalLocalisation_1 = pyqtSignal(str)
    finishSignalLocalisation_2 = pyqtSignal(str)
    finishSignalLocalisation_3 = pyqtSignal(str)

    def __init__(self, target_language, base_dir, stellaris_dir, source_dir, source_language=None):
        """
        Инициализирует поток для работы с локализацией.

        :param target_language: Язык, в который переводим (например, 'russian').
        :param base_dir: Базовая директория для результата. Для подготовки это "Сборка", для копирования в игру - "Индекс".
        :param source_dir: Директория-источник. Для подготовки это папка мода в Steam.
        :param stellaris_dir: Директория с модами Stellarис. Требуется для copy_to_game_mod.
        :param source_language: Язык, который копируем (оригинал, например, 'english').
        """
        super().__init__()
        self.target_language = target_language
        self.base_dir = base_dir  # "Сборка" или "Индекс" в зависимости от задачи
        self.stellaris_dir = stellaris_dir # Папка мода в Steam
        self.source_dir = source_dir          
        self.source_language = source_language        
        self.staging_localisation_dir = os.path.join(self.source_dir, "localisation")
        if self.source_language:
            self.folders_to_copy = [self.source_language, 'random_names', 'replace']
        self.rezerv = ProcessingConstants.REZERV

    
    def update_mod_name(self, createt=True):
        """
        Обновляет имя папки мода в "Сборке" на основе данных из descriptor.mod.
        
        :param mod_dir_in_assembly: Папка мода в "Сборке", имя которого нужно обновить.
        :param steam_mods_content_dir: Путь к папке `steamapps/workshop/content/281990`.
        """
        log_info("Начало задачи: обновление имени мода")
        try:
                        
            mod_dir_in_assembly = self.base_dir
            # 2. Используем self.source_dir            
            steam_mods_content_dir = self.source_dir
            # 1. Извлекаем ID мода из пути к папке в Сборке
            # Например, "D:/Сборки/My Mod - 123456789"
            if createt: 
                log_debug("Выполнение обновление имени") 
                folder_name = os.path.basename(mod_dir_in_assembly)
            else:                   
                folder_name = os.path.basename(steam_mods_content_dir)
            match = re.search(r"\d{9,10}", folder_name)
            if not match:
                self.vozvrat_signal("Ошибка: Не удалось найти ID мода в имени папки.")                
                return
            mod_id = match.group(0) # "123456789"

            # 2. Формируем путь к descriptor.mod в Steam
            # Например, "D:/Games/steam/steamapps/workshop/content/281990/123456789/descriptor.mod"
            if createt:    
                last_folderdes = os.path.join(steam_mods_content_dir, mod_id, "descriptor.mod")
            else:
                last_folderdes = os.path.join(steam_mods_content_dir, "descriptor.mod")
            # 3. Читаем имя мода из файла
            if not os.path.exists(last_folderdes):
                self.vozvrat_signal(f"Ошибка: Файл descriptor.mod не найден по пути:\n{last_folderdes}")
                return

            with open(last_folderdes, encoding="utf8") as f:
                name_linesi = f.read()
                
            name_match = re.search(r"name=\"(.+?)\"", name_linesi)
            log_debug(f"update_mod_name - name_match: {name_match}")
            if not name_match:
                self.vozvrat_signal("Ошибка: Не удалось найти имя мода в файле descriptor.mod.")
                return
                
            original_name = name_match.group(1) # "My Cool Mod"
            log_debug(f"update_mod_name - original_name: {original_name}")
            
            # 4. Очищаем имя от запрещенных символов
            for old, new in [("\"", ""), (":", " -"), ("/", "_"), ("*", "0")]:
                original_name = original_name.replace(old, new)
            log_debug(f"update_mod_name - original_name: {original_name}")
            # 5. Формируем новое имя папки
            # Например, "My Cool Mod - 123456789"
            new_folder_name = f"{original_name} - {mod_id}"
            log_debug(f"update_mod_name - new_folder_name: {new_folder_name}")
            # 6. Полный путь к новой папке
            if createt:
                mod_dir_in_assembly = os.path.dirname(mod_dir_in_assembly)
            new_dir_path = os.path.join(mod_dir_in_assembly, new_folder_name)
            log_debug(f"update_mod_name - new_dir_path: {new_dir_path}")
            # 7. Переименовываем папку
            
            if os.path.exists(new_dir_path):                
                log_debug(f"Error: Папка '{new_folder_name}' уже существует.")
                # Можно предложить пользователю обновить существующую папку
                self.finishSignalLocalisation_3.emit(new_folder_name, new_dir_path)                
                return # Выходим, т.к. обновление - это отдельная задача
                
            if createt:    
                if os.path.exists(mod_dir_in_assembly):
                    os.rename(self.base_dir, new_dir_path)
                    log_debug(f"Папка переименована: {mod_dir_in_assembly} -> {new_dir_path}")
                    self.vozvrat_signal(f"Имя мода успешно обновлено на: {new_folder_name}")
                else:
                    self.vozvrat_signal(f"Ошибка: Папка мода не найдена: {mod_dir_in_assembly}")
            else:
                return new_dir_path
            
        except FileNotFoundError as e:
            log_error(f"Ошибка при обновлении имени: Файл не найден {e}")
            self.vozvrat_signal(f"Ошибка: Файл не найден. {e}")
        except PermissionError as e:
            log_error(f"Ошибка при обновлении имени: Нет доступа {e}")
            self.vozvrat_signal(f"Ошибка: Нет прав на доступ/переименование. {e}")
        except Exception as e:
            log_error(f"Неизвестная ошибка при обновлении имени: {e}")
            self.vozvrat_signal(f"Произошла неизвестная ошибка: {e}")
    # --- Единый метод для подготовки и обновления ---
    def sync_with_steam_mod(self, prepare_mode=True):
        """
        Синхронизирует локализацию из каталога Steam (source_dir) с папкой Сборки (base_dir).
        """
        log_debug("--- НАЧАЛО СИНХРОНИЗАЦИИ ---")
        log_debug(f"Режим: {'ПОДГОТОВКА' if prepare_mode else 'ОБНОВЛЕНИЕ'}")
        log_debug(f"Исходный язык: {self.source_language}, Целевой язык: {self.target_language}")
        log_debug(f"self.source_language: {self.source_language}")
        log_debug(f"self.target_language: {self.target_language}")
        log_debug(f"self.source_dir (Steam): {self.source_dir}")
        log_debug(f"self.base_dir (Сборки): {self.base_dir}")

        try:
            # --- 1. Определение целевой папки ---
            if prepare_mode:
                target_mod_dir_in_base = self.update_mod_name(False)                
            else:
                mod_name_in_staging = os.path.basename(os.path.normpath(self.source_dir))
                target_mod_dir_name = self.update_mod_name(False) # Возвращает полный путь
                target_mod_dir_in_base = os.path.dirname(target_mod_dir_name) # Берем только папку "Сборки")                
            
            os.makedirs(target_mod_dir_in_base, exist_ok=True)
            log_debug(f"Целевая папка гарантированно создана/существует: {target_mod_dir_in_base}")
            
            if prepare_mode:
                # --- РЕЖИМ: ПОДГОТОВКА ---
                log_info("РЕЖИМ: ПОДГОТОВКА К ПЕРЕВОДУ.")
                
                rezerv_dir = os.path.join(target_mod_dir_in_base, f"vs - {self.source_language} - rezerv")
                work_dir = os.path.join(target_mod_dir_in_base, f"vs - {self.target_language}")
                
                os.makedirs(rezerv_dir, exist_ok=True)         
                os.makedirs(work_dir, exist_ok=True)
                
                self._copy_language_files(self.staging_localisation_dir, rezerv_dir, self.source_language)
                self._copy_language_files(self.staging_localisation_dir, work_dir, self.source_language) 
                
                self._finalize_translation_files(work_dir)                
                self.vozvrat_signal("Файлы для перевода успешно подготовлены.")

            else:
                # --- РЕЖИМ: ОБНОВЛЕНИЕ ---
                log_info("РЕЖИМ: ОБНОВЛЕНИЕ ФАЙЛОВ.")
                
                # ! ВАЖНО: Нам нужно обновить конкретно папку с локализацией, а не весь мод.
                # Формируем ПРАВИЛЬНЫЙ путь до целевой папки с локализацией
                target_localisation_dir_to_update = os.path.join(target_mod_dir_in_base, f"vs - {self.target_language}")
                
                if not os.path.exists(target_localisation_dir_to_update):
                    log_warning(f"Папка для обновления '{target_localisation_dir_to_update}' не найдена. Возможно, мод еще не подготовлен.")
                    self.vozvrat_signal(f"Ошибка: папка локализации '{self.target_language}' не найдена. Сначала подготовьте мод.")
                    return

                # Вызываем новый, улучшенный метод обновления
                # Передаем ему исходную папку (Steam) и целевую папку (локализация в сборке)
                self._update_existing_files(self.staging_localisation_dir, target_localisation_dir_to_update)
                
                self.vozvrat_signal(f"Локализация для '{self.target_language}' успешно обновлена.")

        except FileExistsError:
            log_error(f"Ошибка: Папка {target_mod_dir_in_base} уже существует и не является пустой. Попробуйте удалить ее вручную.")
            self.vozvrat_signal(f"Ошибка: Папка уже существует.")
        except PermissionError:
            log_error(f"Ошибка: Нет прав на запись в папку {target_mod_dir_in_base}.")
            self.vozvrat_signal(f"Ошибка: Нет прав на запись.")
        except Exception as e:
            # Логируем полное сообщение об ошибке и тип
            log_error(f"КРИТИЧЕСКАЯ ОШИБКА при синхронизации: {type(e).__name__} - {e}")
            self.vozvrat_signal(f"Произошла ошибка: {e}")
        finally:
            log_debug("--- КОНЕЦ СИНХРОНИЗАЦИИ ---")
            log_debug("-" * 30)

    
    def _update_existing_files(self, source_dir, target_dir):
        """
        "Умное" обновление локализации (гибкая версия).
        Копирует файлы из source_dir (Steam) в target_dir (Сборка), если их там нет.
        Сохраняет всю исходную структуру папок, заменяя только папку языка.
        """
        log_debug("="*50)
        log_debug(f"ЗАПУСК _update_existing_files (ГИБКАЯ ВЕРСИЯ)")
        log_debug(f"ИСХОДНАЯ директория: {source_dir}")
        log_debug(f"ЦЕЛЕВАЯ директория: {target_dir}")
        log_debug("="*50)

        source_suffix = f"_{self.source_language}.yml"
        target_suffix = f"_{self.target_language}.yml"
        log_debug(f"Ищем файлы с суффиксом: '{source_suffix}'")

        # Рекурсивно проходим по ВСЕМ файлам в исходной директории
        for root, _, files in os.walk(source_dir):
            for file_name in files:
                # Берем ТОЛЬКО файлы нужного языка
                if file_name.endswith(source_suffix):
                    source_file_path = os.path.join(root, file_name)
                    
                    # 1. Преобразуем путь!
                    target_file_path = self._transform_path_for_target(source_file_path, source_dir, target_dir)
                    if not target_file_path:
                        log_error(f"Не удалось преобразовать путь для файла: {source_file_path}")
                        continue # Пропускаем этот файл

                    # 2. Формируем новое имя файла (меняем суффикс)
                    target_file_name = file_name.replace(source_suffix, target_suffix)
                    # Заменяем имя файла в полном пути
                    final_target_file_path = os.path.join(os.path.dirname(target_file_path), target_file_name)
                    
                    log_debug(f"-> НАЙДЕН файл: '{source_file_path}'")
                    log_debug(f"   Целевой путь:  '{final_target_file_path}'")

                    # 3. Проверяем существование и копируем
                    if not os.path.exists(final_target_file_path):
                        log_debug(f"   [!] Файла НЕТ. КОПИРУЮ И ПРЕОБРАЗОВЫВАЮ...")
                        try:
                            with open(source_file_path, 'r', encoding="utf8") as f:
                                content = f.read()
                            
                            old_prefix = f'l_{self.source_language}:'
                            new_prefix = f'l_{self.target_language}:'
                            log_debug(f"   Замена префикса: '{old_prefix}' -> '{new_prefix}'")
                            
                            if old_prefix not in content:
                                log_warning(f"   ПРЕДУПРЕЖДЕНИЕ: В файле не найден префикс '{old_prefix}'.")
                            else:
                                content = content.replace(old_prefix, new_prefix)
                            
                            # Создаем все необходимые папки для конечного файла
                            os.makedirs(os.path.dirname(final_target_file_path), exist_ok=True)
                            
                            with open(final_target_file_path, 'w', encoding="utf8") as f:
                                f.write(content)
                            
                            log_debug(f"   [УСПЕХ] Файл '{target_file_name}' добавлен.")
                        except Exception as e:
                            log_error(f"   [ОШИБКА] Не удалось обработать файл: {e}")
                    else:
                        log_debug(f"   [SKIP] Файл уже существует. Пропускаю.")
                else:
                    log_debug(f"-> Пропускаю файл с другим суффиксом: '{file_name}'")

        log_debug("="*50)
        log_debug("ЗАВЕРШЕНИЕ _update_existing_files")
        log_debug("="*50)
    
    def _transform_path_for_target(self, source_file_full_path, source_stem_dir, target_stem_dir):
        """
        Превращает путь к файлу из исходной директории в путь для целевой директории.
        Пример:
            source_file_full_path: 'D:/Steam/.../localisation/english/events/my_event.yml'
            source_stem_dir:        'D:/Steam/.../localisation'
            target_stem_dir:        'F:/Сборки/.../vs - russian'
            
            Возвращает: 'F:/Сборки/.../vs - russian/russian/events/my_event.yml'
        """
        # 1. Получаем путь относительно корня исходной директории
        # Например, 'english/events/my_event.yml'
        relative_path = os.path.relpath(source_file_full_path, source_stem_dir)
        log_debug(f"    -> Преобразование относительного пути: '{relative_path}'")

        # 2. Заменяем имя папки языка в начале пути на целевое имя
        # Например, заменяем 'english/' на 'russian/'
        parts = []
        # Разбиваем путь на части: ['english', 'events', 'my_event.yml']
        path_parts = relative_path.split(os.sep)
        
        if path_parts: # Убедимся, что список не пуст
            # Заменяем первую часть (имя папки языка)
            path_parts[0] = self.target_language
            # Соединяем обратно: 'russian/events/my_event.yml'
            transformed_relative_path = os.sep.join(path_parts)
            log_debug(f"    -> Преобразованный относительный путь: '{transformed_relative_path}'")
            
            # 3. Соединяем с целевой директорией
            final_target_path = os.path.join(target_stem_dir, transformed_relative_path)
            return final_target_path
            
        return None
    
    # --- Метод для копирования в папку мода Stellaris ---


    def copy_to_game_mod(self):        
        """
        Копирует локализацию для ОДНОГО целевого языка (self.target_language).
        Определяет, был ли клик на папку-сборку или на конкретный мод,
        основываясь на содержимих папки (наличии подпапок 'vs - language').
        - При клике на сборку: очищает папку localisation и копирует файлы из всех вложенных модов.
        - При клике на конкретный мод: копирует файлы только из этого мода, не очищая localisation.
        """
        # --- 1. Проверка входных данных (без изменений) ---
        if not self.source_dir or not os.path.isdir(self.source_dir):
            msg = "Ошибка: Базовый путь к папке 'Сборки' (source_dir) не задан или неверный."
            log_error(msg)
            self.vozvrat_signal(msg)
            return
        if not self.base_dir or not os.path.isdir(self.base_dir):
            msg = "Ошибка: Путь к папке мода/сборки (base_dir) не задан или неверный."
            log_error(msg)
            self.vozvrat_signal(msg)
            return
        if not self.stellaris_dir or not os.path.isdir(self.stellaris_dir):
            msg = "Ошибка: Путь к папке модов Stellaris (stellaris_dir) не задан или неверный."
            log_error(msg)
            self.vozvrat_signal(msg)
            return
        if not hasattr(self, 'target_language') or not self.target_language:
            msg = "Ошибка: Целевой язык (target_language) не задан."
            log_error(msg)
            self.vozvrat_signal(msg)
            return

        # --- 2. НОВАЯ ЛОГИКА ОПРЕДЕЛЕНИЯ ИМЕНИ ЦЕЛЕВОЙ ПАПКИ (без изменений) ---
        relative_path = os.path.normpath(os.path.relpath(self.base_dir, self.source_dir))
        collection_name_with_id = relative_path.split(os.sep)[0]
        log_debug(f"copy_to_game_mod - collection_name: {collection_name_with_id}")
        pattern_to_remove = r"\s-\s\d{9,10}$"
        clean_collection_name = re.sub(pattern_to_remove, "", collection_name_with_id).strip()
        if clean_collection_name:
            collection_name = clean_collection_name
        else:
            # Это может произойти, если имя было ТОЛЬКО ID. Используем исходное имя.
            collection_name = collection_name_with_id
        log_debug(f"copy_to_game_mod - collection_name: {collection_name}")
        target_mod_base_path = os.path.join(self.stellaris_dir, collection_name)
        target_localisation_path = os.path.join(target_mod_base_path, "localisation")

        if not os.path.exists(target_mod_base_path) or not os.path.isdir(target_mod_base_path):
            msg = (
                f"Ошибка целостности сборки.\n\n"
                f"Не удалось найти папку с именем '{collection_name}' "
                f"в директории Stellaris/mod:\n{self.stellaris_dir}\n\n"
                f"Это имя было вычислено на основе пути:\n{self.base_dir}"
            )
            log_error(f"Проверка не пройдена: целевая папка '{target_mod_base_path}' отсутствует.")
            self.vozvrat_signal(msg)
            return

        # --- 3. ИЗМЕНЕННАЯ ЛОГИКА ОПРЕДЕЛЕНИЯ РЕЖИМА РАБОТЫ ---
        is_single_mod = False
        try:
            all_items_in_base_dir = next(os.walk(self.base_dir))[1] # Список ВСЕХ вложенных папок
            log_debug(f"В папке '{self.base_dir}' найдено элементов: {len(all_items_in_base_dir)}")

            # Проверяем, есть ли среди них папки, которые НЕ ЯВЛЯЮТСЯ папками языка ('vs - ...')
            # Если таких папок нет, значит, мы в папке одного сложного мода.
            has_non_language_folders = any(
                not item.startswith("vs - ") for item in all_items_in_base_dir
            )

            if not has_non_language_folders and all_items_in_base_dir:
                # Все папки внутри - это 'vs - ...', значит, это ОДИН мод
                is_single_mod = True
                log_debug(f"Определен режим: 'КОПИРОВАНИЕ ОДНОГО МОДА'.")
                log_debug(f"Все вложенные папки ('{', '.join(all_items_in_base_dir)}') выглядят как папки локализации.")
            else:
                # Нашлись папки, не похожие на 'vs - ...', значит, это СБОРКА модов
                log_debug(f"Определен режим: 'КОПИРОВАНИЕ СБОРКИ МОДОВ'.")
                log_debug(f"Найдены папки, не являющиеся локализациями.")

        except StopIteration:
            # Папка base_dir пуста
            is_single_mod = True
            log_debug(f"Определен режим: 'КОПИРОВАНИЕ ОДНОГО МОДА' (папка пуста, но путь указан на мод).")

        # --- 4. УСЛОВНАЯ ОЧИСТКА (без изменений, но теперь relies on correct flag) ---
        if not is_single_mod:
            log_debug(f"РЕЖИМ СБОРКИ: ОДНОКРАТНАЯ очистка папки: {target_localisation_path}")
            os.makedirs(target_localisation_path, exist_ok=True)
            if os.path.exists(target_localisation_path):
                for item in os.listdir(target_localisation_path):
                    item_path = os.path.join(target_localisation_path, item)
                    try:
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                    except Exception as e:
                        log_error(f"  Не удалось удалить '{item_path}': {e}")
        else:
            log_debug(f"РЕЖИМ ОДНОГО МОДА: Очистка папки {target_localisation_path} НЕ производится.")

        # --- 5. Определяем, какие папки обрабатывать ---
        # Если режим "сборка", то обрабатываем все найденные папки.
        # Если режим "один мод", то обрабатываем только ту, что совпадает с целевым языком.
        mod_folders_to_process = []
        if not is_single_mod:
            mod_folders_to_process = all_items_in_base_dir
        else:
            target_lang_folder = f"vs - {self.target_language}"
            if target_lang_folder in all_items_in_base_dir:
                mod_folders_to_process = [target_lang_folder]
            else:
                log_debug(f"  В режиме 'один мод' целевая папка '{target_lang_folder}' не найдена. Копирование невозможно.")
                # Копирование не произойдет, т.к. список для обработки пуст

        log_debug(f"--- Будут обработаны следующие папки: {mod_folders_to_process} ---")

        # --- 6. Основной цикл по модам ---
        copied_mods_count = 0
        for mod_folder_name in mod_folders_to_process:
            log_debug(f"--- Обработка мода/языка: '{mod_folder_name}' ---")
            
            source_mod_path = os.path.join(self.base_dir, mod_folder_name)
            # В режиме "один мод" мы уже знаем, что source_lang_path - это и есть сама папка
            source_lang_path = source_mod_path if is_single_mod else os.path.join(source_mod_path, f"vs - {self.target_language}")
            
            # Эта проверка все еще нужна, если пользователь выберет не тот язык
            if not os.path.exists(source_lang_path):
                log_debug(f"  Предупреждение: Папка локализации не найдена по пути '{source_lang_path}'. Пропускаю.")
                continue

            # --- 7. КОПИРУЕМ ФАЙЛЫ ---
            log_debug(f"  Копирую из '{source_lang_path}' в '{target_localisation_path}'...")
            try:
                for item in os.listdir(source_lang_path):
                    source_item_path = os.path.join(source_lang_path, item)
                    target_item_path = os.path.join(target_localisation_path, item)
                    
                    if os.path.isdir(source_item_path):
                        shutil.copytree(source_item_path, target_item_path, dirs_exist_ok=True)
                    else:
                        shutil.copy2(source_item_path, target_item_path)
                
                process_description = "мода" if not is_single_mod else "языка"
                log_debug(f"  Успешно добавлена локализация для '{self.target_language}' из {process_description} '{mod_folder_name}'.")
                copied_mods_count += 1
            except Exception as e:
                log_error(f"  Ошибка при копировании локализации для '{mod_folder_name}': {e}")
                continue

        # --- 8. Финальный отчет ---
        mode_description = "сборки модов" if not is_single_mod else f"мода '{os.path.basename(self.base_dir)}'"
        if copied_mods_count > 0:
            success_message = (
                f"Готово! Локализация для языка '{self.target_language}' успешно установлена.\n"
                f"Источник: {mode_description}.\n"
                f"Количество скопированных элементов: {copied_mods_count}."
            )
            log_debug(success_message)
            self.vozvrat_signal(success_message)
        else:
            info_message = (
                f"Информация: Локализация для языка '{self.target_language}' не была установлена.\n\n"
                f"Режим: {mode_description}.\n"
                f"Возможные причины:\n"
                f"1. Не найдена папка с локализацией для целевого языка.\n"
                f"2. Папки с локализацией пусты."
            )
            log_debug(info_message)
            self.vozvrat_signal(info_message)

    # --- Вспомогательные (приватные) методы ---
    def _copy_language_files(self, source_localisation_dir, target_dir, language_code):
        """Копирует файлы локализации для указанного языка."""
        for root, _, files in os.walk(source_localisation_dir):
            if root == source_localisation_dir:
                for file in files:
                    if file.endswith(f'{language_code}.yml'):
                        shutil.copy2(os.path.join(root, file), os.path.join(target_dir, file))
                        log_debug(f"Главный файл скопирован: {file}")
            
            elif os.path.basename(root) == language_code:
                dest_folder = os.path.join(target_dir, os.path.basename(root))
                os.makedirs(dest_folder, exist_ok=True)
                for file in files:
                    shutil.copy2(os.path.join(root, file), os.path.join(dest_folder, file))
                log_debug(f"Папка языка '{language_code}' скопирована.")

            elif os.path.basename(root) in ['replace']:
                if any(f.endswith(f'_{language_code}.yml') for f in files):
                    dest_folder = os.path.join(target_dir, os.path.basename(root))
                    os.makedirs(dest_folder, exist_ok=True)
                    for file in files:
                        if file.endswith(f'_{language_code}.yml') or not f'_' in file:
                            shutil.copy2(os.path.join(root, file), os.path.join(dest_folder, file))
                    log_debug(f"Файлы для языка '{language_code}' скопированы из папки '{os.path.basename(root)}'")

    def _finalize_translation_files(self, work_dir):
        """Подготавливает рабочие файлы: переименовывает и меняет префикс."""
        log_debug("Начало финализации файлов...")
        # Переименование
        for root, dirs, files in os.walk(work_dir, topdown=False):
            for filename in files:
                if self.source_language in filename and filename.endswith('.yml'):
                    old_name = os.path.join(root, filename)
                    new_name = old_name.replace(f'_{self.source_language}.yml', f'_{self.target_language}.yml')
                    try:
                        os.rename(old_name, new_name)
                    except OSError as e:
                        log_error(f"Не удалось переименовать файл {filename}: {e}")
            
            for dir_name in dirs:
                if self.source_language in dir_name:
                    old_path = os.path.join(root, dir_name)
                    new_path = old_path.replace(self.source_language, self.target_language)
                    try:
                        os.rename(old_path, new_path)
                    except OSError as e:
                        log_error(f"Не удалось переименовать папку {dir_name}: {e}")
        
        # Смена префикса в содержимом
        old_prefix = f'l_{self.source_language}:'
        new_prefix = f'l_{self.target_language}:'
        for root, _, files in os.walk(work_dir):
            for filename in files:
                if filename.endswith('.yml'):
                    filepath = os.path.join(root, filename)
                    try:
                        with open(filepath, 'r', encoding="utf8") as f:
                            content = f.read()
                        content = content.replace(old_prefix, new_prefix)
                        with open(filepath, 'w', encoding="utf8") as f:
                            f.write(content)
                    except Exception as e:
                        log_error(f"Не удалось изменить файл {filepath}: {e}")

    def _validate_source_directory(self):
        """Проверяет каталог на наличие пустых папок."""
        for root, dirs, _ in os.walk(self.base_dir):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):
                    self.vozvrat_signal(f"В каталоге {os.path.basename(self.base_dir)} пустая папка: {dir_name}.")
                    return False
        return True

    # --- Утилиты ---
    def clean_directory(self, path):
        """Рекурсивно удаляет пустые директории."""
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                self.clean_directory(item_path)
                if not os.listdir(item_path):
                    log_debug(f"Удалена пустая директория: {item_path}")
                    os.rmdir(item_path)
        if not os.listdir(path):
            log_debug(f"Удалена пустая директория: {path}")
            os.rmdir(path)
        
    # --- Сигналы ---
    def vozvrat_signal(self, text):
        self.finishSignalLocalisation_1.emit(text)
        