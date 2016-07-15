#encoding:utf-8

from django import forms

class ALogin(forms.Form):
  username = forms.CharField(error_messages={'required': ('用户名错误 '), 'invalid': ('用户名格式错误')})
  email = forms.EmailField(required = True, error_messages={'required': ('邮箱错误 '), 'invalid': ('邮箱格式错误')})
  ip = forms.GenericIPAddressField(error_messages={'required': ('IP地址错误 '), 'invalid': ('IP地址格式错误')})

