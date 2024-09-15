import subprocess
import time

start_time = time.time()
# command = "echo 'Welcome to the world of speech synthesis!' | piper --model en_US-lessac-medium --output_file piper.wav"
command = "echo 'Hello, my name is Lucas Coudrais, I am 22 years old, I am a robotics student, and I want to eat burgers in Lyon.' | piper --model en_US-lessac-medium.onnx --output_file piper.wav"
# command = "echo 'Bonjour, je m'appelle Lucas Coudrais, j'ai 22 ans, je suis étudiant en robotique et je veux manger des burgers à Lyon.' | piper --model fr_FR-siwis-low.onnx --output_file piper_fr.wav"

# Exécutez la commande en utilisant subprocess
subprocess.run(command, shell=True)

end_time = time.time()
execution_time = end_time - start_time
print(f"Temps exécution {execution_time} secondes")