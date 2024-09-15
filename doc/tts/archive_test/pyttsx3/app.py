# pip install pyttsx3

import time
import pyttsx3

engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 110)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

# """VOICE"""
# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language, gender='male'):
    for voice in engine.getProperty('voices'):
        if language == voice.name and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

# for voice in engine.getProperty('voices'):
#     print(voice)

"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
start_time = time.time()
# change_voice(engine, "french", "male")
# engine.save_to_file('Bonjour, je m\'appelle Lucas Coudrais, j\'ai 22 ans, je suis étudiant en robotique et je veux manger des burgers à Lyon.', 'pyttsx3_fr.mp3')
engine.save_to_file('Hello, my name is Lucas Coudrais, I am 22 years old, I am a robotics student, and I want to eat burgers in Lyon.', 'pyttsx3.mp3')
engine.runAndWait()
end_time = time.time()
execution_time = end_time - start_time
print(f"Temps exécution {execution_time} secondes")