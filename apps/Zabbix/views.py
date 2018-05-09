from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.http import  QueryDict
from .zapi import ZabbixApi
from ZabbixAdmin.paging import Paging
import json
# Create your views here.

class GroupListView(TemplateView):
    template_name = 'groups/group_list.html'
    def get_context_data(self, **kwargs):
        method = 'hostgroup.get'
        key = self.request.GET.get('filter_key')
        value = self.request.GET.get('filter_value')
        if key and value:
            params = {"output": "extend","filter":{key:value.split(',')}}
        else:
            params = {}
        api = ZabbixApi()
        data = api.call(method,params)
        if 'result' in str(data):
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
                "GroupACT": "display: block;",
                "grouplistACT": "active",
                "title": "Zabbix主机组",
                'result': result,
                "page_detail": page_detail,
                "display_counter": display_counter,
                "counter": counter,
                "page_head":'主机组',
            }
        else:
            context = {
                "messages": data
            }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class GroupView(View):

    def get(self,request):
        groupid = request.GET.get('groupid')
        params = {"output": "extend","filter":{'groupid':groupid}}
        method = "hostgroup.get"
        api = ZabbixApi()
        result = api.call(method,params)
        return HttpResponse(result['result'][0]["name"])

    def put(self,request):
        put = QueryDict(request.body,encoding=request.encoding)
        params =  {
            "groupid": put.get('groupid'),
            "name": put.get('groupname')
        }
        method = 'hostgroup.update'
        api = ZabbixApi()
        result = api.call(method,params)
        if 'result' in str(result):
            isSuccess = True
        else:
            isSuccess = False
        return HttpResponse(json.dumps({"isSuccess":isSuccess,"result":str(result)}))

    def post(self,request):
        groupname = request.POST.get('groupname')
        params = {"name":groupname}
        method = 'hostgroup.create'
        api = ZabbixApi()
        result = api.call(method,params)
        if 'result' in str(result):
            isSuccess = True
        else:
            isSuccess = False
        return HttpResponse(json.dumps({"isSuccess":isSuccess,"result":str(result)}))

    def delete(self,request):
        delete = QueryDict(request.body,encoding=request.encoding)
        method = "hostgroup.delete"
        params = [delete.get('groupid')]
        api = ZabbixApi()
        result = api.call(method, params)
        if 'result' in str(result):
            isSuccess = True
        else:
            isSuccess = False
        return HttpResponse(json.dumps({"isSuccess": isSuccess, "result": str(result)}))