from interfaces_services.srv import SentenceCreator, SentenceSplitter, OrderFormatter

import rclpy
from rclpy.node import Node
from .submodules.nlp_algo import NlpAlgorithm

class Nlp(Node):
    def __init__(self):
        super().__init__('nlp')
        self.nlp_algo = NlpAlgorithm(True)

        self.sentence_creator_srv = self.create_service(SentenceCreator, 'sentence_creator', self.sentence_creator_callback)
        self.sentence_splitter_srv = self.create_service(SentenceSplitter, 'sentence_splitter', self.sentence_splitter_callback)
        self.order_formatter_srv = self.create_service(OrderFormatter, 'order_formatter', self.order_formatter_callback)

        self.get_logger().info('NLP service has started')

    def sentence_creator_callback(self, request, response):
        sentence = self.nlp_algo.generate_sentence(request.objects_formatted)
        response.sentence = sentence
        return response

    def sentence_splitter_callback(self, request, response):
        subphrases = self.nlp_algo.split_sentence(request.sentence)
        response.subphrases = subphrases
        return response

    def order_formatter_callback(self, request, response):
        formatted_order = self.nlp_algo.format_order(request.sentence)
        response.object_formatted = formatted_order
        return response

def main(args=None):
    rclpy.init(args=args)
    print('Hi from NLP Node.')
    
    nlp = Nlp()
    
    rclpy.spin(nlp)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
