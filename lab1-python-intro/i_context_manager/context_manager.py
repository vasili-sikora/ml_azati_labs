import io
import sys
import time
from typing import TextIO


class Timer:
    """Context manager for measuring execution time."""

    def __init__(self):
        self._start_time = None
        self.elapsed = 0.0

    def __enter__(self):
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._start_time is not None:
            self.elapsed = time.perf_counter() - self._start_time


class FileManager:
    """Context manager for file operations that ensures proper cleanup."""

    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file is not None:
            self.file.close()


class OutputCapture:
    """Context manager that captures stdout and stderr output."""

    def __init__(self):
        self._old_stdout = None
        self._old_stderr = None
        self.stdout = ""
        self.stderr = ""

    def __enter__(self):
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr

        self._stdout_buffer = io.StringIO()
        self._stderr_buffer = io.StringIO()

        sys.stdout = self._stdout_buffer
        sys.stderr = self._stderr_buffer

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr

        self.stdout = self._stdout_buffer.getvalue()
        self.stderr = self._stderr_buffer.getvalue()

        self._stdout_buffer.close()
        self._stderr_buffer.close()


# Примеры использования (для самопроверки после реализации):
#
# import os
# import sys
#
# # Timer
# with Timer() as timer:
#     time.sleep(0.1)
# print(f"Elapsed: {timer.elapsed:.2f}s")
#
# # FileManager
# with FileManager('demo.txt', 'w') as f:
#     f.write('Hello!')
# with FileManager('demo.txt', 'r') as f:
#     print(f.read())
# os.remove('demo.txt')
#
# # OutputCapture
# with OutputCapture() as captured:
#     print("Test output")
# print(f"Captured: {captured.stdout}")
#
# # Вложенные контекстные менеджеры
# with Timer() as t:
#     with OutputCapture() as cap:
#         print("Nested!")
# print(f"Time: {t.elapsed:.2f}s, Output: {cap.stdout.strip()}")

if __name__ == "__main__":
    import os
    import sys

    # Timer
    with Timer() as timer:
        time.sleep(0.1)
    print(f"Elapsed: {timer.elapsed:.2f}s")

    # FileManager
    with FileManager('demo.txt', 'w') as f:
        f.write('Hello!')
    with FileManager('demo.txt', 'r') as f:
        print(f.read())
    os.remove('demo.txt')

    # OutputCapture
    with OutputCapture() as captured:
        print("Test output")
    print(f"Captured: {captured.stdout}")

    # Вложенные контекстные менеджеры
    with Timer() as t:
        with OutputCapture() as cap:
            print("Nested!")
    print(f"Time: {t.elapsed:.2f}s, Output: {cap.stdout.strip()}")
