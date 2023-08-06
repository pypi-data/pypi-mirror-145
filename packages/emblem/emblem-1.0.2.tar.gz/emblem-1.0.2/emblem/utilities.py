# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Utilities
---------
"""


import requests


def save_svg(url, fname):

    svg = requests.get(url).text

    with open(fname, 'w') as f:
        f.write(svg)
