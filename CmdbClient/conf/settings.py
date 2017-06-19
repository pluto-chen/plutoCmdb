#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Params = {
    "server": "127.0.0.1",
    "server_type":"Virtual",
    "port":8000,
    "project_id":1,
    "name":"panglaoye",
    'request_timeout':30,
    "urls":{
          "asset_report_with_noid":"/asset/asset_report_with_noid/",
          "asset_report":"/asset/asset_report/",
        },
    'asset_id': '%s/conf/.asset_id' % BaseDir,
    'log_file': '%s/logs/run_log' % BaseDir,

    'auth':{
        'user':'lijie3721@126.com',
        'token': 'abc'
        },
}