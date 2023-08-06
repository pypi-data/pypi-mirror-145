import sys
import unittest
import argparse
from vava_utils.camunda.camunda_helper import Camunda_Helper
import logging
import pandas as pd
LOG_FORMAT = '%(asctime)-15s|%(levelname)-7s|%(name)s|%(message)s'

# Run with: python3 test_camunda.py --camunda_url URL --camunda_token TOKEN

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance

@singleton
class CamundaTestConfig(dict):
    pass

class TestDmns(unittest.TestCase):

    def setUp(self):

        self.config = CamundaTestConfig()
        self.camunda_helper = Camunda_Helper(self.config['camunda_url'], self.config['camunda_token'])

    def test_get_io(self):
        vehicles = [pd.Series({'make': 'Fiat', 'model': 'Egea', 'bodytype': 'Sedan', 'fueltype': 'Benzin', 'transmission': 'Manuel'
                                , 'trim': '1.4 Fire Easy 95HP', 'year': 2021, 'glassroof': False, 'km': 10000, 'retailprice': 261400})
                    , pd.Series({'make': 'Renault', 'model': 'Clio', 'bodytype': 'Hathback', 'fueltype': 'Benzin', 'transmission': 'Manuel'
                                , 'trim': '1.4 Fire Easy 95HP', 'year': 2021, 'glassroof': True, 'km': 10000, 'retailprice': 421020})
                    ]

        for v in vehicles:
            response = self.camunda_helper.get_initial_offer(v)
            self.assertEqual(response.discounttype, 'Camunda')
            self.assertTrue(response.minprice >= 0 and response.minprice < 3000000)


        return



def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--camunda_url", dest="camunda_url",
                        help="base url of Camunda platform",
                        type=str, required=True)
    arg_parser.add_argument("--camunda_token", dest="camunda_token",
                        help="camunda token",
                        type=str, required=True)

    return arg_parser.parse_args()



def remove_args():
    keep_args = [True]*len(sys.argv)
    for pos,arg in enumerate(sys.argv):
        if arg in ["--camunda_url", "--camunda_token"]:
            keep_args[pos], keep_args[pos+1] = False, False

    sys.argv = [x for i,x in enumerate(sys.argv) if keep_args[i]]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    config = CamundaTestConfig(vars(parse_args()))
    remove_args()

    unittest.main()
