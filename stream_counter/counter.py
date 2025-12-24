import logging
import os
import threading

logger = logging.getLogger(__name__)


class Counter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lock = threading.Lock()
        self._ensure_file()

    def _ensure_file(self):
        """Create counter file with initial value 0 if it doesn't exist."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                f.write("0")
            logger.info("Created counter file: %s", self.file_path)

    def increment(self):
        """Increment the counter and return the new value."""
        with self.lock:
            try:
                with open(self.file_path, "r+") as f:
                    content = f.read().strip()
                    value = int(content) if content else 0
                    value += 1
                    f.seek(0)
                    f.write(str(value))
                    f.truncate()
                    logger.info("Counter updated: %d", value)
                    return value
            except IOError as e:
                logger.error("File not accessible: %s", e)
            except ValueError as e:
                logger.error("Invalid counter value in file: %s", e)
        return None

    def get_value(self):
        """Get the current counter value."""
        try:
            with open(self.file_path, "r") as f:
                content = f.read().strip()
                return int(content) if content else 0
        except (IOError, ValueError):
            return 0
