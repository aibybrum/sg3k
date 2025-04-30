import os

from pathlib import Path
from utils import ErrorHandler
from dotenv import load_dotenv

dotenv_path = Path('./../.env')
load_dotenv(dotenv_path=dotenv_path)


class TokenValidator:
    @staticmethod
    def get_token():
        token = os.getenv("TOKEN")
        if not token:
            ErrorHandler.log_and_raise_error(ValueError, "Mapbox token not found. Please set the 'TOKEN' Environment variable.")
        return token