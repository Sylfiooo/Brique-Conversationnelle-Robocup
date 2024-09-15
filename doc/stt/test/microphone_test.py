import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100 
duration = 60  # seconds
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

sd.wait()  # Wait until recording is finished
write('output_60.wav', fs, myrecording)  # Save as WAV file 
