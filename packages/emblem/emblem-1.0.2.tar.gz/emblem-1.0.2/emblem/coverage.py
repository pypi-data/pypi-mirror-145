# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Coverage
--------
"""


import re

from matplotlib.cm import get_cmap
from matplotlib.colors import to_rgb, to_hex, LinearSegmentedColormap

from emblem.utilities import save_svg


def custom_map(
    colors= ['darkred', 'lightgreen'],
    weights=None
    ):

    if weights is not None: colors = list(zip(weights, colors))

    m = LinearSegmentedColormap.from_list(colors=colors, 
                                          name='coverageMap')

    return m


def coverage(
    coverage,
    label= 'Coverage',
    style= 'for-the-badge',
    logo=  'pytest',
    fname ='./coverage.svg',
    colors=['#b00909', '#3ade65'],
    cmap=  None
    ):
    """
    ``label``
    Badge label

    ``style``
    Badge style

    ``logo``
    Badge logo to be chosen from the standard set below 
    or simple-icons (https://simpleicons.org/).
        
        * bitcoin
        * dependabot
        * gitlab
        * npm
        * paypal
        * serverfault
        * stackexchange
        * superuser
        * telegram
        * travis    
    """

    # Determine contents of coverage string
    percentage = re.findall('\d+\.*\d*', coverage)

    if not percentage: 
        percentage = 0
    else:
        percentage = float(percentage[0])
        coverage = f'{percentage} %25'

    if cmap is not None:
        cmap = get_cmap(cmap)
    else:
        cmap = custom_map(colors)

    color = to_hex(cmap(percentage/100))[1:]
    
    # Syntax
    style = f"?style={style}" if style else ""
    logo  = f"&logo={logo}" if logo else ""
    
    shield = f'https://img.shields.io/badge/{label}-{coverage}-{color}{style}{logo}'

    save_svg(shield, fname)

    return shield
