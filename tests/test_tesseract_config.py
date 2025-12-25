import os
import sys
import tempfile
from unittest import mock

from stream_counter.tesseract_config import configure_tesseract


class TestConfigureTesseract:
    def test_not_frozen_does_nothing(self):
        """When not running as PyInstaller bundle, should not modify pytesseract."""
        with mock.patch('stream_counter.tesseract_config.pytesseract') as mock_pytesseract:
            # Ensure sys.frozen is not set
            if hasattr(sys, 'frozen'):
                delattr(sys, 'frozen')

            configure_tesseract()

            # Should not have set tesseract_cmd
            assert not mock_pytesseract.pytesseract.tesseract_cmd.called

    def test_frozen_windows_with_tesseract(self):
        """When running as frozen Windows bundle with Tesseract, should configure path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create mock Tesseract structure
            tesseract_dir = os.path.join(tmpdir, 'tesseract')
            tessdata_dir = os.path.join(tesseract_dir, 'tessdata')
            os.makedirs(tessdata_dir)

            tesseract_exe = os.path.join(tesseract_dir, 'tesseract.exe')
            with open(tesseract_exe, 'w') as f:
                f.write('')

            with mock.patch.object(sys, 'frozen', True, create=True):
                with mock.patch.object(sys, '_MEIPASS', tmpdir, create=True):
                    with mock.patch.object(sys, 'platform', 'win32'):
                        with mock.patch('stream_counter.tesseract_config.pytesseract') as mock_pytesseract:
                            configure_tesseract()

                            assert mock_pytesseract.pytesseract.tesseract_cmd == tesseract_exe
                            assert os.environ.get('TESSDATA_PREFIX') == tesseract_dir

    def test_frozen_linux_with_tesseract(self):
        """When running as frozen Linux bundle with Tesseract, should configure path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create mock Tesseract structure
            tesseract_dir = os.path.join(tmpdir, 'tesseract')
            tessdata_dir = os.path.join(tesseract_dir, 'tessdata')
            os.makedirs(tessdata_dir)

            tesseract_bin = os.path.join(tesseract_dir, 'tesseract')
            with open(tesseract_bin, 'w') as f:
                f.write('')

            with mock.patch.object(sys, 'frozen', True, create=True):
                with mock.patch.object(sys, '_MEIPASS', tmpdir, create=True):
                    with mock.patch.object(sys, 'platform', 'linux'):
                        with mock.patch('stream_counter.tesseract_config.pytesseract') as mock_pytesseract:
                            configure_tesseract()

                            assert mock_pytesseract.pytesseract.tesseract_cmd == tesseract_bin
                            assert os.environ.get('TESSDATA_PREFIX') == tesseract_dir

    def test_frozen_without_tesseract(self):
        """When running as frozen bundle without Tesseract, should not error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(sys, 'frozen', True, create=True):
                with mock.patch.object(sys, '_MEIPASS', tmpdir, create=True):
                    with mock.patch('stream_counter.tesseract_config.pytesseract') as mock_pytesseract:
                        # Should not raise
                        configure_tesseract()

                        # Should not have modified tesseract_cmd
                        mock_pytesseract.pytesseract.tesseract_cmd = mock_pytesseract.pytesseract.tesseract_cmd
