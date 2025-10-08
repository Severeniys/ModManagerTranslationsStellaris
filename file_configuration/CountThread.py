from file_configuration.import_libraries.libraries import *

class CountThread_1(QObject):    
    finishSignal_1l = pyqtSignal(int, int)
    def __init__(self, text):
        super(CountThread_1, self).__init__()
        self.text = text
        
    def start1(self):        
        word_count = len(self.text.split())
        char_count = len(self.text)        
        self.finishSignal_1l.emit(word_count, char_count)
        
        
        
class CountThread_2(QObject):    
    finishSignal_1l = pyqtSignal(dict)
    def __init__(self, text, word_list):
        super(CountThread_2, self).__init__()
        self.text = text
        self.word_list = word_list
        
    def start1(self):        
        
        lines = self.text.split("\n")

        color_dict = {}

        for index, line in enumerate(lines):  
            tre = re.findall("\A[ ]{0,}\t{0,}[ ]{0,}[^#: ]+:{1}", line)  
            if tre:
                tre[0]        
            if tre in self.word_list:
                color_dict[index + 1] = "red"               
            else:
                color_dict[index + 1] = "green"
        self.finishSignal_1l.emit(color_dict)