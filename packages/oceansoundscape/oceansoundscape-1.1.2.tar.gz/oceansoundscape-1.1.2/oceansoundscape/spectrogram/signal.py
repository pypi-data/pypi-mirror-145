#!/usr/bin/env python
__author__ = 'Danelle Cline, John Ryan'
__copyright__ = '2021'
__license__ = 'GPL v3'
__contact__ = 'dcline at mbari.org'
__doc__ = '''
 

@var __date__: Date of last svn commit
@undocumented: __doc__ raven
@status: production
@license: GPL
'''

import numpy as np
import scipy


def psd_1sec(x: np.array([]), sample_rate: int, freq_response_db: float):
    """
    Computes power spectral density (PSD) estimates in 1` second bins on the input signal x
    :param x:  sample array of raw float measurements (to be converted to volts)
    :param sample_rate:  sampling rate of the raw samples
    :param freq_response_db:  frequency response of the hydrophone
    :return: power spectral density, array of sample frequencies
    """

    # convert scaled voltage to volts
    v = x * 3

    # initialize empty spectrogram
    num_seconds = round(len(x) / sample_rate)
    nfreq = int(sample_rate / 2 + 1)
    sg = np.empty((nfreq, num_seconds), float)

    # get window for welch
    w = scipy.signal.get_window('hann', sample_rate)

    # process spectrogram
    spa = 1  # seconds per average
    for x in range(0, num_seconds):
        cstart = x * spa * sample_rate
        cend = cstart + spa * sample_rate
        f, psd = scipy.signal.welch(v[cstart:cend], fs=sample_rate, window=w, nfft=sample_rate)
        psd = 10 * np.log10(psd) + freq_response_db
        sg[:, x] = psd

    return sg, f
