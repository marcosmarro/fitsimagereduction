import os
import shutil
import glob
from reduction.bias import create_median_bias
from reduction.darks import create_median_dark
from reduction.flats import create_median_flat
from reduction.ptc import calculate_gain, calculate_readout_noise
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


    # Collects all the different types of images from the given directory, and sorts them in a list
    bias_files = sorted(bias_paths)
    dark_files = sorted(dark_paths)
    flat_files = sorted(flat_paths)
    science_files = science_paths

    # Naming of the median filenames for the biases, darks, and flats
    median_bias_filename = 'Median-Bias.fits'
    median_dark_filename = 'Median-Dark.fits'
    median_flat_filename = 'Median-AutoFlat.fits'

    # Creates the medians from the list of biases, darks, and flats
    median_bias = create_median_bias(bias_files, median_bias_filename)
    median_dark = create_median_dark(dark_files, median_bias_filename, median_dark_filename)
    median_flat = create_median_flat(flat_files, median_bias_filename, median_flat_filename, median_dark_filename)
    
    # Calculates and prints out the gain and readout noise from the list of flats and biases, respectively
    gain = calculate_gain(flat_files)
    print(f"Gain = {gain:.2f} e-/ADU")

    readout_noise = calculate_readout_noise(bias_files, gain)
    print(f"Readout Noise = {readout_noise:.2f} e-")

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
