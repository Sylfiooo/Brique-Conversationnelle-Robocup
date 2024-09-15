import torch
from TTS.api import TTS

# Get device
if torch.cuda.is_available() :
    device = "cuda"  
    print("On utilise cuda sur le gpu")

else : 
    device = "cpu" 
    print("On utilise sur le cpu")


# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# Text to speech to a file
tts.tts_to_file(text="Hello world, I'm the worst president of the whole history of the USA", speaker_wav="trump-9min.mp3", language="en", file_path="test_clone.wav")
