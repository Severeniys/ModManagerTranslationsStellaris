from file_configuration.import_libraries.libraries import *


class GetDialsThread(QObject):
    finishSignal_1 = pyqtSignal(str)
    finishSignal_linesi = pyqtSignal(str)
    finishSignal_filename = pyqtSignal(str)
    finishSignal_error = pyqtSignal(str)
    finishSignal_pytj = pyqtSignal(str)
    
    def __init__(self, text_edit, nova_fail, pytj=None, filename=None, lovie=None):
        super(GetDialsThread, self).__init__()
        self.nova_fail = nova_fail
        self.pytj = pytj
        self.text_talb = text_edit
        self.filename = filename
        self.lovie = lovie        
        
    def start1(self):        
        self.pyti_neispovedimw()
        text_talb = self.text_talb.toPlainText()
        lines = text_talb.split(self.n)            
        self.niti = []        
        for line in lines:
            for x, y in ("\\n\\n\\n", " [-1-] "), \
                        ("\\n\\n", " [-2-] "), \
                        ("\\n", " [-3-] "), \
                        ("[-1-]", " \\n\\n\\n "), \
                        ("[-2-]", " \\n\\n "), \
                        ("[-3-]", " \\n "):                                       
                line = line.replace(x, y)            
            line += self.n                  
            for sers in self.chablon:
                ints = re.findall(sers, line)
                self.niti += ints
        temp = []
        for x in self.niti:
            if x not in temp:
                temp.append(x)
        self.niti = temp
        tait = len(self.niti)
        tait += 1
        tit = list(range(1, tait))
        tit = list(map(str, tit))    
        for ta in tit:
            t = f"[0{ta}]"
            self.iti.append(t)
        faira = dict(zip(self.niti, self.iti))
        with open(self.zamens_sils_c, 'w') as f:
            json.dump(faira, f)
        f.close()
        with open(self.zamens_sils_c) as f:
            temm = json.load(f)
            zamens_sils_c_a = list(temm.items())
        f.close()                                     
        with open(self.zamens) as fif:
            temm = json.load(fif)
            zamens_a = list(temm.items())
        fif.close()        
        for line in lines:
            for x, y in ("\\n\\n\\n", " [-1-] "), \
                        ("\\n\\n", " [-2-] "), \
                        ("\\n", " [-3-] "), \
                        ("[-1-]", " \\n\\n\\n "), \
                        ("[-2-]", " \\n\\n "), \
                        ("[-3-]", " \\n "), \
                        ("$$", "$ $"):                                           
                line = line.replace(x, y)               
            line += self.n
            for x, y in zamens_a:                            
                line = line.replace(x, y)            
            for x, y in zamens_sils_c_a:
                line = line.replace(x, y)
            self.linesi += line                
        
        self.finishSignal_linesi.emit(self.linesi)        
        self.vozvrat_signal()           
    
    def start2(self): 
        self.pyti_neispovedimw()            
        text_talb = self.text_talb.toPlainText()        
        lines = text_talb.split(self.n)         
        for line in lines:
            line += self.n
            for sers in self.chablonh:
                ints = re.findall(sers, line)                
                if ints != ['l_russian:']:                
                    self.niti += ints        
        for x in self.niti:
            if x not in self.temp:
                self.temp.append(x)        
        tait = len(self.temp)
        tait += 1
        tit = list(range(1, tait))
        tit = list(map(str, tit))         
        for ta in tit:
            t = f"[00{ta}]"
            self.iti.append(t)
        faira = dict(zip(self.niti, self.iti))
        with open(self.zamens_sils_v, 'w') as f:
            json.dump(faira, f)
        f.close()
        with open(self.zamens_sils_v) as fif:
            temm = json.load(fif)
            dor = list(temm.items())                    
        f.close()           
        lines = text_talb.split(self.n)        
        for line in lines:
            line += self.n
            intsis = re.findall(self.chablong, line)
            if not intsis:
                self.linesi += line                   
            else:
                intsisi = intsis[0]
                nintir = ''.join(map(str, intsisi))
                for x, y in dor:                            
                    if x == nintir:
                        line = line.replace(x, y)
                        #del dor[0]                       
                self.linesi += line         
        self.finishSignal_linesi.emit(self.linesi)
        self.vozvrat_signal()
        
    def start3(self): 
        self.pyti_neispovedimw()       
        text_talb = self.text_talb.toPlainText()
        text_spisok = text_talb.split(self.n)            
        lines = text_spisok                  
        with open(self.zamens_sils_v) as fif:
            temm = json.load(fif)
            dor1 = list(temm.items())            
        fif.close()
        with open(self.zamens_sils_c) as fif:
            temm = json.load(fif)
            dor2 = list(temm.items())
        fif.close()                       
        with open(self.zamensis) as fif:
            temm = json.load(fif)
            direr = list(temm.items())
        fif.close()        
        for line in lines:
            line += self.n            
            for x, y in dor2:                    
                line = line.replace(y, x)            
            for x, y in direr:                        
                line = line.replace(x, y)
            intsis = re.findall(self.chablonj, line)                    
            if not intsis:
                self.linesi += line            
            else:
                intsisi = intsis[0]
                nintir = ''.join(map(str, intsisi))
                for x, y in dor1:                    
                    if y == nintir:                 
                        line = line.replace(y, f"{x}")
                        del dor1[0]                                                             
                self.linesi += line        
        self.finishSignal_linesi.emit(self.linesi)
        self.vozvrat_signal()
        
    def start4(self):        
        self.pyti_neispovedimw()     
        text_talb = self.text_talb.toPlainText()
        lines = text_talb.split(self.n)        
        with open(self.zamens_sils_s) as fif:
            temm = json.load(fif)
            dor = list(temm.items())            
        fif.close()
        for line in lines:
            line += self.n 
            for x, y in dor:
                line = line.replace(x, y)
            self.linesi += line
        self.finishSignal_linesi.emit(self.linesi)
        self.finishSignal_1.emit(None)       
    
    def start5(self):
        self.pyti_neispovedimw()
        text_talb = self.text_talb.toPlainText()
        lines = text_talb.split(self.n)
        for line in lines:
            line += self.n            
            line = line.replace("#Новая строка", "")
            self.linesi += line
        self.finishSignal_linesi.emit(self.linesi)
        self.finishSignal_1.emit(None) 

    def start6(self): 
        self.pyti_neispovedimw()
        try:
            with open(self.filename, 'r', encoding="utf8") as f:
                self.linesi = f.read()                                
            f.close()            
        except FileNotFoundError:
            self.sigal = f"None"
            self.finishSignal_error.emit(self.sigal)                                     
        name = os.path.basename(self.filename).split('.')[0]        
        self.pytj = f"{self.direktoria1}\{name}.yml" 
        for x, y in ("english", "russian"), \
                    ("braz_por", "russian"), \
                    ("french", "russian"), \
                    ("german", "russian"), \
                    ("japanese", "russian"), \
                    ("korean", "russian"), \
                    ("polish", "russian"), \
                    ("simp_chinese", "russian"), \
                    ("spanish", "russian"):
            self.pytj = self.pytj.replace(x, y)        
        shutil.copy2(self.filename, self.pytj)
        self.finishSignal_filename.emit(self.filename)
        self.finishSignal_linesi.emit(self.linesi)
        self.finishSignal_pytj.emit(self.pytj)
        self.vozvrat_signal()     
    
    def start7(self): 
        self.pyti_neispovedimw()                
        with open(self.zamens_sils_s) as fif:
            temm = json.load(fif)
            dor = list(temm.items())            
        fif.close()        
        liste = len(dor)        
        self.linesi = "{\n"
        for x, y in dor:          
            y = y.replace("\"", "\\\"")
            x = x.replace("\"", "\\\"")            
            if liste - 1 == self.yti:
                oei = f"\t\"{x}\": \"{y}\"\n"
                self.linesi += oei
            else:
                oei = f"\t\"{x}\": \"{y}\",\n"
                self.linesi += oei
                self.yti += 1        
        self.linesi += "}\n"
        self.finishSignal_linesi.emit(self.linesi)
        self.vozvrat_signal()
    
    def start8(self):
        self.pyti_neispovedimw()
        self.linesi = ""     
        faira = self.text_talb.toPlainText()            
        json_object = json.loads(faira)   
        with open(self.zamens_sils_s, 'w', encoding="utf8") as f:
            json.dump(json_object, f)
        f.close()
        self.finishSignal_linesi.emit(self.linesi)        
        self.vozvrat_signal()
    
    def start9(self):
        self.pyti_neispovedimw()  
    
    def start10(self):
        self.pyti_neispovedimw()
        try:
            with open(self.filename, 'r', encoding="utf-8-sig") as f:
                self.linesi = f.read()                                
            f.close()                    
        except FileNotFoundError:
            self.sigal = f"None" 
            self.finishSignal_error.emit(self.sigal) 
        self.finishSignal_linesi.emit(self.linesi)
        self.vozvrat_signal()
        
    def start11(self):
        self.pyti_neispovedimw()
        if self.lovie == "try4":
            name = os.path.basename(self.filename).split('.')[0]        
            filename = self.pytj = f"{self.direktoria1}{name}.yml"            
        if self.lovie == "try5":                   
            filename = self.pytj = self.filename                  
        try:
            with open(filename, 'r', encoding="utf-8-sig") as f:
                self.linesi = f.read()                                                
                                               
        except FileNotFoundError:
            self.sigal = f"None"
            self.finishSignal_error.emit(self.sigal)
        self.finishSignal_filename.emit(self.filename)
        self.finishSignal_linesi.emit(self.linesi)
        self.finishSignal_pytj.emit(self.pytj)
        self.vozvrat_signal()
        
         
    def pyti_neispovedimw(self):
        self.dirs = os.path.abspath(os.curdir)
        katalog = "/katalog/init_l/"
        zamens_sils_c = "/katalog/init_s/zamens_sils_c.json"
        zamens_sils_v = "/katalog/init_s/zamens_sils_v.json"
        zamens_sils_s = "/katalog/init_s/zamens_sils_s.json"
        settings = "/katalog/init_s/settings.json"
        zamensis = "/katalog/init_s/zamensis.json"
        zamens = "/katalog/init_s/zamens.json"
        self.chablon = ["\[\S+\]", "\$\S+\$", "£\S+£", "\['\S+'\]", "'\S+'"]
        self.chablonh = ["\A[ ]{0,}\t{0,}[ ]{0,}[^#: ]+:{1}"] #[ 0123456789]
        self.chablong = "\A[ ]{0,}\t{0,}[ ]{0,}[^#: ]+:{1}"
        self.chablonj = "\A\t{0,}[ ]{0,}\[00\d+\]"
        self.iti = []
        self.niti = []
        self.temp = []
        self.linesi = ""
        self.n = "\n"
        self.world = ""
        self.sigal = ""
        self.pytj = ""
        self.yti = 0
        
        self.zamens = self.dirs + zamens
        self.direktoria1 = self.dirs + katalog
        self.zamens_sils_c = self.dirs + zamens_sils_c
        self.zamens_sils_v = self.dirs + zamens_sils_v
        self.zamens_sils_s = self.dirs + zamens_sils_s
        self.settings = self.dirs + settings
        self.zamensis = self.dirs + zamensis
    
            
    def vozvrat_signal(self):         
        if self.nova_fail == True:
            with open(self.pytj, 'w', encoding="utf-8-sig") as file_l:
                file_l.write(self.linesi)
            file_l.close()        
        self.finishSignal_1.emit(self.lovie) 
        
    
    
