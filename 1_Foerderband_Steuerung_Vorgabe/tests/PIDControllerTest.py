# Copyright 2022 Hochschule Luzern - Informatik
# Author: Silvan Wegmann <silvan.wegmann@hslu.ch>
import unittest
from PIDController import PIDController


class PIDControllerTest(unittest.TestCase):
    def setUp(self):
        self.pid = PIDController()

    def tearDown(self):
        del self.pid

    def test_init(self):
        self.assertEqual(self.pid.errorLinear, self.pid.refposition,
                         "linear error and reference position should be equal at initialisation")
        self.assertEqual(self.pid.errorIntegral, 0,
                         "integral error should be 0 at initialisation")

    def test_7steps(self):
        self.pid.kp = 0.5
        self.pid.ki = 0.05
        self.pid.kd = 0.005

        # TODO: Füllen Sie hier bei den erwarteten Werten (2ter Parameter)
        # die Resultate aus Ihrem Excel-Sheet ein
        self.assertEqual(self.pid.calculateTargetValue(0)[0], 0)
        self.assertEqual(self.pid.calculateTargetValue(100)[0], 0)
        self.assertEqual(self.pid.calculateTargetValue(200)[0], 0)
        self.assertEqual(self.pid.calculateTargetValue(300)[0], 0)
        self.assertEqual(self.pid.calculateTargetValue(380)[0], 0)
        self.assertEqual(self.pid.calculateTargetValue(400)[0], 0)
        self.assertEqual(self.pid.calculateTargetValue(417)[0], 0)

        # TODO: Füllen Sie auch hier beim erwarteten Werte (2ter Parameter)
        # das Resultate für den 7ten Schritt aus Ihrem Excel-Sheet ein
        self.assertAlmostEqual(self.pid.errorIntegral, 0, 3)

    def test_antiwindup(self):
        self.pid.kp = 0.5
        self.pid.ki = 0.5
        self.pid.kd = 0.005

        self.pid.refposition = 70000
        self.pid.reset()

        # TODO: Füllen Sie hier bei den erwarteten Werten (2ter Parameter)
        # die Resultate aus Ihrem Excel-Sheet ein
        self.assertEqual(self.pid.calculateTargetValue(0)[0], 0)
        self.assertEqual(self.pid.calculateTargetValue(100)[0], 0)
        self.assertEqual(self.pid.calculateTargetValue(200)[0], 0)

        self.assertAlmostEqual(self.pid.errorIntegral, 1023/self.pid.ki, 3)

