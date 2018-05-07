# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 20:30
# @Author  : 流沙
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from .views import UserListView,UserCreateView,UserUpdateView,UserDeleteView

app_name = 'sys'

urlpatterns = [
    url(r"^user/$",UserListView.as_view(),name="user"),
    url(r"^user/create/$",UserCreateView.as_view(),name="user-create"),
    url(r'^user/(?P<pk>[0-9]+)/update/$', UserUpdateView.as_view(), name='user-update'),
    url(r"^user/delete/$",UserDeleteView.as_view(),name="user-delete")
]