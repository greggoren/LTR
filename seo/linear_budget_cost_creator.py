import seo.generic_budget_cost_creator as gbcc

import math
class linear_budget_cost_creator(gbcc.generic_budget_cost_creator):
    def __init__(self,model):
        self.model = model

    def activation_func(self,input):
        return abs(input)*2