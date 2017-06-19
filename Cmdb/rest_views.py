#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework import routers, serializers, viewsets
from Cmdb import models
from Cmdb import serializer

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializer.UserSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset =  models.Asset.objects.all()
    serializer_class = serializer.AssetSerializer