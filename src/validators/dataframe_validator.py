from utils import ErrorHandler


class DataFrameValidator:
    @staticmethod
    def validate_not_empty(df, name="DataFrame"):
        if df is None or len(df) == 0:
            ErrorHandler.log_and_raise_error(ValueError, f"{name} cannot be None or empty.")
    
    @staticmethod
    def validate_column_exists(df, column_name):
        if column_name not in df.columns:
            ErrorHandler.log_and_raise_error(ValueError, f"Column {column_name} not found in DataFrame")

    @staticmethod
    def validate_index_in_bounds(df, index, name="index"):
        if not (0 <= index < len(df)):
            ErrorHandler.log_and_raise_error(IndexError, f"{name} is out of bounds for DataFrame")