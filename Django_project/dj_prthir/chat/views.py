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

  elif contact_type == 'group':
    group_obj = models.CGroup.objects.get(id = to_id)
    for member in group_obj.members.select_related():
      if not member.id == request.user.userproile.id:
        if not global_msg_dic.has_key(member.id):
          global_msg_dic[member.id] = utils.Chat()
        global_msg_dic[member.id].msg_queue.put(data)
#  print "Message ID: %s Username: %s" %(user_obj.id, user_obj.name)
  return HttpResponse({'state':'OK'})


def get_msg(request):
  uid = request.GET.get('uid')
  if uid:
    res = []
    if global_msg_dic.has_key(uid):
      res = global_msg_dic[uid].get_qmsg(request)
      return HttpResponse(json.dumps(res))
    else:
      global_msg_dic[uid] = utils.Chat()
      return HttpResponse(json.dumps({}))
#    return HttpResponse(json.dumps(res))
