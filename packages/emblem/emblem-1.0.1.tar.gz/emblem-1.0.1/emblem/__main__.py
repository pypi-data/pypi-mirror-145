# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
CLI
---
"""


import argparse

from emblem import coverage


def add(cli, name, help='', nargs=1):
    cli.add_argument(
        f'--{name}',
        nargs=nargs,
        default=None,
        help=help
    )


def main():

    CLI = argparse.ArgumentParser()

    CLI.add_argument(
        'coverage',
        help='code coverage percentage'
    )

    # Emblem arguments
    e_args = {'label':    ['badge label'],
              'style':    ['badge style'],
              'logo':     ['badge logo'],
              'fname':    ['svg file name'],
              'colors':   ['colors from which to generate a linear segmented colormap, low to high', '*'],
              'cmap':     ['matplotlib colormap']}
    # Runtime arguments
    r_args = {'silence':  ['print shields.io url']}

    _args = {**e_args, **r_args}
    for arg in _args.keys():
        add(CLI, arg, *_args[arg])

    # Parse input
    _input = CLI.parse_args()
    
    # Create input dictionary
    kwargs = {}

    for arg in e_args.keys():
        if getattr(_input, arg) is not None:
            v = getattr(_input, arg)
            if isinstance(v, list) and len(v) == 1:
                v = v[0]
            kwargs[arg] = v

    # Emblem
    q = coverage(_input.coverage, **kwargs)

    if not _input.silence:
        print(f'\n{q}\n')


if __name__ == '__main__':
    main()