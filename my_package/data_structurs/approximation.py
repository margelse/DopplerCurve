from typing import List, Tuple
from ..utils.preprocessing import MinMaxNormalize
from ..data_structurs.base import Mapping
import pandas as pd

class StructurePipelineApproximation:
    def __init__(
            self,
            names_node:list,
            functions: list,
            values_sections:List[List],
            values_parametres:list[Tuple]
    ):
        self.names_node = names_node

        self.functions = functions
        self.values_sections = values_sections
        self.values_parametres = values_parametres

        self._check_size()

    def _check_size(self):
        if len(self.names_node) != len(self.values_sections) & len(self.names_node) != len(self.values_parametres) & len(self.names_node) != len(self.functions):
            raise(ValueError('The size of the input data is different'))
        
    def get_pipeline(self):
        new_pipeline = dict()
        for name, func, section, parametres in zip(self.names_node, self.functions, self.values_sections, self.values_parametres):
            new_pipeline[name] = {
                'function': func,
                'section': section,
                'parametres': parametres
            }

        return new_pipeline
    
class ResultsApproximatingFunction(MinMaxNormalize):
    def __init__(
            self,
            mapping_start:Mapping,
            mapping_result:Mapping,
            function_approximation,
            parametres_function
    ):
        self.mapping_start = mapping_start
        self.mapping_result = mapping_result

        self.func = function_approximation
        self.FUNCTION_NAME = self.func.__code__.co_name
        self.params = parametres_function

        self._check_condition_normalize()

    def _check_condition_normalize(self):
        if (self.mapping_result).condition_normalize:
            super().__init__((self.mapping_start).get_y())

            self.y_approx = None
            self.y_approx_denormalize = self.denormalize((self.mapping_result).get_y())
        else:
            self.y_approx = (self.mapping_result).get_y()
            self.y_approx_denormalize = None

    def metrix_values_show(self, function_metrics:dict):
        if self.y_approx_denormalize is not None:
            self._calculation_metrix(self.y_approx_denormalize, function_metrics)

        else:
            self._calculation_metrix(self.y_approx, function_metrics)

        df = self._converting_the_results_to_df(self.result_calculate)

        return df
    
    def _calculation_metrix(self, y_approx, function_metrics:dict):
        self.result_calculate = [
            {name: func((self.mapping_start).get_y(), y_approx) for name, func in function_metrics.items()}
        ]

    def parametres_show(self):
        name_args = self._get_name_parametres_from_function()
        names_and_values = self._filling_dict(name_args, self.params)

        df = self._converting_the_results_to_df(names_and_values)

        return df
    
    def _get_name_parametres_from_function(self):
        all_name_args = (self.func).__code__.co_varnames
        number_start_args = 1
        count_args = (self.func).__code__.co_argcount
        name_args = all_name_args[number_start_args:count_args]

        return name_args
    
    def _filling_dict(self, keys, values):
        result = [
            {key: val for key, val in zip(keys, values)}
        ]

        return result

    def _converting_the_results_to_df(self, list_with_dict):
        return pd.DataFrame(list_with_dict)