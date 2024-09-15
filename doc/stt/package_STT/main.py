from Vosk import Vosk
from Whisper import Whisper
#import speech_recognition as sr

# class MySTT(Whisper):

#     def init_recorder(self):
#         record_timeout = 2
#         recorder = sr.Recognizer()
#         recorder.energy_threshold = 1000
#     # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
#         recorder.dynamic_energy_threshold = False
#         source = sr.Microphone(sample_rate=16000)
#         with source :
#             recorder.adjust_for_ambient_noise(source)
#         recorder.listen_in_background(source, self.callback, phrase_time_limit=record_timeout)

    
#     def callback(self,_, audio:sr.AudioData) -> None:
#         """
#         Threaded callback function to receive audio data when recordings finish.
#         audio: An AudioData containing the recorded bytes.
#         """
#         # Grab the raw bytes and push it into the thread safe queue.
#         data = audio.get_raw_data()
#         self.q.put(data)



if __name__ == '__main__':
    vosk = Vosk()
    #vosk.load_model_online("en-us")
    #vosk.load_model_local("./STT/modele/modele_vosk/vosk-model-small-fr-0.22")
    vosk.load_model_local("/tmp/vosk-model-fr-0.22")
    vosk.init_recorder(44100.0,8000,None,1,vosk.callback)
    vosk.start_recorder()
    #vosk.init_recorder()
    text = vosk.run_STT(True)
    print("#"*36 + " RESULT " + 36*"#")
    print(text)
    print("#"*80)

    # print("")

    # vosk.reset_data()
    # text = vosk.run_STT(True)
    # print("#"*36 + " RESULT " + 36*"#")
    # print(text)
    # print("#"*80)


    # whisper = Whisper()
    # #vosk.load_model_online("en-us")
    # whisper.load_model_online("base")
    # #vosk.load_model_local("/tmp/vosk-model-en-us-0.22")
    # whisper.init_recorder()
    # whisper.run_STT()
    # #print("#"*36 + " RESULT " + 36*"#")
    # #print(text)
    # #print("#"*80)

