from playsound import playsound
from abc import ABC, abstractmethod

class STT(ABC):


    text = ""
    mot_declancheur = ["ok","okay","okey"]
    mot_fin = ["stop","fin"]
    is_running = True
    is_return = False
    rec_data = False
    samplerate = 0

    def get_text(self):
        return self.text

    def set_mots_declancheur(self, mots_declancheur):
        self.mots_declancheur = mots_declancheur

    def STT_playsound(self,file_play:str):
        playsound(file_play)

    @abstractmethod
    def load_model_local(self, path_model:str):
        pass

    @abstractmethod
    def load_model_online(self, model_name:str):
        pass

    @abstractmethod
    def run_STT(self):
        pass