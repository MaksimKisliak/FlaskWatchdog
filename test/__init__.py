import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_tests():
    pytest.main(['-vv', 'tests'])


if __name__ == '__main__':
    run_tests()
