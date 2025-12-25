"""Configure pytesseract to use bundled Tesseract binary when running as executable."""
import os
import sys

import pytesseract


def configure_tesseract():
    """Configure pytesseract to use bundled Tesseract if running as PyInstaller bundle."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        bundle_dir = sys._MEIPASS

        if sys.platform == 'win32':
            tesseract_path = os.path.join(bundle_dir, 'tesseract', 'tesseract.exe')
        else:
            tesseract_path = os.path.join(bundle_dir, 'tesseract', 'tesseract')

        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

            # Set TESSDATA_PREFIX for language data (must point to tessdata directory itself)
            tessdata_dir = os.path.join(bundle_dir, 'tesseract', 'tessdata')
            if os.path.exists(tessdata_dir):
                os.environ['TESSDATA_PREFIX'] = tessdata_dir
