import torch
from TTS.api import TTS
import time

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS
tts = TTS("tts_models/en/ljspeech/speedy-speech").to(device)

start_time = time.time()

# Text to speech to a file
tts.tts_to_file(text="Hello, my name is Lucas Coudrais, I am 22 years old, I am a robotics student, and I want to eat burgers in Lyon.", file_path="coquiTTS.wav")

end_time = time.time()
execution_time = end_time - start_time
print(f"Temps exécution {execution_time} secondes")