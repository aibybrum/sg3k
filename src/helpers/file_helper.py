import os
import yaml

from validators import Validator
from utils import ErrorHandler
from jinja2 import Template


class FileHelper:
    def __init__(self, validator=None):
        self._validator = validator or Validator()

    @ErrorHandler.log_exceptions
    def read_file(self, filepath, encoding='utf-8', file_type='file'):
        """Read a file after validating its existence."""
        self._validator.file.validate_file_exists(filepath, file_type=file_type)
        try:
            with open(filepath, encoding=encoding) as f:
                return f.read()
        except Exception as e:
            ErrorHandler.log_and_raise_error(IOError, f"Error reading {file_type} at '{filepath}': {e}")

    @ErrorHandler.log_exceptions
    def load_template(self, filename):
        """Load an HTML template from the templates directory."""
        base_dir = os.path.dirname(__file__)
        template_dir = os.path.join(base_dir, '..', 'templates')
        path = os.path.join(template_dir, filename)
        return self.read_file(path, file_type='template')

    @ErrorHandler.log_exceptions
    def load_and_render_template(self, template_name, **kwargs):
        """Load and populate the HTML template."""
        template_content = self.load_template(template_name)
        try:
            template = Template(template_content)
            return template.render(**kwargs)
        except Exception as e:
            ErrorHandler.log_and_raise_error(ValueError, f"Error rendering template '{template_name}': {e}")

    @ErrorHandler.log_exceptions
    def load_yaml(self, config_path):
        """Load and parse YAML thresholds config file."""
        content = self.read_file(config_path, file_type='config file')
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            ErrorHandler.log_and_raise_error(ValueError, f"Error parsing YAML file '{config_path}': {e}")