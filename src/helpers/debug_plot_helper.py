import plotly.graph_objects as go

from helpers import CommonPlotHelper


class DebugPlotHelper(CommonPlotHelper):
    MARKER_SIZE = 7
    PEAK_COLOR = 'Green'
    LOW_COLOR = 'Red'

    def add_markers(self, fig, x_data, y_data, peaks, lows, row=None, col=None):
        """Adds peak, low, and deriv points to the figure, with optional subplot targeting."""
        marker_data = [(peaks, self.PEAK_COLOR), (lows, self.LOW_COLOR)]

        for data, color in marker_data:
            if data is not None and len(data) > 0:
                trace = go.Scatter(
                    x=x_data[data], y=y_data[data],
                    mode='markers', marker=dict(size=self.MARKER_SIZE, color=color), showlegend=False
                )
                if row is not None and col is not None:
                    fig.add_trace(trace, row=row, col=col)
                else:
                    fig.add_trace(trace)

    def create_debug_plot(self, title, x_axis, y_axis, data, y_axis_key, vline_key):
        """Helper method to create a debug plot."""
        fig = self.create_base_figure(title)
        self.plot_data(fig, x_axis, y_axis[y_axis_key])
        self.add_markers(fig, x_axis['data'], y_axis[y_axis_key]['data'], data.get('peaks'), data.get('lows'))
        self.add_vline(fig, x_axis['data'][data[vline_key]])
        return fig