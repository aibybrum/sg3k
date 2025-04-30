import plotly.graph_objects as go


class CommonPlotHelper:
    def empty_layout(self, text):
        """Returns a layout with a centered annotation text."""
        return {
            'layout': go.Layout(
                xaxis={"visible": True},
                yaxis={"visible": True},
                annotations=[
                    {
                        "text": text,
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            )
        }
    
    def create_base_figure(self, title, height=550):
        """Creates a base figure with common settings."""
        fig = go.Figure()
        fig.update_layout(hovermode='x unified', title_text=title, height=height)
        return fig
    
    def add_vline(self, fig, x_value, row=None, col=None, line_width=1.2, line_dash=False):
        """Adds a vertical line to the figure, with optional subplot targeting."""
        dash_style = 'dash' if line_dash else None
        if x_value is not None:
            if row is not None and col is not None:
                fig.add_vline(x=x_value, line_width=line_width, line_dash=dash_style, row=row, col=col)
            else:
                fig.add_vline(x=x_value, line_width=line_width, line_dash=dash_style)

    def plot_data(self, fig, x_axis, y_axis, row=None, col=None):
        """Plots data on the figure, with optional subplot targeting."""
        fig.add_trace(go.Scatter(
            x=x_axis['data'],
            y=y_axis['data'],
            mode='lines',
            line=dict(color=y_axis['color'], width=1.2),
            hovertemplate=y_axis['hovertemplate'],
            showlegend=False
        ), row=row, col=col)

        fig.update_xaxes(title_text=x_axis['title'], row=row, col=col)
        fig.update_yaxes(title_text=y_axis['title'], row=row, col=col)