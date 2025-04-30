import numpy as np

from utils import ErrorHandler


class Utility:
    @staticmethod
    def calculate_derivatives(data, levels):
        """Calculate derivatives up to the specified levels using np.gradient."""
        derivatives = [data]
        for _ in range(levels):
            new_derivative = np.gradient(derivatives[-1])
            derivatives.append(new_derivative)
        return derivatives
    
    @staticmethod
    def map_dataframe(df_from, df_to, index):
        """Map an index from one Dataframe to another based on a common timestamp column."""
        try:
            timestamp = df_from.loc[index, 'timestamp']
            return df_to.index[df_to['timestamp'] == timestamp][0]
        except (IndexError, KeyError):
            ErrorHandler.log_and_raise_error(ValueError, "Mapping failed: no matching timestamp found")