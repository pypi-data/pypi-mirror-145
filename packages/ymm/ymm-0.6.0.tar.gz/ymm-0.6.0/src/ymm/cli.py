import os, re
import argparse
#import pkg_resources
from importlib.metadata import version
from pathlib import Path
from .keys import *
from .file import dict_file
from .ymm import YMM

__version__ = version("ymm")

parser = argparse.ArgumentParser(description='Run actions.')
parser.add_argument('actions', metavar='action', nargs='*',
                    help='actions from <file> to execute')
parser.add_argument('-d','--debug', action='store_true',
                    help='print debugging information')
parser.add_argument('-f','--file', default=DEFAULT_FILE,
                    help='YAML file of actions')
parser.add_argument('-l','--list', action='store_true',
                    help='list available actions')
parser.add_argument('-n','--no-init', action='store_true',
                    help='skip init action')
parser.add_argument('-s','--silent', action='store_true',
                    help='silence outputs')
parser.add_argument('-v','--version', action='version',
                    version=f'%(prog)s {__version__}')

def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

def load_file(yaml_file=DEFAULT_FILE):
    raw_yaml = dict_file(yaml_file)
    return YMM(raw_yaml)

def print_actions(keys, list_actions):
    if list_actions:
        for key in keys:
            print(f' - {key}')

def init(ymm, no_init, has_key):
    ymm.log(f'no_init:{no_init} has_key:{has_key}', "init")
    if (not no_init) & has_key:
        ymm.run(INIT_ACTION)

def exec(ymm, args):
    ymm.log(args, "args")
    ymm.env.args(args)
    keys = ymm.actions
    ymm.log(keys, "keys")
    print_actions(keys, args.list)
    init(ymm, args.no_init, INIT_ACTION in keys)
    actions = args.actions
    results=[]
    for action in actions:
        print(f'; {action}')
        results.append(ymm.run(action))
    return flatten(results)

def main():
    args = parser.parse_args()
    #print(dir(args))
    ymm = load_file(args.file)
    if args.silent: ymm.printOutput = False
    exec(ymm, args)
    return 0
#main()
