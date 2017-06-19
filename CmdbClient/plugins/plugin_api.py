#!/usr/bin/env python
# -*- coding:utf-8 -*-


from plugins.linux import linuxcollect
from plugins.windows import windowscollect


def linuxdata():

    data = linuxcollect.collect()
    return data

def windowsdata():

    data = windowscollect.collect()
    return data