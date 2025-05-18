import tempfile
import nbimporter
from sg3k_dataset import DatasetService
from validators import Validator


class DatasetHandler:
    def __init__(self, validator=None):
        self._validator = validator or Validator()
        self._jump_df = None
        self._dataset_service = None

    def create_dataset(self, uploader, dropzone_elevation):
        """Create a dataset from the uploaded file."""
        if not uploader.value:
            raise ValueError("No file uploaded.")

        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploader.value[0]['content'])
                tmp_file_path = tmp_file.name

            self._dataset_service = DatasetService(track_file=tmp_file_path, sensor_file=None, dropzone_elevation=dropzone_elevation)
            self._jump_df = self._dataset_service.create_jump_data()
        except Exception as e:
            raise ValueError(f"Error processing file: {e}")
        
    def get_dataset_name(self):
        """Get the name of the dataset"""
        if not self._dataset_service:
            raise ValueError("Dataset has not been created yet")
        return self._dataset_service.get_name()

    @property
    def jump_df(self):
        return self._jump_df