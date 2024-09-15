# import wave
# from io import BytesIO  # Pour Python 3
# from picotts import PicoTTS

# picotts = PicoTTS()
# wavs = picotts.synth_wav('Hello World!')

# # Utilisez BytesIO pour traiter les données binaires
# wav = wave.open(BytesIO(wavs), 'rb')
# print(wav.getnchannels(), wav.getframerate(), wav.getnframes())


import wave
from io import BytesIO
from picotts import PicoTTS
import time

# Initialisez le synthétiseur TTS
picotts = PicoTTS()

start_time = time.time()

# Synthétisez le texte en audio
picotts.voice = "fr-FR"
wavs = picotts.synth_wav('Bonjour, je m\'appelle Lucas Coudrais, j\'ai 22 ans, je suis étudiant en robotique et je veux manger des burgers à Lyon.')
# wavs = picotts.synth_wav('Voulez vous que j\'aille chercher des bananes dans le frigo de la cuisine ?')
# wavs = picotts.synth_wav('Un arc-en-ciel est un photométéore, un phénomène optique se produisant dans le ciel, visible dans la direction opposée au Soleil quand il brille pendant la pluie. ')
# wavs = picotts.synth_wav('J\'aime aller à la chorale le dimanche après un brunch')
# wavs = picotts.synth_wav('Hello, my name is Lucas Coudrais, I am 22 years old, I am a robotics student, and I want to eat burgers in Lyon.')

# Utilisez BytesIO pour traiter les données binaires
wav_data = BytesIO(wavs)

wav = wave.open(BytesIO(wavs), 'rb')


# Ouvrez le fichier WAV en mode écriture
# with wave.open('pico.wav', 'wb') as wav_file:
with wave.open('pico_fr.wav', 'wb') as wav_file:
    # Configurez les paramètres du fichier WAV en utilisant les mêmes paramètres que le fichier original
    wav_file.setnchannels(wav.getnchannels())  # Nombre de canaux
    wav_file.setsampwidth(wav.getsampwidth())  # Largeur d'échantillon en octets (2 pour 16 bits)
    wav_file.setframerate(wav.getframerate())  # Fréquence d'échantillonnage en Hz
    wav_file.setnframes(wav.getnframes())  # Nombre de frames

    # Écrivez les données audio dans le fichier WAV
    wav_file.writeframes(wav_data.getvalue())

# Fermez le fichier WAV
wav_data.close()

end_time = time.time()
execution_time = end_time - start_time
print(f"Temps exécution {execution_time} secondes")

print(picotts.voices)
print("Fichier audio sauvegardé avec succès.")


