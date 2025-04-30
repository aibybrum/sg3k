import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ErrorHandler:
    @staticmethod
    def log_exceptions(func):
        """Decorator to log exceptions for wrapped functions."""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                raise
        return wrapper
    
    @staticmethod
    def log_and_raise_error(exception, message):
        """Helper to log and raise an error."""
        logger.error(message)
        raise exception(message)

    @staticmethod
    def get_data_with_error_handling(estimate_func, estimate_type):
        """Helper method to get estimate data and handle errors."""
        try:
            return estimate_func()
        except ValueError as e:
            ErrorHandler.log_and_raise_error(ValueError, f"Error in {estimate_type} estimate: {str(e)}")