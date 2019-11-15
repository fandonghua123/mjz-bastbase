import requests

url = 'https://qun.qq.com/cgi-bin/qun_mgr/search_group_members'
headers = {'cookie':'RK=rTggxbPIFV; ptcz=a7ec62d09e39033c3e359c141d8c0cc3796cafd8a8cc289261c7177ad5f88808; pgv_pvi=7222388736; pgv_pvid=9425135578; pgv_si=s765401088; _qpsvr_localtk=0.582335416456595; ptisp=cnc; uin=o0285824339; skey=@GZyegV5Ve; p_uin=o0285824339; pt4_token=s0RacDkNy6zZb3RSuQ8x2CR0maGFZZPk-JzYVqxr0ik_; p_skey=UIRk*H0rjZQEb6hjWEv65ytb6BCx1RBUcGAlvUZlwjQ_; traceid=f566a00343; pgv_info=ssid=s6206175220; ts_uid=6111019284; ts_last=qun.qq.com/member.html'}
data = {"gc":613536708,'st':0,'end':10,'sort':0,'bkn':1800537617}
request = requests.post(url, data=data, headers=headers, verify=False)
mems=request.json().get('mems')
for mem in mems:
    name = mem.get('card')
    if name == '':
        name = mem.get("nick")
    qq=mem.get('uin')
    img_url="https://q4.qlogo.cn/g?b=qq&nk='%s'&s=140"%(qq)
    touxiang=requests.get(img_url).content
    with open(name+'.jpeg','wb') as f:
        f.write(touxiang)