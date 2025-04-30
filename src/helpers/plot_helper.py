import logging
import plotly.graph_objects as go

from helpers import CommonPlotHelper
from validators import Validator
from utils import ErrorHandler, EventKeys


class PlotHelper(CommonPlotHelper):
    def __init__(self, validator=None):
        super().__init__()
        self._validator = validator or Validator()
        self._key_event_colors = {
            EventKeys.BASE_LEG.value: '#9370DB',         # Medium Purple
            EventKeys.TOGGLE_SEARCH.value: '#FFC107',    # Amber
            EventKeys.INIT_TURN.value: '#45A0E6',        # Light Blue
            EventKeys.MAX_HORZ_SPEED.value: '#FF9900',   # Orange
            EventKeys.MAX_VERT_SPEED.value: '#7A64FA',   # Medium Slate Blue
            EventKeys.START_ROLLOUT.value: '#32CD32',    # Lime Green
            EventKeys.STOP_ROLLOUT.value: '#FF3737',     # Red
            EventKeys.STOP_ESTIMATE.value: '#5C7AEA',    # Light Slate Blue
            EventKeys.FRONT_RISER.value: '#FF6F61',      # Coral
            EventKeys.AFTER_RISER.value: '#FFD700',      # Gold
            EventKeys.AFTER_TURN.value: '#FFD700'        # Gold
        }

    def create_scatter_trace(self, x, y, color, name='', mode='lines', hovertemplate=None, showlegend=False):
        """Creates a Plotly scatter trace with lines or markers."""
        trace_config = {
            'x': x, 'y': y, 'name': name, 'mode': mode,
            'hovertemplate': hovertemplate, 'showlegend': showlegend
        }
        if mode == 'lines':
            trace_config['line'] = dict(color=color, width=1.2)
        elif mode == 'markers':
            trace_config['marker'] = dict(color=color, size=7)
        else:
            ErrorHandler.log_and_raise_error(ValueError, "Mode must be 'lines' or 'markers'")
        return go.Scatter(**trace_config)

    def add_key_event_markers(self, fig, x_axis, y_axis, markers, key_events, showlegend=False):
        """Adds key event markers to the plot for the specified phase."""
        for event_name, label in markers.items():
            event_id = key_events.get(event_name, None)

            if event_id is not None:
                fig.add_trace(self.create_scatter_trace(
                    x=[x_axis['data'][event_id]], y=[y_axis['data'][event_id]],
                    name=label, color=self._key_event_colors.get(event_name, '#000000'), mode='markers', showlegend=showlegend
                ))

    def generate_markers(self, event_keys, key_events, y_axis, event_names, x_axis=None, legend_format="{event}: {value} {metric}"):
        """Generates legend names and markers to plot based on event keys, key events, and event names."""
        self._validator.event.validate_event_names(event_names, key_events)

        legend_names = {}
        markers_to_plot = {}

        valid_event_keys = {event.value for event in EventKeys}
        for event in event_keys.keys():
            if event not in valid_event_keys:
                raise ValueError(f"Invalid event key '{event}' found in event_keys. Please check for typos.")

        for event, axis in event_keys.items():
            if event in key_events:
                value = round(y_axis[axis]['data'][key_events[event]], 2)
                metric = y_axis[axis]['metric']
                if x_axis:
                    x_value = round(x_axis['data'][key_events[event]], 2)
                    x_metric = x_axis['metric']
                    legend_names[event] = legend_format.format(event=event.replace('_', ' '), value=value, metric=metric, x_value=x_value, x_metric=x_metric)
                else:
                    legend_names[event] = legend_format.format(event=event.replace('_', ' '), value=value, metric=metric)

        for event in event_names:
            if event in legend_names:
                markers_to_plot[event] = legend_names[event]
            else:
                logging.warning(f"Event '{event}' not found in legend names.")

        return markers_to_plot

    def plot_overview(self, df, y_axis_params, x_axis, y_axis, height=600, width=None):
        """Generates an overview plot with multiple selected metrics."""
        self._validator.dataframe.validate_not_empty(df, "DataFrame")

        if not y_axis_params:
            logging.warning("No metrics selected for visualization.")
            return go.Figure(self.empty_layout("Please select Y-axis parameters")), None

        for param in y_axis_params:
            if param not in y_axis:
                ErrorHandler.log_and_raise_error(ValueError, f"Selected metric '{param}' is not present in the Y-axis settings.")

        layout = self._generate_overview_layout(y_axis_params, x_axis, y_axis)
        traces = self._generate_overview_traces(y_axis_params, x_axis, y_axis)

        fig = go.Figure(data=traces, layout=go.Layout(**layout))
        fig.update_layout(hovermode="x unified", title_text="Overview", height=height)

        if width:
            fig.update_layout(width=width)
        return fig, x_axis['data']

    def _generate_overview_traces(self, y_axis_params, x_axis, y_axis):
        """Generates traces for the overview plot."""
        traces = []
        for i, parameter in enumerate(y_axis_params):
            trace = go.Scatter(
                x=x_axis['data'],
                y=y_axis[parameter]['data'],
                mode='lines',
                line=dict(color=y_axis[parameter]['color'], width=1.2),
                showlegend=False,
                hovertemplate=y_axis[parameter]['hovertemplate'],
                yaxis=f'y{i+1}' if i > 0 else 'y'
            )
            traces.append(trace)
        return traces

    def _generate_overview_layout(self, y_axis_params, x_axis, y_axis):
        """Generates layout for the overview plot."""
        layout = {
            'xaxis': {
                'domain': [0.06 * (len(y_axis_params) - 1), 1],
                'title': x_axis['title']
            }
        }
        for i, parameter in enumerate(y_axis_params):
            axis_name = f'yaxis{i+1}' if i > 0 else 'yaxis'
            layout[axis_name] = {
                'position': i * 0.06,
                'side': 'left',
                'title': f"{parameter} ({y_axis[parameter]['metric']})",
                'titlefont': {'size': 10, 'color': y_axis[parameter]['color']},
                'anchor': 'free', 'tickfont': {'size': 10, 'color': y_axis[parameter]['color']},
                'showgrid': False,
                'title_standoff': 0
            }
            if i > 0:
                layout[axis_name]['overlaying'] = 'y'
        return layout

    def add_vertical_lines(self, fig, x_data, event_names, key_events):
        """Adds vertical lines for key events to the plot."""
        y_position = 1
        y_offset = 0.05

        event_positions = {}
        self._validator.event.validate_event_names(event_names, key_events)

        for event_name in event_names:
            event_index = key_events.get(event_name)
            if event_index not in event_positions:
                event_positions[event_index] = []
            event_positions[event_index].append(event_name)

        for event_index in sorted(event_positions.keys()):
            names = event_positions[event_index]
            combined_label = " +<br>".join(names)
            fig.add_vline(x=x_data[event_index], line_width=1.2)
            fig.add_annotation(
                x=x_data[event_index],
                y=y_position,
                text=combined_label,
                showarrow=True,
                arrowhead=2,
                xanchor='left',
                yanchor='bottom',
                xref='x',
                yref='paper'
            )
            y_position -= y_offset
            if y_position < (1 - (0.05 * 2)):
                y_position = 1

    def create_plot(self, x_axis, y_axis, title, showlegend=True, x_slice_from=None, x_slice_to=None, y_slice_from=None, y_slice_to=None, height=550, width=None):
        """Creates a Plotly figure with the given axis settings and title."""
        fig = self.create_base_figure(title, height=height)
        
        if width:
            fig.update_layout(width=width)
        
        x_data = x_axis['data'].loc[x_slice_from:x_slice_to] if x_slice_from is not None or x_slice_to is not None else x_axis['data']
        y_data = y_axis['data'].loc[y_slice_from:y_slice_to] if y_slice_from is not None or y_slice_to is not None else y_axis['data']
        
        self.plot_data(fig, {'data': x_data, 'title': x_axis['title']}, {'data': y_data, 'title': y_axis['title'], 'color': y_axis['color'], 'hovertemplate': y_axis['hovertemplate']})
        
        fig.update_layout(
            legend=dict(yanchor="top", y=1, xanchor="right", x=1) if showlegend else {}
        )
        return fig
    
    @property
    def key_event_colors(self):
        return self._key_event_colors