import os
import sys
from dataclasses import dataclass
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.','./src','..','../src')))

import ymm
TEST_FILE="tests/test.yml"
FIRST_KEY='install'

@dataclass
class Args:
    actions: list[str]
    file: str = TEST_FILE
    list: bool = False
    no_init: bool = False
