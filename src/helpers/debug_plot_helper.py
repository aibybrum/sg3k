import plotly.graph_objects as go

from helpers import CommonPlotHelper
from utils import ErrorHandler


class DebugPlotHelper(CommonPlotHelper):
    MARKER_PROPERTIES = {
        'peaks': {'color': 'Green', 'size': 7},
        'lows': {'color': 'Red', 'size': 7},
        'pond': {'color': 'Blue', 'size': 8}
    }

    def _add_marker_trace(self, fig, x_data, y_data, indices, color, size, row=None, col=None, showlegend=False):
        """Adds a marker trace to the figure."""
        if indices is not None and len(indices) > 0:
            trace = go.Scatter(
                x=[x_data[i] for i in indices],
                y=[y_data[i] for i in indices],
                mode='markers',
                marker=dict(size=size, color=color),
                showlegend=showlegend
            )
            if row is not None and col is not None:
                fig.add_trace(trace, row=row, col=col)
            else:
                fig.add_trace(trace)

    def add_markers(self, fig, x_data, y_data, indices, marker_type, row=None, col=None, marker_size=None):
        """Adds markers of a specific type to the figure."""
        if marker_type not in self.MARKER_PROPERTIES:
            ErrorHandler.log_and_raise_error(ValueError, f"Invalid marker_type '{marker_type}'. Valid types are: {', '.join(self.MARKER_PROPERTIES.keys())}")
        
        properties = self.MARKER_PROPERTIES[marker_type]
        color = properties['color']
        size = marker_size if marker_size is not None else properties['size']
        
        self._add_marker_trace(fig, x_data, y_data, indices, color=color, size=size, row=row, col=col)

    def add_multiple_markers(self, fig, x_data, y_data, marker_data, row=None, col=None, marker_size=None, ):
        """Adds multiple types of markers to the figure in a single call."""
        for marker_type, indices in marker_data.items():
            if marker_type not in self.MARKER_PROPERTIES:
                ErrorHandler.log_and_raise_error(
                    ValueError, 
                    f"Invalid marker_type '{marker_type}'. Valid types are: {', '.join(self.MARKER_PROPERTIES.keys())}"
                )
            
            properties = self.MARKER_PROPERTIES[marker_type]
            color = properties['color']
            size = marker_size if marker_size is not None else properties['size']
            
            self._add_marker_trace(fig, x_data, y_data, indices, color=color, size=size, row=row, col=col)
        
    def create_debug_plot(self, title, x_axis, y_axis, data, y_axis_key, vline_key):
        """Creates a debug plot with peak and low markers."""
        fig = self.create_base_figure(title)
        self.plot_data(fig, x_axis, y_axis[y_axis_key])

        marker_data = {
            'peaks': data.get('peaks'),
            'lows': data.get('lows')
        }
        self.add_multiple_markers(fig, x_axis['data'], y_axis[y_axis_key]['data'], marker_data)
        self.add_vline(fig, x_axis['data'][data[vline_key]])
        return fig