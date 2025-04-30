import os
import yaml

from validators import Validator
from utils import ErrorHandler


class FileHelper:
    def __init__(self, validator=None):
        self._validator = validator or Validator()

    def read_file(self, filepath, encoding='utf-8', file_type='file'):
        """Read a file after validating its existence."""
        Validator().file.validate_file_exists(filepath, file_type=file_type)
        with open(filepath, encoding=encoding) as f:
            return f.read()

    def load_template(self, filename):
        """Load an HTML template from the templates directory."""
        base_dir = os.path.dirname(__file__)
        template_dir = os.path.join(base_dir, '..', 'templates')
        path = os.path.join(template_dir, filename)
        return self.read_file(path, file_type='template')

    def load_thresholds(self, config_path):
        """Load and parse YAML thresholds config file."""
        content = self.read_file(config_path, file_type='config file')
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            ErrorHandler.log_and_raise_error(ValueError, f"Error parsing YAML file: {e}")
            