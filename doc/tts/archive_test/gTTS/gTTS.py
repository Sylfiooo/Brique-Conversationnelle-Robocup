# pip install gTTS
from gtts import gTTS
import time

start_time = time.time()
tts = gTTS('Bonjour, je m\'appelle Lucas Coudrais, j\'ai 22 ans, je suis étudiant en robotique et je veux manger des burgers à Lyon.', lang='fr')
# tts = gTTS('Hello, my name is Lucas Coudrais, I am 22 years old, I am a robotics student, and I want to eat burgers in Lyon.', lang='en')
tts.save('gTTS_fr.mp3')
# tts.save('gTTS.mp3')
end_time = time.time()
execution_time = end_time - start_time
print(f"Temps exécution {execution_time} secondes")
