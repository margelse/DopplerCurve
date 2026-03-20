import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from ..data_structurs.base import Mapping
from ..data_structurs.approximation import ResultsApproximatingFunction
from ..utils.preprocessing import MinMaxNormalize, MappingPreprocessingForApproximation
from ..utils.visualization import VisualizationPlots
    
# ---------------------------------------------------------------------------------------------------------------------

def preprocessing_pipeline(mapping:Mapping):
    mapping_processing_start = MappingPreprocessingForApproximation(mapping)

    if not mapping_processing_start.check_none():
        x_without_zero = mapping_processing_start.retreat_from_zero()
    else:
        return None
    
    y = mapping_processing_start.y

    mapping_result = Mapping(x_without_zero, y, mapping_processing_start.condition_normalize)

    return mapping_result

def _normalize_values(values):
    normalize_func = MinMaxNormalize(values)
    normalize_y = normalize_func.normalize()
    return normalize_y

def _unpacking_mapping(mapping:Mapping):
    return mapping.get_x(), mapping.get_y(), mapping.condition_normalize

def search_most_viable_parametres(
        function_approximation,
        mapping:Mapping,
        init_parametres:tuple,
        bounds: tuple,
        condition_normalize_for_approx:bool
):
    x, y, _ = _unpacking_mapping(mapping)

    if condition_normalize_for_approx:
        y = _normalize_values(y)

    try:
        popt, _ = curve_fit(function_approximation, x, y, method='trf', p0=init_parametres, bounds=bounds, maxfev=10000)
    except Exception as e:
        raise(e)

    y_approx = function_approximation(x, *popt)

    mapping_approx = Mapping(x, y_approx, condition_normalize_for_approx)
    result = ResultsApproximatingFunction(
        mapping,
        mapping_approx,
        function_approximation,
        popt
    )
    return result


def get_description_about_results_approximation(
        result_approximating:ResultsApproximatingFunction,
        metrics:dict
):
    print('Values metrics: \n')
    print(result_approximating.metrix_values_show(metrics))

    print('Values MVP: \n')
    print(result_approximating.parametres_show())

def print_plots_results(
        result_approximating:ResultsApproximatingFunction,
        visualization_result:VisualizationPlots
):
    x, y, condition_normalize = _unpacking_mapping(result_approximating.mapping)
    y_approx = result_approximating.y_approx
    
    if condition_normalize:
        y_approx = result_approximating.y_approx_denormalize

    visualization_result.create_plot([x, x], [y, y_approx], ['start line', 'approx line'])