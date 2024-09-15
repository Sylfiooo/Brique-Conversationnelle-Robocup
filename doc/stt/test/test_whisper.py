# import whisper
# import warnings
# import time
# import sys

# audio_path = sys.argv[1]
# warnings.simplefilter("ignore")
# device = "cpu"

# # Exemple d'utilisation de Numba pour la boucle principale

# def main(model, probs):


#     # start = time.time()
#     # # load audio and pad/trim it to fit 30 seconds

#     # print(f"Detected language: {max(probs, key=probs.get)}")

#     # # decode the audio
#     # #options = whisper.DecodingOptions()
#     # # str(max(probs, key=probs.get))
#     # result = model.transcribe(audio_path, language=str(max(probs, key=probs.get)), verbose=True)
#     # stop = time.time() - start
#     # # print the recognized text
#     # print(result['text'])
#     # print(stop)


#     start = time.time()
#     # load audio and pad/trim it to fit 30 seconds

#     print(f"Detected language: {max(probs, key=probs.get)}")

#     # decode the audio
#     #options = whisper.DecodingOptions()
#     # str(max(probs, key=probs.get))
#     result = model.transcribe(audio_path, language=str(max(probs, key=probs.get)),  fp16=False, verbose=True, temperature=0.2, compression_ratio_threshold = 5.2, initial_prompt="Pas plus tard la société de Sam Altman le patron d'une startup valorisée")
#     stop = time.time() - start
#     # print the recognized text
#     print(result['text'])
#     print(stop)

# model = whisper.load_model("tiny").to(device)
# audio = whisper.load_audio(audio_path)
# audio = whisper.pad_or_trim(audio)

# # make log-Mel spectrogram and move to the same device as the model
# mel = whisper.log_mel_spectrogram(audio).to(model.device)

# # detect the spoken language
# _, probs = model.detect_language(mel)
# main(model,probs)

#! python3.7

# import argparse
# import os
# import numpy as np
# import speech_recognition as sr
# import whisper
# import torch

# from datetime import datetime, timedelta
# from queue import Queue
# from time import sleep
# from sys import platform


# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--model", default="medium", help="Model to use",
#                         choices=["tiny", "base", "small", "medium", "large"])
#     parser.add_argument("--non_english", action='store_true',
#                         help="Don't use the english model.")
#     parser.add_argument("--energy_threshold", default=1000,
#                         help="Energy level for mic to detect.", type=int)
#     parser.add_argument("--record_timeout", default=2,
#                         help="How real time the recording is in seconds.", type=float)
#     parser.add_argument("--phrase_timeout", default=3,
#                         help="How much empty space between recordings before we "
#                              "consider it a new line in the transcription.", type=float)
#     if 'linux' in platform:
#         parser.add_argument("--default_microphone", default='default',
#                             help="Default microphone name for SpeechRecognition. "
#                                  "Run this with 'list' to view available Microphones.", type=str)
#     args = parser.parse_args()

#     # The last time a recording was retrieved from the queue.
#     phrase_time = None
#     # Thread safe Queue for passing data from the threaded recording callback.
#     data_queue = Queue()
#     # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
#     recorder = sr.Recognizer()
#     recorder.energy_threshold = 1000
#     # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
#     recorder.dynamic_energy_threshold = False

#     # Important for linux users.
#     # Prevents permanent application hang and crash by using the wrong Microphone
#     if 'linux' in platform:
#         mic_name = args.default_microphone
#         print("#"*8)
#         print(mic_name)
#         print("#"*8)
#         if not mic_name or mic_name == 'list':
#             print("Available microphone devices are: ")
#             for index, name in enumerate(sr.Microphone.list_microphone_names()):
#                 print(f"Microphone with name \"{name}\" found")
#             return
#         else:
#             for index, name in enumerate(sr.Microphone.list_microphone_names()):
#                 if mic_name in name:
#                     source = sr.Microphone(sample_rate=16000, device_index=index)
#                     break
#     else:
#         source = sr.Microphone(sample_rate=16000)

#     print("#"*8)
#     print(sr.Microphone.list_microphone_names())
#     print("#"*8)

#     # Load / Download model
#     model = args.model
#     if args.model != "large" and not args.non_english:
#         model = model + ".en"
#     audio_model = whisper.load_model(model).to("cpu")

#     record_timeout = args.record_timeout
#     phrase_timeout = args.phrase_timeout

#     transcription = ['']

#     with source:
#         recorder.adjust_for_ambient_noise(source)

#     def record_callback(_, audio:sr.AudioData) -> None:
#         """
#         Threaded callback function to receive audio data when recordings finish.
#         audio: An AudioData containing the recorded bytes.
#         """
#         # Grab the raw bytes and push it into the thread safe queue.
#         data = audio.get_raw_data()
#         data_queue.put(data)

#     # Create a background thread that will pass us raw audio bytes.
#     # We could do this manually but SpeechRecognizer provides a nice helper.
#     recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

#     # Cue the user that we're ready to go.
#     print("Model loaded.\n")

#     while True:
#         try:
#             now = datetime.utcnow()
#             # Pull raw recorded audio from the queue.
#             if not data_queue.empty():
#                 phrase_complete = False
#                 # If enough time has passed between recordings, consider the phrase complete.
#                 # Clear the current working audio buffer to start over with the new data.
#                 if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
#                     phrase_complete = True
#                 # This is the last time we received new audio data from the queue.
#                 phrase_time = now
                
#                 # Combine audio data from queue
#                 audio_data = b''.join(data_queue.queue)
#                 data_queue.queue.clear()
                
#                 # Convert in-ram buffer to something the model can use directly without needing a temp file.
#                 # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
#                 # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
#                 audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

#                 # Read the transcription.
#                 result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
#                 text = result['text'].strip()

#                 # If we detected a pause between recordings, add a new item to our transcription.
#                 # Otherwise edit the existing one.
#                 if phrase_complete:
#                     transcription.append(text)
#                 else:
#                     transcription[-1] = text

#                 # Clear the console to reprint the updated transcription.
#                 os.system('cls' if os.name=='nt' else 'clear')
#                 for line in transcription:
#                     print(line)
#                 # Flush stdout.
#                 print('', end='', flush=True)

#                 # Infinite loops are bad for processors, must sleep.
#                 sleep(0.25)
#         except KeyboardInterrupt:
#             break

#     print("\n\nTranscription:")
#     for line in transcription:
#         print(line)


# if __name__ == "__main__":
#     main()
from MyStream import *