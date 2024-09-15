#from STT.package_STT.Vosk import Vosk
from tts.TTSPlayer import FallBackTTSManager
from nlp import init
from stt.package_STT.STT_Whisper_cpp import STT_Whisper_cpp


if __name__ == '__main__':

    fallback_tts_manager = FallBackTTSManager()

    whisper_cpp = STT_Whisper_cpp()
    text = whisper_cpp.run_STT()

    # my_TTSPlayer = TTSPlayer()

    #On affiche le texte
    print("#"*36 + " RESULT " + 36*"#")
    print(text)
    print("#"*80)

    val = init.sentenceSplitter(text)
    print(val)
    tab = []
    for sub_sentance in val :
        sub_formater = init.orderFormatter(sub_sentance)
        tab.append(sub_formater)

    print (tab)
    final_sentance = init.sentenceCreator(tab)
    print(final_sentance)

    
    fallback_tts_manager.generate_and_play_tts(final_sentance)
