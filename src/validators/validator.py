from .dataframe_validator import DataFrameValidator
from .event_validator import EventValidator
from .file_validator import FileValidator
from .metric_validator import MetricValidator
from .threshold_validator import ThresholdValidator
from .token_validator import TokenValidator
from .config_validator import ConfigValidator
from .config_widgets_validator import ConfigWidgetsValidator


class Validator():
    def __init__(self):
        self.dataframe = DataFrameValidator()
        self.event = EventValidator()
        self.file = FileValidator()
        self.metric = MetricValidator()
        self.thresholds = ThresholdValidator()
        self.token = TokenValidator()
        self.config = ConfigValidator()
        self.config_widgets = ConfigWidgetsValidator()