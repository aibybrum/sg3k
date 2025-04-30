import yaml

from utils import ErrorHandler, Threshold
from validators import Validator
from helpers import FileHelper


class ThresholdManager:
    def __init__(self, config_path="./config/thresholds_config.yaml", validator=None):
        self._validator = validator or Validator()
        if config_path is None:
            ErrorHandler.log_and_raise_error(ValueError, "Config path cannot be None")
        self._config_path = config_path
        self._file_helper = FileHelper()
        self._thresholds = self._load_thresholds()
        self._validator.thresholds.validate_thresholds(self._thresholds)

    def _load_thresholds(self):
        """Load thresholds from the configuration file."""
        config = self._file_helper.load_thresholds(self._config_path)
        thresholds = {}
        for category, items in config.items():
            thresholds[category] = {
                key: self._create_threshold(value)
                for key, value in items.items()
            }
        return thresholds

    @staticmethod
    def _create_threshold(data):
        """Create a Threshold or a nested dictionary of Thresholds from the config."""
        if isinstance(data, dict) and all(key in data for key in ['thres_peaks', 'min_dist_peaks', 'thres_lows', 'min_dist_lows']):
            return Threshold(**data)
        return {key: Threshold(**value) for key, value in data.items()}

    def get_threshold(self, category, key):
        """Retrieve a specific threshold by category and key."""
        if category not in self._thresholds:
            ErrorHandler.log_and_raise_error(KeyError, f"Category '{category}' not found.")
        if key not in self._thresholds[category]:
            ErrorHandler.log_and_raise_error(KeyError, f"Threshold '{key}' not found in category '{category}'.")
        return self._thresholds[category][key]