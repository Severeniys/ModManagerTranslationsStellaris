from file_configuration.import_libraries.libraries import *

class GetDialsThreadComparison(QObject):
    finishSignal_1 = pyqtSignal(str, str, list)
    finishSignal_error = pyqtSignal(str)    
    def __init__(self, filename_1_, filename_2_):
        super(GetDialsThreadComparison, self).__init__()        
        self.filename_1_ = filename_1_
        self.filename_2_ = filename_2_  
        
        
    def start1(self):
        if self.filename_1_ == "":            
            self.vozvrat_signal("None")
            return
        if self.filename_2_ == "":            
            self.vozvrat_signal("None")
            return
        lenn_text = ""       
        linesr = ""
        linestel = ""
        lines1, lines2 = [], []
        self.chablong = "\A[ ]{0,}\t{0,}[ ]{0,}[^#: ]+:{1}"
        self.chablong_text = "\S+:{1}"        
        try:
            with open(self.filename_2_, encoding="utf-8-sig") as file_l1:
                lines1_ = file_l1.readlines()
            
            with open(self.filename_1_, encoding="utf-8-sig") as file_l2:
                lines2_ = file_l2.readlines()
        except FileNotFoundError as e:
            self.dialog = f"Файл не найден: {e}"
            self.finishSignal_error.emit(self.dialog)           
            return
        
        except (IOError, OSError) as e:
            self.dialog = f"Ошибка при открытии или чтении файла: {e}"
            self.finishSignal_error.emit(self.dialog) 
            return

        except Exception as e: # На случай других непредвиденных ошибок при чтении
            self.dialog = f"Произошла непредвиденная ошибка при работе с файлами: {e}"
            self.finishSignal_error.emit(self.dialog) 
            return
        
        for linestel in lines2_:
            intsisp = re.findall(self.chablong, linestel)
            if intsisp != []:
                lines2.append(linestel)              
        for linesl in lines1_:     
            intsis_ = ''               
            i = 0                        
            lenn_text += "\n"   
            bools, intsis_1 = self.chablong_text_if_bool(linesl)                      
            if self.english_nait_english(linesl):                                        
                linesr += "l_russian:\n"                        
                continue                       
            elif self.is_blank(linesl):
                linesr += "\n"
                continue                      
            elif self.start_with_hash(linesl):
                linesr += f"{linesl}"                          
                continue       
            elif bools:                                                
                if intsis_1 == []:
                        continue                         
                intsis_1_ = intsis_1[0]                  
                for line1 in lines2:                    
                    intsis = re.findall(self.chablong, line1)
                    if intsis != []:
                        intsis_ = intsis[0]
                    intsis = re.findall(self.chablong_text, intsis_)                    
                    if intsis == []:
                        continue                                                   
                    intsis_ = intsis[0]                                                  
                    if intsis_1_ == intsis_:                                                
                        linesr += line1                        
                        line1 = ''
                        i = 1                        
                        break
                if  i != 1:
                    linesll = linesl.replace('\n', ' #Новая строка\n')
                    linesr += linesll
                    spisok = re.findall("[^#: ]+:{1}", linesl)
                    lines1 += spisok                                     
        self.listOfChangedKeys = lines1
        self.dirs = os.path.abspath(os.curdir)
        #name = os.path.basename(self.filename_1_).split('.')[0]        
        #self.pytj = f"{self.dirs}/katalog/init_l/{name}.yml"                
        with open(self.filename_1_, 'w', encoding="utf-8-sig") as file_l:
            file_l.write(linesr)        
        self.vozvrat_signal()                       
    
       
    def chablong_text_if_bool(self, s):
        intsis_1 = re.findall(self.chablong, s)
        if intsis_1 != []:
            intsis__ = intsis_1[0]
        else:    
            return False, None
        intsis_1 = re.findall(self.chablong_text, intsis__)
        if intsis_1 != []:
            return True, intsis_1
        return False, None
        
    def is_blank(self, s):
        return not s.strip()
    
    def start_with_hash(self, s):
        if s.strip().startswith("#"):
            return True
        else:
            return False  
       
    def english_nait_english(self, s):
        english_nait = re.findall("l_english:", s)
        if "l_english:" in english_nait:
            return True
        return False
    
    def vozvrat_signal(self, stre=None):                
        self.finishSignal_1.emit(self.filename_1_, stre, self.listOfChangedKeys) 