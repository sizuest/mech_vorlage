# Copyright 2022 Hochschule Luzern - Informatik
# Author: Silvan Wegmann <silvan.wegmann@hslu.ch>
import unittest
import math
from Logger import Logger


class LoggerTest(unittest.TestCase):
     def setUp(self):
         self.uut = Logger(1.111, 2.2222, 3.33333, 400)

     def test_plotting(self):
         for i in range(720):
             self.uut.log(i, int(100.0 * math.sin(i * math.pi / 180.0)), [1.111, 2.2222, 3.3333])
         self.uut.showLoggings()