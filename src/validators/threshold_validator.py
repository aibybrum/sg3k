from utils import ErrorHandler


class ThresholdValidator:
    @staticmethod
    def validate_thresholds(thresholds):
        """Validate the thresholds configuration to ensure all required keys are present."""
        required_keys = {
            'landing': {'init_turn', 'toggle_search', 'front_riser', 'rollout', 'stop'},
            'exit': {'elevation', 'horz_speed', 'vert_speed'},
            'pond': {'horz_speed'}
        }

        for category, keys in required_keys.items():
            if category not in thresholds:
                ErrorHandler.log_and_raise_error(ValueError, f"Missing category '{category}' in thresholds.")
            missing_keys = keys - thresholds[category].keys()
            if missing_keys:
                ErrorHandler.log_and_raise_error(ValueError, f"Missing keys in '{category}' thresholds: {', '.join(missing_keys)}")
            for key, threshold in thresholds[category].items():
                if isinstance(threshold, dict):
                    for subkey, subthreshold in threshold.items():
                        ThresholdValidator.validate_threshold(subthreshold, subkey, key, category)
                else:
                    ThresholdValidator.validate_threshold(threshold, key, category)

    @staticmethod
    def validate_threshold(threshold, key, category, subkey=None):
        required_attributes = {'thres_peaks', 'min_dist_peaks', 'thres_lows', 'min_dist_lows'}
        if not required_attributes.issubset(threshold.__dict__.keys()):
            if subkey:
                ErrorHandler.log_and_raise_error(TypeError, f"Subthreshold for '{subkey}' in '{key}' must have attributes {required_attributes}.")
            else:
                ErrorHandler.log_and_raise_error(TypeError, f"Threshold for '{key}' in '{category}' must have attributes {required_attributes}.")

    @staticmethod
    def validate_peaks_lows(peaks, lows, metric_name, validate_peaks=True, validate_lows=True):
        """Validate the detected peaks and lows based on the provided flags."""
        if validate_peaks and peaks.size == 0:
            ErrorHandler.log_and_raise_error(ValueError, f"No peaks found in the {metric_name} metric")
        if validate_lows and lows.size == 0:
            ErrorHandler.log_and_raise_error(ValueError, f"No lows found in the {metric_name} metric")