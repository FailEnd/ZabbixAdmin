from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.base import View
from Zabbix.zapi import ZabbixApi
from ZabbixAdmin.paging import Paging
import json
# Create your views here.


class GroupListView(TemplateView):
    template_name = 'zgroup/group_list.html'
    def get_context_data(self, **kwargs):
        method = 'hostgroup.get'
        api = ZabbixApi()
        data = api.call(method,{})
        counter = len(data['result'])
        display_counter = self.request.GET.get('display_counter')  # 每页显示数据条数
        page = self.request.GET.get('page')
        if not page:
            page = 1
        if not display_counter:
            display_counter = 20  # 默认每页显示20条数据
        result = Paging(data['result'], page, display_counter)
        page_detail = str(page) + '/' + str(result.paginator.num_pages)
        context = {
            "groupACT": "display: block;",
            "currGroupACT": "active",
            "title": "Zabbix主机组",
            'result': result,
            "page_detail": page_detail,
            "display_counter": display_counter,
            "counter": counter
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class ChangeGroupView(View):

    def post(self,request):
        groupid = request.POST.get('groupid')
        groupname = request.POST.get('groupname')
        params =  {
            "groupid": groupid,
            "name": groupname
        }
        method = 'hostgroup.update'
        api = ZabbixApi()
        result = api.call(method,params)
        if 'result' in str(result):
            isSuccess = True
        else:
            isSuccess = False
        return HttpResponse(json.dumps({"isSuccess":isSuccess,"result":str(result)}))