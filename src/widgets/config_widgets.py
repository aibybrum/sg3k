import ipywidgets as widgets
from IPython.display import display, HTML
from .widget_helper import WidgetHelper
from .config_manager_handler import ConfigManagerHandler
from .dataset_handler import DatasetHandler
from helpers.file_helper import FileHelper
from utils import ErrorHandler


class ConfigWidgets(WidgetHelper):
    DEFAULTS = {
        'speed_metric': 'km/u',
        'distance_metric': 'm',
        'is_toggle_search': True,
        'is_front_riser': False,
        'point_after_initiation_visibility': False,
        'point_after_initiation': 3,
        'pattern_elevations_downwind': 1400,
        'pattern_elevations_base_visibility': True,
        'pattern_elevations_base': 1100,
        'dynamic_dropzone_elevation': True,
        'dropzone_elevation': None,
    }

    def __init__(self, defaults=None):
        self._defaults = {**self.DEFAULTS, **(defaults or {})}
        self._file_helper = FileHelper()
        self._config_manager_handler = ConfigManagerHandler()
        self._dataset_handler = DatasetHandler()
        self._widgets = {}
        self._initialize_ui()
        self._initialize_config_manager()

    @ErrorHandler.log_exceptions
    def _initialize_ui(self):
        """Initialize the user interface."""
        self._display_alert_styles()
        self._create_widgets()
        self._add_observers()
        self._create_tabs()

    @ErrorHandler.log_exceptions
    def _initialize_config_manager(self):
        """Initialize the configuration manager."""
        self._config_manager_handler.create_config_manager(self._widgets)
        self._config_manager_handler.validate_config_manager()

    def _display_alert_styles(self):
        """Display custom alert styles."""
        alert_styles_html = self._file_helper.load_template('alert_styles.html')
        display(HTML(alert_styles_html))

    def _create_widgets(self):
        """Create and initialize widgets."""
        # Dropdowns
        self._widgets['speed_metric'] = self.create_dropdown(['km/u', 'mph'], self._defaults['speed_metric'])
        self._widgets['distance_metric'] = self.create_dropdown(['m', 'ft'], self._defaults['distance_metric'])

        # Checkboxes
        self._widgets['is_toggle_search'] = self.create_checkbox(self._defaults['is_toggle_search'], description="Toggle Search:")
        self._widgets['is_front_riser'] = self.create_checkbox(self._defaults['is_front_riser'], description="Front Riser:", disabled=True)
        self._widgets['point_after_initiation_visibility'] = self.create_checkbox(
            self._defaults['point_after_initiation_visibility'], description="Show Point After Initiation"
        )
        self._widgets['pattern_elevations_base_visibility'] = self.create_checkbox(
            self._defaults['pattern_elevations_base_visibility'], description="Show Base Elevation"
        )
        self._widgets['dynamic_dropzone_elevation'] = self.create_checkbox(
            self._defaults['dynamic_dropzone_elevation'], description="Set Dynamically"
        )

        # Float and Int Text Inputs
        self._widgets['point_after_initiation'] = self.create_float_text(self._defaults['point_after_initiation'])
        self._widgets['point_after_initiation'].layout.display = 'none'
        self._widgets['pattern_elevations_downwind'] = self.create_int_text(self._defaults['pattern_elevations_downwind'])
        self._widgets['pattern_elevations_base'] = self.create_int_text(self._defaults['pattern_elevations_base'])
        self._widgets['dropzone_elevation'] = self.create_float_text(self._defaults['dropzone_elevation'])
        self._widgets['dropzone_elevation'].layout.display = 'none'

        # File Upload Widgets
        uploader_label_html = self._file_helper.load_template('uploader_label.html')
        self._widgets['uploader_label'] = self.create_html_label(uploader_label_html)
        self._widgets['uploader'] = self.create_widget(
            widgets.FileUpload,
            accept='*.csv',
            multiple=False,
            layout=widgets.Layout(margin='10px 0 0 0px', width='100%', height='35px')
        )
        self._widgets['upload_message'] = self.create_html_label("", bold=False, margin='15px 0 0 0')
        self._widgets['error_message'] = self.create_html_label("", bold=False, margin='15px 0 0 0')

    def _add_observers(self):
        """Add observers to widgets."""
        self._widgets['uploader'].observe(self._on_file_upload, names='value')
        self._widgets['dynamic_dropzone_elevation'].observe(self._toggle_dropzone_elevation_visibility, names='value')
        self._widgets['dynamic_dropzone_elevation'].observe(self._on_file_upload, names='value')
        self._widgets['dropzone_elevation'].observe(self._on_file_upload, names='value')

        self._widgets['point_after_initiation_visibility'].observe(self._toggle_point_after_initiation_visibility, names='value')
        self._widgets['pattern_elevations_base_visibility'].observe(self._toggle_pattern_elevations_base_visibility, names='value')

        widgets_to_observe = [
            self._widgets['speed_metric'],
            self._widgets['distance_metric'],
            self._widgets['is_toggle_search'],
            self._widgets['is_front_riser'],
            self._widgets['point_after_initiation'],
            self._widgets['pattern_elevations_downwind'],
            self._widgets['pattern_elevations_base'],
        ]
        for widget in widgets_to_observe:
            widget.observe(self._update_config_manager, names='value')

    def _toggle_dropzone_elevation_visibility(self, change):
        """Toggle the visibility of the dropzone elevation widget."""
        self._widgets['dropzone_elevation'].layout.display = 'none' if self._widgets['dynamic_dropzone_elevation'].value else ''

    def _toggle_point_after_initiation_visibility(self, change):
        """Toggle the visibility of the point after initiation widget."""
        self._widgets['point_after_initiation'].layout.display = '' if self._widgets['point_after_initiation_visibility'].value else 'none'

    def _toggle_pattern_elevations_base_visibility(self, change):
        """Toggle the visibility of the pattern elevations base widget."""
        self._widgets['pattern_elevations_base'].layout.display = '' if self._widgets['pattern_elevations_base_visibility'].value else 'none'

    def _on_file_upload(self, change):
        """Handle file upload and dataset creation."""
        try:
            dropzone_elevation = None if self._widgets['dynamic_dropzone_elevation'].value else self._widgets['dropzone_elevation'].value
            self._dataset_handler.create_dataset(self._widgets['uploader'], dropzone_elevation)
            dataset_name = self._dataset_handler.get_dataset_name()
            self._widgets['upload_message'].value = (
                f'<div class="alert alert-success" role="alert">'
                f'Dataset "{dataset_name}" created successfully.</div>'
            )
        except Exception as e:
            self._widgets['upload_message'].value = (
                f'<div class="alert alert-danger" role="alert">Error: {e}</div>'
            )

    def _update_config_manager(self, change):
        """Update the configuration manager."""
        try:
            self._config_manager_handler.create_config_manager(self._widgets)
            self._config_manager_handler.validate_config_manager()
            self._widgets['error_message'].value = ''
        except Exception as e:
            self._widgets['error_message'].value = f'<div class="alert alert-danger" role="alert">{e}</div>'

    def _create_tabs(self):
        """Create and display tabs."""
        file_upload_column = widgets.VBox([
            self._widgets['uploader_label'],
            self._widgets['uploader'],
            self._widgets['upload_message']
        ], layout=widgets.Layout(width='25%'))

        settings_columns = widgets.HBox([
            widgets.VBox([
                self.create_labeled_widget("Dropzone Elevation:", self._widgets['dynamic_dropzone_elevation']),
                self._widgets['dropzone_elevation'],
                self.create_labeled_widget("Speed Metric:", self._widgets['speed_metric']),
                self.create_labeled_widget("Distance Metric:", self._widgets['distance_metric'])
            ],layout=widgets.Layout(margin='10px 0 0 0')),
            widgets.VBox([
                self.create_labeled_widget("Point After Initiation:", self._widgets['point_after_initiation_visibility']),
                self._widgets['point_after_initiation'],
                self.create_labeled_widget("Downwind Elevation:", self._widgets['pattern_elevations_downwind']),
                self.create_labeled_widget("Base Elevation:", self._widgets['pattern_elevations_base_visibility']),
                self._widgets['pattern_elevations_base']
            ], layout=widgets.Layout(margin='10px 0 0 15px')),
            widgets.VBox([
                self.create_labeled_widget("Toggle Search:", self._widgets['is_toggle_search']),
                self.create_labeled_widget("Front Riser:", self._widgets['is_front_riser']),
                self._widgets['error_message']
            ], layout=widgets.Layout(margin='10px 0 0 15px'))
        ], layout=widgets.Layout(width='75%', margin='0 0 0 25px'))

        config_widgets = widgets.HBox([file_upload_column, settings_columns], layout=widgets.Layout(width='100%', justify_content='flex-start'))

        description_html = self._file_helper.load_template('config_description.html')
        description_text = widgets.HTML(value=description_html)

        tab = self.create_tab(config_widgets, description_text, tab_titles=["Configuration", "Description"])
        display(tab)

    @property
    def config_manager(self):
        return self._config_manager_handler.config_manager

    @property
    def jump_df(self):
        return self._dataset_handler.jump_df