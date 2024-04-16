import pymysql
import datetime as dt

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='',
                     database='reviewapp')
 
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
print(db)
date_now= dt.datetime.now().date()
time_now= dt.datetime.now().time()

print(date_now)
print(time_now)
# SQL 插入语句

# state_dict = {'Photoeye': 'OFF', 
#             'Computer': 'ON', 
#             'Poe_Sw': 'ON',
#             'Channel0': 'OFF',
#             'Channel1': 'OFF',
#             'Channel2': 'OFF',
#             'Channel3': 'OFF',
#             'Version':'1.0'
#             }

# user = "{'Photoeye': 'ON', 'Computer': 'OFF', 'Poe_Sw': 'ON','Channel0': 'ON','Channel1': 'OFF', 'Channel2': 'OFF','Channel3': 'OFF','Version':'1.0'}"


user =["{'Photoeye':", "'OFF',", "'Channel3':", "'OFF',", "'Computer':", "'ON',", "'Version':", "'1.0',", "'Poe_Sw':", "'ON',", "'Channel2':", "'OFF',", "'Channel0':", "'OFF',", "'Channel1':", "'OFF'}"]
print(type(user))
user1 = user[0]
print(type(user1))
print(user1)
try:
   
    # for k,v in state_dict.items():
    #     x = k.lower()
    #     y = v
    #     print(x,y)
# 
    # state_dict= exec('c='+user)

    state_dict = eval(user1)

    print(type(state_dict))

    print(f"this is state_dict: {state_dict}")
    
    for k,v in state_dict.items():
        x = k.lower()
        y = v
        print(x,y)

    sql1 = "insert into reviewapp_picomaster (DATE,TIME,photoeye,computer,poe_sw,channel0,channel1,channel2,channel3,version)\
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql1,[date_now,time_now,state_dict['Photoeye'],state_dict['Computer'],state_dict['Poe_Sw'],state_dict['Channel0'],\
            state_dict['Channel1'],state_dict['Channel2'],state_dict['Channel3'],state_dict['Version']])

#     sql2 = "insert into reviewapp_picomaster (DATE,TIME) values(%s,%s)"  
#     cursor.execute(sql2,[date_now,time_now])
# # 


    # sql1 = "insert into reviewapp_manager (DATE,TIME) values(%s,%s)"  
    # cursor.execute(sql1,[date_now,time_now])

   # 执行sql语句
#    cursor.execute(sql1,["Jasper",date_now,time_now])
   # 提交到数据库执行



    db.commit()
    print("insert to DB scuccessfully")
except:
    # 如果发生错误则回滚
    print("mistake occured")
    db.rollback()
 
# 关闭数据库连接
db.close()



# JSON到字典转化：
# ret_dict = simplejson.loads(json_str)
# 字典到JSON转化：
# json_str = simplejson.dumps(dict)


# 1、通过 json 来转换

# >>> import json
# >>> user_info= '{"name" : "john", "gender" : "male", "age": 28}'
# >>> user_dict = json.loads(user_info)
# >>> user_dict
# {u'gender': u'male', u'age': 28, u'name': u'john'}
# 但是使用 json 进行转换存在一个潜在的问题。

# 由于 json 语法规定 数组或对象之中的字符串必须使用双引号，不能使用单引号
# https://blog.csdn.net/HeatDeath/article/details/79370945





# C:\Users\Jasper>mysql -u root -p
# 没有密码
# Enter password:
# Welcome to the MariaDB monitor.  Commands end with ; or \g.
# Your MariaDB connection id is 219
# Server version: 10.4.28-MariaDB mariadb.org binary distribution

# Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.


# 3、通过 literal_eval

# 复制代码
# >>> import ast
# >>> user = '{"name" : "john", "gender" : "male", "age": 28}'
# >>> user_dict = ast.literal_eval(user)
# >>> user_dict
# {'gender': 'male', 'age': 28, 'name': 'john'}
# user_info = "{'name' : 'john', 'gender' : 'male', 'age': 28}"
# >>> user_dict = ast.literal_eval(user)
# >>> user_dict
# {'gender': 'male', 'age': 28, 'name': 'john'}
# 复制代码
# 使用 ast.literal_eval 进行转换既不存在使用 json 进行转换的问题，也不存在使用 eval 进行转换的 安全性问题，因此推荐使用 ast.literal_eval。