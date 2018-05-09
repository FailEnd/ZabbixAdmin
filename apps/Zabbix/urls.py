# -*- coding: utf-8 -*-
# @Time    : 2018/5/7 14:46
# @Author  : 流沙
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from .views import GroupListView,GroupView

app_name = 'zabbix'

urlpatterns = [
    url(r"^group-list/$",GroupListView.as_view(),name="group-list"),
    url(r"^group-operation/$",GroupView.as_view(),name="group-operation")
]