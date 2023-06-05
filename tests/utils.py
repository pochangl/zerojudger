import contextlib
import tempfile

@contextlib.contextmanager
def createfile(str):
    with tempfile.NamedTemporaryFile() as infile:
        infile.write(str.encode())
        infile.seek(0)
        yield infile