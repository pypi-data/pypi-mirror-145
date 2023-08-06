# ymm
YAML Mimics Makefiles

YMM is one of the first examples of YAAPL: YAML as a Programming Language

YMM uses standard YAML files with a few special conventions to function as a task runner.
In addition to simply creating lists and dictionaries, YMM can execute commands (and thus return values) based on the 'contral character' at the beginning of a line.

## Data Structures

YMM files have a top-level dictionary, whose keys are called "actions."
Type `$ ymm <action>` to execute and return the results of that action, which can be a dictionary or a list.
Dictionaries will set the results of that action to the key, which can be accessed as a `{variable}` in future actions.

There are also two special actions:
* `init` which is always executed before any other action
* `default` which is executed if no action is specified

## Scope

Variables cascade via the following rules

1. Built-in Actions (see `src/ymm/builtin.yml`)
2. Environment variables (which are loaded at runtime)
3. init
4. prior actions
5. current action

## Control Characters

1. '.' run this YMM action
2. '+' execute this Python string (use '"""' for docstrings)
3. '$' run this in the shell
4. '^' pipe the prior result into this shell command
5. '~' pipe the prior result into this jquery path

## Motivation

Because I love YAML, and miss `rake`.
I tried PyPyr, which is brilliant but painfully verbose.
I was going to write a preprocessor, then realized it was simpler to just execute the commands myself.
