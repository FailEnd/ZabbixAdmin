# -*- coding: utf-8 -*-
# @Time    : 2018/5/7 14:46
# @Author  : 流沙
# @Site    :
# @File    : urls.py
# @Software: PyCharm
import requests
import json
from Zabbix.dbinfo import findDataSource


class ZabbixApi(object):

    """
    Zabbix API类
    """
    #超时时间(5秒钟）
    TIMEOUT=5
    DataSource = findDataSource()

    class FailedError(Exception):
        """
        使用Zabbix API失败时出错
        """
        ERROR_MESSAGE_TEMPLATE = '"{message}({code}): {data}"'
        def __init__(self,name,reason = None):
            """
            构造函数
            :param name:  失败的方法名称
            :param reason: 错误响应
            """
            message = "Failed to {0}.".format(name)
            if reason is not None:
                message = ''.join([message,self.ERROR_MESSAGE_TEMPLATE.format(**reason)])
            super(ZabbixApi.FailedError,self).__init__(message)

    class AuthenticationFailedError(FailedError):
        """
        验证ZabbixToken失败
        """
        def __init__(self,reason = None):
            """
            构造函数
            :param reason: 失败的方法名称
            """
            super(ZabbixApi.AuthenticationFailedError,self).__init__('authenticate',reason)

    def __init__(self,request_id=1,encode = 'utf-8'):
        """
        构造函数
        :param request_id:JSON-RPC请求标识符
        """
        self.request_id = request_id
        self.AUTH = self.DataSource['token']

    # def __enter__(self):
    #     self.authenticate()
    #     return self

    def call(self,method,params):
        """
        ZabbixAPI请求程序
        :param method: Zabbix API方法名称
        :param params: Zabbix API方法参数
        :param through_authenticate: 事前预认证
        :return:
        """
        body = json.dumps({
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'auth': self.AUTH,
            'id': self.request_id
        })
        headers = {'Content-Type': 'application/json-rpc'}
        try:
            request = requests.post(self.DataSource['uri'],data=body,headers=headers,timeout=self.TIMEOUT)
            response_json = request.json()
            if 'result' in response_json:
                return response_json
            elif 'error' in response_json:
                return ZabbixApi.FailedError(name=method,reason=response_json['error'])
            else:
                return ZabbixApi.AuthenticationFailedError()
        except requests.exceptions.ConnectTimeout:
            return ZabbixApi.AuthenticationFailedError({'code': -1, 'message': 'Connect Timeout.', 'data': 'URI is incorrect.'})

    # def authenticate(self):
    #     """
    #     执行认证
    #     :return:
    #     """
    #     response = self.call('user.login', {'user': self.DataSource['username'], 'password': self.DataSource['password']}, True)
    #     print(response)
    #     if 'result' in response:
    #         self.session_id = response['result']
    #         return response['result']
    #     elif 'error' in response:
    #         raise ZabbixApi.AuthenticationFailedError(response['error'])
    #     else:
    #         raise ZabbixApi.AuthenticationFailedError()
#
# method = 'hostgroup.update'
# params =  {
#             "groupid": 15,
#             "name": 'TEST1'
#         }
# # params = json.loads('{"search": {"name": "Templates/Modules"}}')
# api = ZabbixApi()
# print(api.call(method,params))