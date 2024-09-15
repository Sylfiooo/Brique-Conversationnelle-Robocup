# from example_interfaces.srv import AddTwoInts
from interfaces_services.srv import Tts                                                          

from .submodules.tts_algo import FallBackTTSManager

import rclpy
from rclpy.node import Node


class NodeTTS(Node):
    def __init__(self, fallback_tts_manager):
        super().__init__('tts')
        self.srv = self.create_service(Tts, 'generate_and_play_tts', fallback_tts_manager.generate_and_play_tts)      

       
def main():
    rclpy.init()

    fallback_tts_manager = FallBackTTSManager()

    # Start thread background benchmark
    fallback_tts_manager.start_benchmark_thread()

    node_tts = NodeTTS(fallback_tts_manager)

    rclpy.spin(node_tts)

    rclpy.shutdown()


if __name__ == '__main__':
    main()