#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: science.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from astropy.io import fits
from astroscrappy import detect_cosmics
import os
from astropy.wcs import WCS

def reduce_science_frame(
    science_filename,
    median_bias_filename,
    median_flat_filename,
    median_dark_filename,
    reduced_science_filename="reduced_science.fits",
):
    """This function must:

    - Accept a science frame filename as science_filename.
    - Accept a median bias frame filename as median_bias_filename (the one you created
      using create_median_bias).
    - Accept a median flat frame filename as median_flat_filename (the one you created
      using create_median_flat).
    - Accept a median dark frame filename as median_dark_filename (the one you created
      using create_median_dark).
    - Read all files.
    - Subtract the bias frame from the science frame.
    - Subtract the dark frame from the science frame. Remember to multiply the
      dark frame by the exposure time of the science frame. The exposure time can
      be found in the header of the FITS file.
    - Correct the science frame using the flat frame.
    - Optionally, remove cosmic rays.
    - Save the resulting reduced science frame to a FITS file with the filename
      reduced_science_filename.
    - Return the reduced science frame as a 2D numpy array.

    """
    
    # Reads all the files and grabs their respective array
    science = fits.open(science_filename)

    original_header = science[0].header
    original_wcs = WCS(original_header)
    cropped_wcs = original_wcs.slice((slice(100, -100), slice(100, -100)))
    cropped_header = cropped_wcs.to_header()
    for key in original_header:
      if key in ('HISTORY', 'COMMENT'):
         continue
      if key not in cropped_header:
        cropped_header[key] = original_header[key]


    science_data = science[0].data[100:-100, 100:-100].astype('f4')

    # Exposure time of science to later use with median dark 
    exposure_time = science[0].header['EXPTIME']
    
    # Removes bias and dark frames, and corrects by dividing by flat frame
    if os.path.isfile(median_bias_filename):
      median_bias = fits.getdata(median_bias_filename)
      science_data -= median_bias 
    
    median_dark = fits.getdata(median_dark_filename)
    science_data -= exposure_time * median_dark

    median_flat = fits.getdata(median_flat_filename)
    science_data /= median_flat
    
    # Removal of cosmic rays
    mask, cleaned = detect_cosmics(science_data)
    reduced_science = cleaned

    # Create a new FITS file from the resulting reduced science frame.
    science_hdu = fits.PrimaryHDU(data=reduced_science.data, header=cropped_header)
    science_hdu.header['COMMENT'] = 'Reduced science image correcting from all 3 frames (bias, dark, and flat).'
    hdul = fits.HDUList([science_hdu])
    hdul.writeto(reduced_science_filename, overwrite=True)

    return reduced_science
