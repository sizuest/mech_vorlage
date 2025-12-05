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
        self.assertEqual(self.pid.error_linear, self.pid.reference_value,
                         "linear error and reference position should be equal at initialisation")
        self.assertEqual(self.pid.error_integral, 0,
                         "integral error should be 0 at initialisation")

    def test_7steps(self):
        # Um sicherzustellen, dass für den Test auch wirklich die richtigen
        # PID-Parameter verwendet werden, setzen wir diese vor den Tests auf
        # die Werte, die auch im Excel-Sheet verwendet wurden. Auf diese Weise
        # können Sie die produktiven Parameter in PIDController.py nach Bedarf
        # anpassen und müssen nicht befürchten, dass diese Tests deswegen
        # plötzlich nicht mehr durchlaufen
        self.pid.kp = 0.5
        self.pid.Tn = 10
        self.pid.Tv = 0.01

        self.assertEqual(self.pid.calculate_controller_output(0)[0], 207)
        self.assertEqual(self.pid.calculate_controller_output(100)[0], 107)
        self.assertEqual(self.pid.calculate_controller_output(200)[0], 57)
        self.assertEqual(self.pid.calculate_controller_output(300)[0], 8)
        self.assertEqual(self.pid.calculate_controller_output(380)[0], -21)
        self.assertEqual(self.pid.calculate_controller_output(400)[0], -1)
        self.assertEqual(self.pid.calculate_controller_output(417)[0], -8)

        self.assertAlmostEqual(self.pid.error_integral, 11.08, 3)

    def test_antiwindup(self):
        # Um möglichst schnell in den Windup-Fall zu laufen, verwenden wir
        # hier ein paar aggressivere PID-Parameter. Auch hier entsprechen
        # diese aber wieder den Werten im Excel-Sheet.
        # ACHTUNG: Da wir auch die refposition verändern, müssen wir
        # zusätzlich reset() aufrufen, da innerhalb dieser Funktion
        # self.errorLinear auf refposition zurück gesetzt wird.
        self.pid.kp = 0.5
        self.pid.Tn = 0.05
        self.pid.Tv = 0.01

        self.pid.reference_value = 70000
        self.pid.reset()

        self.assertEqual(self.pid.calculate_controller_output(0)[0], 36023)
        self.assertEqual(self.pid.calculate_controller_output(100)[0], 35923)
        self.assertEqual(self.pid.calculate_controller_output(200)[0], 35873)

        self.assertAlmostEqual(self.pid.error_integral, self.pid.anti_windup / (self.pid.kp / self.pid.Tn), 3)

