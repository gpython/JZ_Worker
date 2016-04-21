#encoding:utf-8
import argparse
import requests
import json
import sys

def json_dumps(data):
  return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, separators=(',',':'))

def get_data(data):
  """
  POST提交json数据
  """
  try:
    r = requests.post(api_url, data=data, headers=headers)
  except Exception, e:
    print "Request Error!!! Info:%s" %e
  else:
    response = json.loads(r.text)
    return response

def zabbix_login(zabbix_user, zabbix_passwd, api_url, headers):
  """
  登录zabbix api 获取登录返回信息 主要获取auth_id
  """
  data = json.dumps({
    'jsonrpc': '2.0',
    'method': 'user.login',
    'params': {
      'user':     '%s' %zabbix_user,
      'password': '%s' %zabbix_passwd,
    },
    'id': 0
  })
  api_params = get_data(data)
  return api_params

def template_get(auth_id):
  """
  获取模板信息 模板id 和 模板名称
  """
  data = json.dumps({
    "jsonrpc": "2.0",
    "method": "template.get",
    "params": {
#      "output": "extend",
      "output": ['templateid', 'name']
    },
    "auth": auth_id,
    "id": 1,
  })
  print api_url
  template_data = get_data(data)
  return template_data

def hostgroup_get(auth_id):
  data = json.dumps({
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
      "output": "extend",
    },
    "auth": auth_id,
    "id": 1
  })
  hostgroup_data = get_data(data)
  return hostgroup_data

def host_get(auth_id, host_ip):
  """
  根据主机IP获取 主机id 主机名称 主机状态 主机 以及主机所关联的模板 和模板名称
  """
  data = json.dumps({
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
#      "output": "extend",
      "output": ["hostid","name","status","host"],
      "filter": {"host": [host_ip,]},
      "selectParentTemplates": ["templateid","name"],
#      "selectItems": ['itemid', 'name'],
#      "selectGraphs": "extend",
      'searchByAny': 1,
    },
    "auth": auth_id,
    "id": 1
  })
  host_get_data = get_data(data)
  return host_get_data

def host_del(auth_id, host_ip):
  """
  删除主机 依据主机IP 获取主机id 'params':[主机id] 列表形式
  """
  data = {
    "jsonrpc": "2.0",
    "method": "host.delete",
    "auth": auth_id,
    "id": 1,
    "params": []
  }
  try:
    host_data = host_get(auth_id, host_ip)
    host_id = host_data['result'][0]['hostid']
  except Exception,e:
    print "Host id get Error -> %s" %e
  else:
    data.update({'params': [host_id]})
    data = json.dumps(data)

  host_del_data = get_data(data)
  return host_del_data

def list_dict(key,data):
  tmp_list = []
  for id in data:
    tmp = {}
    tmp[key] = id
    tmp_list.append(tmp)
  return tmp_list

def host_create(auth_id, host_ip, groups, templates):
  """
  groups = [{'groupid': 1}, {'groupid': 2}]
  templates = [{'templateid': 100}, {'templateid': 101}]
  """
  g_list = list_dict('groupid', groups)
  t_list = list_dict('templateid', templates)
  data = {
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
      "host": host_ip,
      "interfaces": [{
          "type": 1,
          "main": 1,
          "useip": 1,
          "ip": host_ip,
          "dns": "",
          "port": "10050"
        }],
      "groups": g_list,
      "templates": t_list,
    },
    "auth": auth_id,
    "id": 1
  }
#  print json_dumps(data)
  data = json.dumps(data)
  host_create_data = get_data(data)
  return host_create_data

def host_update(auth_id, host_ip, groups=None, templates=None, templates_clear=None):
  host_id = host_get(auth_id, host_ip)['result'][0]['hostid']
  data = {
    "jsonrpc": "2.0",
    "method": "host.update",
    "params": {
      "hostid": host_id,
    },
    "auth": auth_id,
    "id": 1
  }

  if groups:
    g_list = list_dict("groupid", groups)
    data['params'].update({'groups': g_list})
  if templates:
    t_list = list_dict('templateid', templates)
    data['params'].update({'templates': t_list})
  if templates_clear:
    t_clear_list = list_dict('templateid', templates_clear)
    data['params'].update({'templates': t_clear_list})

  print json_dumps(data)
  data = json.dumps(data)
  host_update_data = get_data(data)
  return host_update_data






if __name__ == '__main__':
  zabbix_user = 'admin'
  zabbix_passwd = 'zabbix'
  api_url = 'http://zabbix.g.com/api_jsonrpc.php'
  headers = {'content-type': 'application/json'}

  auth_data = zabbix_login(zabbix_user, zabbix_passwd, api_url, headers)
  auth_id = auth_data['result']


  parser = argparse.ArgumentParser(description="Zabbix add/update host information")

  parser.add_argument('-a', '--add', action="store", dest="add_host", help="Add a New Host")
  parser.add_argument('-u', '--update', action="store", dest="update_host", help="Update an Exists Host")
  parser.add_argument('-g', '--group', action="store", dest="g_coll", help="Add group list")
  parser.add_argument('-t', '--template', action="store", dest="t_coll", help="Add template list")

  parser.add_argument('--list-host', action="store", dest="list_host", help="list host")
  parser.add_argument('--list-template', action="store_true", dest="list_template", help="list template")
  parser.add_argument('--list-hostgroup', action="store_true", dest="list_hostgroup", help="list hostgroup")

  parser.add_argument('-d', '--del', action="store", dest="del_host", help="delete host")

  result = parser.parse_args()

  if len(sys.argv) > 7:
    print "params is too long "
    sys.exit()
  if len(sys.argv) == 1:
    print sys.argv[0], "--list-template"
    print sys.argv[0], "--list-hostgroup"
    print sys.argv[0], "--list-host 'Zabbix server'"
    print sys.argv[0], "-a 10.10.10.40 -g 8 -t 10001,10104"
    print sys.argv[0], "-u 10.10.10.40 -g 8 -t 10001,10104"
    sys.exit()

  if result.list_template:
    template_data = template_get(auth_id)
    for tem_info in template_data['result']:
      print tem_info['name'], tem_info['templateid']

  elif result.list_hostgroup:
    hostgroup_get_data = hostgroup_get(auth_id)
    print "hostgroup_get => ", json_dumps(hostgroup_get_data)

  elif result.list_host:
    host = result.list_host
    host_get_data = host_get(auth_id, "%s" %(host))
#  host_get_data = host_get(auth_id, "10.19.2.215")
    print "host_get => ", json_dumps(host_get_data)

  elif result.del_host:
    host = result.del_host
    host_del_data = host_del(auth_id, "%s" %(host))
    print json_dumps(host_del_data)

  elif result.add_host and result.g_coll and result.t_coll:
    host = result.add_host

    print result.g_coll
    groups = result.g_coll.split(',')
    print groups
    templates = result.t_coll.split(',')
    host_create_data = host_create(auth_id, host_ip=host, groups=groups, templates=templates)
    print json_dumps(host_create_data)

  elif result.update_host and result.t_coll and result.g_coll:
    host =  result.update_host
    groups = result.g_coll.split(',')
    templates = result.t_coll.split(',')
#  host_update_data = host_update(auth_id, '10.10.10.10', groups=[8,], templates=[10001,10104])
    host_update_data = host_update(auth_id, host_ip=host, groups=groups, templates=templates)
    print json_dumps(host_update_data)
