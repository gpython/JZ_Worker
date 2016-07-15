#encoding:utf-8
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http.response import HttpResponse

from web import models
from web import forms
import json

# Create your views here.

def index(request):
  #多对多关系添加
  u1 = models.UserInfo.objects.get(id=5)
  g1 = models.UserGroup.objects.get(id = 3)

  g1.user.add(u1)
  #u1.usergroup_set.add(g1)
  return HttpResponse('this is dj_prtwo index')

def login(request):
  ret = {'data':None, 'err': '', 'title': 'Login'}
  obj = forms.ALogin()
  ret['data'] = obj

  if request.method == 'POST':
    check_form = forms.ALogin(request.POST)
    check_result = check_form.is_valid()
    if check_result:
      pass
    else:
      ret['err'] = check_form.errors.as_data().values()[0][0].messages[0]
      ret['data'] = check_form
    print check_result
    print ret

  return render_to_response('web/login.html', ret)

def ajax(request):
  if request.method == 'POST':
    rev_data = request.POST.get('dat', None)
    data = {
      'status': 0,
      'msg': 'OK',
      'data': ['google', 'yahoo', 'python', 'linux', 'Gentoo'],
      'rev_data': rev_data,
    }
    return HttpResponse(json.dumps(data))
  else:
    return render_to_response('web/ajax_01.html', {'title': 'Ajax'} )
