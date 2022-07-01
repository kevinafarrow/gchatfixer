"""
Copyright (c) <year>, <copyright holder>
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import datetime as dt
from output import message
from functools import wraps

def timeit(f):               
    @wraps(f)                       
    def wrap(*args, **kw):          

        start = dt.datetime.now()         

        result = f(*args, **kw)        

        end = dt.datetime.now()

        message(f"timeit output:")
        message(f"start time: {start:%D %I:%M:%S %p}", status='yellow', level=1)
        message(f"end time: {end:%D %I:%M:%S %p}", status='yellow', level=1)
        message(f"executed func:{f.__name__}", status='yellow', level=1)
        message(f"elapsed time: {end - start}", status='yellow', level=1)
        return 

    return wrap        