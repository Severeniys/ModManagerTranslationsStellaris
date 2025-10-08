from file_configuration.import_libraries.libraries import *


class GetDialsThread2(QObject):
    finishSignal_1 = pyqtSignal(str)
    finishSignal_2 = pyqtSignal(str)
    def __init__(self, path_1, path_2, path_3=None, lokal=None, name=None):
        super(GetDialsThread2, self).__init__()
        self.path_1, self.path_2, self.path_3, self.lokal, self.name = path_1, path_2, path_3, lokal, name 
        self.path_2_local = f"{self.path_2}/localisation"
        self.folders_to_copy = [f'{self.lokal}', 'random_names', 'replace']  
        self.rezerv = ["vs - english - rezerv", 
                  "vs - russian - rezerv",
                  "vs - braz_por - rezerv",
                  "vs - french - rezerv",
                  "vs - german - rezerv",
                  "vs - polish - rezerv",
                  "vs - simp_chinese - rezerv",
                  "vs - spanish - rezerv"]        
    def start1(self): 
        if "localisation" in next(os.walk(self.path_2))[1]:            
            with open(f"{self.path_2}\descriptor.mod", encoding="utf8") as f:
                self.linesi = f.read()                                
            f.close()
            name = (re.findall("name=\".+\"", self.linesi))[0]            
            for x, y in ("name=\"", ""), \
                        ("\"", ""), \
                        (":", " -"), \
                        ("/", "_"), \
                        ("*", "0"):                
                name = name.replace(x, y)
            name = f"{name} - {self.path_2.split('/')[-1]}"            
            os.chdir(self.path_1)
            if not os.path.isdir(f"{name}"):                
                os.mkdir(f"{name}")
            os.chdir(f"{self.path_1}/{name}")                  
            if not os.path.isdir(f"vs - {self.lokal} - rezerv"):            
                os.mkdir(f"vs - {self.lokal} - rezerv") 
            self.path_1_name_lokal = f"{self.path_1}/{name}/vs - {self.lokal} - rezerv"            
                        
            i = 0                     
            # Копирование папок
            for root, dirs, files in os.walk(self.path_2_local):                         
                # Проверка, является ли текущая папка одной из папок для копирования
                if os.path.basename(root) in self.folders_to_copy:                 
                    # Полный путь к папке в целевом каталоге
                    dest_folder = os.path.join(self.path_1_name_lokal, os.path.relpath(root, self.path_2_local))# Получение относительного пути папки относительно исходного каталога
                    # Создание папки в целевом каталоге, если она не существует
                    os.makedirs(dest_folder, exist_ok=True)                                            
            
                    # Копирование файлов в папку назначения
                    for file in files:                                            
                        if self.check_filename(file): #file.endswith(f'{self.lokal}.yml'):                                  
                            shutil.copy(os.path.join(root, file), os.path.join(dest_folder, file)  )
                            
                if root == self.path_2_local:
                    for file in files:                                   
                        if file.endswith(f'{self.lokal}.yml'):                         
                            shutil.copy(os.path.join(root, file), os.path.join(self.path_1_name_lokal, file))
                            
            self.clean_directory(self.path_1_name_lokal)
            self.copy_and_rename_directory(self.path_1_name_lokal, f"{self.path_1}/{name}/vs - russian")
            self.vozvrat_signal("False")
        else: 
            self.vozvrat_signal("У этого мода нет папки \"localisation\"")
        
    def start2(self): #self.path_1 = ИНДЕКС self.path_2 = сборка self.path_3 = мод стелларис 
        self.prov2 = self.path_1.split("/")[-1]       
        self.dirs1 = next(os.walk(self.path_2))[1]           
        prov1 = os.path.basename(os.path.normpath(self.path_1))
        previous_element = self.path_1.split("/")[-2]
        otl = re.findall("vs - \S+ - rezerv", self.path_1)
        if otl != []:            
            otl = otl[0]        
        if otl in self.rezerv:
            self.vozvrat_signal(f"Папка {prov1} является резевной копией и не подлежит этому действию")
            return        
        
        if prov1 in self.dirs1:             
            for dirs in next(os.walk(f"{self.path_1}"))[1]:
                if [] == next(os.walk(f"{self.path_1}/{dirs}"))[1]:
                    self.vozvrat_signal(f"В каталоге этого мода пустая папка мода удалите её и повторите действие")
                    return
                path_1_ = f"{self.path_1}/{dirs}/vs - russian"
                path_2_ = f"{self.path_2}/{prov1}/localisation"                
                shutil.copytree(path_1_, path_2_, dirs_exist_ok=True)
        elif prov1 == "vs - russian":
            path_1_ = f"{self.path_1}"
            path_2_ = f"{self.path_2}/{prov1}/localisation"
            shutil.copytree(path_1_, path_2_, dirs_exist_ok=True)             
        elif previous_element in self.dirs1:
            path_1_ = f"{self.path_1}/vs - russian"
            path_2_ = f"{self.path_2}/{previous_element}/localisation"
            shutil.copytree(path_1_, path_2_, dirs_exist_ok=True)
        elif os.path.isfile(self.path_1):
            path_2_ = self.perebor_pyti(self.path_1)            
            try:          
                shutil.copy(self.path_1, path_2_)
            except FileNotFoundError:
                self.vozvrat_signal("Не удаётся обновить файл.\nПереместите сначала всю сборку или мод для того чтобы создать все папки!")
                return                 
        elif prov1 in ['russian', 'random_names', 'replace']:
            path_2_ = self.perebor_pyti(self.path_1)            
            shutil.copytree(self.path_1, path_2_, dirs_exist_ok=True)             
        self.vozvrat_signal("False")
    
    def start3(self):
        path_1_name_lokal = f"{self.path_1}/vs - {self.lokal} - rezerv"
        path_1_name_lokal_ru = f"{self.path_1}/vs - russian"
    
        for root, dirs, files in os.walk(self.path_2_local):                               
            # Проверка, является ли текущая папка одной из папок для копирования              
            if os.path.basename(root) in self.folders_to_copy:                  
                # Полный путь к папке в целевом каталоге
                dest_folder = os.path.join(path_1_name_lokal, os.path.relpath(root, self.path_2_local))# Получение относительного пути папки относительно исходного каталога
                dest_folder_ru = os.path.join(path_1_name_lokal_ru, os.path.relpath(root, self.path_2_local))                
                # Создание папки в целевом каталоге, если она не существует
                os.makedirs(dest_folder, exist_ok=True)  
                dest_folder_ru = dest_folder_ru.replace(self.lokal, "russian")
                os.makedirs(dest_folder_ru, exist_ok=True)               
                # Копирование файлов в папку назначения
                for file in files:                                                           
                    if self.check_filename(file): #file.endswith(f'{self.lokal}.yml'):                        
                        if self.check_filename_eys(os.path.join(dest_folder, file)):                                 
                            shutil.copy(os.path.join(root, file), os.path.join(dest_folder, file))                  
                        if self.check_filename_eys(os.path.join(dest_folder_ru, file).replace(self.lokal, 'russian')):
                            shutil.copy(os.path.join(root, file), os.path.join(dest_folder_ru, file))                                                    
            
        #$for root, dirs, files in os.walk(self.path_2_local):
            #for file in files:                                   
               # if file.endswith(f'{self.lokal}.yml'):
                    #if self.check_filename_eys(os.path.join(dest_folder, file)):
                    #    shutil.copy(os.path.join(root, file), os.path.join(path_1_name_lokal, file))
                   # if self.check_filename_eys(os.path.join(dest_folder, file).replace(self.lokal, 'russian')):
                     #   path_1_name_lokal_ru = path_1_name_lokal_ru.replace(self.lokal, "russian")
                      #  shutil.copy(os.path.join(root, file), os.path.join(path_1_name_lokal_ru, file))

        if self.lokal != "russian":
            # Переименование папок и файлов
            for root, dirs, files in os.walk(path_1_name_lokal_ru):                                            
                for directory in dirs:
                    if self.lokal in directory:
                        new_name = directory.replace(self.lokal, "russian")
                        try:
                            os.rename(os.path.join(root, directory), os.path.join(root, new_name))
                        except OSError as e:
                            self.vozvrat_signal_statusarr(f"Ошибка при переименовании папки: {e}")
            for root, dirs, files in os.walk(path_1_name_lokal_ru):                
                for filename in files:                    
                    if filename.endswith('.yml'):                        
                        if self.lokal in filename:
                            old_filepath = os.path.join(root, filename)
                            new_filename1 = filename.replace(self.lokal, 'russian')                        
                            new_filepath = os.path.join(root, new_filename1.replace("vs - russian - rezerv", 'vs - russian'))

                            with open(old_filepath, 'r', encoding="utf8") as old_file, open(new_filepath, 'w', encoding="utf8") as new_file:                       
                                new_file.write(old_file.read().replace(f'l_{self.lokal}:', 'l_russian:'))
                                old_file.close()
                                new_file.close() 

                            os.remove(old_filepath)
                                                         
        self.vozvrat_signal("False")

    def perebor_pyti(self, path_1):
        path_2_ = ""
        j = True
        ders2 = ""
        i = 0
        n = ""                 
        while ders2 not in self.dirs1:
            i -= 1
            ders2 = self.path_1.split("/")[i]             
            if ders2 == "vs - russian":
               j = False 
            if j == True:
                n = f"/{ders2}{n}"                  
            if ders2 in self.dirs1:                                            
                path_2_ = f"{self.path_2}/{ders2}/localisation{n}"                
        return path_2_
        
    def clean_directory(self, path):        
        # Получаем все файлы и подпапки в данной директории 
        # Перебираем все файлы и подпапки
        for file in os.listdir(path):           
            # Формируем абсолютный путь к файлу или подпапке
            current_path = os.path.join(path, file)            
            # Если текущий элемент является подпапкой
            if os.path.isdir(current_path):
                # Рекурсивно вызываем эту же функцию для очистки подпапки
                self.clean_directory(current_path)
                # Проверяем, что подпапка стала пуста после очистки
                if os.path.exists(current_path) and os.path.isdir(current_path):
                    if not os.listdir(current_path):
                        # Если она пуста, удаляем ее
                        os.rmdir(current_path)                
        # Проверяем, что текущая директория стала пуста после очистки
        if os.path.exists(path) and os.path.isdir(path):
            if not os.listdir(path):
                # Если она пуста, удаляем ее
                os.rmdir(path)        
            
    def copy_and_rename_directory(self, source_path, destination_path):
        # Копирование каталога
        try:            
            shutil.copytree(source_path, destination_path)
        except shutil.Error as e:
            self.vozvrat_signal(f"Ошибка при копировании каталога: {e}")
            return
        if self.lokal != "russian":
            # Переименование папок и файлов
            for root, dirs, files in os.walk(destination_path):                                            
                for directory in dirs:
                    if self.lokal in directory:
                        new_name = directory.replace(self.lokal, "russian")
                        try:
                            os.rename(os.path.join(root, directory), os.path.join(root, new_name))
                        except OSError as e:
                            self.vozvrat_signal(f"Ошибка при переименовании папки: {e}")
            for root, dirs, files in os.walk(destination_path):                
                for filename in files:                    
                    if filename.endswith('.yml'):                        
                        old_filepath = os.path.join(root, filename)
                        new_filename1 = filename.replace(self.lokal, 'russian')                        
                        new_filepath = os.path.join(root, new_filename1.replace("vs - russian - rezerv", 'vs - russian'))

                        with open(old_filepath, 'r', encoding="utf8") as old_file, open(new_filepath, 'w', encoding="utf8") as new_file:                       
                            new_file.write(old_file.read().replace(f'l_{self.lokal}:', 'l_russian:'))
                            old_file.close()
                            new_file.close() 

                        os.remove(old_filepath)                
    
    def check_filename(self, str_file):
        return self.lokal in str_file and str_file.endswith(".yml")
    
    def check_filename_eys(self, str_file):
        if os.path.exists(str_file):
            return False
        else:
            return True
                
    def vozvrat_signal(self, text):
        self.finishSignal_1.emit(text)
        
    def vozvrat_signal_statusarr(self, text):
        self.finishSignal_2.emit(text)