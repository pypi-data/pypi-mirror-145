from contextlib import contextmanager
import blinker
from collections.abc import Iterable

@contextmanager
def captured_signals(app,signals=None):

    if not signals:
        signals = blinker.signal.__self__.values()
    recorded = []
    if not isinstance(signals,Iterable):
        signals = [signals]
    for s in signals:

        def record(sender, *args,**kwargs):
            recorded.append((s, sender, args, kwargs))
        s.connect(record, app)
    try:
        yield recorded
    finally:
        s.disconnect(record, app)

def init_app(app):
    if not app.testing:
        return