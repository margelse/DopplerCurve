import numpy as np

class Mapping:
    def __init__(
            self,
            independent_var,
            dependent_var,
            condition_normalize:bool
    ):
        self.independent_var = independent_var
        self.dependent_var = dependent_var
        self.condition_normalize = condition_normalize

    def get_x(self):
        return np.copy(self.independent_var)
    
    def get_y(self):
        return np.copy(self.dependent_var)