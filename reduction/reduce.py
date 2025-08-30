#!/usr/bin/env python
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import os
from reduction.bias import create_median_bias
from reduction.darks import create_median_dark
from reduction.flats import create_median_flat
from reduction.science import reduce_science_images

def reduce_science_images(
    bias_files: list, 
    dark_files: list, 
    flat_files: list, 
    science_files: list, 
    output_dir: str,
) -> list:
    """Main function that reduces science FITS images.

    Args:
        bias_files: List of paths to bias frame FITS files.
        flat_files: List of paths to flat frame FITS files.
        dark_files: List of paths to dark frame FITS files.
        science_files: List of paths to science FITS files.
        output_dir : Directory where reduced images should be saved.

    Returns:
        reduced_paths: List of file paths to reduced science images saved in output_dir.
    """

    # Assigning 2D median bias, dark, and flat arrays
    bias           = create_median_bias(bias_files)
    dark, exp_time = create_median_dark(dark_files, bias)        # Need dark exposure time for flat fame reduction
    flat           = create_median_flat(flat_files, bias, dark, exp_time)

    reduced_paths = []
    
    # Reducing science files given the 2D median arrays 
    for science_file in science_files:
        basename  = os.path.basename(science_file)
        name, ext = os.path.splitext(basename)
        reduced_filename = f"reduced_{name}{ext}"
        reduced_filepath = os.path.join(output_dir, reduced_filename)
        
        reduce_science_images(
            science_filename = science_file,
            median_bias      = bias,
            median_flat      = flat,
            median_dark      = dark,
            reduced_filename = reduced_filepath,
        )
        
        reduced_paths.append(reduced_filepath)

    return reduced_paths