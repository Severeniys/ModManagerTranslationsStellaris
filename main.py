from file_configuration.import_libraries.libraries import *
from file_configuration.ModManagerTranslationsStellaris import *
#from file_configuration.ModManagerTranslationsStellaris import *

def application():       
    qdarktheme.enable_hi_dpi()    
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create("Windows"))       
    MMTS = ModManagerTranslationsStellaris()              
    MMTS.show()
    translator = QTranslator(app)
    locale = QLocale.system().name()
    path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    translator.load('qt_%s' % locale, path)
    app.installTranslator(translator)
    sys.exit(app.exec())
    
if __name__ == "__main__":        
    application()
    
    