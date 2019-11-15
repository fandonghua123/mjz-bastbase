import pymysql,hashlib

def op_mysql(sql,many=True):
    db_info = {'user': 'jxz', 'password': '123456',
            'host': '118.24.3.40', 'db': 'jxz', 'port': 3306, 'charset': 'utf8',
            'autocommit': True}
    conn = pymysql.connect(**db_info)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(sql)
    if many:
        result = cur.fetchall()
    else:
        result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def md5(s,salt=''):
    new_s = str(s) + salt
    m = hashlib.md5(new_s.encode())
    return m.hexdigest()