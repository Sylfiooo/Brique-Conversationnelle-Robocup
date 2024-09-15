import subprocess
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
import readline

class GoogleTTSPlayer:
    def generate_and_play_tts(self, text, output_file="./test.mp3"):
        gTTS(text, lang='en').save(output_file)

        # Lit le fichier audio généré
        audio = AudioSegment.from_mp3(output_file)
        play(audio)

class PicoTTSPlayer:
    def generate_and_play_tts(self, text, output_file="./test.wav"):
        command = f"pico2wave -w {output_file} -l \"en-US\" \"<pitch level='80'>{text}\""
        
        # Exécute la commande à l'aide de subprocess
        subprocess.run(command, shell=True)

        # Lit le fichier audio généré
        audio = AudioSegment.from_wav(output_file)
        play(audio)

class FallBackTTSManager:
    def __init__(self, pico_tts_player, google_tts_player):
        self.input_history = []
        self.pico_tts_player = pico_tts_player
        self.google_tts_player = google_tts_player

    # Assume you have a method to check WiFi connection
    def check_wifi_connection(self):
        try:
            # Use subprocess to ping a well-known server (Google's public DNS server)
            subprocess.check_output(["ping", "-c", "1", "8.8.8.8"])
            return True
        except subprocess.CalledProcessError:
            return False

    def loop(self):

        self.google_tts_player.generate_and_play_tts("Hello, I'm ready")

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

            # Check WiFi connection and perform TTS accordingly
            if self.check_wifi_connection():
                self.google_tts_player.generate_and_play_tts(text_to_speak)
            else:
                self.pico_tts_player.generate_and_play_tts(text_to_speak)



if __name__ == "__main__":
    pico_tts_player = PicoTTSPlayer()
    google_tts_player = GoogleTTSPlayer()
    fallback_tts_manager = FallBackTTSManager(pico_tts_player, google_tts_player)
    fallback_tts_manager.loop()
