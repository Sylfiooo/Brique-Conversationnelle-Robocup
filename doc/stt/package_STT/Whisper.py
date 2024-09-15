
import queue
import sounddevice as sd
import json
import os
import time
from datetime import datetime, timedelta
import numpy as np
import whisper
import torch
import speech_recognition as sr

from playsound import playsound

#from STT import STT
from STT.package_STT.STT import STT





class Whisper(STT):
    """Permet de faire une IA qui permet de faire un speech to text à partir d'une entrée sortie
    """

    model = None
    q = queue.Queue()
    compteur = 0
    recognizer = None
    recorder = None
    run_bool = True
    time_start = 0
    transcription = ['']
    phrase_time = None

    def load_model_local(self, path_model:str, samplerate:float = 44100.0):
        """Permet de load un modèle préentrainer depuis sa machine local : https://alphacephei.com/vosk/models 

        Args:
            model_name (str): Le path du modèle que l'on souhaite utiliser
            samplerate (float, optional): La fréquence de l'audio. Defaults to 44100.0.
        """
        # self.STT_playsound("./STT/test/fichier_audio_input/sound.mp3")
        # if (os.path.isdir(path_model)):
        #     self.model = Model(path_model)
        # else :
        #     raise Exception('folder', 'folder doesn\'t exist')

        # self.recognizer = KaldiRecognizer(self.model, samplerate)
        # self.samplerate = samplerate

    def load_model_online(self, model_name:str):
        """permet de crée un modèle à partir d'un modèle préentrainer en ligne (connection requise)

        Args:
            model_name (str): Le nom du modèle que l'on souhaite utiliser en-us, fr, nl;
        """
        self.recognizer = whisper.load_model(model_name+".en").to("cpu")
        # self.recognizer = KaldiRecognizer(self.model, self.samplerate)

    def run_STT(self):
        """Permet de lancer le speech to text
        """
        #try :
            #self.start_recorder()
        #self.start_recorder()

        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)
        self.text = ""
        while self.is_running:
                try:
                    now = datetime.utcnow()
                    # Pull raw recorded audio from the queue.
                    if not self.q.empty():
                            phrase_complete = False
                            # If enough time has passed between recordings, consider the phrase complete.
                            # Clear the current working audio buffer to start over with the new data.
                            if self.phrase_time and now - self.phrase_time > timedelta(seconds=3):
                                phrase_complete = True
                            # This ifrom datetime import datetime, timedeltas the last time we received new audio data from the queue.
                            self.phrase_time = now
                            
                            # Combine audio data from queue
                            #audio_data = self.q.get()
                            audio_data = b''.join(self.q.queue)
                            self.q.queue.clear()
                            
                            # Convert in-ram buffer to something the model can use directly without needing a temp file.
                            # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
                            # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                            # Read the transcription.
                            result = self.recognizer.transcribe(audio_np, fp16=torch.cuda.is_available())
                            text = result['text'].strip()

                            # If we detected a pause between recordings, add a new item to our transcription.
                            # Otherwise edit the existing one.
                            #if phrase_complete:
                            #    self.transcription.append(text)
                            #else:
                            self.transcription[-1] = text

                            # Clear the console to reprint the updated transcription.
                            #os.system('cls' if os.name=='nt' else 'clear')
                            for line in self.transcription:
                                
                                line = line.lower()
                                print(line)
                                 
                                if (not(self.rec_data)  and self.is_activate_word(line)):
                                    self.rec_data = True
                                    self.STT_playsound("./STT/test/fichier_audio_input/sound.mp3")
                                if self.rec_data:
                                    self.text += " " + line
                                if (self.rec_data and ("stop" in line or "kill" in line)):
                                    self.STT_playsound("./STT/test/fichier_audio_input/sound_2.mp3")
                                    self.rec_data = False

                                    self.traitement_final_text()
                                    
                                    # print("#"*80)
                                    # print(self.text)
                                    # print('#'*80)
                                    self.is_running = False
                                    return self.text


                            # Flush stdout.
                            print('', end='', flush=True)

                            # Infinite loops are bad for processors, must sleep.
                            time.sleep(0.25)

                except KeyboardInterrupt:
                    self.is_running = False
                    print("\nDone")
            
    def init_recorder(self):
        record_timeout = 4
        recorder = sr.Recognizer()
        recorder.energy_threshold = 2000
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
        recorder.dynamic_energy_threshold = True
        source = sr.Microphone(sample_rate=16000)
        with source :
            recorder.adjust_for_ambient_noise(source)
        recorder.listen_in_background(source, self.callback, phrase_time_limit=record_timeout)
            

    def start_recorder(self):
        """Permet de lancer le record (peut être overright)

        Raises:
            Exception: Elle se déclanche lorsque le recorder n'a pas été, ou mal initialiser 
        """
        try :
            self.recorder.start()
        except Exception:
            raise Exception('init', "Veuillez préalablement initialiser à l'aide de 'init_recorder'")
            

    def callback(self,_, audio:sr.AudioData) -> None:
        """
        Threaded callback function to receive audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        self.q.put(data)


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
            self.STT_playsound("./STT/test/fichier_audio_input/sound_2.mp3")
            self.text += " "+ json.loads(partial_sentence)['partial']
            #self.recognizer = ""
            self.traitement_final_text()
            print(self.text)
            self.recognizer = KaldiRecognizer(self.model, self.samplerate)

    def detect_void (self, partial_sentence:str):
        if (len(json.loads(partial_sentence)['partial']) == 0 
            and self.rec_data
            and time.time() - self.time_start > 1.5):
                self.compteur += 1   
        else :
            self.compteur = 0

    def traitement_final_text(self):
        self.text = self.text.lower()
        self.text = self.text.replace("."," ")
        self.text = self.text.replace("'"," ")
        self.text = self.text.replace(","," ")
        self.text = self.text.replace("!"," ")
        self.text = self.text.replace("?"," ")
        index_min = float('inf')
        taille_mot = 0
        for mot in self.mot_declancheur:
            if (mot in self.text):
                index_min = min(self.text.index(mot),index_min)
                if index_min == self.text.index(mot):
                    taille_mot = len(mot)
                
        if (index_min+taille_mot >= 0 ):
            self.text = self.text[index_min+taille_mot:]
        if "kill" in self.text:
            self.text = self.text[:self.text.index("kill")]

if __name__ == '__main__':
    vosk = Vosk()
    vosk.load_model_online("en-us")
    #vosk.load_model_local("./STT/modele/modele_vosk/vosk-model-small-fr-0.22")
    #vosk.load_model_local("/tmp/vosk-model-en-us-0.22")
    vosk.init_recorder(44100,8000,None,1,vosk.callback)
    vosk.run_TTS()