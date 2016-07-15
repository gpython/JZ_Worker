
into outfile '/tmp/plat.sql'

select * into outfile '/tmp/2163950.sql' from role_friendtablerecords  where rid=2163950  and  record like  '%"table_room_type":10%"create_user_rid":2163950%' ;
select * into outfile '/tmp/2075173.sql' from role_friendtablerecords where rid=2075173  and  record like  '%"table_room_type":10%"create_user_rid":2075173%' ;

db.orderinfo.find({'state': 3}, {'_id':0, 'pid':1, 'pay_type':1, 'price': 1, 'good_awards':1}).pretty();


select count(*) from goods group by cat_id;
{
  key:{cat_id: 1},
  cond: {},
  reduce: function(curr, result){
    result.total += 1;
  },
  initial:{total:0}

}

> db.vegetableprice.find();
{ "_id" : ObjectId("50271b4ae02ab93d5c5be795"), "name" : "tomato",    "price" : 3.3, "time" : ISODate("2012-08-12T02:56:10.303Z") }

> db.runCommand({"group" : {
 "ns" : "vegetableprice",
 "key" : {"name" : true},
 "initial" : {"time" : 0},
 "$reduce" : function(doc, prev) {
    if(doc.time > prev.time) {
         prev.time = doc.time;
         prev.price = doc.price;
     }
 }
 }});



db.orderinfo.aggregate([{
$group: {
  _id: "$pay_type",
  total_price: {$sum: "$price"}
  }
}])

db.orderinfo.aggregate([
  {$match: {state: {$eq: 3}}},
  {$group: { _id: "$pay_type", total_price: {$sum: "$price"}, total_count: {$sum: 1}}},
  {$sort: {total_count: 1}},
  {$limit: 1}
])

db.orderinfo.aggregate([
  {$match: {state: {$eq: 3}}},
  {$group: { _id: "$pay_type", total_price: {$sum: "$price"}, total_count: {$sum: 1}}},
  {$match: {total_count: {$gt: 2}}}，
  {$sort: {total_count: 1}}
])


match 在group之前相当于where
match 在group之后相当于having
############################################################################
db.orderinfo.group({
  key:{'pid':1, 'pay_type':1},
  cond: {'state':3},
  reduce: function(curr, result){
    result.price_total_count += curr.price;
    result.total_num += 1;
  },
  initial:{
    price_total_count:0,
    total_num:0
  }
})

db.orderinfo.group({
  key:{'pid':1, 'pay_type':1},
  cond: {state: {$eq:3}},
  reduce: function(curr, result){
    result.price_total_count += curr.price;
    result.total_num += 1;
  },
  initial:{
    price_total_count:0,
    total_num:0
  }
})


key 指定要分组的字段                groupby
cond 指定要查询的条件               where
reduce  param1 当前的每一行         聚合函数
        param2 结果记录所在的组

initial 组操作开始前初始化          进入组时初始化
finalize 组操作完成时回调           离开组时初始化

group 需要手写聚合函数
group 不支持shard cluster 无法分布式运算


{
  key:{cat_id:1},
  cond:{},
  reduce:dunction(curr, result){
    result.cnt += 1;
    result.sum += curr.shop_price;
  },
  initialize:{sum:0, cnt:0},
  finalize:function(result){
    result.avg = result.sum/result.cnt;
  },
}




求综合 相加
求最大 最小 比较
求平均  使用finilize 组操作完成后执行回调函数

var eval_result = eval('(' + curr['result'] + ')');
var eval_result = JSON.parse(curr['result']);


######################################################################
db.orderinfo.group({
  key:{'pid':1, 'pay_type':1},
  cond: {'state':3},
  reduce: function(curr, result){
    result.total_price += curr.price;
    result.total_count += 1;
    result.total_good_awards_num += eval(curr.good_awards)[0]['num'];
  },
  initial:{
    total_price:0,
    total_good_awards_num: 0,
    total_count:0,

  }
})

db.orderinfo.group({
  key:{'pay_type':1},
  cond: {'state':3},
  reduce: function(curr, result){
    result.total_price += curr.price;
    result.total_count += 1;
    result.total_good_awards_num += eval(curr.good_awards)[0]['num'];
  },
  initial:{
    total_price:0,
    total_good_awards_num: 0,
    total_count:0,

  }
})

db.tablelog.group({
  key: {'room_type': 1},
  initial: {
    total_count: 0,
    total_rid: 0,
    avg_count: 0.0,
    total_num: {},
  },
  reduce: function(curr, result){
    result.total_count += 1;
    var eval_result = eval('('+ curr['result'] +')');
    for(var i in eval_result){
      if(eval_result[i]['rid'] in result.total_num){
        result.total_num[eval_result[i]['rid']] += 1;
      } else {
        result.total_num[eval_result[i]['rid']] = 1;
      }
    }
  },
  finalize: function(reducor){
    for(var i in reducor.total_num){
      reducor.total_rid += 1;
    }
    reducor.avg_count = Math.round(reducor.total_count / reducor.total_rid)*1000/1000;
    delete reducor.total_num;
  }
})




db.orders.mapReduce(
  function() { emit(this.cust_id, this.amount);},         <--------map      2
  function(key, values) { return Array.sum(values)},      <--------reduce   3
  {
    query: {status: 'A'},                                 <--------query    1
    out: 'order_total'                                    <--------output   4
  }
)

MongoDB 时间戳转换
db.orderinfo.find({state: {$eq: 3}}, {'_id':0}).forEach(
  function(a){
    a['create_time'] = (new Date(a['create_time']*1000).toLocaleString().replace(/:\d{1,2}$/,' '));
    a['time_stamp'] = (new Date(a['time_stamp']*1000).toLocaleString().replace(/:\d{1,2}$/,' '));
    printjson(a)
  })


#####################################################

db.friendsngtablecreatelog.aggregate([
  {$group:{_id: "$player_num",total_signup_cost: {$sum: "$signup_cost"}, total_count: {$sum: 1}}}
])




db.friendsngtablecreatelog.group({
  key:{'player_num': 1, 'room_type': 1},
  initial:{
    total_count: 0,
    total_signup_cost: 0,
  },
  reduce: function(curr, result){
    result.total_count += 1;
    result.total_signup_cost += curr.player_num * curr.signup_cost;
  }
})

db.tablecreatelog.group({
  key: {'room_type':1},
  initial: {
    total_count: 0,
  },
  reduce: function(curr, result){
    result.total_count += 1;
  }
})
db.tablecreatelog.count()


db.createmttlog.find({"match_template_id": {"$gte": 100000}}).count()
db.createmttlog.find({"match_template_id": {"$lt": 100000}}).count()
db.createmttlog.count()


