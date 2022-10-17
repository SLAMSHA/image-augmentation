import json
import os
from log_manager import get_logger

ROOT = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = 'config'

logger = get_logger()


class ConfigurationManager:
    """
    This class is to manage the configuration and deliver the configs as needed
    """
    def __init__(self, env):
        self.env = env

    def get_data_sources(self):
        """
        :return: Returns all the data sources config
        """
        if self.env == 'dev':
            data_sources = {}
            source_path = os.path.join(ROOT, CONFIG_DIR, 'data_sources.json')
            try:
                with open(source_path) as f:
                    data_sources = json.load(f)
            except FileNotFoundError:
                logger.error(f"ERROR: {source_path} FILE NOT FOUND")
            except Exception as e:
                logger.error(f"ERROR: Failed to load the data source configuration:{source_path}.Exception:{str(e)}")
            return data_sources

    def get_data_source(self, name):
        """
        :param name: Name of the particular data source i.e MotoGp
        :return: the dictionary of the data source config
        """
        data_sources = self.get_data_sources()
        for data_source in data_sources:
            if name == data_source['name']:
                return data_source
        return {}

    def get_all_aug_parameters(self):
        """
        :return: all the augmentation config present in augmentations.json
        """
        if self.env == 'dev':
            aug_parameters = {}
            source_path = os.path.join(ROOT, CONFIG_DIR, 'augmentation.json')
            try:
                with open(source_path) as f:
                    aug_parameters = json.load(f)
            except FileNotFoundError:
                logger.error(f"ERROR: {source_path} FILE NOT FOUND")
            except Exception as e:
                logger.error(f"ERROR: Failed to load the data source configuration:{source_path}.Exception:{str(e)}")
            return aug_parameters

    def get_aug_parameters(self, name):
        """
        :param name: name of the augmentation i.e crop, random_crop
        :return: dictionary of the augmentation parameter
        """
        all_aug_details = self.get_all_aug_parameters()
        for aug_detail in all_aug_details:
            if name == aug_detail['name']:
                return aug_detail
        return {}
