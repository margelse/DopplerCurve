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
    
class MinMaxNormalizeForMappings:
    def __init__(self, mapping:Mapping|list):
        self.mapping = mapping
        self._init_minmax_values()

    def _init_minmax_values(self):
        self.max_value = np.max((self.mapping).get_y())
        self.min_value = np.min((self.mapping).get_y())

    def normalize(self):
        if not self.mapping.condition_normalize:
            dependent_v = (self.mapping).get_y()
            dependent_normalize_v = (dependent_v - self.min_value) / (self.max_value - self.min_value)

            return Mapping((self.mapping).get_x(), dependent_normalize_v, True)
        
        else:
            raise(ValueError('The mapping is already normalized!'))
        
    def denormalize(self, mapping_normalize:Mapping):
        if mapping_normalize.condition_normalize:
            dependent_denormalize_v = mapping_normalize.get_y() * (self.max_value - self.min_value) + self.min_value

            return Mapping(mapping_normalize.get_x(), dependent_denormalize_v, False)
        
        else:
            raise(ValueError('The mapping was not normalized!'))
    
class MappingPreprocessingForApproximation:
    def __init__(self, mapping:Mapping):
        self.mapping = mapping
        self._init_mapping_attributes()

    def _init_mapping_attributes(self):
        self.x = (self.mapping).get_x()
        self.y = (self.mapping).get_y()
        self.condition_normalize = (self.mapping).condition_normalize
    
    def check_none(self):
        for name, val in zip(['x', 'y'], (self.x, self.y)):
            count_none = np.sum(np.isnan(val))
            if count_none > 0:
                self._print_message_if_none
                return True
        
        return False
    
    def _print_message_if_none(self, values):
        print(f'{values} contains nan')

    def retreat_from_zero(self):
        X_without_zero = np.copy(self.x)
        X_without_zero[X_without_zero == 0] = 1e-4

        return X_without_zero