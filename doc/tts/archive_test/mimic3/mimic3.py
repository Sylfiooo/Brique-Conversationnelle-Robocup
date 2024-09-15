import subprocess
import time

start_time = time.time()
# command = "mimic3 --voice en_UK/apope_low \"Hello, my name is Lucas Coudrais, I am 22 years old, I am a robotics student, and I want to eat burgers in Lyon.\" > mimic3.wav"
command = "mimic3 --voice fr_FR/tom_low \"Bonjour, je m'appelle Lucas Coudrais, j'ai 22 ans, je suis étudiant en robotique et je veux manger des burgers à Lyon.\" > mimic3_fr.wav"

# Exécutez la commande en utilisant subprocess
subprocess.run(command, shell=True)

end_time = time.time()
execution_time = end_time - start_time
print(f"Temps exécution {execution_time} secondes")