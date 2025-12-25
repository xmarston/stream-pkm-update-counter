import signal
import sys
import threading
from unittest import mock

import numpy as np

from stream_counter.__main__ import main, parse_args


class TestParseArgs:
    def test_parse_required_args(self):
        with mock.patch.object(sys, 'argv', ['prog', '-i', '0', '-f', 'counter.txt', '-p', 'TEST']):
            args = parse_args()
            assert args.inputVideo == 0
            assert args.file == 'counter.txt'
            assert args.phrase == 'TEST'
            assert args.debounce == 15  # default

    def test_parse_all_args(self):
        with mock.patch.object(sys, 'argv', ['prog', '-i', '1', '-f', 'out.txt', '-p', 'HELLO', '-d', '30']):
            args = parse_args()
            assert args.inputVideo == 1
            assert args.file == 'out.txt'
            assert args.phrase == 'HELLO'
            assert args.debounce == 30

    def test_parse_long_form_args(self):
        with mock.patch.object(sys, 'argv', ['prog', '-inputVideo', '2', '-file', 'test.txt', '-phrase', 'WORD', '-debounce', '5']):
            args = parse_args()
            assert args.inputVideo == 2
            assert args.file == 'test.txt'
            assert args.phrase == 'WORD'
            assert args.debounce == 5


class TestMain:
    def test_main_capture_fails(self):
        """Test that main returns 1 when capture fails to open."""
        with mock.patch.object(sys, 'argv', ['prog', '-i', '0', '-f', 'counter.txt', '-p', 'TEST']):
            with mock.patch('stream_counter.__main__.VideoCapture') as mock_capture:
                with mock.patch('stream_counter.__main__.Counter'):
                    with mock.patch('stream_counter.__main__.PhraseDetector'):
                        # Simulate capture failure
                        mock_cap_instance = mock.MagicMock()
                        mock_cap_instance.capture = None
                        mock_cap_instance.__enter__ = mock.MagicMock(return_value=mock_cap_instance)
                        mock_cap_instance.__exit__ = mock.MagicMock(return_value=False)
                        mock_capture.return_value = mock_cap_instance

                        result = main()
                        assert result == 1

    def test_main_capture_not_opened(self):
        """Test that main returns 1 when capture exists but isOpened returns False."""
        with mock.patch.object(sys, 'argv', ['prog', '-i', '0', '-f', 'counter.txt', '-p', 'TEST']):
            with mock.patch('stream_counter.__main__.VideoCapture') as mock_capture:
                with mock.patch('stream_counter.__main__.Counter'):
                    with mock.patch('stream_counter.__main__.PhraseDetector'):
                        mock_cap_instance = mock.MagicMock()
                        mock_cap_instance.capture = mock.MagicMock()
                        mock_cap_instance.capture.isOpened.return_value = False
                        mock_cap_instance.__enter__ = mock.MagicMock(return_value=mock_cap_instance)
                        mock_cap_instance.__exit__ = mock.MagicMock(return_value=False)
                        mock_capture.return_value = mock_cap_instance

                        result = main()
                        assert result == 1

    def test_main_signal_stops_loop(self):
        """Test that main exits gracefully on signal."""
        with mock.patch.object(sys, 'argv', ['prog', '-i', '0', '-f', 'counter.txt', '-p', 'TEST']):
            with mock.patch('stream_counter.__main__.VideoCapture') as mock_capture:
                with mock.patch('stream_counter.__main__.Counter'):
                    with mock.patch('stream_counter.__main__.PhraseDetector'):
                        mock_cap_instance = mock.MagicMock()
                        mock_cap_instance.capture = mock.MagicMock()
                        mock_cap_instance.capture.isOpened.return_value = True
                        mock_cap_instance.read_frame.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
                        mock_cap_instance.__enter__ = mock.MagicMock(return_value=mock_cap_instance)
                        mock_cap_instance.__exit__ = mock.MagicMock(return_value=False)
                        mock_capture.return_value = mock_cap_instance

                        # Capture the signal handler when it's registered
                        captured_handler = None
                        original_signal = signal.signal

                        def capture_signal(signum, handler):
                            nonlocal captured_handler
                            if signum == signal.SIGINT:
                                captured_handler = handler
                            return original_signal(signum, signal.SIG_DFL)

                        with mock.patch('stream_counter.__main__.signal.signal', side_effect=capture_signal):
                            # Run main in a thread and send signal
                            def run_and_signal():
                                # Give main a moment to start, then trigger handler
                                import time
                                time.sleep(0.1)
                                if captured_handler:
                                    captured_handler(signal.SIGINT, None)

                            signal_thread = threading.Thread(target=run_and_signal)
                            signal_thread.start()

                            result = main()
                            signal_thread.join()

                            assert result == 0

    def test_main_handles_none_frame(self):
        """Test that main handles None frames gracefully."""
        with mock.patch.object(sys, 'argv', ['prog', '-i', '0', '-f', 'counter.txt', '-p', 'TEST']):
            with mock.patch('stream_counter.__main__.VideoCapture') as mock_capture:
                with mock.patch('stream_counter.__main__.Counter'):
                    with mock.patch('stream_counter.__main__.PhraseDetector'):
                        mock_cap_instance = mock.MagicMock()
                        mock_cap_instance.capture = mock.MagicMock()
                        mock_cap_instance.capture.isOpened.return_value = True

                        # Return None first, then a valid frame
                        call_count = [0]
                        def read_frame_side_effect():
                            call_count[0] += 1
                            if call_count[0] == 1:
                                return None
                            return np.zeros((100, 100, 3), dtype=np.uint8)

                        mock_cap_instance.read_frame.side_effect = read_frame_side_effect
                        mock_cap_instance.__enter__ = mock.MagicMock(return_value=mock_cap_instance)
                        mock_cap_instance.__exit__ = mock.MagicMock(return_value=False)
                        mock_capture.return_value = mock_cap_instance

                        captured_handler = None
                        original_signal = signal.signal

                        def capture_signal(signum, handler):
                            nonlocal captured_handler
                            if signum == signal.SIGINT:
                                captured_handler = handler
                            return original_signal(signum, signal.SIG_DFL)

                        with mock.patch('stream_counter.__main__.signal.signal', side_effect=capture_signal):
                            def run_and_signal():
                                import time
                                time.sleep(0.2)
                                if captured_handler:
                                    captured_handler(signal.SIGINT, None)

                            signal_thread = threading.Thread(target=run_and_signal)
                            signal_thread.start()

                            result = main()
                            signal_thread.join()

                            assert result == 0
                            # Verify read_frame was called multiple times (retry after None)
                            assert call_count[0] >= 2

    def test_main_calls_detector(self):
        """Test that main calls the detector with frames."""
        with mock.patch.object(sys, 'argv', ['prog', '-i', '0', '-f', 'counter.txt', '-p', 'TEST']):
            with mock.patch('stream_counter.__main__.VideoCapture') as mock_capture:
                with mock.patch('stream_counter.__main__.Counter'):
                    with mock.patch('stream_counter.__main__.PhraseDetector') as mock_detector:
                        mock_cap_instance = mock.MagicMock()
                        mock_cap_instance.capture = mock.MagicMock()
                        mock_cap_instance.capture.isOpened.return_value = True
                        test_frame = np.zeros((100, 100, 3), dtype=np.uint8)
                        mock_cap_instance.read_frame.return_value = test_frame
                        mock_cap_instance.__enter__ = mock.MagicMock(return_value=mock_cap_instance)
                        mock_cap_instance.__exit__ = mock.MagicMock(return_value=False)
                        mock_capture.return_value = mock_cap_instance

                        mock_detector_instance = mock.MagicMock()
                        mock_detector.return_value = mock_detector_instance

                        captured_handler = None
                        original_signal = signal.signal

                        def capture_signal(signum, handler):
                            nonlocal captured_handler
                            if signum == signal.SIGINT:
                                captured_handler = handler
                            return original_signal(signum, signal.SIG_DFL)

                        with mock.patch('stream_counter.__main__.signal.signal', side_effect=capture_signal):
                            def run_and_signal():
                                import time
                                time.sleep(0.15)
                                if captured_handler:
                                    captured_handler(signal.SIGINT, None)

                            signal_thread = threading.Thread(target=run_and_signal)
                            signal_thread.start()

                            result = main()
                            signal_thread.join()

                            assert result == 0
                            # Verify detector was called
                            mock_detector_instance.analyze_frame_async.assert_called()
