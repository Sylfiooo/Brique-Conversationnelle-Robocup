#from STT_Whisper_Cpp_Binder import *
from STT_Whisper_Cpp_Binder import *
import ctypes


class STT_Whisper_cpp :
    # Liste des arguments

    def __init__ (self):
        self.args = [ctypes.c_char_p(b"stream"), ctypes.c_char_p(b"-m"), ctypes.c_char_p("../ggml-base.en.bin".encode('utf-8')), 
                                        ctypes.c_char_p(b"-l"), ctypes.c_char_p(b"en"), 
                                        ctypes.c_char_p(b"-t"), ctypes.c_char_p(b"6"),
                                        ctypes.c_char_p(b"-vth"), ctypes.c_char_p(b"0.7"), 
                                        ctypes.c_char_p(b"-f"), ctypes.c_char_p(b"test.txt"),
                                        None]

        # Créer une instance de la classe STT_Whisper
        self.stt = STT_Whisper_Cpp_Binder(len(self.args) - 1, self.args[:-1]) 

    def run_STT(self):
        # Appeler la fonction run_func avec les arguments
        result = self.stt.run_func(len(self.args) - 1, self.args[:-1])  # Exclure le dernier élément de la liste (None)

        # Afficher le résultat
        #print(result.decode('utf-8', errors='replace'))

        valeurFinal = result.decode('utf-8').replace("."," ")
        valeurFinal = valeurFinal.replace("?"," ")
        valeurFinal = valeurFinal.replace(","," ")
        valeurFinal = valeurFinal.replace("!"," ")
        valeurFinal = valeurFinal.replace(";"," ")
        valeurFinal = valeurFinal.replace("."," ")
        valeurFinal = valeurFinal.lower()

        if ("okay" in valeurFinal):
            index_min = min(valeurFinal.index("okay"),0)
            valeurFinal = valeurFinal[index_min:]
            valeurFinal = valeurFinal.replace("okay","")
        elif ("okey" in valeurFinal):
            index_min = min(valeurFinal.index("okey"),0)
            valeurFinal = valeurFinal[index_min:]
            valeurFinal = valeurFinal.replace("okey","")
        elif ("ok" in valeurFinal):
            index_min = min(valeurFinal.index("ok"),0)
            valeurFinal = valeurFinal[index_min:]
            valeurFinal = valeurFinal.replace("ok","")

        return valeurFinal
    
    def yes_or_no(self):
        result = self.stt.yes_or_no_func(len(self.args) - 1, self.args[:-1])  # Exclure le dernier élément de la liste (None)
        return result



if __name__ == '__main__':
    mon_test = STT_Whisper_cpp()
    valeur = mon_test.run_STT()
    print(valeur)