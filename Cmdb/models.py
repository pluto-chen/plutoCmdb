from django.db import models
from Cmdb.custom_auth import UserProfile
# Create your models here.



class Asset(models.Model):

    asset_type_choices = (
        ('Server',u'服务器'),
        ('Switch',u'交换机'),
        ('Router',u'路由器'),
    )
    asset_type = models.CharField(u'资产类型',choices=asset_type_choices,default='Server',max_length=16)
    project = models.ForeignKey('Project',verbose_name=u'项目')
    name = models.CharField(u'名称',max_length=32)
    idc = models.ForeignKey('IDC',verbose_name=u'IDC数据中心')
    manufactory = models.ForeignKey('Manufactory',verbose_name=u'制造商')
    admin = models.ForeignKey(UserProfile,verbose_name=u'资产管理人')
    create_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date = models.DateTimeField(auto_now=True,blank=True,null=True)
    memo = models.CharField(u'备注',max_length=128,blank=True)

    class Meta:
        verbose_name = '资产列表'
        verbose_name_plural = '资产列表'
        unique_together = ('project','name')

    def __str__(self):
        return '%s:%s' % (self.id,self.name)

class Project(models.Model):

    project_name = models.CharField(u'项目名称',max_length=64,unique=True)
    memo = models.CharField(u'备注',max_length=64,blank=True)

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return '%s:%s'%(self.id,self.project_name)

class Server(models.Model):

    asset = models.OneToOneField('Asset')
    server_type_choices = (
        ('Physical',u'物理机'),
        ('Virtual',u'虚拟机')
    )
    server_type = models.CharField(choices=server_type_choices,max_length=16,default='Virtual')
    sn = models.CharField(u'sn号',max_length=32,blank=True,null=True)
    model = models.CharField(u'型号',max_length=128,blank=True,null=True)
    os_type = models.CharField(u'操作系统',max_length=32,blank=True)
    os_release = models.CharField(u'系统版本',max_length=32,blank=True)
    host_on = models.ForeignKey('self',related_name='host_on_server',blank=True,null=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'

    def __str__(self):
        return '%s sn:%s' %(self.asset.name,self.sn)

class IDC(models.Model):

    idc = models.CharField(u'idc',max_length=32,unique=True)
    idc_attn = models.CharField(u'idc联系人',max_length=32,blank=True)
    idc_num = models.CharField(u'idc联系电话',max_length=32,blank=True)
    idc_addr = models.CharField(u'idc地址',max_length=64,blank=True)

    class Meta:
        verbose_name = 'idc'
        verbose_name_plural = 'idc'

    def __str__(self):
        return self.idc


class Manufactory(models.Model):

    manufactory = models.CharField(u'制造厂商',max_length=64,unique=True)
    mf_attn = models.CharField(u'联系人',max_length=32,blank=True)
    mf_num = models.CharField(u'联系电话',max_length=32,blank=True)
    mf_addr = models.CharField(u'地址',max_length=64,blank=True)

    class Meta:
        verbose_name = '制造商'
        verbose_name_plural = '制造商'

    def __str__(self):
        return self.manufactory


class CPU(models.Model):

    asset = models.OneToOneField('Asset')
    cpu_model = models.CharField(u'cpu型号',max_length=128,blank=True,null=True)
    cpu_count = models.SmallIntegerField(u'cpu物理个数')
    cpu_core_count = models.SmallIntegerField(u'cpu核数')
    memo = models.CharField(u'备注',max_length=128, blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)

    class Meta:
        verbose_name = 'cpu信息'
        verbose_name_plural = 'cpu信息'

    def __str__(self):
        return '%s cpu:%s' %(self.asset.name,self.cpu_model)

class RAM(models.Model):

    asset = models.ForeignKey('Asset')
    ram_model = models.CharField(u'内存型号',max_length=64,blank=True,null=True)
    slot = models.CharField(u'插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(MB)')
    memo = models.CharField(u'备注',max_length=128, blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return '%s:%s:%s' % (self.asset_id,self.slot,self.capacity)
    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"
        unique_together = ("asset", "slot")

class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    slot = models.CharField(u'插槽位',max_length=64)
    model = models.CharField(u'磁盘型号', max_length=128,blank=True,null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )

    iface_type = models.CharField(u'接口类型', max_length=64,choices=disk_iface_choice)
    memo = models.TextField(u'备注', blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)

    class Meta:
        unique_together = ("asset", "slot")
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"
    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id,self.slot,self.capacity)

class EventLog(models.Model):

    asset = models.ForeignKey('Asset')
    name = models.CharField(u'事件名称',max_length=32)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
    )
    event_type = models.SmallIntegerField(u'事件类型',choices=event_type_choices)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间',auto_now_add=True)
    user = models.ForeignKey('UserProfile',verbose_name=u'事件源')
    memo = models.TextField(u'备注', blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"