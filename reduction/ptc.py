#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: ptc.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from astropy.io import fits
import numpy

def calculate_gain(files):
    """This function must:

    - Accept a list of files that you need to calculate the gain
      (two files should be enough, but need to be flats).
    - Read the files and calculate the gain in e-/ADU.
    - Return the gain in e-/ADU.

    """

    # Get the first two flats from the list, making sure we get from the center since edges are nonuniform
    flat1 = fits.getdata(files[0]).astype('f4')[100:-100, 100:-100]
    flat2 = fits.getdata(files[1]).astype('f4')[100:-100, 100:-100]
    
    # Calculate the variance of the difference between the two images
    flat_diff = flat1 - flat2
    flat_diff_var = numpy.var(flat_diff)

    # Get the signal as the average of the two images
    mean_signal = 0.5 * numpy.mean(flat1 + flat2)

    # Calculate the gain
    gain = (2 * mean_signal / flat_diff_var).astype(numpy.float64)

    return gain


def calculate_readout_noise(files, gain):
    """This function must:

    - Accept a list of files that you need to calculate the readout noise
      (two files should be enough, but need to be biases).
    - Accept the gain in e-/ADU as gain. This should be the one you calculated
      in calculate_gain.
    - Read the files and calculate the readout noise in e-.
    - Return the readout noise in e-.

    """

    # Get the first two biases from the list, where we can use a very large region since the bias level is very flat.
    # So we just trim the images to remove the contribution from the edge pixels.
    bias1 = fits.getdata(files[0]).astype('f4')[100:-100, 100:-100]
    bias2 = fits.getdata(files[1]).astype('f4')[100:-100, 100:-100]
    
    # Calculate the variance of the difference between the two images
    bias_diff = bias1 - bias2
    bias_diff_var = numpy.var(bias_diff)
    
    # Calculate the readout noise
    readout_noise_adu = numpy.sqrt(bias_diff_var / 2)
    readout_noise = (readout_noise_adu * gain).astype(numpy.float64)

    return readout_noise
