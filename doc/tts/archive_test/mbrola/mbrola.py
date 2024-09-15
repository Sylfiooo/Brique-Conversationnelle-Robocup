from voxpopuli import Voice
import time

start_time = time.time()

# voice = Voice(lang="us", pitch=50, speed=140, voice_id=2)
# wav = voice.to_audio("Hello, my name is Lucas Coudrais, I am 22 years old, I am a robotics student, and I want to eat burgers in Lyon.", "mbrola.wav")

# voice = Voice(lang="fr", pitch=50, speed=100, voice_id=3)
# wav = voice.to_audio("Bonjour, je m'appelle Lucas Coudrais, j'ai 22 ans, je suis étudiant en robotique et je veux manger des burgers à Lyon.", "mbrola_fr.wav")


voice = Voice(lang="fr", pitch=50, speed=100, voice_id=3)
wav = voice.to_audio("Voulez vous que j'aille chercher des bananes dans le frigo de la cuisine ?", "mbrola_question.wav")




end_time = time.time()
execution_time = end_time - start_time
print(f"Temps exécution {execution_time} secondes")