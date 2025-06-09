#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: darks.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from astropy.io import fits
from astropy.stats import sigma_clip
import numpy

def create_median_dark(dark_list, bias_filename, median_dark_filename):
    """This function must:
 
    - Accept a list of dark file paths to combine as dark_list.
    - Accept a median bias frame filename as bias_filename (the one you created using
      create_median_bias).
    - Read all the images in dark_list and create a list of 2D numpy arrays.
    - Read the bias frame.
    - Subtract the bias frame from each dark image.
    - Divide each dark image by its exposure time so that you get the dark current
      per second. The exposure time can be found in the header of the FITS file.
    - Use a sigma clipping algorithm to combine all the bias-corrected dark frames
      using the median and removing outliers outside 3-sigma for each pixel.
    - Save the resulting dark frame to a FITS file with the name median_dark_filename.
    - Return the median dark frame as a 2D numpy array.

    """
    if dark_list and bias_filename:
      bias = fits.getdata(bias_filename)
      dark_bias_data = []
      exp_times = []

      # Will read each file and append to dark_bias_data list where the arrays have dtype = float32
      for file in dark_list:
          dark = fits.open(file)
          dark_data = dark[0].data[100:-100, 100:-100].astype('f4')
          exptime = dark[0].header['EXPTIME']
          exp_times.append(exptime)

          # Subtracts bias from each dark image
          dark_data_no_bias = dark_data - bias
          
          # Divides each dark image (with bias subtracted) by the exposure time to get dark current, and adds to list
          dark_bias_data.append(dark_data_no_bias / exptime) 

      # Reads the list of darks and sigma clips the arrays
      dark_sc = sigma_clip(dark_bias_data, cenfunc='median', sigma=3, axis=0)

      # Creates a final 2D array that is the mean of each pixel from all different darks
      median_dark = numpy.ma.mean(dark_sc, axis=0)

      # Create a new FITS file from the resulting median dark frame.
      dark_hdu = fits.PrimaryHDU(data=median_dark.data, header=fits.Header())
      dark_hdu.header['EXPTIME'] = numpy.mean(exp_times)
      dark_hdu.header['COMMENT'] = 'Combined dark image with bias subtracted'
      hdul = fits.HDUList([dark_hdu])
      hdul.writeto(median_dark_filename, overwrite=True)

      
      return median_dark
    
    elif dark_list and bias_filename==None:
       raise ValueError("Bias frame filename is required and must exist for dark frame processing.")
    
    else:
       return
