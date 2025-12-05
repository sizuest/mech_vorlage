# Copyright 2023 Hochschule Luzern 

class Test:
    """
    Implements a simple test class.
    """
    def __init__(self):
        self.state = 0
        self.param = 1

    def reset(self):
        self.state = 0

    def addValue(self, value):
        self.state += self.param * value

        return self.state
