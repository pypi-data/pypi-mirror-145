from .. processors import *
from .. plots import *
import copy


class EMGMeasurement:
    """Wrapper of single-trial EMG processing

    Parameters
    ----------
    data : ndarray of shape (n_samples,) or (n_samples, n_channels),
        where n_samples > 15 (See Notes)
        Signal data of one trial.

    hz : float
        Sample rate in hertz.
        See class EMGMeasurementCollection for suggested values of hz.

    timestamp : ndarray or None, default None
        The actual timestamp corresponds to the signal. If it is an
        ndarray, it should be in 1-dim and have the same length as the
        first dimension of x.

    trial_name : str or None, default None
        Trial name.

    channel_names : list of str, or None, default None
        If list, its length should be equal to n_channels.
        Channel names to be shown in the plot.

    emg_plot_params : EMGPlotParams, default None
        Parameters to control the plot. See class EMGPlotParams and
        function emg_plot.

    Notes
    -----
    n_samples has to meet the length condition for using bandpass
    filter. With the default parameter in BandpassFilter, n_samples
    must exceed 15. (See class BandpassFilter, function apply)
    """

    def __init__(self, data, hz, timestamp=None, trial_name=None, channel_names=None, emg_plot_params=None):
        BaseProcessor.assert_input(data)
        assert data.shape[0] > 15, 'first dimension of x must have length > 15'
        self.data = copy.deepcopy(data)
        self.hz = hz
        self.timestamp = copy.deepcopy(timestamp)
        self.timestamp = BaseProcessor.get_timestamp(self.data.shape, self.timestamp, self.hz)
        self.trial_name = trial_name
        self.channel_names = channel_names
        self.emg_plot_params = emg_plot_params

    def apply_dc_offset_remover(self):
        """Apply DC offset remover to the data

        Returns
        -------
        None
        """

        self.data = DCOffsetRemover().apply(self.data)

    def apply_bandpass_filter(self, bf_order=4, bf_cutoff_fq_lo=10, bf_cutoff_fq_hi=450):
        """Apply bandpass filter to the data

        Parameters
        ----------
        bf_order : int, default=4
            Effective order (i.e., order after two-directional
            filtering) of the butterworth filter. bf_order should be
            a multiple of 2.

        bf_cutoff_fq_lo : float, default=10
            Low cutoff frequency of the bandpass filter.
            See class BandpassFilter.

        bf_cutoff_fq_hi : float, default=450
            High cutoff frequency of the bandpass filter.
            See class BandpassFilter.

        Returns
        -------
        None
        """

        self.data = BandpassFilter(self.hz, bf_order, bf_cutoff_fq_lo, bf_cutoff_fq_hi).apply(self.data)

    def apply_full_wave_rectifier(self):
        """Apply full wave rectifier to the data

        Returns
        -------
        None
        """

        self.data = FullWaveRectifier().apply(self.data)

    def apply_linear_envelope(self, le_order=4, le_cutoff_fq=6):
        """Apply linear envelope to the data

        Parameters
        ----------
        le_order : int, default=4
            Effective order (i.e., order after two-directional
            filtering) of the butterworth filter for linear envelope.
            le_order should be a multiple of 2.

        le_cutoff_fq : float, default=6
            Cutoff frequency of the lowpass filter.
            See class LinearEnvelope.

        Returns
        -------
        None
        """

        self.data = LinearEnvelope(self.hz, le_order, le_cutoff_fq).apply(self.data)

    def apply_end_frame_cutter(self, n_end_frames=30):
        """Apply end frame cutter to the data (signal and timestamp)

        Parameters
        ----------
        n_end_frames : int, default=30
            Number of frames to be cut off in both ends of the signal.
            n_end_frames >= 0.

        Returns
        -------
        None
        """

        self.data = EndFrameCutter(n_end_frames).apply(self.data)
        self.timestamp = EndFrameCutter(n_end_frames).apply(self.timestamp)

    def apply_amplitude_normalizer(self, max_amplitude):
        """Apply amplitude normalizer to the data

        Parameters
        ----------
        max_amplitude : scalar, list, or ndarray
            One or more positive values.
            If data is in 1-dim or n_channels is 1, then
            max_amplitude should be one value; otherwise max_amplitude
            should be n_channels values.
            max_amplitude is the value used as divisor in amplitude
            normalization.

        Returns
        -------
        None
        """

        self.data = AmplitudeNormalizer().apply(self.data, divisor=max_amplitude)

    def apply_segmenter(self, beg_ts, end_ts):
        """Apply segmenter to the data (signal and timestamp)

        Parameters
        ----------
        beg_ts : float
            Beginning time of interest. beg_ts <= timestamp[-1].

        end_ts : float
            End time of interest. end_ts >= timestamp[0].
            Also beg_ts < end_ts.

        Returns
        -------
        None
        """

        beg_idx, end_idx = BaseProcessor.get_indices_from_timestamp(self.timestamp, beg_ts, end_ts)
        self.data = Segmenter().apply(self.data, beg_idx=beg_idx, end_idx=end_idx)
        self.timestamp = Segmenter().apply(self.timestamp, beg_idx=beg_idx, end_idx=end_idx)

    def plot(self):
        """Plot the data

        Returns
        -------
        None
        """
        plot_emg(self.data, self.timestamp, channel_names=self.channel_names,
                 main_title=self.trial_name, emg_plot_params=self.emg_plot_params)

    def export_csv(self, csv_path):
        """Export the processing result to csv

        Parameters
        ----------
        csv_path : str
            The destination path to export data.

        Returns
        -------
        None
        """

        BaseProcessor.export_csv(csv_path, self.data, timestamp=self.timestamp, channel_names=self.channel_names)
