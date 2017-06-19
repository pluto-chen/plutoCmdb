#!/usr/bin/env python
# -*- coding:utf-8 -*-


import platform,os,json
from plugins import plugin_api
from conf import settings
import urllib.parse,urllib.request




class ArgvHandler(object):

    def __init__(self,argvs):
        self.sys_argv = argvs
        self.parse_argv()

    def help_msg(self):
        msg = '''
        collect_data
        run_forever
        get_asset_id
        report_asset
        '''
        print(msg)

    def parse_argv(self):
        if len(self.sys_argv) <=1:
            self.help_msg()
        else:
            if hasattr(self,self.sys_argv[1]):
                func = getattr(self,self.sys_argv[1])
                func()
            else:
                self.help_msg()

    def collect_data(self):
        os_sys = platform.system()
        if hasattr(self,os_sys):
            func = getattr(self,os_sys)
            client_data = func()
            return client_data
        else:
            exit("Error: os %s is not support"%os_sys)

    def __post_data(self,post_url,data,method):
        if post_url in settings.Params['urls']:
            if type(settings.Params['port']) is int:
                url = "http://%s:%s%s" % (settings.Params['server'],settings.Params['port'],settings.Params['urls'][post_url])
            else:
                url = "http://%s%s" % (settings.Params['server'],settings.Params['urls'][post_url])
            print(url)

            if method == 'post':
                post_data = urllib.parse.urlencode(data).encode('utf-8')

                req = urllib.request.Request(url=url,data=post_data)
                res_data = urllib.request.urlopen(req,timeout=settings.Params['request_timeout'])
                reply_data = res_data.read().decode("utf-8")
                print('read取到的数据------------>',reply_data)
                reply_data = json.loads(reply_data)
                print(reply_data)




    def report_asset(self):
        client_data = self.collect_data()
        asset_id_file = settings.Params['asset_id']
        if os.path.isfile(asset_id_file):
            asset_id = open(asset_id_file).read().strip()
            if asset_id.isdigit():
                client_data['asset_id'] = asset_id
                post_url = 'asset_report'
            else:
                client_data['asset_id'] = None
                post_url = 'asset_report_with_noid'
        else:
            client_data['asset_id'] = None
            post_url = 'asset_report_with_noid'

        client_data['name'] = settings.Params['name']
        client_data['project_id'] = settings.Params['project_id']
        client_data['server_type'] = settings.Params['server_type']
        data = {'asset_data':json.dumps(client_data)}

        reply = self.__post_data(post_url,data,method='post')




    def Windows(self):

        windata = plugin_api.windowsdata()
        print(windata)
        return windata

    def Linux(self):

        lindata = plugin_api.linuxdata()
        return lindata






