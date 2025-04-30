from utils import ErrorHandler
from validators import Validator


class AxisHelper:
    def __init__(self, distance_metric='m', speed_metric='km/u', validator=None):
        self._distance_metric = distance_metric
        self._speed_metric = speed_metric
        self._validator = validator or Validator()

    @ErrorHandler.log_exceptions
    def get_axis_settings(self, df, x_axis_param=None, y_axis_param=None, start=None, stop=None):
        """Retrieve x and y axis settings for the plots."""
        self._validator.dataframe.validate_not_empty(df, "DataFrame")
        x_data = df[start:stop] if start and stop else df
        
        x_axis = self.get_x_axis(x_data, x_axis_param)
        y_axis = self.get_y_axis(x_data, y_axis_param)
        
        return x_axis, y_axis

    @ErrorHandler.log_exceptions
    def get_x_axis(self, df, parameter=None):
        """Retrieves X-axis plot settings for various metrics in the DataFrame."""
        self._validator.dataframe.validate_not_empty(df, "DataFrame")
        self._validator.metric.validate_metric(distance_metric=self._distance_metric)
        settings = {}

        if 'time_sec' in df.columns:
            settings['Time'] = self._create_setting(df['time_sec'], '#00CC96', 's', 'Time: %{y:.2f} s <extra></extra>', f"Time (s)")

        horz_distance_col = self._get_column_or_none(df, 'horz_distance', self._distance_metric)
        if horz_distance_col is not None:
            settings['Horizontal distance'] = self._create_setting(horz_distance_col, '#636EFA', self._distance_metric, 'Horizontal Distance: %{y:.2f} ' + self._distance_metric + '<extra></extra>', f"Horizontal distance ({self._distance_metric})")

        x_axis_distance_col = self._get_column_or_none(df, 'x_axis_distance', self._distance_metric)
        if x_axis_distance_col is not None:
            settings['Distance'] = self._create_setting(x_axis_distance_col, '#AB63FA', self._distance_metric, 'x-axis distance: %{y:.2f} ' + self._distance_metric + '<extra></extra>', f"X-axis distance ({self._distance_metric})")

        if parameter is not None:
            return self._get_axis_data(settings, parameter)
        return settings

    @ErrorHandler.log_exceptions
    def get_y_axis(self, df, parameter=None):
        """Retrieves Y-axis plot settings for various metrics in the DataFrame."""
        self._validator.dataframe.validate_not_empty(df, "DataFrame")
        self._validator.metric.validate_metric(speed_metric=self._speed_metric, distance_metric=self._distance_metric)
        settings = {}

        if 'elevation' in df.columns:
            settings['Elevation'] = self._create_setting(df['elevation'], '#636EFA', 'ft', 'Elevation: %{y:.2f} ft <extra></extra>', 'Elevation (ft)')

        horz_speed_col = self._get_column_or_none(df, 'horz_speed', self._speed_metric)
        if horz_speed_col is not None:
            settings['Horizontal speed'] = self._create_setting(horz_speed_col, '#FF0B0B', self._speed_metric, f'Horz speed: %{{y:.2f}} {self._speed_metric} <extra></extra>', f"Horizontal speed ({self._speed_metric})")

        y_axis_distance_col = self._get_column_or_none(df, 'y_axis_distance', self._distance_metric)
        if y_axis_distance_col is not None:
            settings['Distance'] = self._create_setting(y_axis_distance_col, '#636EFA', self._distance_metric, f'Y-axis distance: %{{y:.2f}} {self._distance_metric} <extra></extra>', f"Y-axis distance ({self._distance_metric})")

        if 'dive_angle' in df.columns:
            settings['Dive angle'] = self._create_setting(df['dive_angle'], '#AB63FA', 'deg', 'Dive angle: %{y:.2f}° <extra></extra>', f"Dive angle (deg)")

        vert_speed_col = self._get_column_or_none(df, 'vert_speed', self._speed_metric)
        if vert_speed_col is not None:
            settings['Vertical speed'] = self._create_setting(vert_speed_col, '#00CC96', self._speed_metric, f'Vert speed: %{{y:.2f}} {self._speed_metric} <extra></extra>', f"Vertical speed ({self._speed_metric})")

        if 'glide_ratio' in df.columns:
            settings['Glide ratio'] = self._create_setting(df['glide_ratio'], '#FF9900', 'gr', 'Glide ratio: %{y:.2f} <extra></extra>', f"Glide ratio (gr)")

        for col in df.columns:
            if 'first_deriv' in col:
                settings[col] = self._create_setting(df[col], '#9370DB', '', 'First derivative: %{y:.2f} <extra></extra>', 'First derivative')
            elif 'second_deriv' in col:
                settings[col] = self._create_setting(df[col], '#FFD700', '', 'Second derivative: %{y:.2f} <extra></extra>', 'Second derivative')

        if parameter is not None:
            return self._get_axis_data(settings, parameter)
        return settings
    
    def _get_column_or_none(self, df, prefix, metric):
        """Retrieves a column from the DataFrame based on a prefix and metric."""
        column_name = f'{prefix}_{metric}'
        return df[column_name] if column_name in df.columns else None
    
    def _create_setting(self, data, color, metric, hovertemplate, title):
        """Creates a dictionary of plot settings for a specific metric."""
        return {
            'data': data,
            'color': color,
            'metric': metric,
            'hovertemplate': hovertemplate,
            'title': title
        }
    
    def _get_axis_data(self, settings, parameter):
        """Helper function to retrieve axis data and label from settings based on the parameter."""
        if parameter in settings:
            return settings[parameter]
        else:
            ErrorHandler.log_and_raise_error(ValueError, f"Invalid parameter: {parameter}")