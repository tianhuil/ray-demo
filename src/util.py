from contextlib import contextmanager
import datetime
import sys

@contextmanager
def timer(msg, out=sys.stdout):
    start = datetime.datetime.now()
    yield
    end = datetime.datetime.now()
    out.write("{}: {}secs\n".format(msg, (end - start).total_seconds()))
