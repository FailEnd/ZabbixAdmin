# -*- coding: utf-8 -*-
# @Time    : 2018/5/7 14:46
# @Author  : 流沙
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from .views import GroupListView,ChangeGroupView

app_name = 'zabbix'

urlpatterns = [
    url(r"^group-list/$",GroupListView.as_view(),name="group-list"),
    url(r"^group-change/$",ChangeGroupView.as_view(),name="group-change")
]