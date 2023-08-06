# -*- coding: utf-8 -*-
import os

module_path = os.path.dirname(os.path.abspath(__file__))
tests = [
    f for f in os.listdir(module_path) if f.endswith(".py") and f != "__init__.py"
]
__all__ = tests
print(
    "Imported tests: %s" % ", ".join(tests)
    if tests
    else "No tests avaiable in the tests directory."
)
