# file_configuration/constants.py
import os
from dataclasses import dataclass
# --- Импорты из QtCore ---
# Все, что связано с базовыми типами данных, событиями, таймерами, потоками, настройками
from PyQt6.QtCore import (    
    QSize, QPoint
    )


@dataclass
class AppSettings:
    language: str = "Russian"
    theme: str = "dark"
    window_size: QSize = QSize(1564, 772)
    window_position: QPoint = QPoint(188, 150)



class ProcessingConstants:    
    
        # Пути к файлам (относительно self.base_resources_path)
    APP_ICON_NAME = "ModManagerTranslationsStellaris.ico"

    CONFIG_DIR = "config"
    FILE_PATHS = {
        'session_map': os.path.join(CONFIG_DIR, "config_c.json"),
        'view_map': os.path.join(CONFIG_DIR, "config_v.json"),
        'style_map': os.path.join(CONFIG_DIR, "config_s.json"),
        'settings': os.path.join(CONFIG_DIR, "app_settings.json"),
        'placeholder_map': os.path.join(CONFIG_DIR, "placeholder_map.json")
    }
    
    SETTINGS_KEY_LANGUAGE = "app_settings/language"
    SETTINGS_KEY_THEME = "app_settings/theme"
    SETTINGS_KEY_WINDOW_POS = "window/pos"
    SETTINGS_KEY_WINDOW_SIZE = "window/size"
    DEFAULT_SETTINGS = AppSettings()

    AIL_L = r"\fail_l.yml"        
            
    
    # Замены для строк (\n -> placeholder и обратно)
    LINE_PLACEHOLDER_MAP = {
        "\\n\\n\\n": " [1] ",
        "\\n\\n": " [2] ",
        "\\n": " [3] "
    }

    # Замены для форматирования (цвета и т.д.)
    FORMATTING_REPLACEMENTS = {
        "\u00a7B": "[4]",
        "\u00a7E": "[5]",
        "\u00a7H": "[6]",
        "\u00a7L": "[7]",
        "\u00a7M": "[8]",
        "\u00a7P": "[9]",
        "\u00a7R": "[10]",
        "\u00a7S": "[11]",
        "\u00a7W": "[12]",
        "\u00a7T": "[13]",
        "\u00a7Y": "[14]",
        "\u00a7G": "[15]",
        "\u00a7C": "[16]",
        "\u00a7I": "[17]",
        "\u00a7d": "[18]",
        "\u00a7b": "[19]",
        "\u00a7r": "[21]",
        "\u00a7K": "[22]",
        "\u00a7!": "[20]"
    }

    # Замены для "лишних" пробелов и кавычек
    SPACE_REPLACEMENTS = {
        " \"\\n\"": "\"\\n\" ",
        "\"\\n\" ": " \"\\n\"",
        " \"": "   \"",
        " \"": "  \""       
    }

    # Специальная замена
    SPECIAL_CHAR_REPLACE = ("$$", "$ $")
    
    # Регулярные выражения (шаблоны)
    REGEX_PATTERNS = { # chablon -> regex_patterns
        "KEYS": [r"\[\S+\]", r"\$\S+\$", r"£\S+£", r"\['\S+'\]", r"'\S+'"],
        "SECTION_HEADER": [r"\A[ ]{0,}\t{0,}[ ]{0,}[^#: ]+:{1}"], # chablonh -> section_header
        "KEY_DEFINITION": r"\A[ ]{0,}\t{0,}[ ]{0,}[^#: ]+:{1}", # chablong -> key_definition
        "KEY_ID": r"\A\t{0,}[ ]{0,}\[00\d+\]" # chablonj -> key_id
    }
    # Тексты для сигналов
    ERROR_FILE_NOT_FOUND = "File not found"
    NEWLINE_CHAR = "\n"
    
    LOCALISATION = ["english", 
                "russian",
                "braz_por",
                "french",
                "german",
                "polish ",
                "simp_chinese",
                "spanish"]
    
    REZERV = ["vs - english - rezerv", 
                "vs - russian - rezerv",
                "vs - braz_por - rezerv",
                "vs - french - rezerv",
                "vs - german - rezerv",
                "vs - polish - rezerv",
                "vs - simp_chinese - rezerv",
                "vs - spanish - rezerv"]   
    
    REZERV_S = r"vs - \S+ - rezerv"
    REZERV_STR = "rezerv"
        
    @classmethod
    def reset_config_path(cls, new_path):
        cls._config_dir_path = new_path
    
    @staticmethod
    def get_language_localisation(selected_language):
        if selected_language == "Russian":
            return (
                "russian"
            )
        elif selected_language == "English":
            return (
                "english"
            )
        elif selected_language == "French":
            return (
                "french"
            )
        elif selected_language == "Braz_por":
            return (
                "braz_por"
            )
        elif selected_language == "German":
            return (
                "german"
            )
        elif selected_language == "Japanese":
            return (
                "japanese"
            )
        elif selected_language == "Korean":
            return (
                "korean"
            )
        elif selected_language == "Polish":
            return (
                "polish"
            )
        elif selected_language == "Simp_chinese":
            return (
                "simp_chinese"
            )
        elif selected_language == "Spanish":
            return (
                "spanish"
            )
        else:
            return (
                "english"
            )

    @staticmethod
    def get_language_map(selected_language):
        """Возвращает словарь для замены языка в путях к файлам."""
        if selected_language == "Russian":
            return {
                "english": "russian",
                "braz_por": "russian",
                "french": "russian",
                "german": "russian",
                "japanese": "russian",
                "korean": "russian",
                "polish": "russian",
                "simp_chinese": "russian",
                "spanish": "russian",
            }
        elif selected_language == "English":  # Пример для французского
            return {                
                "russian": "english",
                "french": "english",
                "braz_por": "english",
                "german": "english",
                "japanese": "english",
                "korean": "english",
                "polish": "english",
                "simp_chinese": "english",
                "spanish": "english",
            }        
        elif selected_language == "French":
            return {
                "english:": "french:",
                "russian:": "french:",
                "braz_por:": "french:",                
                "german:": "french:",
                "japanese:": "french:",
                "korean:": "french:",
                "polish:": "french:",
                "simp_chinese:": "french:",
                "spanish:": "french:"
            }
        elif selected_language == "Braz_por":
            return {
                "english:": "braz_por:",
                "russian:": "braz_por:",                
                "french:": "braz_por:",
                "german:": "braz_por:",
                "japanese:": "braz_por:",
                "korean:": "braz_por:",
                "polish:": "braz_por:",
                "simp_chinese:": "braz_por:",
                "spanish:": "braz_por:"
            }
        elif selected_language == "German":
            return {
                "english:": "german:",
                "russian:": "german:",
                "braz_por:": "german:",
                "french:": "german:",                
                "japanese:": "german:",
                "korean:": "german:",
                "polish:": "german:",
                "simp_chinese:": "german:",
                "spanish:": "german:"
            }
        elif selected_language == "Japanese":
            return {
                "english:": "japanese:",
                "russian:": "japanese:",
                "braz_por:": "japanese:",
                "french:": "japanese:",
                "german:": "japanese:",                
                "korean:": "japanese:",
                "polish:": "japanese:",
                "simp_chinese:": "japanese:",
                "spanish:": "japanese:"
            }
        elif selected_language == "Korean":
            return {
                "english:": "korean:",
                "russian:": "korean:",
                "braz_por:": "korean:",
                "french:": "korean:",
                "german:": "korean:",
                "japanese:": "korean:",                
                "polish:": "korean:",
                "simp_chinese:": "korean:",
                "spanish:": "korean:"
            }
        elif selected_language == "Polish":
            return {
                "english:": "polish:",
                "russian:": "polish:",
                "braz_por:": "polish:",
                "french:": "polish:",
                "german:": "polish:",
                "japanese:": "polish:",
                "korean:": "polish:",                
                "simp_chinese:": "polish:",
                "spanish:": "polish:"
            }
        elif selected_language == "Simp_chinese":
            return {
                "english:": "simp_chinese:",
                "russian:": "simp_chinese:",
                "braz_por:": "simp_chinese:",
                "french:": "simp_chinese:",
                "german:": "simp_chinese:",
                "japanese:": "simp_chinese:",
                "korean:": "simp_chinese:",
                "polish:": "simp_chinese:",                
                "spanish:": "simp_chinese:"
            }
        elif selected_language == "Spanish":
            return {
                "english:": "spanish:",
                "russian:": "spanish:",
                "braz_por:": "spanish:",
                "french:": "spanish:",
                "german:": "spanish:",
                "japanese:": "spanish:",
                "korean:": "spanish:",
                "polish:": "spanish:",
                "simp_chinese": "spanish:",               
                "spanish:": "spanish:"
            }        
        else:
            return {
                "russian:": "english:",
                "braz_por:": "english:",
                "french:": "english:",
                "german:": "english:",
                "japanese:": "english:",
                "korean:": "english:",
                "polish:": "english:",
                "simp_chinese:": "english:",
                "spanish:": "english:"
            }
    
    @staticmethod
    def get_language_replacements(selected_language):
        if selected_language == "Russian":
            return {
                "l_english:": "l_russian:",               
                "l_braz_por:": "l_russian:",
                "l_french:": "l_russian:",
                "l_german:": "l_russian:",
                "l_japanese:": "l_russian:",
                "l_korean:": "l_russian:",
                "l_polish:": "l_russian:",
                "l_simp_chinese:": "l_russian:",
                "l_spanish:": "l_russian:"
            }
        elif selected_language == "English":
            return {
                "l_russian:": "l_english:",
                "l_braz_por:": "l_english:",
                "l_french:": "l_english:",
                "l_german:": "l_english:",
                "l_japanese:": "l_english:",
                "l_korean:": "l_english:",
                "l_polish:": "l_english:",
                "l_simp_chinese:": "l_english:",
                "l_spanish:": "l_english:"
            }
        elif selected_language == "French":
            return {
                "l_english:": "l_french:",
                "l_russian:": "l_french:",
                "l_braz_por:": "l_french:",                
                "l_german:": "l_french:",
                "l_japanese:": "l_french:",
                "l_korean:": "l_french:",
                "l_polish:": "l_french:",
                "l_simp_chinese:": "l_french:",
                "l_spanish:": "l_french:"
            }
        elif selected_language == "Braz_por":
            return {
                "l_english:": "l_braz_por:",
                "l_russian:": "l_braz_por:",                
                "l_french:": "l_braz_por:",
                "l_german:": "l_braz_por:",
                "l_japanese:": "l_braz_por:",
                "l_korean:": "l_braz_por:",
                "l_polish:": "l_braz_por:",
                "l_simp_chinese:": "l_braz_por:",
                "l_spanish:": "l_braz_por:"
            }
        elif selected_language == "German":
            return {
                "l_english:": "l_german:",
                "l_russian:": "l_german:",
                "l_braz_por:": "l_german:",
                "l_french:": "l_german:",                
                "l_japanese:": "l_german:",
                "l_korean:": "l_german:",
                "l_polish:": "l_german:",
                "l_simp_chinese:": "l_german:",
                "l_spanish:": "l_german:"
            }
        elif selected_language == "Japanese":
            return {
                "l_english:": "l_japanese:",
                "l_russian:": "l_japanese:",
                "l_braz_por:": "l_japanese:",
                "l_french:": "l_japanese:",
                "l_german:": "l_japanese:",                
                "l_korean:": "l_japanese:",
                "l_polish:": "l_japanese:",
                "l_simp_chinese:": "l_japanese:",
                "l_spanish:": "l_japanese:"
            }
        elif selected_language == "Korean":
            return {
                "l_english:": "l_korean:",
                "l_russian:": "l_korean:",
                "l_braz_por:": "l_korean:",
                "l_french:": "l_korean:",
                "l_german:": "l_korean:",
                "l_japanese:": "l_korean:",                
                "l_polish:": "l_korean:",
                "l_simp_chinese:": "l_korean:",
                "l_spanish:": "l_korean:"
            }
        elif selected_language == "Polish":
            return {
                "l_english:": "l_polish:",
                "l_russian:": "l_polish:",
                "l_braz_por:": "l_polish:",
                "l_french:": "l_polish:",
                "l_german:": "l_polish:",
                "l_japanese:": "l_polish:",
                "l_korean:": "l_polish:",                
                "l_simp_chinese:": "l_polish:",
                "l_spanish:": "l_polish:"
            }
        elif selected_language == "Simp_chinese":
            return {
                "l_english:": "l_simp_chinese:",
                "l_russian:": "l_simp_chinese:",
                "l_braz_por:": "l_simp_chinese:",
                "l_french:": "l_simp_chinese:",
                "l_german:": "l_simp_chinese:",
                "l_japanese:": "l_simp_chinese:",
                "l_korean:": "l_simp_chinese:",
                "l_polish:": "l_simp_chinese:",                
                "l_spanish:": "l_simp_chinese:"
            }
        elif selected_language == "Spanish":
            return {
                "l_english:": "l_spanish:",
                "l_russian:": "l_spanish:",
                "l_braz_por:": "l_spanish:",
                "l_french:": "l_spanish:",
                "l_german:": "l_spanish:",
                "l_japanese:": "l_spanish:",
                "l_korean:": "l_spanish:",
                "l_polish:": "l_spanish:",                
                "l_simp_chinese:": "l_spanish:"
            }
        else:
            return {
                "l_russian:": "l_english:",
                "l_braz_por:": "l_english:",
                "l_french:": "l_english:",
                "l_german:": "l_english:",
                "l_japanese:": "l_english:",
                "l_korean:": "l_english:",
                "l_polish:": "l_english:",
                "l_simp_chinese:": "l_english:",
                "l_spanish:": "l_english:"
            }
    
