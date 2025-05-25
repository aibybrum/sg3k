import ipywidgets as widgets

from helpers import *
from utils import ErrorHandler
from .widget_helper import WidgetHelper
from IPython.display import display
from sg3k_swoop import *


class VisualizationWidgets(WidgetHelper):
    def __init__(self, jump_df, config_manager, exit_viz=None, landing_viz=None, landing_service=None, file_helper=None):
        self._file_helper = file_helper or FileHelper()
        self._exit_viz = exit_viz or ExitVisualizations(jump_df, config_manager)
        self._landing_viz = landing_viz or LandingVisualizations(jump_df, config_manager)
        self._landing_service = landing_service or LandingService(jump_df, config_manager)
        self._visualization_config = self._file_helper.load_yaml("../config/visualization_config.yaml")

    def _get_visualization_config(self, key):
        """Retrieve visualization configuration by key."""
        return self._visualization_config.get("visualizations", {}).get(key, {})

    def _load_template(self, title, description, details):
        """Load and populate the HTML template."""
        return self._file_helper.load_and_render_template(
            "visualization_template.html",
            title=title,
            description=description,
            details=details
        )

    def _display_visualization(self, title, description, details, interactive_plot, selectors):
        """Helper to display the visualization with tabs."""
        description_text = self._load_template(title, description, details)
        description_tab = self.create_html_label(description_text)
        settings_tab = widgets.VBox([widgets.HBox(selectors)])
        tab = self.create_tab(description_tab, settings_tab, tab_titles=["Description", "Settings"])
        display(tab, interactive_plot)

    def _create_visualization(self, title, description, details, update_plot_func, selectors):
        """Generic method to create and display a visualization."""
        interactive_plot = widgets.interactive_output(update_plot_func, selectors)
        selector_boxes = self.create_selector_boxes(selectors)
        self._display_visualization(title, description, details, interactive_plot, selector_boxes)

    @ErrorHandler.log_exceptions
    def exit_overview(self):
        """Display the exit overview visualization."""
        config = self._get_visualization_config("exit_overview")
        title = config.get("title", "Exit Overview")
        description = config.get("description", "")
        details = config.get("details", [])

        parameter_options = ['Elevation', 'Vertical speed', 'Glide ratio', 'Horizontal speed', 'Dive angle']
        parameter_selector = self.create_select_multiple(parameter_options, ['Elevation', 'Vertical speed'])
        x_axis_selector = self.create_dropdown(['Horizontal distance', 'Time', 'Distance'], 'Horizontal distance')

        def update_plot(parameters, x_axis):
            fig = self._exit_viz.plt_overview(list(parameters), x_axis)
            display(fig)

        self._create_visualization(title, description, details, update_plot, {
            "parameters": parameter_selector,
            "x_axis": x_axis_selector
        })

    @ErrorHandler.log_exceptions
    def landing_overview(self):
        """Display the landing overview visualization."""
        config = self._get_visualization_config("landing_overview")
        title = config.get("title", "Landing Overview")
        description = config.get("description", "")
        details = config.get("details", [])

        parameter_options = ['Elevation', 'Vertical speed', 'Glide ratio', 'Horizontal speed', 'Dive angle']
        parameter_selector = self.create_select_multiple(parameter_options, parameter_options)
        key_events = tuple(self._landing_service.get_key_events()['landing'].keys())
        key_events_selector = self.create_select_multiple(key_events, key_events)
        x_axis_selector = self.create_dropdown(['Horizontal distance', 'Time', 'Distance'], 'Horizontal distance')

        def update_plot(parameters, x_axis, key_events):
            fig = self._landing_viz.plt_overview(list(parameters), x_axis, list(key_events))
            display(fig)

        self._create_visualization(title, description, details, update_plot, {
            "parameters": parameter_selector,
            "key_events": key_events_selector,
            "x_axis": x_axis_selector
        })

    @ErrorHandler.log_exceptions
    def horizontal_speed(self):
        """Display the horizontal speed visualization."""
        config = self._get_visualization_config("horizontal_speed")
        title = config.get("title", "Horizontal Speed")
        description = config.get("description", "")
        details = config.get("details", [])

        x_axis_selector = self.create_dropdown(['Horizontal distance', 'Time', 'Distance'], 'Horizontal distance')

        def update_plot(x_axis):
            fig = self._landing_viz.plt_speed(x_axis)
            display(fig)

        self._create_visualization(title, description, details, update_plot, {"x_axis": x_axis_selector})

    @ErrorHandler.log_exceptions
    def side_view(self):
        """Display the side view visualization."""
        config = self._get_visualization_config("side_view")
        title = config.get("title", "Side View Of Flight Path")
        description = config.get("description", "")
        details = config.get("details", [])

        key_events = self._landing_service.get_filtered_key_events(
            EventMarkerHelper.get_event_keys_side_view().keys(), event_type='landing'
        )
        key_events_selector = self.create_select_multiple(key_events, key_events)
        x_axis_selector = self.create_dropdown(['Horizontal distance', 'Time', 'Distance'], 'Horizontal distance')

        def update_plot(x_axis, key_events):
            fig = self._landing_viz.plt_side_view(x_axis, list(key_events))
            display(fig)

        self._create_visualization(title, description, details, update_plot, {
            "key_events": key_events_selector,
            "x_axis": x_axis_selector
        })

    @ErrorHandler.log_exceptions
    def overhead_view(self):
        """Display the overhead view visualization."""
        config = self._get_visualization_config("overhead_view")
        title = config.get("title", "Overhead View Of Flight Path")
        description = config.get("description", "")
        details = config.get("details", [])

        key_events = self._landing_service.get_filtered_key_events(
            EventMarkerHelper.get_event_keys_overhead().keys(), event_type='landing'
        )
        key_events_selector = self.create_select_multiple(key_events, key_events)

        def update_plot(key_events):
            fig = self._landing_viz.plt_overhead(list(key_events))
            display(fig)

        self._create_visualization(title, description, details, update_plot, {"key_events": key_events_selector})

    @ErrorHandler.log_exceptions
    def map_2d(self):
        """Display the 2D map visualization."""
        config = self._get_visualization_config("map_2d")
        title = config.get("title", "2D Map")
        description = config.get("description", "")
        details = config.get("details", [])

        key_events = self._landing_service.get_filtered_key_events(
            EventMarkerHelper.get_event_keys_2d_map().keys(), event_type='pattern'
        )
        key_events_selector = self.create_select_multiple(key_events, key_events)

        def update_plot(key_events):
            fig = self._landing_viz.plt_2d_map(list(key_events))
            display(fig)

        self._create_visualization(title, description, details, update_plot, {"key_events": key_events_selector})

    @ErrorHandler.log_exceptions
    def map_3d(self):
        """Display the 3D map visualization."""
        config = self._get_visualization_config("map_3d")
        title = config.get("title", "3D Map")
        description = config.get("description", "")
        details = config.get("details", [])

        key_events = tuple(self._landing_service.get_key_events()['landing'].keys())
        key_events_selector = self.create_select_multiple(key_events, key_events)

        def update_plot(key_events):
            fig = self._landing_viz.plt_3d_map(list(key_events))
            display(fig)

        self._create_visualization(title, description, details, update_plot, {"key_events": key_events_selector})
