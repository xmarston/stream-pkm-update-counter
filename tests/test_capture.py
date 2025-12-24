from unittest.mock import patch, MagicMock
import numpy as np

import pytest

from stream_counter.capture import VideoCapture


class TestVideoCapture:
    def test_open_success(self):
        with patch("cv2.VideoCapture") as mock_cv:
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cv.return_value = mock_cap

            capture = VideoCapture(0)
            result = capture.open()

            assert result is True
            mock_cv.assert_called_once_with(0)

    def test_open_failure(self):
        with patch("cv2.VideoCapture") as mock_cv:
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = False
            mock_cv.return_value = mock_cap

            capture = VideoCapture(0)
            result = capture.open()

            assert result is False

    def test_read_frame_success(self):
        with patch("cv2.VideoCapture") as mock_cv, \
             patch("cv2.cvtColor") as mock_cvt:
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
            mock_cv.return_value = mock_cap
            mock_cvt.return_value = np.zeros((480, 640), dtype=np.uint8)

            capture = VideoCapture(0)
            capture.open()
            frame = capture.read_frame()

            assert frame is not None
            mock_cvt.assert_called_once()

    def test_read_frame_failure(self):
        with patch("cv2.VideoCapture") as mock_cv:
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cap.read.return_value = (False, None)
            mock_cv.return_value = mock_cap

            capture = VideoCapture(0)
            capture.open()
            frame = capture.read_frame()

            assert frame is None

    def test_read_frame_without_open(self):
        capture = VideoCapture(0)
        frame = capture.read_frame()

        assert frame is None

    def test_release(self):
        with patch("cv2.VideoCapture") as mock_cv:
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cv.return_value = mock_cap

            capture = VideoCapture(0)
            capture.open()
            capture.release()

            mock_cap.release.assert_called_once()
            assert capture.capture is None

    def test_context_manager(self):
        with patch("cv2.VideoCapture") as mock_cv:
            mock_cap = MagicMock()
            mock_cap.isOpened.return_value = True
            mock_cv.return_value = mock_cap

            with VideoCapture(0) as capture:
                assert capture.capture is not None

            mock_cap.release.assert_called_once()
