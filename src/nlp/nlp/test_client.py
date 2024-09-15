from interfaces_services.srv import SentenceSplitter, OrderFormatter, SentenceCreator

import rclpy
from rclpy.node import Node

class TestClient(Node):
    def __init__(self):
        super().__init__('test_client_nlp')
        self.cliSenSpli = self.create_client(SentenceSplitter, 'sentence_splitter')
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
    
    def send_splitsentence_request(self, sentence):
        self.reqSenSpli.sentence = sentence
        self.future = self.cliSenSpli.call_async(self.reqSenSpli)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    
    def send_orderformatter_request(self, sentence):
        self.reqOrdFor.sentence = sentence
        self.future = self.cliOrdFor.call_async(self.reqOrdFor)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    
    def send_sentencecreator_request(self, objects_formatted):
        self.reqSenCre.objects_formatted = objects_formatted
        self.future = self.cliSenCre.call_async(self.reqSenCre)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main():
    rclpy.init()

    test_client = TestClient()

    response = test_client.send_splitsentence_request("go into the kitchen and into the bathroom, bring two bananas, a potato and three tacos to Bob and to Cassy and catch me a beer")
    print(response.subphrases)
    subphrases = response.subphrases

    tab = []
    for sub_sentance in subphrases :
        response = test_client.send_orderformatter_request(sub_sentance)
        tab.append(response.object_formatted)
    print(tab)

    response = test_client.send_sentencecreator_request(tab)
    print(response.sentence)

    test_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()    