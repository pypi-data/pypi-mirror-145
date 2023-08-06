# -*- coding: utf-8 -*-
from mkr.core.mk import MicroKernel
from mkr.core.mkp import MicroKernelPluginManager

"""
example1:
from mkr import MicroKernel

mk = MicroKernel(your framework as the inner framework)

print(mk.list())

mk.start()

# mk[plugin_name].func()  # pyfn 'func' in your plugin 

"""