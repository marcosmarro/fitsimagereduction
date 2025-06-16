import os
import tempfile
from reduction.bias import create_median_bias
from reduction.darks import create_median_dark
from reduction.flats import create_median_flat
from reduction.science import reduce_science_frame

def reduce_science_images(bias_paths, flat_paths, dark_paths, science_paths, output_dir):
    """
    Stub function to simulate reducing science FITS images.

    Parameters:
    - bias_path (str or None): Path to bias frame FITS file
    - flat_path (str or None): Path to flat frame FITS file
    - dark_path (str or None): Path to dark frame FITS file
    - science_paths (list of str): List of paths to science FITS files
    - output_dir (str): Directory where reduced images should be saved

    Returns:
    - List of file paths to reduced science images saved in output_dir
    """

    temp_dir = tempfile.mkdtemp()

    # Collects all the different types of images from the given directory, and sorts them in a list
    bias_files = sorted(bias_paths)
    dark_files = sorted(dark_paths)
    flat_files = sorted(flat_paths)
    science_files = science_paths

    # Naming of the median filenames for the biases, darks, and flats
    median_bias_filename = os.path.join(temp_dir, 'Median-Bias.fits')
    median_dark_filename = os.path.join(temp_dir, 'Median-Dark.fits')
    median_flat_filename = os.path.join(temp_dir, 'Median-AutoFlat.fits')

    # Creates the medians from the list of biases, darks, and flats
    create_median_bias(bias_files, median_bias_filename)
    create_median_dark(dark_files, median_bias_filename, median_dark_filename)
    create_median_flat(flat_files, median_bias_filename, median_flat_filename, median_dark_filename)
  
    reduced_paths = []
    
    for science_filename in science_files:
        basename = os.path.basename(science_filename)
        name, ext = os.path.splitext(basename)
        reduced_filename = f"reduced_{name}{ext}"
        reduced_filepath = os.path.join(output_dir, reduced_filename)
        
        reduce_science_frame(
            science_filename,
            median_bias_filename,
            median_flat_filename,
            median_dark_filename,
            reduced_science_filename=reduced_filepath
        )
        
        reduced_paths.append(reduced_filepath)

    return reduced_paths
