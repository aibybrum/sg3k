import numpy as np

from utils import ErrorHandler
from validators import Validator


class StartPointSetter:
    def __init__(self, df, validator=None):
        self._validator = validator or Validator()
        self._validator.dataframe.validate_not_empty(df, "DataFrame")
        self.df = df.copy()

    def _cumulative_sum(self, series, phase='1', offset=0.0):
        """Computes the cumulative sum of differences in a pandas Series."""
        lis, diff = [0.0], 0.0
        if phase == '2':
            lis[0] = round(offset, 6)
            diff = lis[0]
        for i in range(len(series) - 1):
            diff += series[i + 1] - series[i]
            lis.append(round(diff, 6))
        return lis

    def _shift_column(self, key, column_name):
        """Shifts a DataFrame column based on the given key, recalculating values relative to the key."""
        self._validator.dataframe.validate_index_in_bounds(self.df, key)

        first_part = self.df.iloc[:key + 1][column_name][::-1].reset_index(drop=True)
        second_part = self.df.iloc[key + 1:][column_name].reset_index(drop=True)
        offset = second_part.iloc[0] - first_part.iloc[0]
        
        shifted_first = self._cumulative_sum(first_part, phase='1')[::-1]
        shifted_second = self._cumulative_sum(second_part, phase='2', offset=offset)
        
        return np.concatenate((shifted_first, shifted_second))

    @ErrorHandler.log_exceptions
    def set_start_point(self, key, rotate=False):
        """Adjusts multiple columns in the DataFrame to start from a specific key."""
        adjusted_df = self.df.copy()

        columns_to_shift = [
            'time_sec', 'horz_distance_m', 'horz_distance_ft',
            'x_axis_distance_m', 'x_axis_distance_ft',
            'y_axis_distance_m', 'y_axis_distance_ft'
        ]

        for col in columns_to_shift:
            adjusted_df[col] = self._shift_column(key, col)

        if rotate:
            adjusted_df = self.rotate_landing_path(adjusted_df, key)
        
        self.df = adjusted_df
        return self.df
    
    @ErrorHandler.log_exceptions
    def rotate_landing_path(self, df, key):
        """Rotate the landing path so that the last point's y-axis is at 0, while keeping the start point at (0, 0)."""
        start_point = df.iloc[key]
        last_point = df.iloc[-1]

        df['x_axis_distance_ft'] -= start_point['x_axis_distance_ft']
        df['y_axis_distance_ft'] -= start_point['y_axis_distance_ft']
        df['x_axis_distance_m'] -= start_point['x_axis_distance_m']
        df['y_axis_distance_m'] -= start_point['y_axis_distance_m']

        delta_x_ft = last_point['x_axis_distance_ft'] - start_point['x_axis_distance_ft']
        delta_y_ft = last_point['y_axis_distance_ft'] - start_point['y_axis_distance_ft']
        angle_ft = np.arctan2(delta_y_ft, delta_x_ft)

        delta_x_m = last_point['x_axis_distance_m'] - start_point['x_axis_distance_m']
        delta_y_m = last_point['y_axis_distance_m'] - start_point['y_axis_distance_m']
        angle_m = np.arctan2(delta_y_m, delta_x_m)

        df['x_axis_distance_ft'], df['y_axis_distance_ft'] = self._rotate_coordinates(
            df['x_axis_distance_ft'], df['y_axis_distance_ft'], -angle_ft
        )
        df['x_axis_distance_m'], df['y_axis_distance_m'] = self._rotate_coordinates(
            df['x_axis_distance_m'], df['y_axis_distance_m'], -angle_m
        )

        return df

    def _rotate_coordinates(self, x, y, angle):
        """Rotate coordinates by a given angle."""
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        x_rotated = x * cos_angle - y * sin_angle
        y_rotated = x * sin_angle + y * cos_angle
        return x_rotated, y_rotated