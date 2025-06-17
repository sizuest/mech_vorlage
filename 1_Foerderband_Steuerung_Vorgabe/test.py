# Copyright 2022 Hochschule Luzern - Informatik
# Author: Silvan Wegmann <silvan.wegmann@hslu.ch>
import sys, pathlib
from tests.utils import is_raspberrypi
if not is_raspberrypi():
    sys.path.append(str(pathlib.Path(__file__).parent / "tests" / "mocks"))

import unittest
from tests.EncoderTest import EncoderTest
# uncomment the following line when you have matplotlib installed
#from tests.LoggerTest import LoggerTest
from tests.PIDControllerTest import PIDControllerTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(EncoderTest))
    #suite.addTest(unittest.makeSuite(LoggerTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(PIDControllerTest))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
