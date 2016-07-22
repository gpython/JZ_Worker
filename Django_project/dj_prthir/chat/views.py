#encoding=utf-8
from django.shortcuts import render, HttpResponse
import models
import json
import datetime
import models
import utils
# Create your views here.

global_msg_dic = {}

def dashboard(request):
  return render(request, 'chat/dashboard.html', {'title':'Chat'})

def send_msg(request):
  print request.POST
  recv_data = request.POST.get('data')
  data = json.loads(recv_data)
  to_id = data.get('to_id')
  user_obj = models.bbs_models.UserProfile.objects.get(id=to_id)
  contact_type = data.get('contact_type')
  data['dtime'] = datetime.datetime.now().strftime("%F %T")

  if contact_type == 'single':
    if not global_msg_dic.has_key(to_id):
      global_msg_dic[to_id] = utils.Chat()
    global_msg_dic[to_id].msg_queue.put(data)

  print "Message ID: %s Username: %s" %(user_obj.id, user_obj.name)
  return HttpResponse({'state':'OK'})


def get_msg(request):
  uid = request.GET.get('uid')
  if uid:
    res = []
    if global_msg_dic.has_key(uid):
      res = global_msg_dic[uid].get_msg()
      return HttpResponse(json.dumps(res))
    else:
      return HttpResponse(json.dumps("uid not provided"))
