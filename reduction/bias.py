#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: bias.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from astropy.io import fits
from astropy.stats import sigma_clip
import numpy

def create_median_bias(bias_list, median_bias_filename):
    """This function must:

    - Accept a list of bias file paths as bias_list.
    - Read each bias file and create a list of 2D numpy arrays.
    - Use a sigma clipping algorithm to combine all the bias frames using
      the median and removing outliers outside 3-sigma for each pixel.
    - Save the resulting median bias frame to a FITS file with the name
      median_bias_filename.
    - Return the median bias frame as a 2D numpy array.

    """
    
    if bias_list:
      bias_images = []
      
      # Will read each file and append to bias_images list where the arrays have dtype = float32
      for bias in bias_list:
          bias_data = fits.getdata(bias)[100:-100, 100:-100]
          bias_images.append(bias_data.astype('f4'))

      # Reads the list of biases and sigma clips the arrays
      bias_images_masked = sigma_clip(bias_images, cenfunc='median', sigma=3, axis=0) 

      # Creates a final 2D array that is the mean of each pixel from all different biases
      median_bias = numpy.ma.mean(bias_images_masked, axis=0)

      # Create a new FITS file from the resulting median bias frame.
      # You can replace the header with something more meaningful with information.
      primary = fits.PrimaryHDU(data=median_bias.data, header=fits.Header())
      hdul = fits.HDUList([primary])
      hdul.writeto(median_bias_filename, overwrite=True)

      return median_bias

    else:
       return