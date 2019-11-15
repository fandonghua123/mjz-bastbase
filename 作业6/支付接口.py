import flask,redis
import json,time,hashlib
import tools
r = redis.Redis(host='118.24.3.40', password='HK139bc&*', port=6379, db=15, decode_responses=True)
server = flask.Flask(__name__)
@server.route('/api/login',methods=['get'])
def login():
    username = flask.request.values.get('username')
    password = flask.request.values.get('password')
    if username=='' or password=='' :
        d = {'error_code': 0, 'msg': '密码或用户名不能为空'}
        return json.dumps(d, ensure_ascii=False)
    else:
        new_passwd = tools.md5(password)
        sql = 'select username,passwd from app_myuser where username="%s";'% (username)
        result = tools.op_mysql(sql,False)
        if result:
            if new_passwd == result.get('passwd'):
               shijian = time.time()
               seesionid = str(shijian) + username
               m = hashlib.md5(seesionid.encode())
               seesionid = m.hexdigest()
               key_redis = "user_" + seesionid
               r.set(key_redis,'{"user_name":"%s","passwd":"%s","seesionid":"%s"}' % (username, password,seesionid))
               r.expire(key_redis, 60*60)
               d = {'error_code': 0, 'msg': '登录成功', 'username': username, 'password': new_passwd,'seesionid':seesionid}
               return json.dumps(d, ensure_ascii=False)
            else:
                d = {'error_code': 0, 'msg': '密码或用户名密码错误'}
                return json.dumps(d, ensure_ascii=False)
        else:
            d = {'error_code': 0, 'msg': '用户不存在'}
            return json.dumps(d, ensure_ascii=False)

@server.route('/api/pay', methods=['post','get'])
def pay():
    seesionId = flask.request.values.get('seesionId')
    money= flask.request.values.get('money')
    key_redis = "user_" + seesionId

    if r.exists(key_redis):
        info= r.get(key_redis)
        seesionid_value= eval(info)['seesionid']
        if seesionId == seesionid_value:
            user_name = eval(info)['user_name']
            passwd = eval(info)['passwd']
            if money:
                money1 = is_price(money)
                sql = 'select balance from app_myuser WHERE username="%s";'% (user_name)
                balance = tools.op_mysql(sql)
                b = balance[0]['balance']
                if money1 > b :
                    d = {'error_code': 1, 'msg': '余额不足'}
                    return json.dumps(d, ensure_ascii=False)
                else:
                     yu_e=b- money1
                     d = {'error_code': 1, 'msg': '用户余额为%s'% yu_e}
                     sql2 = "update app_myuser set balance='%s' WHERE username='%s';"%(yu_e,user_name)
                     tools.op_mysql(sql2)
                     return json.dumps(d, ensure_ascii=False)
            else:
                d = {'error_code': 0, 'msg': 'money不能为空',  'username': user_name, 'password':passwd}
                return json.dumps(d, ensure_ascii=False)
    else:
            d = {'error_code': 0, 'msg': '用户信息不一致,请重新登陆'}
            return json.dumps(d, ensure_ascii=False)
def is_price(money):
    if money.isdigit():
        return float(money)
    if money.count('.') == 1:
        left, right = money.split('.')
        if left.isdigit() and right.isdigit():
            return money
    return False
server.run(host='0.0.0.0', port=8000, debug=True)




