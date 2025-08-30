#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: flats.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from astropy.io import fits
from astropy.stats import sigma_clip
import numpy
import os

def create_median_flat(
    flat_list,
    median_bias_filename,
    median_flat_filename,
    dark_filename,
):
    """This function must:

    - Accept a list of flat file paths to combine as flat_list. Make sure all
      the flats are for the same filter.
    - Accept a median bias frame filename as bias_filename (the one you created using
      create_median_bias).
    - Read all the images in flat_list and create a list of 2D numpy arrays.
    - Read the bias frame.
    - Subtract the bias frame from each flat image.
    - Optionally you can pass a dark frame filename as dark_filename and subtract
      the dark frame from each flat image (remember to scale the dark frame by the
      exposure time of the flat frame).
    - Use a sigma clipping algorithm to combine all the bias-corrected flat frames
      using the median and removing outliers outside 3-sigma for each pixel.
    - Create a normalised flat divided by the median flat value.
    - Save the resulting median flat frame to a FITS file with the name
      median_flat_filename.
    - Return the normalised median flat frame as a 2D numpy array.

    """
    
    if os.path.isfile(median_bias_filename):
      bias = fits.getdata(median_bias_filename)
    else:
      bias = None

    dark = fits.getdata(dark_filename)
    dark_file = fits.open(dark_filename)
    dark_exptime = dark_file[0].header['EXPTIME']
    
    flat_bias_data = []
    
    # Will read each file and append to dark_bias_data list where the arrays have dtype = float32
    for file in flat_list:
        flat = fits.open(file)
        flat_data = flat[0].data[96:-96, 96:-96].astype('f4')
        flat_exptime = flat[0].header['EXPTIME']
        
        # Subtracts bias from each flat and adds to flat_bias_data list
        if bias is not None:
          flat_data =- bias
        
        flat_data =- dark * flat_exptime / dark_exptime
        
        flat_bias_data.append(flat_data)  

    # Reads the list of flats and sigma clips the arrays
    flat_sc = sigma_clip(flat_bias_data, cenfunc='median', sigma=3, axis=0)
    
    # Creates a final 2D array that is the mean of each pixel from all different flats, and then divides by the median 
    # flat value to normalize
    flat = numpy.ma.mean(flat_sc, axis=0)

    # Normalizes the resulting flat to get the median flat
    median_flat = flat / numpy.median(flat)

    # Create a new FITS file from the resulting median dark frame.
    flat_hdu = fits.PrimaryHDU(data=median_flat.data, header=fits.Header())
    flat_hdu.header['COMMENT'] = 'Normalized flat image with bias subtracted'
    hdul = fits.HDUList([flat_hdu])
    hdul.writeto(median_flat_filename, overwrite=True)

    return median_flat
    
