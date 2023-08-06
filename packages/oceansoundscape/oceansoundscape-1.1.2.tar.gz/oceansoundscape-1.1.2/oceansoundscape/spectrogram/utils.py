#!/usr/bin/env python
__author__ = 'Danelle Cline'
__copyright__ = '2021'
__license__ = 'GPL v3'
__contact__ = 'dcline at mbari.org'
__doc__ = '''

Miscellaneous utilities and utilities for spectrogram generation

@var __date__: Date of last svn commit
@undocumented: __doc__ raven
@status: production
@license: GPL
'''

import numpy as np
import cv2
from scipy.ndimage.filters import convolve
from oceansoundscape.spectrogram import colormap
from oceansoundscape.spectrogram import conf as global_conf

class ImageUtils(object):

    @staticmethod
    def smooth(fft_array, blur_type):
        """
        Smooth fft either in time/frequency
        :param fft_array: fft array
        :param blur_type:  type of blur either 'time' or 'frequency'
        :return:
        # """
        if blur_type == 'time':
            smoothed_fft_array = convolve(fft_array, weights=ImageUtils.gauss2D(shape=(5, 1), sigma=1.0))
        elif blur_type == 'frequency':
            smoothed_fft_array = convolve(fft_array, weights=ImageUtils.gauss2D(shape=(1, 5), sigma=1.0))
        else:
            smoothed_fft_array = convolve(fft_array, weights=ImageUtils.gauss2D(shape=(2, 2), sigma=1.0))

        return smoothed_fft_array

    @staticmethod
    def colorizeDenoise(samples, plotpath_jpeg):
        """
        Colorize, denoise colored image and save spectrogram
        :param samples:  stft array
        :param plotpath: path to the file to save the output to
        :return:
        """
        # Resize and use linear color map
        stft_resize = cv2.resize(samples, global_conf.IMAGE_SIZE, cv2.INTER_AREA)
        stft_scaled = np.int16(stft_resize / (stft_resize.max() / 255.0))
        img = colormap.parula_map(stft_scaled)
        img_rescale = (img * 255).astype('uint8')
        img_denoise = cv2.fastNlMeansDenoisingColored(img_rescale,None,10,10,7,21)
        im_rgb = cv2.cvtColor(np.flipud(img_denoise), cv2.COLOR_BGR2RGB)
        cv2.imwrite(plotpath_jpeg.as_posix(), im_rgb, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    @staticmethod
    def gauss2D(shape=(3, 3), sigma=0.5):
        """
        2D Gaussian mask to emulate MATLAB fspecial('gaussian',[shape],[sigma])
        :param shape (x,y) shape of the mask
        :sigma sigma of the mask
        """
        m, n = [(ss - 1.) / 2. for ss in shape]
        y, x = np.ogrid[-m:m + 1, -n:n + 1]
        mask = np.exp(-(x * x + y * y) / (2. * sigma * sigma))
        mask[mask < np.finfo(mask.dtype).eps * mask.max()] = 0
        mask_sum = mask.sum()
        if mask_sum != 0:
            mask /= mask_sum
        return mask
