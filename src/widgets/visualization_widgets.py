import ipywidgets as widgets

from helpers import *
from .widget_helper import WidgetHelper
from IPython.display import display
from sg3k_swoop import *


class VisualizationWidgets(WidgetHelper):
    def __init__(self, jump_df, config_manager, exit_viz=None, landing_viz=None, landing_service=None):
        self._file_helper = FileHelper()
        self._exit_viz = exit_viz or ExitVisualizations(jump_df, config_manager)
        self._landing_viz = landing_viz or LandingVisualizations(jump_df, config_manager)
        self._landing_service = landing_service or LandingService(jump_df, config_manager)

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
        settings_tab = widgets.VBox(selectors)
        tab = self.create_tab(description_tab, settings_tab, tab_titles=["Description", "Settings"])
        display(tab, interactive_plot)

    def exit_overview(self):
        """Display the exit overview visualization."""
        parameter_options = ['Elevation', 'Vertical speed', 'Glide ratio', 'Horizontal speed', 'Dive angle']
        parameter_selector = self.create_select_multiple(parameter_options, ['Elevation', 'Vertical speed'])
        x_axis_selector = self.create_dropdown(['Horizontal distance', 'Time', 'Distance'], 'Horizontal distance')

        def update_plot(parameters, x_axis):
            fig = self._exit_viz.plt_overview(list(parameters), x_axis)
            display(fig)

        interactive_plot = widgets.interactive_output(update_plot, {'parameters': parameter_selector, 'x_axis': x_axis_selector})

        title = "Exit Overview"
        description = "This visualization provides an overview of data from a skydive, starting when the jumper exited the plane."
        details = [
            {"label": "Metrics", "content": "Elevation, horizontal speed, vertical speed, dive angle, and glide ratio."},
            {"label": "X-axis", "content": "Options include Horizontal distance, Time, and Distance."}
        ]

        parameter_box = self.create_labeled_widget("Parameters", parameter_selector)
        x_axis_box = self.create_labeled_widget("X-axis", x_axis_selector, margin="0 0 0 10px")
        self._display_visualization(title, description, details, interactive_plot, [widgets.HBox([parameter_box, x_axis_box])])

    def landing_overview(self):
        """Display the landing overview visualization."""
        parameter_options = ['Elevation', 'Vertical speed', 'Glide ratio', 'Horizontal speed', 'Dive angle']
        parameter_selector = self.create_select_multiple(parameter_options, parameter_options)
        key_events = tuple(self._landing_service.get_key_events()['landing'].keys())
        key_events_selector = self.create_select_multiple(key_events, key_events)
        x_axis_selector = self.create_dropdown(['Horizontal distance', 'Time', 'Distance'], 'Horizontal distance')

        def update_plot(parameters, x_axis, key_events):
            fig = self._landing_viz.plt_overview(list(parameters), x_axis, list(key_events))
            display(fig)

        interactive_plot = widgets.interactive_output(update_plot, {
            'parameters': parameter_selector,
            'x_axis': x_axis_selector,
            'key_events': key_events_selector
        })

        title = "Landing Overview"
        description = (
            "This visualization offers a comprehensive overview of your skydive swoop landing, "
            "providing valuable insights into your maneuver."
        )
        details = [
            {"label": "Metrics", "content": "Elevation, horizontal speed, vertical speed, dive angle, and glide ratio."},
            {"label": "Events Indicators", "content": "Vertical lines provide additional information about certain events."}
        ]

        parameter_box = self.create_labeled_widget("Parameters", parameter_selector)
        key_events_box = self.create_labeled_widget("Key Events", key_events_selector, margin="0 0 0 10px")
        x_axis_box = self.create_labeled_widget("X-axis", x_axis_selector, margin="0 0 0 10px")
        self._display_visualization(title, description, details, interactive_plot, [widgets.HBox([parameter_box, key_events_box, x_axis_box])])

    def horizontal_speed(self):
        """Display the horizontal speed visualization."""
        x_axis_selector = self.create_dropdown(['Horizontal distance', 'Time', 'Distance'], 'Horizontal distance')

        def update_plot(x_axis):
            fig = self._landing_viz.plt_speed(x_axis)
            display(fig)

        interactive_plot = widgets.interactive_output(update_plot, {'x_axis': x_axis_selector})

        title = "Horizontal Speed"
        description = (
            "Understand the dynamics of your skydive swoop landing with our horizontal speed plot."
        )
        details = [
            {"label": "Speed Profile", "content": "The plot illustrates your horizontal speed, showing velocity changes."},
            {"label": "Performance Insights", "content": "Analyze speed variations to identify areas for improvement."}
        ]
        x_axis_box = self.create_labeled_widget("X-axis", x_axis_selector)
        self._display_visualization(title, description, details, interactive_plot, [widgets.HBox([x_axis_box])])

    def side_view(self):
        """Display the side view visualization."""
        key_events = self._landing_service.get_filtered_key_events(
            EventMarkerHelper.get_event_keys_side_view().keys(), event_type='landing'
        )

        key_events_selector = self.create_select_multiple(key_events, key_events)
        x_axis_selector = self.create_dropdown(['Horizontal distance', 'Time', 'Distance'], 'Horizontal distance')

        def update_plot(x_axis, key_events):
            fig = self._landing_viz.plt_side_view(x_axis, list(key_events))
            display(fig)

        interactive_plot = widgets.interactive_output(update_plot, {
            'x_axis': x_axis_selector,
            'key_events': key_events_selector
        })

        title = "Side View Of Flight Path"
        description = (
            "Examine the nuances of your skydive swoop landing with our side view plot visualization. Here’s what you’re looking at:"
        )
        details = [
            {"label": "Flight Path Profile", "content": "A profile view of your flight path, offering a clear observation of the landing’s rollout."},
            {"label": "Rollout Details", "content": "This perspective reveals the steepness of your descent and your proximity to the gate during the approach."},
            {"label": "Maneuver Altitude", "content": "Gain insight into the altitude at which you initiated your maneuver, providing valuable information for performance analysis."},
            {"label": "Event Markers", "content": "Key events are marked along your flight path."}
        ]

        key_events_box = self.create_labeled_widget("Key Events", key_events_selector)
        x_axis_box = self.create_labeled_widget("X-axis", x_axis_selector, margin="0 0 0 10px")
        self._display_visualization(title, description, details, interactive_plot, [widgets.HBox([key_events_box, x_axis_box])])

    def overhead_view(self):
        """Display the overhead view visualization."""
        key_events = self._landing_service.get_filtered_key_events(
            EventMarkerHelper.get_event_keys_overhead().keys(), event_type='landing'
        )
        key_events_selector = self.create_select_multiple(key_events, key_events)

        def update_plot(key_events):
            fig = self._landing_viz.plt_overhead(list(key_events))
            display(fig)

        interactive_plot = widgets.interactive_output(update_plot, {'key_events': key_events_selector})

        title = "Overhead View Of Flight Path"
        description = ("Gain a unique perspective on your skydive swoop landing with our normal plot visualization. Here’s what you’re seeing:")
        details = [
            {"label": "Flight Trajectory", "content": "Your flight path is plotted, giving you a bird’s-eye view of your skydive."},
            {"label": "Event Markers", "content": "Key events are marked along your flight path."}
        ]

        key_events_box = self.create_labeled_widget("Key Events", key_events_selector)
        self._display_visualization(title, description, details, interactive_plot, [widgets.HBox([key_events_box])])

    def map_2d(self):
        """Display the 2D map visualization."""
        key_events = self._landing_service.get_filtered_key_events(
            EventMarkerHelper.get_event_keys_2d_map().keys(), event_type='pattern'
        )
        key_events_selector = self.create_select_multiple(key_events, key_events)

        def update_plot(key_events):
            fig = self._landing_viz.plt_2d_map(list(key_events))
            display(fig)

        interactive_plot = widgets.interactive_output(update_plot, {'key_events': key_events_selector})

        title = "2D Map"
        description = ("Explore the intricacies of your skydive swoop landing with our detailed 2D map visualization. Here’s what you’re looking at:")
        details = [
            {"label": "Flight Path", "content": "Your flight trajectory is clearly marked on the map, giving you a top-down view of your skydive."},
            {"label": "Event Markers", "content": "Key events are marked along your flight path."}
        ]

        key_events_box = self.create_labeled_widget("Key Events", key_events_selector)
        self._display_visualization(title, description, details, interactive_plot, [widgets.HBox([key_events_box])])

    def map_3d(self):
        """Display the 3D map visualization."""
        key_events = tuple(self._landing_service.get_key_events()['landing'].keys())
        key_events_selector = self.create_select_multiple(key_events, key_events)

        def update_plot(key_events):
            fig = self._landing_viz.plt_3d_map(list(key_events))
            display(fig)

        interactive_plot = widgets.interactive_output(update_plot, {'key_events': key_events_selector})

        title = "3D Map"
        description = ("Dive into the details of your skydive swoop landing with our immersive 3D map visualization. Here’s what you’re seeing:")
        details = [
            {"label": "Flight Path", "content": "Your flight trajectory is vividly overlaid on high-resolution satellite imagery, providing a real-world context to your skydive."},
            {"label": "Altitude Representation", "content": "The altitude changes during your swoop are represented in 3D, giving you a clear view of your descent and landing approach."},
            {"label": "Interactive Exploration", "content": "Rotate, zoom, and pan the map to explore your flight from different angles and perspectives."},
            {"label": "Event Markers", "content": "Key events are marked along your flight path."}
        ]
        key_events_box = self.create_labeled_widget("Key Events", key_events_selector)
        self._display_visualization(title, description, details, interactive_plot, [widgets.HBox([key_events_box])])
