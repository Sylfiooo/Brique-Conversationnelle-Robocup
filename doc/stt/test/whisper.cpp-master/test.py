# from ctypes import cdll, c_int, POINTER, c_char_p
# lib = cdll.LoadLibrary('./libstream.so')

# #print(lib.to_timestamp_func(1629884345))

# lib.run_func.argtypes = [c_int, POINTER(c_char_p)] # (all defined by ctypes)

# args = [c_char_p(b"stream"), c_char_p(b"-m"), c_char_p("/home/triton_04/Téléchargements/ggml-base.en.bin".encode('utf-8')), None]

# # Call main_func with the arguments
# print((c_int)(len(args)))
# lib.run_func(len(args) , (c_char_p * len(args))(*args[:]))




# """foo.py - a simple demo of importing a calss from C++"""
# from ctypes import cdll, c_int, POINTER, c_char_p

# lib = ctypes.cdll.LoadLibrary('./libstream.so')

# import ctypes
# #from ctypes import cdll, c_int, POINTER, c_char_p
# lib = ctypes.cdll.LoadLibrary('./libstream.so')
# args = [ctypes.c_char_p(b"stream"), ctypes.c_char_p(b"-m"), ctypes.c_char_p("/home/triton_04/Téléchargements/ggml-base.en.bin".encode('utf-8')), None]


# class STT_Whisper(object):
#     """The Foo class supports two methods, bar, and foobar..."""
#     def __init__(self):
#         lib.STT_Whisper_new.argtypes = []
#         lib.STT_Whisper_new.restype = ctypes.c_void_p

#         lib.run_func.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
#         lib.run_func.restype = ctypes.c_char_p


#         self.obj = lib.STT_Whisper_new()


#     def run_func(self, nb, argv):
#         """bar returns a string continaing the value"""
#         lib.run_func(nb,argv)

# stt = STT_Whisper()
# stt.run_func(1,(ctypes.c_char_p * len(args))(*args[:]))






import ctypes

# Charger la bibliothèque partagée
lib = ctypes.cdll.LoadLibrary('./libstream.so')

# Définir les types d'arguments et le type de retour de la fonction run_func
lib.STT_Whisper_new.argtypes = []


#lib.run_func.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
lib.run_func.restype = ctypes.c_char_p

class STT_Whisper(object):
    def __init__(self, nb, argv):
        lib.STT_Whisper_new.restype = ctypes.POINTER(ctypes.c_void_p)
        self.obj = lib.STT_Whisper_new(nb, (ctypes.c_char_p * len(argv))(*argv))
        lib.run_func.restype = ctypes.c_char_p
        lib.yes_or_no_func.restype = ctypes.c_int

    def run_func(self, nb, argv):
        return lib.run_func(self.obj, nb, (ctypes.c_char_p * len(argv))(*argv))
    
    def yes_or_no_func (self, nb, argv):
        return lib.yes_or_no_func(self.obj, nb, (ctypes.c_char_p * len(argv))(*argv))

# Liste des arguments
args = [ctypes.c_char_p(b"stream"), ctypes.c_char_p(b"-m"), ctypes.c_char_p("/tmp/ggml-base.en.bin".encode('utf-8')), 
                                    ctypes.c_char_p(b"-l"), ctypes.c_char_p(b"en"), 
                                    ctypes.c_char_p(b"-t"), ctypes.c_char_p(b"6"),
                                    ctypes.c_char_p(b"-vth"), ctypes.c_char_p(b"0.7"), 
                                    ctypes.c_char_p(b"-f"), ctypes.c_char_p(b"test.txt"),
                                    None]

# Créer une instance de la classe STT_Whisper
stt = STT_Whisper(len(args) - 1, args[:-1]) 
result = stt.yes_or_no_func(len(args) - 1, args[:-1])  # Exclure le dernier élément de la liste (None)

print("--------- res 1")
print(result)
result = stt.yes_or_no_func(len(args) - 1, args[:-1]) 

print("--------- res 2")
print(result)
# Appeler la fonction run_func avec les arguments
#result = stt.run_func(len(args) - 1, args[:-1])  # Exclure le dernier élément de la liste (None)

# Afficher le résultat
#print(result.decode('utf-8', errors='replace'))

# valeurFinal = result.decode('utf-8').replace("."," ")
# valeurFinal = valeurFinal.replace("?"," ")
# valeurFinal = valeurFinal.replace(","," ")
# valeurFinal = valeurFinal.replace("!"," ")
# valeurFinal = valeurFinal.replace(";"," ")
# valeurFinal = valeurFinal.replace("."," ")
# valeurFinal = valeurFinal.lower()

# if ("okay" in valeurFinal):
#     valeurFinal = valeurFinal.replace("okay","")
# elif ("okey" in valeurFinal):
#     valeurFinal = valeurFinal.replace("okey","")
# elif ("ok" in valeurFinal):
#     valeurFinal = valeurFinal.replace("ok","")


#print(result)