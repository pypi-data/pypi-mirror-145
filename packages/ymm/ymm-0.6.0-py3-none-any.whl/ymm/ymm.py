import subprocess
import sys
from .keys import *
from .scope import Scope

def is_dict(d): return isinstance(d, dict)

class YMM:
    def __init__(self, yaml):
        self.env = Scope()
        self.env.push("ymm", yaml)
        self.actions = self.env.actions()
        self.printOutput = True

    def run(self,action=DEFAULT_ACTION, hide=True):
        currentOutput = self.printOutput
        if hide: self.printOutput = False
        if not action in self.actions:
            msg = f'ERROR: action [{action}] not found' if action != DEFAULT_ACTION else "Exiting"
            sys.exit(msg)
        self.env.push(action)
        commands = self.env.get(action)
        results = [self.execute(v, k) for k,v in commands.items()] if is_dict(commands) else [self.execute(cmd, f'{action}#{i}') for i,cmd in enumerate(commands)]
        if hide: self.printOutput = currentOutput
        return results

    def execute(self, cmd, key):
        self.log(f'! {key}: {cmd}', "execute")
        if not isinstance(cmd,str): return self.save(cmd, key)
        if cmd[0] == kCall: return "\n".join(self.run(cmd[1:]))
        variables = self.env.flatstr()
        sub = cmd.format(**variables)
        commands = sub.split(" ")
        self.log(commands, "commands")
        result = subprocess.run(commands, stdout=subprocess.PIPE)
        msg = result.stdout.decode("utf-8").strip()
        if msg and isinstance(msg,str): return self.save(msg, key)
        return msg

    def save(self, msg, key):
        if self.printOutput: print(f'# {key}: {msg}')
        #if kLast in self.env: self.env[kPrior] = self.env[kLast]
        self.env.set(kLast, msg)
        self.env.set(key, msg)
        return msg

    def log(self, action, caption=False):
        if self.env.get(kLog, False):
            if caption: print(f'DEBUG_{caption}')
            print(f'DEBUG {action}')
