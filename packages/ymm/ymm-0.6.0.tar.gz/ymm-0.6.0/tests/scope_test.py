#!/usr/bin/env python3
import pytest
from .context import *

@pytest.fixture
def s():
    ctx = ymm.Scope()
    return ctx

def test_scope(s):
    #print(dir(s))
    assert s

def test_builtin(s):
    r = s.get(FIRST_KEY)
    assert "-r" in r[0]

def test_env(s):
    r = s.get("PATH")
    assert "bin" in r

def test_non(s):
    r = s.get(42)
    assert not r

def test_id(s):
    r = s.get(ymm.kID)
    assert "env" in r

def test_set(s):
    r = s.set(ymm.kLast, "last")
    q = s.get(ymm.kLast)
    assert "last" in q

def test_flat(s):
    ctx = s.flat()
    assert "env" in ctx[ymm.kID]
