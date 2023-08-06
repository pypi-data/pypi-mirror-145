#!/usr/bin/env python3
import pytest
from .context import *

@pytest.fixture
def y():
    return ymm.load_file(TEST_FILE)

def test_load(y):
    assert y
    assert y.env
    assert y.env.get(FIRST_KEY)

def test_actions(y):
    a = y.env.actions()
    assert a
    assert FIRST_KEY in a
    assert "PATH" not in a

def test_run(y):
    result = y.run(FIRST_KEY)
    assert FIRST_KEY in result[0]
    key = f'{FIRST_KEY}#0'
    value = y.env.get(key)
    assert value

def test_dict(y):
    ri = y.run("init")
    variables = y.env.flatstr()
    d = variables["DICT"]
    assert ':"' in d

    result = y.run("echo")
    assert ':"' in result[0]
    jval = y.env.get("RESULT")
