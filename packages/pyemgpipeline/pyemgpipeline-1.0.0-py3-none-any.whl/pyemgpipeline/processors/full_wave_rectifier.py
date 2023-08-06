from . base import BaseProcessor
import numpy as np


class FullWaveRectifier(BaseProcessor):
    """Full wave rectifier for EMG signals

    """

    def __init__(self):
        pass

    def apply(self, x, **kwargs):
        """Apply full wave rectifier

        Parameters
        ----------
        x : ndarray
            Shape (n_samples,) or (n_samples, n_channels).
            Signal data to be processed.

        Returns
        -------
        x_processed : ndarray
            Same shape as x.
            The result of applying full wave rectifier to x.
        """

        super().assert_input(x)

        x_processed = np.abs(x)
        return x_processed

    def get_param_values_in_str(self):
        """Getting the parameter values of the processor for display
        purpose

        Returns
        -------
        params_in_str : str
            Parameter values.
        """

        params_in_str = super().get_param_values_in_str()
        return params_in_str
