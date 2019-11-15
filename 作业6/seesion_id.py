import flask
import json,redis,time,hashlib
import tools

r = redis.Redis(host='118.24.3.40', password='HK139bc&*', port=6379, db=15, decode_responses=True)

server = flask.Flask(__name__)

@server.route('/api',methods=['get'])
def login():
    username = flask.request.values.get('username')
    password = flask.request.values.get('password')
    if username=='' or password=='' :
        d = {'error_code': 0, 'msg': '密码或用户名不能为空'}
        return json.dumps(d, ensure_ascii=False)
    else:
        new_passwd = tools.md5(password)
        sql = 'select username,passwd from app_myuser where username="%s";' % (username)
        result = tools.op_mysql(sql,False)
        if result:
            if new_passwd == result.get('passwd'):
               key_redis = "user_seesions_" + username
               shijian = time.time()
               seesionid = str(shijian) + username
               m = hashlib.md5(seesionid.encode())
               seesionid = m.hexdigest()
               r.set(key_redis,'{"user_name":"%s","passwd":"%s","seesionid":"%s"}' % (username, password,seesionid))
               r.expire(key_redis, 60*30)
               d = {'error_code': 0, 'msg': '登录成功', 'username': username, 'password': new_passwd,'seesionid':seesionid}
               return json.dumps(d, ensure_ascii=False)
            else:
                d = {'error_code': 0, 'msg': '密码或用户名密码错误'}
                return json.dumps(d, ensure_ascii=False)
        else:
            d = {'error_code': 0, 'msg': '用户不存在'}
            return json.dumps(d, ensure_ascii=False)

server.run(port = 8000,debug=True)