import logging
import cv2

logger = logging.getLogger(__name__)


class VideoCapture:
    def __init__(self, device_id):
        self.device_id = device_id
        self.capture = None

    def open(self):
        """Open the video capture device."""
        self.capture = cv2.VideoCapture(self.device_id)
        if not self.capture.isOpened():
            logger.error("Failed to open video capture device %d", self.device_id)
            return False
        logger.info("Opened video capture device %d", self.device_id)
        return True

    def read_frame(self):
        """Read a frame and return it as grayscale. Returns None on failure."""
        if self.capture is None:
            return None
        ret, frame = self.capture.read()
        if not ret or frame is None:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def release(self):
        """Release the video capture device."""
        if self.capture is not None:
            self.capture.release()
            self.capture = None
            logger.info("Released video capture device")

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False
