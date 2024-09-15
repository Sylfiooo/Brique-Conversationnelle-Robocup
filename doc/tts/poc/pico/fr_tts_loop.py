import subprocess
from pydub import AudioSegment
from pydub.playback import play
import readline

class TTSPlayer:
    def __init__(self):
        self.input_history = []

    def generate_and_play_tts(self, text, output_file="./test_fr.wav"):
        command = f"pico2wave -w {output_file} -l \"fr-FR\" \"<pitch level='80'>{text}\""
        # Exécute la commande à l'aide de subprocess
        subprocess.run(command, shell=True)

        # Lit le fichier audio généré
        audio = AudioSegment.from_wav(output_file)
        play(audio)

    def loop(self):
        # Boucle d'entrée continue
        while True:
            # Utilise readline pour obtenir une entrée de l'utilisateur avec historique
            text_to_speak = input("Entrez le texte que vous voulez que le programme dise (ou tapez 'exit' pour quitter) : ")

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