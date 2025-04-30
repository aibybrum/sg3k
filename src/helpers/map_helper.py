import plotly.graph_objects as go

from validators import Validator
from jinja2 import Template
from helpers.file_helper import FileHelper


class MapHelper:
    def __init__(self, token, axis_helper, key_events, key_event_colors, validator=None):
        self._token = token
        self._axis_helper = axis_helper
        self._key_events = key_events
        self._key_event_colors = key_event_colors
        self._validator = validator or Validator()
        self._file_helper = FileHelper()

    def generate_map_html(self, mean_lat, mean_lon, geojson_data_js, height=700, width=100):
        """Generate HTML template for Mapbox 3D visualization."""
        template_content = self._file_helper.load_template('map_template.html')
        template = Template(template_content)
        html_content = template.render(
            token=self._token,
            mean_lat=mean_lat,
            mean_lon=mean_lon,
            geojson_data_js=geojson_data_js,
            height=height,
            width=width
        )
        return html_content

    def point_to_square(self, lon, lat, size=0.00001):
        """Generates a square polygon around a point."""
        return [
            [lon - size, lat - size],
            [lon + size, lat - size],
            [lon + size, lat + size],
            [lon - size, lat + size],
            [lon - size, lat - size]
        ]

    def df_to_geojson_polygons(self, df, properties, event_names=[], lat='lat', lon='lon'):
        """Converts DataFrame points to GeoJSON polygons with event-based colors."""
        self._validator.event.validate_event_names(event_names, self._key_events['landing'])

        features = []
        _, y_axis = self._axis_helper.get_axis_settings(df)
        default_color = y_axis['Elevation']['color']
    
        key_events_to_color = {
            event: self._key_events['landing'][event]
            for event in event_names
            if self._key_events['landing'].get(event) is not None
        }
    
        for idx, row in df.iterrows():
            polygon_coords = self.point_to_square(row[lon], row[lat])
            color = default_color
            for event, event_idx in key_events_to_color.items():
                if idx == event_idx:
                    color = self._key_event_colors.get(event, default_color)
                    break 
    
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [polygon_coords]
                },
                "properties": {prop: row[prop] for prop in properties}
            }
            feature["properties"]["color"] = color
            features.append(feature)
    
        return {
            "type": "FeatureCollection",
            "features": features
        }
    
    def generate_2d_map(self, elevation_data, key_events, markers_to_plot, height=550, width=None):
        """Generates a map view of the flight path using scatter mapbox."""
        _, y_axis = self._axis_helper.get_axis_settings(elevation_data)

        fig = go.Figure()
        fig.add_trace(go.Scattermapbox(
            lat=elevation_data.lat.loc[:key_events.get('stop_estimate')],
            lon=elevation_data.lon.loc[:key_events.get('stop_estimate')],
            mode='lines',
            line=dict(color=y_axis['Elevation']['color'], width=1.2),
            showlegend=False
        ))

        for event_name, label in markers_to_plot.items():
            event_id = key_events.get(event_name)
            if event_id is not None:
                color = self._key_event_colors.get(event_name, '#000000')
                fig.add_trace(go.Scattermapbox(
                    lat=[elevation_data.lat[event_id]],
                    lon=[elevation_data.lon[event_id]],
                    name=label,
                    mode='markers',
                    marker=dict(size=7, color=color),
                ))
            
        fig.update_layout(
            height=height,
            width=width,
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(yanchor="top", y=1, xanchor="right", x=1),
            mapbox=dict(
                accesstoken=self._token,
                style="satellite-streets",
                center=go.layout.mapbox.Center(
                    lat=elevation_data.lat[round(len(elevation_data) / 2)],
                    lon=elevation_data.lon[round(len(elevation_data) / 2)]
                ),
                pitch=0,
                zoom=15.5
            )
        )
        return fig