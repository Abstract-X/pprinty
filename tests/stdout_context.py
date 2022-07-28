from io import StringIO
import contextlib


class StdoutContext:

    def __init__(self):
        self._redirect_stdout = None
        self._stdout = None

    def __enter__(self):
        self._redirect_stdout = contextlib.redirect_stdout(StringIO())
        self._stdout = self._redirect_stdout.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._redirect_stdout.__exit__(exc_type, exc_val, exc_tb)

    def get_value(self) -> str:
        return self._stdout.getvalue()
