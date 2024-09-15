import torch
from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play
import base64
import io
import urllib.request
import time
import threading

# Voice RSS text-to-speech SDK for Python 3.x
import http.client
import urllib.parse


class CoquiTTSPlayer():
    def __init__(self):
        device = self.get_device()
        self.tts = TTS("tts_models/en/vctk/vits").to(device)


    def get_device(self):
        if torch.cuda.is_available() :
            device = "cuda"  
            print("Will run on GPU (cuda) for this execution")
        else : 
            device = "cpu" 
            print("Will run on CPU for this execution")
        return device
    

    def generate_and_play_tts(self, text, output_file="./final.wav", play_tts=True):
        self.tts.tts_to_file(text=text,
                file_path=output_file,
                speaker="p330",
                )
        if play_tts:
            audio = AudioSegment.from_wav(output_file)
            play(audio)



class VoiceRSSTTSPlayer():
    def __init__(self):
        self.voice_rss_sdk = VoiceRSS_SDK()
        self.base64_string = None


    def text_to_speech(self, text):
        voice = self.voice_rss_sdk.speech({
            'key': '07c0e45c7f3c4e4893ff700ce48b65c9',
            'hl': 'en-us',
            'v': 'John',
            'src': text,
            'r': '0',
            'c': 'mp3',
            'f': '44khz_16bit_stereo',
            'ssml': 'false',
            'b64': 'true'
        })
        audio_byte_array = voice['response']
        audio_string = audio_byte_array.decode('utf-8')
        self.base64_string = audio_string.split("base64")[1][1:]


    def play_base_64(self, play_tts):
        byte_array = base64.b64decode(self.base64_string)
        audio = AudioSegment.from_file(io.BytesIO(byte_array), format="mp3")
        if play_tts:
            play(audio)


    def generate_and_play_tts(self, text, play_tts=True):
        self.text_to_speech(text)
        if self.base64_string:
            self.play_base_64(play_tts)


class VoiceRSS_SDK():
    def speech(self, settings):
        self.__validate(settings)
        return self.__request(settings)

    def __validate(self, settings):
        if not settings: raise RuntimeError('The settings are undefined')
        if 'key' not in settings or not settings['key']: raise RuntimeError('The API key is undefined')
        if 'src' not in settings or not settings['src']: raise RuntimeError('The text is undefined')
        if 'hl' not in settings or not settings['hl']: raise RuntimeError('The language is undefined')

    def __request(self, settings):
        result = {'error': None, 'response': None}

        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        params = urllib.parse.urlencode(self.__buildRequest(settings))
        
        if 'ssl' in settings and settings['ssl']:
            conn = http.client.HTTPSConnection('api.voicerss.org:443')
        else:
            conn = http.client.HTTPConnection('api.voicerss.org:80')
            
        conn.request('POST', '/', params, headers)
        
        response = conn.getresponse()

        content = response.read()
        
        if response.status != 200:
            result['error'] = response.reason
        elif content.find(b'ERROR') == 0:
            result['error'] = content
        else:
            result['response'] = content
            
        conn.close()

        return result

    def __buildRequest(self, settings):
        params = {'key': '', 'src': '', 'hl': '', 'v': '', 'r': '', 'c': '', 'f': '', 'ssml': '', 'b64': ''}
        
        if 'key' in settings: params['key'] = settings['key']
        if 'src' in settings: params['src'] = settings['src']
        if 'hl' in settings: params['hl'] = settings['hl']
        if 'v' in settings: params['v'] = settings['v']
        if 'r' in settings: params['r'] = settings['r']
        if 'c' in settings: params['c'] = settings['c']
        if 'f' in settings: params['f'] = settings['f']
        if 'ssml' in settings: params['ssml'] = settings['ssml']
        if 'b64' in settings: params['b64'] = settings['b64']
        
        return params



class FallBackTTSManager():
    def __init__(self):
        # super().__init__('tts')
        # # self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        # self.srv = self.create_service(Tts, 'generate_and_play_tts', self.generate_and_play_tts)       # CHANGE

        self.coqui_tts_player = CoquiTTSPlayer()
        self.voice_rss_tts_player = VoiceRSSTTSPlayer()

        # First artificial init, it can take time on certain models
        self.coqui_tts_player.generate_and_play_tts("Hello, I'm ready")
        print("Please, wait few seconds, configuration in progress")
        self.mode = self.benchmark_models()
        print("Ok, we have choose mode : " + self.mode)


    def start_benchmark_thread(self):
        def benchmark_thread_func():
            while True:
                # time.sleep(60)
                time.sleep(180)
                print("Start of the reccurent benchmark in background")
                self.mode = self.benchmark_models()
                print("Ok, we have choose mode : " + self.mode)

        benchmark_thread = threading.Thread(target=benchmark_thread_func)
        benchmark_thread.daemon = True  # Thread will end when principal process will end
        benchmark_thread.start()


    def benchmark_models(self):
        list_check_connexion=[]
        online_total_time=0
        offline_total_time=0
        offline_time_check=5
        # online_time_check=5
        online_time_check=2
        for i in range(5):
            list_check_connexion.append(self.check_wifi_connection())
        if list_check_connexion.count(True) >= 3 :
            for i in range(online_time_check):
                online_total_time = online_total_time + self.get_inference_time("online")
            for j in range(offline_time_check):
                offline_total_time = offline_total_time + self.get_inference_time("offline")
            if (online_total_time/online_time_check) < (offline_total_time/offline_time_check) : 
                return "online"
            else: 
                return "offline"
        else: 
            return "offline"


    def get_inference_time(self, mode):
        text_to_test = "So I need to put the knife on the table and then I have to return in the bathroom to give it to John ?"
        if mode == "offline" : 
            start_time = time.time()
            self.coqui_tts_player.generate_and_play_tts(text_to_test, "./final.wav", False)
            elapsed_time = time.time() - start_time
            print("Offline : " + str(elapsed_time))
        if mode == "online" : 
            start_time = time.time()
            self.voice_rss_tts_player.generate_and_play_tts(text_to_test, False)
            elapsed_time = time.time() - start_time
            print("Online : " + str(elapsed_time))
        return elapsed_time


    def check_wifi_connection(self):
        try:
            start_time = time.time()
            # Request the voicerss website
            urllib.request.urlopen('https://www.voicerss.org/', timeout=1)
            end_time = time.time()
            latency = end_time - start_time
            # Check if response time is less than a maximum time, for example 1sec
            if latency < 1:
                print("Latency : " + str(latency))
                return True
            else:
                print(f"High latency: {latency} seconds")
                return False
        except Exception as e:
            print(f"Error checking connection: {e}")
            return False


    def generate_and_play_tts(self, request, response):
        if self.mode == "online":
            self.voice_rss_tts_player.generate_and_play_tts(request.text)
        else:
            self.coqui_tts_player.generate_and_play_tts(request.text)
        response.result = True
        return response




# def main():
#     rclpy.init()

#     fallback_tts_manager = FallBackTTSManager()

#     # Start thread background benchmark
#     fallback_tts_manager.start_benchmark_thread()

#     rclpy.spin(fallback_tts_manager)

#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()