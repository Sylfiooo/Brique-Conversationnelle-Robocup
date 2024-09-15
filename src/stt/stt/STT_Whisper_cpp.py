import rclpy
from rclpy.node import Node
import signal
import time

from stt.STT_Whisper_Cpp_Binder import *
import ctypes
from std_msgs.msg import String, Empty
from multiprocessing import Process

from interfaces_services.srv import YesOrNo
import asyncio

import sys

class STT_Whisper_cpp(Node) :
    # Liste des arguments

    def __init__ (self):
        self.is_running = True
        super().__init__('stt_whisper_cpp')

        package_share_directory = get_package_share_directory('stt')
        file_path = os.path.join(package_share_directory, 'modele', 'ggml-base.en.bin')
        
        self.args = [ctypes.c_char_p(b"stream"), ctypes.c_char_p(b"-m"), ctypes.c_char_p(file_path.encode('utf-8')), 
                                        ctypes.c_char_p(b"-l"), ctypes.c_char_p(b"en"), 
                                        ctypes.c_char_p(b"-t"), ctypes.c_char_p(b"6"),
                                        ctypes.c_char_p(b"-vth"), ctypes.c_char_p(b"0.7"), 
                                        ctypes.c_char_p(b"-f"), ctypes.c_char_p(b"test.txt"),
                                        None]

        # Créer une instance de la classe STT_Whisper
        self.stt = STT_Whisper_Cpp_Binder(len(self.args) - 1, self.args[:-1])

        self.publisher_res = self.create_publisher(String, 'stt/res', 10)

        self.subscription = self.create_subscription(Empty,'stt/kill',self.kill_callback,10)

        self.srv = self.create_service(YesOrNo, 'stt/yes_or_no', self.run_yes_or_no_func)

        #signal.signal(signal.SIGINT, self.handler)

        #self.run_STT()
        self.loop = asyncio.get_event_loop()
        self.cpp_task = self.loop.run_in_executor(None, self.run_STT)

    def kill_callback(self,data):
        self.cpp_task.cancel()
        self.loop.stop()
        self.stt.kill_func()
    
    def run_yes_or_no_func(self,data, response):
        self.is_running = False
        self.stt.kill_func()
        time.sleep(2)
        self.stt.switch_run_true_func()
        response.res =  self.stt.yes_or_no_func(len(self.args) - 1, self.args[:-1])
        self.is_running = True
        self.cpp_task = self.loop.run_in_executor(None, self.run_STT) 

        return response

    def run_STT(self):
        # Appeler la fonction run_func avec les arguments

        while self.is_running:
            result = self.stt.run_func(len(self.args) - 1, self.args[:-1])  # Exclure le dernier élément de la liste (None)
            print(result)

            if result != None :
                #on supprime tout les caratère spéciau qui pourrait être mal interpréter par le nlp
                valeurFinal = result.decode('utf-8').replace("."," ")
                valeurFinal = valeurFinal.replace("?"," ")
                valeurFinal = valeurFinal.replace(","," ")
                valeurFinal = valeurFinal.replace("!"," ")
                valeurFinal = valeurFinal.replace(";"," ")
                valeurFinal = valeurFinal.replace("."," ")
                valeurFinal = valeurFinal.lower()

                #On suprime le mot d'activation
                if ("okay" in valeurFinal):
                    index_min = min(valeurFinal.index("okay"),0)
                    valeurFinal = valeurFinal[index_min:]
                    valeurFinal = valeurFinal.replace("okay","")
                elif ("okey" in valeurFinal):
                    index_min = min(valeurFinal.index("okey"),0)
                    valeurFinal = valeurFinal[index_min:]
                    valeurFinal = valeurFinal.replace("okey","")
                elif ("ok" in valeurFinal):
                    index_min = min(valeurFinal.index("ok"),0)
                    valeurFinal = valeurFinal[index_min:]
                    valeurFinal = valeurFinal.replace("ok","")

                
                res = String()
                res.data = valeurFinal
                self.publisher_res.publish(res)




def main(args=None):
    rclpy.init(args=args)

    stt_main_node = STT_Whisper_cpp()

    rclpy.spin(stt_main_node)

    stt_main_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
