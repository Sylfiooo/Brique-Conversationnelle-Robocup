import torch
from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play
import readline

class TTSPlayer:
    def __init__(self):
        self.input_history = []
        
        self.tts = TTS("tts_models/multilingual/multi-dataset/your_tts")

    def generate_and_play_tts(self, text, output_file="./test_clone.wav"):
        self.tts.tts_to_file(text=text, speaker_wav="trump-9min.wav", language="en", file_path=output_file)

        # Lit le fichier audio généré
        audio = AudioSegment.from_wav(output_file)
        play(audio)

    def loop(self):
        # première initiation artificielle, celle ci prenant parfois pas mal de temps au début
        self.generate_and_play_tts("Hello, I'm ready")

        # Boucle d'entrée continue
        while True:
            # Utilise readline pour obtenir une entrée de l'utilisateur avec historique
            text_to_speak = input("Enter the text you want the program to say (or type 'exit' to quit): ")

            if text_to_speak.lower() == 'exit':
                print("Program terminated.")
                break

            if text_to_speak.strip():  # Vérifie si l'entrée n'est pas vide
                self.input_history.append(text_to_speak)  # Ajoute l'entrée à l'historique

            # Utilise l'index -1 pour obtenir la dernière entrée de l'historique
            if self.input_history:
                last_input = self.input_history[-1]
                print("Previous input:", last_input)

            self.generate_and_play_tts(text_to_speak)

if __name__ == "__main__":
    tts_player = TTSPlayer()
    tts_player.loop()
