
from interfaces_services.srv import SentenceSplitter, OrderFormatter, SentenceCreator, Tts, YesOrNo
from std_msgs.msg import String

import rclpy
from rclpy.node import Node
import threading


class ConvClient(Node):
    def __init__(self):
        super().__init__('main')

        self.pubRes = self.create_publisher(String, 'main_node/final_order', 10)

        self.cliSenSpli = self.create_client(SentenceSplitter, 'sentence_splitter')
        self.cliYesOrNo = self.create_client(YesOrNo, 'stt/yes_or_no')

        while not self.cliSenSpli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service Sentence Splitter not available, waiting again...')
        self.reqSenSpli = SentenceSplitter.Request()
        self.cliOrdFor = self.create_client(OrderFormatter, 'order_formatter')
        while not self.cliOrdFor.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service Order Formatter not available, waiting again...')
        self.reqOrdFor = OrderFormatter.Request()
        self.cliSenCre = self.create_client(SentenceCreator, 'sentence_creator')
        while not self.cliSenCre.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service Sentence Creator not available, waiting again...')
        self.reqSenCre = SentenceCreator.Request()
        self.cliTssPlay = self.create_client(Tts, 'generate_and_play_tts')
        while not self.cliTssPlay.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service TTS not available, waiting again...')
        self.reqTssPlay = Tts.Request()
        while not self.cliYesOrNo.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service STT Yes or no not available, waiting again...')
        self.reqYesOrNo = YesOrNo.Request()

        self.is_recu = False
        self.text = ""

        self.subStt = self.create_subscription(String,'stt/res',self.receive_text_callback,10)

        self.my_func = threading.Thread(target=self.loop_thread_function)
        self.my_func.daemon = True  # Thread will end when principal process will end
        self.my_func.start()
        
    def loop_thread_function(self):
        while (rclpy.ok()):
            if (self.is_recu):
                self.is_recu = False
                self.main_function()


    def main_function(self):
        print(self.text)
        response = self.send_splitsentence_request(self.text)
        print(response.subphrases)
        subphrases = response.subphrases

        tab = []
        for sub_sentance in subphrases :
            response = self.send_orderformatter_request(sub_sentance)
            tab.append(response.object_formatted)
        print(tab)

        response = self.send_sentencecreator_request(tab)
        print(response.sentence)

        sentence = response.sentence
        response = self.send_ttsplay_request(sentence)

        print(response.result)
        print("Response above should be tts TRUE")

        if (True):

            response_yes_no = self.send_yes_or_no_request()
            print("res = " + str(response_yes_no.res))
            if (response_yes_no.res == 3):
                response = self.send_ttsplay_request(sentence)
                print(response.result)
                print(sentence)
                response_yes_no = self.send_yes_or_no_request()

            if (response_yes_no.res == 1):
                response = self.send_ttsplay_request("Okay i do it !")
                print(response.result)
                print("OK I do it !")
                tab_string = ', '.join(str(x) for x in tab)
                tab_to_send = String()
                tab_to_send.data = tab_string
                self.pubRes.publish(tab_to_send)
                
                
            if (response_yes_no.res == 2):
                response = self.send_ttsplay_request("can you repeat please ?")
                print(response.result)
                print("Can you repeat please ?")

            
            print("res = " + str(response_yes_no.res))


    def receive_text_callback(self,data):
        self.text = data.data
        self.is_recu = True
    
    def send_splitsentence_request(self, sentence):
        self.reqSenSpli.sentence = sentence
        self.future = self.cliSenSpli.call(self.reqSenSpli)
        print(self.future)
        return self.future
    
    def send_orderformatter_request(self, sentence):
        self.reqOrdFor.sentence = sentence
        self.future = self.cliOrdFor.call(self.reqOrdFor)
        return self.future
    
    def send_sentencecreator_request(self, objects_formatted):
        self.reqSenCre.objects_formatted = objects_formatted
        self.future = self.cliSenCre.call(self.reqSenCre)
        return self.future
    
    def send_ttsplay_request(self, text):
        self.reqTssPlay.text = text
        self.future = self.cliTssPlay.call(self.reqTssPlay)
        return self.future
    
    def send_yes_or_no_request(self):
        self.future = self.cliYesOrNo.call(self.reqYesOrNo)
        return self.future


def main():
    print('Hi from main node.')

    rclpy.init()

    conv_client = ConvClient()

    rclpy.spin(conv_client)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
