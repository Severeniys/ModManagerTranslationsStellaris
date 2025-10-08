from file_configuration.import_libraries.libraries import *

class MyQFileSystemModel(QFileSystemModel):

    def headerData(self, section, orientation, role):
        if section == 0 and role == Qt.ItemDataRole.DisplayRole:
            return "Имя"
        elif section == 1 and role == Qt.ItemDataRole.DisplayRole:
            return "Размер"
        elif section == 2 and role == Qt.ItemDataRole.DisplayRole:
            return "Тип"
        elif section == 3 and role == Qt.ItemDataRole.DisplayRole:
            return "Дата изменения"