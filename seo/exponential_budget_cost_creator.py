import seo.generic_budget_cost_creator as gbcc
#import numpy as np
import math
class exponential_budget_cost_creator(gbcc.generic_budget_cost_creator):
    def __init__(self,model):
        self.model = model

    def activation_func(self,input):
        """sign = 1
        if input<0:
            sign = -1
            input = abs(input)
        else:
            if input == 0:
                return float("inf")
        return math.exp(input)*sign"""
        return math.exp(abs(input))