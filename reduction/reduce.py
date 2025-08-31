#!/usr/bin/env python
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from reduction.bias import create_median_bias
from reduction.darks import create_median_dark
from reduction.flats import create_median_flat
from reduction.science import reduce_science_frames

def reduce_science_images(
    bias_files: list, 
    dark_files: list, 
    flat_files: list, 
    science_files: list, 
    output_dir: str,
) -> list:
    """Main function that reduces science FITS images.

    Args:
        bias_files: list of paths to bias frame FITS files.
        dark_files: list of paths to dark frame FITS files.
        flat_files: list of paths to flat frame FITS files.
        science_files: list of paths to science FITS files.
        output_dir : directory where reduced images should be saved.

    Returns:
        reduced_images: list of file paths to reduced science images saved to output_dir.
    """
    # Assigning 2D median bias, dark, and flat arrays
    bias           = create_median_bias(bias_files)
    dark, exp_time = create_median_dark(dark_files, bias)        # Need dark exposure time for flat fame reduction
    flat           = create_median_flat(flat_files, bias, dark, exp_time)
    reduced_images = reduce_science_frames(science_files, bias, dark, flat, output_dir)

    return reduced_images