#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url, include
#from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from Cmdb import models

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('url', 'email', 'name','is_staff')

class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Asset
        fields = ('id','asset_type','name')
