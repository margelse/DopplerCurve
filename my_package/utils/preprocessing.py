import numpy as np
from ..data_structurs.base import Mapping

class MinMaxNormalize:
    def __init__(self, values_start):
        self.values_start = values_start
        
        self.max_value = np.max(self.values_start)
        self.min_value = np.min(self.values_start)

    def normalize(self):
        values_normalize = (self.values_start - self.min_value) / (self.max_value - self.min_value)
        
        return values_normalize
    
    def denormalize(self, values_normalize):
        return values_normalize * (self.max_value - self.min_value) + self.min_value
    
class MappingPreprocessingForApproximation(MinMaxNormalize):
    def __init__(self, mapping:Mapping):
        self.mapping = mapping
        self._init_mapping_attributes()

        MinMaxNormalize.__init__(self, self.y)

    def _init_mapping_attributes(self):
        self.x = (self.mapping).get_x()
        self.y = (self.mapping).get_y()
        self.condition_normalize = (self.mapping).condition_normalize
    
    def check_none(self):
        for name, val in zip(['x', 'y'], (self.x, self.y)):
            count_none = np.sum(np.isnan(val))
            if count_none > 0:
                print(f'{name} contains nan')
                return True
        
        return False
    
    def retreat_from_zero(self):
        X_without_zero = np.copy(self.x)
        X_without_zero[X_without_zero == 0] = 1e-4

        return X_without_zero

    def replacing_duplicates(self):
        pass

    def normalize(self):
        self._check_condition_normalize()
        return super().normalize()
    
    def _check_condition_normalize(self): # Сделать нормальный raise
        if self.condition_normalize:
            raise(ValueError('The data is already normalized'))
    
    def denormalize(self, values_normalize):
        return super().denormalize(values_normalize)