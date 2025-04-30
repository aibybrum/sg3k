import os

from utils import ErrorHandler


class FileValidator:
    @staticmethod
    def validate_file_exists(file_path: str, file_type: str = "file"):
        """Ensure the file exists or raise a FileNotFoundError with context."""
        if not os.path.exists(file_path):
            ErrorHandler.log_and_raise_error(FileNotFoundError, f"The {file_type} at '{file_path}' is not found. Ensure the path is correct.")