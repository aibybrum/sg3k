import peakutils as pu

from utils import ErrorHandler
from validators import Validator


class Threshold:
    """A class to represent threshold settings for peak and low detection."""
    def __init__(self, thres_peaks, min_dist_peaks, thres_lows, min_dist_lows, validator=None):
        self.thres_peaks = thres_peaks
        self.min_dist_peaks = min_dist_peaks
        self.thres_lows = thres_lows
        self.min_dist_lows = min_dist_lows
        self.validator = validator or Validator()

    @ErrorHandler.log_exceptions
    def detect_peaks_lows(self, metric):
        """
        Detects peaks and lows in the provided metric based on threshold values.
        """
        if metric is None or len(metric) == 0:
            ErrorHandler.log_and_raise_error(ValueError, "Input metric is empty or invalid")
        
        peaks = pu.indexes(metric, thres=self.thres_peaks, min_dist=self.min_dist_peaks)
        lows = pu.indexes(-metric, thres=self.thres_lows, min_dist=self.min_dist_lows)
        
        return peaks, lows

    def detect_and_validate_peaks_lows(self, metric, metric_name=None, validate_peaks=True, validate_lows=True):
        """
        Detects peaks and lows in the provided metric and validates based on threshold values.
        Raises ValueError if validation fails.
        """
        peaks, lows = self.detect_peaks_lows(metric)
        name = metric_name if metric_name is not None else getattr(metric, 'name', 'unknown metric')
        self.validator.thresholds.validate_peaks_lows(peaks, lows, name, validate_peaks, validate_lows)
        
        return peaks, lows