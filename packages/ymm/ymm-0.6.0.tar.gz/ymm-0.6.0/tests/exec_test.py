#!/usr/bin/env python3
import pytest
from .context import *

FIRST_KEY='install'

@pytest.fixture
def y():
    return ymm.load_file(TEST_FILE)

def test_exec(y):
    #print(dir(ymm))
    args = Args(['install'])
    result = ymm.exec(y,args)
    #print(result)
    assert FIRST_KEY in result[0]
