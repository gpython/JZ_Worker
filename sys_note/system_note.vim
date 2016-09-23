查看系统进程占用swap情况
for loop in `ls /proc/ | grep -Po '\d{3,}'`
do
  cat /proc/${loop}/smaps | awk '/Swap:/{S+=$2}END{print "'${loop}'", S/1024"M"}'
done | sort -nrk 2


SQL查询记录到文件
into outfile '/tmp/plat.sql'
select * into outfile '/tmp/2163950.sql' from role_friendtablerecords  where rid=2163950  and  record like  '%"table_room_type":10%"create_user_rid":2163950%' ;

select * into outfile '/tmp/2075173.sql' from role_friendtablerecords where rid=2075173  and  record like  '%"table_room_type":10%"create_user_rid":2075173%' ;


with open('/etc/password') as fd:
  for chunk in iter(lambda: fd.read(10), ''):
    n = sys.stdout.write(chunk)

"""
iter 函数一个鲜为人知的特性是它接受一个可选的 callable 对象和一个标记 (结
尾) 值作为输入参数。当以这种方式使用的时候，它会创建一个迭代器，这个迭代器会
不断调用 callable 对象直到返回值和标记值相等为止。
"""

MongoDB 时间戳转换
db.orderinfo.find({state: {$eq: 3}}, {'_id':0}).forEach(
  function(a){
    a['create_time'] = (new Date(a['create_time']*1000).toLocaleString().replace(/:\d{1,2}$/,' '));
    a['time_stamp'] = (new Date(a['time_stamp']*1000).toLocaleString().replace(/:\d{1,2}$/,' '));
    printjson(a)
  })

当前目录
os.path.dirname(os.path.abspath(__file__))

几天前时间
(datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y_%m_%d")

cygwin
wget rawgit.com/transcode-open/apt-cyg/master/apt-cyg
install apt-cyg /bin

import datetime
for i in range(1,8)[::-1]:
  dbname = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y_%m_%d")
  dtime = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
  weekday = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%w")
  print dbname

