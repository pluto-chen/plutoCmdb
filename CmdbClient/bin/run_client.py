#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os,sys,platform

if platform.system() == 'Windows':
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])

else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])

sys.path.append(BASE_DIR)

from core import client_handle

if __name__ == '__main__':
    client_handle.ArgvHandler(sys.argv)
