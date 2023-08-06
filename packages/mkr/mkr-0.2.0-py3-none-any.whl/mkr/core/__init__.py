# -*- coding: utf-8 -*-
from mkr.core.mk import MicroKernel
from mkr.core.mkp import MKPluginManager

"""
example1:
from mkr import MicroKernel

mk = MicroKernel(your framework as the inner framework)

print(mk.list())

mk.start()

# mk[plugin_name].func()  # pyfn 'func' in your plugin 

If you do not know what to do with it. u could try the package 'ekr'(combine mkr and efr) which use eventFramework as the MicroKernel's inner core.
"""