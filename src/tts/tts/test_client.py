import sys
from interfaces_services.srv import Tts                         

import rclpy
from rclpy.node import Node


class ClientTTS(Node):

    def __init__(self):
        super().__init__('test_client_tts')
        self.cli = self.create_client(Tts, 'generate_and_play_tts')       # CHANGE
        # self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        # self.req = AddTwoInts.Request()
        self.req = Tts.Request()                                   # CHANGE

    def loop(self):
        while True:
            # Use readline to get input navigation with arrows
            text_to_speak = input("Enter the text you want the program to say (or type 'exit' to quit): ")
            if text_to_speak.lower() == 'exit':
                print("Program terminated.")
                break
            self.send_request(text_to_speak)

    def send_request(self, text):
        self.req.text = text  
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)


def main():
    rclpy.init()

    client_tts = ClientTTS()
    client_tts.loop()

    client_tts.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()