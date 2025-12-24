import os
import tempfile
import threading
import pytest

from stream_counter.counter import Counter


class TestCounter:
    def test_creates_file_if_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            assert not os.path.exists(path)

            Counter(path)

            assert os.path.exists(path)
            with open(path) as f:
                assert f.read() == "0"

    def test_increment_from_zero(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            counter = Counter(path)

            result = counter.increment()

            assert result == 1
            assert counter.get_value() == 1

    def test_increment_from_existing_value(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            with open(path, "w") as f:
                f.write("42")

            counter = Counter(path)
            result = counter.increment()

            assert result == 43
            assert counter.get_value() == 43

    def test_multiple_increments(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            counter = Counter(path)

            for i in range(5):
                counter.increment()

            assert counter.get_value() == 5

    def test_get_value_empty_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            with open(path, "w") as f:
                f.write("")

            counter = Counter(path)
            assert counter.get_value() == 0

    def test_get_value_invalid_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            with open(path, "w") as f:
                f.write("not a number")

            counter = Counter(path)
            assert counter.get_value() == 0

    def test_thread_safety(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "counter.txt")
            counter = Counter(path)
            threads = []

            for _ in range(10):
                t = threading.Thread(target=counter.increment)
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            assert counter.get_value() == 10
