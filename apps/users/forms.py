# -*- coding: utf-8 -*-
# @Time    : 2018/5/5 14:08
# @Author  : 流沙
# @Site    : 
# @File    : forms.py
# @Software: PyCharm
from django import forms
from django.contrib.auth.models import User

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username','email','password']
#         widgets = {
#             'admin': forms.Select(attrs={
#                 'class': 'select2', 'data-placeholder': ('admin')
#             })
#         }

class UserCreateUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label=('Password'), widget=forms.PasswordInput,
        max_length=128, strip=False, required=False,
    )
    class Meta:
        model = User
        fields = [
            'username', 'email',
        ]
        help_texts = {
            'username': '* required',
            'password': '* required',
            'email': '* required',
        }

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        user = super().save(commit=commit)
        if password:
            user.set_password(password)
            user.save()
        return user