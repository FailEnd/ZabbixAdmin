# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 17:35
# @Author  : 流沙
# @Site    : 
# @File    : paging.py
# @Software: PyCharm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def Paging(queryset,page,display_counter):
    paginator = Paginator(queryset, display_counter)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        # If page is not an integer, deliver first page.
        result = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)
    return result