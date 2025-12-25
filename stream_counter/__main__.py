import argparse
import logging
import signal
import threading

from .counter import Counter
from .capture import VideoCapture
from .detector import PhraseDetector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Stream counter for shiny hunting automation")
    parser.add_argument("-inputVideo", "-i", type=int, required=True, help="Capture device number")
    parser.add_argument("-file", "-f", type=str, required=True, help="Counter file path")
    parser.add_argument("-phrase", "-p", type=str, required=True, help="Phrase to detect")
    parser.add_argument("-debounce", "-d", type=int, default=15, help="Seconds between detections (default: 15)")
    return parser.parse_args()


def main():
    stop_event = threading.Event()

    def signal_handler(signum, frame):
        stop_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    args = parse_args()

    counter = Counter(args.file)
    detector = PhraseDetector(args.phrase, counter, args.debounce)

    with VideoCapture(args.inputVideo) as capture:
        if capture.capture is None or not capture.capture.isOpened():
            return 1

        logger.info("Starting detection for phrase: '%s'", args.phrase)
        logger.info("Press Ctrl+C to stop")

        while not stop_event.is_set():
            frame = capture.read_frame()
            if frame is None:
                logger.warning("Failed to read frame, retrying...")
                stop_event.wait(0.1)
                continue

            detector.analyze_frame_async(frame)
            stop_event.wait(1)

    logger.info("Shutting down...")
    return 0


if __name__ == "__main__":
    exit(main())
