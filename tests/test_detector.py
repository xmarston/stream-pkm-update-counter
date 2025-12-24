import os
import time
import tempfile
from unittest.mock import patch, MagicMock

from stream_counter.counter import Counter
from stream_counter.detector import PhraseDetector


class TestPhraseDetector:
    def test_detects_phrase_and_increments(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            counter = Counter(path)
            detector = PhraseDetector("SHINY", counter, debounce_seconds=0)

            with patch("pytesseract.image_to_string", return_value="Found SHINY pokemon!"):
                detector.analyze_frame(MagicMock())

            assert counter.get_value() == 1

    def test_ignores_frame_without_phrase(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            counter = Counter(path)
            detector = PhraseDetector("SHINY", counter, debounce_seconds=0)

            with patch("pytesseract.image_to_string", return_value="Normal pokemon"):
                detector.analyze_frame(MagicMock())

            assert counter.get_value() == 0

    def test_debounce_prevents_rapid_increments(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            counter = Counter(path)
            detector = PhraseDetector("SHINY", counter, debounce_seconds=10)
            detector.last_found = time.time() - 5  # 5 seconds ago

            with patch("pytesseract.image_to_string", return_value="SHINY"):
                detector.analyze_frame(MagicMock())

            assert counter.get_value() == 0  # Debounced

    def test_debounce_allows_after_timeout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            counter = Counter(path)
            detector = PhraseDetector("SHINY", counter, debounce_seconds=1)
            detector.last_found = time.time() - 2  # 2 seconds ago

            with patch("pytesseract.image_to_string", return_value="SHINY"):
                detector.analyze_frame(MagicMock())

            assert counter.get_value() == 1

    def test_case_sensitive_matching(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            counter = Counter(path)
            detector = PhraseDetector("SHINY", counter, debounce_seconds=0)

            with patch("pytesseract.image_to_string", return_value="shiny"):
                detector.analyze_frame(MagicMock())

            assert counter.get_value() == 0  # Case mismatch

    def test_analyze_frame_async_returns_thread(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            counter = Counter(path)
            detector = PhraseDetector("SHINY", counter, debounce_seconds=0)

            with patch("pytesseract.image_to_string", return_value="SHINY"):
                thread = detector.analyze_frame_async(MagicMock())
                thread.join()

            assert counter.get_value() == 1
