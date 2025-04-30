from utils import ErrorHandler


class ConfigValidator:
    @staticmethod
    def validate_pattern_elevations(pattern_elevations):
        """Validate the pattern elevations."""
        downwind = pattern_elevations['downwind']
        base = pattern_elevations['base']
        
        if not downwind:
            ErrorHandler.log_and_raise_error(ValueError, f"Downwind elevation cannot be empty in pattern_elevations.")
        if base is not None and downwind <= base:
            ErrorHandler.log_and_raise_error(ValueError, f"Downwind elevation must be greater than base elevation if base is specified.")

    @staticmethod
    def validate_point_after_initiation(point_after_initiation):
        """Validate the point after initiation."""
        if point_after_initiation is not None and point_after_initiation < 0:
            ErrorHandler.log_and_raise_error(ValueError, "Point after initiation can't be less than 0")