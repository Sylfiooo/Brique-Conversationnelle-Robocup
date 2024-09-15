
import ctypes



class STT_Whisper_Cpp_Binder(object):
    
    def __init__(self, nb, argv):

        # Charger la bibliothèque partagée
        self.lib = ctypes.cdll.LoadLibrary('./stt/package_STT/libstream.so')
        self.lib.STT_Whisper_new.argtypes = []
        self.lib.STT_Whisper_new.restype = ctypes.POINTER(ctypes.c_void_p)
        self.obj = self.lib.STT_Whisper_new(nb, (ctypes.c_char_p * len(argv))(*argv))
        
    def run_func(self, nb, argv):
        self.lib.run_func.restype = ctypes.c_char_p
        return self.lib.run_func(self.obj, nb, (ctypes.c_char_p * len(argv))(*argv))
    
    def yes_or_no_func(self, nb, argv):
        self.lib.yes_or_no_func.restype = ctypes.c_int
        return self.lib.yes_or_no_func(self.obj, nb, (ctypes.c_char_p * len(argv))(*argv))
    
    def kill_func(self):
        self.lib.kill_process_func(self.obj)

    def switch_run_true_func(self):
        self.lib.switch_run_true_func(self.obj)