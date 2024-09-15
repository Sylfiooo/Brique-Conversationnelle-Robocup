# # #!/usr/bin/env python3

# # import wave
# # import sys
# # import json
# # import numpy as np
# # import time
# # from pydub import AudioSegment


# # from vosk import Model, KaldiRecognizer, SetLogLevel

# # # You can set log level to -1 to disable debug messages

# # SetLogLevel(-1)

# # audio_path = sys.argv[1]



# # # Chargez le fichier audio
# # audio = AudioSegment.from_file(audio_path, format="wav")
# # audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)

# # # Convertissez-le dans le format souhaité (par exemple, WAV)
# # audio.export("audio_convert/convert.wav", format="wav")


# # wf = wave.open("audio_convert/convert.wav", "rb")
# # if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
# #     print("Audio file must be WAV format mono PCM.")
# #     sys.exit(1)

# # start = time.time()
# # #model = Model("/tmp/vosk-model-fr-0.22")
# # model = Model("Modele/vosk-model-small-fr-0.22")

# # # You can also init model by name or with a folder path
# # # model = Model(model_name="vosk-model-en-us-0.21")
# # # model = Model("models/en")

# # rec = KaldiRecognizer(model, wf.getframerate())
# # rec.SetWords(False)
# # rec.SetPartialWords(False)

# # while True:
# #     data = wf.readframes(4000)
# #     if len(data) == 0:
# #         break
# #     if rec.AcceptWaveform(data):
# #         #print(rec.Result())
# #         pass
# #     else:
# #         #print(rec.PartialResult())
# #         pass

# # stop = time.time() - start

# # print(json.loads(rec.FinalResult()))
# # print(stop)





# #!/usr/bin/env python3

# import wave
# import sys
# import json

# from vosk import Model, KaldiRecognizer, SetLogLevel

# SetLogLevel(0)

# import wave
# import sys
# import json
# import numpy as np
# import time
# from pydub import AudioSegment


# from vosk import Model, KaldiRecognizer, SetLogLevel

# # You can set log level to -1 to disable debug messages

# SetLogLevel(-1)

# audio_path = sys.argv[1]

# audio = AudioSegment.from_file(audio_path, format="wav")
# audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)

# # Convertissez-le dans le format souhaité (par exemple, WAV)
# audio.export("audio_convert/convert.wav", format="wav")

# wf = wave.open("audio_convert/convert.wav", "rb")
# if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
#     print("Audio file must be WAV format mono PCM.")
# #     sys.exit(1)

# start = time.time()
# model = Model("/tmp/vosk-model-fr-0.6-linto-2.2.0")
# rec = KaldiRecognizer(model, wf.getframerate())
# rec.SetMaxAlternatives(0)
# rec.SetWords(True)

# while True:
#     data = wf.readframes(100)
#     if len(data) == 0:
#         break
#     if rec.AcceptWaveform(data):
#         pass
#         #print(json.loads(rec.Result()))
#     else:
#         #print(json.loads(rec.PartialResult()))
#         pass
# stop = time.time() - start

# print(json.loads(rec.FinalResult()))
# print(stop)



# #!/usr/bin/env python3


# # import wave
# # import sys
# # import json
# # import numpy as np
# # import time
# # from pydub import AudioSegment


# # from vosk import Model, KaldiRecognizer, SetLogLevel

# # # You can set log level to -1 to disable debug messages

# # SetLogLevel(-1)

# # audio_path = sys.argv[1]

# # audio = AudioSegment.from_file(audio_path, format="wav")
# # audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)

# # # Convertissez-le dans le format souhaité (par exemple, WAV)
# # audio.export("audio_convert/convert.wav", format="wav")

# # wf = wave.open("audio_convert/convert.wav", "rb")
# # if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
# #     print("Audio file must be WAV format mono PCM.")
# # #     sys.exit(1)

# # start = time.time()
# # model = Model("Modele/vosk-model-small-fr-0.22")
# # rec = KaldiRecognizer(model, wf.getframerate())
# # rec.SetMaxAlternatives(5)
# # rec.SetWords(True)

# # while True:
# #     data = wf.readframes(100)
# #     if len(data) == 0:
# #         break
# #     if rec.AcceptWaveform(data):
# #         pass
# #         #print(json.loads(rec.Result()))
# #     else:
# #         #print(json.loads(rec.PartialResult()))
# #         pass
# # stop = time.time() - start

# # print(json.loads(rec.FinalResult()))
# # print(stop)

#!/usr/bin/env python3

# prerequisites: as described in https://alphacephei.com/vosk/install and also python module `sounddevice` (simply run command `pip install sounddevice`)
# Example usage using Dutch (nl) recognition model: `python test_microphone.py -m nl`
# For more help run: `python test_microphone.py -h`

import argparse
import queue
import sys
import sounddevice as sd
import json

from vosk import Model, KaldiRecognizer


from threading import Thread
from playsound import playsound
from multiprocessing import Process



playsound("./STT/test/fichier_audio_input/sound.mp3")


q = queue.Queue()

rec_data = False
compteur = 0

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    print("Je suis la")
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])rec.PartialResult() 
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model("/tmp/vosk-model-fr-0.6-linto-2.2.0")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    print(args.samplerate)
    print(args.device)
    test = sd.RawInputStream(args.samplerate,8000,args.device,1,
            "int16",None,None,callback)
    test.start()

    #with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
     #        dtype="int16", channels=1, callback=callback):

    p = Process(target=sd.RawInputStream,args=(args.samplerate,8000,args.device,1,"int16",None,None,callback))

   # (samplerate=None, blocksize=None, device=None, channels=None, dtype=None, latency=None, extra_settings=None, callback=None, finished_callback=None, clip_off=None, dither_off=None, never_drop_input=None, prime_output_buffers_using_stream_callback=None)
    #p.start()
    if (True):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                print(rec.Result())
            else:
                print(rec.PartialResult())
            if dump_fn is not None:
                dump_fn.write(data)

            # data = q.get()
            # if rec.AcceptWaveform(data) and rec_data:
            #     print(rec.Result())
            # else:
            #     print(rec.PartialResult())
            #     if (("commencer" in rec.PartialResult() or "commencé" in rec.PartialResult() or "commencez" in rec.PartialResult()) and not(rec_data)):
            #         #print(rec.PartialResult())
            #         playsound("./STT/test/fichier_audio_input/sound.mp3")
            #         rec_data = True
            #         compteur = 0
            #     if (rec_data):
            #         #print(rec.PartialResult())
            #         pass
            #     if (len(json.loads(rec.PartialResult())['partial']) == 0 and rec_data):
            #         compteur += 1
            #     else :
            #         compteur = 0
            #     if ((compteur > 3 or "stop" in rec.PartialResult()  ) and rec_data):
            #         rec_data = False
            #         compteur == 0
            #         playsound("./STT/test/fichier_audio_input/sound_2.mp3")
            #         print(rec.Result())

            # if dump_fn is not None:
            #     dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))