import voicerss_tts
import base64
import io
from pydub import AudioSegment
from pydub.playback import play

def text_to_speech(text):
    voice = voicerss_tts.speech({
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
    ausio_string = audio_byte_array.decode('utf-8')
    base64_string = ausio_string.split("base64")[1][1:]
    return base64_string
    
def play_base_64(audio_data):
    byte_array = base64.b64decode(audio_data)
    audio = AudioSegment.from_file(io.BytesIO(byte_array), format="mp3")
    play(audio)

if __name__ == "__main__":

    # Replace 'Hello, world!' with the text you want to convert to speech
    text_to_convert = 'Hello, world! This is a sample text-to-speech conversion.'

    # Convert text to speech and save the audio to a file
    audio_data = text_to_speech(text_to_convert)
    if audio_data:
        play_base_64(audio_data)
