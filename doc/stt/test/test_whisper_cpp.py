# from whisper_cpp_python import Whisper
# from whisper_cpp_python.whisper_cpp import whisper_progress_callback

# import speech_recognition as sr
# import queue
# import sounddevice as sd

# def callback(ctx, state, i, p):
#     print(i)

# class MyClass():

#     q = queue.Queue()
#     recorder = None

#     def __init__(self):
#         model = Whisper('/home/triton_04/Téléchargements/ggml-tiny.bin')
#         #w = Whisper.from_pretrained("tiny.en")
#         model.params.progress_callback = whisper_progress_callback(callback)

#         self.init_recorder()
#         self.start_recorder()
#         self.is_running  = True

#         try :
#             while (self.is_running ):
#                 data = self.q.get()
#                 print(model.transcribe(data))
#                 #pass
#                # print(model.transcribe('./fichier_audio_input/my_english_record.mp3'))
#         except KeyboardInterrupt:
#             self.is_running = False
#             print("\nDone")
            
        

#     def init_recorder(self):
#         self.recorder = sd.RawInputStream(44100,8000,None,1,
#             "int16",None,None,callback=self.callback_sound)
            

#     def start_recorder(self):
#         """Permet de lancer le record (peut être overright)

#         Raises:
#             Exception: Elle se déclanche lorsque le recorder n'a pas été, ou mal initialiser 
#         """
#         try :
#             self.recorder.start()
#         except Exception:
#             raise Exception('init', "Veuillez préalablement initialiser à l'aide de 'init_recorder'")
            

#     def callback_sound(self,indata, frames, time, status):
#         """c'est la callbakc qui s'execute pour chaque bloque audio (peut être overright) """
#         if status:
#             print(status, file=sys.stderr)
#         self.q.put(bytes(indata))
#         #print(bytes(indata))

# MyClass()

# from pywhispercpp.model import Model

# model = Model('base.en', n_threads=6)
# segments = model.transcribe('fichier_audio_input/my_english_record.mp3', speed_up=True)
# for segment in segments:
#     print(segment.text)


# from pywhispercpp.examples.livestream import LiveStream

# url = ""  # Make sure it is a direct stream URL
# ls = LiveStream(url=url, n_threads=4)
# ls.start()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# """
# A simple example showcasing how to use pywhispercpp to transcribe a recording.
# """
# import argparse
# import logging
# import sounddevice as sd
# import pywhispercpp.constants
# from pywhispercpp.model import Model
# import importlib.metadata


# __version__ = importlib.metadata.version('pywhispercpp')

# __header__ = f"""
# ===================================================================
# PyWhisperCpp
# A simple example of transcribing a recording, based on whisper.cpp
# Version: {__version__}               
# ===================================================================
# """


# class Recording:
#     """
#     Recording class

#     Example usage
#     ```python
#     from pywhispercpp.examples.recording import Recording

#     myrec = Recording(5)
#     myrec.start()
#     ```
#     """
#     def __init__(self,
#                  duration: int,
#                  model: str = 'tiny.en',
#                  **model_params):
#         self.duration = duration
#         self.sample_rate = pywhispercpp.constants.WHISPER_SAMPLE_RATE
#         self.channels = 1
#         self.pwcpp_model = Model(model, print_realtime=True, **model_params)

#     def start(self):
#         myarray = []
#         logging.info(f"Start recording for {self.duration}s ...")
#         recording = sd.rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=self.channels)
#         sd.wait()
#         logging.info('Duration finished')
#         res = self.pwcpp_model.transcribe(recording)
#         print(recording[0])
#         self.pwcpp_model.print_timings()

#         myrecording = sd.playrec(myarray, self.sample_rate, channels=2)
#         sd.default.samplerate = self.sample_rate
#         sd.default.channels = 2
#         while (True):
            
#             myrecording = sd.playrec(myarray)


# def _main():
#     print(__header__)
#     parser = argparse.ArgumentParser(description="", allow_abbrev=True)
#     # Positional args
#     parser.add_argument('duration', type=int, help=f"duration in seconds")
#     parser.add_argument('-m', '--model', default='tiny.en', type=str, help="Whisper.cpp model, default to %(default)s")

#     args = parser.parse_args()

#     myrec = Recording(duration=args.duration, model=args.model)
#     myrec.start()


# if __name__ == '__main__':
#     _main()






import sounddevice as sd
import numpy as np
# device_info = sd.query_devices(10, 'input')
# samplerate = int(device_info['default_samplerate'])
# sd.default.samplerate = samplerate
# sd.default.channels = 2
# devices = sd.query_devices()
# print(devices)
# def callback(indata, frames, time, status):
#     #print(indata)
#     sd.play(indata, device=13, blocking=True)
# with sd.InputStream(device = 10, samplerate=44100, dtype='float32', callback=callback):
#     print('#' * 80)
#     print('press Return to quit')
#     print('#' * 80)
#     input()

data = np.array([])

def callback(indata, frames, time, status):
    data = np.array([])
    #outdata[:] = indata
    #print("je suis la")
    print(indata[0])
    buff = data
    data = np.append(buff,indata)
    sd.play(data)
    myrecording = sd.playrec(data, 44100, channels=2)

# with sd.RawStream(channels=2, dtype='int24', callback=callback):
#     sd.sleep(int(4 * 1000))

stream = sd.InputStream(channels=2, dtype='float32', callback=callback,
                            samplerate=44100, blocksize=262144)
stream.start()
while True :
    pass