from django.shortcuts import render, redirect, render_to_response
from django.http.response import HttpResponse
from django.utils.safestring import mark_safe
import json
from page import customPage, try_int, PageInfo
from web import models
from web import forms
# Create your views here.

def index(request, page_num):
#  per_item = try_int(request.COOKIES.get('pager_num', 10), 10)

  page_num = try_int(page_num, 1)
  count = models.Host.objects.all().count()

  pageObj = PageInfo(page_num, count, 2)
  start = pageObj.From()
  end = pageObj.To()
  total_page = pageObj.total_page()

  result = models.Host.objects.all()[start:end]
  ret = {'data': result, 'count': count, 'title':'Index'}

  ret['page_list'] = customPage('/web/index/', page_num, total_page)

  response = render_to_response('web/index.html', ret)
  response.set_cookie('pager_num', per_item)
  return response

def login(request):
  ret = {'data': None, 'err': '', 'title': 'Login'}
  fobj = forms.FLogin()
  ret['data'] = fobj

  if request.method == 'POST':
    check_form = forms.FLogin(request.POST)
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
    return render_to_response('web/ajax.html', {'title':'Ajax'})
