import tempfile
import nbimporter
import ipywidgets as widgets

from utils import ConfigManager
from helpers import WidgetHelper, FileHelper
from validators import Validator
from sg3k_dataset import DatasetService
from IPython.display import display, HTML


class ConfigWidgets(WidgetHelper):
    def __init__(self, validator=None):
        self._jump_df = None
        self._config_manager = None
        self._validator = validator or Validator()
        self._file_helper = FileHelper()
        self._initialize_ui()
        self._initialize_config_manager()

    def _initialize_ui(self):
        """Initialize the user interface."""
        self._display_alert_styles()
        self._create_widgets()
        self._add_observers()
        self._create_tabs()

    def _display_alert_styles(self):
        """Display custom alert styles for success and error messages."""
        alert_styles_html = self._file_helper.load_template('alert_styles.html')
        display(HTML(alert_styles_html))

    def _create_widgets(self):
        """Create and initialize all widgets."""
        # Metric widgets
        self._speed_metric_label, self._speed_metric_widget = self._create_labeled_dropdown("Speed Metric:", ['km/u', 'mph'], 'km/u')
        self._distance_metric_label, self._distance_metric_widget = self._create_labeled_dropdown("Distance Metric:", ['m', 'ft'], 'm')
        # Toggle widgets
        self._is_toggle_search_label, self._is_toggle_search_widget = self._create_labeled_checkbox("Toggle Search:", True)
        self._is_front_riser_label, self._is_front_riser_widget = self._create_labeled_checkbox("Front Riser:", False, disabled=True)
        # Point After Initiation widgets
        self._point_after_initiation_label, self._point_after_initiation_visibility_widget = self._create_labeled_checkbox(
            "Point After Initiation:", False, description="Show Point After Initiation", disabled=False
        )
        self._point_after_initiation_widget = self._create_float_text(3)
        self._point_after_initiation_widget.layout.display = 'none'
        # Pattern Elevations widgets
        self._pattern_elevations_downwind_label, self._pattern_elevations_downwind_widget = self._create_labeled_int_text("Downwind Elevation:", 1400)
        self._pattern_elevations_base_label, self._pattern_elevations_base_visibility_widget = self._create_labeled_checkbox(
            "Base Elevation:", True, description="Show Base Elevation"
        )
        self._pattern_elevations_base_widget = self._create_int_text(1100)
        # Dropzone Elevation widgets
        self._dropzone_elevation_label, self._dynamic_dropzone_elevation_widget = self._create_labeled_checkbox(
            "Dropzone Elevation:", True, description="Set Dynamically"
        )
        self._dropzone_elevation_widget = self._create_float_text(None)
        self._dropzone_elevation_widget.layout.display = 'none'
        # File uploader
        uploader_label_html = self._file_helper.load_template('uploader_label.html')
        self._uploader_label = self._create_html_label(uploader_label_html)
        self._uploader = widgets.FileUpload(
            accept='*.csv', multiple=False, layout=widgets.Layout(margin='10px 0 0 0px', width='100%', height='35px')
        )
        self._upload_message = widgets.HTML(layout=widgets.Layout(margin='10px 0 0 0'))
        self._error_message = widgets.HTML(layout=widgets.Layout(margin='10px 0 0 15px'))

    def _add_observers(self):
        """Add observers to widgets."""
        self._uploader.observe(self.create_dataset, names='value')
        self._dynamic_dropzone_elevation_widget.observe(self.create_dataset, names='value')
        self._dynamic_dropzone_elevation_widget.observe(self._toggle_dropzone_elevation_visibility, names='value')
        self._dropzone_elevation_widget.observe(self.create_dataset, names='value')

        self._point_after_initiation_visibility_widget.observe(self._toggle_point_after_initiation_visibility, names='value')
        self._pattern_elevations_base_visibility_widget.observe(self._toggle_pattern_elevations_base_visibility, names='value')

        widgets_to_observe = [
            self._speed_metric_widget,
            self._distance_metric_widget,
            self._is_toggle_search_widget,
            self._is_front_riser_widget,
            self._point_after_initiation_widget,
            self._pattern_elevations_downwind_widget,
            self._pattern_elevations_base_widget,
        ]
        for widget in widgets_to_observe:
            widget.observe(self._update_config_manager, names='value')

    def _toggle_dropzone_elevation_visibility(self, change):
        """Toggle the visibility of the dropzone elevation widget."""
        self._dropzone_elevation_widget.layout.display = 'none' if self._dynamic_dropzone_elevation_widget.value else ''

    def _toggle_point_after_initiation_visibility(self, change):
        """Toggle the visibility of the point after initiation widget."""
        self._point_after_initiation_widget.layout.display = '' if self._point_after_initiation_visibility_widget.value else 'none'

    def _toggle_pattern_elevations_base_visibility(self, change):
        """Toggle the visibility of the pattern elevations base widget."""
        self._pattern_elevations_base_widget.layout.display = '' if self._pattern_elevations_base_visibility_widget.value else 'none'

    def create_dataset(self, change):
        """Create a dataset from the uploaded file."""
        dropzone_elevation = None if self._dynamic_dropzone_elevation_widget.value else self._dropzone_elevation_widget.value

        if self._uploader.value:
            try:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(self._uploader.value[0].content)
                    tmp_file_path = tmp_file.name

                dataset_service = DatasetService(track_file=tmp_file_path, sensor_file=None, dropzone_elevation=dropzone_elevation)
                self._jump_df = dataset_service.create_jump_data()
                self._upload_message.value = f'<div class="alert alert-success" role="alert">File uploaded and dataset {dataset_service.get_name()} created successfully.</div>'
                self._validator.config_widgets.validate_jump_df(self)
            except Exception as e:
                self._upload_message.value = f'<div class="alert alert-danger" role="alert">Error processing file: {e}</div>'
        else:
            self._upload_message.value = '<div class="alert alert-danger" role="alert">Please upload a file.</div>'

    def _initialize_config_manager(self):
        """Initialize the configuration manager."""
        self._config_manager = self._create_config_manager()
        self._validate_config_manager()

    def _create_config_manager(self):
        """Create a configuration manager."""
        point_after_initiation = self._point_after_initiation_widget.value if self._point_after_initiation_visibility_widget.value else None
        pattern_elevations_base = self._pattern_elevations_base_widget.value if self._pattern_elevations_base_visibility_widget.value else None

        try:
            config_manager = ConfigManager(
                speed_metric=self._speed_metric_widget.value,
                distance_metric=self._distance_metric_widget.value,
                is_toggle_search=self._is_toggle_search_widget.value,
                is_front_riser=self._is_front_riser_widget.value,
                point_after_initiation=point_after_initiation,
                pattern_elevations={
                    'downwind': self._pattern_elevations_downwind_widget.value,
                    'base': pattern_elevations_base
                }
            )
            self._error_message.value = ''
        except ValueError as e:
            self._error_message.value = f'<div class="alert alert-danger" role="alert">{e}</div>'

        return config_manager

    def _update_config_manager(self, change):
        """Update the configuration manager."""
        self._config_manager = self._create_config_manager()
        self._validate_config_manager()

    def _validate_config_manager(self):
        """Validate the configuration manager."""
        try:
            self._validator.config_widgets.validate_config_manager(self)
        except Exception as e:
            self._error_message.value = f'<div class="alert alert-danger" role="alert">{e}</div>'

    def _create_tabs(self):
        """Create and display the configuration tabs."""
        file_upload_column = widgets.VBox([
            self._uploader_label,
            self._uploader,
            self._upload_message
        ], layout=widgets.Layout(width='25%'))

        left_column = widgets.VBox([
            widgets.VBox([self._dropzone_elevation_label, self._dynamic_dropzone_elevation_widget, self._dropzone_elevation_widget]),
            widgets.VBox([self._speed_metric_label, self._speed_metric_widget], layout=widgets.Layout(margin='5px 0 0 0px')),
            widgets.VBox([self._distance_metric_label, self._distance_metric_widget], layout=widgets.Layout(margin='5px 0 0 0px'))
        ])

        middle_column = widgets.VBox([
            widgets.VBox([self._point_after_initiation_label, self._point_after_initiation_visibility_widget, self._point_after_initiation_widget], layout=widgets.Layout(margin='0 0 0 15px')),
            widgets.VBox([self._pattern_elevations_downwind_label, self._pattern_elevations_downwind_widget], layout=widgets.Layout(margin='5px 0 0 15px')),
            widgets.VBox([self._pattern_elevations_base_label, self._pattern_elevations_base_visibility_widget, self._pattern_elevations_base_widget], layout=widgets.Layout(margin='5px 0 0 15px'))
        ])

        right_column = widgets.VBox([
            widgets.VBox([self._is_toggle_search_label, self._is_toggle_search_widget], layout=widgets.Layout(margin='0 0 0 15px')),
            widgets.VBox([self._is_front_riser_label, self._is_front_riser_widget], layout=widgets.Layout(margin='0 0 0 15px')),
            self._error_message
        ])

        settings_columns = widgets.HBox([
            left_column,
            middle_column,
            right_column
        ], layout=widgets.Layout(width='75%', margin='0 0 0 25px'))

        config_widgets = widgets.HBox([
            file_upload_column,
            settings_columns
        ], layout=widgets.Layout(width='100%', justify_content='flex-start'))

        description_html = self._file_helper.load_template('config_description.html')
        description_text = widgets.HTML(value=(description_html))

        tab = widgets.Tab()
        tab.children = [config_widgets, widgets.VBox([description_text])]
        tab.set_title(0, 'Configuration')
        tab.set_title(1, 'Description')

        display(tab)

    @property
    def config_manager(self):
        """Get the configuration manager."""
        return self._config_manager

    @property
    def jump_df(self):
        """Get the jump data frame."""
        return self._jump_df

    @property
    def uploader(self):
        """Get the file uploader widget."""
        return self._uploader