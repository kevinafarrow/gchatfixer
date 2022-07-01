"""
Copyright (c) <year>, <copyright holder>
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. 
"""

import pandas as pd
from colorama import Fore
from pprint import pformat
from jinja2 import Template

def message_string(message, level, tabs=4, status='none'):
    color = {"success": Fore.GREEN, "error": Fore.RED, "attention": Fore.CYAN, "none": Fore.RESET, "yellow": Fore.YELLOW, "magenta": Fore.MAGENTA}
    tm = Template("{{ color }}[{{ '!' if status == 'error' else '+' if level == 0 else '-' }}] {{ ' ' * tabs * level }} {{ message }}{{ reset }}")
    x = locals()
    x['color'] = color[status]
    print(tm.render({**x, 'reset': Fore.RESET}))

def message_list(lst, level, tabs=4, status='none'):
    for l in lst:
        message_string(l, level=level, tabs=tabs, status=status)

def message_dict(dct, level, tabs=4, status='none'):
    for k, v in dct.items():
        message_string(f"{k}: {v}", level=level, tabs=tabs, status=status)

def message_pd_series(series, level, tabs=4, status='none'):
    for row in pformat(series).splitlines():
        message_string(row, level=level, tabs=tabs, status=status)

def message_pd_df(df, level, tabs=4, status='none', show_all=False):
    # Change terminal width
    og_display_width = pd.get_option('display.width')
    #message(f"ORIGINAL DISPLAY WIDTH: {pd.get_option('display.width')}", level=0, status='attention')
    pd.set_option('display.width', (og_display_width - (level * tabs) - 4))
    #message(f"NEW DISPLAY WIDTH: {pd.get_option('display.width')}", level=0, status='attention')
    if show_all:
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_columns', None)
    for row in pformat(df).splitlines():
        message_string(row, level=level, tabs=tabs, status=status)
    if show_all:
        pd.reset_option('display.max_colwidth')
        pd.reset_option('display.max_columns')
    #pd.set_option('display.width', og_display_width)
    #message(f"RESET DISPLAY WIDTH: {pd.get_option('display.width')}", level=0, status='attention')

def message(thing, level=0, tabs=4, status='none', show_all=False):
    lookup = {
        "<class 'str'>": message_string,
        "<class 'list'>": message_list,
        "<class 'numpy.ndarray'>": message_list,
        "<class 'dict'>": message_dict,
        "<class 'pandas.core.series.Series'>": message_pd_series,
        "<class 'pandas.core.frame.DataFrame'>": message_pd_df,
        "<class 'geopandas.geodataframe.GeoDataFrame'>": message_pd_df,
        "<class 'dict_keys'>": message_list,
        }
    func = lookup[str(type(thing))]
    if show_all:
        func(thing, level=level, tabs=tabs, status=status, show_all=show_all)
    else:
        func(thing, level=level, tabs=tabs, status=status)