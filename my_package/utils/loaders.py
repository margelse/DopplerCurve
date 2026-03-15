import os
import pandas as pd
import numpy as np
from ..data_structurs.base import Mapping
from ..data_structurs.approximation import StructurePipelineApproximation

class SeriesLoaderFromCSV:
    def __init__(self, series_dir):
        self.series_dir = series_dir
        self.series_files = sorted(os.listdir(series_dir))
        
    def __len__(self):
        return len(self.series_files)

    def __getitem__(self, idx):
        series_filename = self.series_files[idx]
        series_path = os.path.join(self.series_dir, series_filename)

        try:
            series = pd.read_csv(series_path, sep=',')
        except Exception as e:
            print(e, f"Skipped file: {series_path}")
            return self.__getitem__((idx + 1) % len(self))
        
        label = self._extract_label(series_filename)
        
        return series, label
    
    def _extract_label(self, filename):
        """
        
        Извлекает метку из имени файла.
        Пример: **/Larin^Sergey_ICA LS_270425-202349_7.csv -> Larin^Sergey_ICA LS
        
        """
        name_without_ext = os.path.splitext(filename)[0]
        parts = name_without_ext.split('_')
        label_parts = parts[:-2]
        
        label = '_'.join(label_parts)
        
        return label
    
class MappingLoadersFromNumpy:
    def __init__(self, files_dir):
        self.files_dir = files_dir
        self.series_files = sorted(os.listdir(files_dir))

    def __len__(self):
        return len(self.series_files)
    
    def __getitem__(self, key):
        pass

class PipelineLoader: # добавить аннотацию о работе цепи
    def __init__(self, series_time:Mapping, pipeline:StructurePipelineApproximation):
        self.series_time = series_time
        self.pipeline = pipeline

        self.description = {}

    def __len__(self):
        count_nodes = list((self.pipeline).keys())
        return len(count_nodes)
    
    def __getitem__(self, key):
        now_section_title = list((self.pipeline).keys())[key]
        tags_section = (self.pipeline)[now_section_title]

        local_func = tags_section['function']
        local_mapping = self._get_local_mapping(tags_section['section'])
        local_parametres = tags_section['parametres']

        return local_func, local_mapping, local_parametres

    def _get_local_mapping(self, bounds):
        x = (self.series_time).get_x()
        y = (self.series_time).get_y()
        condition_normalize = (self.series_time).condition_normalize

        start = np.searchsorted(x, bounds[0], side='left')
        end = np.searchsorted(x, bounds[1], side='right') - 1

        local_mapping = Mapping(
            np.copy(x[start:end]),
            np.copy(y[start:end]),
            condition_normalize
        )

        return local_mapping