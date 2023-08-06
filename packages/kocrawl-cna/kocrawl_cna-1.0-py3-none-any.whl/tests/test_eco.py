from kocrawl.eco_activity import EcoCrawler
from unittest import TestCase


class EcoTest(TestCase):

    def test(self):
        crawler = EcoCrawler()
        # 1: 가정, 2:직장, 3:매장, 4:식당, 5:학교
        output = crawler.request_debug('식당') #가정에서_저탄소실천_방안
        self.assertIsInstance(output, tuple)
        print(output)
