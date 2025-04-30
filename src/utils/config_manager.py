from validators import Validator


class ConfigManager:
    def __init__(self, pattern_elevations, is_toggle_search=True, is_front_riser=True, distance_metric='m', speed_metric='km/u', point_after_initiation=3, validator=None):
        self._pattern_elevations = pattern_elevations or {'downwind': 1500, 'base': None}
        self._is_toggle_search = is_toggle_search
        self._is_front_riser = is_front_riser
        self._distance_metric = distance_metric
        self._speed_metric = speed_metric
        self._point_after_initiation = point_after_initiation
        self._validator = validator or Validator()
        
        self._validator.config.validate_pattern_elevations(self._pattern_elevations)
        self._validator.config.validate_point_after_initiation(self._point_after_initiation)

    @property
    def pattern_elevations(self):
        return self._pattern_elevations

    @property
    def is_toggle_search(self):
        return self._is_toggle_search

    @property
    def is_front_riser(self):
        return self._is_front_riser

    @property
    def distance_metric(self):
        return self._distance_metric

    @property
    def speed_metric(self):
        return self._speed_metric

    @property
    def point_after_initiation(self):
        return self._point_after_initiation