import queue
import sys
import sounddevice as sd
import json
import os
import time
from vosk import Model, KaldiRecognizer, SpkModel
from playsound import playsound

from STT.package_STT.STT import STT
#from STT import STT


class Vosk(STT):
    """Permet de faire une IA qui permet de faire un speech to text à partir d'une entrée sortie
    """

    model = None
    q = queue.Queue()
    rec_data = False
    compteur = 0
    recognizer = None
    recorder = None
    time_start = 0

    def load_model_local(self, path_model:str, samplerate:float = 44100.0):
        """Permet de load un modèle préentrainer depuis sa machine local : https://alphacephei.com/vosk/models 

        Args:
            model_name (str): Le path du modèle que l'on souhaite utiliser
            samplerate (float, optional): La fréquence de l'audio. Defaults to 44100.0.
        """
        #self.STT_playsound("./STT/test/fichier_audio_input/sound.mp3")
        if (os.path.isdir(path_model)):
            self.model = Model(path_model)
        else :
            raise Exception('folder', 'folder doesn\'t exist')

        self.recognizer = KaldiRecognizer(self.model, samplerate)
        self.recognizer.SetNLSML(True)
        self.recognizer.SetWords(True)
        #self.recognizer.SetPartialWords(True)
        #self.recognizer.SetMaxAlternatives(1)
        self.samplerate = samplerate

    def load_model_online(self, model_name:str, samplerate:float = 44100.0):
        """permet de crée un modèle à partir d'un modèle préentrainer en ligne (connection requise)

        Args:
            model_name (str): Le nom du modèle que l'on souhaite utiliser en-us, fr, nl;
            samplerate (float, optional): La fréquence de l'audio. Defaults to 44100.0.
        """
        self.model = Model(lang=model_name)
        self.recognizer = KaldiRecognizer(self.model,44100.0)
        self.samplerate = 44100.0
        self.recognizer.SetNLSML(True)
        self.recognizer.SetWords(True)

    def run_STT(self, with_return : bool):
        """Permet de lancer le speech to text

        Args:
            with_return (bool): Permet de définir s'il l'on souhaite une boucle infinie
            ou un retour du text (unique)

        Returns:
            str : Le message enregistrer entre un "OK" et un "Stop" (ou un vide)
        """
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)
        self.STT_playsound("./STT/sounds/sound_3.wav")
        self.is_return = with_return
        while self.is_running: #Tant que l'execution est en cours
            try :
                data = self.q.get() #On défile un élément de la queue
                print(data)
                if self.recognizer.AcceptWaveform(data): #Si la donnée enregistrer est valide
                    if self.rec_data:
                        self.text += " " +  json.loads(self.recognizer.Result())['text']
                    #print(self.recognizer.Result())
                else: #Si non on a juste une donnée partiel
                    print(self.recognizer.PartialResult())
                    #Si un mot d'activation est entendu et qu'on est pas entrain d'enregistrer
                    if (not(self.rec_data) and self.is_activate_word (self.recognizer.PartialResult())):
                        self.STT_playsound("./STT/sounds/sound.mp3")
                        self.rec_data = True
                        self.compteur = 0
                        self.time_start = time.time()
                        self.text = ""

                    #s'il il faut enregistrer
                    if self.rec_data :
                        self.detect_void(self.recognizer.PartialResult())#On regarde s'il y a du vide dans l'enregistrement
                        self.detect_fin(self.recognizer.PartialResult())#On detecte si un mot de fin est prononcer

                    
            except KeyboardInterrupt:
                self.is_running = False
                print("\nDone")
        if (self.is_return):
            return self.text
       
            
    def init_recorder(self,callback,samplerate:float=44100.0,blocksize:int=8000,device:str=None,dtype:str="int16",channels:int=1):
        """permet d'initialiser le recorder, peut être overright en cas de changement de micro d'entrée

        Args:
            callback (function): La fonction de call back 
            samplerate (float, optional): La féquence d'enregistrement. Defaults to 44100.
            blocksize (int, optional): La taille des block d'enregistrement. Defaults to 8000.
            device (str, optional): Le type de périphérique utiliser. Defaults to None.
            dtype (str, optional): _description_. Defaults to "int16".
            channels (int, optional): Le nombre de canal utiliser pour l'enregistrement. Defaults to 1.
        """
        self.recorder = sd.RawInputStream(44100,8000,None,1,
            "int16",None,None,callback=self.callback)

    def start_recorder(self):
        """Permet de lancer le record (peut être overright)

        Raises:
            Exception: Elle se déclanche lorsque le recorder n'a pas été, ou mal initialiser 
        """
        try :
            self.recorder.start()
        except Exception:
            raise Exception('init', "Veuillez préalablement initialiser à l'aide de 'init_recorder'")
            


    def callback(self,indata, frames, time, status):
        """c'est la callbakc qui s'execute pour chaque bloque audio (peut être overright) """
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))


    def is_activate_word (self, partial_sentence:str):
        """Il vérifie si le mot d'activation est dans la sentence

        Args:
            partial_sentence (str): un bloque de la sequence reçu

        Returns:
            bool : return "tru" si un mot d'activation est dans la sentance (false si non)
        """
        mot_trouver = False
        index_mot_declancheur = 0
        while not(mot_trouver) and index_mot_declancheur < len(self.mot_declancheur):
            if (self.mot_declancheur[index_mot_declancheur] in partial_sentence):
                mot_trouver = True
            index_mot_declancheur+=1
        return mot_trouver

    def detect_fin (self, partial_sentence:str):
        """permet de detecter la fin de la sequence que l'on enregistre
        (une sequence commencer par un mot d'activation et un mot de fin ou un vide)

        Args:
            partial_sentence (str): _description_
        """
        if (self.compteur > 3 or "stop" in partial_sentence ) and self.rec_data:
            self.rec_data = False
            self.compteur == 0
            self.STT_playsound("./STT/sounds/sound_2.mp3")
            self.text += " "+ json.loads(partial_sentence)['partial']
            #self.recognizer = ""
            self.traitement_final_text()
            print(self.text)
            self.recognizer = KaldiRecognizer(self.model, self.samplerate)
            if self.is_return :
                self.is_running = False

    def detect_void (self, partial_sentence:str):
        """ermet de dtecter si la sequence en cours est vide (s'il y a un blanc)

        Args:
            partial_sentence (str): La séquence en cours d'enregistrement
        """
        if (len(json.loads(partial_sentence)['partial']) == 0 
            and self.rec_data
            and time.time() - self.time_start > 1.5):
                self.compteur += 1   
        else :
            self.compteur = 0

    def traitement_final_text(self):
        """Permet de formatter et de supprimer les mots de début et de fin
        """
        index_min = float('inf')
        taille_mot = 0
        for mot in self.mot_declancheur:
            if (mot in self.text):
                index_min = min(self.text.index(mot),index_min)
                if index_min == self.text.index(mot):
                    taille_mot = len(mot)
                
        if (index_min >= 0 and index_min+taille_mot < len(self.text)):
            self.text = self.text[index_min+taille_mot:]
        if "stop" in self.text:
            self.text = self.text[:self.text.index("stop")]

    def reset_data(self):
        self.is_running = True
        self.text = ""
        self.compteur = 0