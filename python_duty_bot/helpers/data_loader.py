import pickle
from os.path import exists as os_path_exists
from os.path import join as os_path_join
from pathlib import Path

from helpers.config import Config
from helpers.log import Log


class DataLoader:
    __DATA_FILE_EXT = 'pickle'
    __data_base_path = os_path_join(Path(__file__).parent.parent, Config.data_dir)

    @staticmethod
    def __get_file_path(data_name: str) -> str:
        return os_path_join(DataLoader.__data_base_path, f'{data_name}.{DataLoader.__DATA_FILE_EXT}')

    @staticmethod
    def is_file_exist(data_name: str) -> bool:
        if os_path_exists(DataLoader.__get_file_path(data_name)):
            return True
        return False

    @staticmethod
    def load_data(data_name: str):
        Log.logger.debug(f'Loading {data_name} data')
        return pickle.load(open(DataLoader.__get_file_path(data_name), 'rb'))

    @staticmethod
    def save_data(data_name: str, data) -> None:
        pickle.dump(data, open(DataLoader.__get_file_path(data_name), 'wb'))
        Log.logger.debug(f'Saved {data_name} data')

    @staticmethod
    def load_or_empty(data_name: str, empty_value):
        if DataLoader.is_file_exist(data_name):
            return DataLoader.load_data(data_name)
        return empty_value
