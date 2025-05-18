from utils import ConfigManager
from validators import Validator


class ConfigManagerHandler:
    def __init__(self, validator=None):
        self._validator = validator or Validator()
        self._config_manager = None

    def create_config_manager(self, widgets):
        """Create a configuration manager using widget values."""
        try:
            self._config_manager = ConfigManager(
                speed_metric=widgets['speed_metric'].value,
                distance_metric=widgets['distance_metric'].value,
                is_toggle_search=widgets['is_toggle_search'].value,
                is_front_riser=widgets['is_front_riser'].value,
                point_after_initiation=widgets['point_after_initiation'].value
                if widgets['point_after_initiation_visibility'].value else None,
                pattern_elevations={
                    'downwind': widgets['pattern_elevations_downwind'].value,
                    'base': widgets['pattern_elevations_base'].value
                    if widgets['pattern_elevations_base_visibility'].value else None
                }
            )
        except ValueError as e:
            raise ValueError(f"Error creating ConfigManager: {e}")

    def validate_config_manager(self):
        """Validate the configuration manager."""
        if not self._config_manager:
            raise ValueError("Configuration manager is not set.")
        self._validator.config_widgets.validate_config_manager(self)

    @property
    def config_manager(self):
        return self._config_manager