#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from Cmdb import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class Asset(object):

    def __init__(self,request):
        self.request = request
        self.reply_msg = {
            'Info':[],
            'Warning':[],
            'Error':[]
        }
        self.required_fields = ['asset_id','asset_type','name']

    def msg_reply(self,msg_type,msg_title,msg_content):
        self.reply_msg[msg_type].append({msg_title:msg_content})
        return self.reply_msg

    def required_check(self,data,if_has_assetid=True):
        for field in self.required_fields:
            if field not in data:
                self.msg_reply('Error','AssetDataValueError','The field:[%s] is required'%field)
        else:
            if self.reply_msg['Error']:
                return False
        try:
            if if_has_assetid:
                self.asset_obj = models.Asset.objects.get(id=data['asset_id'],name=data['name'])
            else:
                self.asset_obj = models.Asset.objects.get(project_id=data['project_id'],name=data['name'])
            return True
        except ObjectDoesNotExist as e:
            self.msg_reply('error', 'ObjectDoesNotExist','Asset:%s sn:%s the asset is bot exist' % (data['asset_id'], data['sn']))
            return False

    def data_is_avlid(self):
        print(self.request.POST)
        data = self.request.POST.get('asset_data')
        if data:
            try:
                data = json.loads(data)
                print('检验的数据-------------->',data)
                self.required_check(data)
                self.reporting_data = data
                if not self.reply_msg['Error']:
                    return True
            except ValueError as e:
                self.msg_reply('error', 'ReportDataValueError', 'There is no reporting data')

        else:
            self.msg_reply('Error','ReportDataError','There is no reporting data')

    def data_input(self):
        asset_type = self.reporting_data['asset_type']
        if hasattr(self.asset_obj,asset_type):
            print('资产信息存在,更新信息')
            self._update_asset()
        else:
            print('新的资产信息,开始创建')
            self._create_asset()

    def filter_with_projectname(self):

        data = self.request.POST.get('asset_data')
        if data:
            try:
                data = json.loads(data)
                if self.required_check(data,if_has_assetid=False):
                    reply_data = {'asset_id':self.asset_obj.id}
                    print('不是个数字吗',reply_data)

            except ValueError as e:
                self.msg_reply('Error','AssetDataError',str(e))
                reply_data = self.reply_msg
        else:
            self.msg_reply('Error','AssetDataInvalid','Asset data is not provied')
            reply_data = self.reply_msg

        return reply_data




    def _create_asset(self):
        func =  getattr(self,'_create_%s'%self.reporting_data['asset_type'])
        create_func = func()

    def _update_asset(self):
        func = getattr(self,'_update_%s'%self.reporting_data['asset_type'])
        update_func = func()

    def _update_server(self):
#        self.__update_server_info()
#        self.__update_cpu()
#        self.__update_ram()
        self.__update_disk()

        record_log = "Asset [<a href='#' target='_blank'>%s</a>] has been update" % self.asset_obj

        self.msg_reply('Info','UpdateAsset',record_log)

    def __update_handler(self,related_name,compare_fields,identify_field,component_name):
        print("到我了吗")
        if  hasattr(self.asset_obj,related_name):
            all_objs = getattr(self.asset_obj,related_name).select_related()
            print('硬盘信息:%s'%all_objs)
            for obj in all_objs:
                obj_mark = getattr(obj,identify_field)
                client_component_data = self.reporting_data.get(component_name)
                print('获取到db中each信息:%s 类型:%s'%(obj_mark,type(obj_mark)))
                for item in client_component_data:
                    if item:
                        client_mark = item.get(identify_field)
                        print('client_mark:%s type:%s'%(client_mark,type(client_mark)))
                        if obj_mark == client_mark:
                            print("obj_mark:%s client_mark:%s" % (obj_mark,client_mark))
                            self.__field_compare(obj,compare_fields,item)
                            break

            self.__add_or_delete(all_objs,client_component_data,identify_field,component_name,related_name)
        else:
          self.msg_reply('Warning','ComponentNotExist','Component:%s is not required')

    def __add_or_delete(self,component_data_from_db,component_data_from_client,identify_field,component_name,related_name):
        db_data_set = []
        client_data_set = []
        if component_data_from_db:
            for db_item in component_data_from_db:
                db_data = getattr(db_item,identify_field)
                db_data_set.append(db_data)
        if component_data_from_client:
            for client_item in component_data_from_client:
                client_data = client_item.get(identify_field)
                client_data_set.append(client_data)
        print('db_data_set:',db_data_set)
        print('client_data_set:',client_data_set)
        db_data_set = set(db_data_set)
        client_data_set = set(client_data_set)

        delete_obj = db_data_set - client_data_set
        if len(delete_obj):

            self.__delete_asset(component_data_from_db,delete_obj)

        add_obj = client_data_set - db_data_set
        if len(add_obj):
            self.__add_asset(add_obj,component_name,identify_field,related_name)

    def __delete_asset(self,component_data_from_db,delete_obj):
        print('delete func')

    def __add_asset(self,add_obj,component_name,identify_field,related_name):
        component_data_of_client = self.reporting_data.get(component_name)
        for component_item in component_data_of_client:
            for add_obj_item in add_obj:
                if add_obj_item == component_item.get(identify_field):
                    print(related_name)
                    component_obj = getattr(models,component_name.capitalize())
                    data_set = {
                        'asset_id': self.asset_obj.id,
                    }
                    for k,v in component_item.items():
                        data_set[k] = v
                    print('添加的数据',data_set)
                    field_obj = component_obj(**data_set)
                    field_obj.save()
                    log_msg = "Asset[%s] component[%s] field[%s] was added" %(self.asset_obj,component_obj,field_obj)
                    self.msg_reply('Info','FieldAdd',log_msg)
                    log_handler(self.asset_obj,'ComponentAdded',self.request.user,log_msg)

    def __field_compare(self,model_obj,compare_fields,client_data):
        print('到我了吗')
        for field in compare_fields:
            field_data_of_db = getattr(model_obj,field)
            field_data_of_client = client_data.get(field)
            if field_data_of_client:
                if type(field_data_of_db) is int:field_data_of_client = int(field_data_of_client)
                elif type(field_data_of_db) is str:field_data_of_client = str(field_data_of_client).strip()
                #print(field_data_of_db,field_data_of_client)
                if field_data_of_db == field_data_of_client:
                    pass
                else:
                    field_obj = model_obj._meta.get_field(field)
                    field_obj.save_form_data(model_obj,field_data_of_client)
                    model_obj.update_time = timezone.now()
                    model_obj.save()
                    log_msg = "Asset[%s] component[%s] field[%s] was changed from [%s] to [%s]" %(self.asset_obj,model_obj,field,field_data_of_db,field_data_of_client)
                    self.msg_reply('Info','DataChanged',log_msg)
                    log_handler(self.asset_obj,'FieldChanged',self.request.user,log_msg)
            else:
                self.msg_reply('Warning','AssetDataWarning','component[%s] Field[%s] was not provied'%(model_obj,field))
        model_obj.save()


    def __update_server_info(self):

        compare_fields = ['model','os_type','os_release','sn','host_on_id']
        server_obj = getattr(self.asset_obj,'server')
        self.__field_compare(server_obj,compare_fields,self.reporting_data)

    def __update_cpu(self):
        compare_fields = ['cpu_count','cpu_model','cpu_core_count']
        cpu_obj = getattr(self.asset_obj,'cpu')
        self.__field_compare(cpu_obj,compare_fields,self.reporting_data)

    def __update_ram(self):
        compare_fields = ['ram_model','capacity','slot']
        related_name = 'ram_set'
        identify_field = 'slot'
        component_name = 'ram'
        self.__update_handler(related_name,compare_fields,identify_field,component_name)

    def __update_disk(self):
        compare_fields = ['sn','capacity','slot','model','disk_iface_choice']
        related_name = 'disk_set'
        identify_field = 'slot'
        component_name = 'disk'
        self.__update_handler(related_name,compare_fields,identify_field,component_name)

    def _create_server(self):
        self.__create_server_info()
        self.__create_cpu()
        self.__create_ram()
        self.__create_disk()

        record_log = "Asset [<a href='#' target='_blank'>%s</a>] has been created" % self.asset_obj
        self.msg_reply('Info','NewAsset',record_log)

    def __create_server_info(self):
        try:
            if not len(self.reply_msg['Error']):
                data_set = {
                    'asset_id':self.asset_obj.id,
                    'server_type':self.reporting_data.get('server_type'),
                    'sn': self.reporting_data.get('sn'),
                    'os_type':self.reporting_data.get('os_type'),
                    'os_release':self.reporting_data.get('os_release'),
                    'host_on':self.reporting_data.get('host_on'),
                }
                server_obj = models.Server(**data_set)
                server_obj.save()
                return server_obj
        except Exception as e:
            self.msg_reply('Error','CreateServerObjError',e)

    def __create_cpu(self):
        try:
            if not len(self.reply_msg['Error']):
                print('cpu_model--------------->',self.reporting_data.get('cpu_model'))
                data_set = {
                    'asset_id': self.asset_obj.id,
                    'cpu_model': self.reporting_data.get('cpu_model'),
                    'cpu_count':self.reporting_data.get('cpu_count'),
                    'cpu_core_count':self.reporting_data.get('cpu_core_count'),
                }
                cpu_obj = models.CPU(**data_set)
                cpu_obj.save()
                return cpu_obj
        except Exception as e:
            self.msg_reply('Error', 'CreateCpuObjError', e)

    def __create_ram(self):
        ram_info = self.reporting_data.get('ram')
        if ram_info:
            for ram_item in ram_info:
                try:
                    if not len(self.reply_msg['Error']):
                        data_set = {
                            'asset_id':self.asset_obj.id,
                            'ram_model':ram_item.get('ram_model'),
                            'slot':ram_item.get('slot'),
                            'capacity':ram_item.get('capacity'),
                        }

                        ram_obj = models.RAM(**data_set)
                        ram_obj.save()

                except Exception as e:
                    self.msg_reply('Error', 'CreateRamObjError', e)
        else:
            self.msg_reply('Error', 'ReportingDataError', 'Ram info is not provied')
    def __create_disk(self):
        disk_info = self.reporting_data.get('disk')
        if disk_info:
            for disk_item in disk_info:
                try:
                    if not len(self.reply_msg['Error']):
                        data_set= {
                            'asset_id':self.asset_obj.id,
                            'sn': disk_item.get('sn'),
                            'slot':disk_item.get('slot'),
                            'model':disk_item.get('model'),
                            'capacity':disk_item.get('capacity'),
                            'iface_type':disk_item.get('iface_type'),
                        }

                        disk_obj = models.Disk(**data_set)
                        disk_obj.save()

                except Exception as e:
                    self.msg_reply('Error', 'CreateDiskObjError', e)
        else:
            self.msg_reply('Error','ReportingDataError','Disk info is not provied')


def log_handler(asset_obj,event_name,user,detail):

    catalog = {
        1 : ['FieldChanged','HardwareChanged'],
        2 : ['ComponentAdded',]
    }
    if not user.id:
        user = models.UserProfile.objects.filter(is_admin=True).last()
    for k,v in catalog.items():
        if event_name in v:
            event_type = k
            break
    log_obj = models.EventLog(
        asset_id = asset_obj.id,
        name = event_name,
        event_type = event_type,
        detail = detail,
        user_id = user.id
    )

    log_obj.save()

