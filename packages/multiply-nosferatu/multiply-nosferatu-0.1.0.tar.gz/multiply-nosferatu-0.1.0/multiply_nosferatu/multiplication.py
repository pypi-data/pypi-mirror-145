#Importing Numpy as NP
import numpy as np

class Multiplication:
    """
    Instantiate a multiplication operation.
    Numbers will be multiplied by the given multiplier.
    
    :param multiplier: The multiplier.
    :type multiplier: int
    """
    def __init__(self, multiplier):
        self.multiplier = multiplier

    def multiply(self,number):
        """
        Multiply a given number by a given multiplier

        :param number: The number to multiply.
        :type number: int
        
        :param muiltiplier: The multiplier.
        :type muiltiplier: int
        """
        return np.dot(number, self.multiplier)