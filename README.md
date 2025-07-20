# FITS Image Reduction Web App

[fitsimagereduction.live](https://fitsimagereduction.live)

This web app makes it easy to reduce raw astronomical images using standard calibration frames. Simply upload your **science**, **dark**, **bias**, and **flat** `.fits` files, and the app will process and return cleaned, reduced science images ready for analysis or visualization.

## What It Does

This tool performs basic image reduction using the formula:

Reduced = (Science - Expsoure time * Dark - Bias) / Flat

It removes sensor noise and optical imperfections from your science frames so you can focus on the data that matters.

## Features

- Drag-and-drop interface for FITS file uploads
- Supports:
  - Science frames
  - Dark frames
  - Flat frames 
  - Bias frames (optional)
- Automatic image reduction
- Instant download of reduced science images
- Clean, simple user interface

```
fitsimagereduction/
├── app.py                # Main Flask application
├── wsgi.py               # WSGI entry point
├── reduction/            # Python code for image reduction
├── static/               # Before and after images
├── templates/            # HTML templates
├── requirements.txt      # Dependencies
└── README.md
```

## Built With
Python (Flask)

Astropy, NumPy

HTML/CSS/JS for the frontend

## Try it out!

You can test the app using example FITS files in the [`sample_data/`](sample_data) folder:

- [`science1.fits`](sample_data/LPSEB35_g_20250530_034359.fits)
- [`dark1.fits`](sample_data/Dark_BIN1_20250530_020632.fits)
- [`flat1.fits`](sample_data/domeflat_g_001.fits)
- [`bias1.fits`](sample_data/Bias_BIN1_20250530_020505.fits)

To download a file:
1. Click the link
2. Press the **"Download"** button at the top right of the GitHub file view

Then, go to [fitsimagereduction.live](https://fitsimagereduction.live) and place each of the files to their respective places and wait to download your reduced file!