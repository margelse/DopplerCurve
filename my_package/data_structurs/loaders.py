import pandas as pd
import os

class LoaderCSVFilesObject:
    def __init__(
            self,
            dir,
            separation:str,
    ):
        self.dir = dir
        self.separation = separation

        self._get_file_paths()
        self.delete_files = self._check_format_files()

    def _get_file_paths(self):
        self.files_from_dir = sorted(os.listdir(dir))
        self.file_paths = [os.path.join(self.dir, path) for path in self.files_from_dir]

    def _check_format_files(self):
        VALID_FORMAT = '.csv'
        delete_files = []

        for idx, path in enumerate(self.file_paths):
            _, format_file = os.path.splitext(path)
            if format_file == VALID_FORMAT:
                continue
            else:
                file = self.file_paths.pop(idx)
                delete_files.append(file)

        return delete_files
    
    def description(self):
        TEMPLATE = {
            'directory': self.dir,
            'file paths': self.file_paths,
            'delete files': self.delete_files
        }

        return TEMPLATE
