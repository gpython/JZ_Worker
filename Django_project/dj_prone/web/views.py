#encoding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from models import Asset
from web.forms import RegisterForm

# Create your views here.


def index(request):
  return HttpResponse('Web index')

def login(request):
  return HttpResponse('web Login')

def add(request, name):
  Asset.objects.create(hostname = name)
  return HttpResponse('Asset OK')

"""
def del(request, id):
  Asset.objects.get(id = id).delete()
  return HttpResponse('Asset delete ok')
"""
def dele(request, id):
  Asset.objects.get(id = id).delete()
  return HttpResponse('Asset Delete Ok')

def update(request, id, hostname):
  """
  obj = Asset.objects.get(id=id)
  obj.hostname = hostname
  obj.save()
  """
  x = Asset.objects.filter(id__gt=id).update(hostname=hostname)
  print x.query
  return HttpResponse("Asset Update Ok")

def gett(request, hostname):
  t = Asset.objects.filter(hostname__contains=hostname)
  print t.query
  for i in t:
    print i.hostname, i.create_time
  return HttpResponse("This is Query One ")

def all(request):
  asset_list = Asset.objects.all()
  return render_to_response('assetlist.html', {'data': asset_list, 'title':'AssetLIst', 'user': 'AssetList'})

def Register(request):
  registerForm = RegisterForm()
  if request.method == 'POST':
    form = RegisterForm(request.post)
    if form.is_valid():
      data = form.cleaned_data
      print data
    else:
      print form.errors.as_json()
  else:
    return render_to_response('reg.html', {'form': registerForm} )

def reg(request):
  t1 = models.UserType.objects.create(name = 'Super Admin')
  t2 = models.UserType.objects.create(name = 'Admin')

  t3 = models.UserType.objects.get(name = 'Super Admin')
  u1 = models.UserInfo.objects.create(username = 'google',
    password = '123456',
    email = 'g.@g.com',
    user_type = t3
  )

  t4 = models.UserType.objects.get(name = 'Admin')
  u2 = models.UserInfo.objects.create(username = 'yahoo',
    password = 'yahoo',
    email = 'y@g.com',
    user_type = t4
  )

def login(request):
  username = request.POST.get('username', None)
  password = request.POST.get('password', None)
  is_empty = all([username, password])
  if is_empty:
    count = models.UserInfo.objects.filter(username = username).count()
    if count == 1:
      return redirect('/index')
    else:
      ret['status'] = 'Username or Password error'
  return render_to_response('ogin.html', ret)

def host(request):
  ret = {'status': '', 'data': None, 'group': None}

  usergroup = models.UserGroup.objects.all()
  ret['group'] = usergroup

  if request.method == 'POST':
    hostname = request.POST.get('hostname', None)
    ip = request.POST.get('ip', None)
    groupId = request.POST.get('group', None)

    is_empty = all([hostname, ip])
    if is_empty:
      groupObj = models.UserGroup.objects.get(id = groupId)
      models.Asset.objects.create(hostname = hostname,
        ip = ip,
        user_group = groupObj
      )
    else:
      ret['status'] = 'hostname or ip can not blank'

  data = models.Asset.objects.all()
  ret['data'] = data
#  获取所有Admin用户组的所有用户信息
#  obj = models.Asset.objects.filter(user_group__GroupName = 'Admin')
  return render_to_response('host.html', ret)
