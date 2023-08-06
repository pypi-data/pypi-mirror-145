# -*- coding: utf-8 -*-
import os

def get_version():
    HERE = os.path.dirname(__file__)
    with open(os.path.join(HERE,'__version__.py')) as f:
        return f.read().strip()
