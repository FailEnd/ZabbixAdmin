from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView
from ZabbixAdmin.paging import Paging
from . import forms
import json

create_success_msg = _("<b>%(username)s</b> 创建成功")
update_success_msg = _("<b>%(username)s</b> 修改完成")
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception:
            return None


class Login(View):

    def get(self,request):

        if request.session._session:
            return HttpResponseRedirect('/index')
        else:
            return render(request,'login.html',{})

    def post(self,request):
        username = request.POST.get('username',"")
        password = request.POST.get('password',"")
        result = authenticate(request,username=username,password=password)
        if result is not None:
            login(request,result)
            return HttpResponseRedirect('/index')
        else:
            return render(request,'login.html',{"msg":"用户名或密码错误"})

def Logout(request):
    logout(request)
    return render(request,'login.html')


class Index(View):

    def get(self,request):
        return render(request,'index.html',{})


class UserListView(TemplateView):

    template_name = 'system/local_users.html'
    def get_context_data(self, **kwargs):
        key = self.request.GET.get('filter_key')
        value = self.request.GET.get('filter_value')
        if key and value:
            #构建搜索对象
            filter_obj = {key:[value]}
            con = Q()
            for k,v in filter_obj.items():
                q = Q()
                q.connector = 'OR'
                for item in v:
                    q.children.append((k, item))
                con.add(q, 'AND')
            data = User.objects.filter(con).order_by('id')
            counter = data.count()
        else:
            data = User.objects.all().order_by('id')
            counter = data.count()
        display_counter = self.request.GET.get('display_counter')  # 每页显示数据条数
        page = self.request.GET.get('page')
        if not page:
            page = 1
        if not display_counter:
            display_counter = 20  # 默认每页显示20条数据
        result = Paging(data, page, display_counter)
        page_detail = str(page) + '/' + str(result.paginator.num_pages)
        context = {
            "systemACT":"display: block;",
            "localuserACT":"active",
            "title": "本地用户",
            'result': result,
            "page_detail": page_detail,
            "display_counter": display_counter,
            "counter": counter
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserCreateView(SuccessMessageMixin,CreateView):
    model = User
    form_class = forms.UserCreateUpdateForm
    template_name = 'system/create_user.html'
    success_url = reverse_lazy('sys:user')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "systemACT":"display: block;",
            "localuserACT":"active",
            "title": "本地用户",
            })
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.created_by = self.request.user.username or 'System'
        user.save()
        return super().form_valid(form)


class UserUpdateView(SuccessMessageMixin,UpdateView):

    model = User
    form_class = forms.UserCreateUpdateForm
    template_name = 'system/update_user.html'
    success_url = reverse_lazy('sys:user')
    success_message = update_success_msg

    def get_context_data(self, **kwargs):
        content = {
            "systemACT": "display: block;",
            "localuserACT": "active",
            "title": "本地用户",
        }
        kwargs.update(content)
        return super().get_context_data(**kwargs)


class UserDeleteView(View):

    def post(self,request):
        user_id = request.POST.get('userid')
        User.objects.get(id=user_id).delete()
        return HttpResponse(json.dumps({"isSuccess":True}))


