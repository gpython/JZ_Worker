#Zabbix API simple Usage 

******

##Usage

  修改zabbix 用户名 密码和api_jsonrpc.php链接 
  安装requests模块
  pip install requests

zabbix_local.py

 使用zabbix api 添加主机 指定主机组ID 指定模板ID 以逗号分隔

zabbix_hostgroup_screen_local.py

  将多个主机组 或 多个主机的所有graph添加到screen 若已经存在相应的主机的screen 先删除在执行 



