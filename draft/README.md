# Construction Drawings Converter

This Python script provides a simple GUI tool for converting PDF files to images, splitting PDFs into multiple pages, and merging multiple PDFs into a single file. The GUI is built using Tkinter, and the script leverages the `PyMuPDF` and `Pillow` libraries for PDF processing and image conversion.

## Features

- **Convert PDF to JPG**: Convert individual pages of a PDF file into JPG images.
- **Split PDF into Single Pages**: Split a multi-page PDF into individual single-page PDFs.
- **Split PDF into Multiple Files**: Divide a large PDF into smaller PDFs, each containing a specified number of pages.
- **Merge PDFs**: Combine multiple PDF files into a single PDF file.

## Requirements

- Python 3.x
- The following Python libraries:
  - `PyMuPDF` (for handling PDF files)
  - `Pillow` (for image processing)
  - `Tkinter` (for building the GUI; usually comes pre-installed with Python)

## Install the Required Libraries:
- Install the necessary libraries using pip:
  - pip install Pillow 
  - pip install PyMuPDF

## Usage
- Run the script：
  - python DrawingConverter.py
- A GUI window will open, allowing you to perform the following tasks:
  - Select a PDF file: Click the "Select PDF file" button to choose your input PDF.
Set Output Directory: Click "Selecting the output directory" to specify where the converted files should be saved.
Convert Single Page PDFs to JPG: Click the "Convert single-page PDF to JPG" button.
Split PDF into Single Pages: Click "Convert multi-page PDFs to single pages" to split the PDF.
Split PDF into Multiple Files: Specify the number of pages per split and click "Split multi-page PDF into multiple PDF files."
Merge Multiple PDFs: Click "Combine multiple PDF files into one PDF file" and select the PDFs you want to merge.
