from utils import ErrorHandler


class MetricValidator:
    @staticmethod
    def validate_metric(speed_metric=None, distance_metric=None):
        """Validates if the provided metrics are in the correct format."""
        valid_speed_metrics = {'km/u', 'mph'}
        valid_distance_metrics = {'m', 'ft'}

        if speed_metric and speed_metric not in valid_speed_metrics:
            ErrorHandler.log_and_raise_error(ValueError, f"Invalid speed metric. Expected one of {valid_speed_metrics}.")
        if distance_metric and distance_metric not in valid_distance_metrics:
            ErrorHandler.log_and_raise_error(ValueError, f"Invalid distance metric. Expected one of {valid_distance_metrics}.")

    @staticmethod
    def validate_speed_type(speed_type):
        """Validates if the provided speed type is valid."""
        valid_speed_types = {'vert', 'horz'}
        if speed_type not in valid_speed_types:
            ErrorHandler.log_and_raise_error(ValueError, f"Invalid speed type. Expected one of {valid_speed_types}.")