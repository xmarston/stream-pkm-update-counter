import logging
import time
import threading
import pytesseract

logger = logging.getLogger(__name__)


class PhraseDetector:
    def __init__(self, phrase, counter, debounce_seconds=15):
        self.phrase = phrase
        self.counter = counter
        self.debounce_seconds = debounce_seconds
        self.last_found = time.time()
        self.lock = threading.Lock()

    def analyze_frame(self, img):
        """Analyze a frame for the target phrase. Thread-safe."""
        text = pytesseract.image_to_string(img)
        if self.phrase in text:
            self._on_phrase_detected()

    def _on_phrase_detected(self):
        """Handle phrase detection with debouncing."""
        now = time.time()
        with self.lock:
            if now - self.last_found >= self.debounce_seconds:
                self.last_found = now
                self.counter.increment()

    def analyze_frame_async(self, img):
        """Analyze a frame in a background thread."""
        t = threading.Thread(target=self.analyze_frame, args=(img,), daemon=True)
        t.start()
        return t
